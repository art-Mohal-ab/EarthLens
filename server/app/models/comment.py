from database import db, BaseModel

class Comment(BaseModel):
    __tablename__ = 'comments'
    
    content = db.Column(db.Text, nullable=False)
    

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_comment_user'), nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id', name='fk_comment_report'), nullable=False)
    

    author = db.relationship('User', backref='comments')
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
            'report_id': self.report_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'author': {
                'id': self.author.id,
                'username': self.author.username
            } if self.author else None
        }
    
    def __repr__(self):
        return f'<Comment {self.id}>'