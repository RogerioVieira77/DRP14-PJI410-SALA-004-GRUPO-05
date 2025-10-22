"""
Service de Estatísticas
Lógica de negócio relacionada a estatísticas e relatórios
"""

from datetime import datetime, timedelta
from typing import Dict, Any
from sqlalchemy import func
from app import db
from app.models.reading import Reading
from app.models.sensor import Sensor


class StatisticsService:
    """Serviço de estatísticas e relatórios"""
    
    @staticmethod
    def get_overview() -> Dict[str, Any]:
        """
        Obter visão geral do sistema
        
        Returns:
            Dict: Estatísticas gerais
        """
        # Contar sensores por status
        sensors_by_status = db.session.query(
            Sensor.status, 
            func.count(Sensor.id)
        ).group_by(Sensor.status).all()
        
        # Contar sensores por protocolo
        sensors_by_protocol = db.session.query(
            Sensor.protocol,
            func.count(Sensor.id)
        ).group_by(Sensor.protocol).all()
        
        # Total de leituras
        total_readings = Reading.query.count()
        
        # Leituras nas últimas 24h
        yesterday = datetime.utcnow() - timedelta(days=1)
        readings_24h = Reading.query.filter(Reading.timestamp >= yesterday).count()
        
        # Leituras com atividade nas últimas 24h
        activity_24h = Reading.query.filter(
            Reading.timestamp >= yesterday,
            Reading.activity == 1
        ).count()
        
        return {
            'sensors': {
                'total': Sensor.query.count(),
                'by_status': {status: count for status, count in sensors_by_status},
                'by_protocol': {protocol: count for protocol, count in sensors_by_protocol}
            },
            'readings': {
                'total': total_readings,
                'last_24h': readings_24h,
                'activity_24h': activity_24h
            },
            'timestamp': datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def get_activity_stats(
        period: str = 'day',
        sensor_id: int = None
    ) -> Dict[str, Any]:
        """
        Obter estatísticas de atividade
        
        Args:
            period: Período (day, week, month)
            sensor_id: ID do sensor (opcional)
            
        Returns:
            Dict: Estatísticas de atividade
        """
        # Definir período
        period_map = {
            'day': (timedelta(days=1), timedelta(hours=1)),
            'week': (timedelta(weeks=1), timedelta(days=1)),
            'month': (timedelta(days=30), timedelta(days=1))
        }
        
        if period not in period_map:
            raise ValueError('Período inválido. Use: day, week, month')
        
        time_range, interval = period_map[period]
        start_date = datetime.utcnow() - time_range
        
        # Query base
        query = Reading.query.filter(Reading.timestamp >= start_date)
        
        if sensor_id:
            query = query.filter_by(sensor_id=sensor_id)
        
        # Contar atividades
        total_detections = query.filter(Reading.activity == 1).count()
        total_readings = query.count()
        
        # Atividade por intervalo
        readings = query.all()
        
        activity_timeline = {}
        current = start_date
        end = datetime.utcnow()
        
        while current <= end:
            next_interval = current + interval
            count = len([
                r for r in readings 
                if current <= r.timestamp < next_interval and r.activity == 1
            ])
            activity_timeline[current.isoformat()] = count
            current = next_interval
        
        return {
            'period': period,
            'start_date': start_date.isoformat(),
            'end_date': datetime.utcnow().isoformat(),
            'total_detections': total_detections,
            'total_readings': total_readings,
            'detection_rate': round(
                (total_detections / total_readings * 100), 2
            ) if total_readings > 0 else 0,
            'timeline': activity_timeline
        }
    
    @staticmethod
    def get_sensors_stats() -> Dict[str, Any]:
        """
        Obter estatísticas por sensor
        
        Returns:
            Dict: Estatísticas individuais dos sensores
        """
        sensors = Sensor.query.all()
        
        stats = []
        for sensor in sensors:
            # Leituras totais
            total_readings = Reading.query.filter_by(sensor_id=sensor.id).count()
            
            # Detecções
            detections = Reading.query.filter_by(
                sensor_id=sensor.id,
                activity=1
            ).count()
            
            # Última leitura
            last_reading = Reading.query.filter_by(sensor_id=sensor.id)\
                .order_by(Reading.timestamp.desc()).first()
            
            stats.append({
                'sensor_id': sensor.id,
                'serial_number': sensor.serial_number,
                'protocol': sensor.protocol,
                'location': sensor.location,
                'status': sensor.status,
                'total_readings': total_readings,
                'total_detections': detections,
                'detection_rate': round(
                    (detections / total_readings * 100), 2
                ) if total_readings > 0 else 0,
                'last_reading': last_reading.timestamp.isoformat() if last_reading else None,
                'current_battery_level': sensor.battery_level
            })
        
        return {
            'count': len(stats),
            'sensors': stats
        }
    
    @staticmethod
    def get_capacity_stats(max_capacity: int = 5000) -> Dict[str, Any]:
        """
        Obter estatísticas de capacidade
        
        Args:
            max_capacity: Capacidade máxima do parque
            
        Returns:
            Dict: Estatísticas de capacidade
        """
        yesterday = datetime.utcnow() - timedelta(days=1)
        
        # Entradas
        entries_sensors = Sensor.query.filter(
            Sensor.location.ilike('%entrada%')
        ).all()
        
        total_entries = sum([
            Reading.query.filter(
                Reading.sensor_id == sensor.id,
                Reading.timestamp >= yesterday,
                Reading.activity == 1
            ).count()
            for sensor in entries_sensors
        ])
        
        # Saídas
        exits_sensors = Sensor.query.filter(
            Sensor.location.ilike('%saída%')
        ).all()
        
        total_exits = sum([
            Reading.query.filter(
                Reading.sensor_id == sensor.id,
                Reading.timestamp >= yesterday,
                Reading.activity == 1
            ).count()
            for sensor in exits_sensors
        ])
        
        # Ocupação estimada
        current_occupation = max(0, total_entries - total_exits)
        occupation_percentage = round((current_occupation / max_capacity * 100), 2)
        
        # Status
        if occupation_percentage < 70:
            status = 'normal'
        elif occupation_percentage < 90:
            status = 'alert'
        else:
            status = 'critical'
        
        return {
            'max_capacity': max_capacity,
            'current_occupation': current_occupation,
            'occupation_percentage': occupation_percentage,
            'status': status,
            'entries_24h': total_entries,
            'exits_24h': total_exits,
            'timestamp': datetime.utcnow().isoformat()
        }
