"""
Schema de validação para User
"""

from marshmallow import Schema, fields, validate, validates, ValidationError


class UserSchema(Schema):
    """Schema completo do usuário"""
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    full_name = fields.Str(validate=validate.Length(max=100))
    phone = fields.Str(validate=validate.Length(max=20))
    role = fields.Str(validate=validate.OneOf(['admin', 'operator', 'viewer']))
    is_active = fields.Bool(dump_only=True)
    is_verified = fields.Bool(dump_only=True)
    login_count = fields.Int(dump_only=True)
    last_login = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class UserLoginSchema(Schema):
    """Schema para login"""
    username = fields.Str(required=True, validate=validate.Length(min=3))
    password = fields.Str(required=True, validate=validate.Length(min=6))


class UserRegisterSchema(Schema):
    """Schema para registro de novo usuário"""
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6, max=100))
    full_name = fields.Str(validate=validate.Length(max=100))
    phone = fields.Str(validate=validate.Length(max=20))
    role = fields.Str(
        validate=validate.OneOf(['admin', 'operator', 'viewer']),
        load_default='operator'
    )

    @validates('username')
    def validate_username(self, value):
        """Validar que username não contém caracteres especiais"""
        if not value.replace('_', '').replace('-', '').isalnum():
            raise ValidationError('Username pode conter apenas letras, números, _ e -')


class UserUpdateSchema(Schema):
    """Schema para atualização de usuário"""
    email = fields.Email()
    full_name = fields.Str(validate=validate.Length(max=100))
    phone = fields.Str(validate=validate.Length(max=20))
    role = fields.Str(validate=validate.OneOf(['admin', 'operator', 'viewer']))
    is_active = fields.Bool()


class ChangePasswordSchema(Schema):
    """Schema para mudança de senha"""
    old_password = fields.Str(required=True, validate=validate.Length(min=6))
    new_password = fields.Str(required=True, validate=validate.Length(min=6, max=100))

    @validates('new_password')
    def validate_new_password(self, value):
        """Validar complexidade da senha"""
        if not any(c.isupper() for c in value):
            raise ValidationError('Senha deve conter ao menos uma letra maiúscula')
        if not any(c.isdigit() for c in value):
            raise ValidationError('Senha deve conter ao menos um número')
