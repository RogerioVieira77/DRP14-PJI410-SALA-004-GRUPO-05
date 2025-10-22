"""
Script para corrigir a tabela sensors
"""
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

print("=== CORRIGINDO TABELA SENSORS ===\n")

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
    # Verificar se a coluna protocol_config já existe
    cursor.execute("""
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = %s 
        AND TABLE_NAME = 'sensors' 
        AND COLUMN_NAME = 'protocol_config'
    """, (os.getenv('DB_NAME', 'ceu_tres_pontes_db'),))
    
    if cursor.fetchone():
        print("✅ Coluna protocol_config já existe")
    else:
        # Adicionar coluna protocol_config
        print("📝 Adicionando coluna protocol_config...")
        cursor.execute("""
            ALTER TABLE sensors 
            ADD COLUMN protocol_config JSON AFTER status
        """)
        print("✅ Coluna protocol_config adicionada")
    
    # Verificar se a coluna firmware_version já existe
    cursor.execute("""
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = %s 
        AND TABLE_NAME = 'sensors' 
        AND COLUMN_NAME = 'firmware_version'
    """, (os.getenv('DB_NAME', 'ceu_tres_pontes_db'),))
    
    if cursor.fetchone():
        print("✅ Coluna firmware_version já existe")
    else:
        # Adicionar coluna firmware_version
        print("📝 Adicionando coluna firmware_version...")
        cursor.execute("""
            ALTER TABLE sensors 
            ADD COLUMN firmware_version VARCHAR(20) AFTER protocol_config
        """)
        print("✅ Coluna firmware_version adicionada")
    
    # Commit
    connection.commit()
    print("\n🎉 TABELA SENSORS CORRIGIDA COM SUCESSO!")
    
    # Mostrar estrutura atualizada
    cursor.execute("DESCRIBE sensors")
    columns = cursor.fetchall()
    
    print("\n📋 Estrutura da tabela sensors:")
    for col in columns:
        print(f"  - {col[0]} ({col[1]})")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    connection.rollback()
finally:
    cursor.close()
    connection.close()
