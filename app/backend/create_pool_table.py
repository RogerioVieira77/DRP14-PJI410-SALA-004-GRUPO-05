"""
Script para criar a tabela pool_readings usando SQLAlchemy
"""
import sys
sys.path.insert(0, 'C:\\PI - IV - V1\\backend')

from app import create_app, db
from app.models.pool_reading import PoolReading

print("=" * 60)
print("Criando tabela pool_readings...")
print("=" * 60)

app = create_app('development')

with app.app_context():
    # Criar apenas a tabela pool_readings
    db.create_all()
    print("✅ Tabela pool_readings criada com sucesso!")
    
    # Verificar se existe
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    
    if 'pool_readings' in tables:
        print("✅ Tabela pool_readings confirmada no banco de dados")
        columns = inspector.get_columns('pool_readings')
        print(f"\n📋 Colunas da tabela ({len(columns)}):")
        for col in columns:
            print(f"   - {col['name']}: {col['type']}")
    else:
        print("❌ Tabela pool_readings NÃO foi criada")

print("\n" + "=" * 60)
print("Concluído!")
print("=" * 60)
