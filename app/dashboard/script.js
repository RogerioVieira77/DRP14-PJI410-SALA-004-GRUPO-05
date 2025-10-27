// script.js - CEU Monitor (Versão Otimizada)

// ========== FUNÇÕES DE GRÁFICOS ==========
function initCharts() {
    if ($('#peopleFlowChart')) initPeopleFlowChart();
    if ($('#occupationByAreaChart')) initOccupationByAreaChart();
    if ($('#poolOccupationChart')) initPoolOccupationChart();
    if ($('#waterQualityChart')) initWaterQualityChart();
    if ($('#alertsByTypeChart')) initAlertsByTypeChart();
}

function initPeopleFlowChart() {
    const ctx = document.getElementById('peopleFlowChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '23:59'],
            datasets: [{
                label: 'Pessoas no CEU',
                data: [25, 18, 85, 120, 180, 95, 45],
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

function initOccupationByAreaChart() {
    const ctx = document.getElementById('occupationByAreaChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Piscinas', 'Auditórios', 'Salas Multiuso', 'Quadras', 'Biblioteca', 'Convivência'],
            datasets: [{
                label: 'Ocupação (%)',
                data: [68, 35, 55, 45, 22, 38],
                backgroundColor: [
                    'rgba(52, 152, 219, 0.8)',
                    'rgba(155, 89, 182, 0.8)',
                    'rgba(52, 152, 219, 0.8)',
                    'rgba(46, 204, 113, 0.8)',
                    'rgba(241, 196, 15, 0.8)',
                    'rgba(230, 126, 34, 0.8)'
                ],
                borderColor: [
                    'rgb(52, 152, 219)',
                    'rgb(155, 89, 182)',
                    'rgb(52, 152, 219)',
                    'rgb(46, 204, 113)',
                    'rgb(241, 196, 15)',
                    'rgb(230, 126, 34)'
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

function initPoolOccupationChart() {
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
function initMainPage() {
    if (!$('#current-people')) return;
    
    const updateMetrics = () => {
        const metrics = {
            'current-people': { min: 80, max: 200, calc: val => Math.round((val / 400) * 100) },
            'entries-today': { min: 300, max: 500 },
            'active-alerts': { min: 1, max: 5 }
        };

        Object.entries(metrics).forEach(([id, config]) => {
            const value = randomBetween(config.min, config.max);
            $(`#${id}`).textContent = config.calc ? config.calc(value) : value;
        });

        // Status da capacidade
        const capacity = +$('#current-people').textContent;
        updateStatus('.metric-card:nth-child(1)', capacity, 60, 80, 'Dentro do limite', 'Alerta moderado', 'Capacidade crítica');
        
        // Status dos alertas
        const alerts = +$('#active-alerts').textContent;
        const critical = Math.min(alerts - 1, 2);
        const warning = alerts - critical;
        $('.metric-card:nth-child(4) .metric-subvalue').textContent = `${critical} críticos, ${warning} ${warning === 1 ? 'aviso' : 'avisos'}`;
        updateStatus('.metric-card:nth-child(4)', alerts, 1, 3, 'Sistema estável', 'Monitorar', 'Atenção necessária');
    };

    setInterval(updateMetrics, 10000);
    updateMetrics();
}

// ========== PÁGINA DE ÁREAS ==========
function initAreasPage() {
    if (!$('.areas-grid')) return;
    
    const updateAreaMetrics = () => {
        const areas = [
            { min: 50, max: 80 }, { min: 20, max: 60 }, { min: 30, max: 60 },
            { min: 15, max: 50 }, { min: 5, max: 25 }, { min: 20, max: 40 }
        ];

        $$('.area-card .metric-value').forEach((el, i) => {
            const value = randomBetween(areas[i].min, areas[i].max);
            el.textContent = `${value}%`;
            
            const card = el.closest('.area-card');
            const status = card.querySelector('.metric-status');
            
            if (value > 70) updateElement(status, card, 'Capacidade crítica', 'danger');
            else if (value > 50) updateElement(status, card, 'Quase na capacidade', 'warning');
            else updateElement(status, card, value > 25 ? 'Dentro do normal' : 'Baixa ocupação', 'normal');
        });
    };

    setInterval(updateAreaMetrics, 10000);
    updateAreaMetrics();
}

// ========== PÁGINA DE ALERTAS ==========
function initAlertsPage() {
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
function initPoolPage() {
    if (!$('#pool-occupancy')) return;

    const updatePoolMetrics = () => {
        // Atualizar ocupação
        const occupancy = randomBetween(50, 80);
        $('#pool-occupancy').textContent = `${occupancy}%`;
        const people = Math.round((occupancy / 100) * 60);
        $('#pool-occupancy').nextElementSibling.textContent = `${people} pessoas | Capacidade: 60`;

        // Atualizar status da ocupação
        if (occupancy > 70) {
            updateElement($('#pool-occupancy').closest('.metric-card').querySelector('.metric-status'), 
                         $('#pool-occupancy').closest('.metric-card'), 
                         'Capacidade crítica', 'danger');
        } else if (occupancy > 60) {
            updateElement($('#pool-occupancy').closest('.metric-card').querySelector('.metric-status'), 
                         $('#pool-occupancy').closest('.metric-card'), 
                         'Quase na capacidade', 'warning');
        } else {
            updateElement($('#pool-occupancy').closest('.metric-card').querySelector('.metric-status'), 
                         $('#pool-occupancy').closest('.metric-card'), 
                         'Dentro do limite', 'normal');
        }

        // Atualizar entradas hoje
        const entries = randomBetween(100, 200);
        $('#pool-entries-today').textContent = entries;

        // Atualizar temperaturas
        const localTemp = randomBetweenFloat(22, 30);
        $('#local-temperature').textContent = `${localTemp}°C`;
        const waterTemp = randomBetweenFloat(24, 32);
        $('#water-temperature').textContent = `${waterTemp}°C`;

        // Atualizar qualidade da água
        const phValue = randomBetweenFloat(6.8, 8.0);
        $('#pool-ph').textContent = phValue;
        updatePoolCardStatus('#pool-ph-card', phValue, 7.2, 7.6);

        const chlorine = randomBetweenFloat(0.5, 3.5);
        $('#pool-chlorine').textContent = `${chlorine} ppm`;
        updatePoolCardStatus('#pool-chlorine-card', chlorine, 1.0, 3.0);

        const alkalinity = randomBetween(60, 140);
        $('#pool-alkalinity').textContent = `${alkalinity} ppm`;
        updatePoolCardStatus('#pool-alkalinity-card', alkalinity, 80, 120);
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

    // Atualizar a cada 10 segundos (para demonstração)
    setInterval(updatePoolMetrics, 10000);
    updatePoolMetrics();

    // Simular atualizações mais frequentes para temperaturas e pH (a cada 30 segundos)
    setInterval(() => {
        const localTemp = randomBetweenFloat(22, 30);
        $('#local-temperature').textContent = `${localTemp}°C`;
        const waterTemp = randomBetweenFloat(24, 32);
        $('#water-temperature').textContent = `${waterTemp}°C`;
        
        const phValue = randomBetweenFloat(6.8, 8.0);
        $('#pool-ph').textContent = phValue;
        updatePoolCardStatus('#pool-ph-card', phValue, 7.2, 7.6);
    }, 30000);
}

// ========== INICIALIZAÇÃO ==========
document.addEventListener('DOMContentLoaded', () => {
    if ($('#current-people')) initMainPage();
    else if ($('.areas-grid')) initAreasPage();
    else if ($('#active-alerts-list')) initAlertsPage();
    else if ($('#pool-occupancy')) initPoolPage();
});