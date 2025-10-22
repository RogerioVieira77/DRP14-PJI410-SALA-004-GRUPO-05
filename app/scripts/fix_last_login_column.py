"""
Script para adicionar a coluna last_login na tabela users
"""
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

print("=== CORRIGINDO COLUNA LAST_LOGIN ===\n")

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
    # Verificar se a coluna last_login já existe
    cursor.execute("""
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = %s 
        AND TABLE_NAME = 'users' 
        AND COLUMN_NAME = 'last_login'
    """, (os.getenv('DB_NAME', 'ceu_tres_pontes_db'),))
    
    if cursor.fetchone():
        print("✅ Coluna last_login já existe")
    else:
        # Adicionar coluna last_login
        print("📝 Adicionando coluna last_login...")
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN last_login DATETIME AFTER is_verified
        """)
        print("✅ Coluna last_login adicionada")
    
    # Copiar dados de last_login_at para last_login se necessário
    print("📝 Copiando dados de last_login_at para last_login...")
    cursor.execute("""
        UPDATE users 
        SET last_login = last_login_at
        WHERE last_login_at IS NOT NULL
    """)
    affected = cursor.rowcount
    print(f"✅ {affected} registros atualizados")
    
    # Commit
    connection.commit()
    print("\n🎉 COLUNA LAST_LOGIN CORRIGIDA COM SUCESSO!")
    
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
