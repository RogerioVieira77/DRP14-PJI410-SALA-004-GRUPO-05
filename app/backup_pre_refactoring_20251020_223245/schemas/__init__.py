"""
Schemas para validação e serialização de dados
"""

from .user_schema import UserSchema, UserLoginSchema, UserRegisterSchema, UserUpdateSchema
from .sensor_schema import SensorSchema, SensorCreateSchema, SensorUpdateSchema
from .reading_schema import ReadingSchema, ReadingCreateSchema, ReadingBulkCreateSchema
from .statistics_schema import StatisticsSchema

__all__ = [
    'UserSchema',
    'UserLoginSchema', 
    'UserRegisterSchema',
    'UserUpdateSchema',
    'SensorSchema',
    'SensorCreateSchema',
    'SensorUpdateSchema',
    'ReadingSchema',
    'ReadingCreateSchema',
    'ReadingBulkCreateSchema',
    'StatisticsSchema',
]
