from app.database import db, BaseModel
from datetime import datetime


# Association table for many-to-many relationship between reports and tags
report_tags = db.Table('report_tags',
    db.Column('report_id', db.Integer, db.ForeignKey('reports.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)


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
    severity = db.Column(db.String(20), default='medium')  # low, medium, high, critical

    # AI processing fields
    ai_category = db.Column(db.String(100))
    ai_confidence = db.Column(db.Float)
    ai_advice = db.Column(db.Text)
    ai_processed = db.Column(db.Boolean, default=False)
    ai_processed_at = db.Column(db.DateTime)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    comments = db.relationship('Comment', backref='report', lazy='dynamic', cascade='all, delete-orphan')
    tags = db.relationship('Tag', secondary=report_tags, backref=db.backref('reports', lazy='dynamic'))

    def __init__(self, title, description, user_id, location=None, latitude=None, 
                 longitude=None, image_url=None, is_public=True, severity='medium'):
        self.title = title
        self.description = description
        self.user_id = user_id
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.image_url = image_url
        self.is_public = is_public
        self.severity = severity

    def to_dict(self, include_comments=False, include_author=True):
        """Convert report to dictionary"""
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
            'severity': self.severity,
            'ai_category': self.ai_category,
            'ai_confidence': self.ai_confidence,
            'ai_advice': self.ai_advice,
            'ai_processed': self.ai_processed,
            'ai_processed_at': self.ai_processed_at.isoformat() if self.ai_processed_at else None,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'comments_count': self.comments.count(),
            'tags': [tag.to_dict() for tag in self.tags]
        }

        if include_author and hasattr(self, 'author'):
            data['author'] = self.author.to_dict()

        if include_comments:
            data['comments'] = [comment.to_dict() for comment in self.comments.order_by('created_at')]

        return data

    def add_tag(self, tag):
        """Add a tag to this report"""
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag):
        """Remove a tag from this report"""
        if tag in self.tags:
            self.tags.remove(tag)

    def mark_ai_processed(self, category=None, confidence=None, advice=None):
        """Mark report as processed by AI"""
        self.ai_processed = True
        self.ai_processed_at = datetime.utcnow()
        if category:
            self.ai_category = category
        if confidence is not None:
            self.ai_confidence = confidence
        if advice:
            self.ai_advice = advice

    @classmethod
    def get_public_reports(cls, limit=20, offset=0, status='active'):
        """Get public reports with pagination"""
        return cls.query.filter_by(is_public=True, status=status)\
                        .order_by(cls.created_at.desc())\
                        .limit(limit)\
                        .offset(offset)\
                        .all()

    @classmethod
    def get_by_user(cls, user_id, limit=20, offset=0):
        """Get reports by user"""
        return cls.query.filter_by(user_id=user_id)\
                        .order_by(cls.created_at.desc())\
                        .limit(limit)\
                        .offset(offset)\
                        .all()

    @classmethod
    def get_by_location(cls, latitude, longitude, radius_km=10):
        """Get reports within a radius of given coordinates"""
        # Simple bounding box calculation (for more accuracy, use PostGIS)
        lat_range = radius_km / 111.0  # Rough conversion
        lng_range = radius_km / (111.0 * abs(latitude))
        
        return cls.query.filter(
            cls.latitude.between(latitude - lat_range, latitude + lat_range),
            cls.longitude.between(longitude - lng_range, longitude + lng_range),
            cls.is_public == True,
            cls.status == 'active'
        ).all()

    def __repr__(self):
        return f'<Report {self.title}>'