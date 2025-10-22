"""
Authentication Routes
Endpoints para autenticação e gerenciamento de usuários
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from app import db
from app.models.user import User
from datetime import timedelta

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['POST'])
def register():
    """
    Registrar novo usuário
    
    Payload:
    {
        "username": "string",
        "email": "string",
        "password": "string",
        "full_name": "string"
    }
    """
    data = request.get_json()
    
    # Validar dados obrigatórios
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo {field} é obrigatório'}), 400
    
    # Verificar se usuário já existe
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username já existe'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email já está em uso'}), 400
    
    # Criar usuário
    try:
        user = User.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            full_name=data.get('full_name', ''),
            role=data.get('role', 'operator')
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Usuário criado com sucesso',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/login', methods=['POST'])
def login():
    """
    Login de usuário
    
    Payload:
    {
        "username": "string",
        "password": "string"
    }
    """
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username e password são obrigatórios'}), 400
    
    # Buscar usuário
    user = User.query.filter_by(username=username).first()
    
    if not user or not user.verify_password(password):
        return jsonify({'error': 'Credenciais inválidas'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Conta desativada'}), 401
    
    # Atualizar último login
    user.update_last_login()
    db.session.commit()
    
    # Criar token JWT
    additional_claims = {
        'role': user.role,
        'email': user.email
    }
    
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims=additional_claims,
        expires_delta=timedelta(hours=24)
    )
    
    return jsonify({
        'message': 'Login realizado com sucesso',
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'full_name': user.full_name
        }
    }), 200


@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Obter informações do usuário atual (autenticado)
    Requer token JWT válido
    """
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'full_name': user.full_name,
        'is_active': user.is_active,
        'is_verified': user.is_verified,
        'created_at': user.created_at.isoformat(),
        'last_login': user.last_login.isoformat() if user.last_login else None
    }), 200


@bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """
    Alterar senha do usuário atual
    
    Payload:
    {
        "old_password": "string",
        "new_password": "string"
    }
    """
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    if not old_password or not new_password:
        return jsonify({'error': 'Senhas antigas e nova são obrigatórias'}), 400
    
    # Verificar senha antiga
    if not user.verify_password(old_password):
        return jsonify({'error': 'Senha antiga incorreta'}), 401
    
    # Atualizar senha
    try:
        user.set_password(new_password)
        db.session.commit()
        
        return jsonify({'message': 'Senha alterada com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout do usuário
    (No JWT, o logout é feito no client removendo o token)
    """
    return jsonify({'message': 'Logout realizado com sucesso'}), 200


# Rotas administrativas (apenas admin)

@bp.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    """
    Listar todos os usuários (apenas admin)
    """
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Acesso negado. Apenas administradores.'}), 403
    
    users = User.query.all()
    
    return jsonify({
        'users': [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'full_name': user.full_name,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat()
        } for user in users]
    }), 200


@bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """
    Deletar usuário (apenas admin)
    """
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Acesso negado. Apenas administradores.'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    try:
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'Usuário deletado com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
