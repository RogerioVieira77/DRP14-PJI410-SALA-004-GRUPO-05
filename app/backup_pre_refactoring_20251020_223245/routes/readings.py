"""
Readings Routes
Endpoints para leituras dos sensores
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.reading import Reading
from app.models.sensor import Sensor
from datetime import datetime, timedelta

bp = Blueprint('readings', __name__)


@bp.route('', methods=['GET'])
def list_readings():
    """
    Listar leituras
    Query params:
    - sensor_id: filtrar por sensor
    - start_date: data inicial (ISO format)
    - end_date: data final (ISO format)
    - limit: número máximo de resultados (default: 100)
    """
    sensor_id = request.args.get('sensor_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    limit = request.args.get('limit', default=100, type=int)
    
    query = Reading.query
    
    if sensor_id:
        query = query.filter_by(sensor_id=sensor_id)
    
    if start_date:
        try:
            start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            query = query.filter(Reading.timestamp >= start)
        except ValueError:
            return jsonify({'error': 'Formato de start_date inválido. Use ISO format.'}), 400
    
    if end_date:
        try:
            end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            query = query.filter(Reading.timestamp <= end)
        except ValueError:
            return jsonify({'error': 'Formato de end_date inválido. Use ISO format.'}), 400
    
    # Ordenar por timestamp decrescente (mais recentes primeiro)
    readings = query.order_by(Reading.timestamp.desc()).limit(limit).all()
    
    return jsonify({
        'count': len(readings),
        'readings': [{
            'id': reading.id,
            'sensor_id': reading.sensor_id,
            'sensor_serial': reading.sensor.serial_number if reading.sensor else None,
            'activity': reading.activity,
            'battery_level': reading.battery_level,
            'signal_strength': reading.signal_strength,
            'timestamp': reading.timestamp.isoformat(),
            'metadata': reading.metadata
        } for reading in readings]
    }), 200


@bp.route('/<int:reading_id>', methods=['GET'])
def get_reading(reading_id):
    """Obter detalhes de uma leitura específica"""
    reading = Reading.query.get(reading_id)
    
    if not reading:
        return jsonify({'error': 'Leitura não encontrada'}), 404
    
    return jsonify({
        'id': reading.id,
        'sensor_id': reading.sensor_id,
        'sensor': {
            'id': reading.sensor.id,
            'serial_number': reading.sensor.serial_number,
            'protocol': reading.sensor.protocol,
            'location': reading.sensor.location
        } if reading.sensor else None,
        'activity': reading.activity,
        'battery_level': reading.battery_level,
        'signal_strength': reading.signal_strength,
        'temperature': reading.temperature,
        'humidity': reading.humidity,
        'timestamp': reading.timestamp.isoformat(),
        'metadata': reading.metadata
    }), 200


@bp.route('', methods=['POST'])
def create_reading():
    """
    Criar nova leitura (usado pelo gateway MQTT)
    
    Payload:
    {
        "sensor_id": int,
        "activity": int (0 ou 1),
        "battery_level": float,
        "signal_strength": float,
        "temperature": float (opcional),
        "humidity": float (opcional),
        "metadata": object (opcional)
    }
    """
    data = request.get_json()
    
    # Validar campos obrigatórios
    if 'sensor_id' not in data:
        return jsonify({'error': 'Campo sensor_id é obrigatório'}), 400
    
    # Verificar se sensor existe
    sensor = Sensor.query.get(data['sensor_id'])
    if not sensor:
        return jsonify({'error': 'Sensor não encontrado'}), 404
    
    try:
        # Preparar metadados do sensor
        sensor_metadata = {}
        if 'battery_level' in data:
            sensor_metadata['battery_level'] = data['battery_level']
        if 'signal_strength' in data:
            sensor_metadata['signal_strength'] = data['signal_strength']
        if 'temperature' in data:
            sensor_metadata['temperature'] = data['temperature']
        if 'humidity' in data:
            sensor_metadata['humidity'] = data['humidity']
        
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
        sensor.last_reading_at = datetime.utcnow()
        sensor.total_readings += 1
        
        if 'battery_level' in data:
            sensor.battery_level = data['battery_level']
        if 'signal_strength' in data:
            sensor.signal_strength = data['signal_strength']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Leitura criada com sucesso',
            'reading': {
                'id': reading.id,
                'sensor_id': reading.sensor_id,
                'activity': reading.activity,
                'timestamp': reading.timestamp.isoformat()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/bulk', methods=['POST'])
def create_bulk_readings():
    """
    Criar múltiplas leituras de uma vez
    
    Payload:
    {
        "readings": [
            {
                "sensor_id": int,
                "activity": int,
                "battery_level": float,
                ...
            }
        ]
    }
    """
    data = request.get_json()
    
    if 'readings' not in data or not isinstance(data['readings'], list):
        return jsonify({'error': 'Campo readings deve ser uma lista'}), 400
    
    readings_created = 0
    errors = []
    
    try:
        for reading_data in data['readings']:
            if 'sensor_id' not in reading_data:
                errors.append({'error': 'sensor_id é obrigatório', 'data': reading_data})
                continue
            
            sensor = Sensor.query.get(reading_data['sensor_id'])
            if not sensor:
                errors.append({'error': f'Sensor {reading_data["sensor_id"]} não encontrado'})
                continue
            
            # Preparar metadados do sensor
            sensor_metadata = {}
            if 'battery_level' in reading_data:
                sensor_metadata['battery_level'] = reading_data['battery_level']
            if 'signal_strength' in reading_data:
                sensor_metadata['signal_strength'] = reading_data['signal_strength']
            if 'temperature' in reading_data:
                sensor_metadata['temperature'] = reading_data['temperature']
            if 'humidity' in reading_data:
                sensor_metadata['humidity'] = reading_data['humidity']
            
            # Adicionar metadata customizado
            if 'metadata' in reading_data:
                sensor_metadata.update(reading_data['metadata'])
            
            reading = Reading(
                sensor_id=reading_data['sensor_id'],
                activity=reading_data.get('activity', 0),
                timestamp=datetime.utcnow(),
                sensor_metadata=sensor_metadata if sensor_metadata else None
            )
            
            db.session.add(reading)
            
            # Atualizar sensor
            sensor.last_reading_at = datetime.utcnow()
            sensor.total_readings += 1
            
            readings_created += 1
        
        db.session.commit()
        
        return jsonify({
            'message': f'{readings_created} leituras criadas com sucesso',
            'created': readings_created,
            'errors': errors
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/sensor/<int:sensor_id>/latest', methods=['GET'])
def get_latest_reading(sensor_id):
    """Obter última leitura de um sensor"""
    sensor = Sensor.query.get(sensor_id)
    
    if not sensor:
        return jsonify({'error': 'Sensor não encontrado'}), 404
    
    reading = Reading.query.filter_by(sensor_id=sensor_id)\
        .order_by(Reading.timestamp.desc()).first()
    
    if not reading:
        return jsonify({'error': 'Nenhuma leitura encontrada para este sensor'}), 404
    
    return jsonify({
        'id': reading.id,
        'sensor_id': reading.sensor_id,
        'activity': reading.activity,
        'battery_level': reading.battery_level,
        'signal_strength': reading.signal_strength,
        'timestamp': reading.timestamp.isoformat()
    }), 200


@bp.route('/<int:reading_id>', methods=['DELETE'])
@jwt_required()
def delete_reading(reading_id):
    """Deletar leitura (apenas admin)"""
    reading = Reading.query.get(reading_id)
    
    if not reading:
        return jsonify({'error': 'Leitura não encontrada'}), 404
    
    try:
        db.session.delete(reading)
        db.session.commit()
        
        return jsonify({'message': 'Leitura deletada com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
