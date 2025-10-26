from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from functools import wraps
from flask import request, jsonify
from models.user import User

jwt = JWTManager()

def auth_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        return fn(current_user, *args, **kwargs)
    return wrapper

def optional_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id) if current_user_id else None
        except:
            current_user = None
        return fn(current_user, *args, **kwargs)
    return wrapper
