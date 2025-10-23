from flask import Blueprint, request, jsonify, send_from_directory
from marshmallow import ValidationError
from app.middleware.auth import auth_required
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

@reports_bp.route('', methods=['POST'])
@auth_required
def create_report(current_user):
    """Create new environmental report with AI analysis"""
    try:
        # Handle file upload
        image_url = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_folder = 'uploads'
                os.makedirs(upload_folder, exist_ok=True)
                file.save(os.path.join(upload_folder, filename))
                image_url = f"/uploads/{filename}"

        # Get form data
        if request.content_type.startswith('multipart/form-data'):
            data = request.form.to_dict(flat=True)
            if 'tags' in request.form:
                data['tags'] = request.form.getlist('tags')
        else:
            data = request.get_json() or {}

        # Validate input
        validated_data = report_create_schema.load(data)

        # Create report
        report = Report(
            title=validated_data.get('title'),
            description=validated_data.get('description'),
            user_id=current_user.id,
            location=validated_data.get('location'),
            latitude=validated_data.get('latitude'),
            longitude=validated_data.get('longitude'),
            is_public=validated_data.get('is_public', True),
            image_url=image_url
        )

        # Handle tags
        for tag_name in validated_data.get('tags', []):
            report.tags.append(Tag.get_or_create(tag_name))

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

        report.save()  # Save once at the end

        return jsonify({
            'message': 'Report created successfully',
            'report': report.to_dict(include_comments=False)
        }), 201

    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create report', 'message': str(e)}), 500
