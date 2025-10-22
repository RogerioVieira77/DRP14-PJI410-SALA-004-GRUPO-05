"""
Script para popular o banco de dados com dados de exemplo
"""
import sys
sys.path.insert(0, 'backend')

from app import create_app, db
from app.models.user import User
from app.models.sensor import Sensor

print("=" * 60)
print("POPULANDO BANCO DE DADOS - CEU TRES PONTES")
print("=" * 60)

# Criar app
app = create_app('development')

with app.app_context():
    print("\n1. Criando usuário administrador...")
    
    # Verificar se admin já existe
    admin = User.query.filter_by(username='admin').first()
    
    if admin:
        print("   ℹ️  Usuário 'admin' já existe")
    else:
        admin = User.create_user(
            username='admin',
            email='admin@ceutrespontes.com',
            password='admin123',
            role='admin',
            full_name='Administrador do Sistema'
        )
        admin.is_verified = True
        db.session.add(admin)
        print("   ✅ Usuário 'admin' criado")
        print("      Username: admin")
        print("      Password: admin123")
    
    print("\n2. Criando sensores de exemplo...")
    
    sensors_data = [
        {
            'serial_number': 'LORA-ENTRADA-01',
            'protocol': 'LoRa',
            'location': 'Entrada Principal',
            'description': 'Sensor LoRa na entrada principal do parque',
            'status': 'active'
        },
        {
            'serial_number': 'LORA-SAIDA-01',
            'protocol': 'LoRa',
            'location': 'Saída Principal',
            'description': 'Sensor LoRa na saída principal do parque',
            'status': 'active'
        },
        {
            'serial_number': 'ZIGB-LATERAL-01',
            'protocol': 'ZigBee',
            'location': 'Entrada Lateral Norte',
            'description': 'Sensor ZigBee na entrada lateral norte',
            'status': 'active'
        },
        {
            'serial_number': 'ZIGB-LATERAL-02',
            'protocol': 'ZigBee',
            'location': 'Entrada Lateral Sul',
            'description': 'Sensor ZigBee na entrada lateral sul',
            'status': 'active'
        },
        {
            'serial_number': 'SIGF-BANHEIRO-01',
            'protocol': 'Sigfox',
            'location': 'Banheiros',
            'description': 'Sensor Sigfox próximo aos banheiros',
            'status': 'active'
        },
        {
            'serial_number': 'RFID-PORTARIA-01',
            'protocol': 'RFID',
            'location': 'Portaria',
            'description': 'Leitor RFID na portaria',
            'status': 'active'
        }
    ]
    
    sensors_created = 0
    for sensor_data in sensors_data:
        sensor = Sensor.query.filter_by(serial_number=sensor_data['serial_number']).first()
        
        if sensor:
            print(f"   ℹ️  Sensor {sensor_data['serial_number']} já existe")
        else:
            sensor = Sensor(**sensor_data)
            db.session.add(sensor)
            sensors_created += 1
            print(f"   ✅ Sensor {sensor_data['serial_number']} criado")
    
    # Commit
    try:
        db.session.commit()
        print("\n" + "=" * 60)
        print("✅ BANCO DE DADOS POPULADO COM SUCESSO!")
        print("=" * 60)
        
        print("\n📊 RESUMO:")
        print(f"   - Usuários: {User.query.count()}")
        print(f"   - Sensores: {Sensor.query.count()}")
        
        print("\n🔑 CREDENCIAIS DE ACESSO:")
        print("   Username: admin")
        print("   Password: admin123")
        
        print("\n📍 SENSORES CADASTRADOS:")
        for sensor in Sensor.query.all():
            print(f"   - {sensor.serial_number} ({sensor.protocol}) - {sensor.location}")
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Erro ao popular banco: {e}")
        import traceback
        traceback.print_exc()
