"""
Sensors Routes
Endpoints para gerenciamento de sensores
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app import db
from app.models.sensor import Sensor
from datetime import datetime

bp = Blueprint('sensors', __name__)


@bp.route('', methods=['GET'])
def list_sensors():
    """
    Listar todos os sensores
    Query params:
    - status: filtrar por status (active, inactive, maintenance)
    - protocol: filtrar por protocolo (LoRa, ZigBee, Sigfox, RFID)
    - location: filtrar por localização
    """
    # Filtros opcionais
    status = request.args.get('status')
    protocol = request.args.get('protocol')
    location = request.args.get('location')
    
    query = Sensor.query
    
    if status:
        query = query.filter_by(status=status)
    if protocol:
        query = query.filter_by(protocol=protocol)
    if location:
        query = query.filter(Sensor.location.ilike(f'%{location}%'))
    
    sensors = query.all()
    
    return jsonify({
        'count': len(sensors),
        'sensors': [{
            'id': sensor.id,
            'serial_number': sensor.serial_number,
            'protocol': sensor.protocol,
            'location': sensor.location,
            'status': sensor.status,
            'battery_level': sensor.battery_level,
            'last_reading_at': sensor.last_reading_at.isoformat() if sensor.last_reading_at else None,
            'created_at': sensor.created_at.isoformat()
        } for sensor in sensors]
    }), 200


@bp.route('/<int:sensor_id>', methods=['GET'])
def get_sensor(sensor_id):
    """Obter detalhes de um sensor específico"""
    sensor = Sensor.query.get(sensor_id)
    
    if not sensor:
        return jsonify({'error': 'Sensor não encontrado'}), 404
    
    return jsonify({
        'id': sensor.id,
        'serial_number': sensor.serial_number,
        'protocol': sensor.protocol,
        'location': sensor.location,
        'description': sensor.description,
        'status': sensor.status,
        'battery_level': sensor.battery_level,
        'signal_strength': sensor.signal_strength,
        'firmware_version': sensor.firmware_version,
        'last_reading_at': sensor.last_reading_at.isoformat() if sensor.last_reading_at else None,
        'total_readings': sensor.total_readings,
        'created_at': sensor.created_at.isoformat(),
        'updated_at': sensor.updated_at.isoformat()
    }), 200


@bp.route('', methods=['POST'])
@jwt_required()
def create_sensor():
    """
    Criar novo sensor
    
    Payload:
    {
        "serial_number": "string",
        "protocol": "LoRa|ZigBee|Sigfox|RFID",
        "location": "string",
        "description": "string"
    }
    """
    data = request.get_json()
    
    # Validar campos obrigatórios
    required_fields = ['serial_number', 'protocol', 'location']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo {field} é obrigatório'}), 400
    
    # Verificar se serial_number já existe
    if Sensor.query.filter_by(serial_number=data['serial_number']).first():
        return jsonify({'error': 'Serial number já existe'}), 400
    
    # Criar sensor
    try:
        sensor = Sensor(
            serial_number=data['serial_number'],
            protocol=data['protocol'],
            location=data['location'],
            description=data.get('description', ''),
            status='active'
        )
        
        db.session.add(sensor)
        db.session.commit()
        
        return jsonify({
            'message': 'Sensor criado com sucesso',
            'sensor': {
                'id': sensor.id,
                'serial_number': sensor.serial_number,
                'protocol': sensor.protocol,
                'location': sensor.location
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:sensor_id>', methods=['PUT'])
@jwt_required()
def update_sensor(sensor_id):
    """
    Atualizar sensor
    
    Payload:
    {
        "location": "string",
        "description": "string",
        "status": "active|inactive|maintenance"
    }
    """
    sensor = Sensor.query.get(sensor_id)
    
    if not sensor:
        return jsonify({'error': 'Sensor não encontrado'}), 404
    
    data = request.get_json()
    
    try:
        if 'location' in data:
            sensor.location = data['location']
        if 'description' in data:
            sensor.description = data['description']
        if 'status' in data:
            sensor.status = data['status']
        if 'battery_level' in data:
            sensor.battery_level = data['battery_level']
        if 'signal_strength' in data:
            sensor.signal_strength = data['signal_strength']
        
        sensor.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Sensor atualizado com sucesso',
            'sensor': {
                'id': sensor.id,
                'serial_number': sensor.serial_number,
                'location': sensor.location,
                'status': sensor.status
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:sensor_id>', methods=['DELETE'])
@jwt_required()
def delete_sensor(sensor_id):
    """Deletar sensor (apenas admin)"""
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Acesso negado. Apenas administradores.'}), 403
    
    sensor = Sensor.query.get(sensor_id)
    
    if not sensor:
        return jsonify({'error': 'Sensor não encontrado'}), 404
    
    try:
        db.session.delete(sensor)
        db.session.commit()
        
        return jsonify({'message': 'Sensor deletado com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/protocols', methods=['GET'])
def list_protocols():
    """Listar protocolos suportados"""
    return jsonify({
        'protocols': ['LoRa', 'ZigBee', 'Sigfox', 'RFID']
    }), 200


@bp.route('/status-options', methods=['GET'])
def list_status_options():
    """Listar opções de status"""
    return jsonify({
        'status_options': ['active', 'inactive', 'maintenance']
    }), 200
