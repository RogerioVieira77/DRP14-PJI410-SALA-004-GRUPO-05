"""
Backend Flask Application - CEU Tres Pontes
Sistema de Controle de Acesso e Contagem de Pessoas

Fase 3: API REST + MySQL + MQTT Integration
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_marshmallow import Marshmallow
import logging
from logging.handlers import RotatingFileHandler
import os

# Inicializar extensões
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
ma = Marshmallow()


def create_app(config_name='development'):
    """
    Application Factory Pattern
    Cria e configura a aplicação Flask
    
    Args:
        config_name: Nome da configuração ('development', 'testing', 'production')
    
    Returns:
        Flask app configurada
    """
    app = Flask(__name__)
    
    # Carregar configurações
    from app.config import config
    app.config.from_object(config[config_name])
    
    # Inicializar extensões com app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    
    # Configurar CORS - Permitir todas as origens para desenvolvimento
    CORS(app, resources={
        r"/*": {
            "origins": "*",  # Permitir todas as origens em desenvolvimento
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": False
        }
    })
    
    # Configurar logging
    setup_logging(app)
    
    # Registrar blueprints
    register_blueprints(app)
    
    # Registrar error handlers
    register_error_handlers(app)
    
    # Registrar shell context
    register_shell_context(app)
    
    # Log de inicialização
    app.logger.info("=" * 50)
    app.logger.info("CEU Tres Pontes Backend iniciado")
    app.logger.info(f"Ambiente: {config_name}")
    app.logger.info(f"Debug: {app.config['DEBUG']}")
    app.logger.info("=" * 50)
    
    return app


def setup_logging(app):
    """Configura sistema de logging"""
    if not app.debug and not app.testing:
        # Criar diretório de logs se não existir
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Configurar handler de arquivo com rotação
        log_file = os.path.join(log_dir, app.config.get('LOG_FILE', 'backend.log'))
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        
        # Formato do log
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        )
        file_handler.setFormatter(formatter)
        
        # Configurar nível de log
        log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO'))
        file_handler.setLevel(log_level)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(log_level)
    
    # Console handler para desenvolvimento
    if app.debug:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        app.logger.addHandler(console_handler)
        app.logger.setLevel(logging.DEBUG)


def register_blueprints(app):
    """Registra blueprints da aplicação"""
    from app.routes import sensors, readings, statistics, auth, health, pool
    from flask import send_from_directory
    import os
    
    # Rota para servir a página de teste
    @app.route('/')
    def index():
        """Serve a página de teste"""
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return send_from_directory(project_root, 'test_page.html')
    
    # Prefixo da API
    api_prefix = app.config.get('API_PREFIX', '/api/v1')
    
    # Registrar blueprints
    app.register_blueprint(health.bp)  # Sem prefixo (health check)
    app.register_blueprint(auth.bp, url_prefix=f'{api_prefix}/auth')
    app.register_blueprint(sensors.bp, url_prefix=f'{api_prefix}/sensors')
    app.register_blueprint(readings.bp, url_prefix=f'{api_prefix}/readings')
    app.register_blueprint(statistics.bp, url_prefix=f'{api_prefix}/statistics')
    app.register_blueprint(pool.pool_bp)  # Pool já tem o prefix definido
    
    app.logger.info(f"Blueprints registrados com prefixo: {api_prefix}")


def register_error_handlers(app):
    """Registra handlers de erros globais (refatorados)"""
    from app.utils.error_handlers import register_error_handlers as setup_handlers
    setup_handlers(app)


def register_shell_context(app):
    """Registra contexto do shell para Flask shell"""
    @app.shell_context_processor
    def make_shell_context():
        from app.models import Sensor, Reading, Alert, Statistics
        return {
            'db': db,
            'Sensor': Sensor,
            'Reading': Reading,
            'Alert': Alert,
            'Statistics': Statistics
        }
