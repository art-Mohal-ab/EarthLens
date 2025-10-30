import pytest
import json
from app.models.report import Report


class TestReportCreation:
    """Test report creation functionality"""
    
    def test_create_report_success(self, client, auth_headers):
        """Test successful report creation"""
        data = {
            'title': 'Water Pollution in River',
            'description': 'Noticed chemical waste being dumped into the river',
            'location': 'River Bank, City Center',
            'latitude': 40.7128,
            'longitude': -74.0060,
            'severity': 'high',
            'is_public': True
        }
        
        response = client.post(
            '/api/reports',
            json=data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        assert response.json['message'] == 'Report created successfully'
        assert response.json['report']['title'] == data['title']
        assert response.json['report']['severity'] == 'high'
    
    def test_create_report_without_auth(self, client):
        """Test report creation without authentication"""
        data = {
            'title': 'Test Report',
            'description': 'Test description',
            'location': 'Test Location'
        }
        
        response = client.post('/api/reports', json=data)
        assert response.status_code == 401
    
    def test_create_report_invalid_data(self, client, auth_headers):
        """Test report creation with invalid data"""
        data = {
            'title': 'AB',  # Too short
            'description': 'Short'  # Too short
        }
        
        response = client.post(
            '/api/reports',
            json=data,
            headers=auth_headers
        )
        
        assert response.status_code == 400
        assert 'error' in response.json


class TestReportCRUD:
    """Test CRUD operations for reports"""
    
    def test_get_all_reports(self, client, test_report):
        """Test getting all public reports"""
        response = client.get('/api/reports')
        
        assert response.status_code == 200
        assert 'reports' in response.json
        assert len(response.json['reports']) > 0
    
    def test_get_report_by_id(self, client, test_report):
        """Test getting a specific report"""
        response = client.get(f'/api/reports/{test_report.id}')
        
        assert response.status_code == 200
        assert response.json['report']['id'] == test_report.id
        assert response.json['report']['title'] == test_report.title
    
    def test_update_report(self, client, auth_headers, test_report):
        """Test updating a report"""
        updated_data = {
            'title': 'Updated Report Title',
            'description': 'Updated description with more details',
            'severity': 'critical'
        }
        
        response = client.put(
            f'/api/reports/{test_report.id}',
            json=updated_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert response.json['report']['title'] == updated_data['title']
        assert response.json['report']['severity'] == 'critical'
    
    def test_update_report_unauthorized(self, client, test_report):
        """Test updating report without authorization"""
        response = client.put(
            f'/api/reports/{test_report.id}',
            json={'title': 'Hacked'}
        )
        
        assert response.status_code == 401
    
    def test_delete_report(self, client, auth_headers, test_report):
        """Test deleting a report"""
        response = client.delete(
            f'/api/reports/{test_report.id}',
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert 'deleted successfully' in response.json['message']
        
        # Verify report is deleted
        get_response = client.get(f'/api/reports/{test_report.id}')
        assert get_response.status_code == 404
    
    def test_get_user_reports(self, client, auth_headers, test_report):
        """Test getting current user's reports"""
        response = client.get(
            '/api/reports/my-reports',
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert 'reports' in response.json
        assert len(response.json['reports']) > 0


class TestReportFiltering:
    """Test report filtering and search"""
    
    def test_filter_by_location(self, client, test_report):
        """Test filtering reports by location"""
        response = client.get('/api/reports?location=Test')
        
        assert response.status_code == 200
        assert 'reports' in response.json
    
    def test_pagination(self, client):
        """Test report pagination"""
        response = client.get('/api/reports?page=1&per_page=10')
        
        assert response.status_code == 200
        assert 'pagination' in response.json
        assert response.json['pagination']['page'] == 1
