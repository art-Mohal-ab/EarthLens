import pytest
import os
from app import create_app
from app.database import db
from app.models.user import User
from app.models.report import Report


@pytest.fixture(scope='session')
def app():
    """Create application for testing"""
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture(scope='function', autouse=True)
def db_session(app):
    """Create database session for tests"""
    with app.app_context():
        # Clear all data before each test
        db.session.remove()
        db.drop_all()
        db.create_all()
        yield db.session
        db.session.remove()


@pytest.fixture
def test_user(db_session):
    """Create a test user"""
    user = User(
        username='testuser',
        email='test@example.com',
        first_name='Test',
        last_name='User'
    )
    user.set_password('TestPass123')
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers with JWT token"""
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'TestPass123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def test_report(db_session, test_user):
    """Create a test report"""
    report = Report(
        title='Test Environmental Issue',
        description='This is a test report for environmental monitoring',
        user_id=test_user.id,
        location='Test Location',
        latitude=40.7128,
        longitude=-74.0060,
        severity='medium',
        is_public=True
    )
    db_session.add(report)
    db_session.commit()
    return report
