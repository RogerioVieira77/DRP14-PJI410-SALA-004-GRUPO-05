"""
Alert Model
Representa um alerta do sistema
"""

from datetime import datetime
from app import db


class Alert(db.Model):
    """
    Modelo de Alerta
    
    Armazena alertas gerados pelo sistema:
    - Capacidade do parque
    - Problemas com sensores
    - Anomalias detectadas
    """
    __tablename__ = 'alerts'
    
    # Campos principais
    id = db.Column(db.Integer, primary_key=True)
    alert_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    
    # Relacionamento com sensor (opcional)
    sensor_id = db.Column(
        db.Integer,
        db.ForeignKey('sensors.id', ondelete='SET NULL'),
        nullable=True,
        index=True
    )
    
    # Tipo e severidade
    alert_type = db.Column(
        db.Enum('capacity', 'sensor_offline', 'battery_low', 'anomaly', 'system', name='alert_type'),
        nullable=False,
        index=True
    )
    
    severity = db.Column(
        db.Enum('low', 'medium', 'high', 'critical', name='alert_severity'),
        nullable=False,
        index=True
    )
    
    # Mensagem e dados
    message = db.Column(db.Text, nullable=False)
    data = db.Column(db.JSON)  # Dados adicionais do alerta
    
    # Status
    status = db.Column(
        db.Enum('open', 'acknowledged', 'resolved', 'dismissed', name='alert_status'),
        default='open',
        nullable=False,
        index=True
    )
    
    # Gateway que gerou o alerta
    gateway_id = db.Column(db.String(50), index=True)
    
    # Timestamps
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    acknowledged_at = db.Column(db.DateTime)
    resolved_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Índices compostos
    __table_args__ = (
        db.Index('idx_type_status', 'alert_type', 'status'),
        db.Index('idx_severity_timestamp', 'severity', 'timestamp'),
        db.Index('idx_sensor_type', 'sensor_id', 'alert_type'),
    )
    
    def __repr__(self):
        return f'<Alert {self.alert_id} type={self.alert_type} severity={self.severity}>'
    
    def to_dict(self, include_sensor=False):
        """
        Converte o alerta para dicionário
        
        Args:
            include_sensor: Incluir dados do sensor
        
        Returns:
            dict: Representação do alerta
        """
        data = {
            'id': self.id,
            'alert_id': self.alert_id,
            'sensor_id': self.sensor_id,
            'alert_type': self.alert_type,
            'severity': self.severity,
            'message': self.message,
            'data': self.data,
            'status': self.status,
            'gateway_id': self.gateway_id,
            'timestamp': self.timestamp.isoformat(),
            'acknowledged_at': self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
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
        Cria um alerta a partir de mensagem MQTT
        
        Args:
            mqtt_data: Dicionário com dados da mensagem MQTT
        
        Returns:
            Alert: Nova instância de alerta
        """
        from app.models.sensor import Sensor
        
        # Buscar sensor se especificado
        sensor_id = None
        if 'sensor' in mqtt_data.get('data', {}):
            sensor = Sensor.get_by_serial(mqtt_data['data']['sensor'])
            if sensor:
                sensor_id = sensor.id
        
        alert = cls(
            alert_id=mqtt_data.get('alert_id'),
            sensor_id=sensor_id,
            alert_type=mqtt_data.get('type', 'system'),
            severity=mqtt_data.get('severity', 'medium'),
            message=mqtt_data.get('message', 'Alert'),
            data=mqtt_data.get('data', {}),
            gateway_id=mqtt_data.get('gateway_id'),
            timestamp=datetime.fromisoformat(mqtt_data['timestamp'].replace('Z', '+00:00'))
        )
        
        return alert
    
    def acknowledge(self):
        """Marca alerta como reconhecido"""
        self.status = 'acknowledged'
        self.acknowledged_at = datetime.utcnow()
    
    def resolve(self):
        """Marca alerta como resolvido"""
        self.status = 'resolved'
        self.resolved_at = datetime.utcnow()
    
    def dismiss(self):
        """Descarta o alerta"""
        self.status = 'dismissed'
    
    @classmethod
    def get_open_alerts(cls, severity=None):
        """
        Busca alertas abertos
        
        Args:
            severity: Filtrar por severidade (opcional)
        
        Returns:
            Query: Query de alertas
        """
        query = cls.query.filter_by(status='open')
        
        if severity:
            query = query.filter_by(severity=severity)
        
        return query.order_by(cls.timestamp.desc())
    
    @classmethod
    def get_by_sensor(cls, sensor_id, status=None):
        """
        Busca alertas de um sensor
        
        Args:
            sensor_id: ID do sensor
            status: Filtrar por status (opcional)
        
        Returns:
            Query: Query de alertas
        """
        query = cls.query.filter_by(sensor_id=sensor_id)
        
        if status:
            query = query.filter_by(status=status)
        
        return query.order_by(cls.timestamp.desc())
    
    @classmethod
    def get_by_date_range(cls, start_date, end_date, alert_type=None):
        """
        Busca alertas em um intervalo de datas
        
        Args:
            start_date: Data inicial
            end_date: Data final
            alert_type: Tipo de alerta (opcional)
        
        Returns:
            Query: Query de alertas
        """
        query = cls.query.filter(
            cls.timestamp >= start_date,
            cls.timestamp <= end_date
        )
        
        if alert_type:
            query = query.filter_by(alert_type=alert_type)
        
        return query.order_by(cls.timestamp.desc())
    
    @classmethod
    def count_by_type(cls, start_date=None, end_date=None):
        """
        Conta alertas por tipo
        
        Args:
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
        
        Returns:
            dict: Contagem por tipo
        """
        from sqlalchemy import func
        
        query = db.session.query(
            cls.alert_type,
            func.count(cls.id).label('count')
        )
        
        if start_date:
            query = query.filter(cls.timestamp >= start_date)
        if end_date:
            query = query.filter(cls.timestamp <= end_date)
        
        results = query.group_by(cls.alert_type).all()
        
        return {alert_type: count for alert_type, count in results}
