"""
Script de Teste Geral - CEU Tres Pontes
Testa todos os componentes da aplicação

Fase 1: Simuladores
Fase 2: Gateway + MQTT
Fase 3: Backend + Banco de Dados
"""

import sys
import os
from datetime import datetime

# Cores para output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")

# Contadores
tests_passed = 0
tests_failed = 0
tests_skipped = 0

print_header("TESTE GERAL - CEU TRES PONTES")
print_info(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print_info(f"Python: {sys.version.split()[0]}")
print_info(f"Diretório: {os.getcwd()}")

# ============================================================================
# TESTE 1: Verificar Ambiente Virtual
# ============================================================================
print_header("TESTE 1: Verificar Ambiente Virtual")

try:
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if in_venv:
        print_success(f"Ambiente virtual ativo: {sys.prefix}")
        tests_passed += 1
    else:
        print_warning("Ambiente virtual NÃO está ativo!")
        print_info("Execute: .\\venv\\Scripts\\Activate.ps1")
        tests_failed += 1
except Exception as e:
    print_error(f"Erro ao verificar ambiente virtual: {e}")
    tests_failed += 1

# ============================================================================
# TESTE 2: Verificar Dependências Python
# ============================================================================
print_header("TESTE 2: Verificar Dependências Python")

dependencies = {
    'flask': 'Flask',
    'flask_sqlalchemy': 'Flask-SQLAlchemy',
    'flask_migrate': 'Flask-Migrate',
    'flask_jwt_extended': 'Flask-JWT-Extended',
    'flask_cors': 'Flask-CORS',
    'flask_marshmallow': 'Flask-Marshmallow',
    'marshmallow': 'marshmallow',
    'sqlalchemy': 'SQLAlchemy',
    'pymysql': 'PyMySQL',
    'paho.mqtt.client': 'paho-mqtt',
    'dotenv': 'python-dotenv'
}

for module, name in dependencies.items():
    try:
        __import__(module)
        print_success(f"{name} instalado")
        tests_passed += 1
    except ImportError:
        print_error(f"{name} NÃO instalado")
        tests_failed += 1

# ============================================================================
# TESTE 3: Verificar Estrutura de Arquivos
# ============================================================================
print_header("TESTE 3: Verificar Estrutura de Arquivos")

required_files = [
    'backend/app.py',
    'backend/app/__init__.py',
    'backend/app/config.py',
    'backend/app/models/__init__.py',
    'backend/app/models/sensor.py',
    'backend/app/models/reading.py',
    'backend/app/models/user.py',
    'backend/app/models/alert.py',
    'backend/app/models/statistics.py',
    'backend/app/routes/__init__.py',
    'backend/app/routes/health.py',
    'backend/app/routes/auth.py',
    'backend/app/routes/sensors.py',
    'backend/app/routes/readings.py',
    'backend/app/routes/statistics.py',
    'backend/gateway/gateway.py',
    'backend/gateway/mqtt_client.py',
    'sensores/base_sensor.py',
    'sensores/lora_sensor.py',
    'sensores/zigbee_sensor.py',
    '.env',
    '.flaskenv'
]

for file_path in required_files:
    if os.path.exists(file_path):
        print_success(f"{file_path}")
        tests_passed += 1
    else:
        print_error(f"{file_path} NÃO encontrado")
        tests_failed += 1

# ============================================================================
# TESTE 4: Teste dos Simuladores (Fase 1)
# ============================================================================
print_header("TESTE 4: Simuladores de Sensores (Fase 1)")

try:
    from sensores import LoRaSensor, ZigBeeSensor, SigfoxSensor, RFIDSensor
    
    # Testar LoRa
    lora = LoRaSensor(location="Teste")
    reading = lora.simulate_detection()
    assert 'serial_number' in reading
    assert 'protocol' in reading
    print_success("LoRa Sensor OK")
    tests_passed += 1
    
    # Testar ZigBee
    zigbee = ZigBeeSensor(location="Teste")
    reading = zigbee.simulate_detection()
    assert reading['protocol'] == 'ZigBee'
    print_success("ZigBee Sensor OK")
    tests_passed += 1
    
    # Testar Sigfox
    sigfox = SigfoxSensor(location="Teste")
    reading = sigfox.simulate_detection()
    assert reading['protocol'] == 'Sigfox'
    print_success("Sigfox Sensor OK")
    tests_passed += 1
    
    # Testar RFID
    rfid = RFIDSensor(location="Teste")
    reading = rfid.simulate_detection()
    assert reading['protocol'] == 'RFID'
    print_success("RFID Sensor OK")
    tests_passed += 1
    
except Exception as e:
    print_error(f"Erro nos simuladores: {e}")
    tests_failed += 1

# ============================================================================
# TESTE 5: Verificar Configurações (.env)
# ============================================================================
print_header("TESTE 5: Verificar Configurações (.env)")

try:
    from dotenv import load_dotenv
    load_dotenv()
    
    env_vars = [
        'FLASK_APP',
        'DB_HOST',
        'DB_USER',
        'DB_PASSWORD',
        'DB_NAME',
        'MQTT_BROKER_HOST',
        'MQTT_BROKER_PORT',
        'SECRET_KEY',
        'JWT_SECRET_KEY'
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            # Não mostrar senhas completas
            if 'PASSWORD' in var or 'SECRET' in var:
                masked = value[:3] + '***' + value[-3:] if len(value) > 6 else '***'
                print_success(f"{var} = {masked}")
            else:
                print_success(f"{var} = {value}")
            tests_passed += 1
        else:
            print_warning(f"{var} não definido")
            tests_failed += 1
            
except Exception as e:
    print_error(f"Erro ao verificar .env: {e}")
    tests_failed += 1

# ============================================================================
# TESTE 6: Verificar Conexão MySQL
# ============================================================================
print_header("TESTE 6: Verificar Conexão com MySQL")

try:
    import pymysql
    from dotenv import load_dotenv
    load_dotenv()
    
    connection = pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'ceu_tres_pontes'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME', 'ceu_tres_pontes_db')
    )
    
    cursor = connection.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    
    print_success(f"MySQL conectado: {version[0]}")
    
    # Verificar tabelas
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    if tables:
        print_success(f"Tabelas encontradas: {len(tables)}")
        for table in tables:
            print_info(f"  - {table[0]}")
        tests_passed += 1
    else:
        print_warning("Nenhuma tabela encontrada! Execute: python backend/init_db.py")
        tests_failed += 1
    
    cursor.close()
    connection.close()
    tests_passed += 1
    
except Exception as e:
    print_error(f"Erro ao conectar ao MySQL: {e}")
    print_info("Verifique se o MySQL está rodando e as credenciais no .env")
    tests_failed += 1

# ============================================================================
# TESTE 7: Verificar Mosquitto MQTT
# ============================================================================
print_header("TESTE 7: Verificar Mosquitto MQTT")

try:
    import paho.mqtt.client as mqtt
    from dotenv import load_dotenv
    load_dotenv()
    
    mqtt_connected = False
    
    def on_connect(client, userdata, flags, rc):
        global mqtt_connected
        if rc == 0:
            mqtt_connected = True
    
    client = mqtt.Client()
    client.on_connect = on_connect
    
    broker_host = os.getenv('MQTT_BROKER_HOST', 'localhost')
    broker_port = int(os.getenv('MQTT_BROKER_PORT', 1883))
    
    client.connect(broker_host, broker_port, 60)
    client.loop_start()
    
    import time
    time.sleep(2)
    
    if mqtt_connected:
        print_success(f"Mosquitto conectado: {broker_host}:{broker_port}")
        tests_passed += 1
    else:
        print_error("Não foi possível conectar ao Mosquitto")
        print_info("Verifique se o serviço está rodando: Get-Service mosquitto")
        tests_failed += 1
    
    client.loop_stop()
    client.disconnect()
    
except Exception as e:
    print_error(f"Erro ao verificar Mosquitto: {e}")
    tests_failed += 1

# ============================================================================
# TESTE 8: Testar Importação do Backend
# ============================================================================
print_header("TESTE 8: Testar Importação do Backend")

try:
    sys.path.insert(0, 'backend')
    from app import create_app, db
    
    print_success("Backend importado com sucesso")
    
    # Criar app em contexto de teste
    app = create_app('development')
    print_success(f"App Flask criado: {app.name}")
    
    # Verificar blueprints registrados
    blueprints = list(app.blueprints.keys())
    print_success(f"Blueprints registrados: {len(blueprints)}")
    for bp in blueprints:
        print_info(f"  - {bp}")
    
    tests_passed += 1
    
except Exception as e:
    print_error(f"Erro ao importar backend: {e}")
    import traceback
    traceback.print_exc()
    tests_failed += 1

# ============================================================================
# TESTE 9: Testar Modelos do Banco de Dados
# ============================================================================
print_header("TESTE 9: Testar Modelos do Banco de Dados")

try:
    from app.models import Sensor, Reading, User, Alert, Statistics
    
    models = {
        'Sensor': Sensor,
        'Reading': Reading,
        'User': User,
        'Alert': Alert,
        'Statistics': Statistics
    }
    
    for model_name, model_class in models.items():
        # Verificar se o modelo tem __tablename__
        if hasattr(model_class, '__tablename__'):
            print_success(f"{model_name}: tabela '{model_class.__tablename__}'")
            tests_passed += 1
        else:
            print_warning(f"{model_name}: sem __tablename__")
            tests_failed += 1
            
except Exception as e:
    print_error(f"Erro ao testar modelos: {e}")
    tests_failed += 1

# ============================================================================
# TESTE 10: Verificar Rotas da API
# ============================================================================
print_header("TESTE 10: Verificar Rotas da API")

try:
    with app.app_context():
        routes = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                routes.append({
                    'endpoint': rule.endpoint,
                    'methods': ','.join(rule.methods - {'HEAD', 'OPTIONS'}),
                    'path': str(rule)
                })
        
        print_success(f"Total de rotas: {len(routes)}")
        
        # Agrupar por blueprint
        blueprints_routes = {}
        for route in routes:
            bp = route['endpoint'].split('.')[0] if '.' in route['endpoint'] else 'main'
            if bp not in blueprints_routes:
                blueprints_routes[bp] = []
            blueprints_routes[bp].append(route)
        
        for bp, bp_routes in blueprints_routes.items():
            print_info(f"\n  Blueprint '{bp}': {len(bp_routes)} rotas")
            for route in bp_routes[:5]:  # Mostrar apenas primeiras 5
                print_info(f"    {route['methods']:15} {route['path']}")
            if len(bp_routes) > 5:
                print_info(f"    ... e mais {len(bp_routes) - 5} rotas")
        
        tests_passed += 1
        
except Exception as e:
    print_error(f"Erro ao verificar rotas: {e}")
    tests_failed += 1

# ============================================================================
# RESUMO DOS TESTES
# ============================================================================
print_header("RESUMO DOS TESTES")

total_tests = tests_passed + tests_failed + tests_skipped
success_rate = (tests_passed / total_tests * 100) if total_tests > 0 else 0

print(f"\n{Colors.BOLD}Total de Testes:{Colors.ENDC} {total_tests}")
print_success(f"Passou: {tests_passed}")
if tests_failed > 0:
    print_error(f"Falhou: {tests_failed}")
if tests_skipped > 0:
    print_warning(f"Pulado: {tests_skipped}")

print(f"\n{Colors.BOLD}Taxa de Sucesso:{Colors.ENDC} {success_rate:.1f}%")

if success_rate == 100:
    print(f"\n{Colors.OKGREEN}{Colors.BOLD}🎉 TODOS OS TESTES PASSARAM! 🎉{Colors.ENDC}")
    print(f"{Colors.OKGREEN}Sua aplicação está pronta para uso!{Colors.ENDC}\n")
elif success_rate >= 80:
    print(f"\n{Colors.WARNING}{Colors.BOLD}⚠️  QUASE LÁ! ⚠️{Colors.ENDC}")
    print(f"{Colors.WARNING}Alguns componentes precisam de ajustes.{Colors.ENDC}\n")
else:
    print(f"\n{Colors.FAIL}{Colors.BOLD}❌ ATENÇÃO NECESSÁRIA ❌{Colors.ENDC}")
    print(f"{Colors.FAIL}Vários componentes precisam ser corrigidos.{Colors.ENDC}\n")

print_header("PRÓXIMOS PASSOS")

if tests_failed > 0:
    print_info("1. Revise os testes que falharam acima")
    print_info("2. Corrija os problemas identificados")
    print_info("3. Execute novamente: python test_aplicacao.py")
else:
    print_success("✅ Todos os componentes estão funcionando!")
    print_info("\nPara iniciar a aplicação:")
    print_info("  1. Inicializar banco: python backend/init_db.py")
    print_info("  2. Popular dados: flask seed-db")
    print_info("  3. Iniciar servidor: flask run")
    print_info("  4. Acessar: http://localhost:5000/api/v1/health")

print("\n")
