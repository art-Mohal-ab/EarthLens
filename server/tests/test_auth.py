import pytest
from app.models.user import User


class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_user_registration(self, client):
        """Test user registration"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        response = client.post('/api/auth/register', json=data)
        
        assert response.status_code == 201
        assert 'access_token' in response.json
        assert response.json['user']['username'] == 'newuser'
    
    def test_registration_duplicate_email(self, client, test_user):
        """Test registration with duplicate email"""
        data = {
            'username': 'anotheruser',
            'email': 'test@example.com',  # Already exists
            'password': 'SecurePass123'
        }
        
        response = client.post('/api/auth/register', json=data)
        
        assert response.status_code == 400
        assert 'already registered' in response.json['error'].lower()
    
    def test_registration_weak_password(self, client):
        """Test registration with weak password"""
        data = {
            'username': 'weakuser',
            'email': 'weak@example.com',
            'password': 'weak'  # Too short, no uppercase, no number
        }
        
        response = client.post('/api/auth/register', json=data)
        
        assert response.status_code == 400
    
    def test_user_login(self, client, test_user):
        """Test user login"""
        data = {
            'email': 'test@example.com',
            'password': 'TestPass123'
        }
        
        response = client.post('/api/auth/login', json=data)
        
        assert response.status_code == 200
        assert 'access_token' in response.json
        assert 'refresh_token' in response.json
    
    def test_login_invalid_credentials(self, client, test_user):
        """Test login with invalid credentials"""
        data = {
            'email': 'test@example.com',
            'password': 'WrongPassword'
        }
        
        response = client.post('/api/auth/login', json=data)
        
        assert response.status_code == 401
    
    def test_get_current_user(self, client, auth_headers):
        """Test getting current user profile"""
        response = client.get('/api/auth/me', headers=auth_headers)
        
        assert response.status_code == 200
        assert 'user' in response.json
        assert response.json['user']['username'] == 'testuser'
    
    def test_update_profile(self, client, auth_headers):
        """Test updating user profile"""
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'bio': 'Environmental activist'
        }
        
        response = client.put('/api/auth/me', json=data, headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json['user']['first_name'] == 'Updated'
    
    def test_refresh_token(self, client, test_user):
        """Test token refresh"""
        # First login to get refresh token
        login_response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'TestPass123'
        })
        
        refresh_token = login_response.json['refresh_token']
        
        # Use refresh token to get new access token
        response = client.post(
            '/api/auth/refresh',
            headers={'Authorization': f'Bearer {refresh_token}'}
        )
        
        assert response.status_code == 200
        assert 'access_token' in response.json
