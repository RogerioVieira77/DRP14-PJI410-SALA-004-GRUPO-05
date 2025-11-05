#!/usr/bin/env python3
"""
Script de Simulação de Eventos de Sensores - SmartCEU
=====================================================

Simula eventos em tempo real para todos os sensores do parque, gerando
leituras nas tabelas 'readings' e 'pool_readings' como se fossem atividades
reais acontecendo no CEU Três Pontes.

Tipos de Eventos Simulados:
- Detecção de presença (PIR e LoRa)
- Temperatura e umidade (DHT22)
- Qualidade do ar (MQ135)
- Temperatura da água (piscina)
- Qualidade da água (pH, cloro, alcalinidade)
- Temperatura ambiente da área da piscina

Uso:
    python3 simulate_sensor_events.py [opções]

Opções:
    --interval SEGUNDOS    Intervalo entre eventos (padrão: 30)
    --duration MINUTOS     Duração da simulação em minutos (padrão: infinito)
    --sensor TIPO         Simular apenas um tipo de sensor
    --batch N             Gerar N eventos de uma vez e sair

Exemplos:
    # Executar continuamente
    python3 simulate_sensor_events.py

    # Executar por 1 hora com eventos a cada 15 segundos
    python3 simulate_sensor_events.py --interval 15 --duration 60

    # Gerar 100 eventos de uma vez
    python3 simulate_sensor_events.py --batch 100

    # Simular apenas sensores da piscina
    python3 simulate_sensor_events.py --sensor pool
"""

import sys
import os
import time
import random
import argparse
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Adicionar o diretório do app ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.reading import Reading
from app.models.pool_reading import PoolReading
from app.models.sensor import Sensor

# Configurações
TIMEZONE = ZoneInfo('America/Sao_Paulo')

# Definição das áreas e seus sensores
AREAS = {
    'quadra_esportes': {
        'name': 'Quadra de Esportes',
        'sensors': [1, 2]  # IDs dos sensores
    },
    'biblioteca': {
        'name': 'Biblioteca',
        'sensors': [3, 4]  # IDs dos sensores
    },
    'piscina': {
        'name': 'Área da Piscina',
        'sensors': [5, 6]  # IDs dos sensores
    }
}

# Padrões de comportamento por horário
def get_activity_multiplier():
    """Retorna um multiplicador de atividade baseado no horário"""
    now = datetime.now(TIMEZONE)
    hour = now.hour
    
    # Horário de pico: 9h-11h e 14h-17h
    if 9 <= hour <= 11 or 14 <= hour <= 17:
        return 1.5
    # Horário normal: 7h-9h, 11h-14h, 17h-20h
    elif (7 <= hour < 9) or (11 < hour < 14) or (17 < hour <= 20):
        return 1.0
    # Horário baixo: 6h-7h, 20h-22h
    elif (6 <= hour < 7) or (20 < hour <= 22):
        return 0.3
    # Fechado: 22h-6h
    else:
        return 0.0

def generate_pir_reading(sensor_id, area):
    """Gera leitura de sensor PIR (presença infravermelha)"""
    activity = get_activity_multiplier()
    
    if activity == 0:
        return None  # CEU fechado
    
    # Probabilidade de detecção baseada na atividade
    if random.random() < (0.4 * activity):
        detection = 1  # Presença detectada
        value = random.uniform(50, 100)  # Intensidade
    else:
        detection = 0  # Sem presença
        value = 0
    
    return {
        'sensor_id': sensor_id,
        'area': area,
        'protocol': 'pir',
        'value': value,
        'detection': detection,
        'battery': random.randint(65, 100)
    }

def generate_lora_reading(sensor_id, area):
    """Gera leitura de sensor LoRa (presença por radiofrequência)"""
    activity = get_activity_multiplier()
    
    if activity == 0:
        return None  # CEU fechado
    
    # Probabilidade de detecção
    if random.random() < (0.35 * activity):
        detection = 1
        value = random.uniform(40, 90)
        # Simular múltiplas pessoas
        people_count = random.choices([1, 2, 3, 4, 5], weights=[40, 30, 15, 10, 5])[0]
    else:
        detection = 0
        value = 0
        people_count = 0
    
    return {
        'sensor_id': sensor_id,
        'area': area,
        'protocol': 'lora',
        'value': value,
        'detection': detection,
        'battery': random.randint(70, 100),
        'metadata': f'{{"people_count": {people_count}, "signal_strength": {random.randint(-80, -40)}}}'
    }

def generate_dht_reading(sensor_id, area):
    """Gera leitura de sensor DHT22 (temperatura e umidade)"""
    now = datetime.now(TIMEZONE)
    hour = now.hour
    
    # Temperatura varia com o horário
    if 6 <= hour < 12:
        temp_base = random.uniform(18, 25)  # Manhã
    elif 12 <= hour < 18:
        temp_base = random.uniform(25, 32)  # Tarde
    elif 18 <= hour < 22:
        temp_base = random.uniform(22, 27)  # Noite
    else:
        temp_base = random.uniform(15, 20)  # Madrugada
    
    # Umidade varia inversamente à temperatura
    humidity = random.uniform(40, 80) - (temp_base - 20) * 2
    humidity = max(30, min(90, humidity))  # Limitar entre 30-90%
    
    return {
        'sensor_id': sensor_id,
        'area': area,
        'protocol': 'dht22',
        'value': round(temp_base, 1),
        'detection': 0,
        'battery': random.randint(60, 100),
        'metadata': f'{{"temperature": {round(temp_base, 1)}, "humidity": {round(humidity, 1)}}}'
    }

def generate_mq_reading(sensor_id, area):
    """Gera leitura de sensor MQ135 (qualidade do ar)"""
    activity = get_activity_multiplier()
    
    # Qualidade do ar piora com mais atividade
    base_quality = random.uniform(50, 100)
    quality = base_quality - (activity * random.uniform(0, 20))
    quality = max(20, min(100, quality))
    
    # Classificação
    if quality >= 80:
        classification = 'excelente'
    elif quality >= 60:
        classification = 'boa'
    elif quality >= 40:
        classification = 'moderada'
    else:
        classification = 'ruim'
    
    return {
        'sensor_id': sensor_id,
        'area': area,
        'protocol': 'mq135',
        'value': round(quality, 1),
        'detection': 0,
        'battery': random.randint(55, 100),
        'metadata': f'{{"air_quality": {round(quality, 1)}, "classification": "{classification}", "co2_ppm": {random.randint(400, 1200)}}}'
    }

def generate_water_temp_reading():
    """Gera leitura de temperatura da água da piscina"""
    now = datetime.now(TIMEZONE)
    hour = now.hour
    
    # Piscina opera das 6h às 22h
    if not (6 <= hour <= 22):
        return None
    
    # Temperatura da água varia pouco durante o dia
    # Base: 26-28°C, com variação de ±1°C
    base_temp = 27.0
    variation = random.uniform(-1.0, 1.0)
    
    # Aquecimento durante o dia
    if 12 <= hour <= 16:
        variation += random.uniform(0, 0.5)
    
    temp = base_temp + variation
    
    return {
        'sensor_type': 'water_temp',
        'value': round(temp, 2),
        'unit': '°C'
    }

def generate_ambient_temp_reading():
    """Gera leitura de temperatura ambiente da área da piscina"""
    now = datetime.now(TIMEZONE)
    hour = now.hour
    
    if not (6 <= hour <= 22):
        return None
    
    # Temperatura ambiente varia mais que a da água
    if 6 <= hour < 12:
        temp = random.uniform(20, 26)
    elif 12 <= hour < 18:
        temp = random.uniform(26, 34)
    elif 18 <= hour <= 22:
        temp = random.uniform(22, 28)
    else:
        temp = random.uniform(18, 22)
    
    return {
        'sensor_type': 'ambient_temp',
        'value': round(temp, 2),
        'unit': '°C'
    }

def generate_water_quality_reading():
    """Gera leitura de qualidade da água (pH, cloro, alcalinidade)"""
    now = datetime.now(TIMEZONE)
    hour = now.hour
    
    if not (6 <= hour <= 22):
        return None
    
    # pH ideal: 7.2-7.6
    ph = random.uniform(7.1, 7.7)
    
    # Cloro livre ideal: 1.0-3.0 ppm
    chlorine = random.uniform(0.8, 3.5)
    
    # Alcalinidade ideal: 80-120 ppm
    alkalinity = random.uniform(75, 125)
    
    # Temperatura afeta os valores
    if 14 <= hour <= 17:  # Horário de maior uso
        # Cloro consome mais rápido
        chlorine *= random.uniform(0.7, 0.9)
        # pH pode subir
        ph += random.uniform(0, 0.2)
    
    return {
        'sensor_type': 'water_quality',
        'value': round(ph, 2),  # Usar pH como valor principal
        'unit': 'pH',
        'metadata': f'{{"ph": {round(ph, 2)}, "chlorine_ppm": {round(chlorine, 2)}, "alkalinity_ppm": {round(alkalinity, 1)}}}'
    }

def save_reading(reading_data):
    """Salva uma leitura de sensor normal no banco"""
    try:
        reading = Reading(
            sensor_id=reading_data['sensor_id'],
            activity=reading_data['detection'],  # 0 ou 1
            timestamp=datetime.now(TIMEZONE),
            sensor_metadata={
                'battery_level': reading_data['battery'],
                'protocol': reading_data['protocol'],
                'value': reading_data['value'],
                **(eval(reading_data.get('metadata', '{}')) if reading_data.get('metadata') else {})
            }
        )
        db.session.add(reading)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro ao salvar leitura: {e}")
        return False

def save_pool_reading(pool_data):
    """Salva uma leitura de sensor da piscina no banco"""
    try:
        now = datetime.now(TIMEZONE)
        
        # Preparar dados baseados no tipo
        temperature = None
        water_quality = None
        
        if pool_data['sensor_type'] in ['water_temp', 'ambient_temp']:
            temperature = pool_data['value']
        elif pool_data['sensor_type'] == 'water_quality':
            # Usar pH como temperatura temporariamente
            metadata = eval(pool_data.get('metadata', '{}'))
            ph = metadata.get('ph', 7.0)
            
            # Classificar qualidade
            if 7.2 <= ph <= 7.6 and metadata.get('chlorine_ppm', 0) >= 1.0:
                water_quality = 'Ótima'
            elif 7.0 <= ph <= 8.0:
                water_quality = 'Boa'
            elif 6.5 <= ph <= 8.5:
                water_quality = 'Regular'
            else:
                water_quality = 'Imprópria'
        
        reading = PoolReading(
            sensor_type=pool_data['sensor_type'],
            reading_date=now.date(),
            reading_time=now.time(),
            temperature=temperature,
            water_quality=water_quality
        )
        db.session.add(reading)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro ao salvar leitura da piscina: {e}")
        return False

def generate_event():
    """Gera um evento aleatório de sensor"""
    # Decidir entre sensor normal ou piscina (70% normal, 30% piscina)
    is_pool = random.random() < 0.3
    
    if is_pool:
        # Sensores da piscina
        pool_sensor_type = random.choice(['water_temp', 'ambient_temp', 'water_quality'])
        
        if pool_sensor_type == 'water_temp':
            data = generate_water_temp_reading()
            if data:
                if save_pool_reading(data):
                    return f"🌊 Piscina - Temp. Água: {data['value']}°C"
        elif pool_sensor_type == 'ambient_temp':
            data = generate_ambient_temp_reading()
            if data:
                if save_pool_reading(data):
                    return f"🌡️ Piscina - Temp. Ambiente: {data['value']}°C"
        else:  # water_quality
            data = generate_water_quality_reading()
            if data:
                if save_pool_reading(data):
                    metadata = eval(data.get('metadata', '{}'))
                    return f"💧 Piscina - Qualidade: pH {metadata.get('ph', 0)}, Cloro {metadata.get('chlorine_ppm', 0)}ppm"
    else:
        # Sensores normais
        area_key = random.choice(list(AREAS.keys()))
        area = AREAS[area_key]
        sensor_id = random.choice(area['sensors'])
        
        # Buscar informações do sensor para determinar o protocolo
        sensor = Sensor.query.get(sensor_id)
        if not sensor:
            return None
        
        protocol = sensor.protocol.lower()
        
        # Gerar dados baseado no protocolo
        if protocol == 'lora':
            data = generate_lora_reading(sensor_id, area_key)
        elif protocol == 'zigbee':
            data = generate_pir_reading(sensor_id, area_key)  # Zigbee pode ser PIR
        elif protocol == 'sigfox':
            data = generate_dht_reading(sensor_id, area_key)  # Sigfox para temperatura
        elif protocol == 'rfid':
            data = generate_mq_reading(sensor_id, area_key)  # RFID para qualidade do ar
        else:
            # Protocolo desconhecido, usar PIR como padrão
            data = generate_pir_reading(sensor_id, area_key)
        
        if data and save_reading(data):
            detection_str = "✓ Presença" if data['detection'] == 1 else "○ Vazio"
            return f"{area['name']} [{sensor.serial_number}] - {data['protocol'].upper()} - {detection_str} - {data['value']:.1f} - 🔋{data['battery']}%"
    
    return None

def main():
    parser = argparse.ArgumentParser(
        description='Simulador de Eventos de Sensores - SmartCEU',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--interval', type=int, default=30,
                        help='Intervalo entre eventos em segundos (padrão: 30)')
    parser.add_argument('--duration', type=int, default=0,
                        help='Duração da simulação em minutos (0 = infinito)')
    parser.add_argument('--batch', type=int, default=0,
                        help='Gerar N eventos e sair (modo batch)')
    parser.add_argument('--sensor', type=str, default='all',
                        choices=['all', 'pool', 'presence', 'environment'],
                        help='Tipo de sensor a simular')
    
    args = parser.parse_args()
    
    app = create_app()
    
    with app.app_context():
        print('='*70)
        print('🎯 SIMULADOR DE EVENTOS DE SENSORES - SmartCEU')
        print('='*70)
        print()
        print(f'⏱️  Intervalo: {args.interval} segundos')
        
        if args.batch > 0:
            print(f'📦 Modo batch: {args.batch} eventos')
        elif args.duration > 0:
            print(f'⏰ Duração: {args.duration} minutos')
        else:
            print('♾️  Duração: Infinito (Ctrl+C para parar)')
        
        print(f'🎚️  Filtro: {args.sensor}')
        print()
        print('='*70)
        print()
        
        start_time = datetime.now(TIMEZONE)
        events_count = 0
        
        try:
            if args.batch > 0:
                # Modo batch
                for i in range(args.batch):
                    result = generate_event()
                    if result:
                        events_count += 1
                        print(f"[{events_count:04d}] {datetime.now(TIMEZONE).strftime('%H:%M:%S')} - {result}")
                print()
                print(f'✅ {events_count} eventos gerados com sucesso!')
            else:
                # Modo contínuo
                while True:
                    result = generate_event()
                    if result:
                        events_count += 1
                        now = datetime.now(TIMEZONE)
                        elapsed = (now - start_time).seconds
                        print(f"[{events_count:04d}] {now.strftime('%H:%M:%S')} (+{elapsed}s) - {result}")
                    
                    # Verificar duração
                    if args.duration > 0:
                        elapsed_minutes = (datetime.now(TIMEZONE) - start_time).seconds / 60
                        if elapsed_minutes >= args.duration:
                            break
                    
                    time.sleep(args.interval)
                
        except KeyboardInterrupt:
            print()
            print()
            print('='*70)
            print('⏹️  Simulação interrompida pelo usuário')
        
        # Estatísticas finais
        end_time = datetime.now(TIMEZONE)
        duration = (end_time - start_time).seconds
        
        print('='*70)
        print('📊 ESTATÍSTICAS DA SIMULAÇÃO')
        print('='*70)
        print(f'🎯 Total de eventos: {events_count}')
        print(f'⏱️  Duração: {duration} segundos ({duration//60}m {duration%60}s)')
        if duration > 0:
            print(f'⚡ Taxa: {events_count/duration*60:.1f} eventos/minuto')
        print('='*70)
        print()
        print('✅ Simulação finalizada com sucesso!')
        print()

if __name__ == '__main__':
    main()
