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