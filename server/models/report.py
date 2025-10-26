 database import db, BaseModel

class Report(BaseModel):
    __tablename__ = 'reports'

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    image_url = db.Column(db.String(500))
    is_public = db.Column(db.Boolean, default=True)
    status = db.Column(db.String(50), default='active')  # active, resolved, archived

    # AI processing fields
    ai_category = db.Column(db.String(100))
    ai_confidence = db.Column(db.Float)
    ai_advice = db.Column(db.Text)
    ai_processed = db.Column(db.Boolean, default=False)
    ai_processed_at = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    user = db.relationship('User', backref=db.backref('reports', lazy='dynamic'))
    tags = db.relationship('Tag', secondary='report_tags', back_populates='reports', lazy='dynamic')

    def __init__(self, title, description, location=None, latitude=None, longitude=None,
                 image_url=None, user_id=None, is_public=True):
        self.title = title
        self.description = description
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.image_url = image_url
        self.user_id = user_id
        self.is_public = is_public

    def to_dict(self, include_comments=True, include_tags=True):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'image_url': self.image_url,
            'is_public': self.is_public,
            'status': self.status,
            'ai_category': self.ai_category,
            'ai_confidence': self.ai_confidence,
            'ai_advice': self.ai_advice,
            'ai_processed': self.ai_processed,
            'ai_processed_at': self.ai_processed_at.isoformat() if self.ai_processed_at else None,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_comments:
            data['comments_count'] = self.comments.count()

        if include_tags:
            data['tags'] = [tag.to_dict() for tag in self.tags]

        return data

    @classmethod
    def get_public_reports(cls, limit=20, offset=0):
        return cls.query.filter_by(is_public=True, status='active')\
                        .order_by(cls.created_at.desc())\
                        .limit(limit)\
                        .offset(offset)\
                        .all()

    def __repr__(self):
        return f'<Report {self.title}>'
