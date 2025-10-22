#!/usr/bin/env python3
"""
Verifica todas as leituras de hoje para entender a distribuição.
"""
import sys
sys.path.insert(0, '/var/www/smartceu/app/backend')

from datetime import date
from app import create_app, db
from app.models.pool_reading import PoolReading

app = create_app()

with app.app_context():
    today = date.today()
    
    print(f"📅 Verificando leituras de hoje: {today}")
    print()
    
    # Buscar todas as leituras de hoje
    today_readings = PoolReading.query.filter(
        PoolReading.reading_date == today
    ).order_by(
        PoolReading.reading_time.desc()
    ).limit(10).all()
    
    if today_readings:
        print(f"📊 {len(today_readings)} últimas leituras de hoje:")
        for reading in today_readings:
            print(f"   {reading.sensor_type:15} - {reading.reading_time} - Temp: {reading.temperature}")
        
        # Estatísticas
        print()
        print(f"⏰ Horários:")
        print(f"   Mais recente: {today_readings[0].reading_time}")
        print(f"   Mais antiga (dos últimos 10): {today_readings[-1].reading_time}")
    else:
        print("❌ Nenhuma leitura encontrada para hoje")
