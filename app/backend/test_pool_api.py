"""
Teste de autenticação e endpoints da API de Pool
"""
import requests
import json

API_BASE = "http://localhost:5000/api/v1"

print("\n" + "=" * 70)
print("🧪 TESTE DE API - MONITORAMENTO DA PISCINA")
print("=" * 70 + "\n")

# Passo 1: Autenticação
print("1️⃣  Testando autenticação...")
print("-" * 70)

try:
    response = requests.post(
        f"{API_BASE}/auth/login",
        json={
            "username": "admin",
            "password": "admin123"
        },
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('access_token')
        print(f"✅ Token obtido: {token[:50]}..." if token else "❌ Token não encontrado")
    else:
        print("❌ Erro na autenticação")
        exit(1)
        
except Exception as e:
    print(f"❌ Erro: {e}")
    exit(1)

print()

# Passo 2: Testar endpoint /pool/readings/latest
print("2️⃣  Testando /pool/readings/latest...")
print("-" * 70)

try:
    response = requests.get(
        f"{API_BASE}/pool/readings/latest",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Resposta recebida:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"❌ Erro: {response.text}")
        
except Exception as e:
    print(f"❌ Erro: {e}")

print()

# Passo 3: Testar endpoint /pool/statistics
print("3️⃣  Testando /pool/statistics...")
print("-" * 70)

try:
    response = requests.get(
        f"{API_BASE}/pool/statistics?days=7",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Resposta recebida:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"❌ Erro: {response.text}")
        
except Exception as e:
    print(f"❌ Erro: {e}")

print()

# Passo 4: Testar endpoint /pool/alerts
print("4️⃣  Testando /pool/alerts...")
print("-" * 70)

try:
    response = requests.get(
        f"{API_BASE}/pool/alerts",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Resposta recebida:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"❌ Erro: {response.text}")
        
except Exception as e:
    print(f"❌ Erro: {e}")

print()

# Passo 5: Testar endpoint /pool/temperature/history
print("5️⃣  Testando /pool/temperature/history (water_temp)...")
print("-" * 70)

try:
    response = requests.get(
        f"{API_BASE}/pool/temperature/history?sensor_type=water_temp&days=7&limit=10",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Resposta recebida:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"❌ Erro: {response.text}")
        
except Exception as e:
    print(f"❌ Erro: {e}")

print("\n" + "=" * 70)
print("✅ Testes concluídos!")
print("=" * 70 + "\n")
