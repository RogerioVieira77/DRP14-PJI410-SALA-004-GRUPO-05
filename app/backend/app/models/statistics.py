"""
Statistics Model
Representa estatísticas agregadas do sistema
"""

from datetime import datetime, date
from app import db


class Statistics(db.Model):
    """
    Modelo de Estatísticas
    
    Armazena estatísticas agregadas por hora/dia:
    - Entradas
    - Saídas
    - Total de pessoas no parque
    - Ocupação média
    """
    __tablename__ = 'statistics'
    
    # Campos principais
    id = db.Column(db.Integer, primary_key=True)
    
    # Data e hora
    date = db.Column(db.Date, nullable=False, index=True)
    hour = db.Column(db.SmallInteger, nullable=False, index=True)  # 0-23
    
    # Estatísticas de fluxo
    entries = db.Column(db.Integer, default=0, nullable=False)  # Entradas
    exits = db.Column(db.Integer, default=0, nullable=False)    # Saídas
    
    # Ocupação
    current_people = db.Column(db.Integer, default=0, nullable=False)  # Pessoas no momento
    avg_people = db.Column(db.Float, default=0.0)  # Média de pessoas na hora
    max_people = db.Column(db.Integer, default=0)  # Pico de pessoas
    min_people = db.Column(db.Integer, default=0)  # Mínimo de pessoas
    
    # Capacidade
    capacity_percentage = db.Column(db.Float, default=0.0)  # % de ocupação
    
    # Sensor específico (opcional - para estatísticas por sensor)
    sensor_id = db.Column(
        db.Integer,
        db.ForeignKey('sensors.id', ondelete='SET NULL'),
        nullable=True,
        index=True
    )
    
    # Metadados
    total_readings = db.Column(db.Integer, default=0)  # Total de leituras processadas
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Índices compostos e constraint única
    __table_args__ = (
        db.UniqueConstraint('date', 'hour', 'sensor_id', name='uix_date_hour_sensor'),
        db.Index('idx_date_hour', 'date', 'hour'),
        db.Index('idx_date_sensor', 'date', 'sensor_id'),
    )
    
    def __repr__(self):
        return f'<Statistics {self.date} {self.hour:02d}:00 entries={self.entries}>'
    
    def to_dict(self, include_sensor=False):
        """
        Converte as estatísticas para dicionário
        
        Returns:
            dict: Representação das estatísticas
        """
        data = {
            'id': self.id,
            'date': self.date.isoformat(),
            'hour': self.hour,
            'entries': self.entries,
            'exits': self.exits,
            'current_people': self.current_people,
            'avg_people': self.avg_people,
            'max_people': self.max_people,
            'min_people': self.min_people,
            'capacity_percentage': self.capacity_percentage,
            'sensor_id': self.sensor_id,
            'total_readings': self.total_readings,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_sensor and self.sensor:
            data['sensor'] = {
                'serial_number': self.sensor.serial_number,
                'location': self.sensor.location
            }
        
        return data
    
    @classmethod
    def get_or_create(cls, date_obj, hour, sensor_id=None):
        """
        Busca ou cria estatística para uma data/hora específica
        
        Args:
            date_obj: Objeto date
            hour: Hora (0-23)
            sensor_id: ID do sensor (opcional)
        
        Returns:
            Statistics: Instância de estatística
        """
        stat = cls.query.filter_by(
            date=date_obj,
            hour=hour,
            sensor_id=sensor_id
        ).first()
        
        if not stat:
            stat = cls(
                date=date_obj,
                hour=hour,
                sensor_id=sensor_id
            )
            db.session.add(stat)
        
        return stat
    
    @classmethod
    def get_by_date(cls, date_obj, sensor_id=None):
        """
        Busca estatísticas de um dia específico
        
        Args:
            date_obj: Objeto date
            sensor_id: ID do sensor (opcional)
        
        Returns:
            list: Lista de estatísticas (24 horas)
        """
        query = cls.query.filter_by(date=date_obj)
        
        if sensor_id:
            query = query.filter_by(sensor_id=sensor_id)
        
        return query.order_by(cls.hour).all()
    
    @classmethod
    def get_by_date_range(cls, start_date, end_date, sensor_id=None):
        """
        Busca estatísticas em um intervalo de datas
        
        Args:
            start_date: Data inicial
            end_date: Data final
            sensor_id: ID do sensor (opcional)
        
        Returns:
            list: Lista de estatísticas
        """
        query = cls.query.filter(
            cls.date >= start_date,
            cls.date <= end_date
        )
        
        if sensor_id:
            query = query.filter_by(sensor_id=sensor_id)
        
        return query.order_by(cls.date, cls.hour).all()
    
    @classmethod
    def aggregate_daily(cls, date_obj, sensor_id=None):
        """
        Agrega estatísticas de um dia completo
        
        Args:
            date_obj: Objeto date
            sensor_id: ID do sensor (opcional)
        
        Returns:
            dict: Estatísticas agregadas do dia
        """
        from sqlalchemy import func
        
        query = db.session.query(
            func.sum(cls.entries).label('total_entries'),
            func.sum(cls.exits).label('total_exits'),
            func.avg(cls.avg_people).label('avg_people'),
            func.max(cls.max_people).label('peak_people'),
            func.avg(cls.capacity_percentage).label('avg_capacity')
        ).filter_by(date=date_obj)
        
        if sensor_id:
            query = query.filter_by(sensor_id=sensor_id)
        
        result = query.first()
        
        return {
            'date': date_obj.isoformat(),
            'total_entries': result.total_entries or 0,
            'total_exits': result.total_exits or 0,
            'avg_people': round(result.avg_people or 0, 2),
            'peak_people': result.peak_people or 0,
            'avg_capacity': round(result.avg_capacity or 0, 2)
        }
    
    @classmethod
    def get_busiest_hours(cls, start_date, end_date, limit=10):
        """
        Retorna os horários mais movimentados
        
        Args:
            start_date: Data inicial
            end_date: Data final
            limit: Número de resultados
        
        Returns:
            list: Lista de horários ordenados por movimento
        """
        from sqlalchemy import func
        
        results = db.session.query(
            cls.hour,
            func.avg(cls.entries).label('avg_entries')
        ).filter(
            cls.date >= start_date,
            cls.date <= end_date
        ).group_by(cls.hour)\
         .order_by(func.avg(cls.entries).desc())\
         .limit(limit)\
         .all()
        
        return [
            {
                'hour': hour,
                'avg_entries': round(avg_entries, 2)
            }
            for hour, avg_entries in results
        ]
    
    def update_from_readings(self, readings):
        """
        Atualiza estatísticas a partir de leituras
        
        Args:
            readings: Lista de leituras (Reading objects)
        """
        if not readings:
            return
        
        # Contar entradas (detecções)
        detections = sum(1 for r in readings if r.activity == 1)
        self.entries += detections
        self.total_readings += len(readings)
        
        # Atualizar timestamp
        self.updated_at = datetime.utcnow()
