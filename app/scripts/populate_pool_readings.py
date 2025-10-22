#!/usr/bin/env python3
"""
Script para popular o banco de dados com leituras simuladas da piscina
Cria leituras dos últimos 20 dias para os sensores:
- water_temp (temperatura da água)
- ambient_temp (temperatura ambiente)
- water_quality (qualidade da água)

Média de 87 a 253 leituras diárias por tipo de sensor
"""

from app import create_app, db
from app.models.pool_reading import PoolReading
from datetime import datetime, timedelta, date, time
from zoneinfo import ZoneInfo
import random

# Timezone do servidor
TIMEZONE = ZoneInfo('America/Sao_Paulo')

def generate_pool_readings():
    """Gera leituras simuladas para os sensores da piscina"""
    
    app = create_app()
    with app.app_context():
        print('='*70)
        print('Gerando leituras da piscina (últimos 20 dias)')
        print('='*70)
        print()
        
        # Verificar leituras existentes
        existing_count = PoolReading.query.count()
        if existing_count > 0:
            print(f'⚠️  Já existem {existing_count} leituras da piscina no banco!')
            response = input('Deseja adicionar mais leituras? (s/N): ')
            if response.lower() != 's':
                print('Operação cancelada.')
                return
        
        # Configurações
        days_back = 20
        sensor_types = ['water_temp', 'ambient_temp', 'water_quality']
        
        # Horários de operação da piscina: 6h às 22h
        start_hour = 6
        end_hour = 22
        
        total_readings_created = 0
        readings_by_type = {sensor_type: 0 for sensor_type in sensor_types}
        
        # Para cada tipo de sensor
        for sensor_type in sensor_types:
            print(f'📊 Gerando leituras para: {sensor_type}')
            
            sensor_readings = []
            
            # Para cada dia
            for day_offset in range(days_back, -1, -1):
                # Data com timezone correto
                now_with_tz = datetime.now(TIMEZONE)
                reading_date = (now_with_tz - timedelta(days=day_offset)).date()
                
                # Para o dia atual, limitar hora ao horário atual
                is_today = (day_offset == 0)
                current_hour = now_with_tz.hour
                max_hour = current_hour if is_today else end_hour
                
                # Não gerar leituras se ainda não chegou ao horário de abertura hoje
                if is_today and current_hour < start_hour:
                    continue
                
                # Número de leituras neste dia (variado entre 87 e 253)
                if sensor_type == 'water_quality':
                    # Qualidade da água é medida menos frequentemente
                    num_readings = random.randint(30, 60)
                else:
                    # Temperaturas são medidas mais frequentemente
                    num_readings = random.randint(87, 253)
                
                # Para hoje, ajustar o número de leituras proporcionalmente
                if is_today:
                    hours_elapsed = current_hour - start_hour + 1
                    total_hours = end_hour - start_hour + 1
                    num_readings = int(num_readings * hours_elapsed / total_hours)
                
                # Gerar leituras distribuídas ao longo do dia
                for _ in range(num_readings):
                    # Hora aleatória entre start_hour e max_hour
                    hour = random.randint(start_hour, max_hour)
                    
                    # Para a hora atual, limitar os minutos
                    if is_today and hour == current_hour:
                        minute = random.randint(0, now_with_tz.minute)
                    else:
                        minute = random.randint(0, 59)
                    
                    second = random.randint(0, 59)
                    
                    # Criar datetime completo com timezone e depois extrair o time
                    dt = datetime(reading_date.year, reading_date.month, reading_date.day, 
                                  hour, minute, second, tzinfo=TIMEZONE)
                    reading_time = dt.time().replace(tzinfo=None)  # MySQL TIME não suporta timezone
                    
                    # Gerar valores baseados no tipo de sensor e hora do dia
                    reading_data = generate_sensor_value(
                        sensor_type, 
                        reading_date, 
                        hour
                    )
                    
                    # Criar reading
                    reading = PoolReading(
                        sensor_type=sensor_type,
                        reading_date=reading_date,
                        reading_time=reading_time,
                        temperature=reading_data.get('temperature'),
                        water_quality=reading_data.get('water_quality')
                    )
                    
                    sensor_readings.append(reading)
            
            # Adicionar todas as leituras do sensor
            db.session.bulk_save_objects(sensor_readings)
            db.session.commit()
            
            total_readings_created += len(sensor_readings)
            readings_by_type[sensor_type] = len(sensor_readings)
            print(f'   ✅ {len(sensor_readings)} leituras criadas')
            print()
        
        print('='*70)
        print(f'✅ Total de {total_readings_created} leituras da piscina criadas!')
        print('='*70)
        print()
        print('📊 Distribuição por tipo de sensor:')
        for sensor_type, count in readings_by_type.items():
            print(f'   {sensor_type:20s}: {count:5d} leituras')
        print()
        print('🌐 Teste na API:')
        print('   GET http://82.25.75.88/smartceu/api/v1/pool/readings/latest')
        print('   GET http://82.25.75.88/smartceu/api/v1/pool/statistics')
        print()
        print('📱 Visualize no monitoramento:')
        print('   http://82.25.75.88/smartceu/pool')
        print()

def generate_sensor_value(sensor_type, reading_date, hour):
    """
    Gera valores de leitura baseados no tipo de sensor
    
    Args:
        sensor_type: Tipo do sensor (water_temp, ambient_temp, water_quality)
        reading_date: Data da leitura
        hour: Hora do dia (0-23)
    
    Returns:
        dict: Dados da leitura
    """
    
    if sensor_type == 'water_temp':
        # Temperatura da água: 24-28°C
        # Mais estável, varia pouco ao longo do dia
        base_temp = 26.0
        variation = random.uniform(-2.0, 2.0)
        # Leve aquecimento ao longo do dia
        hour_effect = (hour - 12) * 0.1 if hour > 12 else 0
        temperature = round(base_temp + variation + hour_effect, 2)
        # Manter no range 24-28°C
        temperature = max(24.0, min(28.0, temperature))
        
        return {
            'temperature': temperature,
            'water_quality': None
        }
    
    elif sensor_type == 'ambient_temp':
        # Temperatura ambiente: 18-35°C
        # Varia mais ao longo do dia
        if hour < 6:
            base_temp = 20.0  # Madrugada fria
        elif hour < 12:
            base_temp = 22.0 + (hour - 6) * 1.5  # Aquecendo
        elif hour < 18:
            base_temp = 30.0  # Tarde quente
        else:
            base_temp = 28.0 - (hour - 18) * 2.0  # Esfriando
        
        variation = random.uniform(-3.0, 3.0)
        temperature = round(base_temp + variation, 2)
        # Manter no range 18-35°C
        temperature = max(18.0, min(35.0, temperature))
        
        return {
            'temperature': temperature,
            'water_quality': None
        }
    
    elif sensor_type == 'water_quality':
        # Qualidade da água
        # 85% Ótima, 10% Boa, 4% Regular, 1% Imprópria
        rand = random.random()
        
        if rand < 0.85:
            quality = 'Ótima'
        elif rand < 0.95:
            quality = 'Boa'
        elif rand < 0.99:
            quality = 'Regular'
        else:
            quality = 'Imprópria'
        
        return {
            'temperature': None,
            'water_quality': quality
        }
    
    return {}

if __name__ == '__main__':
    generate_pool_readings()
