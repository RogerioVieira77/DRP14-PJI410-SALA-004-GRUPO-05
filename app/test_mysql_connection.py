"""
Script para testar conexão com MySQL
"""
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

# Tentar conexão direta
print("=== TESTE DE CONEXÃO MYSQL ===\n")

host = os.getenv('DB_HOST', 'localhost')
port = int(os.getenv('DB_PORT', 3306))
user = os.getenv('DB_USER', 'ceu_tres_pontes')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME', 'ceu_tres_pontes_db')

print(f"Host: {host}:{port}")
print(f"User: {user}")
print(f"Password: {'*' * len(password) if password else 'NOT SET'}")
print(f"Database: {database}\n")

try:
    print("Tentando conectar...")
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        charset='utf8mb4'
    )
    
    print("✅ Conexão bem-sucedida!")
    
    cursor = connection.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print(f"✅ MySQL Version: {version[0]}")
    
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"\nTabelas existentes: {len(tables)}")
    for table in tables:
        print(f"  - {table[0]}")
    
    cursor.close()
    connection.close()
    
    print("\n✅ CONEXÃO OK!")
    
except pymysql.err.OperationalError as e:
    print(f"❌ Erro de conexão: {e}")
    print("\nPossíveis causas:")
    print("  1. Senha incorreta no .env")
    print("  2. Usuário não tem permissões")
    print("  3. MySQL não está rodando")
    print("\nPara corrigir, execute no MySQL:")
    print(f"  ALTER USER '{user}'@'localhost' IDENTIFIED BY '{password}';")
    print(f"  GRANT ALL PRIVILEGES ON {database}.* TO '{user}'@'localhost';")
    print(f"  FLUSH PRIVILEGES;")
    
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
    import traceback
    traceback.print_exc()
