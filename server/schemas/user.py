from marshmallow import Schema, fields, validate, validates, ValidationError

class UserRegisterSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))

    @validates('username')
    def validate_username(self, value):
        if not value.replace('_', '').replace('-', '').isalnum():
            raise ValidationError('Username can only contain letters, numbers, underscores, and hyphens.')

class UserLoginSchema(Schema):
    username_or_email = fields.Str(required=True)
    password = fields.Str(required=True)

class UserUpdateSchema(Schema):
    username = fields.Str(validate=validate.Length(min=3, max=50))
    email = fields.Email()
    current_password = fields.Str()
    new_password = fields.Str(validate=validate.Length(min=6))

    @validates('username')
    def validate_username(self, value):
        if not value.replace('_', '').replace('-', '').isalnum():
            raise ValidationError('Username can only contain letters, numbers, underscores, and hyphens.')

user_register_schema = UserRegisterSchema()
user_login_schema = UserLoginSchema()
user_update_schema = UserUpdateSchema()
