import pytest
from unittest.mock import patch, MagicMock


class TestAIRoutes:
    """Test AI service routes"""
    
    def test_ai_health_check(self, client):
        """Test AI service health check"""
        response = client.get('/api/ai/health')
        
        assert response.status_code in [200, 503]
        assert 'status' in response.json
        assert 'service' in response.json
    
    @patch('app.services.ai_service.AIService.analyze_report')
    def test_analyze_report(self, mock_analyze, client, auth_headers, test_report):
        """Test AI report analysis"""
        mock_analyze.return_value = {
            'category': 'water-issues',
            'confidence': 0.85,
            'advice': 'Report to water authorities immediately'
        }
        
        response = client.post(
            f'/api/ai/analyze-report/{test_report.id}',
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert 'analysis' in response.json
        assert response.json['analysis']['category'] == 'water-issues'
        assert response.json['analysis']['confidence'] == 0.85
    
    def test_analyze_nonexistent_report(self, client, auth_headers):
        """Test analyzing a non-existent report"""
        response = client.post(
            '/api/ai/analyze-report/99999',
            headers=auth_headers
        )
        
        assert response.status_code == 404
    
    def test_get_green_advice(self, client):
        """Test getting green advice"""
        response = client.get('/api/ai/green-advice?category=energy')
        
        assert response.status_code == 200
        assert 'advice' in response.json
        assert response.json['category'] == 'energy'
    
    def test_generate_task(self, client):
        """Test generating a green task"""
        response = client.get('/api/ai/generate-task?category=water&difficulty=easy')
        
        assert response.status_code == 200
        assert 'task' in response.json
        assert response.json['task']['category'] in ['water', 'Water']
    
    def test_generate_task_post(self, client):
        """Test generating task via POST"""
        data = {
            'category': 'energy',
            'difficulty': 'medium',
            'location': 'Urban Area'
        }
        
        response = client.post('/api/ai/generate-task', json=data)
        
        assert response.status_code == 200
        assert 'task' in response.json
    
    def test_categorize_text(self, client, auth_headers):
        """Test text categorization"""
        data = {
            'text': 'There is a lot of plastic waste dumped near the river'
        }
        
        response = client.post(
            '/api/ai/categorize-text',
            json=data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert 'category' in response.json
        assert 'confidence' in response.json
        assert 'suggestions' in response.json
    
    def test_categorize_text_missing_data(self, client, auth_headers):
        """Test categorization without text"""
        response = client.post(
            '/api/ai/categorize-text',
            json={},
            headers=auth_headers
        )
        
        assert response.status_code == 400
        assert 'error' in response.json


class TestAIServiceIntegration:
    """Test AI service integration"""
    
    @patch('app.services.ai_service.AIService.classify_environmental_issue')
    def test_classification_fallback(self, mock_classify, client):
        """Test AI classification with fallback"""
        mock_classify.return_value = {
            'category': 'general',
            'confidence': 0.5
        }
        
        response = client.get('/api/ai/green-advice?category=general')
        
        assert response.status_code == 200
    
    def test_ai_advice_all_categories(self, client):
        """Test AI advice for all categories"""
        categories = ['energy', 'water', 'waste', 'general']
        
        for category in categories:
            response = client.get(f'/api/ai/green-advice?category={category}')
            assert response.status_code == 200
            assert 'advice' in response.json
