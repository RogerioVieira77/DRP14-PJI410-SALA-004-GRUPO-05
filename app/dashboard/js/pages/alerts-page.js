// alerts-page.js - Lógica da página de alertas
import { fetchActiveAlerts } from '../api.js';
import { $, formatTimestamp, formatRelativeTime } from '../utils.js';

// Estado dos filtros
let currentFilters = {
    type: 'all',      // all, capacity, security, maintenance, system
    priority: 'all',  // all, high, medium, low
    status: 'active'  // all, active, resolved, ignored
};

/**
 * Inicializa a página de alertas
 */
export async function initAlertsPage() {
    console.log('🚨 Inicializando página de alertas...');
    
    // Configurar event listeners dos filtros
    setupFilterListeners();
    
    // Primeira atualização
    await updateAlertsData();
    
    // Auto-refresh a cada 15 segundos (alertas precisam ser mais rápidos)
    setInterval(updateAlertsData, 15000);
}

/**
 * Configura listeners dos filtros
 */
function setupFilterListeners() {
    // Filtro de tipo
    const typeFilter = $('#filter-type');
    if (typeFilter) {
        typeFilter.addEventListener('change', (e) => {
            currentFilters.type = e.target.value;
            updateAlertsData();
        });
    }
    
    // Filtro de prioridade
    const priorityFilter = $('#filter-priority');
    if (priorityFilter) {
        priorityFilter.addEventListener('change', (e) => {
            currentFilters.priority = e.target.value;
            updateAlertsData();
        });
    }
    
    // Filtro de status
    const statusFilter = $('#filter-status');
    if (statusFilter) {
        statusFilter.addEventListener('change', (e) => {
            currentFilters.status = e.target.value;
            updateAlertsData();
        });
    }
}

/**
 * Atualiza dados de alertas
 */
async function updateAlertsData() {
    const data = await fetchActiveAlerts();
    
    if (!data || !data.alerts) {
        console.warn('Nenhum alerta disponível');
        showNoAlerts();
        return;
    }
    
    // Aplicar filtros
    const filteredAlerts = filterAlerts(data.alerts);
    
    // Atualizar resumo
    updateAlertsSummary(data.alerts);
    
    // Atualizar lista de alertas
    updateAlertsList(filteredAlerts);
}

/**
 * Aplica filtros aos alertas
 */
function filterAlerts(alerts) {
    return alerts.filter(alert => {
        // Filtro de tipo
        if (currentFilters.type !== 'all' && alert.type !== currentFilters.type) {
            return false;
        }
        
        // Filtro de prioridade
        if (currentFilters.priority !== 'all' && alert.priority !== currentFilters.priority) {
            return false;
        }
        
        // Filtro de status
        if (currentFilters.status !== 'all' && alert.status !== currentFilters.status) {
            return false;
        }
        
        return true;
    });
}

/**
 * Atualiza cards de resumo
 */
function updateAlertsSummary(alerts) {
    const totalAlerts = alerts.length;
    const highPriority = alerts.filter(a => a.priority === 'high').length;
    const activeAlerts = alerts.filter(a => a.status === 'active').length;
    const resolvedToday = alerts.filter(a => {
        if (a.status !== 'resolved') return false;
        const today = new Date().toDateString();
        const alertDate = new Date(a.resolved_at).toDateString();
        return today === alertDate;
    }).length;
    
    const totalElement = $('#total-alerts');
    const highElement = $('#high-priority-alerts');
    const activeElement = $('#active-alerts');
    const resolvedElement = $('#resolved-today');
    
    if (totalElement) totalElement.textContent = totalAlerts;
    if (highElement) highElement.textContent = highPriority;
    if (activeElement) activeElement.textContent = activeAlerts;
    if (resolvedElement) resolvedElement.textContent = resolvedToday;
}

/**
 * Atualiza lista de alertas
 */
function updateAlertsList(alerts) {
    const container = $('#alerts-list');
    if (!container) return;
    
    if (alerts.length === 0) {
        showNoAlerts();
        return;
    }
    
    // Ordenar por prioridade e data
    const sortedAlerts = [...alerts].sort((a, b) => {
        // Prioridade: high > medium > low
        const priorityOrder = { high: 3, medium: 2, low: 1 };
        const priorityDiff = (priorityOrder[b.priority] || 0) - (priorityOrder[a.priority] || 0);
        
        if (priorityDiff !== 0) return priorityDiff;
        
        // Se mesma prioridade, ordenar por data (mais recente primeiro)
        return new Date(b.created_at) - new Date(a.created_at);
    });
    
    container.innerHTML = sortedAlerts.map(alert => {
        const priorityClass = getPriorityClass(alert.priority);
        const typeIcon = getTypeIcon(alert.type);
        const statusBadge = getStatusBadge(alert.status);
        
        return `
            <div class="alert-card ${priorityClass} ${alert.status}">
                <div class="alert-header">
                    <div class="alert-type">
                        <i class="fas ${typeIcon}"></i>
                        <span>${getTypeLabel(alert.type)}</span>
                    </div>
                    <div class="alert-priority">
                        ${getPriorityBadge(alert.priority)}
                    </div>
                </div>
                
                <div class="alert-body">
                    <h4 class="alert-title">${alert.title || 'Sem título'}</h4>
                    <p class="alert-message">${alert.message || 'Sem descrição'}</p>
                    
                    <div class="alert-meta">
                        <span class="alert-time">
                            <i class="fas fa-clock"></i>
                            ${formatRelativeTime(alert.created_at)}
                        </span>
                        ${alert.area ? `
                            <span class="alert-location">
                                <i class="fas fa-map-marker-alt"></i>
                                ${alert.area}
                            </span>
                        ` : ''}
                    </div>
                </div>
                
                <div class="alert-footer">
                    <div class="alert-status">
                        ${statusBadge}
                    </div>
                    <div class="alert-actions">
                        ${alert.status === 'active' ? `
                            <button class="btn-sm btn-resolve" 
                                    onclick="resolveAlert('${alert.id}')">
                                <i class="fas fa-check"></i> Resolver
                            </button>
                            <button class="btn-sm btn-ignore" 
                                    onclick="ignoreAlert('${alert.id}')">
                                <i class="fas fa-times"></i> Ignorar
                            </button>
                        ` : ''}
                        <button class="btn-sm btn-details" 
                                onclick="viewAlertDetails('${alert.id}')">
                            <i class="fas fa-info-circle"></i> Detalhes
                        </button>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

/**
 * Mostra mensagem quando não há alertas
 */
function showNoAlerts() {
    const container = $('#alerts-list');
    if (!container) return;
    
    container.innerHTML = `
        <div class="no-alerts">
            <i class="fas fa-check-circle"></i>
            <h3>Nenhum alerta encontrado</h3>
            <p>Todos os sistemas estão funcionando normalmente</p>
        </div>
    `;
}

/**
 * Retorna classe CSS da prioridade
 */
function getPriorityClass(priority) {
    const classes = {
        high: 'priority-high',
        medium: 'priority-medium',
        low: 'priority-low'
    };
    return classes[priority] || 'priority-low';
}

/**
 * Retorna ícone do tipo de alerta
 */
function getTypeIcon(type) {
    const icons = {
        capacity: 'fa-users',
        security: 'fa-shield-alt',
        maintenance: 'fa-tools',
        system: 'fa-server',
        sensor: 'fa-sensor',
        other: 'fa-exclamation-triangle'
    };
    return icons[type] || icons.other;
}

/**
 * Retorna label do tipo
 */
function getTypeLabel(type) {
    const labels = {
        capacity: 'Capacidade',
        security: 'Segurança',
        maintenance: 'Manutenção',
        system: 'Sistema',
        sensor: 'Sensor',
        other: 'Outro'
    };
    return labels[type] || 'Outro';
}

/**
 * Retorna badge de prioridade
 */
function getPriorityBadge(priority) {
    const badges = {
        high: '<span class="badge badge-danger">Alta</span>',
        medium: '<span class="badge badge-warning">Média</span>',
        low: '<span class="badge badge-info">Baixa</span>'
    };
    return badges[priority] || badges.low;
}

/**
 * Retorna badge de status
 */
function getStatusBadge(status) {
    const badges = {
        active: '<span class="badge badge-danger">Ativo</span>',
        resolved: '<span class="badge badge-success">Resolvido</span>',
        ignored: '<span class="badge badge-secondary">Ignorado</span>'
    };
    return badges[status] || badges.active;
}

/**
 * Funções globais para ações nos alertas
 */
window.resolveAlert = async function(alertId) {
    console.log('Resolvendo alerta:', alertId);
    // TODO: Implementar chamada à API para resolver alerta
    alert(`Alerta ${alertId} marcado como resolvido`);
    await updateAlertsData();
};

window.ignoreAlert = async function(alertId) {
    console.log('Ignorando alerta:', alertId);
    // TODO: Implementar chamada à API para ignorar alerta
    alert(`Alerta ${alertId} ignorado`);
    await updateAlertsData();
};

window.viewAlertDetails = function(alertId) {
    console.log('Visualizando detalhes do alerta:', alertId);
    // TODO: Implementar modal ou página de detalhes
    alert(`Detalhes do alerta ${alertId} serão implementados em breve`);
};
