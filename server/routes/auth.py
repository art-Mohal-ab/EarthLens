from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from models.user import User
from schemas.user import user_register_schema, user_login_schema
from middleware.auth import jwt
from flask_jwt_extended import create_access_token
from database import db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No data provided'}), 400

        validated_data = user_register_schema.load(json_data)

        # Check if user already exists
        if User.find_by_username(validated_data['username']):
            return jsonify({'error': 'Username already exists'}), 400
        if User.find_by_email(validated_data['email']):
            return jsonify({'error': 'Email already registered'}), 400

        # Create new user
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.save()

        # Generate token
        access_token = create_access_token(identity=user.id)

        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'access_token': access_token
        }), 201

    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed', 'message': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No data provided'}), 400

        validated_data = user_login_schema.load(json_data)

        # Find user by username or email
        user = User.find_by_username(validated_data['username_or_email']) or \
               User.find_by_email(validated_data['username_or_email'])

        if not user or not user.check_password(validated_data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401

        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 401

        # Generate token
        access_token = create_access_token(identity=user.id)

        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token
        }), 200

    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400
    except Exception as e:
        return jsonify({'error': 'Login failed', 'message': str(e)}), 500
