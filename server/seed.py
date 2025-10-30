#!/usr/bin/env python3
import sys
from app import create_app
from app.database import db
from app.models.user import User
from app.models.report import Report
from app.models.tag import Tag
from datetime import datetime

def seed_database():
    app = create_app()
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        user1 = User(username='john_doe', email='john@example.com', first_name='John', last_name='Doe')
        user1.set_password('password123')
        user1.save()

        user2 = User(username='jane_smith', email='jane@example.com', first_name='Jane', last_name='Smith')
        user2.set_password('password123')
        user2.save()
        
        tag1 = Tag(name='pollution')
        tag1.save()
        
        tag2 = Tag(name='water-quality')
        tag2.save()
        
        tag3 = Tag(name='air-quality')
        tag3.save()
        
        report1 = Report(
            title='Plastic waste in local park',
            description='Large amounts of plastic bottles and bags scattered throughout Central Park. This is affecting local wildlife and water quality.',
            user_id=user1.id,
            location='Central Park, New York',
            latitude=40.7829,
            longitude=-73.9654
        )
        report1.ai_category = 'pollution'
        report1.ai_confidence = 0.95
        report1.ai_advice = 'Report to local environmental authorities and organize a cleanup drive.'
        report1.ai_processed = True
        report1.ai_processed_at = datetime.utcnow()
        report1.is_public = True
        report1.save()
        report1.tags.append(tag1)
        
        report2 = Report(
            title='River contamination observed',
            description='The local river has an unusual color and smell. Fish have been found dead along the banks.',
            user_id=user2.id,
            location='Hudson River, NY',
            latitude=40.7589,
            longitude=-73.9851
        )
        report2.ai_category = 'water-issues'
        report2.ai_confidence = 0.88
        report2.ai_advice = 'Contact water management authorities immediately and avoid contact with the water.'
        report2.ai_processed = True
        report2.ai_processed_at = datetime.utcnow()
        report2.is_public = True
        report2.save()
        report2.tags.append(tag2)
        
        report3 = Report(
            title='Heavy smog in downtown area',
            description='Thick smog covering the downtown area, visibility is very low and people are having breathing difficulties.',
            user_id=user1.id,
            location='Downtown Manhattan, NY',
            latitude=40.7505,
            longitude=-73.9934
        )
        report3.ai_category = 'air-quality'
        report3.ai_confidence = 0.92
        report3.ai_advice = 'Stay indoors, use air purifiers, and report to air quality monitoring authorities.'
        report3.ai_processed = True
        report3.ai_processed_at = datetime.utcnow()
        report3.is_public = True
        report3.save()
        report3.tags.append(tag3)
        
        db.session.commit()
        
        print(f"Database seeded successfully!")

if __name__ == "__main__":
    seed_database()