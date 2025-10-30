import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from app.database import db
from app.config import get_config


def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    config = get_config(config_name)
    app.config.from_object(config)
    
    # Setup logging
    logging.basicConfig(
        level=getattr(logging, app.config.get('LOG_LEVEL', 'INFO')),
        format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    
    # Setup CORS
    CORS(app, origins=app.config.get('CORS_ORIGINS', ['*']), supports_credentials=True)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Serve uploaded files
    @app.route('/uploads/<path:filename>')
    def serve_upload(filename):
        from flask import send_from_directory
        upload_folder = app.config.get('UPLOAD_FOLDER', os.path.join(os.path.dirname(__file__), '..', 'uploads'))
        return send_from_directory(upload_folder, filename)
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'EarthLens API is running',
            'version': app.config.get('VERSION', '1.0.0'),
            'environment': config_name
        })
    
    @app.route('/')
    def root():
        return jsonify({
            'message': 'Welcome to EarthLens API',
            'version': app.config.get('VERSION', '1.0.0'),
            'endpoints': {
                'health': '/api/health',
                'auth': '/api/auth',
                'reports': '/api/reports',
                'ai': '/api/ai',
                'users': '/api/users'
            }
        })
    
    return app


def register_blueprints(app):
    """Register all blueprints"""
    from app.routes.auth import auth_bp
    from app.routes.reports import reports_bp
    from app.routes.ai import ai_bp
    from app.routes.users import users_bp
    from app.routes.comments import comments_bp
    from app.routes.tags import tags_bp
    from app.routes.profile import profile_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(comments_bp, url_prefix='/api/comments')
    app.register_blueprint(tags_bp, url_prefix='/api/tags')
    app.register_blueprint(profile_bp)


def register_error_handlers(app):
    """Register error handlers"""
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': 'Unauthorized'}), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': 'Forbidden'}), 403
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500