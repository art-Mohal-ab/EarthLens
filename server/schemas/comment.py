from marshmallow import Schema, fields, validate, validates, ValidationError

class CommentCreateSchema(Schema):
    content = fields.Str(required=True, validate=validate.Length(min=1, max=1000))
    parent_id = fields.Int(allow_none=True)
    user_id = fields.Int(required=True)
    report_id = fields.Int(required=True)

    @validates("content")
    def validate_content_not_blank(self, value):
        if not value.strip():
            raise ValidationError("Comment cannot be empty or only whitespace.")

class CommentUpdateSchema(Schema):
    content = fields.Str(required=True, validate=validate.Length(min=1, max=1000))

    @validates("content")
    def validate_content_not_blank(self, value):
        if not value.strip():
            raise ValidationError("Updated comment cannot be empty or only whitespace.")

class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    parent_id = fields.Int(dump_only=True)
    author = fields.Dict(dump_only=True)
    replies_count = fields.Int(dump_only=True)
    replies = fields.List(fields.Dict(), dump_only=True)

comment_create_schema = CommentCreateSchema()
comment_update_schema = CommentUpdateSchema()
comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
