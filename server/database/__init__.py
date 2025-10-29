from .db import db, BaseModel
from flask_sqlalchemy import SQLAlchemy

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
