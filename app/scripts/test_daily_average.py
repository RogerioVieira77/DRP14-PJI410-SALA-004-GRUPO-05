#!/usr/bin/env python3
"""
Teste da nova API de média diária de temperatura.
"""
import sys
sys.path.insert(0, '/var/www/smartceu/app/backend')

from app import create_app
from app.services.pool_service import PoolService

app = create_app()

with app.app_context():
    print("📊 Testando cálculo de média diária de temperatura\n")
    
    # Testar temperatura da água
    print("💧 Temperatura da Água (últimos 10 dias):")
    water_averages = PoolService.get_daily_temperature_average('water_temp', days=10)
    
    if water_averages:
        for day in water_averages:
            print(f"  📅 {day['date']}: {day['avg_temperature']}°C (baseado em {day['reading_count']} leituras)")
    else:
        print("  ❌ Sem dados")
    
    print()
    
    # Testar temperatura ambiente
    print("☀️ Temperatura Ambiente (últimos 10 dias):")
    ambient_averages = PoolService.get_daily_temperature_average('ambient_temp', days=10)
    
    if ambient_averages:
        for day in ambient_averages:
            print(f"  📅 {day['date']}: {day['avg_temperature']}°C (baseado em {day['reading_count']} leituras)")
    else:
        print("  ❌ Sem dados")
