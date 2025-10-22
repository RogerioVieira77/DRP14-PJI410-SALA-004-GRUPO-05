"""
Script para adicionar a coluna full_name na tabela users
"""
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

print("=== CORRIGINDO TABELA USERS ===\n")

# Conexão
connection = pymysql.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    port=int(os.getenv('DB_PORT', 3306)),
    user=os.getenv('DB_USER', 'ceu_tres_pontes'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME', 'ceu_tres_pontes_db'),
    charset='utf8mb4'
)

cursor = connection.cursor()

try:
    # Adicionar coluna full_name
    print("📝 Adicionando coluna full_name...")
    cursor.execute("""
        ALTER TABLE users 
        ADD COLUMN full_name VARCHAR(120) AFTER password_hash
    """)
    print("✅ Coluna full_name adicionada")
    
    # Adicionar coluna phone
    print("📝 Adicionando coluna phone...")
    cursor.execute("""
        ALTER TABLE users 
        ADD COLUMN phone VARCHAR(20) AFTER full_name
    """)
    print("✅ Coluna phone adicionada")
    
    # Adicionar coluna is_verified
    print("📝 Adicionando coluna is_verified...")
    cursor.execute("""
        ALTER TABLE users 
        ADD COLUMN is_verified BOOLEAN DEFAULT FALSE AFTER is_active
    """)
    print("✅ Coluna is_verified adicionada")
    
    # Adicionar coluna login_count
    print("📝 Adicionando coluna login_count...")
    cursor.execute("""
        ALTER TABLE users 
        ADD COLUMN login_count INT DEFAULT 0 AFTER last_login_at
    """)
    print("✅ Coluna login_count adicionada")
    
    # Atualizar full_name com first_name + last_name existentes
    print("📝 Atualizando full_name com dados existentes...")
    cursor.execute("""
        UPDATE users 
        SET full_name = CONCAT_WS(' ', first_name, last_name)
        WHERE first_name IS NOT NULL OR last_name IS NOT NULL
    """)
    affected = cursor.rowcount
    print(f"✅ {affected} registros atualizados")
    
    # Commit
    connection.commit()
    print("\n🎉 TABELA USERS CORRIGIDA COM SUCESSO!")
    
    # Mostrar estrutura atualizada
    cursor.execute("DESCRIBE users")
    columns = cursor.fetchall()
    
    print("\n📋 Estrutura da tabela users:")
    for col in columns:
        print(f"  - {col[0]} ({col[1]})")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    connection.rollback()
finally:
    cursor.close()
    connection.close()
