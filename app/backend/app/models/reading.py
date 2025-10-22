"""
Reading Model
Representa uma leitura de sensor
"""

from datetime import datetime
from app import db


class Reading(db.Model):
    """
    Modelo de Leitura de Sensor
    
    Armazena cada leitura individual de um sensor:
    - Timestamp
    - Atividade detectada (0 = nada, 1 = pessoa)
    - Metadados do sensor
    """
    __tablename__ = 'readings'
    
    # Campos principais
    id = db.Column(db.BigInteger, primary_key=True)
    sensor_id = db.Column(
        db.Integer,
        db.ForeignKey('sensors.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    
    # Dados da leitura
    activity = db.Column(db.SmallInteger, nullable=False)  # 0 = nada, 1 = detecção
    timestamp = db.Column(db.DateTime, nullable=False, index=True)
    
    # Metadados do sensor no momento da leitura (JSON)
    sensor_metadata = db.Column(db.JSON)  # battery_level, rssi, temperature, etc.
    
    # Message ID do MQTT (para rastreamento)
    message_id = db.Column(db.String(100), index=True)
    gateway_id = db.Column(db.String(50), index=True)
    
    # Timestamp de inserção no banco
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Índices compostos para queries otimizadas
    __table_args__ = (
        db.Index('idx_sensor_timestamp', 'sensor_id', 'timestamp'),
        db.Index('idx_timestamp_activity', 'timestamp', 'activity'),
        db.Index('idx_sensor_activity', 'sensor_id', 'activity'),
        db.Index('idx_gateway_timestamp', 'gateway_id', 'timestamp'),
    )
    
    def __repr__(self):
        return f'<Reading {self.id} sensor={self.sensor_id} activity={self.activity}>'
    
    def to_dict(self, include_sensor=False):
        """
        Converte a leitura para dicionário
        
        Args:
            include_sensor: Incluir dados do sensor
        
        Returns:
            dict: Representação da leitura
        """
        data = {
            'id': self.id,
            'sensor_id': self.sensor_id,
            'activity': self.activity,
            'timestamp': self.timestamp.isoformat(),
            'sensor_metadata': self.sensor_metadata,
            'message_id': self.message_id,
            'gateway_id': self.gateway_id,
            'created_at': self.created_at.isoformat()
        }
        
        if include_sensor and self.sensor:
            data['sensor'] = {
                'serial_number': self.sensor.serial_number,
                'protocol': self.sensor.protocol,
                'location': self.sensor.location
            }
        
        return data
    
    @classmethod
    def create_from_mqtt(cls, mqtt_data):
        """
        Cria uma leitura a partir de mensagem MQTT
        
        Args:
            mqtt_data: Dicionário com dados da mensagem MQTT
        
        Returns:
            Reading: Nova instância de leitura
        """
        from app.models.sensor import Sensor
        
        # Buscar sensor pelo serial number
        sensor = Sensor.get_by_serial(mqtt_data['sensor']['serial_number'])
        
        if not sensor:
            raise ValueError(f"Sensor não encontrado: {mqtt_data['sensor']['serial_number']}")
        
        # Criar leitura
        reading = cls(
            sensor_id=sensor.id,
            activity=mqtt_data['data']['activity'],
            timestamp=datetime.fromisoformat(mqtt_data['data']['timestamp'].replace('Z', '+00:00')),
            sensor_metadata=mqtt_data.get('metadata', {}),
            message_id=mqtt_data.get('message_id'),
            gateway_id=mqtt_data.get('gateway_id')
        )
        
        # Atualizar estatísticas do sensor
        sensor.total_readings += 1
        sensor.last_reading_at = reading.timestamp
        
        # Atualizar battery_level e signal_strength se disponíveis
        if reading.sensor_metadata:
            if 'battery_level' in reading.sensor_metadata:
                sensor.battery_level = reading.sensor_metadata['battery_level']
            if 'rssi_dbm' in reading.sensor_metadata:
                sensor.signal_strength = reading.sensor_metadata['rssi_dbm']
        
        return reading
    
    @classmethod
    def get_by_sensor(cls, sensor_id, limit=100, offset=0):
        """
        Busca leituras de um sensor específico
        
        Args:
            sensor_id: ID do sensor
            limit: Número máximo de resultados
            offset: Offset para paginação
        
        Returns:
            list: Lista de leituras
        """
        return cls.query.filter_by(sensor_id=sensor_id)\
            .order_by(cls.timestamp.desc())\
            .limit(limit)\
            .offset(offset)\
            .all()
    
    @classmethod
    def get_by_date_range(cls, start_date, end_date, sensor_id=None):
        """
        Busca leituras em um intervalo de datas
        
        Args:
            start_date: Data inicial
            end_date: Data final
            sensor_id: ID do sensor (opcional)
        
        Returns:
            Query: Query de leituras
        """
        query = cls.query.filter(
            cls.timestamp >= start_date,
            cls.timestamp <= end_date
        )
        
        if sensor_id:
            query = query.filter_by(sensor_id=sensor_id)
        
        return query.order_by(cls.timestamp.desc())
    
    @classmethod
    def count_detections(cls, start_date, end_date, sensor_id=None):
        """
        Conta detecções (activity=1) em um período
        
        Args:
            start_date: Data inicial
            end_date: Data final
            sensor_id: ID do sensor (opcional)
        
        Returns:
            int: Número de detecções
        """
        query = cls.query.filter(
            cls.timestamp >= start_date,
            cls.timestamp <= end_date,
            cls.activity == 1
        )
        
        if sensor_id:
            query = query.filter_by(sensor_id=sensor_id)
        
        return query.count()
    
    @classmethod
    def get_hourly_detections(cls, date, sensor_id=None):
        """
        Agrupa detecções por hora em uma data específica
        
        Args:
            date: Data para análise
            sensor_id: ID do sensor (opcional)
        
        Returns:
            list: Lista de tuplas (hora, contagem)
        """
        from sqlalchemy import func, extract
        from datetime import datetime, timedelta
        
        start = datetime.combine(date, datetime.min.time())
        end = start + timedelta(days=1)
        
        query = db.session.query(
            extract('hour', cls.timestamp).label('hour'),
            func.count(cls.id).label('count')
        ).filter(
            cls.timestamp >= start,
            cls.timestamp < end,
            cls.activity == 1
        )
        
        if sensor_id:
            query = query.filter_by(sensor_id=sensor_id)
        
        return query.group_by('hour').order_by('hour').all()
