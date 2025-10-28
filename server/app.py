from flask import Flask, jsonify
from flask_cors import CORS
from database.db import db
from config import Config
from routes.auth import auth_bp
from routes.reports import reports_bp
from routes.comments import comments_bp
from routes.profile import profile_bp
from routes.tags import tags_bp

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(comments_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(tags_bp)

@app.route('/')
def home():
    return jsonify({'message': 'EarthLens API is running!', 'status': 'success'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
