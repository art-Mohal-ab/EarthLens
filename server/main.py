import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from database import db, init_db


def create_app(config_name=None):
    app = Flask(__name__)

    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    config_module = f"config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)

    logging.basicConfig(
        level=app.config.get("LOG_LEVEL", "INFO"),
        format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
    )

    CORS(app, origins=app.config.get("CORS_ORIGINS", ["*"]))

    init_db(app)
    migrate = Migrate(app, db)
    try:
        from app.routes.report import reports_bp
        app.register_blueprint(reports_bp)
    except ImportError as e:
        app.logger.warning(f"Failed to load reports blueprint: {e}")

    try:
        from app.routes.auth import auth_bp
        app.register_blueprint(auth_bp)
    except ImportError as e:
        app.logger.warning(f"Failed to load auth blueprint: {e}")

    try:
        from app.routes.ai import ai_bp
        app.register_blueprint(ai_bp)
    except ImportError as e:
        app.logger.warning(f"Failed to load ai blueprint: {e}")

    @app.route("/api/health")
    def health_check():
        return jsonify({
            "status": "healthy",
            "message": "EarthLens AI backend running",
            "environment": config_name
        }), 200

    @app.route("/")
    def root():
        return jsonify({
            "message": " Welcome to EarthLens AI Backend",
            "version": "1.0.0",
            "available_endpoints": {
                "reports": "/api/reports",
                "ai": "/api/ai",
                "health": "/api/health"
            }
        }), 200

    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    debug = True

    print(f"Starting EarthLens AI backend on port {port} (debug={debug})")

    app = create_app()
    app.run(host="0.0.0.0", port=port, debug=debug)
