from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    
    with app.app_context():
        from app.models.user import User
        from app.models.report import Report
        from app.models.tag import Tag, report_tags
        from app.models.comment import Comment
        
        db.create_all()

def reset_db(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database reset successfully!")

class BaseModel(db.Model):
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow, 
        nullable=False
    )
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def to_dict(self):
        table = getattr(self, '__table__', None)
        if table is not None:
            return {
                column.name: getattr(self, column.name)
                for column in table.columns
            }
        return {}
