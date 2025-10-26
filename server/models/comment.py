from database import db, BaseModel

class Comment(BaseModel):
    __tablename__ = 'comments'

    content = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'), nullable=False)

    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    replies = db.relationship(
        'Comment',
        backref=db.backref('parent', remote_side='Comment.id'),
        lazy='dynamic'
    )

    user = db.relationship('User', backref=db.backref('comments', lazy='dynamic'))
    report = db.relationship('Report', backref=db.backref('comments', lazy='dynamic'))

    def __init__(self, content, user_id, report_id, parent_id=None):
        self.content = content
        self.user_id = user_id
        self.report_id = report_id
        self.parent_id = parent_id

    def to_dict(self, include_author=True, include_replies=False):
        data = {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'parent_id': self.parent_id
        }

        if include_author and self.user:
            data['author'] = {
                'id': self.user.id,
                'username': self.user.username
            }

        if include_replies:
            data['replies_count'] = self.replies.count()
            data['replies'] = [r.to_dict(include_replies=False) for r in self.replies.limit(3)]

        return data

    @classmethod
    def get_report_comments(cls, report_id, limit=20, offset=0):
        return cls.query.filter_by(report_id=report_id, parent_id=None)\
                        .order_by(cls.created_at.desc())\
                        .limit(limit)\
                        .offset(offset)\
                        .all()

    def __repr__(self):
        return f'<Comment {self.id}>'
