"""
Script para popular banco de dados usando PyMySQL direto (sem SQLAlchemy)
"""
import pymysql
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

print("=" * 60)
print("POPULANDO BANCO DE DADOS - CEU TRES PONTES")
print("=" * 60)

# Conectar ao banco
connection = pymysql.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    port=int(os.getenv('DB_PORT', 3306)),
    user=os.getenv('DB_USER', 'ceu_tres_pontes'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME', 'ceu_tres_pontes_db'),
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

cursor = connection.cursor()

print("\n1. Criando usuário administrador...")

# Verificar se admin já existe
cursor.execute("SELECT * FROM users WHERE username = 'admin'")
admin = cursor.fetchone()

if admin:
    print("   ℹ️  Usuário 'admin' já existe")
else:
    password_hash = generate_password_hash('admin123')
    cursor.execute("""
        INSERT INTO users (username, email, password_hash, first_name, last_name, role, is_active)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, ('admin', 'admin@ceutrespontes.com', password_hash, 'Administrador', 'Sistema', 'admin', True))
    print("   ✅ Usuário 'admin' criado")
    print("      Username: admin")
    print("      Password: admin123")

print("\n2. Criando sensores de exemplo...")

sensors_data = [
    ('LORA-ENTRADA-01', 'LoRa', 'Entrada Principal', 'Sensor LoRa na entrada principal do parque', 'active'),
    ('LORA-SAIDA-01', 'LoRa', 'Saída Principal', 'Sensor LoRa na saída principal do parque', 'active'),
    ('ZIGB-LATERAL-01', 'ZigBee', 'Entrada Lateral Norte', 'Sensor ZigBee na entrada lateral norte', 'active'),
    ('ZIGB-LATERAL-02', 'ZigBee', 'Entrada Lateral Sul', 'Sensor ZigBee na entrada lateral sul', 'active'),
    ('SIGF-BANHEIRO-01', 'Sigfox', 'Banheiros', 'Sensor Sigfox próximo aos banheiros', 'active'),
    ('RFID-PORTARIA-01', 'RFID', 'Portaria', 'Leitor RFID na portaria', 'active')
]

sensors_created = 0
for serial, protocol, location, desc, status in sensors_data:
    # Verificar se sensor já existe
    cursor.execute("SELECT * FROM sensors WHERE serial_number = %s", (serial,))
    sensor = cursor.fetchone()
    
    if sensor:
        print(f"   ℹ️  Sensor {serial} já existe")
    else:
        cursor.execute("""
            INSERT INTO sensors (serial_number, protocol, location, description, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (serial, protocol, location, desc, status))
        sensors_created += 1
        print(f"   ✅ Sensor {serial} criado")

# Commit
try:
    connection.commit()
    
    # Obter estatísticas
    cursor.execute("SELECT COUNT(*) as count FROM users")
    user_count = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM sensors")
    sensor_count = cursor.fetchone()['count']
    
    print("\n" + "=" * 60)
    print("✅ BANCO DE DADOS POPULADO COM SUCESSO!")
    print("=" * 60)
    
    print("\n📊 RESUMO:")
    print(f"   - Usuários: {user_count}")
    print(f"   - Sensores: {sensor_count}")
    
    print("\n🔑 CREDENCIAIS DE ACESSO:")
    print("   Username: admin")
    print("   Password: admin123")
    print("   Role: admin")
    
    print("\n📍 SENSORES CADASTRADOS:")
    cursor.execute("SELECT serial_number, protocol, location FROM sensors ORDER BY serial_number")
    sensors = cursor.fetchall()
    for sensor in sensors:
        print(f"   - {sensor['serial_number']} ({sensor['protocol']}) - {sensor['location']}")
    
    print("\n")
    
except Exception as e:
    connection.rollback()
    print(f"\n❌ Erro ao popular banco: {e}")
    import traceback
    traceback.print_exc()
finally:
    cursor.close()
    connection.close()
