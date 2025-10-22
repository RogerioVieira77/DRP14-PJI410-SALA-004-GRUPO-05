"""
Simulador de Sensor LoRa (Long Range)
Sistema de Controle de Acesso - CEU Tres Pontes

LoRa é um protocolo de comunicação de longo alcance e baixo consumo de energia,
ideal para aplicações IoT em áreas extensas como parques.
"""

from .base_sensor import BaseSensor
import random


class LoRaSensor(BaseSensor):
    """
    Simulador de sensor com comunicação LoRa.
    
    Características do LoRa:
    - Longo alcance (até 15 km em áreas abertas)
    - Baixo consumo de energia
    - Taxa de transmissão baixa (0.3 - 50 kbps)
    - Frequência: 915 MHz (Brasil)
    - Spreading Factor (SF7-SF12)
    
    Attributes:
        frequency (float): Frequência de operação em MHz
        spreading_factor (int): Fator de espalhamento (7-12)
        bandwidth (int): Largura de banda em kHz
        signal_strength (int): Força do sinal (RSSI) em dBm
        battery_level (int): Nível de bateria em porcentagem
    """
    
    def __init__(self, location: str, serial_number: str = None, 
                 spreading_factor: int = 7):
        """
        Inicializa o sensor LoRa.
        
        Args:
            location (str): Localização do sensor
            serial_number (str, optional): Número de série personalizado
            spreading_factor (int): SF entre 7 e 12 (default: 7)
        """
        super().__init__(location, serial_number)
        self.frequency = 915.0  # MHz - Frequência Brasil
        self.spreading_factor = max(7, min(12, spreading_factor))
        self.bandwidth = 125  # kHz
        self.signal_strength = -60  # RSSI inicial
        self.battery_level = 100  # Porcentagem
        self.transmission_power = 14  # dBm
        
    def _get_protocol_name(self) -> str:
        """Retorna o nome do protocolo."""
        return "LoRa"
    
    def _get_protocol_specific_data(self) -> dict:
        """
        Retorna dados específicos do protocolo LoRa.
        
        Returns:
            dict: Parâmetros LoRa simulados
        """
        # Simula variação no RSSI (força do sinal)
        rssi_variation = random.randint(-5, 5)
        self.signal_strength = max(-120, min(-30, self.signal_strength + rssi_variation))
        
        # Simula consumo de bateria (descarga lenta)
        if self.activity == 1:
            self.battery_level = max(0, self.battery_level - 0.01)
        
        # Simula SNR (Signal-to-Noise Ratio)
        snr = random.uniform(5.0, 15.0)
        
        return {
            'frequency_mhz': self.frequency,
            'spreading_factor': self.spreading_factor,
            'bandwidth_khz': self.bandwidth,
            'rssi_dbm': round(self.signal_strength, 1),
            'snr_db': round(snr, 2),
            'transmission_power_dbm': self.transmission_power,
            'battery_level': round(self.battery_level, 1),
            'data_rate': self._calculate_data_rate()
        }
    
    def _calculate_data_rate(self) -> float:
        """
        Calcula a taxa de dados baseada no SF e BW.
        
        Returns:
            float: Taxa de dados em bps
        """
        # Fórmula simplificada: DR = SF * (BW / 2^SF)
        data_rate = self.spreading_factor * (self.bandwidth * 1000 / (2 ** self.spreading_factor))
        return round(data_rate, 2)
    
    def set_spreading_factor(self, sf: int):
        """
        Ajusta o Spreading Factor (alcance vs velocidade).
        
        Args:
            sf (int): Spreading Factor entre 7 (rápido, curto alcance) 
                      e 12 (lento, longo alcance)
        """
        if 7 <= sf <= 12:
            self.spreading_factor = sf
        else:
            raise ValueError("Spreading Factor deve estar entre 7 e 12")
    
    def recharge_battery(self, percent: int = 100):
        """
        Simula recarga da bateria.
        
        Args:
            percent (int): Nível de carga desejado (0-100)
        """
        self.battery_level = max(0, min(100, percent))
    
    def get_range_estimate(self) -> str:
        """
        Estima o alcance baseado no SF.
        
        Returns:
            str: Estimativa de alcance
        """
        ranges = {
            7: "2-5 km",
            8: "4-6 km",
            9: "5-8 km",
            10: "7-10 km",
            11: "10-12 km",
            12: "12-15 km"
        }
        return ranges.get(self.spreading_factor, "Desconhecido")
    
    def __str__(self) -> str:
        """Representação em string do sensor LoRa."""
        return (f"LoRa Sensor [{self.serial_number}] - {self.location}\n"
                f"  SF: {self.spreading_factor} | Range: {self.get_range_estimate()} | "
                f"Battery: {self.battery_level:.1f}% | "
                f"Detections: {self.total_detections}")
