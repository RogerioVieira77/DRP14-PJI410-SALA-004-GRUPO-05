#!/usr/bin/env python3
"""
Script para popular o banco de dados com leituras simuladas
Cria leituras dos últimos 20 dias para todos os sensores
Média de 87 a 253 leituras diárias por sensor
"""

from app import create_app, db
from app.models.sensor import Sensor
from app.models.reading import Reading
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import random
import json

# Timezone do servidor
TIMEZONE = ZoneInfo('America/Sao_Paulo')

def generate_readings():
    """Gera leituras simuladas para todos os sensores"""
    
    app = create_app()
    with app.app_context():
        # Buscar todos os sensores
        sensors = Sensor.query.all()
        
        if not sensors:
            print('❌ Nenhum sensor encontrado no banco!')
            print('   Execute primeiro: create_sensors.py')
            return
        
        print('='*70)
        print(f'Gerando leituras simuladas para {len(sensors)} sensores')
        print('Período: Últimos 20 dias')
        print('='*70)
        print()
        
        # Verificar leituras existentes
        existing_count = Reading.query.count()
        if existing_count > 0:
            print(f'⚠️  Já existem {existing_count} leituras no banco!')
            response = input('Deseja adicionar mais leituras? (s/N): ')
            if response.lower() != 's':
                print('Operação cancelada.')
                return
        
        # Configurações
        days_back = 20
        min_readings_per_day = 87
        max_readings_per_day = 253
        
        total_readings_created = 0
        
        # Para cada sensor
        for sensor in sensors:
            sensor_readings = []
            print(f'📡 {sensor.description}')
            print(f'   Serial: {sensor.serial_number}')
            
            # Gerar leituras para cada dia
            for day_offset in range(days_back, -1, -1):
                # Data base do dia com timezone correto
                day_date = datetime.now(TIMEZONE) - timedelta(days=day_offset)
                day_start = day_date.replace(hour=6, minute=0, second=0, microsecond=0)
                day_end = day_date.replace(hour=22, minute=0, second=0, microsecond=0)
                
                # Número aleatório de leituras para este dia
                num_readings = random.randint(min_readings_per_day, max_readings_per_day)
                
                # Gerar leituras distribuídas ao longo do dia
                for _ in range(num_readings):
                    # Timestamp aleatório entre 6h e 22h
                    random_seconds = random.randint(0, int((day_end - day_start).total_seconds()))
                    timestamp = day_start + timedelta(seconds=random_seconds)
                    
                    # Gerar dados baseados no tipo de sensor
                    reading_data = generate_sensor_data(sensor, timestamp)
                    
                    # Extrair activity (obrigatório)
                    activity = reading_data.pop('activity', 0)
                    
                    # Criar reading
                    reading = Reading(
                        sensor_id=sensor.id,
                        timestamp=timestamp,
                        activity=activity,
                        sensor_metadata=reading_data
                    )
                    
                    sensor_readings.append(reading)
            
            # Adicionar todas as leituras do sensor
            db.session.bulk_save_objects(sensor_readings)
            db.session.commit()
            
            total_readings_created += len(sensor_readings)
            print(f'   ✅ {len(sensor_readings)} leituras criadas')
            print()
            
            # Atualizar estatísticas do sensor
            sensor.total_readings = len(sensor_readings)
            sensor.last_reading_at = max(r.timestamp for r in sensor_readings)
            db.session.commit()
        
        print('='*70)
        print(f'✅ Total de {total_readings_created} leituras criadas!')
        print('='*70)
        print()
        print('📊 Estatísticas:')
        print(f'   Sensores: {len(sensors)}')
        print(f'   Período: {days_back} dias')
        print(f'   Média por sensor: {total_readings_created // len(sensors)} leituras')
        print(f'   Média diária: {total_readings_created // (len(sensors) * days_back)} leituras/sensor/dia')
        print()
        print('🌐 Teste na API:')
        print('   GET http://82.25.75.88/smartceu/api/v1/readings/latest')
        print('   GET http://82.25.75.88/smartceu/api/v1/statistics/overview')
        print()

def generate_sensor_data(sensor, timestamp):
    """
    Gera dados de leitura baseados no tipo de sensor
    
    Args:
        sensor: Instância do sensor
        timestamp: Data/hora da leitura
    
    Returns:
        dict: Dados da leitura
    """
    # Hora do dia (para variações)
    hour = timestamp.hour
    
    # Dados base
    data = {
        'timestamp': timestamp.isoformat(),
        'protocol': sensor.protocol
    }
    
    # Dados específicos por protocolo
    if sensor.protocol == 'LoRa':
        # Sensor da piscina tem dados especiais
        if 'Piscina' in sensor.location:
            data.update({
                'water_temperature': round(random.uniform(24.0, 28.0), 1),
                'ambient_temperature': round(random.uniform(18.0, 32.0), 1),
                'ph': round(random.uniform(7.0, 7.6), 2),
                'activity': random.randint(0, 1)
            })
        else:
            # Sensor de presença normal
            # Mais atividade entre 8h-20h
            activity_prob = 0.4 if 8 <= hour <= 20 else 0.1
            data.update({
                'activity': 1 if random.random() < activity_prob else 0,
                'rssi': round(random.uniform(-75, -50), 1),
                'snr': round(random.uniform(5, 15), 2),
                'battery': round(random.uniform(85, 100), 1)
            })
    
    elif sensor.protocol == 'Zigbee':
        # Mais atividade durante horário comercial
        activity_prob = 0.45 if 8 <= hour <= 20 else 0.12
        data.update({
            'activity': 1 if random.random() < activity_prob else 0,
            'link_quality': random.randint(150, 255),
            'rssi': round(random.uniform(-65, -45), 1),
            'battery': round(random.uniform(80, 98), 1)
        })
    
    elif sensor.protocol == 'Sigfox':
        # Sigfox tem menor taxa de transmissão
        activity_prob = 0.35 if 9 <= hour <= 19 else 0.08
        data.update({
            'activity': 1 if random.random() < activity_prob else 0,
            'rssi': round(random.uniform(-80, -60), 1),
            'battery': round(random.uniform(75, 95), 1),
            'messages_sent': random.randint(1, 3)
        })
    
    elif sensor.protocol == 'RFID':
        # RFID só registra quando há leitura de tag
        # Simula presença de pessoas
        activity_prob = 0.5 if 8 <= hour <= 20 else 0.05
        if random.random() < activity_prob:
            data.update({
                'tag_id': f'TAG-{random.randint(1000, 9999)}',
                'tag_type': random.choice(['student', 'staff', 'visitor']),
                'access_granted': True,
                'activity': 1
            })
        else:
            data.update({
                'activity': 0
            })
    
    return data

if __name__ == '__main__':
    generate_readings()
