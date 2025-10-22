"""
Simulador de Sensor RFID (Radio Frequency Identification)
Sistema de Controle de Acesso - CEU Tres Pontes

RFID é uma tecnologia de identificação por radiofrequência, ideal para
controle de acesso preciso e identificação de pessoas/objetos.
"""

from .base_sensor import BaseSensor
import random
import string


class RFIDSensor(BaseSensor):
    """
    Simulador de sensor RFID.
    
    Características do RFID:
    - Curto alcance (alguns centímetros a metros)
    - Identificação única por tag
    - Alta precisão
    - Frequências: 125 kHz (LF), 13.56 MHz (HF), 860-960 MHz (UHF)
    - Tipos: Passivo (sem bateria) ou Ativo (com bateria)
    
    Attributes:
        frequency_type (str): Tipo de frequência (LF, HF, UHF)
        frequency (float): Frequência de operação
        reader_power (int): Potência do leitor em dBm
        read_range (float): Alcance de leitura em metros
        tag_type (str): Tipo de tag (Passive, Active)
        last_tag_id (str): Último ID de tag lido
        tags_detected (list): Lista de tags detectadas
    """
    
    def __init__(self, location: str, serial_number: str = None,
                 frequency_type: str = "HF", tag_type: str = "Passive"):
        """
        Inicializa o sensor RFID.
        
        Args:
            location (str): Localização do sensor
            serial_number (str, optional): Número de série personalizado
            frequency_type (str): Tipo de frequência ('LF', 'HF', 'UHF')
            tag_type (str): Tipo de tag ('Passive', 'Active')
        """
        super().__init__(location, serial_number)
        self.frequency_type = frequency_type if frequency_type in ['LF', 'HF', 'UHF'] else 'HF'
        self.frequency = self._get_frequency()
        self.tag_type = tag_type if tag_type in ['Passive', 'Active'] else 'Passive'
        self.reader_power = 30  # dBm
        self.read_range = self._get_read_range()
        self.last_tag_id = None
        self.tags_detected = []
        self.antenna_count = random.randint(1, 4)
        self.read_rate = 0  # Tags por segundo
        
    def _get_protocol_name(self) -> str:
        """Retorna o nome do protocolo."""
        return "RFID"
    
    def _get_frequency(self) -> float:
        """Retorna a frequência baseada no tipo."""
        frequencies = {
            'LF': 0.125,    # 125 kHz
            'HF': 13.56,    # 13.56 MHz
            'UHF': 915.0    # 915 MHz (Brasil)
        }
        return frequencies.get(self.frequency_type, 13.56)
    
    def _get_read_range(self) -> float:
        """Calcula o alcance de leitura baseado no tipo."""
        if self.tag_type == "Active":
            ranges = {'LF': 1.0, 'HF': 3.0, 'UHF': 100.0}
        else:  # Passive
            ranges = {'LF': 0.1, 'HF': 1.0, 'UHF': 12.0}
        return ranges.get(self.frequency_type, 1.0)
    
    def _generate_tag_id(self) -> str:
        """Gera um ID de tag RFID simulado."""
        # EPC (Electronic Product Code) format: 96 bits (24 caracteres hex)
        if self.frequency_type == 'UHF':
            return ''.join(random.choices(string.hexdigits.upper()[:16], k=24))
        else:
            # UID format para LF/HF: 7-10 bytes
            return ''.join(random.choices(string.hexdigits.upper()[:16], k=14))
    
    def _get_protocol_specific_data(self) -> dict:
        """
        Retorna dados específicos do protocolo RFID.
        
        Returns:
            dict: Parâmetros RFID simulados
        """
        # Se houve detecção, gera uma tag
        if self.activity == 1:
            self.last_tag_id = self._generate_tag_id()
            
            # Adiciona à lista de tags detectadas
            tag_reading = {
                'tag_id': self.last_tag_id,
                'timestamp': self.timestamp.isoformat(),
                'rssi': random.randint(-70, -30),
                'read_count': 1,
                'antenna_port': random.randint(1, self.antenna_count)
            }
            self.tags_detected.append(tag_reading)
            
            # Mantém apenas as últimas 1000 leituras
            if len(self.tags_detected) > 1000:
                self.tags_detected = self.tags_detected[-1000:]
        
        # Calcula taxa de leitura (tags por segundo)
        self.read_rate = random.uniform(0, 50) if self.activity == 1 else 0
        
        return {
            'frequency_type': self.frequency_type,
            'frequency_mhz': self.frequency,
            'tag_type': self.tag_type,
            'reader_power_dbm': self.reader_power,
            'read_range_meters': self.read_range,
            'last_tag_id': self.last_tag_id,
            'antenna_count': self.antenna_count,
            'read_rate_tps': round(self.read_rate, 2),
            'total_tags_detected': len(self.tags_detected),
            'protocol_standard': self._get_protocol_standard()
        }
    
    def _get_protocol_standard(self) -> str:
        """Retorna o padrão de protocolo RFID."""
        standards = {
            'LF': 'ISO 14223',
            'HF': 'ISO 14443 / ISO 15693',
            'UHF': 'ISO 18000-6C / EPC Gen2'
        }
        return standards.get(self.frequency_type, 'Unknown')
    
    def read_tag(self) -> dict:
        """
        Simula a leitura de uma tag RFID.
        
        Returns:
            dict: Dados da tag lida
        """
        # Força uma detecção
        reading = self.simulate_detection(force_detection=True)
        
        if self.last_tag_id:
            return {
                'success': True,
                'tag_id': self.last_tag_id,
                'tag_type': self.tag_type,
                'rssi': random.randint(-70, -30),
                'timestamp': self.timestamp.isoformat(),
                'reader': self.serial_number,
                'location': self.location
            }
        else:
            return {
                'success': False,
                'error': 'No tag detected'
            }
    
    def get_detected_tags(self, limit: int = 10) -> list:
        """
        Retorna as últimas tags detectadas.
        
        Args:
            limit (int): Número máximo de tags a retornar
        
        Returns:
            list: Lista das últimas tags detectadas
        """
        return self.tags_detected[-limit:]
    
    def get_unique_tags_count(self) -> int:
        """
        Conta quantas tags únicas foram detectadas.
        
        Returns:
            int: Número de tags únicas
        """
        unique_tags = set(tag['tag_id'] for tag in self.tags_detected)
        return len(unique_tags)
    
    def set_reader_power(self, power_dbm: int):
        """
        Ajusta a potência do leitor RFID.
        
        Args:
            power_dbm (int): Potência em dBm (tipicamente 10-30)
        """
        if 10 <= power_dbm <= 36:
            self.reader_power = power_dbm
            # Ajusta o alcance baseado na potência
            self.read_range = self._get_read_range() * (power_dbm / 30)
        else:
            raise ValueError("Potência deve estar entre 10 e 36 dBm")
    
    def clear_tag_history(self):
        """Limpa o histórico de tags detectadas."""
        self.tags_detected = []
        self.last_tag_id = None
    
    def get_reader_info(self) -> dict:
        """
        Retorna informações detalhadas do leitor RFID.
        
        Returns:
            dict: Informações do leitor
        """
        return {
            'serial_number': self.serial_number,
            'location': self.location,
            'frequency_type': self.frequency_type,
            'frequency': f"{self.frequency} {'kHz' if self.frequency < 1 else 'MHz'}",
            'tag_type_supported': self.tag_type,
            'read_range': f"{self.read_range} meters",
            'antenna_count': self.antenna_count,
            'protocol_standard': self._get_protocol_standard(),
            'total_reads': len(self.tags_detected),
            'unique_tags': self.get_unique_tags_count()
        }
    
    def __str__(self) -> str:
        """Representação em string do sensor RFID."""
        freq_unit = 'kHz' if self.frequency < 1 else 'MHz'
        return (f"RFID Sensor [{self.serial_number}] - {self.location}\n"
                f"  Type: {self.frequency_type} ({self.frequency} {freq_unit}) | "
                f"Range: {self.read_range}m | "
                f"Tags: {len(self.tags_detected)} (unique: {self.get_unique_tags_count()}) | "
                f"Detections: {self.total_detections}")
