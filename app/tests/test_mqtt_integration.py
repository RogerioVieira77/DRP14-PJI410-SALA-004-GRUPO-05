"""
Teste de Integração MQTT - Fase 2
Sistema de Controle de Acesso - CEU Tres Pontes

Testa a comunicação completa:
Sensores → Gateway → MQTT Broker → Subscriber
"""

import sys
import os
import time
import threading

# Adicionar paths
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sensores import LoRaSensor, ZigBeeSensor, SigfoxSensor, RFIDSensor
from backend.gateway.gateway import Gateway
from backend.gateway.mqtt_subscriber import MQTTSubscriber


def print_header(title: str):
    """Imprime cabeçalho formatado."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def test_phase2_integration(duration: int = 60):
    """
    Teste completo de integração da Fase 2.
    
    Args:
        duration: Duração do teste em segundos
    """
    print_header("TESTE DE INTEGRAÇÃO - FASE 2: GATEWAY E MQTT")
    
    print("\n📋 Este teste vai:")
    print("  1. Criar sensores simulados")
    print("  2. Iniciar Gateway")
    print("  3. Iniciar Subscriber")
    print("  4. Coletar e publicar dados via MQTT")
    print("  5. Receber e processar mensagens")
    print(f"  6. Rodar por {duration} segundos")
    
    print("\n⚠️  IMPORTANTE: Certifique-se de que o Mosquitto está rodando!")
    print("   Windows: net start mosquitto")
    print("   Linux: sudo systemctl start mosquitto")
    
    input("\nPressione ENTER para começar o teste...")
    
    # === 1. CRIAR SENSORES ===
    print_header("1. CRIANDO SENSORES")
    
    sensores = [
        LoRaSensor(location="Entrada Principal", spreading_factor=7),
        ZigBeeSensor(location="Saída Norte", node_type="Router"),
        SigfoxSensor(location="Portão Sul"),
        RFIDSensor(location="Catraca 1", frequency_type="HF"),
        LoRaSensor(location="Entrada Lateral", spreading_factor=9),
        ZigBeeSensor(location="Saída Leste", node_type="End Device")
    ]
    
    print(f"\n✅ {len(sensores)} sensores criados:")
    for sensor in sensores:
        print(f"  • {sensor.protocol:8} - {sensor.location} [{sensor.serial_number}]")
    
    # === 2. CRIAR E INICIAR GATEWAY ===
    print_header("2. INICIANDO GATEWAY")
    
    try:
        gateway = Gateway()
        gateway.register_sensors(sensores)
        gateway.start()
        
        if not gateway.running:
            print("❌ Gateway não iniciou corretamente")
            print("   Verifique se o Mosquitto está rodando!")
            return
        
        print("✅ Gateway iniciado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao iniciar Gateway: {e}")
        return
    
    # === 3. CRIAR E INICIAR SUBSCRIBER ===
    print_header("3. INICIANDO SUBSCRIBER")
    
    # Contadores para callbacks personalizados
    detections_count = [0]  # Usar lista para modificar no callback
    
    def on_detection_callback(data):
        """Callback personalizado para detecções."""
        if data.get('data', {}).get('activity') == 1:
            detections_count[0] += 1
    
    try:
        subscriber = MQTTSubscriber(client_id="test_integration_subscriber")
        subscriber.set_callback('sensor', on_detection_callback)
        
        if not subscriber.start():
            print("❌ Subscriber não iniciou corretamente")
            gateway.stop()
            return
        
        print("✅ Subscriber iniciado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao iniciar Subscriber: {e}")
        gateway.stop()
        return
    
    # === 4. MONITORAMENTO ===
    print_header("4. MONITORAMENTO EM TEMPO REAL")
    
    print(f"\n🔄 Sistema rodando por {duration} segundos...")
    print("📊 Estatísticas serão mostradas a cada 10 segundos\n")
    
    start_time = time.time()
    last_stats_time = start_time
    
    try:
        while time.time() - start_time < duration:
            time.sleep(1)
            
            # Mostrar estatísticas a cada 10 segundos
            if time.time() - last_stats_time >= 10:
                elapsed = int(time.time() - start_time)
                remaining = duration - elapsed
                
                print(f"\n⏱️  Tempo decorrido: {elapsed}s | Restante: {remaining}s")
                print("-" * 80)
                
                # Estatísticas do Gateway
                gateway_stats = gateway.get_stats()
                print(f"\n📤 GATEWAY:")
                print(f"  Leituras coletadas: {gateway_stats['readings_collected']}")
                print(f"  Leituras publicadas: {gateway_stats['readings_published']}")
                print(f"  Alertas enviados: {gateway_stats['alerts_sent']}")
                print(f"  Erros: {gateway_stats['errors']}")
                print(f"  Buffer: {gateway_stats['buffer_size']} mensagens")
                
                # Estatísticas do Subscriber
                subscriber_stats = subscriber.get_stats()
                print(f"\n📥 SUBSCRIBER:")
                print(f"  Leituras recebidas: {subscriber_stats['sensor_readings']}")
                print(f"  Status updates: {subscriber_stats['status_updates']}")
                print(f"  Alertas recebidos: {subscriber_stats['alerts_received']}")
                print(f"  Cache: {subscriber_stats['cache_size']} mensagens")
                print(f"  Detecções processadas: {detections_count[0]}")
                
                # Total de detecções nos sensores
                total_detections = sum(s.total_detections for s in sensores)
                print(f"\n🚶 DETECÇÕES TOTAIS: {total_detections}")
                
                last_stats_time = time.time()
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Teste interrompido pelo usuário")
    
    # === 5. RESULTADOS FINAIS ===
    print_header("5. RESULTADOS FINAIS")
    
    # Estatísticas finais
    gateway_stats = gateway.get_stats()
    subscriber_stats = subscriber.get_stats()
    
    print("\n📊 ESTATÍSTICAS FINAIS:\n")
    
    print("GATEWAY:")
    print(f"  ✓ Sensores registrados: {gateway_stats['sensors_registered']}")
    print(f"  ✓ Leituras coletadas: {gateway_stats['readings_collected']}")
    print(f"  ✓ Leituras publicadas: {gateway_stats['readings_published']}")
    print(f"  ✓ Alertas enviados: {gateway_stats['alerts_sent']}")
    print(f"  ✓ Uptime: {gateway_stats['uptime_seconds']}s")
    print(f"  ✗ Erros: {gateway_stats['errors']}")
    
    print("\nSUBSCRIBER:")
    print(f"  ✓ Leituras recebidas: {subscriber_stats['sensor_readings']}")
    print(f"  ✓ Status updates: {subscriber_stats['status_updates']}")
    print(f"  ✓ Alertas recebidos: {subscriber_stats['alerts_received']}")
    print(f"  ✓ Cache final: {subscriber_stats['cache_size']} mensagens")
    print(f"  ✗ Erros: {subscriber_stats['errors']}")
    
    print("\nSENSORES:")
    total_detections = sum(s.total_detections for s in sensores)
    print(f"  🚶 Total de detecções: {total_detections}")
    for sensor in sensores:
        print(f"    • {sensor.protocol} [{sensor.location}]: {sensor.total_detections} detecções")
    
    # Validação
    print("\n" + "=" * 80)
    print("VALIDAÇÃO DO TESTE:")
    
    success = True
    
    if gateway_stats['readings_published'] == 0:
        print("  ❌ Nenhuma leitura foi publicada")
        success = False
    else:
        print(f"  ✅ {gateway_stats['readings_published']} leituras publicadas")
    
    if subscriber_stats['sensor_readings'] == 0:
        print("  ❌ Nenhuma leitura foi recebida")
        success = False
    else:
        print(f"  ✅ {subscriber_stats['sensor_readings']} leituras recebidas")
    
    # Verificar se publicadas ≈ recebidas (pode haver diferença mínima)
    diff = abs(gateway_stats['readings_published'] - subscriber_stats['sensor_readings'])
    if diff > 5:  # Tolerância de 5 mensagens
        print(f"  ⚠️  Diferença entre publicadas e recebidas: {diff}")
    else:
        print(f"  ✅ Publicadas ≈ Recebidas (diferença: {diff})")
    
    if gateway_stats['errors'] > 0 or subscriber_stats['errors'] > 0:
        print(f"  ⚠️  Erros detectados (Gateway: {gateway_stats['errors']}, Subscriber: {subscriber_stats['errors']})")
    else:
        print("  ✅ Sem erros")
    
    print("=" * 80)
    
    if success:
        print("\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
        print("✅ Sistema MQTT funcionando corretamente!")
    else:
        print("\n⚠️  TESTE CONCLUÍDO COM PROBLEMAS")
        print("❌ Verifique os erros acima")
    
    # === 6. EXPORTAR DADOS ===
    print_header("6. EXPORTANDO DADOS")
    
    export_file = f"mqtt_test_results_{int(time.time())}.json"
    try:
        subscriber.export_data(export_file)
        print(f"\n💾 Dados exportados para: {export_file}")
    except Exception as e:
        print(f"\n❌ Erro ao exportar dados: {e}")
    
    # === 7. LIMPAR ===
    print_header("7. FINALIZANDO")
    
    print("\n🛑 Parando Gateway...")
    gateway.stop()
    
    print("🛑 Parando Subscriber...")
    subscriber.stop()
    
    time.sleep(2)
    
    print("\n✅ Sistema finalizado!\n")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Teste de Integração MQTT - Fase 2')
    parser.add_argument(
        '--duration',
        type=int,
        default=60,
        help='Duração do teste em segundos (padrão: 60)'
    )
    
    args = parser.parse_args()
    
    try:
        test_phase2_integration(duration=args.duration)
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
