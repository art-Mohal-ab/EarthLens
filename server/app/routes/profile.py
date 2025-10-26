from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from middleware.auth import auth_required
from models.user import User
from models.report import Report
from models.comment import Comment
from schemas.user import user_update_schema
from database import db
from sqlalchemy import func

profile_bp = Blueprint('profile', __name__, url_prefix='/api/profile')


@profile_bp.route('', methods=['GET'])
@auth_required
def get_profile(current_user):
    """Get user's profile, impact, and activity summary"""
    try:
        # Basic stats
        reports_count = Report.query.filter_by(user_id=current_user.id).count()
        comments_count = Comment.query.filter_by(user_id=current_user.id).count()
        public_reports_count = Report.query.filter_by(user_id=current_user.id, is_public=True).count()

        # Top category (most reported AI classification)
        top_category = (
            db.session.query(Report.ai_category, func.count(Report.id).label('count'))
            .filter(Report.user_id == current_user.id, Report.ai_category.isnot(None))
            .group_by(Report.ai_category)
            .order_by(func.count(Report.id).desc())
            .first()
        )
        top_category_name = top_category[0] if top_category else None

        # Recent activity
        recent_reports = (
            Report.query.filter_by(user_id=current_user.id)
            .order_by(Report.created_at.desc())
            .limit(3)
            .all()
        )
        recent_comments = (
            Comment.query.filter_by(user_id=current_user.id)
            .order_by(Comment.created_at.desc())
            .limit(3)
            .all()
        )

        # Combine into profile response
        profile_data = current_user.to_dict(include_sensitive=True)
        profile_data.update({
            'impact': {
                'reports_submitted': reports_count,
                'comments_made': comments_count,
                'public_reports': public_reports_count
            },
            'top_category': top_category_name,
            'recent_activity': {
                'reports': [r.to_dict(include_comments=False, include_tags=False) for r in recent_reports],
                'comments': [c.to_dict(include_replies=False) for c in recent_comments]
            }
        })

        return jsonify({'profile': profile_data}), 200

    except Exception as e:
        return jsonify({'error': 'Failed to retrieve profile', 'message': str(e)}), 500


@profile_bp.route('', methods=['PUT'])
@auth_required
def update_profile(current_user):
    """Update user's profile (username, email, password)"""
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No data provided'}), 400

        try:
            validated_data = user_update_schema.load(json_data)
        except ValidationError as err:
            return jsonify({'error': 'Validation failed', 'details': err.messages}), 400

        # Username update
        if 'username' in validated_data and validated_data['username'] != current_user.username:
            if User.find_by_username(validated_data['username']):
                return jsonify({'error': 'Username already in use'}), 400
            current_user.username = validated_data['username']

        # Email update
        if 'email' in validated_data and validated_data['email'] != current_user.email:
            if User.find_by_email(validated_data['email']):
                return jsonify({'error': 'Email already registered'}), 400
            current_user.email = validated_data['email'].lower()

        # Password update
        if 'new_password' in validated_data:
            if 'current_password' not in validated_data:
                return jsonify({'error': 'Current password required'}), 400
            if not current_user.check_password(validated_data['current_password']):
                return jsonify({'error': 'Invalid current password'}), 400
            current_user.set_password(validated_data['new_password'])

        current_user.save()
        return jsonify({
            'message': 'Profile updated successfully',
            'profile': current_user.to_dict(include_sensitive=True)
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update profile', 'message': str(e)}), 500


@profile_bp.route('/activity', methods=['GET'])
@auth_required
def get_profile_activity(current_user):
    """Get user's recent reports and comments"""
    try:
        limit = min(int(request.args.get('limit', 10)), 50)
        activity_type = request.args.get('type', 'all')
        activities = []

        if activity_type in ['all', 'reports']:
            reports = (
                Report.query.filter_by(user_id=current_user.id)
                .order_by(Report.created_at.desc())
                .limit(limit)
                .all()
            )
            for report in reports:
                activities.append({
                    'type': 'report',
                    'id': report.id,
                    'title': report.title,
                    'created_at': report.created_at.isoformat()
                })

        if activity_type in ['all', 'comments']:
            comments = (
                Comment.query.filter_by(user_id=current_user.id)
                .order_by(Comment.created_at.desc())
                .limit(limit)
                .all()
            )
            for comment in comments:
                activities.append({
                    'type': 'comment',
                    'id': comment.id,
                    'content': comment.content[:100] + '...' if len(comment.content) > 100 else comment.content,
                    'created_at': comment.created_at.isoformat(),
                    'report_id': comment.report_id
                })

        activities.sort(key=lambda x: x['created_at'], reverse=True)
        return jsonify({'activities': activities[:limit]}), 200

    except Exception as e:
        return jsonify({'error': 'Failed to retrieve activity', 'message': str(e)}), 500