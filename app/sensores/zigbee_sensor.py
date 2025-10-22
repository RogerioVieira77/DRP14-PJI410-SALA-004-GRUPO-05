"""
Simulador de Sensor ZigBee
Sistema de Controle de Acesso - CEU Tres Pontes

ZigBee é um protocolo de comunicação sem fio baseado em mesh network,
ideal para redes de sensores com múltiplos dispositivos interconectados.
"""

from .base_sensor import BaseSensor
import random


class ZigBeeSensor(BaseSensor):
    """
    Simulador de sensor com comunicação ZigBee.
    
    Características do ZigBee:
    - Mesh network (rede em malha)
    - Alcance médio (10-100 metros)
    - Baixo consumo de energia
    - Taxa de transmissão: 250 kbps
    - Frequência: 2.4 GHz
    - Suporta até 65.000 nós por rede
    
    Attributes:
        channel (int): Canal de comunicação (11-26)
        pan_id (str): PAN ID (Personal Area Network Identifier)
        node_type (str): Tipo do nó (Coordinator, Router, End Device)
        link_quality (int): Qualidade do link (LQI - 0-255)
        neighbor_count (int): Número de vizinhos na rede mesh
        battery_level (int): Nível de bateria em porcentagem
    """
    
    def __init__(self, location: str, serial_number: str = None,
                 node_type: str = "Router", channel: int = 11):
        """
        Inicializa o sensor ZigBee.
        
        Args:
            location (str): Localização do sensor
            serial_number (str, optional): Número de série personalizado
            node_type (str): Tipo do nó ('Coordinator', 'Router', 'End Device')
            channel (int): Canal ZigBee (11-26)
        """
        super().__init__(location, serial_number)
        self.frequency = 2.4  # GHz
        self.channel = max(11, min(26, channel))
        self.pan_id = self._generate_pan_id()
        self.node_type = node_type if node_type in ['Coordinator', 'Router', 'End Device'] else 'Router'
        self.link_quality = 255  # LQI inicial (máximo)
        self.neighbor_count = random.randint(2, 8)  # Vizinhos na mesh
        self.battery_level = 100  # Porcentagem
        self.hop_count = 0  # Número de saltos até o coordenador
        self.data_rate = 250  # kbps
        
    def _get_protocol_name(self) -> str:
        """Retorna o nome do protocolo."""
        return "ZigBee"
    
    def _generate_pan_id(self) -> str:
        """Gera um PAN ID único."""
        return f"0x{random.randint(0x0000, 0xFFFF):04X}"
    
    def _get_protocol_specific_data(self) -> dict:
        """
        Retorna dados específicos do protocolo ZigBee.
        
        Returns:
            dict: Parâmetros ZigBee simulados
        """
        # Simula variação na qualidade do link
        lqi_variation = random.randint(-10, 10)
        self.link_quality = max(0, min(255, self.link_quality + lqi_variation))
        
        # Simula consumo de bateria
        if self.activity == 1:
            # Routers consomem mais (sempre ligados para rotear)
            consumption = 0.02 if self.node_type == "Router" else 0.01
            self.battery_level = max(0, self.battery_level - consumption)
        
        # Simula variação no número de vizinhos
        if random.random() < 0.1:  # 10% de chance de mudança
            self.neighbor_count = max(1, self.neighbor_count + random.randint(-1, 1))
        
        # Calcula hop count baseado no tipo de nó
        if self.node_type == "Coordinator":
            self.hop_count = 0
        elif self.node_type == "Router":
            self.hop_count = random.randint(1, 3)
        else:  # End Device
            self.hop_count = random.randint(1, 5)
        
        return {
            'frequency_ghz': self.frequency,
            'channel': self.channel,
            'pan_id': self.pan_id,
            'node_type': self.node_type,
            'link_quality_lqi': self.link_quality,
            'neighbor_count': self.neighbor_count,
            'hop_count': self.hop_count,
            'data_rate_kbps': self.data_rate,
            'battery_level': round(self.battery_level, 1),
            'mesh_enabled': True
        }
    
    def set_node_type(self, node_type: str):
        """
        Define o tipo do nó na rede ZigBee.
        
        Args:
            node_type (str): 'Coordinator', 'Router' ou 'End Device'
        """
        valid_types = ['Coordinator', 'Router', 'End Device']
        if node_type in valid_types:
            self.node_type = node_type
        else:
            raise ValueError(f"Tipo de nó inválido. Use: {', '.join(valid_types)}")
    
    def set_channel(self, channel: int):
        """
        Define o canal ZigBee.
        
        Args:
            channel (int): Canal entre 11 e 26
        """
        if 11 <= channel <= 26:
            self.channel = channel
        else:
            raise ValueError("Canal ZigBee deve estar entre 11 e 26")
    
    def discover_neighbors(self) -> list:
        """
        Simula a descoberta de vizinhos na rede mesh.
        
        Returns:
            list: Lista de vizinhos descobertos
        """
        neighbors = []
        for i in range(self.neighbor_count):
            neighbor = {
                'address': f"0x{random.randint(0x0000, 0xFFFF):04X}",
                'lqi': random.randint(180, 255),
                'rssi': random.randint(-70, -30),
                'relationship': random.choice(['Parent', 'Child', 'Sibling'])
            }
            neighbors.append(neighbor)
        return neighbors
    
    def get_mesh_info(self) -> dict:
        """
        Retorna informações sobre a rede mesh.
        
        Returns:
            dict: Informações da topologia mesh
        """
        return {
            'pan_id': self.pan_id,
            'node_type': self.node_type,
            'neighbors': self.neighbor_count,
            'hop_count': self.hop_count,
            'can_route': self.node_type in ['Coordinator', 'Router']
        }
    
    def recharge_battery(self, percent: int = 100):
        """
        Simula recarga da bateria.
        
        Args:
            percent (int): Nível de carga desejado (0-100)
        """
        self.battery_level = max(0, min(100, percent))
    
    def __str__(self) -> str:
        """Representação em string do sensor ZigBee."""
        return (f"ZigBee Sensor [{self.serial_number}] - {self.location}\n"
                f"  Type: {self.node_type} | PAN: {self.pan_id} | "
                f"LQI: {self.link_quality} | Neighbors: {self.neighbor_count} | "
                f"Battery: {self.battery_level:.1f}% | "
                f"Detections: {self.total_detections}")
