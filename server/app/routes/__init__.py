from .auth import auth_bp
from .reports import reports_bp
from .ai import ai_bp
from .users import users_bp
from .comments import comments_bp
from .tags import tags_bp

__all__ = ['auth_bp', 'reports_bp', 'ai_bp', 'users_bp', 'comments_bp', 'tags_bp']
