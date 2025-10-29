from flask import Blueprint, request, jsonify

from app.models.user import User
from app.middleware.auth import auth_required, optional_auth

users_bp = Blueprint('users', __name__)


@users_bp.route('/<int:user_id>', methods=['GET'])
@optional_auth
def get_user(user_id, current_user=None):
    """Get user profile"""
    try:
        user = User.query.get_or_404(user_id)
        
        # Include email only if viewing own profile
        include_email = current_user and current_user.id == user_id
        
        return jsonify({
            'user': user.to_dict(include_email=include_email)
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to get user', 'message': str(e)}), 500


@users_bp.route('', methods=['GET'])
def get_users():
    """Get list of users with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        search = request.args.get('search', '')
        
        query = User.query.filter(User.is_active == True)
        
        if search:
            query = query.filter(
                User.username.contains(search) |
                User.first_name.contains(search) |
                User.last_name.contains(search)
            )
        
        users = query.order_by(User.created_at.desc())\
                    .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'users': [user.to_dict() for user in users.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': users.total,
                'pages': users.pages
            }
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to get users', 'message': str(e)}), 500


@users_bp.route('/search', methods=['GET'])
def search_users():
    """Search users by username or name"""
    try:
        query = request.args.get('q', '').strip()
        limit = min(request.args.get('limit', 10, type=int), 50)
        
        if not query:
            return jsonify({'users': []}), 200
        
        users = User.query.filter(
            (User.username.contains(query) |
             User.first_name.contains(query) |
             User.last_name.contains(query)) &
            (User.is_active == True)
        ).limit(limit).all()
        
        return jsonify({
            'users': [user.to_dict() for user in users],
            'query': query
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to search users', 'message': str(e)}), 500


@users_bp.route('/<int:user_id>/stats', methods=['GET'])
@optional_auth
def get_user_stats(user_id, current_user=None):
    """Get user statistics"""
    try:
        user = User.query.get_or_404(user_id)
        
        stats = {
            'reports_count': user.reports.count(),
            'public_reports_count': user.reports.filter_by(is_public=True).count(),
            'comments_count': user.comments.count(),
            'member_since': user.created_at.isoformat() if user.created_at else None
        }
        
        # Add private stats if viewing own profile
        if current_user and current_user.id == user_id:
            stats.update({
                'private_reports_count': user.reports.filter_by(is_public=False).count(),
                'draft_reports_count': user.reports.filter_by(status='draft').count()
            })
        
        return jsonify({
            'user_id': user_id,
            'stats': stats
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to get user stats', 'message': str(e)}), 500