"""
Routes Package
Agrupa todos os blueprints da API
"""

from app.routes.health import bp as health_bp
from app.routes.auth import bp as auth_bp
from app.routes.sensors import bp as sensors_bp
from app.routes.readings import bp as readings_bp
from app.routes.statistics import bp as statistics_bp

__all__ = [
    'health_bp',
    'auth_bp',
    'sensors_bp',
    'readings_bp',
    'statistics_bp'
]
