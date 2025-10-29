from marshmallow import Schema, fields, validate, validates, ValidationError
from app.models.user import User


class UserRegistrationSchema(Schema):
    username = fields.Str(
        required=True,
        validate=[
            validate.Length(min=3, max=80),
            validate.Regexp(
                r'^[a-zA-Z0-9_-]+$',
                error="Username can only contain letters, numbers, underscores, and hyphens"
            )
        ]
    )
    email = fields.Email(
        required=True,
        validate=validate.Length(max=120)
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6),
        load_only=True
    )

    @validates('username')
    def validate_username_unique(self, value):
        if User.find_by_username(value):
            raise ValidationError('Username already exists.')

    @validates('email')
    def validate_email_unique(self, value):
        if User.find_by_email(value):
            raise ValidationError('Email already registered.')


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class UserProfileSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(dump_only=True)
    email = fields.Email(dump_only=True)
    is_active = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    reports_count = fields.Int(dump_only=True)
    comments_count = fields.Int(dump_only=True)


class UserUpdateSchema(Schema):
    username = fields.Str(
        validate=[
            validate.Length(min=3, max=80),
            validate.Regexp(
                r'^[a-zA-Z0-9_-]+$',
                error="Username can only contain letters, numbers, underscores, and hyphens"
            )
        ]
    )
    email = fields.Email(
        validate=validate.Length(max=120)
    )
    current_password = fields.Str(load_only=True)
    new_password = fields.Str(
        validate=validate.Length(min=6),
        load_only=True
    )


class PasswordResetSchema(Schema):
    email = fields.Email(required=True)


class PasswordResetConfirmSchema(Schema):
    token = fields.Str(required=True)
    new_password = fields.Str(
        required=True,
        validate=validate.Length(min=6),
        load_only=True
    )


# Schema instances
user_registration_schema = UserRegistrationSchema()
user_login_schema = UserLoginSchema()
user_profile_schema = UserProfileSchema()
user_update_schema = UserUpdateSchema()
password_reset_schema = PasswordResetSchema()
password_reset_confirm_schema = PasswordResetConfirmSchema()
