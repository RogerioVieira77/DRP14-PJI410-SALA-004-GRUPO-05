"""
Formatador de Mensagens MQTT
Sistema de Controle de Acesso - CEU Tres Pontes

Responsável por formatar as mensagens dos sensores em JSON padronizado.
"""

import json
from datetime import datetime
from typing import Dict, Any, List


class MessageFormatter:
    """
    Classe para formatar mensagens dos sensores em padrão JSON.
    """
    
    def __init__(self, gateway_id: str = "gateway_001"):
        """
        Inicializa o formatador de mensagens.
        
        Args:
            gateway_id: ID do gateway que está enviando as mensagens
        """
        self.gateway_id = gateway_id
        self.message_count = 0
    
    def format_sensor_reading(self, sensor_reading: Dict[str, Any]) -> str:
        """
        Formata uma leitura de sensor para JSON MQTT.
        
        Args:
            sensor_reading: Dicionário com os dados da leitura do sensor
        
        Returns:
            String JSON formatada
        """
        self.message_count += 1
        
        # Estrutura padronizada da mensagem
        message = {
            'message_id': f"{self.gateway_id}_{self.message_count}",
            'gateway_id': self.gateway_id,
            'timestamp': datetime.now().isoformat(),
            'sensor': {
                'serial_number': sensor_reading.get('serial_number'),
                'protocol': sensor_reading.get('protocol'),
                'location': sensor_reading.get('location'),
            },
            'data': {
                'activity': sensor_reading.get('activity'),
                'timestamp': sensor_reading.get('timestamp'),
                'total_detections': sensor_reading.get('total_detections', 0),
            },
            'metadata': self._extract_metadata(sensor_reading)
        }
        
        return json.dumps(message, ensure_ascii=False)
    
    def _extract_metadata(self, sensor_reading: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrai metadados específicos do protocolo.
        
        Args:
            sensor_reading: Dicionário com os dados da leitura
        
        Returns:
            Dicionário com metadados
        """
        # Remove campos já processados
        excluded_keys = {
            'serial_number', 'protocol', 'location', 
            'activity', 'timestamp', 'total_detections'
        }
        
        metadata = {
            key: value 
            for key, value in sensor_reading.items() 
            if key not in excluded_keys
        }
        
        return metadata
    
    def format_batch_readings(self, readings: List[Dict[str, Any]]) -> str:
        """
        Formata múltiplas leituras em uma mensagem batch.
        
        Args:
            readings: Lista de leituras de sensores
        
        Returns:
            String JSON com batch de leituras
        """
        batch = {
            'batch_id': f"{self.gateway_id}_batch_{self.message_count}",
            'gateway_id': self.gateway_id,
            'timestamp': datetime.now().isoformat(),
            'count': len(readings),
            'readings': [
                json.loads(self.format_sensor_reading(reading))
                for reading in readings
            ]
        }
        
        return json.dumps(batch, ensure_ascii=False)
    
    def format_status_message(self, status: str, details: Dict[str, Any] = None) -> str:
        """
        Formata mensagem de status do gateway.
        
        Args:
            status: Status atual ('online', 'offline', 'error', 'warning')
            details: Detalhes adicionais do status
        
        Returns:
            String JSON com status
        """
        message = {
            'gateway_id': self.gateway_id,
            'timestamp': datetime.now().isoformat(),
            'status': status,
            'details': details or {}
        }
        
        return json.dumps(message, ensure_ascii=False)
    
    def format_alert_message(self, alert_type: str, severity: str, 
                            message: str, data: Dict[str, Any] = None) -> str:
        """
        Formata mensagem de alerta.
        
        Args:
            alert_type: Tipo do alerta ('capacity', 'sensor_offline', 'anomaly')
            severity: Severidade ('low', 'medium', 'high', 'critical')
            message: Mensagem descritiva do alerta
            data: Dados adicionais do alerta
        
        Returns:
            String JSON com alerta
        """
        alert = {
            'alert_id': f"{self.gateway_id}_alert_{self.message_count}",
            'gateway_id': self.gateway_id,
            'timestamp': datetime.now().isoformat(),
            'type': alert_type,
            'severity': severity,
            'message': message,
            'data': data or {}
        }
        
        return json.dumps(alert, ensure_ascii=False)
    
    def parse_message(self, json_string: str) -> Dict[str, Any]:
        """
        Parse uma mensagem JSON recebida.
        
        Args:
            json_string: String JSON para fazer parse
        
        Returns:
            Dicionário com os dados da mensagem
        """
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            raise ValueError(f"Erro ao fazer parse da mensagem JSON: {e}")
    
    def get_message_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas das mensagens processadas.
        
        Returns:
            Dicionário com estatísticas
        """
        return {
            'gateway_id': self.gateway_id,
            'total_messages': self.message_count,
            'timestamp': datetime.now().isoformat()
        }
    
    def reset_counter(self):
        """Reseta o contador de mensagens."""
        self.message_count = 0


if __name__ == "__main__":
    # Teste do formatador de mensagens
    print("=== TESTE: Message Formatter ===\n")
    
    formatter = MessageFormatter("gateway_test")
    
    # Exemplo de leitura de sensor
    sensor_reading = {
        'serial_number': 'LORA-12345',
        'protocol': 'LoRa',
        'location': 'Entrada Principal',
        'activity': 1,
        'timestamp': '2025-10-14T10:30:00',
        'total_detections': 42,
        'rssi_dbm': -65,
        'battery_level': 98.5,
        'spreading_factor': 7
    }
    
    # Testar formatação de leitura
    print("1. Leitura de Sensor:")
    reading_json = formatter.format_sensor_reading(sensor_reading)
    print(json.dumps(json.loads(reading_json), indent=2))
    
    # Testar mensagem de status
    print("\n2. Mensagem de Status:")
    status_json = formatter.format_status_message('online', {
        'sensors_connected': 4,
        'uptime_seconds': 3600
    })
    print(json.dumps(json.loads(status_json), indent=2))
    
    # Testar mensagem de alerta
    print("\n3. Mensagem de Alerta:")
    alert_json = formatter.format_alert_message(
        'capacity',
        'high',
        'Capacidade do parque atingiu 80%',
        {'current_capacity': 4000, 'max_capacity': 5000}
    )
    print(json.dumps(json.loads(alert_json), indent=2))
    
    # Estatísticas
    print("\n4. Estatísticas:")
    print(json.dumps(formatter.get_message_stats(), indent=2))
    
    print("\n✅ Testes concluídos!")
