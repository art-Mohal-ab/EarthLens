from database.db import db, BaseModel

report_tags = db.Table(
    'report_tags',
    db.Column('report_id', db.Integer, db.ForeignKey('reports.id', ondelete='CASCADE'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)

class Tag(BaseModel):
    __tablename__ = 'tags'

    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.String(200))
    color = db.Column(db.String(7), default='#2d5016')  # Hex color code (green tone)

    # Many-to-many relationship with reports
    reports = db.relationship(
        'Report',
        secondary=report_tags,
        back_populates='tags',
        lazy='dynamic'
    )

    def __init__(self, name, description=None, color='#2d5016'):
        """Initialize Tag with lowercase, trimmed name."""
        self.name = name.lower().strip()
        self.description = description
        self.color = color

    def to_dict(self, include_reports_count=False):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'created_at': self.created_at.isoformat()
        }

        if include_reports_count:
            data['reports_count'] = self.reports.count()

        return data

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name.lower().strip()).first()

    @classmethod
    def get_or_create(cls, name, description=None, color='#2d5016'):
        tag = cls.find_by_name(name)
        if not tag:
            tag = cls(name=name, description=description, color=color)
            tag.save()
        return tag

    @classmethod
    def get_popular_tags(cls, limit=20):
        return (
            cls.query
            .join(report_tags)
            .group_by(cls.id)
            .order_by(db.func.count(report_tags.c.report_id).desc())
            .limit(limit)
            .all()
        )

    def __repr__(self):
        return f"<Tag name='{self.name}'>"
