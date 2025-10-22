#!/usr/bin/env python3
"""
Teste para entender como MySQL está interpretando os horários.
"""
import sys
sys.path.insert(0, '/var/www/smartceu/app/backend')

from datetime import datetime, time, date
from zoneinfo import ZoneInfo
from app import create_app, db
from app.models.pool_reading import PoolReading

# Timezone
TIMEZONE = ZoneInfo('America/Sao_Paulo')

app = create_app()

with app.app_context():
    print(f"⏰ Hora atual do servidor: {datetime.now()}")
    print(f"⏰ Hora atual com timezone: {datetime.now(TIMEZONE)}")
    print()
    
    # Criar uma leitura de teste com hora conhecida
    test_date = date.today()
    test_hour = datetime.now(TIMEZONE).hour
    test_minute = datetime.now(TIMEZONE).minute
    
    # Método 1: time simples
    t1 = time(test_hour, test_minute, 0)
    print(f"📝 Método 1 - time simples:")
    print(f"   Criado: time({test_hour}, {test_minute}, 0)")
    print(f"   Resultado: {t1}")
    print()
    
    # Método 2: datetime com timezone -> time
    dt2 = datetime(test_date.year, test_date.month, test_date.day, 
                   test_hour, test_minute, 0, tzinfo=TIMEZONE)
    t2 = dt2.time().replace(tzinfo=None)
    print(f"📝 Método 2 - datetime com timezone -> time:")
    print(f"   Criado: datetime(..., tzinfo=TIMEZONE).time().replace(tzinfo=None)")
    print(f"   Datetime: {dt2}")
    print(f"   Time: {dt2.time()}")
    print(f"   Time sem tz: {t2}")
    print()
    
    # Método 3: datetime sem timezone -> time
    dt3 = datetime(test_date.year, test_date.month, test_date.day, 
                   test_hour, test_minute, 0)
    t3 = dt3.time()
    print(f"📝 Método 3 - datetime sem timezone -> time:")
    print(f"   Criado: datetime(...).time()")
    print(f"   Datetime: {dt3}")
    print(f"   Time: {t3}")
    print()
    
    # Testar salvando e lendo do banco
    print("💾 Testando salvamento no banco de dados...")
    
    # Limpar leituras de teste antigas
    PoolReading.query.filter(PoolReading.sensor_type == 'TEST').delete()
    
    # Criar uma leitura de teste
    test_reading = PoolReading(
        sensor_type='TEST',
        reading_date=test_date,
        reading_time=t2,  # Usando método 2
        temperature=25.5
    )
    
    db.session.add(test_reading)
    db.session.commit()
    
    print(f"   ✅ Salvo: {test_date} {t2}")
    
    # Ler de volta do banco
    retrieved = PoolReading.query.filter(PoolReading.sensor_type == 'TEST').first()
    print(f"   📖 Lido: {retrieved.reading_date} {retrieved.reading_time}")
    print(f"   to_dict: {retrieved.to_dict()}")
    
    # Limpar
    db.session.delete(retrieved)
    db.session.commit()
