"""
Funções auxiliares para respostas HTTP padronizadas
"""

from flask import jsonify
from typing import Any, Dict, List


def success_response(data: Any, message: str = None, status: int = 200) -> tuple:
    """
    Resposta de sucesso padronizada
    
    Args:
        data: Dados a retornar
        message: Mensagem de sucesso (opcional)
        status: Código HTTP
        
    Returns:
        tuple: (response, status_code)
    """
    response = {}
    
    if message:
        response['message'] = message
    
    if isinstance(data, dict):
        response.update(data)
    else:
        response['data'] = data
    
    return jsonify(response), status


def error_response(error: str, status: int = 400, details: Any = None) -> tuple:
    """
    Resposta de erro padronizada
    
    Args:
        error: Mensagem de erro
        status: Código HTTP
        details: Detalhes adicionais (opcional)
        
    Returns:
        tuple: (response, status_code)
    """
    response = {'error': error}
    
    if details:
        response['details'] = details
    
    return jsonify(response), status


def paginated_response(
    items: List[Any],
    total: int,
    page: int = 1,
    per_page: int = 50
) -> tuple:
    """
    Resposta paginada padronizada
    
    Args:
        items: Lista de itens
        total: Total de itens
        page: Página atual
        per_page: Itens por página
        
    Returns:
        tuple: (response, status_code)
    """
    total_pages = (total + per_page - 1) // per_page
    
    response = {
        'items': items,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    }
    
    return jsonify(response), 200
