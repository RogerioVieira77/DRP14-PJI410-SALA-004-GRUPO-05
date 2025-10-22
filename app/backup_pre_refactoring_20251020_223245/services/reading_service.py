"""
Service de Leituras
Lógica de negócio relacionada a leituras de sensores
"""

from typing import Optional, List
from datetime import datetime
from app import db
from app.models.reading import Reading
from app.models.sensor import Sensor
from app.services.sensor_service import SensorService


class ReadingService:
    """Serviço de gerenciamento de leituras"""
    
    @staticmethod
    def list_readings(
        sensor_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 50
    ) -> List[Reading]:
        """
        Listar leituras com filtros
        
        Args:
            sensor_id: Filtrar por sensor
            start_date: Data inicial
            end_date: Data final
            limit: Limite de resultados
            
        Returns:
            List[Reading]: Lista de leituras
        """
        query = Reading.query
        
        if sensor_id:
            query = query.filter_by(sensor_id=sensor_id)
        
        if start_date:
            query = query.filter(Reading.timestamp >= start_date)
        
        if end_date:
            query = query.filter(Reading.timestamp <= end_date)
        
        return query.order_by(Reading.timestamp.desc()).limit(limit).all()
    
    @staticmethod
    def get_reading_by_id(reading_id: int) -> Reading:
        """
        Buscar leitura por ID
        
        Args:
            reading_id: ID da leitura
            
        Returns:
            Reading: Leitura encontrada
            
        Raises:
            ValueError: Se leitura não encontrada
        """
        reading = Reading.query.get(reading_id)
        if not reading:
            raise ValueError('Leitura não encontrada')
        return reading
    
    @staticmethod
    def create_reading(data: dict) -> Reading:
        """
        Criar nova leitura
        
        Args:
            data: Dados da leitura
            
        Returns:
            Reading: Leitura criada
            
        Raises:
            ValueError: Se sensor não encontrado
        """
        # Verificar se sensor existe
        sensor = SensorService.get_sensor_by_id(data['sensor_id'])
        
        # Preparar metadados do sensor
        sensor_metadata = {}
        metadata_fields = ['battery_level', 'signal_strength', 'temperature', 'humidity']
        
        for field in metadata_fields:
            if field in data:
                sensor_metadata[field] = data[field]
        
        # Adicionar metadata customizado
        if 'metadata' in data:
            sensor_metadata.update(data['metadata'])
        
        # Criar leitura
        reading = Reading(
            sensor_id=data['sensor_id'],
            activity=data.get('activity', 0),
            timestamp=datetime.utcnow(),
            sensor_metadata=sensor_metadata if sensor_metadata else None
        )
        
        db.session.add(reading)
        
        # Atualizar sensor
        ReadingService._update_sensor_stats(sensor, data)
        
        db.session.commit()
        
        return reading
    
    @staticmethod
    def create_bulk_readings(readings_data: List[dict]) -> dict:
        """
        Criar múltiplas leituras
        
        Args:
            readings_data: Lista de dados de leituras
            
        Returns:
            dict: Resultado com contadores
        """
        created = 0
        errors = []
        
        for data in readings_data:
            try:
                ReadingService.create_reading(data)
                created += 1
            except ValueError as e:
                errors.append({
                    'data': data,
                    'error': str(e)
                })
            except Exception as e:
                errors.append({
                    'data': data,
                    'error': f'Erro inesperado: {str(e)}'
                })
        
        return {
            'created': created,
            'errors': errors
        }
    
    @staticmethod
    def get_latest_reading(sensor_id: int) -> Optional[Reading]:
        """
        Obter última leitura de um sensor
        
        Args:
            sensor_id: ID do sensor
            
        Returns:
            Reading: Última leitura ou None
        """
        return Reading.query.filter_by(sensor_id=sensor_id)\
            .order_by(Reading.timestamp.desc()).first()
    
    @staticmethod
    def _update_sensor_stats(sensor: Sensor, reading_data: dict) -> None:
        """
        Atualizar estatísticas do sensor
        
        Args:
            sensor: Sensor a ser atualizado
            reading_data: Dados da leitura
        """
        sensor.last_reading_at = datetime.utcnow()
        sensor.total_readings += 1
        
        if 'battery_level' in reading_data:
            sensor.battery_level = reading_data['battery_level']
        
        if 'signal_strength' in reading_data:
            sensor.signal_strength = reading_data['signal_strength']
