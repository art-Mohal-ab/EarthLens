from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session
from database import SessionLocal, create_tables
from models.user import User
import jwt
from datetime import datetime, timedelta

create_tables()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

CORS(app, origins=["*"], allow_headers=["Content-Type"], methods=["GET", "POST", "OPTIONS"])

def get_db():
    return SessionLocal()

def create_access_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

@app.route('/')
def root():
    return jsonify({"message": "EarthLens API is running"})

@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy", "message": "EarthLens backend running"})

@app.route('/api/auth/signup', methods=['GET'])
def signup_get():
    return jsonify({"message": "Use POST method for signup", "methods": ["POST"]})

@app.route('/api/auth/login', methods=['GET'])
def login_get():
    return jsonify({"message": "Use POST method for login", "methods": ["POST"]})

@app.route('/test')
def test():
    return jsonify({"message": "Test route working"})

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        if not all([name, email, password]):
            return jsonify({"error": "Missing required fields"}), 400
        
        db = get_db()
        
        try:
            existing_user = db.query(User).filter(User.email == email).first()
            if existing_user:
                return jsonify({"error": "Email already registered"}), 409
            
            new_user = User(name=name, email=email)
            new_user.set_password(password)
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        finally:
            db.close()
        
        access_token = create_access_token(new_user.id)
        
        return jsonify({
            "message": "User registered successfully",
            "user": {"id": new_user.id, "name": new_user.name, "email": new_user.email},
            "access_token": access_token,
            "token_type": "bearer"
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        if not all([email, password]):
            return jsonify({"error": "Missing email or password"}), 400
        
        db = get_db()
        
        try:
            user = db.query(User).filter(User.email == email).first()
            if not user or not user.check_password(password):
                return jsonify({"error": "Invalid email or password"}), 401
        finally:
            db.close()
        
        access_token = create_access_token(user.id)
        
        return jsonify({
            "message": "Login successful",
            "user": {"id": user.id, "name": user.name, "email": user.email},
            "access_token": access_token,
            "token_type": "bearer"
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
Meets