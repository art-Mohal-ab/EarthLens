from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app.database import db
from app.models.comment import Comment
from app.models.report import Report
from app.schemas.comment import CommentCreateSchema, CommentUpdateSchema
from app.middleware.auth import auth_required

comments_bp = Blueprint('comments', __name__)

# Initialize schemas
comment_create_schema = CommentCreateSchema()
comment_update_schema = CommentUpdateSchema()


@comments_bp.route('', methods=['POST'])
@auth_required
def create_comment(current_user):
    """Create a new comment"""
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate input data
        data = comment_create_schema.load(json_data)
        
        # Check if report exists and is accessible
        report = Report.query.get_or_404(data['report_id'])
        if not report.is_public and report.user_id != current_user.id:
            return jsonify({'error': 'Report not found'}), 404
        
        # Check if parent comment exists (for replies)
        if data.get('parent_id'):
            parent_comment = Comment.query.get_or_404(data['parent_id'])
            if parent_comment.report_id != data['report_id']:
                return jsonify({'error': 'Parent comment not in same report'}), 400

        # Create comment
        comment = Comment(
            content=data['content'],
            user_id=current_user.id,
            report_id=data['report_id'],
            parent_id=data.get('parent_id')
        )
        comment.save()

        return jsonify({
            'message': 'Comment created successfully',
            'comment': comment.to_dict(include_author=True)
        }), 201

    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create comment', 'message': str(e)}), 500


@comments_bp.route('/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    """Get a specific comment"""
    try:
        comment = Comment.query.get_or_404(comment_id)
        
        return jsonify({
            'comment': comment.to_dict(include_author=True, include_replies=True)
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to get comment', 'message': str(e)}), 500


@comments_bp.route('/<int:comment_id>', methods=['PUT'])
@auth_required
def update_comment(comment_id, current_user):
    """Update a comment"""
    try:
        comment = Comment.query.get_or_404(comment_id)
        
        # Check if user owns this comment
        if comment.user_id != current_user.id:
            return jsonify({'error': 'Permission denied'}), 403

        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate input data
        data = comment_update_schema.load(json_data)
        
        # Update comment
        comment.edit_content(data['content'])

        return jsonify({
            'message': 'Comment updated successfully',
            'comment': comment.to_dict(include_author=True)
        }), 200

    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update comment', 'message': str(e)}), 500


@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@auth_required
def delete_comment(comment_id, current_user):
    """Delete a comment"""
    try:
        comment = Comment.query.get_or_404(comment_id)
        
        # Check if user owns this comment
        if comment.user_id != current_user.id:
            return jsonify({'error': 'Permission denied'}), 403

        comment.delete()

        return jsonify({'message': 'Comment deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete comment', 'message': str(e)}), 500


@comments_bp.route('/report/<int:report_id>', methods=['GET'])
def get_report_comments(report_id):
    """Get all comments for a report"""
    try:
        report = Report.query.get_or_404(report_id)
        
        # Only show comments for public reports or if user owns the report
        if not report.is_public:
            return jsonify({'error': 'Report not found'}), 404

        include_replies = request.args.get('include_replies', 'true').lower() == 'true'
        comments = Comment.get_by_report(report_id, include_replies=include_replies)
        
        return jsonify({
            'comments': [comment.to_dict(include_author=True, include_replies=include_replies) 
                        for comment in comments],
            'report_id': report_id,
            'total_comments': report.comments.count()
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to get comments', 'message': str(e)}), 500