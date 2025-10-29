from app.database import db, BaseModel


class Comment(BaseModel):
    __tablename__ = 'comments'
    
    content = db.Column(db.Text, nullable=False)
    is_edited = db.Column(db.Boolean, default=False)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))  # For nested comments
    
    # Relationships
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side='Comment.id'), lazy='dynamic')
    
    def __init__(self, content, user_id, report_id, parent_id=None):
        self.content = content
        self.user_id = user_id
        self.report_id = report_id
        self.parent_id = parent_id
    
    def to_dict(self, include_author=True, include_replies=False):
        """Convert comment to dictionary"""
        data = {
            'id': self.id,
            'content': self.content,
            'is_edited': self.is_edited,
            'user_id': self.user_id,
            'report_id': self.report_id,
            'parent_id': self.parent_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'replies_count': self.replies.count()
        }
        
        if include_author and hasattr(self, 'author'):
            data['author'] = {
                'id': self.author.id,
                'username': self.author.username,
                'full_name': self.author.full_name,
                'avatar_url': self.author.avatar_url
            }
        
        if include_replies:
            data['replies'] = [reply.to_dict(include_author=True) for reply in self.replies.order_by('created_at')]
        
        return data
    
    def edit_content(self, new_content):
        """Edit comment content"""
        self.content = new_content
        self.is_edited = True
        self.save()
    
    @classmethod
    def get_by_report(cls, report_id, include_replies=True):
        """Get comments for a report"""
        if include_replies:
            return cls.query.filter_by(report_id=report_id, parent_id=None)\
                           .order_by(cls.created_at.desc()).all()
        else:
            return cls.query.filter_by(report_id=report_id)\
                           .order_by(cls.created_at.desc()).all()
    
    def __repr__(self):
        return f'<Comment {self.id} by User {self.user_id}>'