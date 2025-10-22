"""
Rotas da API para monitoramento da piscina.
Endpoints para gerenciar leituras dos sensores da piscina.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from datetime import datetime, date

from app.schemas.pool_schema import (
    PoolReadingCreateSchema,
    PoolReadingResponseSchema,
    PoolReadingListQuerySchema,
    PoolStatisticsSchema,
    LatestReadingsSchema
)
from app.services.pool_service import PoolService


# Criar blueprint
pool_bp = Blueprint('pool', __name__, url_prefix='/api/v1/pool')


# Schemas
reading_create_schema = PoolReadingCreateSchema()
reading_response_schema = PoolReadingResponseSchema()
readings_response_schema = PoolReadingResponseSchema(many=True)
query_schema = PoolReadingListQuerySchema()
statistics_schema = PoolStatisticsSchema()
latest_schema = LatestReadingsSchema()


@pool_bp.route('/readings', methods=['POST'])
@jwt_required()
def create_reading():
    """
    Cria uma nova leitura de sensor da piscina.
    
    Requer autenticação JWT.
    
    Body (JSON):
    {
        "sensor_type": "water_temp|ambient_temp|water_quality",
        "reading_date": "2024-01-15" (opcional),
        "reading_time": "14:30:00" (opcional),
        "temperature": 28.5 (para sensores de temperatura),
        "water_quality": "Ótima|Boa|Regular|Imprópria" (para sensor water_quality)
    }
    
    Returns:
        201: Leitura criada com sucesso
        400: Dados inválidos
        401: Não autenticado
    """
    try:
        # Validar dados de entrada
        data = reading_create_schema.load(request.json)
        
        # Criar leitura
        reading = PoolService.create_reading(data)
        
        # Retornar resposta
        return jsonify({
            'message': 'Leitura criada com sucesso',
            'data': reading_response_schema.dump(reading)
        }), 201
        
    except ValidationError as e:
        return jsonify({
            'error': 'Dados inválidos',
            'details': e.messages
        }), 400
    except ValueError as e:
        return jsonify({
            'error': 'Erro ao criar leitura',
            'details': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'error': 'Erro interno do servidor',
            'details': str(e)
        }), 500


@pool_bp.route('/readings', methods=['GET'])
@jwt_required()
def get_readings():
    """
    Lista leituras da piscina com filtros opcionais.
    
    Requer autenticação JWT.
    
    Query Parameters:
        sensor_type: Tipo de sensor (opcional)
        start_date: Data inicial YYYY-MM-DD (opcional)
        end_date: Data final YYYY-MM-DD (opcional)
        limit: Número máximo de resultados (padrão: 100)
        offset: Offset para paginação (padrão: 0)
    
    Returns:
        200: Lista de leituras
        400: Parâmetros inválidos
        401: Não autenticado
    """
    try:
        # Validar query parameters
        query_params = query_schema.load(request.args)
        
        # Buscar leituras
        readings, total = PoolService.get_readings(
            sensor_type=query_params.get('sensor_type'),
            start_date=query_params.get('start_date'),
            end_date=query_params.get('end_date'),
            limit=query_params.get('limit', 100),
            offset=query_params.get('offset', 0)
        )
        
        # Retornar resposta
        return jsonify({
            'data': readings_response_schema.dump(readings),
            'pagination': {
                'total': total,
                'limit': query_params.get('limit', 100),
                'offset': query_params.get('offset', 0)
            }
        }), 200
        
    except ValidationError as e:
        return jsonify({
            'error': 'Parâmetros inválidos',
            'details': e.messages
        }), 400
    except Exception as e:
        return jsonify({
            'error': 'Erro interno do servidor',
            'details': str(e)
        }), 500


@pool_bp.route('/readings/latest', methods=['GET'])
@jwt_required()
def get_latest_readings():
    """
    Retorna a última leitura de cada tipo de sensor.
    
    Requer autenticação JWT.
    
    Returns:
        200: Últimas leituras de cada sensor
        401: Não autenticado
    """
    try:
        latest = PoolService.get_latest_readings()
        
        return jsonify({
            'data': latest_schema.dump(latest)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Erro interno do servidor',
            'details': str(e)
        }), 500


@pool_bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_statistics():
    """
    Retorna estatísticas agregadas das leituras da piscina.
    
    Requer autenticação JWT.
    
    Query Parameters:
        days: Número de dias para incluir (padrão: 7)
    
    Returns:
        200: Estatísticas da piscina
        401: Não autenticado
    """
    try:
        days = request.args.get('days', default=7, type=int)
        
        if days < 1 or days > 365:
            return jsonify({
                'error': 'Parâmetro days deve estar entre 1 e 365'
            }), 400
        
        stats = PoolService.get_statistics(days=days)
        
        return jsonify({
            'data': statistics_schema.dump(stats)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Erro interno do servidor',
            'details': str(e)
        }), 500


@pool_bp.route('/temperature/history', methods=['GET'])
@jwt_required()
def get_temperature_history():
    """
    Retorna histórico de temperatura para gráficos.
    
    Requer autenticação JWT.
    
    Query Parameters:
        sensor_type: 'water_temp' ou 'ambient_temp' (obrigatório)
        days: Número de dias de histórico (padrão: 7)
        limit: Número máximo de pontos (padrão: 100)
    
    Returns:
        200: Histórico de temperatura
        400: Parâmetros inválidos
        401: Não autenticado
    """
    try:
        sensor_type = request.args.get('sensor_type')
        
        if not sensor_type:
            return jsonify({
                'error': 'Parâmetro sensor_type é obrigatório'
            }), 400
        
        if sensor_type not in ['water_temp', 'ambient_temp']:
            return jsonify({
                'error': 'sensor_type deve ser water_temp ou ambient_temp'
            }), 400
        
        days = request.args.get('days', default=7, type=int)
        limit = request.args.get('limit', default=100, type=int)
        
        readings = PoolService.get_temperature_history(
            sensor_type=sensor_type,
            days=days,
            limit=limit
        )
        
        return jsonify({
            'data': readings_response_schema.dump(readings),
            'sensor_type': sensor_type,
            'period_days': days
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Erro interno do servidor',
            'details': str(e)
        }), 500


@pool_bp.route('/temperature/daily-average', methods=['GET'])
@jwt_required()
def get_daily_temperature_average():
    """
    Retorna a média diária de temperatura para gráficos.
    
    Requer autenticação JWT.
    
    Query Parameters:
        sensor_type: 'water_temp' ou 'ambient_temp' (obrigatório)
        days: Número de dias de histórico (padrão: 10)
    
    Returns:
        200: Média diária de temperatura
        400: Parâmetros inválidos
        401: Não autenticado
    """
    try:
        sensor_type = request.args.get('sensor_type')
        
        if not sensor_type:
            return jsonify({
                'error': 'Parâmetro sensor_type é obrigatório'
            }), 400
        
        if sensor_type not in ['water_temp', 'ambient_temp']:
            return jsonify({
                'error': 'sensor_type deve ser water_temp ou ambient_temp'
            }), 400
        
        days = request.args.get('days', default=10, type=int)
        
        if days < 1 or days > 365:
            return jsonify({
                'error': 'Parâmetro days deve estar entre 1 e 365'
            }), 400
        
        daily_averages = PoolService.get_daily_temperature_average(
            sensor_type=sensor_type,
            days=days
        )
        
        return jsonify({
            'data': daily_averages,
            'sensor_type': sensor_type,
            'period_days': days
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Erro interno do servidor',
            'details': str(e)
        }), 500


@pool_bp.route('/alerts', methods=['GET'])
@jwt_required()
def get_alerts():
    """
    Retorna alertas ativos de qualidade da água.
    
    Requer autenticação JWT.
    
    Returns:
        200: Lista de alertas ativos
        401: Não autenticado
    """
    try:
        alerts = PoolService.check_water_quality_alerts()
        
        return jsonify({
            'data': alerts,
            'total': len(alerts)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Erro interno do servidor',
            'details': str(e)
        }), 500


# Endpoint de health check (sem autenticação)
@pool_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check do módulo de piscina.
    
    Returns:
        200: Status do módulo
    """
    try:
        # Tentar buscar estatísticas básicas
        stats = PoolService.get_statistics(days=1)
        
        return jsonify({
            'status': 'healthy',
            'module': 'pool_monitoring',
            'total_readings_today': stats.get('total_readings', 0),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'module': 'pool_monitoring',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500
