from marshmallow import Schema, fields, validate

class ReportCreateSchema(Schema):
    title = fields.Str(
        required=True,
        validate=validate.Length(min=5, max=200, error_messages={
            "invalid": "Title must be between 5 and 200 characters."
        })
    )
    description = fields.Str(
        required=True,
        validate=validate.Length(min=10, max=2000, error_messages={
            "invalid": "Description must be between 10 and 2000 characters."
        })
    )
    location = fields.Str(validate=validate.Length(max=200))
    latitude = fields.Float(validate=validate.Range(min=-90, max=90))
    longitude = fields.Float(validate=validate.Range(min=-180, max=180))
    is_public = fields.Bool(default=True)

class ReportUpdateSchema(Schema):
    title = fields.Str(
        validate=validate.Length(min=5, max=200, error_messages={
            "invalid": "Title must be between 5 and 200 characters."
        })
    )
    description = fields.Str(
        validate=validate.Length(min=10, max=2000, error_messages={
            "invalid": "Description must be between 10 and 2000 characters."
        })
    )
    location = fields.Str(validate=validate.Length(max=200))
    latitude = fields.Float(validate=validate.Range(min=-90, max=90))
    longitude = fields.Float(validate=validate.Range(min=-180, max=180))
    is_public = fields.Bool()

class ReportSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)
    location = fields.Str(dump_only=True)
    latitude = fields.Float(dump_only=True)
    longitude = fields.Float(dump_only=True)
    image_url = fields.Str(dump_only=True)
    is_public = fields.Bool(dump_only=True)
    status = fields.Str(dump_only=True)
    ai_category = fields.Str(dump_only=True)
    ai_confidence = fields.Float(dump_only=True)
    ai_advice = fields.Str(dump_only=True)
    ai_processed = fields.Bool(dump_only=True)
    ai_processed_at = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    comments_count = fields.Int(dump_only=True)
    tags = fields.List(fields.Dict(), dump_only=True)

# Schema instances
report_create_schema = ReportCreateSchema()
report_update_schema = ReportUpdateSchema()
report_schema = ReportSchema()
reports_schema = ReportSchema(many=True)
