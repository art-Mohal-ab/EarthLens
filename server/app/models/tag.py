from app.database import db, BaseModel


class Tag(BaseModel):
    __tablename__ = 'tags'
    
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    color = db.Column(db.String(7), default='#007bff')  # Hex color code
    is_active = db.Column(db.Boolean, default=True)
    
    def __init__(self, name, description=None, color='#007bff'):
        self.name = name.lower().strip()  # Normalize tag names
        self.description = description
        self.color = color
    
    def to_dict(self):
        """Convert tag to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'is_active': self.is_active,
            'reports_count': len(self.reports),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def get_or_create(cls, name, description=None, color='#007bff'):
        """Get existing tag or create new one"""
        normalized_name = name.lower().strip()
        tag = cls.query.filter_by(name=normalized_name).first()
        
        if not tag:
            tag = cls(name=normalized_name, description=description, color=color)
            tag.save()
        
        return tag
    
    @classmethod
    def get_popular_tags(cls, limit=10):
        """Get most popular tags by report count"""
        from app.models.report import report_tags
        
        return db.session.query(cls)\
                        .join(report_tags)\
                        .group_by(cls.id)\
                        .order_by(db.func.count(report_tags.c.report_id).desc())\
                        .limit(limit)\
                        .all()
    
    @classmethod
    def search_tags(cls, query, limit=10):
        """Search tags by name"""
        return cls.query.filter(
            cls.name.contains(query.lower()),
            cls.is_active == True
        ).limit(limit).all()
    
    def __repr__(self):
        return f'<Tag {self.name}>'