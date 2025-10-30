#!/usr/bin/env python3
"""
Script para popular o banco com leituras de sensores para o dia atual
Simula um dia típico de funcionamento do CEU Três Pontes

Uso:
    python populate_readings_today.py [--quantidade N]
    
Exemplo:
    python populate_readings_today.py --quantidade 500
"""

import sys
import os
from datetime import datetime, timedelta
import random
import argparse

# Adicionar o diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.sensor import Sensor
from app.models.reading import Reading

# Configurações
HORARIO_ABERTURA = 6  # 06:00
HORARIO_FECHAMENTO = 22  # 22:00

# Padrão de fluxo de pessoas por hora
FLUXO_POR_HORA = {
    6: 20,   # 06:00 - Abertura (baixo)
    7: 40,   # 07:00 - Manhã cedo
    8: 80,   # 08:00 - Aumentando
    9: 120,  # 09:00 - Manhã ativa
    10: 150, # 10:00 - Pico manhã
    11: 140, # 11:00 - Mantendo
    12: 100, # 12:00 - Almoço (reduz)
    13: 90,  # 13:00 - Almoço
    14: 130, # 14:00 - Retorno almoço
    15: 160, # 15:00 - Pico tarde
    16: 180, # 16:00 - Pico máximo
    17: 150, # 17:00 - Tarde
    18: 110, # 18:00 - Começa a esvaziar
    19: 80,  # 19:00 - Noite
    20: 50,  # 20:00 - Noite avançada
    21: 30,  # 21:00 - Fechando
    22: 10   # 22:00 - Fechamento
}


def get_sensors():
    """Busca todos os sensores ativos do banco"""
    return Sensor.query.filter_by(status='active').all()


def generate_reading(sensor, timestamp, is_entry):
    """
    Gera uma leitura de sensor
    
    Args:
        sensor: Objeto Sensor
        timestamp: Datetime da leitura
        is_entry: True para entrada (activity=1), False para saída (activity=0)
    
    Returns:
        Reading object
    """
    # Metadados do sensor (temperatura e umidade simuladas)
    sensor_metadata = {
        'temperature': round(random.uniform(20.0, 32.0), 1),
        'humidity': round(random.uniform(40.0, 80.0), 1),
        'battery': round(random.uniform(80.0, 100.0), 1)
    }
    
    return Reading(
        sensor_id=sensor.id,
        timestamp=timestamp,
        activity=1 if is_entry else 0,
        sensor_metadata=sensor_metadata,
        message_id=f"MSG-{timestamp.strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}",
        gateway_id=f"GW-{sensor.protocol.upper()}-01"
    )


def populate_day(date=None, quantidade=None):
    """
    Popula o banco com leituras para um dia específico
    
    Args:
        date: Data para popular (default: hoje)
        quantidade: Número total de leituras a gerar (default: calculado pelo fluxo)
    """
    if date is None:
        date = datetime.now().date()
    
    sensors = get_sensors()
    
    if not sensors:
        print("❌ Erro: Nenhum sensor ativo encontrado no banco!")
        print("   Execute: flask seed-db")
        return False
    
    print(f"📊 Sensores disponíveis: {len(sensors)}")
    for sensor in sensors:
        print(f"   - {sensor.serial_number} ({sensor.location})")
    
    # Se quantidade não especificada, calcular baseado no fluxo padrão
    if quantidade is None:
        quantidade = sum(FLUXO_POR_HORA.values())
    
    print(f"\n🎯 Gerando {quantidade} leituras para {date.strftime('%d/%m/%Y')}...")
    
    readings = []
    entradas_total = 0
    saidas_total = 0
    
    # Distribuir leituras ao longo do dia
    for hora in range(HORARIO_ABERTURA, HORARIO_FECHAMENTO + 1):
        # Quantas leituras nesta hora (baseado no padrão)
        leituras_hora = FLUXO_POR_HORA.get(hora, 50)
        
        # Ajustar proporcionalmente se quantidade foi especificada
        if quantidade:
            proporcao = quantidade / sum(FLUXO_POR_HORA.values())
            leituras_hora = int(leituras_hora * proporcao)
        
        # Mais entradas nas primeiras horas, mais saídas nas últimas
        if hora < 14:
            ratio_entradas = 0.70  # 70% entradas
        elif hora < 18:
            ratio_entradas = 0.60  # 60% entradas
        else:
            ratio_entradas = 0.30  # 30% entradas (mais saídas)
        
        for _ in range(leituras_hora):
            # Timestamp aleatório dentro da hora
            minuto = random.randint(0, 59)
            segundo = random.randint(0, 59)
            timestamp = datetime.combine(date, datetime.min.time()) + \
                        timedelta(hours=hora, minutes=minuto, seconds=segundo)
            
            # Escolher sensor aleatório
            sensor = random.choice(sensors)
            
            # Determinar se é entrada ou saída
            is_entry = random.random() < ratio_entradas
            
            # Criar leitura
            reading = generate_reading(sensor, timestamp, is_entry)
            readings.append(reading)
            
            if is_entry:
                entradas_total += 1
            else:
                saidas_total += 1
    
    # Inserir no banco em lotes (mais eficiente)
    print(f"\n💾 Inserindo {len(readings)} leituras no banco...")
    try:
        batch_size = 100
        for i in range(0, len(readings), batch_size):
            batch = readings[i:i+batch_size]
            db.session.bulk_save_objects(batch)
            db.session.commit()
            print(f"   ✓ Inseridos {min(i+batch_size, len(readings))}/{len(readings)} registros")
        
        print(f"\n✅ Sucesso!")
        print(f"   📥 Entradas: {entradas_total}")
        print(f"   📤 Saídas: {saidas_total}")
        print(f"   👥 Pessoas atuais no CEU: {entradas_total - saidas_total}")
        print(f"   📊 Total de leituras: {len(readings)}")
        
        return True
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Erro ao inserir dados: {e}")
        return False


def clear_today_readings():
    """Remove todas as leituras de hoje (útil para repovoar)"""
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    count = Reading.query.filter(Reading.timestamp >= today_start).delete()
    db.session.commit()
    
    print(f"🗑️  Removidas {count} leituras de hoje")
    return count


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description='Popula o banco com leituras de sensores para hoje'
    )
    parser.add_argument(
        '--quantidade', '-q',
        type=int,
        help='Número de leituras a gerar (default: ~1200 baseado no fluxo típico)'
    )
    parser.add_argument(
        '--limpar', '-l',
        action='store_true',
        help='Limpar leituras de hoje antes de popular'
    )
    parser.add_argument(
        '--dias', '-d',
        type=int,
        default=0,
        help='Número de dias no passado para popular (0 = hoje, 1 = ontem, etc)'
    )
    
    args = parser.parse_args()
    
    # Criar aplicação Flask
    app = create_app('production')
    
    with app.app_context():
        print("=" * 60)
        print("🏊 SmartCEU - População de Leituras de Sensores")
        print("=" * 60)
        
        # Calcular data
        if args.dias > 0:
            target_date = (datetime.now() - timedelta(days=args.dias)).date()
            print(f"📅 Data alvo: {target_date.strftime('%d/%m/%Y')} ({args.dias} dia(s) atrás)")
        else:
            target_date = datetime.now().date()
            print(f"📅 Data alvo: HOJE ({target_date.strftime('%d/%m/%Y')})")
        
        # Limpar se solicitado
        if args.limpar and args.dias == 0:
            print("\n⚠️  Modo: LIMPAR + POPULAR")
            resposta = input("Confirma remoção das leituras de hoje? (s/N): ")
            if resposta.lower() == 's':
                clear_today_readings()
            else:
                print("❌ Operação cancelada")
                return
        
        # Popular
        success = populate_day(date=target_date, quantidade=args.quantidade)
        
        if success:
            print("\n" + "=" * 60)
            print("✅ Processo concluído com sucesso!")
            print("=" * 60)
            print("\n🌐 Acesse o dashboard:")
            print("   http://82.25.75.88/smartceu/dashboard")
        else:
            print("\n" + "=" * 60)
            print("❌ Processo finalizado com erros")
            print("=" * 60)
            sys.exit(1)


if __name__ == '__main__':
    main()
