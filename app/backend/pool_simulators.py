"""
Simuladores de Sensores de Monitoramento da Piscina
Gera dados realistas para temperatura da água, temperatura ambiente e qualidade da água.

Executa continuamente enviando leituras para a API a cada 30 segundos.
"""

import requests
import time
import random
from datetime import datetime, date
import json
import sys


# ============================================================
# CONFIGURAÇÕES
# ============================================================

API_BASE_URL = "http://localhost:5000/api/v1"
USERNAME = "admin"
PASSWORD = "admin123"

# Intervalo entre leituras (30 segundos conforme solicitado)
READING_INTERVAL = 30  # segundos

# Headers padrão
HEADERS = {
    "Content-Type": "application/json"
}


# ============================================================
# AUTENTICAÇÃO
# ============================================================

def get_auth_token():
    """
    Autentica na API e retorna o token JWT.
    
    Returns:
        str: Token JWT ou None se falhar
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            json={
                "username": USERNAME,
                "password": PASSWORD
            },
            headers=HEADERS,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            print(f"✅ Autenticado com sucesso!")
            return token
        else:
            print(f"❌ Erro na autenticação: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao conectar com API: {e}")
        return None


# ============================================================
# SIMULADORES DE SENSORES
# ============================================================

class WaterTempSensor:
    """Simulador de sensor de temperatura da água."""
    
    def __init__(self):
        self.current_temp = 26.0  # Temperatura inicial
        self.min_temp = 20.0
        self.max_temp = 35.0
    
    def read(self):
        """
        Gera uma leitura de temperatura da água.
        Simula variação gradual ao longo do dia.
        
        Returns:
            float: Temperatura em Celsius (20-35°C)
        """
        # Variação baseada na hora do dia
        hour = datetime.now().hour
        
        # Temperatura mais baixa de madrugada (4h), mais alta à tarde (15h)
        if 4 <= hour < 12:
            # Manhã: temperatura subindo
            target_temp = 24.0 + (hour - 4) * 0.5
        elif 12 <= hour < 18:
            # Tarde: temperatura alta
            target_temp = 28.0 + (hour - 12) * 0.3
        else:
            # Noite: temperatura caindo
            target_temp = 26.0 - (hour - 18) * 0.2 if hour >= 18 else 23.0
        
        # Adicionar variação aleatória pequena
        variation = random.uniform(-0.5, 0.5)
        self.current_temp = target_temp + variation
        
        # Garantir limites
        self.current_temp = max(self.min_temp, min(self.max_temp, self.current_temp))
        
        return round(self.current_temp, 2)


class AmbientTempSensor:
    """Simulador de sensor de temperatura ambiente."""
    
    def __init__(self):
        self.current_temp = 28.0
        self.min_temp = 25.0
        self.max_temp = 40.0
    
    def read(self):
        """
        Gera uma leitura de temperatura ambiente.
        Geralmente 2-5°C mais quente que a água.
        
        Returns:
            float: Temperatura em Celsius (25-40°C)
        """
        hour = datetime.now().hour
        
        # Temperatura ambiente segue padrão similar mas mais extremo
        if 4 <= hour < 12:
            target_temp = 26.0 + (hour - 4) * 1.0
        elif 12 <= hour < 18:
            target_temp = 32.0 + (hour - 12) * 1.2
        else:
            target_temp = 30.0 - (hour - 18) * 0.5 if hour >= 18 else 27.0
        
        # Adicionar variação aleatória
        variation = random.uniform(-1.0, 1.0)
        self.current_temp = target_temp + variation
        
        # Garantir limites
        self.current_temp = max(self.min_temp, min(self.max_temp, self.current_temp))
        
        return round(self.current_temp, 2)


class WaterQualitySensor:
    """Simulador de sensor de qualidade da água."""
    
    def __init__(self):
        self.qualities = ['Ótima', 'Boa', 'Regular', 'Imprópria']
        # Pesos para simular distribuição realista
        # Geralmente a água está boa, raramente imprópria
        self.weights = [0.50, 0.35, 0.12, 0.03]  # 50% Ótima, 35% Boa, 12% Regular, 3% Imprópria
        self.current_quality = 'Ótima'
        self.readings_count = 0
    
    def read(self):
        """
        Gera uma leitura de qualidade da água.
        Qualidade tende a se manter estável, mudanças graduais.
        
        Returns:
            str: Qualidade ('Ótima', 'Boa', 'Regular', 'Imprópria')
        """
        self.readings_count += 1
        
        # A cada 10 leituras, chance de mudança
        if self.readings_count % 10 == 0:
            # 30% de chance de mudar
            if random.random() < 0.3:
                self.current_quality = random.choices(self.qualities, weights=self.weights)[0]
        
        return self.current_quality


# ============================================================
# ENVIO DE LEITURAS
# ============================================================

def send_reading(token, sensor_type, temperature=None, water_quality=None):
    """
    Envia uma leitura para a API.
    
    Args:
        token: Token JWT de autenticação
        sensor_type: Tipo do sensor
        temperature: Temperatura (opcional)
        water_quality: Qualidade da água (opcional)
        
    Returns:
        bool: True se enviado com sucesso
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    data = {
        "sensor_type": sensor_type,
        "reading_date": date.today().isoformat(),
        "reading_time": datetime.now().strftime("%H:%M:%S")
    }
    
    if temperature is not None:
        data["temperature"] = temperature
    
    if water_quality is not None:
        data["water_quality"] = water_quality
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/pool/readings",
            json=data,
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 201:
            return True
        else:
            print(f"   ⚠️  Erro ao enviar {sensor_type}: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro de conexão ao enviar {sensor_type}: {e}")
        return False


# ============================================================
# LOOP PRINCIPAL
# ============================================================

def main():
    """Loop principal dos simuladores."""
    
    print("=" * 60)
    print("🏊 SIMULADORES DE MONITORAMENTO DA PISCINA")
    print("=" * 60)
    print(f"📡 API: {API_BASE_URL}")
    print(f"⏰ Intervalo: {READING_INTERVAL} segundos")
    print(f"👤 Usuário: {USERNAME}")
    print("=" * 60)
    print()
    
    # Criar instâncias dos sensores
    water_temp_sensor = WaterTempSensor()
    ambient_temp_sensor = AmbientTempSensor()
    water_quality_sensor = WaterQualitySensor()
    
    # Autenticar
    print("🔐 Autenticando...")
    token = get_auth_token()
    
    if not token:
        print("❌ Falha na autenticação. Encerrando.")
        sys.exit(1)
    
    print()
    print("✅ Simuladores iniciados!")
    print("   Pressione CTRL+C para parar")
    print()
    print("-" * 60)
    
    reading_count = 0
    
    try:
        while True:
            reading_count += 1
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\n📊 Leitura #{reading_count} - {timestamp}")
            print("-" * 60)
            
            # Gerar leituras
            water_temp = water_temp_sensor.read()
            ambient_temp = ambient_temp_sensor.read()
            water_quality = water_quality_sensor.read()
            
            # Indicador de alerta
            alert_indicator = ""
            if water_quality in ['Regular', 'Imprópria']:
                alert_indicator = " ⚠️ ALERTA!"
            
            print(f"🌡️  Temperatura da Água:    {water_temp}°C")
            print(f"🌡️  Temperatura Ambiente:   {ambient_temp}°C")
            print(f"💧 Qualidade da Água:      {water_quality}{alert_indicator}")
            
            # Enviar para API
            print("\n📤 Enviando para API...")
            
            success_count = 0
            
            if send_reading(token, "water_temp", temperature=water_temp):
                print("   ✅ Temperatura da água enviada")
                success_count += 1
            
            if send_reading(token, "ambient_temp", temperature=ambient_temp):
                print("   ✅ Temperatura ambiente enviada")
                success_count += 1
            
            if send_reading(token, "water_quality", water_quality=water_quality):
                print("   ✅ Qualidade da água enviada")
                success_count += 1
            
            if success_count == 3:
                print(f"\n✅ Todas as leituras enviadas com sucesso!")
            else:
                print(f"\n⚠️  {success_count}/3 leituras enviadas")
            
            # Aguardar próximo ciclo
            print(f"\n⏳ Aguardando {READING_INTERVAL} segundos...")
            time.sleep(READING_INTERVAL)
            
            # Re-autenticar a cada 100 leituras (prevenir expiração do token)
            if reading_count % 100 == 0:
                print("\n🔄 Renovando token de autenticação...")
                token = get_auth_token()
                if not token:
                    print("❌ Falha ao renovar token. Encerrando.")
                    break
    
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("⏹️  Simuladores parados pelo usuário")
        print(f"📊 Total de leituras geradas: {reading_count * 3}")
        print("=" * 60)
        sys.exit(0)
    
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
