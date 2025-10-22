"""
Handlers de erro globais
"""

from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, OperationalError
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
    """
    Registrar handlers de erro na aplicação
    
    Args:
        app: Instância do Flask
    """
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Tratar erros de validação do Marshmallow"""
        return jsonify({
            'error': 'Erro de validação',
            'messages': error.messages
        }), 400
    
    @app.errorhandler(ValueError)
    def handle_value_error(error):
        """Tratar erros de valor (lógica de negócio)"""
        return jsonify({
            'error': str(error)
        }), 400
    
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        """Tratar erros de integridade do banco"""
        return jsonify({
            'error': 'Erro de integridade de dados',
            'details': 'Violação de constraint do banco de dados'
        }), 409
    
    @app.errorhandler(OperationalError)
    def handle_operational_error(error):
        """Tratar erros operacionais do banco"""
        return jsonify({
            'error': 'Erro de banco de dados',
            'details': 'Não foi possível conectar ao banco de dados'
        }), 503
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Tratar exceções HTTP"""
        return jsonify({
            'error': error.description
        }), error.code
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """Tratar erro 404"""
        return jsonify({
            'error': 'Recurso não encontrado'
        }), 404
    
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Tratar erro 405"""
        return jsonify({
            'error': 'Método não permitido'
        }), 405
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        """Tratar erro 500"""
        app.logger.error(f'Erro interno: {error}')
        return jsonify({
            'error': 'Erro interno do servidor'
        }), 500
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Tratar erros inesperados"""
        app.logger.error(f'Erro inesperado: {error}', exc_info=True)
        return jsonify({
            'error': 'Erro inesperado',
            'details': str(error) if app.debug else 'Entre em contato com o suporte'
        }), 500
