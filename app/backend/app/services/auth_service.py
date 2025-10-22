"""
Service de Autenticação
Lógica de negócio relacionada a usuários e autenticação
"""

from flask_jwt_extended import create_access_token
from datetime import timedelta
from app import db
from app.models.user import User
from app.schemas.user_schema import (
    UserSchema, UserLoginSchema, UserRegisterSchema, UserUpdateSchema
)


class AuthService:
    """Serviço de autenticação e gerenciamento de usuários"""
    
    @staticmethod
    def login(username: str, password: str) -> dict:
        """
        Realizar login do usuário
        
        Args:
            username: Nome de usuário
            password: Senha
            
        Returns:
            dict: Dados do usuário e token JWT
            
        Raises:
            ValueError: Se credenciais inválidas ou conta desativada
        """
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.verify_password(password):
            raise ValueError('Credenciais inválidas')
        
        if not user.is_active:
            raise ValueError('Conta desativada')
        
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
        
        return {
            'access_token': access_token,
            'user': UserSchema().dump(user)
        }
    
    @staticmethod
    def register(data: dict) -> User:
        """
        Registrar novo usuário
        
        Args:
            data: Dados do usuário
            
        Returns:
            User: Usuário criado
            
        Raises:
            ValueError: Se username ou email já existem
        """
        # Validar se usuário já existe
        if User.query.filter_by(username=data['username']).first():
            raise ValueError('Username já existe')
        
        if User.query.filter_by(email=data['email']).first():
            raise ValueError('Email já está em uso')
        
        # Criar usuário
        user = User.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            full_name=data.get('full_name', ''),
            role=data.get('role', 'operator')
        )
        
        db.session.add(user)
        db.session.commit()
        
        return user
    
    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """
        Buscar usuário por ID
        
        Args:
            user_id: ID do usuário
            
        Returns:
            User: Usuário encontrado
            
        Raises:
            ValueError: Se usuário não encontrado
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError('Usuário não encontrado')
        return user
    
    @staticmethod
    def update_user(user_id: int, data: dict) -> User:
        """
        Atualizar dados do usuário
        
        Args:
            user_id: ID do usuário
            data: Dados para atualizar
            
        Returns:
            User: Usuário atualizado
            
        Raises:
            ValueError: Se usuário não encontrado
        """
        user = AuthService.get_user_by_id(user_id)
        
        # Atualizar campos
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        db.session.commit()
        return user
    
    @staticmethod
    def change_password(user_id: int, old_password: str, new_password: str) -> None:
        """
        Alterar senha do usuário
        
        Args:
            user_id: ID do usuário
            old_password: Senha antiga
            new_password: Nova senha
            
        Raises:
            ValueError: Se senha antiga incorreta
        """
        user = AuthService.get_user_by_id(user_id)
        
        if not user.verify_password(old_password):
            raise ValueError('Senha antiga incorreta')
        
        user.set_password(new_password)
        db.session.commit()
    
    @staticmethod
    def list_users() -> list:
        """
        Listar todos os usuários
        
        Returns:
            list: Lista de usuários
        """
        return User.query.all()
    
    @staticmethod
    def delete_user(user_id: int) -> None:
        """
        Deletar usuário
        
        Args:
            user_id: ID do usuário
            
        Raises:
            ValueError: Se usuário não encontrado
        """
        user = AuthService.get_user_by_id(user_id)
        db.session.delete(user)
        db.session.commit()
