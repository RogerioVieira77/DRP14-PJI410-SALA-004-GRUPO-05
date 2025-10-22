"""
Sensor Model
Representa um sensor IoT no sistema
"""

from datetime import datetime
from app import db


class Sensor(db.Model):
    """
    Modelo de Sensor IoT
    
    Representa os dispositivos físicos instalados no parque:
    - LoRa
    - ZigBee
    - Sigfox
    - RFID
    """
    __tablename__ = 'sensors'
    
    # Campos principais
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    protocol = db.Column(db.String(20), nullable=False, index=True)  # LoRa, ZigBee, Sigfox, RFID
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    # Status
    status = db.Column(
        db.Enum('active', 'inactive', 'maintenance', 'error', name='sensor_status'),
        default='active',
        nullable=False,
        index=True
    )
    
    # Metadados do protocolo (JSON)
    protocol_config = db.Column(db.JSON)  # Ex: spreading_factor, frequency, etc.
    
    # Informações de hardware
    firmware_version = db.Column(db.String(20))
    battery_level = db.Column(db.Float)  # Porcentagem (0-100)
    signal_strength = db.Column(db.Float)  # RSSI em dBm
    
    # Estatísticas
    total_readings = db.Column(db.Integer, default=0)
    last_reading_at = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relacionamentos
    readings = db.relationship(
        'Reading',
        backref='sensor',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    alerts = db.relationship(
        'Alert',
        backref='sensor',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    # Índices compostos
    __table_args__ = (
        db.Index('idx_protocol_status', 'protocol', 'status'),
        db.Index('idx_status_created', 'status', 'created_at'),
    )
    
    def __repr__(self):
        return f'<Sensor {self.serial_number} ({self.protocol})>'
    
    def to_dict(self, include_stats=False):
        """
        Converte o sensor para dicionário
        
        Args:
            include_stats: Incluir estatísticas de leituras
        
        Returns:
            dict: Representação do sensor
        """
        data = {
            'id': self.id,
            'serial_number': self.serial_number,
            'protocol': self.protocol,
            'location': self.location,
            'description': self.description,
            'status': self.status,
            'protocol_config': self.protocol_config,
            'firmware_version': self.firmware_version,
            'battery_level': self.battery_level,
            'signal_strength': self.signal_strength,
            'total_readings': self.total_readings,
            'last_reading_at': self.last_reading_at.isoformat() if self.last_reading_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_stats:
            data['stats'] = self.get_statistics()
        
        return data
    
    def get_statistics(self, hours=24):
        """
        Obtém estatísticas do sensor
        
        Args:
            hours: Número de horas para calcular estatísticas
        
        Returns:
            dict: Estatísticas do sensor
        """
        from datetime import timedelta
        from sqlalchemy import func
        from app.models.reading import Reading
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        # Contar leituras recentes
        recent_readings = Reading.query.filter(
            Reading.sensor_id == self.id,
            Reading.timestamp >= cutoff_time
        ).count()
        
        # Contar detecções (activity = 1)
        recent_detections = Reading.query.filter(
            Reading.sensor_id == self.id,
            Reading.timestamp >= cutoff_time,
            Reading.activity == 1
        ).count()
        
        # Média do battery_level
        avg_battery = db.session.query(
            func.avg(Reading.metadata['battery_level'].astext.cast(db.Float))
        ).filter(
            Reading.sensor_id == self.id,
            Reading.timestamp >= cutoff_time
        ).scalar()
        
        return {
            'readings_last_24h': recent_readings,
            'detections_last_24h': recent_detections,
            'avg_battery_level': round(avg_battery, 2) if avg_battery else None,
            'is_online': (
                self.last_reading_at and
                (datetime.utcnow() - self.last_reading_at).seconds < 300  # 5 minutos
            ),
            'uptime_percentage': self._calculate_uptime(hours)
        }
    
    def _calculate_uptime(self, hours=24):
        """Calcula porcentagem de uptime baseado nas leituras"""
        from datetime import timedelta
        from app.models.reading import Reading
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        # Contar intervalos de 5 minutos com pelo menos 1 leitura
        total_intervals = hours * 12  # 12 intervalos de 5 min por hora
        
        readings_count = Reading.query.filter(
            Reading.sensor_id == self.id,
            Reading.timestamp >= cutoff_time
        ).count()
        
        if readings_count == 0:
            return 0.0
        
        # Estimar uptime baseado na quantidade de leituras
        # (assumindo leituras a cada 2 segundos)
        expected_readings = hours * 60 * 30  # 30 leituras por minuto
        uptime = min((readings_count / expected_readings) * 100, 100)
        
        return round(uptime, 2)
    
    def update_from_dict(self, data):
        """
        Atualiza campos do sensor a partir de um dicionário
        
        Args:
            data: Dicionário com campos a atualizar
        """
        updateable_fields = [
            'location', 'description', 'status', 'protocol_config',
            'firmware_version', 'battery_level', 'signal_strength'
        ]
        
        for field in updateable_fields:
            if field in data:
                setattr(self, field, data[field])
        
        self.updated_at = datetime.utcnow()
    
    @classmethod
    def get_by_serial(cls, serial_number):
        """Busca sensor pelo serial number"""
        return cls.query.filter_by(serial_number=serial_number).first()
    
    @classmethod
    def get_active_sensors(cls):
        """Retorna todos os sensores ativos"""
        return cls.query.filter_by(status='active').all()
    
    @classmethod
    def get_by_protocol(cls, protocol):
        """Retorna sensores de um protocolo específico"""
        return cls.query.filter_by(protocol=protocol).all()
