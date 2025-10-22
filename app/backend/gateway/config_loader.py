"""
Carregador de Configurações MQTT
Sistema de Controle de Acesso - CEU Tres Pontes
"""

import os
import configparser
from typing import Dict, Any


def load_mqtt_config(config_file: str = None) -> Dict[str, Any]:
    """
    Carrega configurações MQTT do arquivo .ini
    
    Args:
        config_file: Caminho para o arquivo de configuração.
                    Se None, usa o caminho padrão.
    
    Returns:
        Dict com todas as configurações MQTT
    """
    if config_file is None:
        # Caminho padrão
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_file = os.path.join(base_dir, 'config', 'mqtt_config.ini')
    
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')
    
    # Extrair configurações
    mqtt_config = {
        'broker': {
            'host': config.get('MQTT', 'BROKER_HOST', fallback='localhost'),
            'port': config.getint('MQTT', 'BROKER_PORT', fallback=1883),
            'keepalive': config.getint('MQTT', 'BROKER_KEEPALIVE', fallback=60),
            'username': config.get('MQTT', 'BROKER_USERNAME', fallback=''),
            'password': config.get('MQTT', 'BROKER_PASSWORD', fallback=''),
        },
        'topics': {
            'prefix': config.get('MQTT', 'TOPIC_PREFIX', fallback='ceu/tres_pontes'),
            'sensors': config.get('MQTT', 'TOPIC_SENSORS', fallback='sensores'),
            'status': config.get('MQTT', 'TOPIC_STATUS', fallback='status'),
            'alerts': config.get('MQTT', 'TOPIC_ALERTS', fallback='alertas'),
            'commands': config.get('MQTT', 'TOPIC_COMMANDS', fallback='comandos'),
        },
        'qos': config.getint('MQTT', 'QOS_LEVEL', fallback=1),
        'gateway': {
            'id': config.get('GATEWAY', 'GATEWAY_ID', fallback='gateway_001'),
            'name': config.get('GATEWAY', 'GATEWAY_NAME', fallback='Gateway Principal'),
            'location': config.get('GATEWAY', 'GATEWAY_LOCATION', fallback='Sala de Controle'),
            'publish_interval': config.getint('GATEWAY', 'PUBLISH_INTERVAL', fallback=2),
            'batch_size': config.getint('GATEWAY', 'BATCH_SIZE', fallback=10),
        },
        'logging': {
            'level': config.get('LOGGING', 'LOG_LEVEL', fallback='INFO'),
            'file': config.get('LOGGING', 'LOG_FILE', fallback='logs/gateway.log'),
            'max_size': config.getint('LOGGING', 'LOG_MAX_SIZE', fallback=10485760),
            'backup_count': config.getint('LOGGING', 'LOG_BACKUP_COUNT', fallback=5),
        },
        'parque': {
            'nome': config.get('PARQUE', 'NOME', fallback='CEU Tres Pontes'),
            'capacidade_maxima': config.getint('PARQUE', 'CAPACIDADE_MAXIMA', fallback=5000),
            'timezone': config.get('PARQUE', 'TIMEZONE', fallback='America/Sao_Paulo'),
        }
    }
    
    return mqtt_config


def get_topic(config: Dict[str, Any], topic_type: str, sensor_id: str = None) -> str:
    """
    Gera o tópico MQTT completo.
    
    Args:
        config: Dicionário de configuração
        topic_type: Tipo do tópico ('sensors', 'status', 'alerts', 'commands')
        sensor_id: ID do sensor (opcional, usado para tópicos de sensores)
    
    Returns:
        String com o tópico completo
    
    Examples:
        >>> get_topic(config, 'sensors', 'LORA-001')
        'ceu/tres_pontes/sensores/LORA-001'
        
        >>> get_topic(config, 'status')
        'ceu/tres_pontes/status'
    """
    prefix = config['topics']['prefix']
    topic = config['topics'][topic_type]
    
    if sensor_id:
        return f"{prefix}/{topic}/{sensor_id}"
    else:
        return f"{prefix}/{topic}"


def validate_config(config: Dict[str, Any]) -> tuple[bool, str]:
    """
    Valida a configuração MQTT.
    
    Args:
        config: Dicionário de configuração para validar
    
    Returns:
        Tupla (is_valid, error_message)
    """
    # Validar campos obrigatórios
    required_keys = ['broker', 'topics', 'qos', 'gateway']
    
    for key in required_keys:
        if key not in config:
            return False, f"Configuração '{key}' não encontrada"
    
    # Validar broker
    if not config['broker']['host']:
        return False, "Host do broker não configurado"
    
    if not (1 <= config['broker']['port'] <= 65535):
        return False, "Porta do broker inválida"
    
    # Validar QoS
    if config['qos'] not in [0, 1, 2]:
        return False, "QoS deve ser 0, 1 ou 2"
    
    return True, "Configuração válida"


if __name__ == "__main__":
    # Teste do carregador de configurações
    try:
        config = load_mqtt_config()
        is_valid, message = validate_config(config)
        
        if is_valid:
            print("✅ Configuração carregada com sucesso!")
            print(f"\nBroker: {config['broker']['host']}:{config['broker']['port']}")
            print(f"Gateway: {config['gateway']['name']} ({config['gateway']['id']})")
            print(f"QoS: {config['qos']}")
            
            # Exemplos de tópicos
            print("\nExemplos de tópicos:")
            print(f"  Sensor: {get_topic(config, 'sensors', 'LORA-001')}")
            print(f"  Status: {get_topic(config, 'status')}")
            print(f"  Alertas: {get_topic(config, 'alerts')}")
        else:
            print(f"❌ Erro na configuração: {message}")
            
    except Exception as e:
        print(f"❌ Erro ao carregar configuração: {e}")
