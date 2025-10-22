#!/usr/bin/env python3
"""
Script para verificar horários das últimas leituras por tipo.
"""
import sys
sys.path.insert(0, '/var/www/smartceu/app/backend')

from app import create_app, db
from app.models.pool_reading import PoolReading
from datetime import datetime
from sqlalchemy import desc

app = create_app()

with app.app_context():
    sensor_types = ['water_temp', 'ambient_temp', 'water_quality']
    
    print(f"⏰ Hora atual do servidor: {datetime.now()}")
    print()
    
    for sensor_type in sensor_types:
        reading = PoolReading.query.filter(
            PoolReading.sensor_type == sensor_type
        ).order_by(
            desc(PoolReading.reading_date),
            desc(PoolReading.reading_time)
        ).first()
        
        if reading:
            print(f"📊 {sensor_type}:")
            print(f"   Data: {reading.reading_date}")
            print(f"   Hora: {reading.reading_time}")
            if reading.temperature:
                print(f"   Temperatura: {reading.temperature}°C")
            if reading.water_quality:
                print(f"   Qualidade: {reading.water_quality}")
            print(f"   Created at: {reading.created_at}")
            print(f"   to_dict(): {reading.to_dict()}")
            print()
