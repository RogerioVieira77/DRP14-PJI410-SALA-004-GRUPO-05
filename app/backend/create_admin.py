#!/usr/bin/env python3
"""Script para criar usuário admin no SmartCEU"""

from app import create_app, db
from app.models.user import User

def create_admin():
    app = create_app()
    with app.app_context():
        # Verificar se admin já existe
        existing = User.query.filter_by(username='admin').first()
        if existing:
            print('⚠️  Usuário admin já existe!')
            print(f'   Username: {existing.username}')
            print(f'   Email: {existing.email}')
            return
        
        # Criar novo usuário admin
        user = User(username='admin', email='admin@smartceu.com')
        user.set_password('admin123')
        
        db.session.add(user)
        db.session.commit()
        
        print('✅ Usuário admin criado com sucesso!')
        print('   Username: admin')
        print('   Password: admin123')
        print('   Email: admin@smartceu.com')

if __name__ == '__main__':
    create_admin()
