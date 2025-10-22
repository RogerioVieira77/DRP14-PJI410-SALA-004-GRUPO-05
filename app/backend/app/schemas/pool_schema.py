"""
Schemas de validação para endpoints de monitoramento da piscina.
Utiliza Marshmallow para serialização e validação de dados.
"""
from marshmallow import Schema, fields, validate, validates, ValidationError, post_load
from datetime import date, time


class PoolReadingCreateSchema(Schema):
    """Schema para criação de nova leitura da piscina."""
    
    sensor_type = fields.Str(
        required=True,
        validate=validate.OneOf(['water_temp', 'ambient_temp', 'water_quality']),
        error_messages={'required': 'Tipo de sensor é obrigatório'}
    )
    
    reading_date = fields.Date(
        required=False,
        allow_none=True,
        format='%Y-%m-%d'
    )
    
    reading_time = fields.Time(
        required=False,
        allow_none=True,
        format='%H:%M:%S'
    )
    
    temperature = fields.Decimal(
        required=False,
        allow_none=True,
        places=2,
        as_string=False
    )
    
    water_quality = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.OneOf(['Ótima', 'Boa', 'Regular', 'Imprópria'])
    )
    
    @validates('temperature')
    def validate_temperature(self, value):
        """Valida que a temperatura está em um range válido."""
        if value is not None:
            temp = float(value)
            if temp < 15.0 or temp > 45.0:
                raise ValidationError('Temperatura deve estar entre 15°C e 45°C')
    
    @post_load
    def validate_sensor_data(self, data, **kwargs):
        """
        Valida que os dados estão consistentes com o tipo de sensor.
        - Sensores de temperatura devem ter temperature
        - Sensor de qualidade deve ter water_quality
        """
        sensor_type = data.get('sensor_type')
        
        if sensor_type in ['water_temp', 'ambient_temp']:
            if data.get('temperature') is None:
                raise ValidationError(
                    f'Sensor {sensor_type} requer campo temperature',
                    field_name='temperature'
                )
            # Remove water_quality se presente
            data.pop('water_quality', None)
            
        elif sensor_type == 'water_quality':
            if data.get('water_quality') is None:
                raise ValidationError(
                    'Sensor water_quality requer campo water_quality',
                    field_name='water_quality'
                )
            # Remove temperature se presente
            data.pop('temperature', None)
        
        return data


class PoolReadingResponseSchema(Schema):
    """Schema para resposta de leitura da piscina."""
    
    id = fields.Int(dump_only=True)
    sensor_type = fields.Str()
    reading_date = fields.Date(format='%Y-%m-%d')
    reading_time = fields.Time(format='%H:%M:%S')
    temperature = fields.Decimal(places=2, as_string=False, allow_none=True)
    water_quality = fields.Str(allow_none=True)
    created_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    updated_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    
    # Campo extra para alertas
    alert_level = fields.Method('get_alert_level')
    
    def get_alert_level(self, obj):
        """Retorna o nível de alerta se aplicável."""
        if hasattr(obj, 'water_quality') and obj.water_quality:
            quality = obj.water_quality.value if hasattr(obj.water_quality, 'value') else obj.water_quality
            if quality == 'Regular':
                return 'warning'
            elif quality == 'Imprópria':
                return 'danger'
        return None


class PoolReadingListQuerySchema(Schema):
    """Schema para query parameters ao listar leituras."""
    
    sensor_type = fields.Str(
        required=False,
        validate=validate.OneOf(['water_temp', 'ambient_temp', 'water_quality'])
    )
    
    start_date = fields.Date(
        required=False,
        format='%Y-%m-%d'
    )
    
    end_date = fields.Date(
        required=False,
        format='%Y-%m-%d'
    )
    
    limit = fields.Int(
        required=False,
        validate=validate.Range(min=1, max=1000),
        load_default=100
    )
    
    offset = fields.Int(
        required=False,
        validate=validate.Range(min=0),
        load_default=0
    )


class PoolStatisticsSchema(Schema):
    """Schema para estatísticas da piscina."""
    
    total_readings = fields.Int()
    
    water_temp = fields.Dict(
        keys=fields.Str(),
        values=fields.Raw()
    )
    
    ambient_temp = fields.Dict(
        keys=fields.Str(),
        values=fields.Raw()
    )
    
    water_quality = fields.Dict(
        keys=fields.Str(),
        values=fields.Raw()
    )
    
    last_update = fields.DateTime(format='%Y-%m-%d %H:%M:%S', allow_none=True)
    
    active_alerts = fields.List(fields.Dict())


class LatestReadingsSchema(Schema):
    """Schema para as últimas leituras de cada sensor."""
    
    water_temp = fields.Nested(PoolReadingResponseSchema, allow_none=True)
    ambient_temp = fields.Nested(PoolReadingResponseSchema, allow_none=True)
    water_quality = fields.Nested(PoolReadingResponseSchema, allow_none=True)
