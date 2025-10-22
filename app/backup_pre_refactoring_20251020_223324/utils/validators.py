"""
Validadores de requisição
"""

from flask import request
from functools import wraps
from marshmallow import Schema, ValidationError


def validate_request_json(schema: Schema, partial: bool = False):
    """
    Decorator para validar JSON da requisição
    
    Args:
        schema: Schema Marshmallow para validação
        partial: Se True, permite validação parcial
        
    Usage:
        @validate_request_json(UserSchema())
        def create_user():
            data = request.validated_data
            ...
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            json_data = request.get_json()
            
            if not json_data:
                raise ValidationError({'_error': 'Request body deve ser JSON'})
            
            try:
                validated_data = schema.load(json_data, partial=partial)
                request.validated_data = validated_data
            except ValidationError as err:
                raise err
            
            return f(*args, **kwargs)
        
        return wrapper
    return decorator
