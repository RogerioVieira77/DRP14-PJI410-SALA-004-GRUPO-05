#!/usr/bin/env python3
"""
Script para criar e popular sensores no banco de dados SmartCEU
Cria 6 sensores (1 de cada protocolo + extras)
"""

from app import create_app, db
from app.models.sensor import Sensor
from datetime import datetime

def create_sensors():
    """Cria os 6 sensores no banco de dados"""
    
    app = create_app()
    with app.app_context():
        # Verificar se já existem sensores
        existing_count = Sensor.query.count()
        if existing_count > 0:
            print(f'⚠️  Já existem {existing_count} sensores no banco!')
            response = input('Deseja recriar os sensores? (s/N): ')
            if response.lower() != 's':
                print('Operação cancelada.')
                return
            
            # Limpar sensores existentes
            Sensor.query.delete()
            db.session.commit()
            print('✅ Sensores anteriores removidos.')
        
        # Lista de sensores a criar
        sensors_data = [
            {
                'serial_number': 'LORA-A1B2C3D4',
                'protocol': 'LoRa',
                'location': 'Entrada Principal',
                'description': 'Sensor de presença LoRa - Entrada Principal',
                'status': 'active',
                'protocol_config': {
                    'frequency_mhz': 915.0,
                    'spreading_factor': 7,
                    'bandwidth_khz': 125,
                    'transmission_power_dbm': 14
                },
                'firmware_version': '1.2.0',
                'battery_level': 100.0,
                'signal_strength': -60.0
            },
            {
                'serial_number': 'ZIGB-E5F6G7H8',
                'protocol': 'Zigbee',
                'location': 'Quadra Esportiva',
                'description': 'Sensor de presença Zigbee - Quadra Esportiva',
                'status': 'active',
                'protocol_config': {
                    'channel': 15,
                    'pan_id': '0x1234',
                    'power_mode': 'RxOnWhenIdle'
                },
                'firmware_version': '2.1.5',
                'battery_level': 95.0,
                'signal_strength': -55.0
            },
            {
                'serial_number': 'SIGF-I9J0K1L2',
                'protocol': 'Sigfox',
                'location': 'Playground',
                'description': 'Sensor de presença Sigfox - Playground',
                'status': 'active',
                'protocol_config': {
                    'device_id': 'ABC123',
                    'pac_code': 'XYZ789',
                    'rc_zone': 'RC4'
                },
                'firmware_version': '1.0.3',
                'battery_level': 88.0,
                'signal_strength': -70.0
            },
            {
                'serial_number': 'RFID-M3N4O5P6',
                'protocol': 'RFID',
                'location': 'Biblioteca',
                'description': 'Leitor RFID - Controle de acesso Biblioteca',
                'status': 'active',
                'protocol_config': {
                    'frequency_khz': 13560,
                    'read_range_cm': 10,
                    'protocol_type': 'ISO14443A'
                },
                'firmware_version': '3.0.1',
                'battery_level': None,  # Alimentado por rede
                'signal_strength': None
            },
            {
                'serial_number': 'LORA-Q7R8S9T0',
                'protocol': 'LoRa',
                'location': 'Área da Piscina',
                'description': 'Sensor multiparâmetro LoRa - Piscina (temp água, temp ambiente, pH)',
                'status': 'active',
                'protocol_config': {
                    'frequency_mhz': 915.0,
                    'spreading_factor': 8,
                    'bandwidth_khz': 125,
                    'transmission_power_dbm': 14,
                    'sensors': ['water_temp', 'ambient_temp', 'ph']
                },
                'firmware_version': '1.3.2',
                'battery_level': 92.0,
                'signal_strength': -65.0
            },
            {
                'serial_number': 'ZIGB-U1V2W3X4',
                'protocol': 'Zigbee',
                'location': 'Saída Lateral',
                'description': 'Sensor de presença Zigbee - Saída Lateral',
                'status': 'active',
                'protocol_config': {
                    'channel': 20,
                    'pan_id': '0x5678',
                    'power_mode': 'RxOnWhenIdle'
                },
                'firmware_version': '2.1.5',
                'battery_level': 90.0,
                'signal_strength': -58.0
            }
        ]
        
        print('\n' + '='*60)
        print('Criando sensores no banco de dados...')
        print('='*60 + '\n')
        
        created_sensors = []
        for sensor_data in sensors_data:
            sensor = Sensor(
                serial_number=sensor_data['serial_number'],
                protocol=sensor_data['protocol'],
                location=sensor_data['location'],
                description=sensor_data['description'],
                status=sensor_data['status'],
                protocol_config=sensor_data['protocol_config'],
                firmware_version=sensor_data['firmware_version'],
                battery_level=sensor_data['battery_level'],
                signal_strength=sensor_data['signal_strength']
            )
            
            db.session.add(sensor)
            created_sensors.append(sensor)
            
            print(f"✅ {sensor.description}")
            print(f"   Serial: {sensor.serial_number}")
            print(f"   Protocolo: {sensor.protocol}")
            print(f"   Localização: {sensor.location}")
            print()
        
        # Commit todas as mudanças
        db.session.commit()
        
        print('='*60)
        print(f'✅ {len(created_sensors)} sensores criados com sucesso!')
        print('='*60)
        print()
        print('📊 Resumo:')
        print(f'   LoRa:   2 sensores')
        print(f'   Zigbee: 2 sensores')
        print(f'   Sigfox: 1 sensor')
        print(f'   RFID:   1 sensor')
        print()
        print('🌐 Teste na API:')
        print('   GET http://82.25.75.88/smartceu/api/v1/sensors')
        print()

if __name__ == '__main__':
    create_sensors()
