"""
Teste de Conexão com o Banco de Dados Remoto
"""
import pymysql
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

print("=" * 50)
print("TESTE DE CONEXÃO COM BANCO DE DADOS REMOTO")
print("=" * 50)

# Configurações do banco
config = {
    'host': os.getenv('DB_HOST', '82.25.75.88'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'smartceu_user'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME', 'smartceu_db'),
    'charset': 'utf8mb4',
    'connect_timeout': 10
}

print(f"\nConfigurações:")
print(f"  Host: {config['host']}")
print(f"  Port: {config['port']}")
print(f"  User: {config['user']}")
print(f"  Database: {config['database']}")
print(f"  Password: {'*' * len(config['password']) if config['password'] else 'NÃO CONFIGURADA'}")

if not config['password']:
    print("\n❌ ERRO: Senha do banco não está configurada no .env")
    exit(1)

print("\n🔄 Tentando conectar...")

try:
    # Tentar conectar
    connection = pymysql.connect(**config)
    print("✅ Conexão estabelecida com sucesso!")
    
    # Testar query
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"\n📊 Versão do MySQL: {version[0]}")
        
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"\n📋 Tabelas no banco ({len(tables)}):")
        for table in tables:
            print(f"  - {table[0]}")
            
        # Contar registros
        cursor.execute("SELECT COUNT(*) FROM sensors")
        sensors_count = cursor.fetchone()[0]
        print(f"\n📡 Sensores cadastrados: {sensors_count}")
        
        cursor.execute("SELECT COUNT(*) FROM readings")
        readings_count = cursor.fetchone()[0]
        print(f"📊 Leituras registradas: {readings_count}")
        
        cursor.execute("SELECT COUNT(*) FROM pool_readings")
        pool_count = cursor.fetchone()[0]
        print(f"🏊 Leituras de piscina: {pool_count}")
    
    connection.close()
    print("\n✅ TESTE CONCLUÍDO COM SUCESSO!")
    print("=" * 50)

except pymysql.err.OperationalError as e:
    print(f"\n❌ ERRO DE CONEXÃO: {e}")
    print("\n💡 Possíveis causas:")
    print("  1. Firewall bloqueando porta 3306")
    print("  2. Senha incorreta no arquivo .env")
    print("  3. Usuário não tem permissão remota")
    print("  4. MySQL não está aceitando conexões remotas")
    print("\n🔧 Soluções:")
    print("  - Verifique a senha no arquivo .env")
    print("  - Solicite liberação do seu IP no servidor")
    print("  - Use túnel SSH como alternativa")
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")

print("\n" + "=" * 50)