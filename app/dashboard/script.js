// script.js - CEU Monitor (Versão com API Real)

// ========== CONFIGURAÇÃO DA API ==========
const API_BASE = '/smartceu/api/v1/dashboard';

// ========== FUNÇÕES DE API ==========
async function fetchCurrentStats() {
    try {
        const response = await fetch(`${API_BASE}/current-stats`);
        if (!response.ok) throw new Error('Erro ao buscar estatísticas');
        return await response.json();
    } catch (error) {
        console.error('Erro em fetchCurrentStats:', error);
        return null;
    }
}

async function fetchPeopleFlow() {
    try {
        const response = await fetch(`${API_BASE}/people-flow`);
        if (!response.ok) throw new Error('Erro ao buscar fluxo de pessoas');
        return await response.json();
    } catch (error) {
        console.error('Erro em fetchPeopleFlow:', error);
        return null;
    }
}

async function fetchAreasOccupation() {
    try {
        const response = await fetch(`${API_BASE}/areas-occupation`);
        if (!response.ok) throw new Error('Erro ao buscar ocupação por área');
        return await response.json();
    } catch (error) {
        console.error('Erro em fetchAreasOccupation:', error);
        return null;
    }
}

async function fetchPoolCurrent() {
    try {
        const response = await fetch(`${API_BASE}/pool/current`);
        if (!response.ok) throw new Error('Erro ao buscar status da piscina');
        return await response.json();
    } catch (error) {
        console.error('Erro em fetchPoolCurrent:', error);
        return null;
    }
}

async function fetchPoolQuality() {
    try {
        const response = await fetch(`${API_BASE}/pool/quality`);
        if (!response.ok) throw new Error('Erro ao buscar qualidade da água');
        return await response.json();
    } catch (error) {
        console.error('Erro em fetchPoolQuality:', error);
        return null;
    }
}

async function fetchActiveAlerts() {
    try {
        const response = await fetch(`${API_BASE}/alerts/active`);
        if (!response.ok) throw new Error('Erro ao buscar alertas');
        return await response.json();
    } catch (error) {
        console.error('Erro em fetchActiveAlerts:', error);
        return null;
    }
}

// ========== FUNÇÕES DE GRÁFICOS ==========
function initCharts() {
    if ($('#peopleFlowChart')) initPeopleFlowChart();
    if ($('#occupationByAreaChart')) initOccupationByAreaChart();
    if ($('#poolOccupationChart')) initPoolOccupationChart();
    if ($('#waterQualityChart')) initWaterQualityChart();
    if ($('#alertsByTypeChart')) initAlertsByTypeChart();
}

async function initPeopleFlowChart() {
    const ctx = document.getElementById('peopleFlowChart').getContext('2d');
    
    // Buscar dados reais da API
    const flowData = await fetchPeopleFlow();
    
    const labels = flowData ? flowData.labels : ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'];
    const data = flowData ? flowData.data : [25, 18, 85, 120, 180, 95];
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Pessoas no CEU',
                data: data,
                borderColor: '#3498db',
                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Número de Pessoas'
                    }
                }
            }
        }
    });
}

async function initOccupationByAreaChart() {
    const ctx = document.getElementById('occupationByAreaChart').getContext('2d');
    
    // Buscar dados reais da API
    const areasData = await fetchAreasOccupation();
    
    let labels, data;
    if (areasData && areasData.areas) {
        labels = areasData.areas.map(area => area.name);
        data = areasData.areas.map(area => area.percentage);
    } else {
        labels = ['Entrada Principal', 'Lateral Norte', 'Lateral Sul', 'Banheiros', 'Portaria'];
        data = [48, 52, 54, 65, 45];
    }
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Ocupação (%)',
                data: data,
                backgroundColor: [
                    'rgba(52, 152, 219, 0.8)',
                    'rgba(155, 89, 182, 0.8)',
                    'rgba(52, 152, 219, 0.8)',
                    'rgba(46, 204, 113, 0.8)',
                    'rgba(241, 196, 15, 0.8)'
                ],
                borderColor: [
                    'rgb(52, 152, 219)',
                    'rgb(155, 89, 182)',
                    'rgb(52, 152, 219)',
                    'rgb(46, 204, 113)',
                    'rgb(241, 196, 15)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Ocupação (%)'
                    }
                }
            }
        }
    });
}

async function initPoolOccupationChart() {
    const ctx = document.getElementById('poolOccupationChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00'],
            datasets: [{
                label: 'Ocupação da Piscina',
                data: [10, 25, 45, 60, 68, 55, 35, 15],
                borderColor: '#3498db',
                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Ocupação (%)'
                    }
                }
            }
        }
    });
}

function initWaterQualityChart() {
    const ctx = document.getElementById('waterQualityChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00'],
            datasets: [
                {
                    label: 'pH',
                    data: [7.2, 7.3, 7.4, 7.4, 7.3, 7.4, 7.3, 7.2],
                    borderColor: '#e74c3c',
                    backgroundColor: 'rgba(231, 76, 60, 0.1)',
                    tension: 0.4,
                    yAxisID: 'y'
                },
                {
                    label: 'Cloro (ppm)',
                    data: [1.8, 2.0, 2.1, 2.2, 2.0, 2.1, 1.9, 1.8],
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    tension: 0.4,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'pH'
                    },
                    min: 6.5,
                    max: 8.5
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Cloro (ppm)'
                    },
                    min: 0,
                    max: 5,
                    grid: {
                        drawOnChartArea: false,
                    },
                }
            }
        }
    });
}

function initAlertsByTypeChart() {
    const ctx = document.getElementById('alertsByTypeChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Críticos', 'Avisos', 'Informativos'],
            datasets: [{
                data: [3, 2, 1],
                backgroundColor: [
                    'rgba(231, 76, 60, 0.8)',
                    'rgba(241, 196, 15, 0.8)',
                    'rgba(52, 152, 219, 0.8)'
                ],
                borderColor: [
                    'rgb(231, 76, 60)',
                    'rgb(241, 196, 15)',
                    'rgb(52, 152, 219)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// ========== INICIALIZAÇÃO ==========
document.addEventListener('DOMContentLoaded', () => {
    if ($('#current-people')) initMainPage();
    else if ($('.areas-grid')) initAreasPage();
    else if ($('#active-alerts-list')) initAlertsPage();
    else if ($('#pool-occupancy')) initPoolPage();
    
    // Inicializar gráficos em todas as páginas
    initCharts();
});






// ========== FUNÇÕES UTILITÁRIAS ==========
const randomBetweenFloat = (min, max) => {
    const value = Math.random() * (max - min) + min;
    return Number(value.toFixed(2));
};
const randomBetween = (min, max) => Math.floor(Math.random() * (max - min) + min);
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);

// ========== PÁGINA PRINCIPAL ==========
async function initMainPage() {
    if (!$('#current-people')) return;
    
    const updateMetrics = async () => {
        // Buscar dados reais da API
        const stats = await fetchCurrentStats();
        const alerts = await fetchActiveAlerts();
        
        console.log('📊 Stats recebidos da API:', stats);
        
        if (stats) {
            // Atualizar métricas com dados reais
            console.log('✅ Atualizando current_people para:', stats.current_people);
            $('#current-people').textContent = stats.current_people;
            $('#entries-today').textContent = stats.entries_today;
            
            // Atualizar capacidade
            const capacityPercent = stats.capacity_percentage;
            updateStatus('.metric-card:nth-child(1)', capacityPercent, 60, 80, 'Dentro do limite', 'Alerta moderado', 'Capacidade crítica');
        }
        
        if (alerts) {
            // Atualizar alertas
            $('#active-alerts').textContent = alerts.total;
            
            // Contar alertas por severidade
            const critical = alerts.alerts.filter(a => a.severity === 'critical').length;
            const warning = alerts.alerts.filter(a => a.severity === 'warning').length;
            
            if (alerts.total > 0) {
                $('.metric-card:nth-child(4) .metric-subvalue').textContent = 
                    `${critical} críticos, ${warning} ${warning === 1 ? 'aviso' : 'avisos'}`;
                updateStatus('.metric-card:nth-child(4)', alerts.total, 1, 3, 'Sistema estável', 'Monitorar', 'Atenção necessária');
            } else {
                $('.metric-card:nth-child(4) .metric-subvalue').textContent = 'Nenhum alerta ativo';
                updateStatus('.metric-card:nth-child(4)', 0, 1, 3, 'Sistema estável', 'Monitorar', 'Atenção necessária');
            }
        }
    };

    // Atualizar a cada 30 segundos
    setInterval(updateMetrics, 30000);
    await updateMetrics();
}

// ========== PÁGINA DE ÁREAS ==========
async function initAreasPage() {
    if (!$('.areas-grid')) return;
    
    const updateAreaMetrics = async () => {
        // Buscar dados reais da API
        const areasData = await fetchAreasOccupation();
        
        if (areasData && areasData.areas) {
            // Atualizar cada card de área com dados reais
            $$('.area-card .metric-value').forEach((el, i) => {
                if (areasData.areas[i]) {
                    const area = areasData.areas[i];
                    el.textContent = `${area.percentage}%`;
                    
                    // Atualizar informações adicionais
                    const card = el.closest('.area-card');
                    const subvalue = card.querySelector('.metric-subvalue');
                    if (subvalue) {
                        subvalue.textContent = `${area.current}/${area.capacity} pessoas`;
                    }
                    
                    // Atualizar status
                    const statusEl = card.querySelector('.metric-status');
                    if (statusEl) {
                        if (area.status === 'critical') {
                            statusEl.textContent = 'Capacidade crítica';
                            statusEl.className = 'metric-status danger';
                        } else if (area.status === 'warning') {
                            statusEl.textContent = 'Alerta moderado';
                            statusEl.className = 'metric-status warning';
                        } else {
                            statusEl.textContent = 'Dentro do limite';
                            statusEl.className = 'metric-status normal';
                        }
                    }
                }
            });
        }
    };

    // Atualizar a cada 30 segundos
    setInterval(updateAreaMetrics, 30000);
    await updateAreaMetrics();
}

// ========== PÁGINA DE ALERTAS ==========
async function initAlertsPage() {
    if (!$('#active-alerts-list')) return;
    
    let state = { active: 5, critical: 3, resolved: 12 };

    window.resolveAlert = (id) => updateAlert(id, true);
    window.ignoreAlert = (id) => updateAlert(id, false);

    const updateAlert = (id, resolve) => {
        const alert = $(`.alert-item[data-id="${id}"]`);
        if (!alert || alert.classList.contains('resolved')) return;

        state.active--;
        if (alert.dataset.type === 'critical') state.critical--;
        if (resolve) state.resolved++;

        updateAlertsMetrics();
        
        if (resolve) {
            alert.classList.add('resolved');
            alert.querySelector('.alert-icon').className = 'alert-icon success';
            alert.querySelector('.alert-icon i').className = 'fas fa-check-circle';
            alert.querySelector('.alert-actions').innerHTML = '<button class="btn btn-resolved" disabled>Resolvido</button>';
            addToHistory(alert);
            setTimeout(() => alert.remove(), 1000);
        } else {
            alert.style.opacity = '0.5';
            setTimeout(() => alert.remove(), 500);
        }
    };

    const addToHistory = (alert) => {
        const clone = alert.cloneNode(true);
        clone.querySelector('.alert-time').textContent = 'Resolvido agora';
        $('#history-alerts-list').prepend(clone);
    };

    const updateAlertsMetrics = () => {
        $('#active-alerts').textContent = state.active;
        $('#critical-alerts').textContent = state.critical;
        $('#resolved-alerts').textContent = state.resolved;
        
        const warning = state.active - state.critical;
        $('.metric-card:nth-child(1) .metric-subvalue').textContent = 
            `${state.critical} críticos, ${warning} ${warning === 1 ? 'aviso' : 'avisos'}`;
        
        updateStatus('.metric-card:nth-child(1)', state.active, 1, 3, 'Sistema estável', 'Monitorar', 'Atenção necessária');
    };

    // Filtros
    $('#filter-type')?.addEventListener('change', filterAlerts);
    $('#filter-area')?.addEventListener('change', filterAlerts);

    const filterAlerts = () => {
        const typeFilter = $('#filter-type').value;
        const areaFilter = $('#filter-area').value;
        
        $$('#active-alerts-list .alert-item').forEach(alert => {
            const typeMatch = typeFilter === 'all' || alert.dataset.type === typeFilter;
            const areaMatch = areaFilter === 'all' || alert.dataset.area === areaFilter;
            alert.style.display = typeMatch && areaMatch ? 'flex' : 'none';
        });
    };

    // Simulação de novos alertas
    setInterval(() => {
        if (Math.random() < 0.3) {
            state.active++;
            state.critical++;
            updateAlertsMetrics();
            
            const alerts = [
                { type: 'critical', icon: 'exclamation-circle', area: 'sensors', title: 'Novo sensor com falha' },
                { type: 'warning', icon: 'thermometer-half', area: 'piscina', title: 'Temperatura da água elevada' },
                { type: 'info', icon: 'info-circle', area: 'system', title: 'Atualização disponível' }
            ];
            
            const randomAlert = alerts[Math.floor(Math.random() * alerts.length)];
            const id = Date.now();
            
            $('#active-alerts-list').insertAdjacentHTML('afterbegin', `
                <div class="alert-item" data-id="${id}" data-type="${randomAlert.type}" data-area="${randomAlert.area}">
                    <div class="alert-icon ${randomAlert.type}">
                        <i class="fas fa-${randomAlert.icon}"></i>
                    </div>
                    <div class="alert-content">
                        <h4>${randomAlert.title}</h4>
                        <p class="alert-desc">Alerta gerado automaticamente pelo sistema</p>
                        <div class="alert-meta">
                            <span class="alert-time">Agora</span>
                            <span class="alert-area">${randomAlert.area}</span>
                            <span class="alert-priority">${randomAlert.type === 'critical' ? 'Crítico' : randomAlert.type === 'warning' ? 'Aviso' : 'Informativo'}</span>
                        </div>
                    </div>
                    <div class="alert-actions">
                        <button class="btn btn-resolve" onclick="resolveAlert(${id})">Resolver</button>
                        <button class="btn btn-ignore" onclick="ignoreAlert(${id})">Ignorar</button>
                    </div>
                </div>
            `);
        }
    }, 30000);

    updateAlertsMetrics();
}

// ========== FUNÇÕES AUXILIARES ==========
function updateStatus(selector, value, warn, danger, normalText, warnText, dangerText) {
    const card = $(selector);
    const status = card.querySelector('.metric-status');
    
    if (value >= danger) updateElement(status, card, dangerText, 'danger');
    else if (value >= warn) updateElement(status, card, warnText, 'warning');
    else updateElement(status, card, normalText, 'normal');
}

function updateElement(status, card, text, type) {
    status.textContent = text;
    status.className = `metric-status status-${type}`;
    card.classList.remove('warning', 'danger');
    if (type !== 'normal') card.classList.add(type);
}

// ========== INICIALIZAÇÃO ==========
document.addEventListener('DOMContentLoaded', () => {
    if ($('#current-people')) initMainPage();
    else if ($('.areas-grid')) initAreasPage();
    else if ($('#active-alerts-list')) initAlertsPage();
});

// ========== PÁGINA DA PISCINA ==========
async function initPoolPage() {
    if (!$('#pool-occupancy')) return;

    const updatePoolMetrics = async () => {
        // Buscar dados reais da API
        const poolData = await fetchPoolCurrent();
        const qualityData = await fetchPoolQuality();
        
        if (poolData) {
            // Atualizar ocupação
            const occupancy = poolData.occupancy_percentage;
            $('#pool-occupancy').textContent = `${occupancy}%`;
            $('#pool-occupancy').nextElementSibling.textContent = 
                `${poolData.current_people} pessoas | Capacidade: ${poolData.capacity}`;

            // Atualizar status da ocupação
            const occupancyCard = $('#pool-occupancy').closest('.metric-card');
            const occupancyStatus = occupancyCard.querySelector('.metric-status');
            
            if (occupancy > 70) {
                updateElement(occupancyStatus, occupancyCard, 'Capacidade crítica', 'danger');
            } else if (occupancy > 60) {
                updateElement(occupancyStatus, occupancyCard, 'Quase na capacidade', 'warning');
            } else {
                updateElement(occupancyStatus, occupancyCard, 'Dentro do limite', 'normal');
            }

            // Atualizar entradas hoje
            $('#pool-entries-today').textContent = poolData.entries_today;

            // Atualizar temperaturas
            $('#local-temperature').textContent = `${poolData.ambient_temperature}°C`;
            $('#water-temperature').textContent = `${poolData.water_temperature}°C`;
        }
        
        if (qualityData) {
            // Atualizar qualidade da água
            $('#pool-ph').textContent = qualityData.ph.value;
            updatePoolCardStatus('#pool-ph-card', qualityData.ph.value, 
                qualityData.ph.min_safe, qualityData.ph.max_safe);

            $('#pool-chlorine').textContent = `${qualityData.chlorine.value} ppm`;
            updatePoolCardStatus('#pool-chlorine-card', qualityData.chlorine.value, 
                qualityData.chlorine.min_safe, qualityData.chlorine.max_safe);

            $('#pool-alkalinity').textContent = `${qualityData.alkalinity.value} ppm`;
            updatePoolCardStatus('#pool-alkalinity-card', qualityData.alkalinity.value, 
                qualityData.alkalinity.min_safe, qualityData.alkalinity.max_safe);
        }
    };

    const updatePoolCardStatus = (selector, value, min, max) => {
        const card = $(selector);
        const status = card.querySelector('.metric-status');
        const trend = card.querySelector('.metric-trend span');

        if (value >= min && value <= max) {
            status.textContent = 'Dentro do ideal';
            status.className = 'metric-status status-normal';
            card.classList.remove('warning', 'danger');
        } else {
            status.textContent = 'Fora do ideal';
            status.className = 'metric-status status-danger';
            card.classList.remove('warning');
            card.classList.add('danger');
        }

        // Simular tendência
        const trends = ['Estável', 'Leve aumento', 'Leve redução'];
        trend.textContent = trends[Math.floor(Math.random() * trends.length)];
    };

    // Atualizar a cada 30 segundos
    setInterval(updatePoolMetrics, 30000);
    await updatePoolMetrics();
}

// ========== INICIALIZAÇÃO ==========
document.addEventListener('DOMContentLoaded', () => {
    if ($('#current-people')) initMainPage();
    else if ($('.areas-grid')) initAreasPage();
    else if ($('#active-alerts-list')) initAlertsPage();
    else if ($('#pool-occupancy')) initPoolPage();
});
