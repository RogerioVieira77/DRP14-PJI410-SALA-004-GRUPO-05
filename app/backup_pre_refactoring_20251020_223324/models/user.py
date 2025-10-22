"""
User Model
Representa um usuário do sistema
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(db.Model):
    """
    Modelo de Usuário
    
    Para autenticação e autorização no sistema
    """
    __tablename__ = 'users'
    
    # Campos principais
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Informações pessoais
    full_name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    
    # Role e permissões
    role = db.Column(
        db.Enum('admin', 'operator', 'viewer', name='user_role'),
        default='viewer',
        nullable=False,
        index=True
    )
    
    # Status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    
    # Login tracking
    last_login = db.Column(db.DateTime)
    login_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Define o hash da senha"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica se a senha está correta"""
        return check_password_hash(self.password_hash, password)
    
    def verify_password(self, password):
        """Alias para check_password (para compatibilidade)"""
        return self.check_password(password)
    
    def update_last_login(self):
        """Atualiza o último login do usuário"""
        from datetime import datetime
        self.last_login = datetime.utcnow()
        if self.login_count is None:
            self.login_count = 0
        self.login_count += 1
    
    def to_dict(self, include_sensitive=False):
        """
        Converte o usuário para dicionário
        
        Args:
            include_sensitive: Incluir dados sensíveis (para admin)
        
        Returns:
            dict: Representação do usuário
        """
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email if include_sensitive else self._mask_email(),
            'full_name': self.full_name,
            'role': self.role,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat()
        }
        
        if include_sensitive:
            data.update({
                'phone': self.phone,
                'last_login': self.last_login.isoformat() if self.last_login else None,
                'login_count': self.login_count,
                'updated_at': self.updated_at.isoformat()
            })
        
        return data
    
    def _mask_email(self):
        """Mascara o email para privacidade"""
        if not self.email:
            return None
        
        parts = self.email.split('@')
        if len(parts) != 2:
            return self.email
        
        name = parts[0]
        domain = parts[1]
        
        if len(name) <= 2:
            masked_name = name[0] + '*'
        else:
            masked_name = name[0] + '*' * (len(name) - 2) + name[-1]
        
        return f"{masked_name}@{domain}"
    
    def record_login(self):
        """Registra um login bem-sucedido"""
        self.last_login = datetime.utcnow()
        self.login_count += 1
    
    def has_permission(self, required_role):
        """
        Verifica se o usuário tem permissão para determinado role
        
        Args:
            required_role: Role necessário
        
        Returns:
            bool: True se tem permissão
        """
        role_hierarchy = {
            'viewer': 0,
            'operator': 1,
            'admin': 2
        }
        
        user_level = role_hierarchy.get(self.role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        
        return user_level >= required_level and self.is_active
    
    @classmethod
    def get_by_username(cls, username):
        """Busca usuário pelo username"""
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def get_by_email(cls, email):
        """Busca usuário pelo email"""
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def create_user(cls, username, email, password, role='viewer', full_name=None):
        """
        Cria um novo usuário
        
        Args:
            username: Nome de usuário
            email: Email
            password: Senha em texto plano (será hashada)
            role: Role do usuário
            full_name: Nome completo (opcional)
        
        Returns:
            User: Nova instância de usuário
        """
        user = cls(
            username=username,
            email=email,
            role=role,
            full_name=full_name
        )
        user.set_password(password)
        
        return user
