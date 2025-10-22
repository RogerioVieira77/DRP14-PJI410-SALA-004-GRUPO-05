"""
Query direta aos dados da tabela pool_readings usando PyMySQL
"""
import pymysql
from datetime import datetime

# Configurações de conexão do .env
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'ceu_tres_pontes',
    'password': 'CeuTresPontes2025!',
    'database': 'ceu_tres_pontes_db',
    'charset': 'utf8mb4'
}

print("\n" + "=" * 90)
print("📊 CONSULTA DE DADOS DA TABELA POOL_READINGS")
print("=" * 90 + "\n")

try:
    # Tentar conectar
    print("🔌 Tentando conectar ao MySQL...")
    connection = pymysql.connect(**MYSQL_CONFIG)
    print("✅ Conexão estabelecida com sucesso!\n")
    
    with connection.cursor() as cursor:
        # Contar total de registros
        cursor.execute("SELECT COUNT(*) FROM pool_readings")
        total = cursor.fetchone()[0]
        print(f"📈 Total de registros na tabela: {total}\n")
        
        if total == 0:
            print("⚠️  Tabela está vazia. Execute o script de migração primeiro!")
        else:
            # Buscar os 100 primeiros registros
            query = """
                SELECT 
                    id,
                    sensor_type,
                    reading_date,
                    reading_time,
                    temperature,
                    water_quality,
                    created_at
                FROM pool_readings
                ORDER BY reading_date DESC, reading_time DESC
                LIMIT 100
            """
            
            cursor.execute(query)
            readings = cursor.fetchall()
            
            print(f"📋 Exibindo {len(readings)} registro(s):\n")
            print("-" * 90)
            
            # Cabeçalho
            print(f"{'ID':<6} {'Tipo':<17} {'Data':<12} {'Hora':<10} {'Temp(°C)':<10} {'Qualidade':<15}")
            print("-" * 90)
            
            # Dados
            for r in readings:
                id_val = r[0]
                sensor_type = r[1]
                reading_date = r[2].strftime('%Y-%m-%d') if r[2] else 'N/A'
                reading_time = str(r[3]) if r[3] else 'N/A'
                temperature = f"{float(r[4]):.2f}" if r[4] else "---"
                water_quality = r[5] if r[5] else "---"
                
                print(f"{id_val:<6} {sensor_type:<17} {reading_date:<12} {reading_time:<10} {temperature:<10} {water_quality:<15}")
            
            print("-" * 90)
            
            # Estatísticas por tipo de sensor
            print("\n📊 RESUMO POR TIPO DE SENSOR:\n")
            
            cursor.execute("""
                SELECT sensor_type, COUNT(*) as count
                FROM pool_readings
                GROUP BY sensor_type
            """)
            
            for row in cursor.fetchall():
                print(f"   {row[0]:<20}: {row[1]} registro(s)")
            
            # Temperaturas médias
            print("\n🌡️  TEMPERATURAS:\n")
            
            cursor.execute("""
                SELECT AVG(temperature)
                FROM pool_readings
                WHERE sensor_type = 'water_temp'
            """)
            water_temp_avg = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT AVG(temperature)
                FROM pool_readings
                WHERE sensor_type = 'ambient_temp'
            """)
            ambient_temp_avg = cursor.fetchone()[0]
            
            if water_temp_avg:
                print(f"   Temperatura Média da Água:     {float(water_temp_avg):.2f}°C")
            else:
                print(f"   Temperatura Média da Água:     Sem dados")
            
            if ambient_temp_avg:
                print(f"   Temperatura Média Ambiente:    {float(ambient_temp_avg):.2f}°C")
            else:
                print(f"   Temperatura Média Ambiente:    Sem dados")
            
            # Qualidade da água
            print("\n💧 QUALIDADE DA ÁGUA:\n")
            
            cursor.execute("""
                SELECT water_quality, COUNT(*) as count
                FROM pool_readings
                WHERE water_quality IS NOT NULL
                GROUP BY water_quality
            """)
            
            for row in cursor.fetchall():
                count = row[1]
                percentage = (count / total) * 100
                print(f"   {row[0]:<15}: {count} registro(s) ({percentage:.1f}%)")
    
    connection.close()
    
    print("\n" + "=" * 90)
    print("✅ Consulta concluída!")
    print("=" * 90 + "\n")

except pymysql.err.OperationalError as e:
    print(f"\n❌ ERRO DE CONEXÃO: {e}")
    print("\n💡 SOLUÇÕES:")
    print("   1. Verifique se o MySQL está rodando")
    print("   2. Ajuste as credenciais no topo deste arquivo:")
    print(f"      - Usuário atual: '{MYSQL_CONFIG['user']}'")
    print(f"      - Senha atual: '{MYSQL_CONFIG['password'] or '(vazio)'}'")
    print(f"      - Banco: '{MYSQL_CONFIG['database']}'")
    print("\n   3. Tente executar manualmente no MySQL:")
    print("      SELECT * FROM pool_readings LIMIT 10;\n")

except Exception as e:
    print(f"\n❌ ERRO: {e}")
