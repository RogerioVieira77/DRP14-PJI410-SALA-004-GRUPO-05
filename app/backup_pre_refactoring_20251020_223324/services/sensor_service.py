"""
Service de Sensores
Lógica de negócio relacionada a sensores
"""

from typing import Optional, List
from app import db
from app.models.sensor import Sensor
from app.schemas.sensor_schema import SensorSchema


class SensorService:
    """Serviço de gerenciamento de sensores"""
    
    @staticmethod
    def list_sensors(
        status: Optional[str] = None,
        protocol: Optional[str] = None,
        location: Optional[str] = None
    ) -> List[Sensor]:
        """
        Listar sensores com filtros opcionais
        
        Args:
            status: Filtrar por status
            protocol: Filtrar por protocolo
            location: Filtrar por localização (busca parcial)
            
        Returns:
            List[Sensor]: Lista de sensores
        """
        query = Sensor.query
        
        if status:
            query = query.filter_by(status=status)
        
        if protocol:
            query = query.filter_by(protocol=protocol)
        
        if location:
            query = query.filter(Sensor.location.ilike(f'%{location}%'))
        
        return query.all()
    
    @staticmethod
    def get_sensor_by_id(sensor_id: int) -> Sensor:
        """
        Buscar sensor por ID
        
        Args:
            sensor_id: ID do sensor
            
        Returns:
            Sensor: Sensor encontrado
            
        Raises:
            ValueError: Se sensor não encontrado
        """
        sensor = Sensor.query.get(sensor_id)
        if not sensor:
            raise ValueError('Sensor não encontrado')
        return sensor
    
    @staticmethod
    def get_sensor_by_serial(serial_number: str) -> Optional[Sensor]:
        """
        Buscar sensor por serial number
        
        Args:
            serial_number: Número de série do sensor
            
        Returns:
            Sensor: Sensor encontrado ou None
        """
        return Sensor.query.filter_by(serial_number=serial_number).first()
    
    @staticmethod
    def create_sensor(data: dict) -> Sensor:
        """
        Criar novo sensor
        
        Args:
            data: Dados do sensor
            
        Returns:
            Sensor: Sensor criado
            
        Raises:
            ValueError: Se serial number já existe
        """
        # Verificar se serial number já existe
        if SensorService.get_sensor_by_serial(data['serial_number']):
            raise ValueError('Serial number já existe')
        
        sensor = Sensor(**data)
        db.session.add(sensor)
        db.session.commit()
        
        return sensor
    
    @staticmethod
    def update_sensor(sensor_id: int, data: dict) -> Sensor:
        """
        Atualizar sensor
        
        Args:
            sensor_id: ID do sensor
            data: Dados para atualizar
            
        Returns:
            Sensor: Sensor atualizado
            
        Raises:
            ValueError: Se sensor não encontrado
        """
        sensor = SensorService.get_sensor_by_id(sensor_id)
        
        # Atualizar campos
        for key, value in data.items():
            if hasattr(sensor, key):
                setattr(sensor, key, value)
        
        db.session.commit()
        return sensor
    
    @staticmethod
    def delete_sensor(sensor_id: int) -> None:
        """
        Deletar sensor
        
        Args:
            sensor_id: ID do sensor
            
        Raises:
            ValueError: Se sensor não encontrado
        """
        sensor = SensorService.get_sensor_by_id(sensor_id)
        db.session.delete(sensor)
        db.session.commit()
    
    @staticmethod
    def get_protocols() -> List[str]:
        """
        Obter lista de protocolos suportados
        
        Returns:
            List[str]: Lista de protocolos
        """
        return ['LoRa', 'ZigBee', 'Sigfox', 'RFID', 'BLE', 'WiFi']
    
    @staticmethod
    def get_status_options() -> List[str]:
        """
        Obter opções de status
        
        Returns:
            List[str]: Lista de status
        """
        return ['active', 'inactive', 'maintenance', 'error']
