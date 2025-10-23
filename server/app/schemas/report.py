from marshmallow import Schema, fields, validate, validates, ValidationError, post_load
from models.report import Report

class ReportCreateSchema(Schema):
    title = fields.Str(
        required=True,
        validate=validate.Length(min=5, max=200, error="Title must be between 5 and 200 characters")
    )
    description = fields.Str(
        required=True,
        validate=validate.Length(min=10, max=2000, error="Description must be between 10 and 2000 characters")
    )
    location = fields.Str(
        validate=validate.Length(max=200, error="Location must be less than 200 characters")
    )
    latitude = fields.Float(
        validate=validate.Range(min=-90, max=90, error="Latitude must be between -90 and 90")
    )
    longitude = fields.Float(
        validate=validate.Range(min=-180, max=180, error="Longitude must be between -180 and 180")
    )
    is_public = fields.Bool(missing=True)
    tags = fields.List(fields.Str(), missing=[])

class ReportUpdateSchema(Schema):
    title = fields.Str(
        validate=validate.Length(min=5, max=200, error="Title must be between 5 and 200 characters")
    )
    description = fields.Str(
        validate=validate.Length(min=10, max=2000, error="Description must be between 10 and 2000 characters")
    )
    location = fields.Str(
        validate=validate.Length(max=200, error="Location must be less than 200 characters")
    )
    latitude = fields.Float(
        validate=validate.Range(min=-90, max=90, error="Latitude must be between -90 and 90")
    )
    longitude = fields.Float(
        validate=validate.Range(min=-180, max=180, error="Longitude must be between -180 and 180")
    )
    is_public = fields.Bool()
    tags = fields.List(fields.Str())

class ReportSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)
    location = fields.Str(dump_only=True)
    latitude = fields.Float(dump_only=True)
    longitude = fields.Float(dump_only=True)
    image_url = fields.Str(dump_only=True)
    ai_category = fields.Str(dump_only=True)
    ai_confidence = fields.Float(dump_only=True)
    ai_advice = fields.Str(dump_only=True)
    ai_processed = fields.Bool(dump_only=True)
    status = fields.Str(dump_only=True)
    is_public = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    author = fields.Dict(dump_only=True)
    tags = fields.List(fields.Dict(), dump_only=True)
    comments_count = fields.Int(dump_only=True)

class ReportFilterSchema(Schema):
    category = fields.Str()
    location = fields.Str()
    author_id = fields.Int()
    tags = fields.List(fields.Str())
    status = fields.Str(validate=validate.OneOf(['active', 'archived', 'flagged']))
    is_public = fields.Bool()
    limit = fields.Int(validate=validate.Range(min=1, max=100), missing=20)
    offset = fields.Int(validate=validate.Range(min=0), missing=0)
    sort_by = fields.Str(validate=validate.OneOf(['created_at', 'updated_at', 'title']), missing='created_at')
    sort_order = fields.Str(validate=validate.OneOf(['asc', 'desc']), missing='desc')

# schema instances
report_create_schema = ReportCreateSchema()
report_update_schema = ReportUpdateSchema()
report_schema = ReportSchema()
report_filter_schema = ReportFilterSchema()