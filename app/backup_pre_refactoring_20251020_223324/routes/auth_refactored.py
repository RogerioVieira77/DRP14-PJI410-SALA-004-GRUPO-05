"""
Authentication Routes (Refatorado)
Endpoints para autenticação e gerenciamento de usuários
"""

from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import AuthService
from app.schemas.user_schema import (
    UserSchema, UserLoginSchema, UserRegisterSchema, 
    UserUpdateSchema, ChangePasswordSchema
)
from app.utils.validators import validate_request_json
from app.utils.responses import success_response, error_response
from app.utils.decorators import admin_required

bp = Blueprint('auth', __name__)

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@bp.route('/register', methods=['POST'])
@validate_request_json(UserRegisterSchema())
def register():
    """
    Registrar novo usuário
    
    Body:
        username (str): Nome de usuário (mín. 3 caracteres)
        email (str): Email válido
        password (str): Senha (mín. 6 caracteres)
        full_name (str, opcional): Nome completo
        phone (str, opcional): Telefone
        role (str, opcional): Papel (admin, operator, viewer)
    
    Returns:
        201: Usuário criado com sucesso
        400: Dados inválidos
    """
    from flask import request
    
    try:
        user = AuthService.register(request.validated_data)
        return success_response(
            {'user': user_schema.dump(user)},
            message='Usuário criado com sucesso',
            status=201
        )
    except ValueError as e:
        return error_response(str(e), 400)


@bp.route('/login', methods=['POST'])
@validate_request_json(UserLoginSchema())
def login():
    """
    Login de usuário
    
    Body:
        username (str): Nome de usuário
        password (str): Senha
    
    Returns:
        200: Login bem-sucedido com token JWT
        401: Credenciais inválidas
    """
    from flask import request
    
    try:
        result = AuthService.login(
            request.validated_data['username'],
            request.validated_data['password']
        )
        return success_response(
            result,
            message='Login realizado com sucesso'
        )
    except ValueError as e:
        return error_response(str(e), 401)


@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Obter informações do usuário atual
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        200: Dados do usuário
        404: Usuário não encontrado
    """
    try:
        user_id = int(get_jwt_identity())
        user = AuthService.get_user_by_id(user_id)
        return success_response(user_schema.dump(user))
    except ValueError as e:
        return error_response(str(e), 404)


@bp.route('/change-password', methods=['POST'])
@jwt_required()
@validate_request_json(ChangePasswordSchema())
def change_password():
    """
    Alterar senha do usuário
    
    Headers:
        Authorization: Bearer <token>
    
    Body:
        old_password (str): Senha antiga
        new_password (str): Nova senha (mín. 6 caracteres, 1 maiúscula, 1 número)
    
    Returns:
        200: Senha alterada com sucesso
        401: Senha antiga incorreta
    """
    from flask import request
    
    try:
        user_id = int(get_jwt_identity())
        AuthService.change_password(
            user_id,
            request.validated_data['old_password'],
            request.validated_data['new_password']
        )
        return success_response(
            {},
            message='Senha alterada com sucesso'
        )
    except ValueError as e:
        return error_response(str(e), 401)


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout do usuário
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        200: Logout bem-sucedido
    
    Note:
        No JWT, o logout é gerenciado pelo client (remover token)
    """
    return success_response(
        {},
        message='Logout realizado com sucesso'
    )


# Rotas administrativas

@bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def list_users():
    """
    Listar todos os usuários (admin only)
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        200: Lista de usuários
        403: Acesso negado
    """
    users = AuthService.list_users()
    return success_response({
        'users': users_schema.dump(users),
        'count': len(users)
    })


@bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_user(user_id):
    """
    Obter usuário por ID (admin only)
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        200: Dados do usuário
        404: Usuário não encontrado
    """
    try:
        user = AuthService.get_user_by_id(user_id)
        return success_response(user_schema.dump(user))
    except ValueError as e:
        return error_response(str(e), 404)


@bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@admin_required
@validate_request_json(UserUpdateSchema(), partial=True)
def update_user(user_id):
    """
    Atualizar usuário (admin only)
    
    Headers:
        Authorization: Bearer <token>
    
    Body:
        email (str, opcional): Novo email
        full_name (str, opcional): Novo nome completo
        phone (str, opcional): Novo telefone
        role (str, opcional): Novo papel
        is_active (bool, opcional): Status ativo
    
    Returns:
        200: Usuário atualizado
        404: Usuário não encontrado
    """
    from flask import request
    
    try:
        user = AuthService.update_user(user_id, request.validated_data)
        return success_response(
            user_schema.dump(user),
            message='Usuário atualizado com sucesso'
        )
    except ValueError as e:
        return error_response(str(e), 404)


@bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    """
    Deletar usuário (admin only)
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        200: Usuário deletado
        404: Usuário não encontrado
    """
    try:
        AuthService.delete_user(user_id)
        return success_response(
            {},
            message='Usuário deletado com sucesso'
        )
    except ValueError as e:
        return error_response(str(e), 404)
