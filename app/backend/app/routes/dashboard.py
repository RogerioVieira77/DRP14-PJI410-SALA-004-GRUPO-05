"""
Dashboard Routes
Endpoints públicos para o dashboard frontend (sem autenticação JWT)
Retorna dados agregados e estatísticas para visualização
APENAS DADOS REAIS DO BANCO - SEM SIMULAÇÃO
"""

from flask import Blueprint, jsonify
from app import db
from app.models.reading import Reading
from app.models.sensor import Sensor
from app.models.alert import Alert
from datetime import datetime, timedelta
from sqlalchemy import func, and_

bp = Blueprint('dashboard', __name__)


# ========== CONFIGURAÇÕES ==========
MAX_CAPACITY = 300  # Capacidade máxima do CEU
POOL_CAPACITY = 60  # Capacidade da piscina

# Mapeamento de sensores para áreas
AREA_MAPPING = {
    'Entrada Principal': {'sensors': ['LORA-ENTRADA-01', 'LORA-SAIDA-01'], 'capacity': 100},
    'Entrada Lateral Norte': {'sensors': ['ZIGB-LATERAL-01'], 'capacity': 50},
    'Entrada Lateral Sul': {'sensors': ['ZIGB-LATERAL-02'], 'capacity': 50},
    'Banheiros': {'sensors': ['SIGF-BANHEIRO-01'], 'capacity': 40},
    'Portaria': {'sensors': ['RFID-PORTARIA-01'], 'capacity': 20}
}


# ========== ENDPOINT 1: Estatísticas Atuais ==========
@bp.route('/current-stats', methods=['GET'])
def get_current_stats():
    """
    Retorna estatísticas atuais do CEU baseadas nos dados reais do banco
    
    Returns:
        JSON com:
        - current_people: Número atual de pessoas no CEU
        - entries_today: Total de entradas hoje
        - exits_today: Total de saídas hoje
        - capacity_percentage: Percentual da capacidade
        - last_reading: Data/hora da última leitura
        - timestamp: Data/hora da consulta
    """
    try:
        # Data de hoje (início do dia)
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Buscar entradas (activity = 1) de hoje
        entries_today = Reading.query.filter(
            Reading.timestamp >= today_start,
            Reading.activity == 1
        ).count()
        
        # Buscar saídas (activity = 0) de hoje
        exits_today = Reading.query.filter(
            Reading.timestamp >= today_start,
            Reading.activity == 0
        ).count()
        
        # Calcular pessoas atuais (simplificado)
        current_people = max(0, entries_today - exits_today)
        
        # Buscar última leitura registrada (independente do dia)
        last_reading_obj = Reading.query.order_by(Reading.timestamp.desc()).first()
        last_reading = last_reading_obj.timestamp.isoformat() if last_reading_obj else None
        
        # Calcular percentual da capacidade
        capacity_percentage = round((current_people / MAX_CAPACITY) * 100, 1)
        
        return jsonify({
            'current_people': current_people,
            'entries_today': entries_today,
            'exits_today': exits_today,
            'capacity_percentage': capacity_percentage,
            'max_capacity': MAX_CAPACITY,
            'last_reading': last_reading,
            'has_data_today': entries_today > 0 or exits_today > 0,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Erro ao buscar estatísticas atuais',
            'details': str(e)
        }), 500


# ========== ENDPOINT 2: Fluxo de Pessoas (24h) ==========
@bp.route('/people-flow', methods=['GET'])
def get_people_flow():
    """
    Retorna dados para gráfico de fluxo de pessoas nas últimas 24 horas
    Dados agrupados em intervalos de 4 horas
    
    Returns:
        JSON com:
        - labels: Horários (00:00, 04:00, 08:00, etc)
        - data: Número de pessoas em cada período
    """
    try:
        # Última 24 horas
        yesterday = datetime.utcnow() - timedelta(days=1)
        
        # Buscar readings das últimas 24h
        readings = Reading.query.filter(
            Reading.timestamp >= yesterday
        ).all()
        
        # Agrupar por período de 4 horas
        periods = {
            '00:00': 0, '04:00': 0, '08:00': 0, 
            '12:00': 0, '16:00': 0, '20:00': 0
        }
        
        for reading in readings:
            hour = reading.timestamp.hour
            if hour < 4:
                periods['00:00'] += 1
            elif hour < 8:
                periods['04:00'] += 1
            elif hour < 12:
                periods['08:00'] += 1
            elif hour < 16:
                periods['12:00'] += 1
            elif hour < 20:
                periods['16:00'] += 1
            else:
                periods['20:00'] += 1
        
        # Converter contagem em média de pessoas
        data = [max(0, int(count / 2)) for count in periods.values()]
        
        return jsonify({
            'labels': ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
            'data': data,
            'period': '24h',
            'total_readings': len(readings),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Erro ao buscar fluxo de pessoas',
            'details': str(e)
        }), 500


# ========== ENDPOINT 3: Ocupação por Área ==========
@bp.route('/areas-occupation', methods=['GET'])
def get_areas_occupation():
    """
    Retorna ocupação atual de cada área monitorada
    Baseado apenas em dados reais do banco
    
    Returns:
        JSON com array de áreas, cada uma com:
        - name: Nome da área
        - current: Pessoas atuais
        - capacity: Capacidade máxima
        - percentage: Percentual de ocupação
    """
    try:
        areas = []
        
        # Últimos 15 minutos (atividade recente)
        recent_time = datetime.utcnow() - timedelta(minutes=15)
        
        for area_name, area_config in AREA_MAPPING.items():
            # Buscar sensores da área
            sensor_serials = area_config['sensors']
            capacity = area_config['capacity']
            
            # Contar readings recentes dos sensores desta área
            current_count = Reading.query.join(Sensor).filter(
                Sensor.serial_number.in_(sensor_serials),
                Reading.timestamp >= recent_time,
                Reading.activity == 1
            ).count()
            
            percentage = round((current_count / capacity) * 100, 1) if capacity > 0 else 0
            
            areas.append({
                'name': area_name,
                'current': current_count,
                'capacity': capacity,
                'percentage': percentage,
                'status': 'critical' if percentage > 80 else 'warning' if percentage > 60 else 'normal'
            })
        
        # Buscar última leitura geral
        last_reading_obj = Reading.query.order_by(Reading.timestamp.desc()).first()
        last_reading = last_reading_obj.timestamp.isoformat() if last_reading_obj else None
        
        return jsonify({
            'areas': areas,
            'total_areas': len(areas),
            'last_reading': last_reading,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Erro ao buscar ocupação por área',
            'details': str(e)
        }), 500


# ========== ENDPOINT 4: Status da Piscina ==========
@bp.route('/pool/current', methods=['GET'])
def get_pool_current():
    """
    Retorna status atual da piscina
    Baseado apenas em dados reais (se disponíveis)
    
    Returns:
        JSON com:
        - occupancy_percentage: Percentual de ocupação
        - current_people: Pessoas na piscina agora
        - capacity: Capacidade máxima
        - entries_today: Entradas hoje
        - water_temperature: Temperatura da água (°C)
        - ambient_temperature: Temperatura ambiente (°C)
        - status: normal/warning/critical
        - last_reading: Data/hora da última leitura
    """
    try:
        # Nota: Como pool_readings pode estar vazia, retornamos valores zerados
        # mas mantemos a estrutura para quando houver dados reais
        
        # Valores padrão (sem dados)
        occupancy_percentage = 0
        current_people = 0
        entries_today = 0
        water_temperature = None
        ambient_temperature = None
        status = 'normal'
        last_reading = None
        
        # TODO: Quando houver dados em pool_readings, buscar aqui
        # Exemplo de query futura:
        # latest_temp = PoolReading.query.filter_by(sensor_type='water_temp').order_by(PoolReading.timestamp.desc()).first()
        
        return jsonify({
            'occupancy_percentage': occupancy_percentage,
            'current_people': current_people,
            'capacity': POOL_CAPACITY,
            'entries_today': entries_today,
            'water_temperature': water_temperature,
            'ambient_temperature': ambient_temperature,
            'status': status,
            'last_reading': last_reading,
            'has_data': False,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Erro ao buscar status da piscina',
            'details': str(e)
        }), 500


# ========== ENDPOINT 5: Qualidade da Água ==========
@bp.route('/pool/quality', methods=['GET'])
def get_pool_quality():
    """
    Retorna dados de qualidade da água da piscina
    Baseado apenas em dados reais (se disponíveis)
    
    Returns:
        JSON com métricas de qualidade:
        - ph: Valor e status
        - chlorine: Cloro livre (ppm) e status
        - alkalinity: Alcalinidade (ppm) e status
    """
    try:
        # Nota: Como pool_readings pode estar vazia, retornamos valores None
        # TODO: Quando houver dados, buscar da tabela pool_readings
        
        return jsonify({
            'ph': {
                'value': None,
                'status': 'no_data',
                'min_safe': 7.2,
                'max_safe': 7.6,
                'unit': ''
            },
            'chlorine': {
                'value': None,
                'status': 'no_data',
                'min_safe': 1.0,
                'max_safe': 3.0,
                'unit': 'ppm'
            },
            'alkalinity': {
                'value': None,
                'status': 'no_data',
                'min_safe': 80,
                'max_safe': 120,
                'unit': 'ppm'
            },
            'overall_status': 'no_data',
            'has_data': False,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Erro ao buscar qualidade da água',
            'details': str(e)
        }), 500


# ========== ENDPOINT 6: Alertas Ativos ==========
@bp.route('/alerts/active', methods=['GET'])
def get_active_alerts():
    """
    Retorna alertas ativos (não resolvidos)
    Baseado apenas em dados reais do banco
    
    Returns:
        JSON com:
        - alerts: Array de alertas ativos
        - total: Número total de alertas
    """
    try:
        # Buscar alertas não resolvidos da tabela alerts
        active_alerts = Alert.query.filter(
            Alert.status.in_(['open', 'acknowledged'])
        ).order_by(
            Alert.timestamp.desc()
        ).limit(10).all()
        
        alerts_list = []
        
        for alert in active_alerts:
            alerts_list.append({
                'id': alert.id,
                'type': alert.alert_type,
                'severity': alert.severity,
                'message': alert.message,
                'timestamp': alert.timestamp.isoformat(),
                'sensor_id': alert.sensor_id,
                'area': 'Sistema'  # Pode ser melhorado com JOIN
            })
        
        return jsonify({
            'alerts': alerts_list,
            'total': len(alerts_list),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Erro ao buscar alertas ativos',
            'details': str(e)
        }), 500


# ========== ENDPOINT DE HEALTH CHECK ==========
@bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check do módulo dashboard
    Verifica se os endpoints estão respondendo
    """
    try:
        # Testar conexão com banco
        sensor_count = Sensor.query.count()
        reading_count = Reading.query.count()
        
        return jsonify({
            'status': 'healthy',
            'module': 'dashboard',
            'database': 'connected',
            'sensors': sensor_count,
            'readings': reading_count,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'module': 'dashboard',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500
