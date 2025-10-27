from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from marshmallow import ValidationError
from database import db
from models.user import User
from schemas.user import (user_registration_schema, user_login_schema, user_profile_schema, user_update_schema)
from middleware.auth import auth_required
from utils.security import SecurityUtils

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


# ---------------------- SIGNUP ----------------------
@auth_bp.route('/signup', methods=['POST'])
def signup():
    """Register a new user"""
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate data
        data = user_registration_schema.load(json_data)
        data['email'] = data['email'].lower()

        # Check duplicates
        if User.find_by_email(data['email']):
            return jsonify({'error': 'Email already registered'}), 400
        if User.find_by_username(data['username']):
            return jsonify({'error': 'Username already taken'}), 400

        # Validate password strength
        is_strong, password_message = SecurityUtils.validate_password_strength(data['password'])
        if not is_strong:
            return jsonify({'error': 'Weak password', 'message': password_message}), 400

        # Create and save user
        user = User(**data)
        user.save()

        tokens = user.generate_tokens()

        return jsonify({
            'message': 'User registered successfully',
            'user': user_profile_schema.dump(user.to_dict(include_sensitive=True)),
            'token': tokens['access_token'],
            'refresh_token': tokens['refresh_token']
        }), 201

    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed', 'message': str(e)}), 500


# ---------------------- LOGIN ----------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return JWT token"""
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No data provided'}), 400

        data = user_login_schema.load(json_data)
        email = data['email'].lower()

        user = User.find_by_email(email)
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401

        if not user.is_active:
            return jsonify({'error': 'Account disabled'}), 403

        tokens = user.generate_tokens()

        return jsonify({
            'message': 'Login successful',
            'user': user_profile_schema.dump(user.to_dict(include_sensitive=True)),
            'token': tokens['access_token'],
            'refresh_token': tokens['refresh_token']
        }), 200

    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    except Exception as e:
        return jsonify({'error': 'Login failed', 'message': str(e)}), 500


# ---------------------- GET PROFILE ----------------------
@auth_bp.route('/me', methods=['GET'])
@auth_required
def get_current_user(current_user):
    """Get current user profile"""
    try:
        return jsonify({
            'user': user_profile_schema.dump(current_user.to_dict(include_sensitive=True))
        }), 200
    except Exception:
        return jsonify({'error': 'Failed to retrieve user profile'}), 500


# ---------------------- UPDATE PROFILE ----------------------
@auth_bp.route('/me', methods=['PUT'])
@auth_required
def update_profile(current_user):
    """Update current user profile"""
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No data provided'}), 400

        data = user_update_schema.load(json_data)

        # Username update
        if 'username' in data and data['username'] != current_user.username:
            if User.find_by_username(data['username']):
                return jsonify({'error': 'Username already taken'}), 400
            current_user.username = data['username']

        # Email update
        if 'email' in data and data['email'].lower() != current_user.email:
            if User.find_by_email(data['email'].lower()):
                return jsonify({'error': 'Email already registered'}), 400
            current_user.email = data['email'].lower()

        # Password change
        if 'new_password' in data:
            if 'current_password' not in data:
                return jsonify({'error': 'Current password required'}), 400
            if not current_user.check_password(data['current_password']):
                return jsonify({'error': 'Current password incorrect'}), 400

            is_strong, message = SecurityUtils.validate_password_strength(data['new_password'])
            if not is_strong:
                return jsonify({'error': 'Weak password', 'message': message}), 400

            current_user.set_password(data['new_password'])

        current_user.save()

        return jsonify({
            'message': 'Profile updated successfully',
            'user': user_profile_schema.dump(current_user.to_dict(include_sensitive=True))
        }), 200

    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update profile', 'message': str(e)}), 500


# ---------------------- REFRESH TOKEN ----------------------
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    """Refresh JWT access token"""
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)

        if not user or not user.is_active:
            return jsonify({'error': 'Invalid refresh token'}), 401

        new_token = create_access_token(identity=user.id)
        return jsonify({'message': 'Token refreshed successfully', 'token': new_token}), 200

    except Exception as e:
        return jsonify({'error': 'Failed to refresh token', 'message': str(e)}), 500


# ---------------------- LOGOUT ----------------------
@auth_bp.route('/logout', methods=['POST'])
@auth_required
def logout(current_user):
    """Logout user (client-side token removal)"""
    return jsonify({'message': 'Logged out successfully'}), 200


# ---------------------- HEALTH CHECK ----------------------
@auth_bp.route('/health', methods=['GET'])
def health_check():
    """Health check for auth service"""
    return jsonify({
        'status': 'healthy',
        'service': 'auth',
        'message': 'Authentication service is running'
    }), 200
