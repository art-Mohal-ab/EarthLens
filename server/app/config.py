import os
from datetime import timedelta


class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # File Upload Configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # AI Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    GPT_MODEL = os.environ.get('GPT_MODEL', 'gpt-4-turbo')
    GPT_TEMPERATURE = float(os.environ.get('GPT_TEMPERATURE', '0.7'))
    GPT_MAX_TOKENS = int(os.environ.get('GPT_MAX_TOKENS', '500'))
    
    # CORS Configuration
    FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
    CORS_ORIGINS = [FRONTEND_URL, 'http://localhost:5173', 'http://127.0.0.1:5173', 'http://localhost:5174', 'http://localhost:5175', 'http://127.0.0.1:5175', 'https://earth-lens-9mgz-git-main-art-mohal-abs-projects.vercel.app']
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # App Info
    APP_NAME = 'EarthLens API'
    VERSION = '1.0.0'


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///dev.db'
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    # Handle Render's postgres:// vs postgresql:// URL format
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///earthlens.db')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = database_url
    LOG_LEVEL = 'WARNING'


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    WTF_CSRF_ENABLED = False
    LOG_LEVEL = 'DEBUG'


def get_config(config_name):
    """Get configuration class by name"""
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,
        'default': DevelopmentConfig
    }
    
    return config_map.get(config_name.lower(), DevelopmentConfig)