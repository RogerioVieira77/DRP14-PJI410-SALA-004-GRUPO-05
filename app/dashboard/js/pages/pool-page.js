// pool-page.js - Lógica da página de monitoramento da piscina
import { fetchPoolCurrent, fetchPoolQuality } from '../api.js';
import { $, updateElement, updateStatus } from '../utils.js';

/**
 * Inicializa a página de piscina
 */
export async function initPoolPage() {
    console.log('🏊 Inicializando página de piscina...');
    
    // Primeira atualização
    await updatePoolData();
    
    // Auto-refresh a cada 30 segundos
    setInterval(updatePoolData, 30000);
}

/**
 * Atualiza todos os dados da piscina
 */
async function updatePoolData() {
    // Buscar dados em paralelo
    const [currentData, qualityData] = await Promise.all([
        fetchPoolCurrent(),
        fetchPoolQuality()
    ]);
    
    if (currentData) {
        updateCurrentMetrics(currentData);
        updateOccupation(currentData);
    }
    
    if (qualityData) {
        updateWaterQuality(qualityData);
    }
}

/**
 * Atualiza métricas atuais (temperatura, horário)
 */
function updateCurrentMetrics(data) {
    // Temperatura da água
    if (data.temperature !== undefined) {
        const tempElement = $('#pool-temperature');
        if (tempElement) {
            tempElement.textContent = `${data.temperature.toFixed(1)}°C`;
            
            // Atualizar status visual baseado na temperatura
            const tempStatus = getTemperatureStatus(data.temperature);
            updateStatus(tempElement, tempStatus.class);
        }
    }
    
    // Temperatura ambiente
    if (data.ambient_temperature !== undefined) {
        updateElement('#ambient-temperature', `${data.ambient_temperature.toFixed(1)}°C`);
    }
    
    // Última atualização
    if (data.last_update) {
        updateElement('#pool-last-update', formatTime(data.last_update));
    }
    
    // Status operacional
    const operationalStatus = data.operational_status || 'unknown';
    updateOperationalStatus(operationalStatus);
}

/**
 * Atualiza dados de ocupação
 */
function updateOccupation(data) {
    const currentPeople = data.current_people || 0;
    const capacity = data.capacity || 50;
    const percentage = capacity > 0 ? (currentPeople / capacity) * 100 : 0;
    
    // Atualizar números
    updateElement('#pool-current-people', currentPeople);
    updateElement('#pool-capacity', capacity);
    updateElement('#pool-available', capacity - currentPeople);
    
    // Atualizar percentual e barra de progresso
    const percentageElement = $('#pool-occupation-percentage');
    if (percentageElement) {
        percentageElement.textContent = `${percentage.toFixed(0)}%`;
    }
    
    const progressBar = $('#pool-occupation-bar');
    if (progressBar) {
        progressBar.style.width = `${Math.min(percentage, 100)}%`;
        
        // Atualizar cor baseado na ocupação
        progressBar.className = 'progress-fill';
        if (percentage >= 90) {
            progressBar.classList.add('critical');
        } else if (percentage >= 75) {
            progressBar.classList.add('warning');
        } else if (percentage >= 50) {
            progressBar.classList.add('moderate');
        } else {
            progressBar.classList.add('normal');
        }
    }
    
    // Atualizar status de ocupação
    updateOccupationStatus(percentage);
}

/**
 * Atualiza qualidade da água
 */
function updateWaterQuality(data) {
    // pH
    if (data.ph !== undefined) {
        updateQualityMetric('ph', data.ph, 7.2, 7.8);
    }
    
    // Cloro
    if (data.chlorine !== undefined) {
        updateQualityMetric('chlorine', data.chlorine, 1.0, 3.0);
    }
    
    // Alcalinidade
    if (data.alkalinity !== undefined) {
        updateQualityMetric('alkalinity', data.alkalinity, 80, 120);
    }
    
    // Turbidez
    if (data.turbidity !== undefined) {
        updateQualityMetric('turbidity', data.turbidity, 0, 5, true); // menor é melhor
    }
    
    // Status geral da qualidade
    updateOverallQualityStatus(data);
}

/**
 * Atualiza uma métrica de qualidade individual
 */
function updateQualityMetric(metricName, value, minIdeal, maxIdeal, lowerIsBetter = false) {
    const valueElement = $(`#${metricName}-value`);
    const statusElement = $(`#${metricName}-status`);
    
    if (!valueElement) return;
    
    // Atualizar valor
    valueElement.textContent = value.toFixed(2);
    
    // Determinar status
    let status, statusText, statusClass;
    
    if (lowerIsBetter) {
        if (value <= maxIdeal) {
            status = 'optimal';
            statusText = 'Ideal';
            statusClass = 'status-optimal';
        } else if (value <= maxIdeal * 1.5) {
            status = 'warning';
            statusText = 'Atenção';
            statusClass = 'status-warning';
        } else {
            status = 'critical';
            statusText = 'Crítico';
            statusClass = 'status-critical';
        }
    } else {
        if (value >= minIdeal && value <= maxIdeal) {
            status = 'optimal';
            statusText = 'Ideal';
            statusClass = 'status-optimal';
        } else if (value >= minIdeal * 0.9 && value <= maxIdeal * 1.1) {
            status = 'warning';
            statusText = 'Atenção';
            statusClass = 'status-warning';
        } else {
            status = 'critical';
            statusText = 'Crítico';
            statusClass = 'status-critical';
        }
    }
    
    // Atualizar visual do status
    if (statusElement) {
        statusElement.textContent = statusText;
        statusElement.className = `quality-status ${statusClass}`;
    }
    
    // Atualizar cor do card
    const card = valueElement.closest('.quality-card');
    if (card) {
        card.className = `quality-card ${statusClass}`;
    }
}

/**
 * Atualiza status geral da qualidade
 */
function updateOverallQualityStatus(data) {
    const statusElement = $('#overall-quality-status');
    if (!statusElement) return;
    
    // Verificar se todos os parâmetros estão ideais
    const ph = data.ph || 0;
    const chlorine = data.chlorine || 0;
    const alkalinity = data.alkalinity || 0;
    const turbidity = data.turbidity || 0;
    
    const phOk = ph >= 7.2 && ph <= 7.8;
    const chlorineOk = chlorine >= 1.0 && chlorine <= 3.0;
    const alkalinityOk = alkalinity >= 80 && alkalinity <= 120;
    const turbidityOk = turbidity <= 5;
    
    if (phOk && chlorineOk && alkalinityOk && turbidityOk) {
        statusElement.innerHTML = `
            <span class="badge badge-success">
                <i class="fas fa-check-circle"></i> Excelente
            </span>
        `;
    } else if (!phOk || !chlorineOk) {
        statusElement.innerHTML = `
            <span class="badge badge-danger">
                <i class="fas fa-exclamation-triangle"></i> Requer Atenção
            </span>
        `;
    } else {
        statusElement.innerHTML = `
            <span class="badge badge-warning">
                <i class="fas fa-exclamation-circle"></i> Aceitável
            </span>
        `;
    }
}

/**
 * Retorna status da temperatura
 */
function getTemperatureStatus(temp) {
    if (temp >= 26 && temp <= 29) {
        return { class: 'optimal', text: 'Ideal' };
    } else if (temp >= 24 && temp <= 31) {
        return { class: 'warning', text: 'Aceitável' };
    } else {
        return { class: 'critical', text: 'Fora do ideal' };
    }
}

/**
 * Atualiza status operacional
 */
function updateOperationalStatus(status) {
    const statusElement = $('#operational-status');
    if (!statusElement) return;
    
    const statuses = {
        open: { icon: 'fa-check-circle', text: 'Aberta', class: 'badge-success' },
        closed: { icon: 'fa-times-circle', text: 'Fechada', class: 'badge-danger' },
        maintenance: { icon: 'fa-tools', text: 'Manutenção', class: 'badge-warning' },
        unknown: { icon: 'fa-question-circle', text: 'Desconhecido', class: 'badge-secondary' }
    };
    
    const statusConfig = statuses[status] || statuses.unknown;
    
    statusElement.innerHTML = `
        <span class="badge ${statusConfig.class}">
            <i class="fas ${statusConfig.icon}"></i> ${statusConfig.text}
        </span>
    `;
}

/**
 * Atualiza status de ocupação
 */
function updateOccupationStatus(percentage) {
    const statusElement = $('#occupation-status');
    if (!statusElement) return;
    
    let statusHtml;
    
    if (percentage >= 90) {
        statusHtml = `
            <span class="badge badge-danger">
                <i class="fas fa-exclamation-triangle"></i> Lotada
            </span>
        `;
    } else if (percentage >= 75) {
        statusHtml = `
            <span class="badge badge-warning">
                <i class="fas fa-exclamation-circle"></i> Cheia
            </span>
        `;
    } else if (percentage >= 50) {
        statusHtml = `
            <span class="badge badge-info">
                <i class="fas fa-users"></i> Moderada
            </span>
        `;
    } else {
        statusHtml = `
            <span class="badge badge-success">
                <i class="fas fa-check"></i> Disponível
            </span>
        `;
    }
    
    statusElement.innerHTML = statusHtml;
}

/**
 * Formata hora
 */
function formatTime(timestamp) {
    if (!timestamp) return '--:--';
    
    const date = new Date(timestamp);
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    
    return `${hours}:${minutes}`;
}
