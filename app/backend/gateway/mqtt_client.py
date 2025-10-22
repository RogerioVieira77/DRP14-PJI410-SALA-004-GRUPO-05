"""
Cliente MQTT
Sistema de Controle de Acesso - CEU Tres Pontes

Cliente para publicação e subscrição de mensagens via MQTT.
"""

import paho.mqtt.client as mqtt
import logging
import time
from typing import Callable, Dict, Any, Optional
from threading import Lock


class MQTTClient:
    """
    Cliente MQTT para comunicação com o broker Mosquitto.
    """
    
    def __init__(self, config: Dict[str, Any], client_id: str = None):
        """
        Inicializa o cliente MQTT.
        
        Args:
            config: Dicionário com configurações MQTT
            client_id: ID do cliente (opcional)
        """
        self.config = config
        self.client_id = client_id or config['gateway']['id']
        self.broker = config['broker']
        self.qos = config['qos']
        
        # Criar cliente MQTT
        self.client = mqtt.Client(client_id=self.client_id)
        
        # Configurar autenticação se fornecida
        if self.broker.get('username') and self.broker.get('password'):
            self.client.username_pw_set(
                self.broker['username'],
                self.broker['password']
            )
        
        # Callbacks
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_publish = self._on_publish
        self.client.on_message = self._on_message
        
        # Estado
        self.connected = False
        self.subscribed_topics = []
        self.message_callbacks = {}
        self.lock = Lock()
        
        # Estatísticas
        self.stats = {
            'messages_published': 0,
            'messages_received': 0,
            'connection_attempts': 0,
            'connection_failures': 0
        }
        
        # Logging
        self.logger = logging.getLogger(__name__)
    
    def _on_connect(self, client, userdata, flags, rc):
        """Callback quando conectado ao broker."""
        if rc == 0:
            self.connected = True
            self.logger.info(f"✅ Conectado ao broker MQTT: {self.broker['host']}:{self.broker['port']}")
            
            # Re-subscrever tópicos após reconexão
            for topic in self.subscribed_topics:
                self.client.subscribe(topic, self.qos)
                self.logger.info(f"📥 Re-subscrito ao tópico: {topic}")
        else:
            self.connected = False
            self.stats['connection_failures'] += 1
            error_messages = {
                1: "Protocolo incorreto",
                2: "Client ID inválido",
                3: "Servidor indisponível",
                4: "Usuário/senha incorretos",
                5: "Não autorizado"
            }
            error_msg = error_messages.get(rc, f"Erro desconhecido: {rc}")
            self.logger.error(f"❌ Falha na conexão: {error_msg}")
    
    def _on_disconnect(self, client, userdata, rc):
        """Callback quando desconectado do broker."""
        self.connected = False
        if rc != 0:
            self.logger.warning(f"⚠️  Desconectado inesperadamente. Código: {rc}")
        else:
            self.logger.info("🔌 Desconectado do broker MQTT")
    
    def _on_publish(self, client, userdata, mid):
        """Callback quando mensagem é publicada."""
        with self.lock:
            self.stats['messages_published'] += 1
        self.logger.debug(f"📤 Mensagem publicada (MID: {mid})")
    
    def _on_message(self, client, userdata, msg):
        """Callback quando mensagem é recebida."""
        with self.lock:
            self.stats['messages_received'] += 1
        
        self.logger.debug(f"📨 Mensagem recebida no tópico: {msg.topic}")
        
        # Executar callback específico do tópico se existir
        if msg.topic in self.message_callbacks:
            try:
                self.message_callbacks[msg.topic](msg.topic, msg.payload.decode('utf-8'))
            except Exception as e:
                self.logger.error(f"❌ Erro ao processar mensagem: {e}")
    
    def connect(self, retry_attempts: int = 3, retry_delay: int = 5) -> bool:
        """
        Conecta ao broker MQTT.
        
        Args:
            retry_attempts: Número de tentativas de reconexão
            retry_delay: Delay entre tentativas (segundos)
        
        Returns:
            True se conectado com sucesso
        """
        for attempt in range(1, retry_attempts + 1):
            try:
                self.stats['connection_attempts'] += 1
                self.logger.info(f"🔄 Tentativa {attempt}/{retry_attempts} de conexão ao broker...")
                
                self.client.connect(
                    self.broker['host'],
                    self.broker['port'],
                    self.broker['keepalive']
                )
                
                # Iniciar loop em thread separada
                self.client.loop_start()
                
                # Aguardar conexão
                timeout = 10
                elapsed = 0
                while not self.connected and elapsed < timeout:
                    time.sleep(0.5)
                    elapsed += 0.5
                
                if self.connected:
                    return True
                    
            except Exception as e:
                self.logger.error(f"❌ Erro na tentativa {attempt}: {e}")
                if attempt < retry_attempts:
                    self.logger.info(f"⏳ Aguardando {retry_delay}s antes de tentar novamente...")
                    time.sleep(retry_delay)
        
        return False
    
    def disconnect(self):
        """Desconecta do broker MQTT."""
        if self.connected:
            self.client.loop_stop()
            self.client.disconnect()
            self.logger.info("👋 Desconectando do broker...")
    
    def publish(self, topic: str, message: str, retain: bool = False) -> bool:
        """
        Publica uma mensagem no tópico especificado.
        
        Args:
            topic: Tópico MQTT
            message: Mensagem (string JSON)
            retain: Se a mensagem deve ser retida pelo broker
        
        Returns:
            True se publicado com sucesso
        """
        if not self.connected:
            self.logger.error("❌ Não conectado ao broker. Não é possível publicar.")
            return False
        
        try:
            result = self.client.publish(topic, message, qos=self.qos, retain=retain)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                self.logger.debug(f"✅ Publicado em {topic}")
                return True
            else:
                self.logger.error(f"❌ Erro ao publicar: {result.rc}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Exceção ao publicar: {e}")
            return False
    
    def subscribe(self, topic: str, callback: Callable = None):
        """
        Subscreve a um tópico MQTT.
        
        Args:
            topic: Tópico para subscrever
            callback: Função callback(topic, message) para processar mensagens
        """
        if not self.connected:
            self.logger.warning("⚠️  Não conectado. Subscrevendo após conexão...")
        
        self.client.subscribe(topic, self.qos)
        self.subscribed_topics.append(topic)
        
        if callback:
            self.message_callbacks[topic] = callback
        
        self.logger.info(f"📥 Subscrito ao tópico: {topic}")
    
    def unsubscribe(self, topic: str):
        """
        Cancela subscrição de um tópico.
        
        Args:
            topic: Tópico para cancelar subscrição
        """
        self.client.unsubscribe(topic)
        if topic in self.subscribed_topics:
            self.subscribed_topics.remove(topic)
        if topic in self.message_callbacks:
            del self.message_callbacks[topic]
        
        self.logger.info(f"📤 Cancelada subscrição do tópico: {topic}")
    
    def is_connected(self) -> bool:
        """Retorna se está conectado ao broker."""
        return self.connected
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas do cliente.
        
        Returns:
            Dicionário com estatísticas
        """
        with self.lock:
            return {
                'client_id': self.client_id,
                'connected': self.connected,
                'broker': f"{self.broker['host']}:{self.broker['port']}",
                'subscribed_topics': len(self.subscribed_topics),
                'messages_published': self.stats['messages_published'],
                'messages_received': self.stats['messages_received'],
                'connection_attempts': self.stats['connection_attempts'],
                'connection_failures': self.stats['connection_failures']
            }


if __name__ == "__main__":
    # Teste do cliente MQTT (requer Mosquitto rodando)
    import sys
    import os
    
    # Adicionar path para importar módulos
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from backend.gateway.config_loader import load_mqtt_config
    from backend.gateway.message_formatter import MessageFormatter
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("=== TESTE: Cliente MQTT ===\n")
    print("⚠️  Certifique-se de que o Mosquitto está rodando!\n")
    
    try:
        # Carregar configuração
        config = load_mqtt_config()
        
        # Criar cliente
        client = MQTTClient(config, client_id="test_client")
        
        # Tentar conectar
        if client.connect():
            print("✅ Conectado com sucesso!\n")
            
            # Publicar mensagem de teste
            formatter = MessageFormatter("gateway_test")
            test_message = formatter.format_status_message('online', {
                'test': True,
                'timestamp': 'now'
            })
            
            topic = f"{config['topics']['prefix']}/{config['topics']['status']}"
            client.publish(topic, test_message)
            
            print(f"📤 Mensagem publicada em: {topic}\n")
            
            # Aguardar um pouco
            time.sleep(2)
            
            # Mostrar estatísticas
            print("📊 Estatísticas:")
            stats = client.get_stats()
            for key, value in stats.items():
                print(f"  {key}: {value}")
            
            # Desconectar
            client.disconnect()
            time.sleep(1)
            
            print("\n✅ Teste concluído!")
        else:
            print("❌ Não foi possível conectar ao broker")
            print("Verifique se o Mosquitto está rodando:")
            print("  mosquitto -v")
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
