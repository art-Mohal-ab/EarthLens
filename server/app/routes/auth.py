from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from marshmallow import ValidationError
from app.database import db
from app.models.user import User
from app.schemas.user import UserRegistrationSchema, UserLoginSchema, UserUpdateSchema
from app.middleware.auth import auth_required
from app.utils.security import SecurityUtils

auth_bp = Blueprint('auth', __name__)

# Initialize schemas
user_registration_schema = UserRegistrationSchema()
user_login_schema = UserLoginSchema()
user_update_schema = UserUpdateSchema()


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate input data
        data = user_registration_schema.load(json_data)

        # Check if user already exists
        if User.find_by_email(data['email']):
            return jsonify({'error': 'Email already registered'}), 400

        if User.find_by_username(data['username']):
            return jsonify({'error': 'Username already taken'}), 400

        # Create new user
        user = User(
            username=data['username'],
            email=data['email'].lower(),
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )
        user.set_password(data['password'])
        user.save()

        # Generate tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(include_email=True),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201

    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed', 'message': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate input data
        data = user_login_schema.load(json_data)

        # Find user by email or username
        user = User.find_by_email(data['email']) or User.find_by_username(data['email'])

        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401

        if not user.is_active:
            return jsonify({'error': 'Account is disabled'}), 403

        # Generate tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(include_email=True),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200

    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    except Exception as e:
        return jsonify({'error': 'Login failed', 'message': str(e)}), 500


@auth_bp.route('/me', methods=['GET'])
@auth_required
def get_profile(current_user):
    """Get current user profile"""
    try:
        return jsonify({
            'user': current_user.to_dict(include_email=True)
        }), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get profile', 'message': str(e)}), 500


@auth_bp.route('/me', methods=['PUT'])
@auth_required
def update_profile(current_user):
    """Update current user profile"""
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate input data
        data = user_update_schema.load(json_data)

        # Check for username conflicts
        if 'username' in data and data['username'] != current_user.username:
            if User.find_by_username(data['username']):
                return jsonify({'error': 'Username already taken'}), 400

        # Check for email conflicts
        if 'email' in data and data['email'].lower() != current_user.email:
            if User.find_by_email(data['email']):
                return jsonify({'error': 'Email already registered'}), 400

        # Update user fields
        for field in ['username', 'first_name', 'last_name', 'bio']:
            if field in data:
                setattr(current_user, field, data[field])

        if 'email' in data:
            current_user.email = data['email'].lower()

        # Handle password change
        if 'new_password' in data:
            if not data.get('current_password'):
                return jsonify({'error': 'Current password required'}), 400

            if not current_user.check_password(data['current_password']):
                return jsonify({'error': 'Current password is incorrect'}), 401

            current_user.set_password(data['new_password'])

        current_user.save()

        return jsonify({
            'message': 'Profile updated successfully',
            'user': current_user.to_dict(include_email=True)
        }), 200

    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update profile', 'message': str(e)}), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user or not user.is_active:
            return jsonify({'error': 'Invalid refresh token'}), 401

        access_token = create_access_token(identity=user.id)

        return jsonify({
            'message': 'Token refreshed successfully',
            'access_token': access_token
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to refresh token', 'message': str(e)}), 500


@auth_bp.route('/logout', methods=['POST'])
@auth_required
def logout(current_user):
    """Logout user (client should discard tokens)"""
    return jsonify({'message': 'Logged out successfully'}), 200
