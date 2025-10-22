"""
Health Check Routes
Endpoints para verificar saúde da API
"""

from flask import Blueprint, jsonify
from datetime import datetime
from app import db

bp = Blueprint('health', __name__)


@bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check básico
    
    Returns:
        JSON com status da API
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'CEU Tres Pontes API',
        'version': '1.0.0'
    }), 200


@bp.route('/health/db', methods=['GET'])
def database_health():
    """
    Health check do banco de dados
    
    Returns:
        JSON com status da conexão com o banco
    """
    try:
        # Tentar uma query simples
        db.session.execute(db.text('SELECT 1'))
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 503


@bp.route('/health/detailed', methods=['GET'])
def detailed_health():
    """
    Health check detalhado com estatísticas
    
    Returns:
        JSON com informações detalhadas do sistema
    """
    from app.models import Sensor, Reading, Alert
    
    try:
        # Estatísticas básicas
        total_sensors = Sensor.query.count()
        active_sensors = Sensor.query.filter_by(status='active').count()
        total_readings = Reading.query.count()
        open_alerts = Alert.query.filter_by(status='open').count()
        
        # Verificar conexão com banco
        db.session.execute(db.text('SELECT 1'))
        db_status = 'connected'
    
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 503
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'CEU Tres Pontes API',
        'version': '1.0.0',
        'database': {
            'status': db_status,
            'stats': {
                'total_sensors': total_sensors,
                'active_sensors': active_sensors,
                'total_readings': total_readings,
                'open_alerts': open_alerts
            }
        }
    }), 200
