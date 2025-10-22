"""
Schema de validação para Sensor
"""

from marshmallow import Schema, fields, validate, validates, ValidationError


class SensorSchema(Schema):
    """Schema completo do sensor"""
    id = fields.Int(dump_only=True)
    serial_number = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    protocol = fields.Str(
        required=True,
        validate=validate.OneOf(['LoRa', 'ZigBee', 'Sigfox', 'RFID', 'BLE', 'WiFi'])
    )
    location = fields.Str(required=True, validate=validate.Length(max=200))
    description = fields.Str(validate=validate.Length(max=500))
    status = fields.Str(
        validate=validate.OneOf(['active', 'inactive', 'maintenance', 'error']),
        load_default='active'
    )
    protocol_config = fields.Dict()
    firmware_version = fields.Str(validate=validate.Length(max=20))
    battery_level = fields.Int(validate=validate.Range(min=0, max=100))
    signal_strength = fields.Int(validate=validate.Range(min=-120, max=0))
    total_readings = fields.Int(dump_only=True)
    last_reading_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class SensorCreateSchema(Schema):
    """Schema para criação de sensor"""
    serial_number = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    protocol = fields.Str(
        required=True,
        validate=validate.OneOf(['LoRa', 'ZigBee', 'Sigfox', 'RFID', 'BLE', 'WiFi'])
    )
    location = fields.Str(required=True, validate=validate.Length(max=200))
    description = fields.Str(validate=validate.Length(max=500))
    status = fields.Str(
        validate=validate.OneOf(['active', 'inactive', 'maintenance', 'error']),
        load_default='active'
    )
    protocol_config = fields.Dict()
    firmware_version = fields.Str(validate=validate.Length(max=20))
    battery_level = fields.Int(validate=validate.Range(min=0, max=100))
    signal_strength = fields.Int(validate=validate.Range(min=-120, max=0))

    @validates('serial_number')
    def validate_serial_number(self, value):
        """Validar formato do serial number"""
        if not value.replace('-', '').replace('_', '').isalnum():
            raise ValidationError('Serial number pode conter apenas letras, números, - e _')


class SensorUpdateSchema(Schema):
    """Schema para atualização de sensor"""
    location = fields.Str(validate=validate.Length(max=200))
    description = fields.Str(validate=validate.Length(max=500))
    status = fields.Str(
        validate=validate.OneOf(['active', 'inactive', 'maintenance', 'error'])
    )
    protocol_config = fields.Dict()
    firmware_version = fields.Str(validate=validate.Length(max=20))
    battery_level = fields.Int(validate=validate.Range(min=0, max=100))
    signal_strength = fields.Int(validate=validate.Range(min=-120, max=0))
