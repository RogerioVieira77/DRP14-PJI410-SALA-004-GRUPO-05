"""
Service layer para operações de leituras da piscina.
Contém toda a lógica de negócio relacionada ao monitoramento da piscina.
"""
from datetime import datetime, date, time, timedelta
from typing import Dict, List, Optional, Tuple
from sqlalchemy import func, and_, or_, desc
from app import db
from app.models.pool_reading import PoolReading


class PoolService:
    """Serviço para gerenciar leituras dos sensores da piscina."""
    
    @staticmethod
    def create_reading(data: Dict) -> PoolReading:
        """
        Cria uma nova leitura da piscina.
        
        Args:
            data: Dicionário com os dados da leitura
            
        Returns:
            PoolReading: Objeto da leitura criada
            
        Raises:
            ValueError: Se os dados forem inválidos
        """
        try:
            # Usar sensor_type como string diretamente
            sensor_type = data.get('sensor_type')
            
            # Usar data/hora atual se não fornecidas
            reading_date = data.get('reading_date') or date.today()
            reading_time = data.get('reading_time') or datetime.now().time()
            
            # Criar objeto de leitura
            reading = PoolReading(
                sensor_type=sensor_type,
                reading_date=reading_date,
                reading_time=reading_time
            )
            
            # Adicionar temperatura ou qualidade da água
            if sensor_type in ['water_temp', 'ambient_temp']:
                reading.temperature = data.get('temperature')
            elif sensor_type == 'water_quality':
                reading.water_quality = data.get('water_quality')
            
            db.session.add(reading)
            db.session.commit()
            
            return reading
            
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Erro ao criar leitura: {str(e)}")
    
    @staticmethod
    def get_readings(
        sensor_type: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Tuple[List[PoolReading], int]:
        """
        Busca leituras com filtros opcionais.
        
        Args:
            sensor_type: Tipo de sensor para filtrar
            start_date: Data inicial
            end_date: Data final
            limit: Número máximo de resultados
            offset: Offset para paginação
            
        Returns:
            Tuple[List[PoolReading], int]: Lista de leituras e total de registros
        """
        query = PoolReading.query
        
        # Aplicar filtros
        if sensor_type:
            query = query.filter(PoolReading.sensor_type == sensor_type)
        
        if start_date:
            query = query.filter(PoolReading.reading_date >= start_date)
        
        if end_date:
            query = query.filter(PoolReading.reading_date <= end_date)
        
        # Contar total
        total = query.count()
        
        # Ordenar por data/hora decrescente
        query = query.order_by(
            desc(PoolReading.reading_date),
            desc(PoolReading.reading_time)
        )
        
        # Aplicar paginação
        readings = query.limit(limit).offset(offset).all()
        
        return readings, total
    
    @staticmethod
    def get_latest_readings() -> Dict[str, Optional[PoolReading]]:
        """
        Busca a última leitura de cada tipo de sensor.
        
        Returns:
            Dict[str, Optional[PoolReading]]: Dicionário com as últimas leituras
        """
        result = {
            'water_temp': None,
            'ambient_temp': None,
            'water_quality': None
        }
        
        # Lista de tipos de sensores
        sensor_types = ['water_temp', 'ambient_temp', 'water_quality']
        
        for sensor_type in sensor_types:
            reading = PoolReading.query.filter(
                PoolReading.sensor_type == sensor_type
            ).order_by(
                desc(PoolReading.reading_date),
                desc(PoolReading.reading_time)
            ).first()
            
            result[sensor_type] = reading
        
        return result
    
    @staticmethod
    def get_statistics(days: int = 7) -> Dict:
        """
        Calcula estatísticas das leituras da piscina.
        
        Args:
            days: Número de dias para incluir nas estatísticas
            
        Returns:
            Dict: Estatísticas agregadas
        """
        start_date = date.today() - timedelta(days=days)
        
        # Total de leituras
        total_readings = PoolReading.query.filter(
            PoolReading.reading_date >= start_date
        ).count()
        
        # Estatísticas de temperatura da água
        water_temp_stats = db.session.query(
            func.avg(PoolReading.temperature).label('avg'),
            func.min(PoolReading.temperature).label('min'),
            func.max(PoolReading.temperature).label('max'),
            func.count(PoolReading.id).label('count')
        ).filter(
            and_(
                PoolReading.sensor_type == 'water_temp',
                PoolReading.reading_date >= start_date
            )
        ).first()
        
        # Estatísticas de temperatura ambiente
        ambient_temp_stats = db.session.query(
            func.avg(PoolReading.temperature).label('avg'),
            func.min(PoolReading.temperature).label('min'),
            func.max(PoolReading.temperature).label('max'),
            func.count(PoolReading.id).label('count')
        ).filter(
            and_(
                PoolReading.sensor_type == 'ambient_temp',
                PoolReading.reading_date >= start_date
            )
        ).first()
        
        # Distribuição da qualidade da água
        quality_distribution = db.session.query(
            PoolReading.water_quality,
            func.count(PoolReading.id).label('count')
        ).filter(
            and_(
                PoolReading.sensor_type == 'water_quality',
                PoolReading.reading_date >= start_date
            )
        ).group_by(PoolReading.water_quality).all()
        
        quality_dist_dict = {}
        for quality, count in quality_distribution:
            if quality:
                quality_dist_dict[quality] = count
        
        # Última atualização
        last_reading = PoolReading.query.order_by(
            desc(PoolReading.created_at)
        ).first()
        
        # Alertas ativos (qualidade Regular ou Imprópria)
        active_alerts = PoolReading.query.filter(
            and_(
                PoolReading.sensor_type == 'water_quality',
                or_(
                    PoolReading.water_quality == 'Regular',
                    PoolReading.water_quality == 'Imprópria'
                ),
                PoolReading.reading_date >= start_date
            )
        ).order_by(
            desc(PoolReading.reading_date),
            desc(PoolReading.reading_time)
        ).limit(10).all()
        
        alerts_list = []
        for alert in active_alerts:
            alerts_list.append({
                'id': alert.id,
                'water_quality': alert.water_quality,
                'alert_level': 'warning' if alert.water_quality == 'Regular' else 'danger',
                'reading_date': alert.reading_date.isoformat(),
                'reading_time': alert.reading_time.strftime('%H:%M:%S'),
                'created_at': alert.created_at.isoformat()
            })
        
        return {
            'total_readings': total_readings,
            'period_days': days,
            'water_temp': {
                'avg': float(water_temp_stats.avg) if water_temp_stats.avg else None,
                'min': float(water_temp_stats.min) if water_temp_stats.min else None,
                'max': float(water_temp_stats.max) if water_temp_stats.max else None,
                'count': water_temp_stats.count
            },
            'ambient_temp': {
                'avg': float(ambient_temp_stats.avg) if ambient_temp_stats.avg else None,
                'min': float(ambient_temp_stats.min) if ambient_temp_stats.min else None,
                'max': float(ambient_temp_stats.max) if ambient_temp_stats.max else None,
                'count': ambient_temp_stats.count
            },
            'water_quality': {
                'distribution': quality_dist_dict,
                'total_readings': sum(quality_dist_dict.values())
            },
            'last_update': last_reading.created_at if last_reading else None,
            'active_alerts': alerts_list
        }
    
    @staticmethod
    def get_temperature_history(
        sensor_type: str,
        days: int = 7,
        limit: int = 100
    ) -> List[PoolReading]:
        """
        Busca histórico de temperatura para gráficos.
        
        Args:
            sensor_type: 'water_temp' ou 'ambient_temp'
            days: Número de dias de histórico
            limit: Número máximo de pontos
            
        Returns:
            List[PoolReading]: Lista de leituras ordenadas por data/hora
        """
        if sensor_type not in ['water_temp', 'ambient_temp']:
            return []
        
        start_date = date.today() - timedelta(days=days)
        
        readings = PoolReading.query.filter(
            and_(
                PoolReading.sensor_type == sensor_type,
                PoolReading.reading_date >= start_date
            )
        ).order_by(
            PoolReading.reading_date.asc(),
            PoolReading.reading_time.asc()
        ).limit(limit).all()
        
        return readings
    
    @staticmethod
    def get_daily_temperature_average(
        sensor_type: str,
        days: int = 10
    ) -> List[Dict]:
        """
        Calcula a média diária de temperatura dos últimos N dias.
        
        Args:
            sensor_type: 'water_temp' ou 'ambient_temp'
            days: Número de dias de histórico (padrão: 10)
            
        Returns:
            List[Dict]: Lista com a média de cada dia no formato:
                        [{'date': 'YYYY-MM-DD', 'avg_temperature': float}, ...]
        """
        if sensor_type not in ['water_temp', 'ambient_temp']:
            return []
        
        start_date = date.today() - timedelta(days=days - 1)
        
        # Buscar todas as leituras do período
        readings = PoolReading.query.filter(
            and_(
                PoolReading.sensor_type == sensor_type,
                PoolReading.reading_date >= start_date
            )
        ).order_by(
            PoolReading.reading_date.asc()
        ).all()
        
        # Agrupar por data e calcular média
        daily_averages = {}
        for reading in readings:
            reading_date_str = reading.reading_date.isoformat()
            
            if reading_date_str not in daily_averages:
                daily_averages[reading_date_str] = {
                    'sum': 0,
                    'count': 0
                }
            
            if reading.temperature is not None:
                daily_averages[reading_date_str]['sum'] += float(reading.temperature)
                daily_averages[reading_date_str]['count'] += 1
        
        # Calcular médias e formatar resultado
        result = []
        for day_date in sorted(daily_averages.keys()):
            data = daily_averages[day_date]
            if data['count'] > 0:
                avg_temp = round(data['sum'] / data['count'], 2)
                result.append({
                    'date': day_date,
                    'avg_temperature': avg_temp,
                    'reading_count': data['count']
                })
        
        return result
    
    @staticmethod
    def check_water_quality_alerts() -> List[Dict]:
        """
        Verifica alertas de qualidade da água nas últimas 24 horas.
        
        Returns:
            List[Dict]: Lista de alertas ativos
        """
        yesterday = date.today() - timedelta(days=1)
        
        alerts = PoolReading.query.filter(
            and_(
                PoolReading.sensor_type == 'water_quality',
                or_(
                    PoolReading.water_quality == 'Regular',
                    PoolReading.water_quality == 'Imprópria'
                ),
                PoolReading.reading_date >= yesterday
            )
        ).order_by(
            desc(PoolReading.reading_date),
            desc(PoolReading.reading_time)
        ).all()
        
        result = []
        for alert in alerts:
            result.append({
                'id': alert.id,
                'water_quality': alert.water_quality,
                'alert_level': PoolReading.get_alert_level(alert.water_quality),
                'reading_date': alert.reading_date.isoformat(),
                'reading_time': alert.reading_time.strftime('%H:%M:%S'),
                'message': f'Qualidade da água: {alert.water_quality}'
            })
        
        return result
