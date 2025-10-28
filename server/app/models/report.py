from database import db, BaseModel
from datetime import datetime

class Report(BaseModel):
    __tablename__ = 'reports'

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    image_url = db.Column(db.String(500))
    image_filename = db.Column(db.String(200))


    ai_category = db.Column(db.String(100))
    ai_confidence = db.Column(db.Float)
    ai_advice = db.Column(db.Text)
    ai_processed = db.Column(db.Boolean, default=False)
    ai_processed_at = db.Column(db.DateTime)

    status = db.Column(db.String(20), default='active')
    is_public = db.Column(db.Boolean, default=True)


    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_report_user'), nullable=False)
    author = db.relationship('User', back_populates='reports')
    comments = db.relationship('Comment', backref='report', lazy='dynamic', cascade='all, delete-orphan')
    tags = db.relationship('Tag', secondary='report_tags', back_populates='reports')

    def __init__(self, title, description, user_id, location=None, latitude=None, longitude=None):
        self.title = title
        self.description = description
        self.user_id = user_id
        self.location = location
        self.latitude = latitude
        self.longitude = longitude

    def to_dict(self, include_author=True, include_comments=False, include_tags=True):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'image_url': self.image_url,
            'ai_category': self.ai_category,
            'ai_confidence': self.ai_confidence,
            'ai_advice': self.ai_advice,
            'ai_processed': self.ai_processed,
            'status': self.status,
            'is_public': self.is_public,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

        if include_author and hasattr(self, "author") and self.author:
            data['author'] = {
                'id': self.author.id,
                'username': self.author.username
            }

        if include_comments:
            data['comments_count'] = self.comments.count()
            data['comments'] = [comment.to_dict() for comment in self.comments.limit(5)]

        if include_tags:
            tags = getattr(self, 'tags', None)
            if tags is not None:
                try:
                    data['tags'] = [tag.to_dict() for tag in tags]
                except (AttributeError, TypeError):
                    data['tags'] = []
            else:
                data['tags'] = []

        return data

    @classmethod
    def get_public_reports(cls, limit=50, offset=0):
        return cls.query.filter_by(is_public=True, status='active') \
                      .order_by(cls.created_at.desc()) \
                      .limit(limit) \
                      .offset(offset) \
                      .all()

    @classmethod
    def get_user_reports(cls, user_id, limit=50, offset=0):
        return cls.query.filter_by(user_id=user_id) \
                      .order_by(cls.created_at.desc()) \
                      .limit(limit) \
                      .offset(offset) \
                      .all()

    def __repr__(self):
        return f'<Report {self.title}>'
