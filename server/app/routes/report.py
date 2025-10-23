from flask import Blueprint, request, jsonify, send_from_directory
from marshmallow import ValidationError
from middleware.auth import auth_required, optional_auth
from models.report import Report
from models.tag import Tag
from app.schemas.report import report_create_schema, report_update_schema, report_schema, report_filter_schema
from services.ai_service import ai_service
from database import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename

reports_bp = Blueprint('reports', __name__, url_prefix='/api/reports')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Serve uploaded files
@reports_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

@reports_bp.route('', methods=['GET'])
@optional_auth
def get_reports(current_user):
    """Get reports with filtering and pagination"""
    try:
        try:
            filters = report_filter_schema.load(request.args) # Validate and deserialize input
        except ValidationError as err:
            return jsonify({
                'error': 'Invalid filters',
                'details': err.messages
            }), 400

        query = Report.query
        
        # Application of filters
        if filters.get('category'):
            query = query.filter(Report.ai_category == filters['category'])
        if filters.get('location'):
            query = query.filter(Report.location.ilike(f"%{filters['location']}%"))
        if filters.get('author_id'):
            query = query.filter(Report.user_id == filters['author_id'])
        if filters.get('status'):
            query = query.filter(Report.status == filters['status'])
        else:
            query = query.filter(Report.status == 'active')
        if not current_user or filters.get('author_id') != current_user.id:
            query = query.filter(Report.is_public == True) # for other users, only public reports
        if filters.get('tags'):
            query = query.join(Report.tags).filter(Tag.name.in_(filters['tags']))
        
        # Validate sort_by column
        if not hasattr(Report, filters['sort_by']):
            return jsonify({'error': f"Invalid sort_by field: {filters['sort_by']}"}), 400

        sort_column = getattr(Report, filters['sort_by'])
        if filters['sort_order'] == 'desc':
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
        
        total = query.count()
        reports = query.offset(filters['offset']).limit(filters['limit']).all()
        
        return jsonify({
            'reports': [report.to_dict(include_comments=False) for report in reports],
            'pagination': {
                'total': total,
                'limit': filters['limit'],
                'offset': filters['offset'],
                'has_more': total > (filters['offset'] + filters['limit'])
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve reports',
            'message': str(e)
        }), 500


@reports_bp.route('', methods=['POST'])
@auth_required
def create_report(current_user):
    """Create new environmental report"""
    try:
        # Handle file upload if present
        image_url = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # upload to cloud storage
                upload_folder = 'uploads'
                os.makedirs(upload_folder, exist_ok=True)
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                image_url = f"/uploads/{filename}"
        
        # Get form data
        if request.content_type.startswith('multipart/form-data'):
            data = dict(request.form)
            if 'tags' in request.form:
                data['tags'] = request.form.getlist('tags')
        else:
            data = request.get_json() or {}
        
        try:
            validated_data = report_create_schema.load(data) # validate and deserialize input
        except ValidationError as err:
            return jsonify({
                'error': 'Validation failed',
                'details': err.messages
            }), 400
        
        # Create report
        report = Report(
            title=validated_data['title'],
            description=validated_data['description'],
            user_id=current_user.id,
            location=validated_data.get('location'),
            latitude=validated_data.get('latitude'),
            longitude=validated_data.get('longitude')
        )
        
        report.image_url = image_url
        report.is_public = validated_data.get('is_public', True)
        report.save()
        
        # Handle tags
        tag_names = validated_data.get('tags', []) 
        for tag_name in tag_names:
            tag = Tag.get_or_create(tag_name)
            report.tags.append(tag)
        
        # AI Analysis
        try:
            classification = ai_service.classify_environmental_issue(
                title=report.title,
                description=report.description,
                image_url=report.image_url
            )
            
            advice = ai_service.generate_advice(
                category=classification['category'],
                title=report.title,
                description=report.description,
                location=report.location
            )
            
            report.ai_category = classification['category']
            report.ai_confidence = classification['confidence']
            report.ai_advice = advice
            report.ai_processed = True
            report.ai_processed_at = datetime.utcnow()
            
        except Exception as ai_error:
            print(f"AI processing failed: {ai_error}")
        
        report.save()
        
        return jsonify({
            'message': 'Report created successfully',
            'report': report.to_dict(include_comments=False)
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to create report',
            'message': str(e)
        }), 500

@reports_bp.route('/<int:report_id>', methods=['GET'])
@optional_auth
def get_report(report_id, current_user):
    """Get specific report by ID"""
    try:
        report = Report.query.get(report_id)
        
        if not report:
            return jsonify({
                'error': 'Report not found',
                'message': 'The requested report does not exist'
            }), 404
    
        if not report.is_public and (not current_user or current_user.id != report.user_id):
            return jsonify({
                'error': 'Access denied',
                'message': 'This report is private'
            }), 403
        
        return jsonify({
            'report': report.to_dict(include_comments=True)
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve report',
            'message': str(e)
        }), 500

@reports_bp.route('/<int:report_id>', methods=['PUT'])
@auth_required
def update_report(report_id, current_user):
    """Update report (only by owner)"""
    try:
        report = Report.query.get(report_id)
        
        if not report:
            return jsonify({
                'error': 'Report not found',
                'message': 'The requested report does not exist'
            }), 404
        
        if report.user_id != current_user.id:
            return jsonify({
                'error': 'Access denied',
                'message': 'You can only edit your own reports'
            }), 403
        
        json_data = request.get_json()
        if not json_data:
            return jsonify({
                'error': 'No data provided',
                'message': 'Request body must contain JSON data'
            }), 400
        
        try:
            validated_data = report_update_schema.load(json_data)
        except ValidationError as err:
            return jsonify({
                'error': 'Validation failed',
                'details': err.messages
            }), 400
        
        # Update fields
        for field, value in validated_data.items():
            if field == 'tags':
                report.tags.clear()
                for tag_name in value:
                    tag = Tag.get_or_create(tag_name)
                    report.tags.append(tag)
            else:
                setattr(report, field, value)
        
        report.save()
        
        return jsonify({
            'message': 'Report updated successfully',
            'report': report.to_dict(include_comments=False)
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to update report',
            'message': str(e)
        }), 500

@reports_bp.route('/<int:report_id>', methods=['DELETE'])
@auth_required
def delete_report(report_id, current_user):
    """Delete report (only by owner)"""
    try:
        report = Report.query.get(report_id)
        
        if not report:
            return jsonify({
                'error': 'Report not found',
                'message': 'The requested report does not exist'
            }), 404
        
        if report.user_id != current_user.id:
            return jsonify({
                'error': 'Access denied',
                'message': 'You can only delete your own reports'
            }), 403
        
        report.status = 'deleted'
        report.save()
        
        return jsonify({
            'message': 'Report deleted successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to delete report',
            'message': str(e)
        }), 500

@reports_bp.route('/my', methods=['GET'])
@auth_required
def get_my_reports(current_user):
    """Get current user's reports"""
    try:
        limit = min(int(request.args.get('limit', 20)), 100)
        offset = max(int(request.args.get('offset', 0)), 0)
        
        reports = Report.get_user_reports(current_user.id, limit=limit, offset=offset)
        total = Report.query.filter_by(user_id=current_user.id).count()
        
        return jsonify({
            'reports': [report.to_dict(include_comments=False) for report in reports],
            'pagination': {
                'total': total,
                'limit': limit,
                'offset': offset,
                'has_more': total > (offset + limit)
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve your reports',
            'message': str(e)
        }), 500