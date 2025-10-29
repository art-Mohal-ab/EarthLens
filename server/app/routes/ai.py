from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app.models.report import Report
from app.services.ai_service import AIService
from app.middleware.auth import auth_required

ai_bp = Blueprint('ai', __name__)


@ai_bp.route('/analyze-report/<int:report_id>', methods=['POST'])
@auth_required
def analyze_report(report_id, current_user):
    """Analyze a report with AI"""
    try:
        report = Report.query.get_or_404(report_id)
        
        # Check if user owns this report or if it's public
        if not report.is_public and report.user_id != current_user.id:
            return jsonify({'error': 'Permission denied'}), 403

        ai_service = AIService()
        result = ai_service.analyze_report(report)
        
        if result:
            # Update report with AI analysis
            report.mark_ai_processed(
                category=result.get('category'),
                confidence=result.get('confidence'),
                advice=result.get('advice')
            )
            report.save()
            
            return jsonify({
                'message': 'Report analyzed successfully',
                'analysis': result,
                'report': report.to_dict()
            }), 200
        else:
            return jsonify({'error': 'AI analysis failed'}), 500

    except Exception as e:
        return jsonify({'error': 'Failed to analyze report', 'message': str(e)}), 500


@ai_bp.route('/green-advice', methods=['GET'])
def get_green_advice():
    """Get AI-generated green advice and actions"""
    try:
        category = request.args.get('category', 'general')
        location = request.args.get('location')
        
        ai_service = AIService()
        advice = ai_service.generate_green_advice(category=category, location=location)
        
        return jsonify({
            'advice': advice,
            'category': category,
            'location': location
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to generate advice', 'message': str(e)}), 500


@ai_bp.route('/categorize-text', methods=['POST'])
@auth_required
def categorize_text(current_user):
    """Categorize environmental text using AI"""
    try:
        json_data = request.get_json()
        if not json_data or 'text' not in json_data:
            return jsonify({'error': 'Text is required'}), 400

        text = json_data['text']
        ai_service = AIService()
        result = ai_service.categorize_environmental_issue(text)
        
        return jsonify({
            'text': text,
            'category': result.get('category'),
            'confidence': result.get('confidence'),
            'suggestions': result.get('suggestions', [])
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to categorize text', 'message': str(e)}), 500


@ai_bp.route('/health', methods=['GET'])
def health_check():
    """Health check for AI service"""
    try:
        ai_service = AIService()
        is_healthy = ai_service.health_check()
        
        return jsonify({
            'status': 'healthy' if is_healthy else 'unhealthy',
            'service': 'ai',
            'message': 'AI service is running' if is_healthy else 'AI service unavailable'
        }), 200 if is_healthy else 503

    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'service': 'ai',
            'message': str(e)
        }), 503