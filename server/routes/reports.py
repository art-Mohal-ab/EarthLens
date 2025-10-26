from flask import Blueprint, request, jsonify, send_from_directory
from marshmallow import ValidationError
from middleware.auth import auth_required
from models.report import Report
from schemas.report import (report_create_schema,report_update_schema,report_schema)
from services.ai_service import ai_service
from database import db
from datetime import datetime
from werkzeug.utils import secure_filename
import os

reports_bp = Blueprint('reports', __name__, url_prefix='/api/reports')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Serve uploaded files
@reports_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)


# ---------------------- CREATE REPORT ----------------------
@reports_bp.route('', methods=['POST'])
@auth_required
def create_report(current_user):
    try:
        image_url = None

        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_folder = 'uploads'
                os.makedirs(upload_folder, exist_ok=True)
                file.save(os.path.join(upload_folder, filename))
                image_url = f"/uploads/{filename}"

        data = request.get_json() or {}
        validated_data = report_create_schema.load(data)

        report = Report(
            title=validated_data.get('title'),
            description=validated_data.get('description'),
            location=validated_data.get('location'),
            latitude=validated_data.get('latitude'),
            longitude=validated_data.get('longitude'),
            user_id=current_user.id,
            is_public=validated_data.get('is_public', True),
            image_url=image_url
        )

        # AI Classification and Advice
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
        return jsonify({'message': 'Report created successfully', 'report': report.to_dict()}), 201

    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create report', 'message': str(e)}), 500


# ---------------------- READ ALL REPORTS ----------------------
@reports_bp.route('', methods=['GET'])
def get_reports():
    try:
        reports = Report.get_public_reports(limit=20)
        return jsonify({
            'reports': [report.to_dict() for report in reports],
            'total': len(reports)
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get reports', 'message': str(e)}), 500


# ---------------------- READ SINGLE REPORT ----------------------
@reports_bp.route('/<int:report_id>', methods=['GET'])
def get_report(report_id):
    try:
        report = Report.query.get(report_id)
        if not report:
            return jsonify({'error': 'Report not found'}), 404
        return jsonify({'report': report.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve report', 'message': str(e)}), 500


# ---------------------- UPDATE REPORT ----------------------
@reports_bp.route('/<int:report_id>', methods=['PUT'])
@auth_required
def update_report(report_id, current_user):
    try:
        report = Report.query.get(report_id)
        if not report:
            return jsonify({'error': 'Report not found'}), 404

        if report.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403

        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No data provided'}), 400

        validated_data = report_update_schema.load(json_data)

        for field, value in validated_data.items():
            setattr(report, field, value)

        report.updated_at = datetime.utcnow()
        report.save()

        return jsonify({'message': 'Report updated successfully', 'report': report.to_dict()}), 200

    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update report', 'message': str(e)}), 500


# ---------------------- DELETE REPORT ----------------------
@reports_bp.route('/<int:report_id>', methods=['DELETE'])
@auth_required
def delete_report(report_id, current_user):
    try:
        report = Report.query.get(report_id)
        if not report:
            return jsonify({'error': 'Report not found'}), 404

        if report.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403

        db.session.delete(report)
        db.session.commit()

        return jsonify({'message': 'Report deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete report', 'message': str(e)}), 500
