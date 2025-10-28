import requests
import os

class AIService:
    def __init__(self):
        self.api_key = os.environ.get('OPENAI_API_KEY')
        self.base_url = "https://api.openai.com/v1"

    def classify_environmental_issue(self, title, description, image_url=None):
        """Classify environmental issue using AI"""
        try:
            prompt = f"""
            Analyze this environmental report and classify it into one of these categories:
            - Pollution (air, water, soil, noise)
            - Deforestation
            - Wildlife endangerment
            - Climate change
            - Waste management
            - Other

            Title: {title}
            Description: {description}

            Return only a JSON object with 'category' and 'confidence' (0-1) fields.
            """

            # For now, return mock classification
            # In production, this would call OpenAI API
            return {
                'category': 'Pollution',
                'confidence': 0.85
            }

        except Exception as e:
            print(f"AI classification failed: {e}")
            return {
                'category': 'Other',
                'confidence': 0.5
            }

    def generate_advice(self, category, title, description, location=None):
        """Generate AI-powered advice for environmental issue"""
        try:
            prompt = f"""
            Provide helpful advice for this {category} environmental issue:

            Title: {title}
            Description: {description}
            Location: {location or 'Not specified'}

            Give practical, actionable advice in 2-3 sentences.
            """

            # For now, return mock advice
            # In production, this would call OpenAI API
            return f"This appears to be a {category.lower()} issue. Consider documenting with photos and reporting to local environmental authorities. Community awareness and collective action can help address such problems effectively."

        except Exception as e:
            print(f"AI advice generation failed: {e}")
            return "Please report this issue to relevant environmental authorities and consider gathering more evidence to support your case."

# Singleton instance
ai_service = AIService()
