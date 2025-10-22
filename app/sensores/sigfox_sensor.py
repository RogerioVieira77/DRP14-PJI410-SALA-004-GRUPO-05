"""
Simulador de Sensor Sigfox
Sistema de Controle de Acesso - CEU Tres Pontes

Sigfox é uma rede LPWAN (Low Power Wide Area Network) com cobertura global,
ideal para transmissão de pequenos pacotes de dados a longas distâncias.
"""

from .base_sensor import BaseSensor
import random


class SigfoxSensor(BaseSensor):
    """
    Simulador de sensor com comunicação Sigfox.
    
    Características do Sigfox:
    - LPWAN (Low Power Wide Area Network)
    - Alcance muito longo (até 50 km em áreas rurais)
    - Consumo extremamente baixo
    - Limite de mensagens: 140 mensagens/dia (uplink)
    - Payload: 12 bytes por mensagem
    - Frequência: 902 MHz (Brasil - RCZ4)
    - Cobertura global através de operadoras
    
    Attributes:
        device_id (str): ID único do dispositivo Sigfox
        pac_code (str): Código PAC para ativação
        rcz (int): Radio Configuration Zone (4 para Brasil)
        messages_sent_today (int): Contador de mensagens enviadas hoje
        message_limit (int): Limite diário de mensagens
        signal_strength (int): Força do sinal em dBm
        battery_level (int): Nível de bateria em porcentagem
    """
    
    def __init__(self, location: str, serial_number: str = None):
        """
        Inicializa o sensor Sigfox.
        
        Args:
            location (str): Localização do sensor
            serial_number (str, optional): Número de série personalizado
        """
        super().__init__(location, serial_number)
        self.device_id = self._generate_device_id()
        self.pac_code = self._generate_pac_code()
        self.frequency = 902  # MHz - RCZ4 (Brasil)
        self.rcz = 4  # Radio Configuration Zone - Brasil
        self.messages_sent_today = 0
        self.message_limit = 140  # Limite diário
        self.signal_strength = -110  # RSSI inicial
        self.battery_level = 100  # Porcentagem
        self.payload_size = 12  # bytes
        self.last_sequence_number = 0
        
    def _get_protocol_name(self) -> str:
        """Retorna o nome do protocolo."""
        return "Sigfox"
    
    def _generate_device_id(self) -> str:
        """Gera um Device ID Sigfox (hexadecimal de 8 caracteres)."""
        return f"{random.randint(0x00000000, 0xFFFFFFFF):08X}"
    
    def _generate_pac_code(self) -> str:
        """Gera um PAC Code (16 caracteres hexadecimais)."""
        return ''.join(random.choices('0123456789ABCDEF', k=16))
    
    def _get_protocol_specific_data(self) -> dict:
        """
        Retorna dados específicos do protocolo Sigfox.
        
        Returns:
            dict: Parâmetros Sigfox simulados
        """
        # Simula variação no RSSI
        rssi_variation = random.randint(-3, 3)
        self.signal_strength = max(-140, min(-90, self.signal_strength + rssi_variation))
        
        # Simula consumo de bateria (muito baixo)
        if self.activity == 1:
            self.battery_level = max(0, self.battery_level - 0.005)
        
        # Incrementa contador de mensagens se houver detecção
        if self.activity == 1 and self.messages_sent_today < self.message_limit:
            self.messages_sent_today += 1
            self.last_sequence_number += 1
        
        # Calcula estimativa de vida útil da bateria
        battery_life_days = self._estimate_battery_life()
        
        return {
            'device_id': self.device_id,
            'pac_code': self.pac_code,
            'frequency_mhz': self.frequency,
            'rcz': f"RCZ{self.rcz}",
            'rssi_dbm': round(self.signal_strength, 1),
            'messages_sent_today': self.messages_sent_today,
            'messages_remaining': self.message_limit - self.messages_sent_today,
            'message_limit': self.message_limit,
            'payload_size_bytes': self.payload_size,
            'sequence_number': self.last_sequence_number,
            'battery_level': round(self.battery_level, 2),
            'battery_life_estimate_days': battery_life_days
        }
    
    def _estimate_battery_life(self) -> int:
        """
        Estima a vida útil da bateria em dias.
        
        Returns:
            int: Dias estimados de bateria
        """
        if self.battery_level <= 0:
            return 0
        
        # Assume consumo médio por mensagem e frequência de detecções
        avg_messages_per_day = 50  # Estimativa conservadora
        consumption_per_message = 0.005
        days_remaining = self.battery_level / (avg_messages_per_day * consumption_per_message)
        
        return int(days_remaining)
    
    def can_send_message(self) -> bool:
        """
        Verifica se o sensor pode enviar uma mensagem.
        
        Returns:
            bool: True se ainda há crédito de mensagens disponível
        """
        return self.messages_sent_today < self.message_limit
    
    def reset_daily_counter(self):
        """Reseta o contador diário de mensagens (simula início de um novo dia)."""
        self.messages_sent_today = 0
    
    def get_coverage_info(self) -> dict:
        """
        Retorna informações sobre cobertura Sigfox.
        
        Returns:
            dict: Informações de cobertura
        """
        # Simula qualidade de cobertura baseada no RSSI
        if self.signal_strength >= -120:
            coverage = "Excelente"
        elif self.signal_strength >= -130:
            coverage = "Bom"
        elif self.signal_strength >= -135:
            coverage = "Regular"
        else:
            coverage = "Fraco"
        
        return {
            'coverage_quality': coverage,
            'rssi': self.signal_strength,
            'rcz': f"RCZ{self.rcz}",
            'operator': "Sigfox Brasil",
            'global_coverage': True
        }
    
    def simulate_downlink(self) -> dict:
        """
        Simula recebimento de mensagem downlink (da rede para o dispositivo).
        Sigfox permite 4 mensagens downlink por dia.
        
        Returns:
            dict: Dados da mensagem downlink
        """
        return {
            'downlink_data': f"{random.randint(0, 255):02X}" * 8,  # 8 bytes
            'ack': True,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
    
    def recharge_battery(self, percent: int = 100):
        """
        Simula recarga/troca da bateria.
        
        Args:
            percent (int): Nível de carga desejado (0-100)
        """
        self.battery_level = max(0, min(100, percent))
    
    def __str__(self) -> str:
        """Representação em string do sensor Sigfox."""
        return (f"Sigfox Sensor [{self.serial_number}] - {self.location}\n"
                f"  Device ID: {self.device_id} | "
                f"Messages: {self.messages_sent_today}/{self.message_limit} | "
                f"Battery: {self.battery_level:.2f}% ({self._estimate_battery_life()} days) | "
                f"Detections: {self.total_detections}")
