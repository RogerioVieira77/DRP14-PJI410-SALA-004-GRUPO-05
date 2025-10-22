"""
Configurações da Aplicação Flask
Diferentes configurações para desenvolvimento, testes e produção
"""

import os
from datetime import timedelta
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Carregar variáveis de ambiente do .env
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """Configurações base compartilhadas por todos os ambientes"""
    
    # Secret Keys
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    
    # JWT Configuration
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600)))
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    
    # Database Configuration
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = int(os.environ.get('DB_PORT', 3306))
    DB_USER = os.environ.get('DB_USER', 'ceu_tres_pontes')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
    DB_NAME = os.environ.get('DB_NAME', 'ceu_tres_pontes_db')
    
    # URL encode da senha para evitar problemas com caracteres especiais
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_RECYCLE = 3600
    SQLALCHEMY_POOL_TIMEOUT = 30
    
    # MQTT Configuration (Herdado da Fase 2)
    MQTT_BROKER_HOST = os.environ.get('MQTT_BROKER_HOST', 'localhost')
    MQTT_BROKER_PORT = int(os.environ.get('MQTT_BROKER_PORT', 1883))
    MQTT_USERNAME = os.environ.get('MQTT_USERNAME')
    MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD')
    MQTT_BASE_TOPIC = os.environ.get('MQTT_BASE_TOPIC', 'ceu/tres_pontes')
    
    # Gateway Configuration
    GATEWAY_ID = os.environ.get('GATEWAY_ID', 'gateway_001')
    
    # API Configuration
    API_PREFIX = os.environ.get('API_PREFIX', '/api/v1')
    API_TITLE = os.environ.get('API_TITLE', 'CEU Tres Pontes API')
    API_VERSION = os.environ.get('API_VERSION', '1.0.0')
    
    # CORS Configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Pagination
    DEFAULT_PAGE_SIZE = int(os.environ.get('DEFAULT_PAGE_SIZE', 50))
    MAX_PAGE_SIZE = int(os.environ.get('MAX_PAGE_SIZE', 1000))
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'backend.log')
    
    # JSON Configuration
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # Upload Configuration (para futuro)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    
    # Cache (Redis - opcional)
    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
    REDIS_DB = int(os.environ.get('REDIS_DB', 0))
    
    # RabbitMQ (opcional)
    RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'localhost')
    RABBITMQ_PORT = int(os.environ.get('RABBITMQ_PORT', 5672))
    RABBITMQ_USER = os.environ.get('RABBITMQ_USER', 'guest')
    RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD', 'guest')
    
    @staticmethod
    def init_app(app):
        """Inicialização específica da configuração"""
        pass


class DevelopmentConfig(Config):
    """Configuração para desenvolvimento"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True  # Log SQL queries
    LOG_LEVEL = 'DEBUG'


class TestingConfig(Config):
    """Configuração para testes"""
    TESTING = True
    DEBUG = True
    
    # Usar banco de dados de teste
    DB_NAME = os.environ.get('TEST_DB_NAME', 'ceu_tres_pontes_test')
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{Config.DB_USER}:{Config.DB_PASSWORD}@"
        f"{Config.DB_HOST}:{Config.DB_PORT}/{DB_NAME}?charset=utf8mb4"
    )
    
    # Desabilitar CSRF para testes
    WTF_CSRF_ENABLED = False
    
    # JWT com expiração menor para testes
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)


class ProductionConfig(Config):
    """Configuração para produção"""
    DEBUG = False
    TESTING = False
    
    # Em produção, as secret keys DEVEM vir do ambiente
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    
    # Validar que as chaves foram configuradas
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Validar configurações críticas
        if not cls.SECRET_KEY or cls.SECRET_KEY == 'dev-secret-key-change-in-production':
            raise ValueError('SECRET_KEY must be set in production')
        
        if not cls.JWT_SECRET_KEY or cls.JWT_SECRET_KEY == 'jwt-secret-key-change-in-production':
            raise ValueError('JWT_SECRET_KEY must be set in production')
        
        # Log para syslog ou outro serviço
        import logging
        from logging.handlers import SysLogHandler
        
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


# Dicionário de configurações
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
