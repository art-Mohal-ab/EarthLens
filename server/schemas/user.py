from marshmallow import Schema, fields, validate, validates, ValidationError

class UserRegisterSchema(Schema):
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=80, error_messages={
            "invalid": "Username must be between 3 and 80 characters."
        })
    )
    email = fields.Email(required=True)
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6, error_messages={
            "invalid": "Password must be at least 6 characters long."
        })
    )

    @validates("username")
    def validate_username(self, value):
        if not value.strip():
            raise ValidationError("Username cannot be empty or only whitespace.")
        if ' ' in value:
            raise ValidationError("Username cannot contain spaces.")

class UserLoginSchema(Schema):
    username_or_email = fields.Str(required=True)
    password = fields.Str(required=True)

class UserUpdateSchema(Schema):
    username = fields.Str(
        validate=validate.Length(min=3, max=80, error_messages={
            "invalid": "Username must be between 3 and 80 characters."
        })
    )
    email = fields.Email()
    current_password = fields.Str()
    new_password = fields.Str(
        validate=validate.Length(min=6, error_messages={
            "invalid": "New password must be at least 6 characters long."
        })
    )

    @validates("username")
    def validate_username(self, value):
        if value and not value.strip():
            raise ValidationError("Username cannot be empty or only whitespace.")
        if value and ' ' in value:
            raise ValidationError("Username cannot contain spaces.")

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(dump_only=True)
    email = fields.Str(dump_only=True)
    is_active = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

# Schema instances
user_register_schema = UserRegisterSchema()
user_login_schema = UserLoginSchema()
user_update_schema = UserUpdateSchema()
user_schema = UserSchema()
users_schema = UserSchema(many=True)
