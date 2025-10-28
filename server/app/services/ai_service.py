from openai import OpenAI
import os
import json
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None
        self.model = os.getenv("GPT_MODEL", "gpt-4o-mini")
        self.temperature = float(os.getenv("GPT_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("GPT_MAX_TOKENS", "500"))

    def classify_environmental_issue(self, title, description, image_url=None):
        text = f"{title}. {description}".strip()

        try:
            if not self.client:
                raise Exception("OpenAI client not configured")
                
            prompt = f"""
            You are an environmental issue classification assistant.

            Classify the following report into one of these categories:
            ["pollution", "climate-change", "deforestation", "water-issues", "air-quality", "wildlife", "environmental-issue"]

            Respond ONLY with valid JSON in this format:
            {{
              "category": "<category>",
              "confidence": <number between 0 and 1>
            }}

            Report:
            {text}
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt.strip()}],
                temperature=0.0,
                max_tokens=self.max_tokens,
            )

            content = response.choices[0].message.content
            if content is None:
                raise ValueError("Empty GPT response")
            content = content.strip()
            if not content:
                raise ValueError("Empty GPT response")

            classification = json.loads(content)
            classification["raw_result"] = "gpt"
            return classification

        except Exception as e:
            logger.warning(f"GPT classification failed: {e}")
            return self._keyword_classification(text)

    def _keyword_classification(self, text):
        text = text.lower()
        categories = {
            "pollution": ["pollution", "waste", "garbage", "trash", "contamination", "toxic", "dump"],
            "climate-change": ["climate", "temperature", "weather", "global warming", "carbon", "heat"],
            "deforestation": ["forest", "trees", "logging", "deforestation", "habitat", "wood"],
            "water-issues": ["water", "river", "ocean", "lake", "drought", "flood", "stream"],
            "air-quality": ["air", "smog", "emissions", "smoke", "breathing", "fumes"],
            "wildlife": ["animals", "wildlife", "species", "endangered", "biodiversity", "birds"],
        }

        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return {"category": category, "confidence": 0.8, "raw_result": "keyword_match"}

        return {"category": "environmental-issue", "confidence": 0.6, "raw_result": "default"}

    def generate_advice(self, category, title, description, location=None):
        prompt = f"""
        You are an expert in sustainability and environmental management.

        Based on the following information, give **2–3 short actionable tips**
        the user can take to help mitigate or report this issue.

        Format the response as a short paragraph (no JSON).

        Category: {category}
        Title: {title}
        Description: {description}
        Location: {location or 'N/A'}
        """

        try:
            if not self.client:
                raise Exception("OpenAI client not configured")
                
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt.strip()}],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            advice = response.choices[0].message.content
            if advice is None:
                raise ValueError("Empty GPT advice response")
            advice = advice.strip()
            if not advice:
                raise ValueError("Empty GPT advice response")

            return advice

        except Exception as e:
            logger.warning(f"GPT advice generation failed: {e}")
            return self._default_advice(category)

    def _default_advice(self, category):
        advice_map = {
            "pollution": "Report to local environmental authorities and avoid littering. Organize a cleanup drive if possible.",
            "climate-change": "Use energy-efficient appliances, reduce car use, and support tree-planting initiatives.",
            "deforestation": "Report illegal logging, support reforestation programs, and reduce paper waste.",
            "water-issues": "Conserve water, report leaks, and avoid dumping waste into water bodies.",
            "air-quality": "Limit burning of waste, use public transport, and plant trees to improve air quality.",
            "wildlife": "Do not disturb natural habitats. Report illegal poaching or trade to wildlife authorities.",
            "environmental-issue": "Document and report the issue to local authorities for further investigation.",
        }
        return advice_map.get(category, advice_map["environmental-issue"])

    def get_green_actions(self, user_location=None, interests=None):
        base_actions = [
            {"title": "Switch to LED Bulbs", "category": "Energy", "difficulty": "Easy", "description": "Replace traditional bulbs with energy efficient LED lights throughout your home.", "impact": "Saves 75% energy, reduces 200kg CO₂/year"},
            {"title": "Collect Rainwater", "category": "Water", "difficulty": "Medium", "description": "Set up rainwater harvesting system for watering plants and gardens.", "impact": "Saves 500+ litres per month"},
            {"title": "Plant Native Trees", "category": "Nature", "difficulty": "Medium", "description": "Plant indigenous tree species in your community to restore ecosystem.", "impact": "Absorb 20kg carbon dioxide per tree"},
            {"title": "Start Composting", "category": "Waste", "difficulty": "Medium", "description": "Turn food waste into nutrient-rich compost for gardening.", "impact": "Diverts 150kg waste from landfills per year"},
            {"title": "Install Solar Panels", "category": "Energy", "difficulty": "Hard", "description": "Generate clean energy by installing solar panels on your roof.", "impact": "Saves 3,000kgs carbon dioxide per year"},
            {"title": "Fix Water Leaks", "category": "Water", "difficulty": "Easy", "description": "Repair dripping taps and leaking pipes to conserve water.", "impact": "Saves 20 litres per day"},
            {"title": "Use Public Transport", "category": "Lifestyle", "difficulty": "Easy", "description": "Choose buses, trains, or carpool instead of driving alone.", "impact": "Reduces 1,000kg carbon dioxide per year"},
            {"title": "Create Wildlife Habitat", "category": "Nature", "difficulty": "Medium", "description": "Plant native flowers and shrubs to support local pollinators and birds.", "impact": "Supports 50+ species"},
            {"title": "Reduce Plastic Use", "category": "Waste", "difficulty": "Easy", "description": "Use reusable bags, bottles, and containers to minimize plastic waste.", "impact": "Prevents 100kg plastic waste per year"},
            {"title": "Bike to Work", "category": "Lifestyle", "difficulty": "Easy", "description": "Cycle for short trips instead of driving to reduce emissions.", "impact": "Saves 500kg CO₂ per year"}
        ]

        if interests:
            base_actions = [a for a in base_actions if any(i.lower() in a["title"].lower() for i in interests)]

        return base_actions



ai_service = AIService()
