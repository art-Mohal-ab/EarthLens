from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from app.models.user import User


def auth_required(f):
    """Decorator that requires authentication"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        try:
            current_user_id = int(get_jwt_identity())
            current_user = User.query.get(current_user_id)
            
            if not current_user or not current_user.is_active:
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            return f(current_user=current_user, *args, **kwargs)
        
        except Exception as e:
            return jsonify({'error': 'Authentication failed', 'message': str(e)}), 401
    
    return decorated_function


def optional_auth(f):
    """Decorator that allows optional authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Try to verify JWT token
            verify_jwt_in_request(optional=True)
            current_user_id = get_jwt_identity()

            current_user = None
            if current_user_id:
                current_user = User.query.get(int(current_user_id))
                if not current_user or not current_user.is_active:
                    current_user = None
            
            return f(current_user=current_user, *args, **kwargs)
        
        except Exception:
            # If JWT verification fails, continue without authentication
            return f(current_user=None, *args, **kwargs)
    
    return decorated_function