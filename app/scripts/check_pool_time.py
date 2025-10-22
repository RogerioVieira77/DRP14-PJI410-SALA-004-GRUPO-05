#!/usr/bin/env python3
"""
Script para verificar horários das leituras da piscina.
"""
import sys
sys.path.insert(0, '/var/www/smartceu/app/backend')

from app import create_app, db
from app.models.pool_reading import PoolReading
from datetime import datetime

app = create_app()

with app.app_context():
    # Pegar última leitura
    reading = PoolReading.query.order_by(PoolReading.id.desc()).first()
    
    if reading:
        print(f"📊 Última leitura no banco de dados:")
        print(f"   ID: {reading.id}")
        print(f"   Tipo: {reading.sensor_type}")
        print(f"   Data: {reading.reading_date}")
        print(f"   Hora: {reading.reading_time}")
        print(f"   Temperatura: {reading.temperature}")
        print(f"   Created at: {reading.created_at}")
        print()
        print(f"🔍 Serialização to_dict():")
        print(f"   {reading.to_dict()}")
        print()
        print(f"⏰ Hora atual do servidor:")
        print(f"   {datetime.now()}")
    else:
        print("❌ Nenhuma leitura encontrada")
