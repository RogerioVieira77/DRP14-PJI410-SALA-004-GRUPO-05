"""
Script de Teste dos Simuladores de Sensores
Sistema de Controle de Acesso - CEU Tres Pontes

Este script demonstra o funcionamento de todos os simuladores de sensores.
"""

import sys
import os
import time
import json
from datetime import datetime

# Adiciona o diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sensores import LoRaSensor, ZigBeeSensor, SigfoxSensor, RFIDSensor


def print_header(title: str):
    """Imprime um cabeçalho formatado."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_sensor_info(sensor):
    """Imprime informações detalhadas do sensor."""
    print(f"\n{sensor}")
    print("-" * 80)


def test_lora_sensor():
    """Testa o simulador LoRa."""
    print_header("TESTE: SENSOR LORA")
    
    # Cria sensor LoRa
    lora = LoRaSensor(location="Entrada Principal", spreading_factor=7)
    print_sensor_info(lora)
    
    # Simula algumas detecções
    print("\nSimulando 5 detecções:")
    for i in range(5):
        reading = lora.simulate_detection()
        if reading['activity'] == 1:
            print(f"  ✓ Detecção #{i+1}: Pessoa detectada!")
            print(f"    RSSI: {reading['rssi_dbm']} dBm | Battery: {reading['battery_level']}%")
        else:
            print(f"  - Leitura #{i+1}: Nenhuma atividade")
        time.sleep(0.5)
    
    # Testa mudança de SF
    print(f"\nAlcance atual (SF{lora.spreading_factor}): {lora.get_range_estimate()}")
    lora.set_spreading_factor(12)
    print(f"Alcance após ajuste (SF{lora.spreading_factor}): {lora.get_range_estimate()}")
    
    # Mostra status
    print("\nStatus do Sensor:")
    print(json.dumps(lora.get_status(), indent=2))
    
    return lora


def test_zigbee_sensor():
    """Testa o simulador ZigBee."""
    print_header("TESTE: SENSOR ZIGBEE")
    
    # Cria sensor ZigBee
    zigbee = ZigBeeSensor(location="Saída Lateral", node_type="Router")
    print_sensor_info(zigbee)
    
    # Simula algumas detecções
    print("\nSimulando 5 detecções:")
    for i in range(5):
        reading = zigbee.simulate_detection()
        if reading['activity'] == 1:
            print(f"  ✓ Detecção #{i+1}: Pessoa detectada!")
            print(f"    LQI: {reading['link_quality_lqi']} | Neighbors: {reading['neighbor_count']}")
        else:
            print(f"  - Leitura #{i+1}: Nenhuma atividade")
        time.sleep(0.5)
    
    # Mostra informações da rede mesh
    print("\nInformações da Rede Mesh:")
    mesh_info = zigbee.get_mesh_info()
    print(json.dumps(mesh_info, indent=2))
    
    # Descobre vizinhos
    print("\nVizinhos Descobertos:")
    neighbors = zigbee.discover_neighbors()
    for idx, neighbor in enumerate(neighbors[:3], 1):  # Mostra apenas 3
        print(f"  Vizinho {idx}: {neighbor['address']} - LQI: {neighbor['lqi']}")
    
    return zigbee


def test_sigfox_sensor():
    """Testa o simulador Sigfox."""
    print_header("TESTE: SENSOR SIGFOX")
    
    # Cria sensor Sigfox
    sigfox = SigfoxSensor(location="Portão de Emergência")
    print_sensor_info(sigfox)
    
    # Simula algumas detecções
    print("\nSimulando 5 detecções:")
    for i in range(5):
        if sigfox.can_send_message():
            reading = sigfox.simulate_detection()
            if reading['activity'] == 1:
                print(f"  ✓ Detecção #{i+1}: Pessoa detectada!")
                print(f"    Mensagens: {reading['messages_sent_today']}/{reading['message_limit']}")
                print(f"    Battery Life: {reading['battery_life_estimate_days']} dias")
            else:
                print(f"  - Leitura #{i+1}: Nenhuma atividade")
        else:
            print(f"  ✗ Limite de mensagens atingido!")
        time.sleep(0.5)
    
    # Mostra informações de cobertura
    print("\nInformações de Cobertura:")
    coverage = sigfox.get_coverage_info()
    print(json.dumps(coverage, indent=2))
    
    return sigfox


def test_rfid_sensor():
    """Testa o simulador RFID."""
    print_header("TESTE: SENSOR RFID")
    
    # Cria sensor RFID
    rfid = RFIDSensor(location="Catraca Principal", frequency_type="HF", tag_type="Passive")
    print_sensor_info(rfid)
    
    # Simula leitura de tags
    print("\nSimulando leitura de 5 tags:")
    for i in range(5):
        tag_data = rfid.read_tag()
        if tag_data['success']:
            print(f"  ✓ Tag #{i+1} lida com sucesso!")
            print(f"    ID: {tag_data['tag_id'][:16]}... | RSSI: {tag_data['rssi']} dBm")
        else:
            print(f"  ✗ Falha ao ler tag #{i+1}")
        time.sleep(0.5)
    
    # Mostra informações do leitor
    print("\nInformações do Leitor:")
    reader_info = rfid.get_reader_info()
    print(json.dumps(reader_info, indent=2))
    
    # Mostra tags únicas detectadas
    print(f"\nTotal de tags únicas detectadas: {rfid.get_unique_tags_count()}")
    
    return rfid


def test_continuous_monitoring(sensors: dict, duration: int = 10):
    """Simula monitoramento contínuo de todos os sensores."""
    print_header(f"MONITORAMENTO CONTÍNUO - {duration} segundos")
    
    print("\nMonitorando todos os sensores simultaneamente...")
    print("(Pressione Ctrl+C para interromper)\n")
    
    start_time = time.time()
    try:
        while (time.time() - start_time) < duration:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Leitura dos sensores:")
            
            for name, sensor in sensors.items():
                reading = sensor.simulate_detection()
                if reading['activity'] == 1:
                    print(f"  🚶 {name}: PESSOA DETECTADA em {sensor.location}")
                else:
                    print(f"  ⚪ {name}: Nenhuma atividade em {sensor.location}")
            
            time.sleep(2)
    
    except KeyboardInterrupt:
        print("\n\nMonitoramento interrompido pelo usuário.")
    
    # Mostra resumo
    print_header("RESUMO DO MONITORAMENTO")
    total_detections = 0
    for name, sensor in sensors.items():
        detections = sensor.total_detections
        total_detections += detections
        print(f"  {name} ({sensor.location}): {detections} detecções")
    
    print(f"\n  TOTAL DE PESSOAS DETECTADAS: {total_detections}")


def generate_report(sensors: dict):
    """Gera um relatório JSON com os dados de todos os sensores."""
    print_header("GERANDO RELATÓRIO")
    
    report = {
        'parque': 'CEU Tres Pontes',
        'timestamp': datetime.now().isoformat(),
        'sensores': {}
    }
    
    for name, sensor in sensors.items():
        report['sensores'][name] = {
            'status': sensor.get_status(),
            'history': sensor.get_history(limit=5)
        }
    
    # Salva relatório em arquivo
    report_file = os.path.join(os.path.dirname(__file__), 'relatorio_sensores.json')
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Relatório salvo em: {report_file}")
    return report_file


def main():
    """Função principal de teste."""
    print_header("SISTEMA DE CONTROLE DE ACESSO - CEU TRES PONTES")
    print("\nFASE 1: TESTE DOS SIMULADORES DE SENSORES")
    print("\nProtocolos implementados:")
    print("  • LoRa (Long Range)")
    print("  • ZigBee (Mesh Network)")
    print("  • Sigfox (LPWAN)")
    print("  • RFID (Radio Frequency Identification)")
    
    input("\nPressione ENTER para iniciar os testes...")
    
    # Testa cada sensor individualmente
    lora = test_lora_sensor()
    input("\nPressione ENTER para continuar...")
    
    zigbee = test_zigbee_sensor()
    input("\nPressione ENTER para continuar...")
    
    sigfox = test_sigfox_sensor()
    input("\nPressione ENTER para continuar...")
    
    rfid = test_rfid_sensor()
    input("\nPressione ENTER para continuar...")
    
    # Testa monitoramento contínuo
    sensors = {
        'LoRa': lora,
        'ZigBee': zigbee,
        'Sigfox': sigfox,
        'RFID': rfid
    }
    
    test_continuous_monitoring(sensors, duration=10)
    
    # Gera relatório final
    generate_report(sensors)
    
    print_header("TESTES CONCLUÍDOS COM SUCESSO!")
    print("\n✓ Todos os simuladores estão funcionando corretamente.")
    print("✓ Fase 1 do projeto concluída.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTeste interrompido pelo usuário.")
    except Exception as e:
        print(f"\n✗ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()
