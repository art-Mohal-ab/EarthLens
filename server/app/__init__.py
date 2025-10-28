from flask import Flask
from flask_cors import CORS
from server.config import Config
from server.database import db, bcrypt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    
    db.init_app(app)
    bcrypt.init_app(app)
    CORS(app)  

    from server.app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    @app.route("/")
    def home():
        return {"message": "EarthLens backend running!"}

    return app
