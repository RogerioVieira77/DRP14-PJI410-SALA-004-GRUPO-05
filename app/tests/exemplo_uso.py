"""
Exemplo Simples de Uso dos Simuladores
Sistema de Controle de Acesso - CEU Tres Pontes

Este script demonstra o uso básico de cada tipo de sensor.
"""

import sys
import os

# Adiciona o diretório sensores ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sensores import LoRaSensor, ZigBeeSensor, SigfoxSensor, RFIDSensor


def exemplo_lora():
    """Exemplo básico do sensor LoRa"""
    print("\n=== SENSOR LORA ===")
    
    # Criar sensor
    sensor = LoRaSensor(location="Entrada Principal", spreading_factor=7)
    print(f"Sensor criado: {sensor.serial_number}")
    
    # Simular detecção
    leitura = sensor.simulate_detection(force_detection=True)
    
    print(f"Pessoa detectada: {leitura['activity'] == 1}")
    print(f"Timestamp: {leitura['timestamp']}")
    print(f"RSSI: {leitura['rssi_dbm']} dBm")
    print(f"Bateria: {leitura['battery_level']}%")
    print(f"Alcance estimado: {sensor.get_range_estimate()}")


def exemplo_zigbee():
    """Exemplo básico do sensor ZigBee"""
    print("\n=== SENSOR ZIGBEE ===")
    
    # Criar sensor
    sensor = ZigBeeSensor(location="Saída Lateral", node_type="Router")
    print(f"Sensor criado: {sensor.serial_number}")
    
    # Simular detecção
    leitura = sensor.simulate_detection(force_detection=True)
    
    print(f"Pessoa detectada: {leitura['activity'] == 1}")
    print(f"Tipo de nó: {leitura['node_type']}")
    print(f"PAN ID: {leitura['pan_id']}")
    print(f"Qualidade do link (LQI): {leitura['link_quality_lqi']}")
    print(f"Vizinhos na rede: {leitura['neighbor_count']}")


def exemplo_sigfox():
    """Exemplo básico do sensor Sigfox"""
    print("\n=== SENSOR SIGFOX ===")
    
    # Criar sensor
    sensor = SigfoxSensor(location="Portão de Emergência")
    print(f"Sensor criado: {sensor.serial_number}")
    print(f"Device ID: {sensor.device_id}")
    
    # Simular detecção
    leitura = sensor.simulate_detection(force_detection=True)
    
    print(f"Pessoa detectada: {leitura['activity'] == 1}")
    print(f"Mensagens enviadas hoje: {leitura['messages_sent_today']}/{leitura['message_limit']}")
    print(f"Bateria: {leitura['battery_level']:.2f}%")
    print(f"Vida útil estimada: {leitura['battery_life_estimate_days']} dias")


def exemplo_rfid():
    """Exemplo básico do sensor RFID"""
    print("\n=== SENSOR RFID ===")
    
    # Criar sensor
    sensor = RFIDSensor(location="Catraca Principal", frequency_type="HF")
    print(f"Sensor criado: {sensor.serial_number}")
    
    # Simular leitura de tag
    tag = sensor.read_tag()
    
    if tag['success']:
        print(f"Tag lida com sucesso!")
        print(f"Tag ID: {tag['tag_id']}")
        print(f"RSSI: {tag['rssi']} dBm")
        print(f"Tipo: {tag['tag_type']}")
        print(f"Alcance de leitura: {sensor.read_range} metros")


def exemplo_monitoramento():
    """Exemplo de monitoramento de múltiplos sensores"""
    print("\n=== MONITORAMENTO DE MÚLTIPLOS SENSORES ===")
    
    # Criar array de sensores
    sensores = [
        LoRaSensor(location="Entrada Principal"),
        ZigBeeSensor(location="Saída Norte"),
        SigfoxSensor(location="Portão Sul"),
        RFIDSensor(location="Catraca 1")
    ]
    
    print(f"\nTotal de sensores ativos: {len(sensores)}")
    print("\nRealizando leituras simultâneas...\n")
    
    total_deteccoes = 0
    
    for sensor in sensores:
        leitura = sensor.simulate_detection()
        status = "🚶 DETECTADO" if leitura['activity'] == 1 else "⚪ Sem atividade"
        print(f"{sensor.protocol:8} [{sensor.location:20}]: {status}")
        
        if leitura['activity'] == 1:
            total_deteccoes += 1
    
    print(f"\nTotal de pessoas detectadas: {total_deteccoes}")


if __name__ == "__main__":
    print("=" * 70)
    print("  SISTEMA DE CONTROLE DE ACESSO - CEU TRES PONTES")
    print("  Exemplos de Uso dos Simuladores")
    print("=" * 70)
    
    # Executar exemplos
    exemplo_lora()
    exemplo_zigbee()
    exemplo_sigfox()
    exemplo_rfid()
    exemplo_monitoramento()
    
    print("\n" + "=" * 70)
    print("  ✓ Exemplos executados com sucesso!")
    print("=" * 70 + "\n")
