import os
import json
import logging
from groq import Groq

logger = logging.getLogger(__name__)


class AIService:
    """Service for AI-powered environmental analysis"""
    
    def __init__(self):
        self.api_key = os.environ.get('GROQ_API_KEY')
        self.client = None
        if self.api_key and self.api_key not in ['your-groq-api-key-here', 'your-gro************here', '']:
            try:
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize Groq client: {e}")
                self.client = None
        self.model = os.environ.get('GROQ_MODEL', 'llama-3.1-70b-versatile')
        self.temperature = float(os.environ.get('GROQ_TEMPERATURE', '0.7'))
        self.max_tokens = int(os.environ.get('GROQ_MAX_TOKENS', '500'))
    
    def health_check(self):
        """Check if AI service is available"""
        return self.client is not None and self.api_key is not None
    
    def analyze_report(self, report):
        """Analyze an environmental report"""
        try:
            classification = self.classify_environmental_issue(
                report.title, 
                report.description, 
                report.image_url
            )
            
            # Generate advice
            advice = self.generate_advice(
                classification.get('category', 'environmental-issue'),
                report.title,
                report.description,
                report.location
            )
            
            return {
                'category': classification.get('category'),
                'confidence': classification.get('confidence'),
                'advice': advice
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze report {report.id}: {e}")
            return None
    
    def classify_environmental_issue(self, title, description, image_url=None):
        """Classify environmental issue using AI"""
        text = f"{title}. {description}".strip()
        
        try:
            if not self.client:
                return self._keyword_classification(text)
            
            prompt = f"""
            You are an environmental issue classification assistant.
            
            Classify the following environmental report into one of these categories:
            ["pollution", "climate-change", "deforestation", "water-issues", "air-quality", "wildlife", "waste-management", "energy", "general"]
            
            Respond ONLY with valid JSON in this exact format:
            {{
              "category": "<category>",
              "confidence": <number between 0 and 1>
            }}
            
            Report: {text}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt.strip()}],
                temperature=0.1,
                max_tokens=100
            )
            
            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty AI response")
            
            result = json.loads(content.strip())
            return result
            
        except Exception as e:
            logger.warning(f"AI classification failed: {e}")
            return self._keyword_classification(text)
    
    def _keyword_classification(self, text):
        """Fallback keyword-based classification"""
        text_lower = text.lower()
        
        categories = {
            "pollution": ["pollution", "contamination", "toxic", "chemical", "oil spill"],
            "water-issues": ["water", "river", "lake", "ocean", "drought", "flood", "sewage"],
            "air-quality": ["air", "smog", "emissions", "smoke", "dust", "fumes"],
            "waste-management": ["waste", "garbage", "trash", "litter", "dump", "landfill"],
            "deforestation": ["forest", "trees", "logging", "deforestation", "habitat loss"],
            "wildlife": ["animals", "wildlife", "species", "endangered", "poaching"],
            "climate-change": ["climate", "temperature", "global warming", "carbon", "greenhouse"],
            "energy": ["energy", "electricity", "power", "solar", "renewable"]
        }
        
        for category, keywords in categories.items():
            if any(keyword in text_lower for keyword in keywords):
                return {"category": category, "confidence": 0.7}
        
        return {"category": "general", "confidence": 0.5}
    
    def generate_advice(self, category, title, description, location=None):
        """Generate actionable advice for environmental issue"""
        try:
            if not self.client:
                return self._default_advice(category)
            
            prompt = f"""
            You are an environmental expert providing actionable advice.
            
            Based on this environmental issue, provide 2-3 specific, actionable steps 
            that individuals can take to help address or report this problem.
            
            Keep the response concise and practical. Format as a short paragraph.
            
            Category: {category}
            Issue: {title}
            Details: {description}
            Location: {location or 'Not specified'}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt.strip()}],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            advice = response.choices[0].message.content
            return advice.strip() if advice else self._default_advice(category)
            
        except Exception as e:
            logger.warning(f"AI advice generation failed: {e}")
            return self._default_advice(category)
    
    def _default_advice(self, category):
        """Fallback advice based on category"""
        advice_map = {
            "pollution": "Report to local environmental authorities, document with photos, and avoid the contaminated area until cleaned.",
            "water-issues": "Report to water management authorities, conserve water usage, and avoid using contaminated water sources.",
            "air-quality": "Report to air quality monitoring agencies, limit outdoor activities during poor air quality, and use air purifiers indoors.",
            "waste-management": "Report illegal dumping to local authorities, organize community cleanup efforts, and practice proper waste segregation.",
            "deforestation": "Report illegal logging to forest authorities, support reforestation programs, and reduce paper consumption.",
            "wildlife": "Report to wildlife protection agencies, maintain safe distance from animals, and support conservation efforts.",
            "climate-change": "Reduce energy consumption, use sustainable transportation, and support renewable energy initiatives.",
            "energy": "Switch to energy-efficient appliances, use renewable energy sources, and reduce overall energy consumption.",
            "general": "Document the issue thoroughly, report to relevant local authorities, and engage with community environmental groups."
        }
        
        return advice_map.get(category, advice_map["general"])
    
    def generate_green_advice(self, category='general', location=None):
        """Generate green actions and advice"""
        actions = [
            {"title": "Switch to LED Bulbs", "category": "Energy", "difficulty": "Easy",
             "description": "Replace traditional bulbs with energy efficient LED lights throughout your home.",
             "impact": "Saves 75% energy, reduces 200kg CO₂/year"},
            {"title": "Collect Rainwater", "category": "Water", "difficulty": "Medium",
             "description": "Set up rainwater harvesting system for watering plants and gardens.",
             "impact": "Saves 500+ litres per month"},
            {"title": "Plant Native Trees", "category": "Nature", "difficulty": "Medium",
             "description": "Plant indigenous tree species in your community to restore ecosystem.",
             "impact": "Absorb 20kg carbon dioxide per tree"},
            {"title": "Start Composting", "category": "Waste", "difficulty": "Medium",
             "description": "Turn food waste into nutrient-rich compost for gardening.",
             "impact": "Diverts 150kg waste from landfills per year"},
            {"title": "Install Solar Panels", "category": "Energy", "difficulty": "Hard",
             "description": "Generate clean energy by installing solar panels on your roof.",
             "impact": "Saves 3,000kg carbon dioxide per year"},
            {"title": "Fix Water Leaks", "category": "Water", "difficulty": "Easy",
             "description": "Repair dripping taps and leaking pipes to conserve water.",
             "impact": "Saves 20 litres per day"},
            {"title": "Use Public Transport", "category": "Lifestyle", "difficulty": "Easy",
             "description": "Choose buses, trains, or carpool instead of driving alone.",
             "impact": "Reduces 1,000kg carbon dioxide per year"},
            {"title": "Create Wildlife Habitat", "category": "Nature", "difficulty": "Medium",
             "description": "Plant native flowers and shrubs to support local pollinators and birds.",
             "impact": "Supports 50+ species"},
            {"title": "Reduce Plastic Use", "category": "Waste", "difficulty": "Easy",
             "description": "Use reusable bags, bottles, and containers to minimize plastic waste.",
             "impact": "Prevents 100kg plastic waste per year"},
            {"title": "Bike to Work", "category": "Lifestyle", "difficulty": "Easy",
             "description": "Cycle for short trips instead of driving to reduce emissions.",
             "impact": "Saves 500kg CO₂ per year"}
        ]

        # Filter by category if specified
        if category != 'general' and category != 'all':
            actions = [action for action in actions
                      if action['category'].lower() == category.lower()]

        return {"actions": actions, "total": len(actions)}

    def generate_green_task(self, category='general', difficulty=None, location=None):
        """Generate a single AI-powered green task"""
        try:
            if not self.client:
                return self._generate_fallback_task(category, difficulty)

            # Build prompt for AI task generation
            prompt = f"""
            Generate a unique, actionable green environmental task for someone to complete.

            Requirements:
            - Category: {category}
            - Difficulty: {difficulty if difficulty else 'any level (easy, medium, or hard)'}
            - Location context: {location if location else 'general location'}

            The task should be:
            - Specific and actionable
            - Realistic and achievable
            - Environmentally beneficial
            - Include measurable impact where possible

            Respond with valid JSON in this exact format:
            {{
              "title": "Task Title",
              "category": "{category}",
              "difficulty": "Easy|Medium|Hard",
              "description": "Detailed description of what to do",
              "impact": "Environmental impact or benefit",
              "time_estimate": "Estimated time to complete",
              "materials_needed": ["item1", "item2"] or null
            }}
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt.strip()}],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty AI response")

            task = json.loads(content.strip())
            return task

        except Exception as e:
            logger.warning(f"AI task generation failed: {e}")
            return self._generate_fallback_task(category, difficulty)

    def _generate_fallback_task(self, category, difficulty=None):
        """Fallback task generation when AI is unavailable"""
        fallback_tasks = {
            "energy": [
                {"title": "Audit Home Energy Use", "difficulty": "Easy", "description": "Go through your home and identify energy-wasting appliances and habits.", "impact": "Identify 10-20% energy savings opportunities", "time_estimate": "30 minutes", "materials_needed": None},
                {"title": "Install Smart Thermostat", "difficulty": "Medium", "description": "Replace your traditional thermostat with a smart, programmable one.", "impact": "Reduce heating/cooling costs by 10%", "time_estimate": "1 hour", "materials_needed": ["Smart thermostat device"]},
                {"title": "Home Solar Assessment", "difficulty": "Hard", "description": "Research and get quotes for solar panel installation on your property.", "impact": "Potential for 100% renewable energy", "time_estimate": "2-3 hours", "materials_needed": None}
            ],
            "water": [
                {"title": "Check for Leaks", "difficulty": "Easy", "description": "Inspect all faucets, toilets, and pipes for water leaks.", "impact": "Save up to 10 gallons per day", "time_estimate": "15 minutes", "materials_needed": None},
                {"title": "Install Low-Flow Fixtures", "difficulty": "Medium", "description": "Replace showerheads and faucets with water-efficient models.", "impact": "Reduce water usage by 40%", "time_estimate": "45 minutes", "materials_needed": ["Low-flow showerhead", "Low-flow faucet aerators"]},
                {"title": "Create Rain Garden", "difficulty": "Hard", "description": "Design and install a rain garden to manage stormwater runoff.", "impact": "Prevent 1,000+ gallons of runoff annually", "time_estimate": "4-6 hours", "materials_needed": ["Native plants", "Mulch", "Shovel"]}
            ],
            "waste": [
                {"title": "Zero Waste Week Challenge", "difficulty": "Easy", "description": "Try to produce no trash for one week by composting and reusing.", "impact": "Reduce landfill waste by 5-10 lbs", "time_estimate": "7 days", "materials_needed": None},
                {"title": "Upcycle Old Furniture", "difficulty": "Medium", "description": "Transform old furniture or items into something new and useful.", "impact": "Keep items out of landfill", "time_estimate": "2-4 hours", "materials_needed": ["Paint", "Sandpaper", "Basic tools"]},
                {"title": "Community Clean-up Event", "difficulty": "Hard", "description": "Organize a neighborhood or park cleanup event.", "impact": "Remove hundreds of pounds of litter", "time_estimate": "4-6 hours", "materials_needed": ["Trash bags", "Gloves", "Safety vests"]}
            ],
            "general": [
                {"title": "Plant a Vegetable Garden", "difficulty": "Easy", "description": "Start a small vegetable garden in containers or a plot.", "impact": "Grow your own food sustainably", "time_estimate": "30 minutes setup", "materials_needed": ["Seeds or seedlings", "Containers or soil"]},
                {"title": "Conduct Energy Audit", "difficulty": "Medium", "description": "Use an energy audit app or checklist to assess your home's efficiency.", "impact": "Identify energy savings of 15-25%", "time_estimate": "1 hour", "materials_needed": ["Energy audit app or checklist"]},
                {"title": "Install Home Wind Turbine", "difficulty": "Hard", "description": "Research and install a small residential wind turbine.", "impact": "Generate clean energy for your home", "time_estimate": "Full day + installation", "materials_needed": ["Wind turbine kit", "Installation tools"]}
            ]
        }

        # Get tasks for category or fallback to general
        tasks = fallback_tasks.get(category.lower(), fallback_tasks["general"])

        # Filter by difficulty if specified
        if difficulty:
            tasks = [task for task in tasks if task["difficulty"].lower() == difficulty.lower()]

        # Return random task or first one
        import random
        selected_task = random.choice(tasks) if tasks else tasks[0]

        # Ensure it has the required fields
        task_data = {
            "title": selected_task["title"],
            "category": category.title(),
            "difficulty": selected_task["difficulty"],
            "description": selected_task["description"],
            "impact": selected_task["impact"],
            "time_estimate": selected_task.get("time_estimate", "1 hour"),
            "materials_needed": selected_task.get("materials_needed")
        }

        return task_data
    
    def categorize_environmental_issue(self, text):
        """Categorize environmental text and provide suggestions"""
        classification = self.classify_environmental_issue("", text)
        
        suggestions = self._get_category_suggestions(classification.get('category', 'general'))
        
        return {
            'category': classification.get('category'),
            'confidence': classification.get('confidence'),
            'suggestions': suggestions
        }
    
    def _get_category_suggestions(self, category):
        """Get suggestions based on category"""
        suggestions_map = {
            "pollution": ["Document with photos", "Report to EPA", "Avoid contaminated area"],
            "water-issues": ["Test water quality", "Report to water authority", "Use alternative water source"],
            "air-quality": ["Monitor air quality index", "Use air purifiers", "Report to environmental agency"],
            "waste-management": ["Organize cleanup", "Report illegal dumping", "Implement recycling"],
            "deforestation": ["Report illegal logging", "Support reforestation", "Use sustainable products"],
            "wildlife": ["Contact wildlife authorities", "Maintain safe distance", "Support conservation"],
            "climate-change": ["Reduce carbon footprint", "Use renewable energy", "Support climate action"],
            "energy": ["Use energy-efficient appliances", "Install solar panels", "Reduce consumption"],
            "general": ["Document the issue", "Contact local authorities", "Engage community"]
        }
        
        return suggestions_map.get(category, suggestions_map["general"])