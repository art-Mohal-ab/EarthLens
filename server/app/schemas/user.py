from marshmallow import Schema, fields, validate, validates, ValidationError
import re


class UserRegistrationSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    first_name = fields.Str(validate=validate.Length(max=50))
    last_name = fields.Str(validate=validate.Length(max=50))

    @validates('username')
    def validate_username(self, value, **kwargs):
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise ValidationError('Username can only contain letters, numbers, and underscores')

    @validates('password')
    def validate_password(self, value, **kwargs):
        if not re.search(r'[A-Z]', value):
            raise ValidationError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', value):
            raise ValidationError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', value):
            raise ValidationError('Password must contain at least one number')


class UserLoginSchema(Schema):
    email = fields.Str(required=True)  # Can be email or username
    password = fields.Str(required=True)


class UserUpdateSchema(Schema):
    username = fields.Str(validate=validate.Length(min=3, max=80))
    email = fields.Email()
    first_name = fields.Str(validate=validate.Length(max=50))
    last_name = fields.Str(validate=validate.Length(max=50))
    bio = fields.Str(validate=validate.Length(max=500))
    current_password = fields.Str()
    new_password = fields.Str(validate=validate.Length(min=8))

    @validates('username')
    def validate_username(self, value, **kwargs):
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise ValidationError('Username can only contain letters, numbers, and underscores')

    @validates('new_password')
    def validate_new_password(self, value, **kwargs):
        if not re.search(r'[A-Z]', value):
            raise ValidationError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', value):
            raise ValidationError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', value):
            raise ValidationError('Password must contain at least one number')


class PasswordResetSchema(Schema):
    email = fields.Email(required=True)


class PasswordResetConfirmSchema(Schema):
    token = fields.Str(required=True)
    new_password = fields.Str(required=True, validate=validate.Length(min=8))

    @validates('new_password')
    def validate_new_password(self, value, **kwargs):
        if not re.search(r'[A-Z]', value):
            raise ValidationError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', value):
            raise ValidationError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', value):
            raise ValidationError('Password must contain at least one number')


# Schema instances
user_registration_schema = UserRegistrationSchema()
user_login_schema = UserLoginSchema()
user_update_schema = UserUpdateSchema()
password_reset_schema = PasswordResetSchema()
password_reset_confirm_schema = PasswordResetConfirmSchema()
