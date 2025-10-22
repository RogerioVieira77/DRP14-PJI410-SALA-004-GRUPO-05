"""
Decorators personalizados
"""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt


def role_required(*allowed_roles):
    """
    Decorator para verificar role do usuário
    
    Args:
        allowed_roles: Roles permitidas
        
    Usage:
        @role_required('admin', 'operator')
        def sensitive_endpoint():
            ...
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get('role')
            
            if user_role not in allowed_roles:
                return jsonify({
                    'error': 'Acesso negado',
                    'details': f'Requer uma das roles: {", ".join(allowed_roles)}'
                }), 403
            
            return f(*args, **kwargs)
        
        return wrapper
    return decorator


def admin_required(f):
    """
    Decorator para verificar se usuário é admin
    
    Usage:
        @admin_required
        def admin_endpoint():
            ...
    """
    return role_required('admin')(f)
