"""
Script para consultar dados da tabela pool_readings
"""
import sys
sys.path.insert(0, 'C:\\PI - IV - V1\\backend')

from app import create_app, db
from app.models.pool_reading import PoolReading
from sqlalchemy import func

print("\n" + "=" * 80)
print("📊 CONSULTA DE DADOS DA TABELA POOL_READINGS")
print("=" * 80 + "\n")

app = create_app('development')

with app.app_context():
    # Contar total de registros
    total = db.session.query(func.count(PoolReading.id)).scalar()
    print(f"📈 Total de registros na tabela: {total}\n")
    
    if total == 0:
        print("⚠️  Tabela está vazia. Nenhum registro encontrado.")
    else:
        # Buscar os 100 primeiros registros ordenados por data/hora
        readings = PoolReading.query.order_by(
            PoolReading.reading_date.desc(),
            PoolReading.reading_time.desc()
        ).limit(100).all()
        
        print(f"📋 Exibindo {len(readings)} registro(s):\n")
        print("-" * 80)
        
        # Cabeçalho
        print(f"{'ID':<6} {'Tipo':<15} {'Data':<12} {'Hora':<10} {'Temp(°C)':<10} {'Qualidade':<15}")
        print("-" * 80)
        
        # Dados
        for r in readings:
            id_str = str(r.id)
            tipo = r.sensor_type.value if hasattr(r.sensor_type, 'value') else str(r.sensor_type)
            data = r.reading_date.strftime('%Y-%m-%d') if r.reading_date else 'N/A'
            hora = r.reading_time.strftime('%H:%M:%S') if r.reading_time else 'N/A'
            temp = f"{r.temperature:.2f}" if r.temperature else "---"
            qual = r.water_quality.value if r.water_quality else "---"
            
            print(f"{id_str:<6} {tipo:<15} {data:<12} {hora:<10} {temp:<10} {qual:<15}")
        
        print("-" * 80)
        
        # Estatísticas por tipo de sensor
        print("\n📊 RESUMO POR TIPO DE SENSOR:\n")
        
        from app.models.pool_reading import SensorType
        
        for sensor_type in SensorType:
            count = PoolReading.query.filter_by(sensor_type=sensor_type).count()
            print(f"   {sensor_type.value:<20}: {count} registro(s)")
        
        # Se houver leituras de temperatura, mostrar médias
        print("\n🌡️  TEMPERATURAS:\n")
        
        water_temp_avg = db.session.query(func.avg(PoolReading.temperature)).filter(
            PoolReading.sensor_type == SensorType.WATER_TEMP
        ).scalar()
        
        ambient_temp_avg = db.session.query(func.avg(PoolReading.temperature)).filter(
            PoolReading.sensor_type == SensorType.AMBIENT_TEMP
        ).scalar()
        
        if water_temp_avg:
            print(f"   Temperatura Média da Água:     {water_temp_avg:.2f}°C")
        else:
            print(f"   Temperatura Média da Água:     Sem dados")
            
        if ambient_temp_avg:
            print(f"   Temperatura Média Ambiente:    {ambient_temp_avg:.2f}°C")
        else:
            print(f"   Temperatura Média Ambiente:    Sem dados")
        
        # Qualidade da água
        print("\n💧 QUALIDADE DA ÁGUA:\n")
        
        from app.models.pool_reading import WaterQuality
        
        for quality in WaterQuality:
            count = PoolReading.query.filter_by(water_quality=quality).count()
            if count > 0:
                percentage = (count / total) * 100
                print(f"   {quality.value:<15}: {count} registro(s) ({percentage:.1f}%)")

print("\n" + "=" * 80)
print("✅ Consulta concluída!")
print("=" * 80 + "\n")
