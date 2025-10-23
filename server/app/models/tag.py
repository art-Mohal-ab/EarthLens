from database import db, BaseModel

class Tag(BaseModel):
    __tablename__ = 'tags'
    
    name = db.Column(db.String(50), unique=True, nullable=False)
    

    reports = db.relationship('Report', secondary='report_tags', back_populates='tags')
    
    @classmethod
    def get_or_create(cls, name):
        tag = cls.query.filter_by(name=name).first()
        if not tag:
            tag = cls(name=name)
            tag.save()
        return tag
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Tag {self.name}>'


report_tags = db.Table('report_tags',
    db.Column('report_id', db.Integer, db.ForeignKey('reports.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)