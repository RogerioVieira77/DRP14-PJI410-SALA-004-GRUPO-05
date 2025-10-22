"""
Script para popular o banco de dados com leituras de teste
Gera 5 dias de dados para todos os sensores
"""

import pymysql
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
load_dotenv('backend/.env')

# Configuração do banco
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'ceu_tres_pontes'),
    'password': os.getenv('DB_PASSWORD', 'CeuTresPontes2025!'),
    'database': os.getenv('DB_NAME', 'ceu_tres_pontes_db'),
    'charset': 'utf8mb4'
}

print(f"📡 Tentando conectar ao banco: {DB_CONFIG['user']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}")
print(f"🔑 Senha configurada: {'✅ Sim' if DB_CONFIG['password'] else '❌ Não'}\n")

def generate_readings():
    """Gera leituras de teste para 5 dias"""
    
    connection = pymysql.connect(**DB_CONFIG)
    cursor = connection.cursor()
    
    try:
        # Buscar todos os sensores
        cursor.execute("SELECT id, serial_number, location FROM sensors")
        sensors = cursor.fetchall()
        
        print(f"📡 Encontrados {len(sensors)} sensores")
        print("=" * 60)
        
        # Data inicial: 5 dias atrás
        start_date = datetime.now() - timedelta(days=5)
        
        total_readings = 0
        
        for sensor_id, serial_number, location in sensors:
            sensor_readings = 0
            print(f"\n🔄 Processando: {serial_number} ({location})")
            
            # Para cada dia
            for day in range(5):
                # Número de leituras para este dia (entre 100 e 300)
                daily_readings = random.randint(100, 300)
                
                day_start = start_date + timedelta(days=day)
                
                # Gerar leituras distribuídas ao longo do dia
                for i in range(daily_readings):
                    # Timestamp aleatório dentro do dia
                    random_seconds = random.randint(0, 86399)  # segundos em 24h
                    timestamp = day_start + timedelta(seconds=random_seconds)
                    
                    # Atividade: sensores de entrada/saída têm mais atividade
                    if 'entrada' in location.lower() or 'saida' in location.lower():
                        activity = random.choices([0, 1], weights=[60, 40])[0]  # 40% atividade
                    elif 'portaria' in location.lower():
                        activity = random.choices([0, 1], weights=[70, 30])[0]  # 30% atividade
                    elif 'banheiro' in location.lower():
                        activity = random.choices([0, 1], weights=[80, 20])[0]  # 20% atividade
                    else:
                        activity = random.choices([0, 1], weights=[85, 15])[0]  # 15% atividade
                    
                    # Metadados do sensor (simulação realista)
                    battery_level = random.randint(65, 100)
                    signal_strength = random.randint(-90, -50)
                    
                    # Ocasionalmente adicionar temperatura e umidade
                    sensor_metadata = {
                        'battery_level': battery_level,
                        'signal_strength': signal_strength
                    }
                    
                    if random.random() > 0.7:  # 30% das leituras têm temperatura
                        sensor_metadata['temperature'] = round(random.uniform(18.0, 28.0), 1)
                    
                    if random.random() > 0.7:  # 30% das leituras têm umidade
                        sensor_metadata['humidity'] = round(random.uniform(40.0, 70.0), 1)
                    
                    # Inserir leitura
                    cursor.execute("""
                        INSERT INTO readings 
                        (sensor_id, activity, timestamp, sensor_metadata, created_at)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        sensor_id,
                        activity,
                        timestamp,
                        str(sensor_metadata).replace("'", '"'),
                        datetime.now()
                    ))
                    
                    sensor_readings += 1
                    total_readings += 1
                
                # Atualizar sensor após cada dia
                cursor.execute("""
                    UPDATE sensors 
                    SET 
                        total_readings = %s,
                        last_reading_at = %s,
                        battery_level = %s,
                        signal_strength = %s
                    WHERE id = %s
                """, (
                    sensor_readings,
                    timestamp,
                    battery_level,
                    signal_strength,
                    sensor_id
                ))
                
                connection.commit()
                print(f"  ✅ Dia {day + 1}: {daily_readings} leituras criadas")
            
            print(f"  📊 Total para {serial_number}: {sensor_readings} leituras")
        
        print("\n" + "=" * 60)
        print(f"✅ CONCLUÍDO!")
        print(f"📊 Total de leituras criadas: {total_readings}")
        print(f"📅 Período: {start_date.strftime('%d/%m/%Y')} até {datetime.now().strftime('%d/%m/%Y')}")
        
        # Mostrar estatísticas finais
        cursor.execute("SELECT COUNT(*) FROM readings")
        total_db = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM readings WHERE activity = 1")
        total_activity = cursor.fetchone()[0]
        
        print(f"\n📈 Estatísticas do Banco:")
        print(f"  • Total de leituras: {total_db}")
        print(f"  • Detecções (activity=1): {total_activity}")
        print(f"  • Taxa de detecção: {round((total_activity/total_db)*100, 2)}%")
        
    except Exception as e:
        connection.rollback()
        print(f"\n❌ Erro: {e}")
        raise
    
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 POPULANDO BANCO DE DADOS COM LEITURAS DE TESTE")
    print("=" * 60)
    print(f"📅 Gerando dados para 5 dias")
    print(f"📊 Média: 100-300 leituras por sensor/dia")
    print("=" * 60)
    
    confirm = input("\n⚠️  Deseja continuar? (s/n): ")
    if confirm.lower() != 's':
        print("❌ Operação cancelada")
        exit()
    
    print("\n🔄 Iniciando população do banco...\n")
    generate_readings()
    print("\n✅ Script finalizado com sucesso!")
