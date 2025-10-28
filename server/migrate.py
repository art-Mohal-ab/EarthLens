import os
from flask_migrate import init, migrate, upgrade
from main import create_app

def setup_migrations():
    app = create_app()
    
    with app.app_context():
        if not os.path.exists('migrations'):
            print("Initializing migrations...")
            init()
            print("Migrations initialized")
        
        print("Creating migration...")
        migrate(message="Initial migration")
        print("Migration created")
    
        print("Applying migration...")
        upgrade()
        print("Migration applied successfully")

if __name__ == "__main__":
    setup_migrations()