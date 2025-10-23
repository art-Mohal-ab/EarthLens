import os
from flask import Flask
from flask_cors import CORS
from database import init_db

def create_app(config_name=None):
    """Factory function for AI/report backend"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(f'config.{config_name.capitalize()}Config')

    CORS(app, origins=app.config.get('CORS_ORIGINS', '*'))

    init_db(app)

    # Register only your AI/report routes
    from app.routes.report import reports_bp
    from app.routes.ai import ai_bp

    app.register_blueprint(reports_bp)
    app.register_blueprint(ai_bp)

    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return {"status": "healthy", "message": "EarthLens AI backend running"}

    # Root endpoint
    @app.route('/')
    def root():
        return {
            "message": "Welcome to EarthLens AI backend",
            "version": "1.0.0",
            "endpoints": {
                "reports": "/api/reports",
                "ai": "/api/ai",
                "health": "/api/health"
            }
        }

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5001)) 
    debug = os.environ.get('FLASK_ENV') == 'development'
    print(f"Starting AI backend on port {port}, debug={debug}")
    app.run(host="0.0.0.0", port=port, debug=debug)
