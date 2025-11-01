// areas-page.js - Lógica da página de monitoramento de áreas
import { fetchAreasOccupation } from '../api.js';
import { $, updateStatus, updateElement } from '../utils.js';

/**
 * Inicializa a página de áreas
 */
export async function initAreasPage() {
    console.log('🏢 Inicializando página de áreas...');
    
    // Primeira atualização
    await updateAreasData();
    
    // Auto-refresh a cada 30 segundos
    setInterval(updateAreasData, 30000);
}

/**
 * Atualiza dados de todas as áreas
 */
async function updateAreasData() {
    const data = await fetchAreasOccupation();
    
    if (!data || !data.areas) {
        console.warn('Nenhum dado de áreas disponível');
        return;
    }
    
    // Atualizar resumo geral
    updateGeneralSummary(data);
    
    // Atualizar tabela de áreas
    updateAreasTable(data.areas);
    
    // Atualizar status de alertas
    updateCapacityAlerts(data.areas);
}

/**
 * Atualiza cards de resumo geral
 */
function updateGeneralSummary(data) {
    const totalAreas = data.areas?.length || 0;
    const criticalAreas = data.areas?.filter(a => a.occupation_percentage >= 90).length || 0;
    const warningAreas = data.areas?.filter(a => a.occupation_percentage >= 75 && a.occupation_percentage < 90).length || 0;
    const totalOccupancy = data.total_people || 0;
    
    updateElement('#total-areas', totalAreas);
    updateElement('#critical-areas', criticalAreas);
    updateElement('#warning-areas', warningAreas);
    updateElement('#total-occupancy', totalOccupancy);
}

/**
 * Atualiza tabela de áreas
 */
function updateAreasTable(areas) {
    const tbody = $('#areas-table-body');
    if (!tbody) return;
    
    // Ordenar por percentual de ocupação (decrescente)
    const sortedAreas = [...areas].sort((a, b) => 
        (b.occupation_percentage || 0) - (a.occupation_percentage || 0)
    );
    
    tbody.innerHTML = sortedAreas.map(area => {
        const percentage = area.occupation_percentage || 0;
        const status = getAreaStatus(percentage);
        const statusClass = getStatusClass(percentage);
        
        return `
            <tr class="area-row ${statusClass}">
                <td class="area-name">
                    <i class="fas fa-map-marker-alt"></i>
                    ${area.name || 'Sem nome'}
                </td>
                <td class="area-current">${area.current_people || 0}</td>
                <td class="area-capacity">${area.capacity || 0}</td>
                <td class="area-percentage">
                    <div class="progress-bar">
                        <div class="progress-fill ${statusClass}" 
                             style="width: ${Math.min(percentage, 100)}%">
                        </div>
                        <span class="progress-text">${percentage.toFixed(0)}%</span>
                    </div>
                </td>
                <td class="area-status">
                    <span class="badge badge-${statusClass}">${status}</span>
                </td>
                <td class="area-actions">
                    <button class="btn-sm btn-details" 
                            onclick="viewAreaDetails('${area.id}')">
                        <i class="fas fa-eye"></i> Detalhes
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

/**
 * Retorna status textual baseado no percentual
 */
function getAreaStatus(percentage) {
    if (percentage >= 90) return 'Crítico';
    if (percentage >= 75) return 'Atenção';
    if (percentage >= 50) return 'Moderado';
    return 'Normal';
}

/**
 * Retorna classe CSS baseada no percentual
 */
function getStatusClass(percentage) {
    if (percentage >= 90) return 'critical';
    if (percentage >= 75) return 'warning';
    if (percentage >= 50) return 'moderate';
    return 'normal';
}

/**
 * Atualiza alertas de capacidade
 */
function updateCapacityAlerts(areas) {
    const alertsContainer = $('#capacity-alerts');
    if (!alertsContainer) return;
    
    // Filtrar áreas críticas e de atenção
    const criticalAreas = areas.filter(a => (a.occupation_percentage || 0) >= 90);
    const warningAreas = areas.filter(a => {
        const pct = a.occupation_percentage || 0;
        return pct >= 75 && pct < 90;
    });
    
    if (criticalAreas.length === 0 && warningAreas.length === 0) {
        alertsContainer.innerHTML = `
            <div class="alert alert-success">
                <i class="fas fa-check-circle"></i>
                Todas as áreas estão com ocupação normal
            </div>
        `;
        return;
    }
    
    let alertsHtml = '';
    
    // Alertas críticos
    if (criticalAreas.length > 0) {
        alertsHtml += criticalAreas.map(area => `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle"></i>
                <strong>${area.name}</strong>: Capacidade crítica 
                (${area.current_people}/${area.capacity} - ${area.occupation_percentage.toFixed(0)}%)
            </div>
        `).join('');
    }
    
    // Alertas de atenção
    if (warningAreas.length > 0) {
        alertsHtml += warningAreas.map(area => `
            <div class="alert alert-warning">
                <i class="fas fa-exclamation-circle"></i>
                <strong>${area.name}</strong>: Atenção na ocupação 
                (${area.current_people}/${area.capacity} - ${area.occupation_percentage.toFixed(0)}%)
            </div>
        `).join('');
    }
    
    alertsContainer.innerHTML = alertsHtml;
}

/**
 * Função global para visualizar detalhes de uma área
 * (Será acessada pelo onclick nos botões)
 */
window.viewAreaDetails = function(areaId) {
    console.log('Visualizando detalhes da área:', areaId);
    // TODO: Implementar modal ou página de detalhes
    alert(`Detalhes da área ${areaId} serão implementados em breve`);
};
