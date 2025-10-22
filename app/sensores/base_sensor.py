"""
Classe Base para Simulação de Sensores
Sistema de Controle de Acesso - CEU Tres Pontes
"""

from abc import ABC, abstractmethod
from datetime import datetime
import uuid
import random
import json


class BaseSensor(ABC):
    """
    Classe abstrata base para todos os sensores do sistema.
    
    Attributes:
        serial_number (str): Número de série único do sensor
        protocol (str): Protocolo de comunicação utilizado
        location (str): Localização do sensor no parque
        activity (int): Estado binário (0 ou 1) indicando detecção
        timestamp (datetime): Data e hora da última atividade
    """
    
    def __init__(self, location: str, serial_number: str = None):
        """
        Inicializa o sensor base.
        
        Args:
            location (str): Localização do sensor (ex: "Entrada Principal", "Saída Lateral")
            serial_number (str, optional): Número de série. Se não fornecido, gera automaticamente.
        """
        self.serial_number = serial_number or self._generate_serial_number()
        self.location = location
        self.activity = 0
        self.timestamp = None
        self.protocol = self._get_protocol_name()
        self.total_detections = 0
        self.last_readings = []  # Histórico das últimas leituras
        
    @abstractmethod
    def _get_protocol_name(self) -> str:
        """Retorna o nome do protocolo de comunicação."""
        pass
    
    def _generate_serial_number(self) -> str:
        """Gera um número de série único para o sensor."""
        prefix = self._get_protocol_name().upper()[:4]
        unique_id = uuid.uuid4().hex[:8].upper()
        return f"{prefix}-{unique_id}"
    
    def simulate_detection(self, force_detection: bool = None) -> dict:
        """
        Simula uma detecção de pessoa pelo sensor.
        
        Args:
            force_detection (bool, optional): Força um valor específico de detecção.
                                             Se None, gera aleatoriamente.
        
        Returns:
            dict: Dados da leitura do sensor
        """
        # Se não forçado, gera aleatoriamente (30% de chance de detecção)
        if force_detection is None:
            self.activity = 1 if random.random() < 0.3 else 0
        else:
            self.activity = 1 if force_detection else 0
        
        # Registra o timestamp
        self.timestamp = datetime.now()
        
        # Incrementa contador se houve detecção
        if self.activity == 1:
            self.total_detections += 1
        
        # Cria o registro da leitura
        reading = self._create_reading()
        
        # Adiciona ao histórico (mantém últimas 100 leituras)
        self.last_readings.append(reading)
        if len(self.last_readings) > 100:
            self.last_readings.pop(0)
        
        return reading
    
    def _create_reading(self) -> dict:
        """
        Cria um registro de leitura do sensor.
        
        Returns:
            dict: Dados formatados da leitura
        """
        reading = {
            'serial_number': self.serial_number,
            'protocol': self.protocol,
            'location': self.location,
            'activity': self.activity,
            'timestamp': self.timestamp.isoformat(),
            'total_detections': self.total_detections
        }
        
        # Adiciona dados específicos do protocolo
        reading.update(self._get_protocol_specific_data())
        
        return reading
    
    @abstractmethod
    def _get_protocol_specific_data(self) -> dict:
        """
        Retorna dados específicos do protocolo de comunicação.
        Deve ser implementado pelas classes filhas.
        """
        pass
    
    def get_status(self) -> dict:
        """
        Retorna o status atual do sensor.
        
        Returns:
            dict: Informações de status do sensor
        """
        return {
            'serial_number': self.serial_number,
            'protocol': self.protocol,
            'location': self.location,
            'total_detections': self.total_detections,
            'last_activity': self.timestamp.isoformat() if self.timestamp else None,
            'operational': True
        }
    
    def get_history(self, limit: int = 10) -> list:
        """
        Retorna o histórico de leituras.
        
        Args:
            limit (int): Número máximo de leituras a retornar
        
        Returns:
            list: Lista das últimas leituras
        """
        return self.last_readings[-limit:]
    
    def reset(self):
        """Reseta o sensor para o estado inicial."""
        self.activity = 0
        self.timestamp = None
        self.total_detections = 0
        self.last_readings = []
    
    def to_json(self) -> str:
        """
        Converte o estado atual do sensor para JSON.
        
        Returns:
            str: Representação JSON do sensor
        """
        return json.dumps(self.get_status(), indent=2)
    
    def __str__(self) -> str:
        """Representação em string do sensor."""
        return (f"{self.protocol} Sensor [{self.serial_number}] - "
                f"Location: {self.location} - "
                f"Detections: {self.total_detections}")
    
    def __repr__(self) -> str:
        """Representação técnica do sensor."""
        return (f"{self.__class__.__name__}(serial_number='{self.serial_number}', "
                f"location='{self.location}')")
