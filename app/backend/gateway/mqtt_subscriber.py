"""
MQTT Subscriber
Sistema de Controle de Acesso - CEU Tres Pontes

Subscriber para receber e processar mensagens do broker MQTT.
"""

import logging
import time
import json
from typing import Dict, Any, Callable, Optional
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.gateway.mqtt_client import MQTTClient
from backend.gateway.config_loader import load_mqtt_config, get_topic


class MQTTSubscriber:
    """
    Subscriber MQTT para receber mensagens dos sensores.
    """
    
    def __init__(self, config: Dict[str, Any] = None, client_id: str = "subscriber_001"):
        """
        Inicializa o subscriber.
        
        Args:
            config: Dicionário de configuração
            client_id: ID do cliente subscriber
        """
        self.config = config or load_mqtt_config()
        self.client_id = client_id
        
        # Cliente MQTT
        self.mqtt_client = MQTTClient(self.config, client_id=self.client_id)
        
        # Callbacks personalizados
        self.custom_callbacks = {}
        
        # Estatísticas
        self.stats = {
            'start_time': None,
            'messages_received': 0,
            'sensor_readings': 0,
            'status_updates': 0,
            'alerts_received': 0,
            'errors': 0
        }
        
        # Armazenamento temporário de dados
        self.sensor_data_cache = []
        self.max_cache_size = 1000
        
        # Logging
        self.logger = logging.getLogger(f"Subscriber.{self.client_id}")
        self.logger.setLevel(logging.INFO)
        
        # Handler console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def _on_sensor_message(self, topic: str, message: str):
        """
        Processa mensagem de sensor.
        
        Args:
            topic: Tópico MQTT
            message: Mensagem JSON
        """
        try:
            data = json.loads(message)
            self.stats['sensor_readings'] += 1
            
            # Adicionar ao cache
            self.sensor_data_cache.append(data)
            if len(self.sensor_data_cache) > self.max_cache_size:
                self.sensor_data_cache.pop(0)
            
            # Log se houver atividade
            if data.get('data', {}).get('activity') == 1:
                sensor_info = data.get('sensor', {})
                self.logger.info(
                    f"🚶 DETECÇÃO: {sensor_info.get('location')} "
                    f"[{sensor_info.get('protocol')} - {sensor_info.get('serial_number')}]"
                )
            
            # Callback personalizado se existir
            if 'sensor' in self.custom_callbacks:
                self.custom_callbacks['sensor'](data)
                
        except json.JSONDecodeError as e:
            self.stats['errors'] += 1
            self.logger.error(f"❌ Erro ao decodificar mensagem de sensor: {e}")
        except Exception as e:
            self.stats['errors'] += 1
            self.logger.error(f"❌ Erro ao processar mensagem de sensor: {e}")
    
    def _on_status_message(self, topic: str, message: str):
        """
        Processa mensagem de status do gateway.
        
        Args:
            topic: Tópico MQTT
            message: Mensagem JSON
        """
        try:
            data = json.loads(message)
            self.stats['status_updates'] += 1
            
            status = data.get('status')
            details = data.get('details', {})
            
            if status == 'online':
                self.logger.info(
                    f"✅ Gateway ONLINE - Sensores: {details.get('sensors_connected', 0)}"
                )
            elif status == 'offline':
                self.logger.warning("⚠️  Gateway OFFLINE")
            
            # Callback personalizado se existir
            if 'status' in self.custom_callbacks:
                self.custom_callbacks['status'](data)
                
        except json.JSONDecodeError as e:
            self.stats['errors'] += 1
            self.logger.error(f"❌ Erro ao decodificar mensagem de status: {e}")
        except Exception as e:
            self.stats['errors'] += 1
            self.logger.error(f"❌ Erro ao processar mensagem de status: {e}")
    
    def _on_alert_message(self, topic: str, message: str):
        """
        Processa mensagem de alerta.
        
        Args:
            topic: Tópico MQTT
            message: Mensagem JSON
        """
        try:
            data = json.loads(message)
            self.stats['alerts_received'] += 1
            
            alert_type = data.get('type')
            severity = data.get('severity')
            alert_message = data.get('message')
            
            # Emoji baseado na severidade
            emoji = {
                'low': '💡',
                'medium': '⚠️ ',
                'high': '🚨',
                'critical': '🔴'
            }.get(severity, '📢')
            
            self.logger.warning(f"{emoji} ALERTA [{severity.upper()}]: {alert_message}")
            
            # Callback personalizado se existir
            if 'alert' in self.custom_callbacks:
                self.custom_callbacks['alert'](data)
                
        except json.JSONDecodeError as e:
            self.stats['errors'] += 1
            self.logger.error(f"❌ Erro ao decodificar mensagem de alerta: {e}")
        except Exception as e:
            self.stats['errors'] += 1
            self.logger.error(f"❌ Erro ao processar mensagem de alerta: {e}")
    
    def set_callback(self, message_type: str, callback: Callable):
        """
        Define callback personalizado para tipo de mensagem.
        
        Args:
            message_type: Tipo da mensagem ('sensor', 'status', 'alert')
            callback: Função callback(data)
        """
        self.custom_callbacks[message_type] = callback
        self.logger.info(f"✅ Callback registrado para: {message_type}")
    
    def start(self):
        """Inicia o subscriber e conecta ao broker."""
        self.logger.info(f"🚀 Iniciando Subscriber '{self.client_id}'...")
        
        # Conectar ao broker
        if not self.mqtt_client.connect():
            self.logger.error("❌ Falha ao conectar ao broker MQTT")
            return False
        
        # Subscrever aos tópicos
        # Sensores (wildcard para todos os sensores)
        sensor_topic = f"{self.config['topics']['prefix']}/{self.config['topics']['sensors']}/#"
        self.mqtt_client.subscribe(sensor_topic, self._on_sensor_message)
        
        # Status
        status_topic = get_topic(self.config, 'status')
        self.mqtt_client.subscribe(status_topic, self._on_status_message)
        
        # Alertas
        alert_topic = get_topic(self.config, 'alerts')
        self.mqtt_client.subscribe(alert_topic, self._on_alert_message)
        
        self.stats['start_time'] = time.time()
        
        self.logger.info("✅ Subscriber iniciado com sucesso!")
        self.logger.info(f"📡 Broker: {self.config['broker']['host']}:{self.config['broker']['port']}")
        self.logger.info(f"📥 Aguardando mensagens...")
        
        return True
    
    def stop(self):
        """Para o subscriber."""
        self.logger.info("🛑 Parando Subscriber...")
        self.mqtt_client.disconnect()
        self.logger.info("👋 Subscriber parado")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas do subscriber.
        
        Returns:
            Dicionário com estatísticas
        """
        uptime = time.time() - self.stats['start_time'] if self.stats['start_time'] else 0
        
        return {
            'client_id': self.client_id,
            'uptime_seconds': int(uptime),
            'messages_received': self.stats['messages_received'],
            'sensor_readings': self.stats['sensor_readings'],
            'status_updates': self.stats['status_updates'],
            'alerts_received': self.stats['alerts_received'],
            'errors': self.stats['errors'],
            'cache_size': len(self.sensor_data_cache),
            'mqtt_stats': self.mqtt_client.get_stats()
        }
    
    def get_recent_readings(self, limit: int = 10) -> list:
        """
        Retorna as leituras mais recentes do cache.
        
        Args:
            limit: Número máximo de leituras a retornar
        
        Returns:
            Lista das leituras mais recentes
        """
        return self.sensor_data_cache[-limit:]
    
    def get_readings_by_sensor(self, serial_number: str) -> list:
        """
        Retorna leituras de um sensor específico.
        
        Args:
            serial_number: Número de série do sensor
        
        Returns:
            Lista de leituras do sensor
        """
        return [
            reading for reading in self.sensor_data_cache
            if reading.get('sensor', {}).get('serial_number') == serial_number
        ]
    
    def export_data(self, filename: str):
        """
        Exporta dados do cache para arquivo JSON.
        
        Args:
            filename: Nome do arquivo para exportar
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'export_time': datetime.now().isoformat(),
                    'stats': self.get_stats(),
                    'readings': self.sensor_data_cache
                }, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"💾 Dados exportados para: {filename}")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao exportar dados: {e}")


if __name__ == "__main__":
    print("=== MQTT SUBSCRIBER - CEU TRES PONTES ===\n")
    print("⚠️  Certifique-se de que o Mosquitto e o Gateway estão rodando!\n")
    
    try:
        # Criar subscriber
        subscriber = MQTTSubscriber(client_id="test_subscriber")
        
        # Definir callbacks personalizados (opcional)
        def on_detection(data):
            """Callback personalizado para detecções."""
            if data.get('data', {}).get('activity') == 1:
                print(f"  💡 Callback: Nova pessoa detectada!")
        
        def on_alert(data):
            """Callback personalizado para alertas."""
            print(f"  🔔 Callback: Alerta processado - {data.get('type')}")
        
        subscriber.set_callback('sensor', on_detection)
        subscriber.set_callback('alert', on_alert)
        
        # Iniciar subscriber
        if subscriber.start():
            print("\n✅ Subscriber rodando! Aguardando mensagens...")
            print("Pressione Ctrl+C para parar\n")
            
            try:
                while True:
                    time.sleep(30)
                    
                    # Mostrar estatísticas periodicamente
                    stats = subscriber.get_stats()
                    print(f"\n📊 Estatísticas do Subscriber:")
                    print(f"  Uptime: {stats['uptime_seconds']}s")
                    print(f"  Leituras recebidas: {stats['sensor_readings']}")
                    print(f"  Status updates: {stats['status_updates']}")
                    print(f"  Alertas: {stats['alerts_received']}")
                    print(f"  Cache: {stats['cache_size']} mensagens")
                    
            except KeyboardInterrupt:
                print("\n\n🛑 Parando subscriber...")
                
                # Exportar dados antes de parar
                export_file = f"subscriber_data_{int(time.time())}.json"
                subscriber.export_data(export_file)
                
                subscriber.stop()
                print("✅ Subscriber parado com sucesso!")
        else:
            print("❌ Não foi possível iniciar o subscriber")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
