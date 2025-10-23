"""
EarthLens Server Startup Script
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import create_app

if __name__ == "__main__":
    # Create Flask app
    app = create_app()
    
    # Get configuration
    port = int(os.environ.get("PORT", 5001))
    debug = os.environ.get("FLASK_ENV") == "development"
    
    pass
    
    # Run the app
    app.run(host="0.0.0.0", port=port, debug=debug)