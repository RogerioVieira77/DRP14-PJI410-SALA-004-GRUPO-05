"""
Statistics Routes
Endpoints para estatísticas e relatórios
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.reading import Reading
from app.models.sensor import Sensor
from app.models.statistics import Statistics
from datetime import datetime, timedelta
from sqlalchemy import func

bp = Blueprint('statistics', __name__)


@bp.route('/overview', methods=['GET'])
def get_overview():
    """
    Visão geral do sistema
    Retorna estatísticas gerais sobre sensores e leituras
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
    
    return jsonify({
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
    }), 200


@bp.route('/activity', methods=['GET'])
def get_activity_stats():
    """
    Estatísticas de atividade
    Query params:
    - period: day, week, month (default: day)
    - sensor_id: filtrar por sensor específico
    """
    period = request.args.get('period', 'day')
    sensor_id = request.args.get('sensor_id', type=int)
    
    # Definir período
    if period == 'day':
        start_date = datetime.utcnow() - timedelta(days=1)
        interval = timedelta(hours=1)
    elif period == 'week':
        start_date = datetime.utcnow() - timedelta(weeks=1)
        interval = timedelta(days=1)
    elif period == 'month':
        start_date = datetime.utcnow() - timedelta(days=30)
        interval = timedelta(days=1)
    else:
        return jsonify({'error': 'Período inválido. Use: day, week, month'}), 400
    
    # Query base
    query = Reading.query.filter(Reading.timestamp >= start_date)
    
    if sensor_id:
        query = query.filter_by(sensor_id=sensor_id)
    
    # Contar atividades
    total_detections = query.filter(Reading.activity == 1).count()
    total_readings = query.count()
    
    # Atividade por hora/dia
    readings = query.all()
    
    # Agrupar por intervalo
    activity_timeline = {}
    current = start_date
    end = datetime.utcnow()
    
    while current <= end:
        next_interval = current + interval
        count = len([r for r in readings if current <= r.timestamp < next_interval and r.activity == 1])
        activity_timeline[current.isoformat()] = count
        current = next_interval
    
    return jsonify({
        'period': period,
        'start_date': start_date.isoformat(),
        'end_date': datetime.utcnow().isoformat(),
        'total_detections': total_detections,
        'total_readings': total_readings,
        'detection_rate': round((total_detections / total_readings * 100), 2) if total_readings > 0 else 0,
        'timeline': activity_timeline
    }), 200


@bp.route('/sensors', methods=['GET'])
def get_sensors_stats():
    """
    Estatísticas por sensor
    Retorna estatísticas individuais de cada sensor
    """
    sensors = Sensor.query.all()
    
    stats = []
    for sensor in sensors:
        # Leituras totais
        total_readings = Reading.query.filter_by(sensor_id=sensor.id).count()
        
        # Detecções (activity = 1)
        detections = Reading.query.filter_by(
            sensor_id=sensor.id,
            activity=1
        ).count()
        
        # Última leitura
        last_reading = Reading.query.filter_by(sensor_id=sensor.id)\
            .order_by(Reading.timestamp.desc()).first()
        
        # Média de bateria
        avg_battery = db.session.query(func.avg(Reading.battery_level))\
            .filter(Reading.sensor_id == sensor.id)\
            .scalar()
        
        stats.append({
            'sensor_id': sensor.id,
            'serial_number': sensor.serial_number,
            'protocol': sensor.protocol,
            'location': sensor.location,
            'status': sensor.status,
            'total_readings': total_readings,
            'total_detections': detections,
            'detection_rate': round((detections / total_readings * 100), 2) if total_readings > 0 else 0,
            'last_reading': last_reading.timestamp.isoformat() if last_reading else None,
            'avg_battery_level': round(avg_battery, 2) if avg_battery else None,
            'current_battery_level': sensor.battery_level
        })
    
    return jsonify({
        'count': len(stats),
        'sensors': stats
    }), 200


@bp.route('/capacity', methods=['GET'])
def get_capacity_stats():
    """
    Estatísticas de capacidade do parque
    Calcula ocupação atual baseada nas detecções
    """
    # Capacidade máxima (exemplo - ajustar conforme necessário)
    max_capacity = 5000
    
    # Calcular ocupação nas últimas 24h
    yesterday = datetime.utcnow() - timedelta(days=1)
    
    # Entradas (detecções nos sensores de entrada)
    entries_sensors = Sensor.query.filter(
        Sensor.location.ilike('%entrada%')
    ).all()
    
    total_entries = 0
    for sensor in entries_sensors:
        entries = Reading.query.filter(
            Reading.sensor_id == sensor.id,
            Reading.timestamp >= yesterday,
            Reading.activity == 1
        ).count()
        total_entries += entries
    
    # Saídas (detecções nos sensores de saída)
    exits_sensors = Sensor.query.filter(
        Sensor.location.ilike('%saída%')
    ).all()
    
    total_exits = 0
    for sensor in exits_sensors:
        exits = Reading.query.filter(
            Reading.sensor_id == sensor.id,
            Reading.timestamp >= yesterday,
            Reading.activity == 1
        ).count()
        total_exits += exits
    
    # Ocupação atual estimada
    current_occupation = max(0, total_entries - total_exits)
    occupation_percentage = round((current_occupation / max_capacity * 100), 2)
    
    # Determinar status
    if occupation_percentage < 70:
        status = 'normal'
    elif occupation_percentage < 90:
        status = 'alert'
    else:
        status = 'critical'
    
    return jsonify({
        'max_capacity': max_capacity,
        'current_occupation': current_occupation,
        'occupation_percentage': occupation_percentage,
        'status': status,
        'entries_24h': total_entries,
        'exits_24h': total_exits,
        'timestamp': datetime.utcnow().isoformat()
    }), 200


@bp.route('/history', methods=['GET'])
def get_historical_stats():
    """
    Estatísticas históricas
    Query params:
    - start_date: data inicial (ISO format)
    - end_date: data final (ISO format)
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date or not end_date:
        return jsonify({'error': 'start_date e end_date são obrigatórios'}), 400
    
    try:
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
    except ValueError:
        return jsonify({'error': 'Formato de data inválido. Use ISO format.'}), 400
    
    # Buscar estatísticas salvas (se existirem)
    saved_stats = Statistics.query.filter(
        Statistics.date >= start.date(),
        Statistics.date <= end.date()
    ).all()
    
    return jsonify({
        'start_date': start.isoformat(),
        'end_date': end.isoformat(),
        'statistics': [{
            'date': stat.date.isoformat(),
            'total_detections': stat.total_detections,
            'total_entries': stat.total_entries,
            'total_exits': stat.total_exits,
            'peak_occupation': stat.peak_occupation,
            'avg_occupation': stat.avg_occupation
        } for stat in saved_stats]
    }), 200


@bp.route('/export', methods=['GET'])
@jwt_required()
def export_stats():
    """
    Exportar estatísticas (CSV ou JSON)
    Query params:
    - format: csv ou json (default: json)
    - period: day, week, month
    """
    format_type = request.args.get('format', 'json')
    period = request.args.get('period', 'day')
    
    # Buscar dados conforme período
    if period == 'day':
        start_date = datetime.utcnow() - timedelta(days=1)
    elif period == 'week':
        start_date = datetime.utcnow() - timedelta(weeks=1)
    elif period == 'month':
        start_date = datetime.utcnow() - timedelta(days=30)
    else:
        return jsonify({'error': 'Período inválido'}), 400
    
    readings = Reading.query.filter(Reading.timestamp >= start_date).all()
    
    if format_type == 'json':
        return jsonify({
            'period': period,
            'start_date': start_date.isoformat(),
            'end_date': datetime.utcnow().isoformat(),
            'readings': [{
                'sensor_id': r.sensor_id,
                'activity': r.activity,
                'timestamp': r.timestamp.isoformat()
            } for r in readings]
        }), 200
    
    # TODO: Implementar exportação CSV
    return jsonify({'error': 'Formato CSV ainda não implementado'}), 501
