"""
Script para inicializar o banco de dados
Cria todas as tabelas necessárias
"""

import sys
import os

# Adicionar o diretório backend ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar app e db
from app import create_app, db

print("=" * 60)
print("Inicializando banco de dados - CEU Tres Pontes")
print("=" * 60)

# Criar aplicação
app = create_app('development')

# Criar contexto da aplicação
with app.app_context():
    print("\n📊 Criando tabelas no banco de dados...")
    
    try:
        # Criar todas as tabelas
        db.create_all()
        
        print("✅ Tabelas criadas com sucesso!\n")
        
        # Listar tabelas criadas
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"📋 Tabelas criadas ({len(tables)}):")
        for table in tables:
            print(f"  - {table}")
        
        print("\n" + "=" * 60)
        print("✅ Banco de dados inicializado com sucesso!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erro ao criar tabelas: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
