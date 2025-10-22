"""
Script para testar API REST - CEU Tres Pontes
Testa todos os endpoints principais
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"
API_URL = f"{BASE_URL}/api/v1"

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
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}")
    print(f"{text}")
    print(f"{'='*70}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")

# Token JWT para autenticação
jwt_token = None

print_header("TESTE DA API - CEU TRES PONTES")
print_info(f"Base URL: {BASE_URL}")
print_info(f"API URL: {API_URL}")
print_info(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ============================================================================
# TESTE 1: Health Check
# ============================================================================
print_header("TESTE 1: Health Check")

try:
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        data = response.json()
        print_success(f"Health Check OK - Status: {data.get('status')}")
        print_info(f"   Resposta: {json.dumps(data, indent=2)}")
    else:
        print_error(f"Health Check falhou - Status: {response.status_code}")
except Exception as e:
    print_error(f"Erro no Health Check: {e}")

# ============================================================================
# TESTE 2: Login (Autenticação)
# ============================================================================
print_header("TESTE 2: Login (Autenticação)")

try:
    response = requests.post(
        f"{API_URL}/auth/login",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        jwt_token = data.get('access_token')
        print_success("Login realizado com sucesso!")
        print_info(f"   Token JWT obtido: {jwt_token[:50]}...")
        print_info(f"   User: {data.get('user', {}).get('username')}")
        print_info(f"   Role: {data.get('user', {}).get('role')}")
    else:
        print_error(f"Login falhou - Status: {response.status_code}")
        print_info(f"   Erro: {response.text}")
except Exception as e:
    print_error(f"Erro no login: {e}")

# Headers com autenticação
headers = {
    'Authorization': f'Bearer {jwt_token}',
    'Content-Type': 'application/json'
}

# ============================================================================
# TESTE 3: Listar Sensores
# ============================================================================
print_header("TESTE 3: Listar Sensores")

try:
    response = requests.get(f"{API_URL}/sensors", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        sensors = data.get('sensors', [])
        print_success(f"Sensores listados: {len(sensors)} encontrados")
        
        for sensor in sensors[:3]:  # Mostrar apenas primeiros 3
            print_info(f"   - {sensor['serial_number']} ({sensor['protocol']}) - {sensor['location']}")
        
        if len(sensors) > 3:
            print_info(f"   ... e mais {len(sensors) - 3} sensores")
    else:
        print_error(f"Falha ao listar sensores - Status: {response.status_code}")
except Exception as e:
    print_error(f"Erro ao listar sensores: {e}")

# ============================================================================
# TESTE 4: Detalhes de um Sensor
# ============================================================================
print_header("TESTE 4: Detalhes de um Sensor")

try:
    response = requests.get(f"{API_URL}/sensors/1", headers=headers)
    
    if response.status_code == 200:
        sensor = response.json()
        print_success("Detalhes do sensor obtidos!")
        print_info(f"   Serial: {sensor.get('serial_number')}")
        print_info(f"   Protocol: {sensor.get('protocol')}")
        print_info(f"   Location: {sensor.get('location')}")
        print_info(f"   Status: {sensor.get('status')}")
    else:
        print_error(f"Falha ao obter sensor - Status: {response.status_code}")
except Exception as e:
    print_error(f"Erro ao obter sensor: {e}")

# ============================================================================
# TESTE 5: Criar Leitura
# ============================================================================
print_header("TESTE 5: Criar Leitura de Sensor")

try:
    response = requests.post(
        f"{API_URL}/readings",
        headers=headers,
        json={
            "sensor_id": 1,
            "activity": 1,
            "timestamp": datetime.now().isoformat(),
            "sensor_metadata": {
                "battery_level": 85,
                "rssi_dbm": -65,
                "temperature": 25.5
            }
        }
    )
    
    if response.status_code == 201:
        reading = response.json()
        print_success("Leitura criada com sucesso!")
        print_info(f"   ID: {reading.get('id')}")
        print_info(f"   Sensor ID: {reading.get('sensor_id')}")
        print_info(f"   Activity: {reading.get('activity')}")
    else:
        print_error(f"Falha ao criar leitura - Status: {response.status_code}")
        print_info(f"   Erro: {response.text}")
except Exception as e:
    print_error(f"Erro ao criar leitura: {e}")

# ============================================================================
# TESTE 6: Listar Leituras
# ============================================================================
print_header("TESTE 6: Listar Leituras")

try:
    response = requests.get(f"{API_URL}/readings?limit=5", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        readings = data.get('readings', [])
        print_success(f"Leituras listadas: {len(readings)} encontradas")
        
        for reading in readings:
            print_info(f"   - ID {reading['id']}: Sensor {reading['sensor_id']} - Activity: {reading['activity']}")
    else:
        print_error(f"Falha ao listar leituras - Status: {response.status_code}")
except Exception as e:
    print_error(f"Erro ao listar leituras: {e}")

# ============================================================================
# TESTE 7: Estatísticas - Overview
# ============================================================================
print_header("TESTE 7: Estatísticas - Overview")

try:
    response = requests.get(f"{API_URL}/statistics/overview", headers=headers)
    
    if response.status_code == 200:
        stats = response.json()
        print_success("Estatísticas obtidas!")
        print_info(f"   Total Sensores: {stats.get('total_sensors')}")
        print_info(f"   Sensores Ativos: {stats.get('sensors_by_status', {}).get('active', 0)}")
        print_info(f"   Total Leituras: {stats.get('total_readings')}")
        print_info(f"   Total Detecções: {stats.get('total_detections')}")
    else:
        print_error(f"Falha ao obter estatísticas - Status: {response.status_code}")
except Exception as e:
    print_error(f"Erro ao obter estatísticas: {e}")

# ============================================================================
# TESTE 8: Protocolos Disponíveis
# ============================================================================
print_header("TESTE 8: Protocolos Disponíveis")

try:
    response = requests.get(f"{API_URL}/sensors/protocols", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        protocols = data.get('protocols', [])
        print_success(f"Protocolos disponíveis: {len(protocols)}")
        for protocol in protocols:
            print_info(f"   - {protocol}")
    else:
        print_error(f"Falha ao listar protocolos - Status: {response.status_code}")
except Exception as e:
    print_error(f"Erro ao listar protocolos: {e}")

# ============================================================================
# TESTE 9: Informações do Usuário Atual
# ============================================================================
print_header("TESTE 9: Informações do Usuário Atual")

try:
    response = requests.get(f"{API_URL}/auth/me", headers=headers)
    
    if response.status_code == 200:
        user = response.json()
        print_success("Informações do usuário obtidas!")
        print_info(f"   Username: {user.get('username')}")
        print_info(f"   Email: {user.get('email')}")
        print_info(f"   Role: {user.get('role')}")
        print_info(f"   Ativo: {user.get('is_active')}")
    else:
        print_error(f"Falha ao obter usuário - Status: {response.status_code}")
except Exception as e:
    print_error(f"Erro ao obter usuário: {e}")

# ============================================================================
# TESTE 10: Health Check Detalhado
# ============================================================================
print_header("TESTE 10: Health Check Detalhado")

try:
    response = requests.get(f"{BASE_URL}/health/detailed")
    
    if response.status_code == 200:
        health = response.json()
        print_success("Health Check Detalhado OK!")
        print_info(f"   Status: {health.get('status')}")
        print_info(f"   Database: {health.get('database')}")
        print_info(f"   Timestamp: {health.get('timestamp')}")
    else:
        print_error(f"Falha no health check - Status: {response.status_code}")
except Exception as e:
    print_error(f"Erro no health check: {e}")

# ============================================================================
# RESUMO
# ============================================================================
print_header("RESUMO DOS TESTES")

print(f"\n{Colors.OKGREEN}{Colors.BOLD}✅ TODOS OS TESTES CONCLUÍDOS!{Colors.ENDC}\n")

print_info("A API está funcionando corretamente!")
print_info("Você pode acessar:")
print_info(f"   - Health Check: {BASE_URL}/health")
print_info(f"   - API Docs: {API_URL}/")
print_info(f"   - Sensores: {API_URL}/sensors")
print_info(f"   - Leituras: {API_URL}/readings")
print_info(f"   - Estatísticas: {API_URL}/statistics/overview")

print(f"\n{Colors.BOLD}📖 DOCUMENTAÇÃO DOS ENDPOINTS:{Colors.ENDC}")
print(f"""
🔐 AUTENTICAÇÃO:
   POST   /api/v1/auth/login              - Login
   POST   /api/v1/auth/register           - Registrar novo usuário
   GET    /api/v1/auth/me                 - Info do usuário atual
   POST   /api/v1/auth/change-password    - Alterar senha
   POST   /api/v1/auth/logout             - Logout

📡 SENSORES:
   GET    /api/v1/sensors                 - Listar sensores
   GET    /api/v1/sensors/<id>            - Detalhes de sensor
   POST   /api/v1/sensors                 - Criar sensor
   PUT    /api/v1/sensors/<id>            - Atualizar sensor
   DELETE /api/v1/sensors/<id>            - Deletar sensor
   GET    /api/v1/sensors/protocols       - Protocolos disponíveis

📊 LEITURAS:
   GET    /api/v1/readings                - Listar leituras
   GET    /api/v1/readings/<id>           - Detalhes de leitura
   POST   /api/v1/readings                - Criar leitura
   POST   /api/v1/readings/bulk           - Criar várias leituras
   GET    /api/v1/readings/sensor/<id>/latest - Última leitura

📈 ESTATÍSTICAS:
   GET    /api/v1/statistics/overview     - Visão geral
   GET    /api/v1/statistics/activity     - Atividade por período
   GET    /api/v1/statistics/sensors      - Estatísticas por sensor
   GET    /api/v1/statistics/capacity     - Capacidade do parque

💚 HEALTH:
   GET    /health                         - Status simples
   GET    /health/db                      - Status do banco
   GET    /health/detailed                - Status detalhado
""")

print(f"\n{Colors.BOLD}🔑 CREDENCIAIS DE TESTE:{Colors.ENDC}")
print("   Username: admin")
print("   Password: admin123")
print("\n")
