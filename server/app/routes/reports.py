from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app.database import db
from app.models.report import Report
from app.models.tag import Tag
from app.schemas.report import ReportCreateSchema, ReportUpdateSchema
from app.middleware.auth import auth_required, optional_auth
from app.services.ai_service import AIService

reports_bp = Blueprint('reports', __name__)

# Initialize schemas
report_create_schema = ReportCreateSchema()
report_update_schema = ReportUpdateSchema()


@reports_bp.route('', methods=['GET'])
@optional_auth
def get_reports(current_user=None):
    """Get all public reports with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        status = request.args.get('status', 'active')
        
        offset = (page - 1) * per_page
        
        reports = Report.get_public_reports(limit=per_page, offset=offset, status=status)
        
        return jsonify({
            'reports': [report.to_dict(include_author=True) for report in reports],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': Report.query.filter_by(is_public=True, status=status).count()
            }
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to get reports', 'message': str(e)}), 500


@reports_bp.route('', methods=['POST'])
@auth_required
def create_report(current_user):
    """Create a new report"""
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate input data
        data = report_create_schema.load(json_data)
        
        # Create new report
        report = Report(
            title=data['title'],
            description=data['description'],
            user_id=current_user.id,
            location=data.get('location'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            image_url=data.get('image_url'),
            is_public=data.get('is_public', True),
            severity=data.get('severity', 'medium')
        )
        
        report.save()
        
        # Add tags if provided
        if 'tags' in data:
            for tag_name in data['tags']:
                tag = Tag.get_or_create(tag_name)
                report.add_tag(tag)
            db.session.commit()
        
        # Process with AI if enabled
        try:
            ai_service = AIService()
            ai_result = ai_service.analyze_report(report)
            if ai_result:
                report.mark_ai_processed(
                    category=ai_result.get('category'),
                    confidence=ai_result.get('confidence'),
                    advice=ai_result.get('advice')
                )
                db.session.commit()
        except Exception as ai_error:
            # AI processing failed, but report creation succeeded
            pass

        return jsonify({
            'message': 'Report created successfully',
            'report': report.to_dict(include_author=True)
        }), 201

    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create report', 'message': str(e)}), 500


@reports_bp.route('/<int:report_id>', methods=['GET'])
@optional_auth
def get_report(report_id, current_user=None):
    """Get a specific report"""
    try:
        report = Report.query.get_or_404(report_id)
        
        # Check if user can view this report
        if not report.is_public and (not current_user or current_user.id != report.user_id):
            return jsonify({'error': 'Report not found'}), 404

        return jsonify({
            'report': report.to_dict(include_author=True, include_comments=True)
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to get report', 'message': str(e)}), 500


@reports_bp.route('/<int:report_id>', methods=['PUT'])
@auth_required
def update_report(report_id, current_user):
    """Update a report"""
    try:
        report = Report.query.get_or_404(report_id)
        
        # Check if user owns this report
        if report.user_id != current_user.id:
            return jsonify({'error': 'Permission denied'}), 403

        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate input data
        data = report_update_schema.load(json_data)
        
        # Update report fields
        for field in ['title', 'description', 'location', 'latitude', 'longitude', 
                     'image_url', 'is_public', 'severity', 'status']:
            if field in data:
                setattr(report, field, data[field])
        
        # Update tags if provided
        if 'tags' in data:
            # Clear existing tags
            report.tags.clear()
            # Add new tags
            for tag_name in data['tags']:
                tag = Tag.get_or_create(tag_name)
                report.add_tag(tag)
        
        report.save()

        return jsonify({
            'message': 'Report updated successfully',
            'report': report.to_dict(include_author=True)
        }), 200

    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update report', 'message': str(e)}), 500


@reports_bp.route('/<int:report_id>', methods=['DELETE'])
@auth_required
def delete_report(report_id, current_user):
    """Delete a report"""
    try:
        report = Report.query.get_or_404(report_id)
        
        # Check if user owns this report
        if report.user_id != current_user.id:
            return jsonify({'error': 'Permission denied'}), 403

        report.delete()

        return jsonify({'message': 'Report deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete report', 'message': str(e)}), 500


@reports_bp.route('/user/<int:user_id>', methods=['GET'])
@optional_auth
def get_user_reports(user_id, current_user=None):
    """Get reports by a specific user"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        
        offset = (page - 1) * per_page
        
        # If viewing own reports, show all; otherwise show only public
        if current_user and current_user.id == user_id:
            reports = Report.get_by_user(user_id, limit=per_page, offset=offset)
            total = Report.query.filter_by(user_id=user_id).count()
        else:
            reports = Report.query.filter_by(user_id=user_id, is_public=True, status='active')\
                                  .order_by(Report.created_at.desc())\
                                  .limit(per_page).offset(offset).all()
            total = Report.query.filter_by(user_id=user_id, is_public=True, status='active').count()

        return jsonify({
            'reports': [report.to_dict(include_author=True) for report in reports],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total
            }
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to get user reports', 'message': str(e)}), 500


@reports_bp.route('/nearby', methods=['GET'])
def get_nearby_reports():
    """Get reports near a location"""
    try:
        latitude = request.args.get('lat', type=float)
        longitude = request.args.get('lng', type=float)
        radius = request.args.get('radius', 10, type=float)
        
        if not latitude or not longitude:
            return jsonify({'error': 'Latitude and longitude are required'}), 400

        reports = Report.get_by_location(latitude, longitude, radius)
        
        return jsonify({
            'reports': [report.to_dict(include_author=True) for report in reports],
            'location': {'latitude': latitude, 'longitude': longitude, 'radius': radius}
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to get nearby reports', 'message': str(e)}), 500