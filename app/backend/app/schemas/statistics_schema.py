"""
Schema de validação para Statistics
"""

from marshmallow import Schema, fields


class StatisticsSchema(Schema):
    """Schema de estatísticas"""
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    total_detections = fields.Int()
    total_entries = fields.Int()
    total_exits = fields.Int()
    peak_occupation = fields.Int()
    avg_occupation = fields.Float()
    created_at = fields.DateTime(dump_only=True)
