from marshmallow import Schema, fields, validate


class CommentCreateSchema(Schema):
    content = fields.Str(required=True, validate=validate.Length(min=1, max=2000))
    report_id = fields.Int(required=True)
    parent_id = fields.Int()  # For nested comments/replies


class CommentUpdateSchema(Schema):
    content = fields.Str(required=True, validate=validate.Length(min=1, max=2000))