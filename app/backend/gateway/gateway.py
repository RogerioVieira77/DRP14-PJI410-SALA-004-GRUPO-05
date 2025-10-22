"""
Gateway Principal
Sistema de Controle de Acesso - CEU Tres Pontes

Gateway que gerencia sensores e publica dados via MQTT.
"""

import time
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from threading import Thread, Event
import sys
import os

# Adicionar path dos sensores
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sensores.base_sensor import BaseSensor
from backend.gateway.mqtt_client import MQTTClient
from backend.gateway.message_formatter import MessageFormatter
from backend.gateway.config_loader import load_mqtt_config, get_topic


class Gateway:
    """
    Gateway que coleta dados dos sensores e publica via MQTT.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Inicializa o Gateway.
        
        Args:
            config: Dicionário de configuração. Se None, carrega do arquivo.
        """
        # Carregar configuração
        self.config = config or load_mqtt_config()
        self.gateway_id = self.config['gateway']['id']
        self.gateway_name = self.config['gateway']['name']
        self.publish_interval = self.config['gateway']['publish_interval']
        self.batch_size = self.config['gateway']['batch_size']
        
        # Componentes
        self.mqtt_client = MQTTClient(self.config, client_id=self.gateway_id)
        self.formatter = MessageFormatter(self.gateway_id)
        
        # Sensores gerenciados
        self.sensors: List[BaseSensor] = []
        self.sensor_readings_buffer = []
        
        # Controle de threads
        self.running = False
        self.publish_thread: Optional[Thread] = None
        self.monitor_thread: Optional[Thread] = None
        self.stop_event = Event()
        
        # Estatísticas
        self.stats = {
            'start_time': None,
            'readings_collected': 0,
            'readings_published': 0,
            'sensors_registered': 0,
            'errors': 0,
            'alerts_sent': 0
        }
        
        # Logging
        self.logger = self._setup_logging()
        
        self.logger.info(f"🏭 Gateway '{self.gateway_name}' inicializado")
    
    def _setup_logging(self) -> logging.Logger:
        """Configura o sistema de logging."""
        logger = logging.getLogger(f"Gateway.{self.gateway_id}")
        logger.setLevel(getattr(logging, self.config['logging']['level']))
        
        # Criar diretório de logs se não existir
        log_file = self.config['logging']['file']
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Handler para arquivo
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formato
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def register_sensor(self, sensor: BaseSensor):
        """
        Registra um sensor no gateway.
        
        Args:
            sensor: Instância do sensor a ser registrado
        """
        self.sensors.append(sensor)
        self.stats['sensors_registered'] += 1
        self.logger.info(f"📡 Sensor registrado: {sensor.serial_number} ({sensor.protocol}) - {sensor.location}")
    
    def register_sensors(self, sensors: List[BaseSensor]):
        """
        Registra múltiplos sensores de uma vez.
        
        Args:
            sensors: Lista de sensores
        """
        for sensor in sensors:
            self.register_sensor(sensor)
    
    def collect_readings(self):
        """Coleta leituras de todos os sensores registrados."""
        for sensor in self.sensors:
            try:
                # Simular detecção do sensor
                reading = sensor.simulate_detection()
                self.sensor_readings_buffer.append(reading)
                self.stats['readings_collected'] += 1
                
                if reading['activity'] == 1:
                    self.logger.debug(
                        f"🚶 Detecção em {sensor.location} "
                        f"({sensor.protocol} - {sensor.serial_number})"
                    )
                    
            except Exception as e:
                self.stats['errors'] += 1
                self.logger.error(f"❌ Erro ao coletar do sensor {sensor.serial_number}: {e}")
    
    def publish_readings(self):
        """Publica leituras no broker MQTT."""
        if not self.sensor_readings_buffer:
            return
        
        while self.sensor_readings_buffer:
            # Pegar leituras do buffer
            batch = self.sensor_readings_buffer[:self.batch_size]
            self.sensor_readings_buffer = self.sensor_readings_buffer[self.batch_size:]
            
            # Publicar cada leitura
            for reading in batch:
                try:
                    # Formatar mensagem
                    message = self.formatter.format_sensor_reading(reading)
                    
                    # Definir tópico
                    topic = get_topic(
                        self.config,
                        'sensors',
                        reading['serial_number']
                    )
                    
                    # Publicar
                    if self.mqtt_client.publish(topic, message):
                        self.stats['readings_published'] += 1
                    else:
                        self.stats['errors'] += 1
                        
                except Exception as e:
                    self.stats['errors'] += 1
                    self.logger.error(f"❌ Erro ao publicar leitura: {e}")
    
    def publish_status(self):
        """Publica status do gateway."""
        try:
            uptime = time.time() - self.stats['start_time'] if self.stats['start_time'] else 0
            
            status_data = {
                'sensors_connected': len(self.sensors),
                'sensors_active': sum(1 for s in self.sensors if hasattr(s, 'activity') and s.activity == 1),
                'uptime_seconds': int(uptime),
                'readings_collected': self.stats['readings_collected'],
                'readings_published': self.stats['readings_published'],
                'errors': self.stats['errors'],
                'buffer_size': len(self.sensor_readings_buffer)
            }
            
            message = self.formatter.format_status_message('online', status_data)
            topic = get_topic(self.config, 'status')
            
            self.mqtt_client.publish(topic, message, retain=True)
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao publicar status: {e}")
    
    def check_alerts(self):
        """Verifica e envia alertas se necessário."""
        try:
            # Verificar capacidade do parque
            total_detections = sum(s.total_detections for s in self.sensors)
            max_capacity = self.config['parque']['capacidade_maxima']
            current_percentage = (total_detections / max_capacity) * 100
            
            if current_percentage >= 80 and current_percentage < 90:
                self.send_alert(
                    'capacity',
                    'medium',
                    f'Capacidade do parque em {current_percentage:.1f}%',
                    {'current': total_detections, 'max': max_capacity}
                )
            elif current_percentage >= 90:
                self.send_alert(
                    'capacity',
                    'high',
                    f'Capacidade do parque CRÍTICA: {current_percentage:.1f}%',
                    {'current': total_detections, 'max': max_capacity}
                )
            
            # Verificar sensores offline (exemplo)
            # Aqui você pode adicionar lógica para detectar sensores inativos
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao verificar alertas: {e}")
    
    def send_alert(self, alert_type: str, severity: str, message: str, data: Dict = None):
        """
        Envia um alerta via MQTT.
        
        Args:
            alert_type: Tipo do alerta
            severity: Severidade ('low', 'medium', 'high', 'critical')
            message: Mensagem do alerta
            data: Dados adicionais
        """
        try:
            alert_message = self.formatter.format_alert_message(
                alert_type, severity, message, data
            )
            
            topic = get_topic(self.config, 'alerts')
            self.mqtt_client.publish(topic, alert_message)
            
            self.stats['alerts_sent'] += 1
            self.logger.warning(f"⚠️  Alerta enviado: {message}")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao enviar alerta: {e}")
    
    def _publish_loop(self):
        """Loop de publicação (roda em thread separada)."""
        self.logger.info("🔄 Loop de publicação iniciado")
        
        last_status_time = time.time()
        last_alert_check = time.time()
        
        while not self.stop_event.is_set():
            try:
                # Coletar leituras
                self.collect_readings()
                
                # Publicar leituras
                if self.mqtt_client.is_connected():
                    self.publish_readings()
                    
                    # Publicar status a cada 30 segundos
                    if time.time() - last_status_time >= 30:
                        self.publish_status()
                        last_status_time = time.time()
                    
                    # Verificar alertas a cada 60 segundos
                    if time.time() - last_alert_check >= 60:
                        self.check_alerts()
                        last_alert_check = time.time()
                
                # Aguardar intervalo configurado
                self.stop_event.wait(self.publish_interval)
                
            except Exception as e:
                self.logger.error(f"❌ Erro no loop de publicação: {e}")
                self.stats['errors'] += 1
                time.sleep(1)
    
    def start(self):
        """Inicia o gateway."""
        if self.running:
            self.logger.warning("⚠️  Gateway já está rodando")
            return
        
        self.logger.info(f"🚀 Iniciando Gateway '{self.gateway_name}'...")
        
        # Conectar ao MQTT
        if not self.mqtt_client.connect():
            self.logger.error("❌ Falha ao conectar ao broker MQTT")
            return
        
        # Publicar status inicial
        self.publish_status()
        
        # Iniciar loops
        self.running = True
        self.stats['start_time'] = time.time()
        self.stop_event.clear()
        
        self.publish_thread = Thread(target=self._publish_loop, daemon=True)
        self.publish_thread.start()
        
        self.logger.info(f"✅ Gateway '{self.gateway_name}' iniciado com sucesso!")
        self.logger.info(f"📊 Sensores registrados: {len(self.sensors)}")
        self.logger.info(f"📡 Broker: {self.config['broker']['host']}:{self.config['broker']['port']}")
    
    def stop(self):
        """Para o gateway."""
        if not self.running:
            return
        
        self.logger.info("🛑 Parando Gateway...")
        
        self.running = False
        self.stop_event.set()
        
        # Aguardar threads terminarem
        if self.publish_thread:
            self.publish_thread.join(timeout=5)
        
        # Publicar status offline
        try:
            message = self.formatter.format_status_message('offline', {})
            topic = get_topic(self.config, 'status')
            self.mqtt_client.publish(topic, message, retain=True)
        except:
            pass
        
        # Desconectar MQTT
        self.mqtt_client.disconnect()
        
        self.logger.info("👋 Gateway parado")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas do gateway.
        
        Returns:
            Dicionário com estatísticas
        """
        uptime = time.time() - self.stats['start_time'] if self.stats['start_time'] else 0
        
        return {
            'gateway_id': self.gateway_id,
            'gateway_name': self.gateway_name,
            'running': self.running,
            'uptime_seconds': int(uptime),
            'sensors_registered': self.stats['sensors_registered'],
            'readings_collected': self.stats['readings_collected'],
            'readings_published': self.stats['readings_published'],
            'alerts_sent': self.stats['alerts_sent'],
            'errors': self.stats['errors'],
            'buffer_size': len(self.sensor_readings_buffer),
            'mqtt_stats': self.mqtt_client.get_stats()
        }


if __name__ == "__main__":
    # Exemplo de uso do Gateway
    from sensores import LoRaSensor, ZigBeeSensor, SigfoxSensor, RFIDSensor
    
    print("=== GATEWAY CEU TRES PONTES ===\n")
    print("⚠️  Certifique-se de que o Mosquitto está rodando!\n")
    
    try:
        # Criar Gateway
        gateway = Gateway()
        
        # Criar e registrar sensores
        sensores = [
            LoRaSensor(location="Entrada Principal"),
            ZigBeeSensor(location="Saída Norte", node_type="Router"),
            SigfoxSensor(location="Portão Sul"),
            RFIDSensor(location="Catraca 1", frequency_type="HF")
        ]
        
        gateway.register_sensors(sensores)
        
        # Iniciar gateway
        gateway.start()
        
        print("\n✅ Gateway iniciado! Monitorando sensores...")
        print("Pressione Ctrl+C para parar\n")
        
        # Rodar por um tempo
        try:
            while True:
                time.sleep(10)
                
                # Mostrar estatísticas
                stats = gateway.get_stats()
                print(f"\n📊 Estatísticas:")
                print(f"  Uptime: {stats['uptime_seconds']}s")
                print(f"  Leituras coletadas: {stats['readings_collected']}")
                print(f"  Leituras publicadas: {stats['readings_published']}")
                print(f"  Alertas enviados: {stats['alerts_sent']}")
                print(f"  Erros: {stats['errors']}")
                
        except KeyboardInterrupt:
            print("\n\n🛑 Parando gateway...")
            gateway.stop()
            print("✅ Gateway parado com sucesso!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
