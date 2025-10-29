from marshmallow import Schema, fields, validate, validates, ValidationError
import re


class TagCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    description = fields.Str(validate=validate.Length(max=200))
    color = fields.Str(validate=validate.Length(equal=7))  # Hex color code
    
    @validates('name')
    def validate_name(self, value):
        if not re.match(r'^[a-zA-Z0-9\s\-_]+$', value):
            raise ValidationError('Tag name can only contain letters, numbers, spaces, hyphens, and underscores')
    
    @validates('color')
    def validate_color(self, value):
        if not re.match(r'^#[0-9A-Fa-f]{6}$', value):
            raise ValidationError('Color must be a valid hex color code (e.g., #007bff)')


class TagUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=50))
    description = fields.Str(validate=validate.Length(max=200))
    color = fields.Str(validate=validate.Length(equal=7))
    is_active = fields.Bool()
    
    @validates('name')
    def validate_name(self, value):
        if not re.match(r'^[a-zA-Z0-9\s\-_]+$', value):
            raise ValidationError('Tag name can only contain letters, numbers, spaces, hyphens, and underscores')
    
    @validates('color')
    def validate_color(self, value):
        if not re.match(r'^#[0-9A-Fa-f]{6}$', value):
            raise ValidationError('Color must be a valid hex color code (e.g., #007bff)')