from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.middleware.auth import auth_required
from app.services.ai_service import ai_service
from app.models.report import Report
from database import db
from datetime import datetime
import logging

ai_bp = Blueprint("ai", __name__, url_prefix="/api/ai")
logger = logging.getLogger(__name__)

@ai_bp.route('', methods=['GET'])
def ai_info():
    """Get AI service information"""
    return jsonify({
        'message': 'EarthLens AI Service',
        'endpoints': {
            'analyze': '/api/ai/analyze',
            'green-advice': '/api/ai/green-advice',
            'categories': '/api/ai/categories'
        }
    }), 200

@ai_bp.route("/analyze", methods=["POST"])
@auth_required
def analyze_report(current_user):
    """
    Analyze an environmental report using AI.
    - Classifies the issue
    - Generates tailored advice
    - Optionally updates the corresponding report in the database
    """
    try:
        json_data = request.get_json(silent=True)
        if not json_data:
            return jsonify({
                "error": "No data provided",
                "message": "Request body must contain JSON data."
            }), 400

        title = json_data.get("title", "").strip()
        description = json_data.get("description", "").strip()
        location = json_data.get("location")
        image_url = json_data.get("image_url")
        report_id = json_data.get("report_id")

        if not title or not description:
            return jsonify({
                "error": "Missing required fields",
                "message": "Both 'title' and 'description' are required."
            }), 400

        # AI Classification 
        classification = ai_service.classify_environmental_issue(
            title=title,
            description=description,
            image_url=image_url
        )

        # AI Advice Generation 
        advice = ai_service.generate_advice(
            category=classification.get("category", "environmental-issue"),
            title=title,
            description=description,
            location=location
        )

        # Save results to the database if report_id is provided 
        if report_id:
            report = Report.query.filter_by(id=report_id, user_id=current_user.id).first()
            if report:
                report.ai_category = classification.get("category")
                report.ai_confidence = classification.get("confidence")
                report.ai_advice = advice
                report.ai_processed = True
                report.ai_processed_at = datetime.utcnow()
                db.session.commit()
            else:
                logger.warning(f"Report with ID {report_id} not found for user {current_user.id}")

        # Return response 
        return jsonify({
            "message": "Analysis completed successfully",
            "analysis": {
                "category": classification.get("category"),
                "confidence": classification.get("confidence"),
                "advice": advice,
                "processed_at": datetime.utcnow().isoformat(),
                "saved_to_report": bool(report_id)
            }
        }), 200

    except ValidationError as ve:
        logger.warning(f"Validation error during AI analysis: {ve}")
        return jsonify({
            "error": "Validation error",
            "message": str(ve)
        }), 400

    except Exception as e:
        logger.error(f"AI analysis failed: {e}")
        return jsonify({
            "error": "Analysis failed",
            "message": "An error occurred during AI analysis. Please try again later."
        }), 500


@ai_bp.route("/green-advice", methods=["GET"])
@auth_required
def get_green_advice(current_user):
    """
    Retrieve personalized green actions and sustainability tips.
    - Optionally filtered by location or interests
    """
    try:
        location = request.args.get("location")
        interests = request.args.getlist("interests")

        actions = ai_service.get_green_actions(
            user_location=location,
            interests=interests
        )

        return jsonify({
            "message": "Green actions retrieved successfully",
            "actions": actions
        }), 200

    except Exception as e:
        logger.error(f"Failed to generate green advice: {e}")
        return jsonify({
            "error": "Failed to get green advice",
            "message": "An error occurred while generating recommendations."
        }), 500


@ai_bp.route("/categories", methods=["GET"])
def get_categories():
    """
    Return a list of supported environmental categories.
    """
    categories = [
        {"name": "pollution", "description": "Environmental pollution issues"},
        {"name": "climate-change", "description": "Climate change and global warming concerns"},
        {"name": "deforestation", "description": "Forest degradation and habitat loss"},
        {"name": "water-issues", "description": "Water scarcity, flooding, and contamination"},
        {"name": "air-quality", "description": "Air pollution and emissions concerns"},
        {"name": "wildlife", "description": "Biodiversity and wildlife conservation"},
        {"name": "environmental-issue", "description": "Other general environmental problems"}
    ]

    return jsonify({
        "message": "Categories retrieved successfully",
        "categories": categories
    }), 200
