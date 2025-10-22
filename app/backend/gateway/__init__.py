"""
Módulo Gateway
Sistema de Controle de Acesso - CEU Tres Pontes

Este módulo gerencia a comunicação entre sensores e o broker MQTT.
"""

from .gateway import Gateway
from .mqtt_client import MQTTClient
from .message_formatter import MessageFormatter
from .config_loader import load_mqtt_config

__all__ = [
    'Gateway',
    'MQTTClient',
    'MessageFormatter',
    'load_mqtt_config'
]

__version__ = '2.0.0'
