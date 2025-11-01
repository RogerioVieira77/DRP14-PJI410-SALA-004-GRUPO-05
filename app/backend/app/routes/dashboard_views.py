"""
Dashboard Views
Rotas para servir páginas HTML usando templates Jinja2
"""

from flask import Blueprint, render_template, current_app

# Criar blueprint para views do dashboard
views_bp = Blueprint(
    'dashboard_views', 
    __name__,
    url_prefix='/smartceu/dashboard'
)


@views_bp.route('/')
@views_bp.route('/index')
def index():
    """
    Página principal do dashboard
    """
    return render_template(
        'dashboard/index.html',
        page_title='Painel Principal',
        active_page='index',
        user_name='Administrador'
    )


@views_bp.route('/areas')
@views_bp.route('/areas.html')
def areas():
    """
    Página de monitoramento por áreas
    """
    return render_template(
        'dashboard/areas.html',
        page_title='Áreas',
        active_page='areas',
        user_name='Administrador'
    )


@views_bp.route('/alertas')
@views_bp.route('/alertas.html')
def alertas():
    """
    Página de alertas do sistema
    """
    return render_template(
        'dashboard/alertas.html',
        page_title='Alertas',
        active_page='alertas',
        user_name='Administrador'
    )


@views_bp.route('/piscina')
@views_bp.route('/piscina.html')
def piscina():
    """
    Página de monitoramento da piscina
    """
    return render_template(
        'dashboard/piscina.html',
        page_title='Monitoramento da Piscina',
        active_page='piscina',
        user_name='Administrador'
    )


@views_bp.route('/resumo-sensores')
@views_bp.route('/resumo-sensores.html')
def resumo_sensores():
    """
    Página de resumo de sensores
    """
    return render_template(
        'dashboard/resumo-sensores.html',
        page_title='Resumo de Sensores',
        active_page='resumo-sensores',
        user_name='Administrador'
    )
