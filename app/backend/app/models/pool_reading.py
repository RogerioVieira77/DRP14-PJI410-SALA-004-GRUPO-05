"""
Modelo de dados para leituras dos sensores da piscina.
Armazena temperatura da água, temperatura ambiente e qualidade da água.
"""
from datetime import datetime, date, time
from app import db
from sqlalchemy import Enum
import enum


class SensorType(enum.Enum):
    """Tipos de sensores da piscina."""
    WATER_TEMP = 'water_temp'
    AMBIENT_TEMP = 'ambient_temp'
    WATER_QUALITY = 'water_quality'


class WaterQuality(enum.Enum):
    """Classificação da qualidade da água."""
    OTIMA = 'Ótima'
    BOA = 'Boa'
    REGULAR = 'Regular'
    IMPROPRIA = 'Imprópria'


class PoolReading(db.Model):
    """
    Modelo para armazenar leituras dos sensores de monitoramento da piscina.
    
    Attributes:
        id: Identificador único da leitura
        sensor_type: Tipo do sensor (water_temp, ambient_temp, water_quality)
        reading_date: Data da leitura
        reading_time: Hora da leitura
        temperature: Temperatura medida (Celsius) - para sensores de temperatura
        water_quality: Qualidade da água - apenas para sensor water_quality
        created_at: Timestamp de criação do registro
        updated_at: Timestamp da última atualização
    """
    
    __tablename__ = 'pool_readings'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    
    # Tipo do sensor - usando String para compatibilidade com valores do banco
    sensor_type = db.Column(
        db.String(20),
        nullable=False,
        index=True
    )
    
    # Data e hora da leitura
    reading_date = db.Column(db.Date, nullable=False, index=True)
    reading_time = db.Column(db.Time, nullable=False)
    
    # Valores das leituras
    temperature = db.Column(
        db.Numeric(5, 2),
        nullable=True,
        comment='Temperatura em Celsius (20-40°C)'
    )
    
    water_quality = db.Column(
        db.String(20),
        nullable=True
    )
    
    # Metadados
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True
    )
    
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    def __repr__(self):
        """Representação string do objeto."""
        if self.sensor_type in ['water_temp', 'ambient_temp']:
            return f'<PoolReading {self.sensor_type} {self.temperature}°C @ {self.reading_date} {self.reading_time}>'
        else:
            return f'<PoolReading {self.sensor_type} {self.water_quality} @ {self.reading_date} {self.reading_time}>'
    
    def to_dict(self):
        """
        Converte o objeto para dicionário.
        
        Returns:
            dict: Representação em dicionário da leitura
        """
        return {
            'id': self.id,
            'sensor_type': self.sensor_type,
            'reading_date': self.reading_date.isoformat() if self.reading_date else None,
            'reading_time': self.reading_time.strftime('%H:%M:%S') if self.reading_time else None,
            'temperature': float(self.temperature) if self.temperature else None,
            'water_quality': self.water_quality if self.water_quality else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def needs_alert(water_quality_value):
        """
        Verifica se uma leitura de qualidade da água requer alerta.
        
        Args:
            water_quality_value: Valor da qualidade da água
            
        Returns:
            bool: True se requer alerta (Regular ou Imprópria)
        """
        if isinstance(water_quality_value, str):
            return water_quality_value in ['Regular', 'Imprópria']
        return False
    
    @staticmethod
    def get_alert_level(water_quality_value):
        """
        Retorna o nível de alerta para uma qualidade de água.
        
        Args:
            water_quality_value: Valor da qualidade da água
            
        Returns:
            str: 'warning' para Regular, 'danger' para Imprópria, None caso contrário
        """
        if isinstance(water_quality_value, str):
            quality = water_quality_value
        else:
            quality = str(water_quality_value)
            
        if quality == 'Regular':
            return 'warning'
        elif quality == 'Imprópria':
            return 'danger'
        return None
