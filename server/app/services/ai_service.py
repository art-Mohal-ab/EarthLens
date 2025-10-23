from openai import OpenAI
from datetime import datetime
import os
import json

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

class AIService:
    def __init__(self):
        pass

    def classify_environmental_issue(self, title, description, image_url=None):
        text = f"{title}. {description}".strip()
        try:
            prompt = f"""
            Classify the following environmental report into one of these categories:
            pollution, climate-change, deforestation, water-issues, air-quality, wildlife, environmental-issue.
            Respond with JSON: {{ "category": "<category>", "confidence": 0-1 }}

            Report:
            {text}
            """
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            content = response.choices[0].message.content
            if content is None:
                raise Exception("Empty response from OpenAI")
            classification = json.loads(content.strip())
            classification['raw_result'] = 'gpt-4'
            return classification

        except Exception as e:
            print(f"GPT-4 classification failed: {e}")
            return self._keyword_classification(text)

    def _keyword_classification(self, text):
        text = text.lower()
        categories = {
            'pollution': ['pollution', 'waste', 'garbage', 'trash', 'contamination', 'toxic', 'dump'],
            'climate-change': ['climate', 'temperature', 'weather', 'global warming', 'carbon', 'heat'],
            'deforestation': ['forest', 'trees', 'logging', 'deforestation', 'habitat', 'wood'],
            'water-issues': ['water', 'river', 'ocean', 'lake', 'drought', 'flood', 'stream'],
            'air-quality': ['air', 'smog', 'emissions', 'smoke', 'breathing', 'fumes'],
            'wildlife': ['animals', 'wildlife', 'species', 'endangered', 'biodiversity', 'birds']
        }
        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return {'category': category, 'confidence': 0.8, 'raw_result': 'keyword_match'}
        return {'category': 'environmental-issue', 'confidence': 0.6, 'raw_result': 'default'}

    def generate_advice(self, category, title, description, location=None):
        text = f"Generate actionable advice for the following environmental report:\nCategory: {category}\nTitle: {title}\nDescription: {description}\nLocation: {location or 'N/A'}"
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": text}],
                temperature=0.7
            )
            advice = response.choices[0].message.content
            if advice is None:
                raise Exception("Empty response from OpenAI")
            return advice.strip()
        except Exception as e:
            print(f"GPT-4 advice generation failed: {e}")
            return self._default_advice(category)

    def _default_advice(self, category):
        advice_map = {
            'pollution': "Report this to local environmental authorities. Document with photos and location details.",
            'climate-change': "Reduce your carbon footprint by using public transport and conserving energy.",
            'deforestation': "Report illegal logging to forestry authorities. Support reforestation efforts.",
            'water-issues': "Report to water management authorities. Conserve water usage.",
            'air-quality': "Monitor air quality indexes. Report industrial emissions to authorities.",
            'wildlife': "Contact local wildlife protection agencies. Document with photos safely.",
            'environmental-issue': "Document the issue and report to local environmental authorities."
        }
        return advice_map.get(category, advice_map['environmental-issue'])

    def get_green_actions(self, user_location=None, interests=None):
        """
        Generate 10 AI-powered eco-tips.
        Tries GPT-4 first; falls back to static tips if GPT-4 fails.
        """
        try:
            prompt = """
            Generate 10 short and actionable sustainability tips (eco-tips) suitable for a webpage.
            Each tip should include:
            - title
            - tag (Energy, Water, Travel, Nature, Food, Waste)
            - description
            - impact_text (e.g., "Saves 3,000kg carbon dioxide per year")
            - difficulty (Easy, Medium, Hard)
            Respond ONLY in JSON array format.
            """
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            content = response.choices[0].message.content
            if content is None:
                raise Exception("Empty response from OpenAI")
            return json.loads(content.strip())

        except Exception as e:
            print(f"GPT-4 eco-tips generation failed: {e}")
            # Fallback static tips
            return [
                {"title": "Reduce Plastic Use", "tag": "Waste", "description": "Use reusable bags and water bottles", "impact_text": "Reduces plastic waste by 50kg per year", "difficulty": "Easy"},
                {"title": "Save Energy at Home", "tag": "Energy", "description": "Switch to LED bulbs and unplug devices", "impact_text": "Saves 1,000 kWh per year", "difficulty": "Easy"},
                {"title": "Use Public Transport", "tag": "Travel", "description": "Take buses, trains, or cycle instead of driving", "impact_text": "Cuts 500kg CO2 per year", "difficulty": "Medium"},
                {"title": "Compost Organic Waste", "tag": "Waste", "description": "Turn food scraps into compost", "impact_text": "Reduces landfill waste by 200kg per year", "difficulty": "Medium"},
                {"title": "Plant Trees", "tag": "Nature", "description": "Participate in local tree planting events", "impact_text": "Supports 50+ species locally", "difficulty": "Medium"},
                {"title": "Save Water", "tag": "Water", "description": "Fix leaks and use water-saving appliances", "impact_text": "Saves 5,000 liters per month", "difficulty": "Easy"},
                {"title": "Eat More Plant-Based Meals", "tag": "Food", "description": "Reduce meat consumption to lower carbon footprint", "impact_text": "Saves 1,200kg CO2 per year", "difficulty": "Medium"},
                {"title": "Avoid Fast Fashion", "tag": "Waste", "description": "Buy fewer, higher-quality clothes and donate old items", "impact_text": "Reduces textile waste by 10kg per year", "difficulty": "Medium"},
                {"title": "Support Local Produce", "tag": "Food", "description": "Buy from local farmers to reduce transport emissions", "impact_text": "Reduces food transport CO2 by 300kg per year", "difficulty": "Easy"},
                {"title": "Use Eco-Friendly Cleaning Products", "tag": "Waste", "description": "Switch to biodegradable detergents and cleaning agents", "impact_text": "Prevents 100L of chemical runoff annually", "difficulty": "Easy"}
            ]

ai_service = AIService()
