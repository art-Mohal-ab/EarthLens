from marshmallow import Schema, fields, validate, validates, ValidationError


class ReportCreateSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=5, max=200))
    description = fields.Str(required=True, validate=validate.Length(min=10, max=5000))
    location = fields.Str(validate=validate.Length(max=200))
    latitude = fields.Float(validate=validate.Range(min=-90, max=90))
    longitude = fields.Float(validate=validate.Range(min=-180, max=180))
    image_url = fields.Url()
    is_public = fields.Bool(missing=True)
    severity = fields.Str(validate=validate.OneOf(['low', 'medium', 'high', 'critical']), missing='medium')
    tags = fields.List(fields.Str(validate=validate.Length(min=1, max=50)))

    @validates('tags')
    def validate_tags(self, value):
        if len(value) > 10:
            raise ValidationError('Maximum 10 tags allowed')


class ReportUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=5, max=200))
    description = fields.Str(validate=validate.Length(min=10, max=5000))
    location = fields.Str(validate=validate.Length(max=200))
    latitude = fields.Float(validate=validate.Range(min=-90, max=90))
    longitude = fields.Float(validate=validate.Range(min=-180, max=180))
    image_url = fields.Url()
    is_public = fields.Bool()
    severity = fields.Str(validate=validate.OneOf(['low', 'medium', 'high', 'critical']))
    status = fields.Str(validate=validate.OneOf(['active', 'resolved', 'archived', 'draft']))
    tags = fields.List(fields.Str(validate=validate.Length(min=1, max=50)))

    @validates('tags')
    def validate_tags(self, value):
        if len(value) > 10:
            raise ValidationError('Maximum 10 tags allowed')


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
    limit = fields.Int(validate=validate.Range(min=1, max=100))
    offset = fields.Int(validate=validate.Range(min=0))
    sort_by = fields.Str(validate=validate.OneOf(['created_at', 'updated_at', 'title']))
    sort_order = fields.Str(validate=validate.OneOf(['asc', 'desc']))

# schema instances
report_create_schema = ReportCreateSchema()
report_update_schema = ReportUpdateSchema()
report_schema = ReportSchema()
report_filter_schema = ReportFilterSchema()
