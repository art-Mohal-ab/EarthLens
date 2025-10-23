"""
Simple migration script for EarthLens database
"""
import os
from flask_migrate import init, migrate, upgrade
from main import create_app

def setup_migrations():
    """Initialize Flask-Migrate if not already done"""
    app = create_app()
    
    with app.app_context():
        # Check if migrations folder exists
        if not os.path.exists('migrations'):
            print("Initializing migrations...")
            init()
            print("Migrations initialized")
        
        # Create migration
        print("Creating migration...")
        migrate(message="Initial migration")
        print("Migration created")
        
        # Apply migration
        print("Applying migration...")
        upgrade()
        print("Migration applied successfully")

if __name__ == "__main__":
    setup_migrations()