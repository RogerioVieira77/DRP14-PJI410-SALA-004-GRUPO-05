"""
Teste rápido da refatoração
Verifica se todos os endpoints continuam funcionando
"""

import requests
import json

API_URL = "http://localhost:5000/api/v1"

def test_health():
    """Testar health check"""
    print("1. Testando Health Check... ", end='')
    response = requests.get("http://localhost:5000/health")
    assert response.status_code == 200
    print("✅")

def test_login():
    """Testar login"""
    print("2. Testando Login... ", end='')
    response = requests.post(
        f"{API_URL}/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data
    assert 'user' in data
    print("✅")
    return data['access_token']

def test_profile(token):
    """Testar perfil"""
    print("3. Testando Perfil... ", end='')
    response = requests.get(
        f"{API_URL}/auth/me",
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    data = response.json()
    assert 'username' in data
    assert data['username'] == 'admin'
    print("✅")

def test_sensors(token):
    """Testar sensores"""
    print("4. Testando Sensores... ", end='')
    response = requests.get(
        f"{API_URL}/sensors",
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    data = response.json()
    assert 'sensors' in data
    assert len(data['sensors']) == 6
    print("✅")

def test_statistics(token):
    """Testar estatísticas"""
    print("5. Testando Estatísticas... ", end='')
    response = requests.get(
        f"{API_URL}/statistics/overview",
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    data = response.json()
    assert 'sensors' in data
    assert 'readings' in data
    print("✅")

def test_validation_error():
    """Testar validação de erro"""
    print("6. Testando Validação... ", end='')
    response = requests.post(
        f"{API_URL}/auth/login",
        json={"username": "admin"}  # Faltando password
    )
    assert response.status_code == 400
    data = response.json()
    assert 'error' in data or 'messages' in data
    print("✅")

def main():
    print("=" * 60)
    print("🧪 TESTE DA REFATORAÇÃO")
    print("=" * 60)
    print()
    
    try:
        test_health()
        token = test_login()
        test_profile(token)
        test_sensors(token)
        test_statistics(token)
        test_validation_error()
        
        print()
        print("=" * 60)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("=" * 60)
        print()
        print("📊 Resultados:")
        print("   • Health Check: OK")
        print("   • Login (refatorado): OK")
        print("   • Perfil (refatorado): OK")
        print("   • Sensores: OK")
        print("   • Estatísticas: OK")
        print("   • Validação de erros: OK")
        print()
        print("✨ A refatoração foi aplicada com sucesso!")
        print("🎯 Todos os endpoints continuam funcionando normalmente")
        
    except AssertionError as e:
        print(f"\n❌ ERRO: {e}")
        return 1
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRO: Servidor não está rodando")
        print("💡 Execute: flask run --host=0.0.0.0 --port=5000")
        return 1
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
