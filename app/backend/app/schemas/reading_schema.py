"""
Schema de validação para Reading
"""

from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class ReadingSchema(Schema):
    """Schema completo de leitura"""
    id = fields.Int(dump_only=True)
    sensor_id = fields.Int(required=True)
    activity = fields.Int(
        required=True,
        validate=validate.OneOf([0, 1])
    )
    timestamp = fields.DateTime(dump_only=True)
    sensor_metadata = fields.Dict()
    message_id = fields.Str()
    gateway_id = fields.Str()
    created_at = fields.DateTime(dump_only=True)


class ReadingCreateSchema(Schema):
    """Schema para criação de leitura"""
    sensor_id = fields.Int(required=True)
    activity = fields.Int(
        validate=validate.OneOf([0, 1]),
        load_default=0
    )
    battery_level = fields.Int(validate=validate.Range(min=0, max=100))
    signal_strength = fields.Int(validate=validate.Range(min=-120, max=0))
    temperature = fields.Float(validate=validate.Range(min=-50, max=100))
    humidity = fields.Float(validate=validate.Range(min=0, max=100))
    metadata = fields.Dict()


class ReadingBulkCreateSchema(Schema):
    """Schema para criação em lote de leituras"""
    readings = fields.List(
        fields.Nested(ReadingCreateSchema),
        required=True,
        validate=validate.Length(min=1, max=1000)
    )

    @validates_schema
    def validate_readings(self, data, **kwargs):
        """Validar lista de leituras"""
        if not data.get('readings'):
            raise ValidationError('Lista de leituras não pode estar vazia', 'readings')
