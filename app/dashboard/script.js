// script.js - CEU Monitor (Versão com API Real)

// ========== CONFIGURAÇÃO DA API ==========
const API_BASE = '/smartceu/api/v1/dashboard';

// ========== FUNÇÕES UTILITÁRIAS ==========
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);
const randomBetweenFloat = (min, max) => {
    const value = Math.random() * (max - min) + min;
    return Number(value.toFixed(2));
};
const randomBetween = (min, max) => Math.floor(Math.random() * (max - min) + min);

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

async function fetchPeakPrediction() {
    try {
        const response = await fetch(`${API_BASE}/peak-prediction`);
        if (!response.ok) throw new Error('Erro ao buscar previsão de pico');
        return await response.json();
    } catch (error) {
        console.error('Erro em fetchPeakPrediction:', error);
        return null;
    }
}

async function fetchAdvancedStats() {
    try {
        const response = await fetch(`${API_BASE}/advanced-stats`);
        if (!response.ok) throw new Error('Erro ao buscar estatísticas avançadas');
        return await response.json();
    } catch (error) {
        console.error('Erro em fetchAdvancedStats:', error);
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






// ========== PÁGINA PRINCIPAL ==========
async function initMainPage() {
    if (!$('#current-people')) return;
    
    const updateLastUpdateIndicator = (lastReading) => {
        const indicator = $('#last-update-indicator');
        console.log('🔄 updateLastUpdateIndicator chamado', { lastReading, indicator });
        
        if (!indicator) {
            console.error('❌ Elemento #last-update-indicator não encontrado!');
            return;
        }
        
        if (lastReading) {
            const date = new Date(lastReading);
            const now = new Date();
            const diff = Math.floor((now - date) / 1000 / 60); // minutos
            
            console.log('⏰ Diferença de tempo:', diff, 'minutos');
            
            // Formatar data e hora: 31/10/2025 - 17:50
            const dia = String(date.getDate()).padStart(2, '0');
            const mes = String(date.getMonth() + 1).padStart(2, '0');
            const ano = date.getFullYear();
            const hora = String(date.getHours()).padStart(2, '0');
            const minuto = String(date.getMinutes()).padStart(2, '0');
            const dataFormatada = `${dia}/${mes}/${ano} - ${hora}:${minuto}`;
            
            let icon, textColor;
            if (diff < 5) {
                icon = '<i class="fas fa-check-circle"></i>';
                textColor = '#5efc82'; // Verde claro brilhante
            } else if (diff < 30) {
                icon = '<i class="fas fa-clock"></i>';
                textColor = '#ffd54f'; // Amarelo claro
            } else {
                icon = '<i class="fas fa-exclamation-triangle"></i>';
                textColor = '#ff8a80'; // Vermelho claro
            }
            
            const text = `${icon} Atualizado: ${dataFormatada}`;
            
            indicator.innerHTML = text;
            indicator.style.color = textColor;
            console.log('✅ Indicador atualizado:', text, textColor);
        } else {
            indicator.innerHTML = '<i class="fas fa-sync-alt"></i> Carregando...';
            indicator.style.color = '#b0bec5'; // Cinza claro
            console.log('⚠️ Sem last_reading, mostrando "Carregando..."');
        }
    };
    
    const updateMetrics = async () => {
        // Buscar dados reais da API
        const stats = await fetchCurrentStats();
        const alerts = await fetchActiveAlerts();
        const peak = await fetchPeakPrediction();
        const advanced = await fetchAdvancedStats();
        
        console.log('📊 Stats recebidos da API:', stats);
        console.log('🔔 Alertas:', alerts);
        console.log('📈 Previsão de pico:', peak);
        console.log('📉 Stats avançadas:', advanced);
        
        // ========== CARD 1: PESSOAS NO CEU ==========
        if (stats) {
            // Atualizar valor principal
            $('#current-people').textContent = stats.current_people;
            
            // Atualizar capacidade
            $('#capacity-info').textContent = `${stats.current_people}/${stats.max_capacity} pessoas`;
            
            // Atualizar indicador de última atualização
            updateLastUpdateIndicator(stats.last_reading);
            
            // Atualizar status baseado na capacidade
            const capacityPercent = stats.capacity_percentage;
            const statusEl = $('#capacity-status');
            const card1 = $('.metric-card:nth-child(1)');
            
            if (capacityPercent >= 80) {
                statusEl.textContent = 'Capacidade crítica';
                statusEl.className = 'metric-status status-danger';
                card1.classList.add('danger');
            } else if (capacityPercent >= 60) {
                statusEl.textContent = 'Alerta moderado';
                statusEl.className = 'metric-status status-warning';
                card1.classList.add('warning');
            } else {
                statusEl.textContent = 'Dentro do limite';
                statusEl.className = 'metric-status status-normal';
                card1.classList.remove('warning', 'danger');
            }
        }
        
        // ========== CARD 2: ENTRADAS HOJE ==========
        if (stats) {
            $('#entries-today').textContent = stats.entries_today;
        }
        
        if (advanced) {
            // Atualizar média diária
            $('#daily-average').textContent = `Média: ${advanced.daily_average}/dia`;
            
            // Atualizar tendência
            const trendEl = $('#entries-trend');
            const trendPercent = advanced.trend_percentage;
            const trendDirection = advanced.trend_direction;
            
            let trendIcon = 'fa-minus';
            let trendClass = '';
            let trendText = 'Estável em relação a ontem';
            
            if (trendDirection === 'up') {
                trendIcon = 'fa-arrow-up';
                trendClass = 'trend-up';
                trendText = `+${Math.abs(trendPercent)}% em relação a ontem`;
            } else if (trendDirection === 'down') {
                trendIcon = 'fa-arrow-down';
                trendClass = 'trend-down';
                trendText = `${trendPercent}% em relação a ontem`;
            }
            
            trendEl.innerHTML = `
                <i class="fas ${trendIcon} ${trendClass}"></i>
                <span>${trendText}</span>
            `;
            
            // Atualizar status
            const entriesStatusEl = $('#entries-status');
            if (Math.abs(trendPercent) > 20) {
                entriesStatusEl.textContent = 'Variação significativa';
                entriesStatusEl.className = 'metric-status status-warning';
            } else {
                entriesStatusEl.textContent = 'Normal';
                entriesStatusEl.className = 'metric-status status-normal';
            }
        }
        
        // ========== CARD 3: HORÁRIO DE PICO ==========
        if (peak) {
            // Atualizar horário do pico
            $('#next-peak').textContent = peak.peak_hour;
            
            // Atualizar previsão
            $('#peak-prediction').textContent = `Previsão: ${peak.capacity_prediction}% de capacidade`;
            
            // Atualizar status
            const peakStatusEl = $('#peak-status');
            const card3 = $('.metric-card:nth-child(3)');
            
            if (peak.capacity_prediction >= 80) {
                peakStatusEl.textContent = 'Preparar equipe de apoio';
                peakStatusEl.className = 'metric-status status-danger';
                card3.classList.remove('warning');
                card3.classList.add('danger');
            } else if (peak.capacity_prediction >= 60) {
                peakStatusEl.textContent = 'Monitorar ocupação';
                peakStatusEl.className = 'metric-status status-warning';
                card3.classList.remove('danger');
                card3.classList.add('warning');
            } else {
                peakStatusEl.textContent = 'Fluxo normal esperado';
                peakStatusEl.className = 'metric-status status-normal';
                card3.classList.remove('warning', 'danger');
            }
            
            // Atualizar tendência com confiança
            const peakTrendEl = $('#peak-trend');
            peakTrendEl.innerHTML = `
                <i class="fas fa-chart-line"></i>
                <span>Confiança: ${peak.confidence}% (${peak.total_readings} leituras)</span>
            `;
        }
        
        // ========== CARD 4: ALERTAS ATIVOS ==========
        if (alerts) {
            // Atualizar número de alertas
            $('#active-alerts').textContent = alerts.total;
            
            // Contar alertas por severidade
            const critical = alerts.alerts.filter(a => a.severity === 'critical').length;
            const warning = alerts.alerts.filter(a => a.severity === 'warning').length;
            const info = alerts.alerts.filter(a => a.severity === 'info').length;
            
            // Atualizar breakdown
            $('#alerts-breakdown').textContent = `${critical} críticos, ${warning} avisos, ${info} informativos`;
            
            // Atualizar status
            const alertsStatusEl = $('#alerts-status');
            const card4 = $('.metric-card:nth-child(4)');
            
            if (critical > 0) {
                alertsStatusEl.textContent = 'Atenção necessária';
                alertsStatusEl.className = 'metric-status status-danger';
                card4.classList.remove('warning');
                card4.classList.add('danger');
            } else if (warning > 0) {
                alertsStatusEl.textContent = 'Monitorar';
                alertsStatusEl.className = 'metric-status status-warning';
                card4.classList.remove('danger');
                card4.classList.add('warning');
            } else {
                alertsStatusEl.textContent = 'Sistema estável';
                alertsStatusEl.className = 'metric-status status-normal';
                card4.classList.remove('warning', 'danger');
            }
            
            // Atualizar tendência
            const alertsTrendEl = $('#alerts-trend');
            if (alerts.total === 0) {
                alertsTrendEl.innerHTML = `
                    <i class="fas fa-check-circle" style="color: #27ae60;"></i>
                    <span>Nenhum alerta ativo</span>
                `;
            } else {
                alertsTrendEl.innerHTML = `
                    <i class="fas fa-bell"></i>
                    <span>Total de ${alerts.total} alerta(s) requer(em) atenção</span>
                `;
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
    
    let state = { active: 0, critical: 0, resolved: 0 };

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
        $('#history-alerts-list')?.prepend(clone);
    };

    const updateAlertsMetrics = () => {
        $('#active-alerts').textContent = state.active;
        $('#critical-alerts').textContent = state.critical;
        $('#resolved-alerts').textContent = state.resolved;
        
        const warning = state.active - state.critical;
        const subvalueEl = $('.metric-card:nth-child(1) .metric-subvalue');
        if (subvalueEl) {
            subvalueEl.textContent = `${state.critical} críticos, ${warning} ${warning === 1 ? 'aviso' : 'avisos'}`;
        }
        
        updateStatus('.metric-card:nth-child(1)', state.active, 1, 3, 'Sistema estável', 'Monitorar', 'Atenção necessária');
    };

    // Carregar alertas reais da API
    const loadAlerts = async () => {
        const alertsData = await fetchActiveAlerts();
        
        if (alertsData && alertsData.alerts) {
            // Limpar lista
            const activeList = $('#active-alerts-list');
            if (activeList) activeList.innerHTML = '';
            
            // Atualizar state
            state.active = alertsData.total;
            state.critical = alertsData.alerts.filter(a => a.severity === 'critical').length;
            
            // Adicionar cada alerta à lista
            alertsData.alerts.forEach(alert => {
                const iconMap = {
                    'critical': 'exclamation-circle',
                    'warning': 'exclamation-triangle',
                    'info': 'info-circle'
                };
                
                const priorityMap = {
                    'critical': 'Crítico',
                    'warning': 'Aviso',
                    'info': 'Informativo'
                };
                
                const alertTime = new Date(alert.timestamp);
                const now = new Date();
                const diffMinutes = Math.floor((now - alertTime) / 60000);
                const timeText = diffMinutes < 1 ? 'Agora' : 
                                diffMinutes < 60 ? `${diffMinutes} min atrás` : 
                                `${Math.floor(diffMinutes / 60)}h atrás`;
                
                if (activeList) {
                    activeList.insertAdjacentHTML('beforeend', `
                        <div class="alert-item" data-id="${alert.id}" data-type="${alert.severity}" data-area="${alert.area}">
                            <div class="alert-icon ${alert.severity}">
                                <i class="fas fa-${iconMap[alert.severity] || 'bell'}"></i>
                            </div>
                            <div class="alert-content">
                                <h4>${alert.type || 'Alerta do Sistema'}</h4>
                                <p class="alert-desc">${alert.message}</p>
                                <div class="alert-meta">
                                    <span class="alert-time">${timeText}</span>
                                    <span class="alert-area">${alert.area}</span>
                                    <span class="alert-priority">${priorityMap[alert.severity]}</span>
                                </div>
                            </div>
                            <div class="alert-actions">
                                <button class="btn btn-resolve" onclick="resolveAlert(${alert.id})">Resolver</button>
                                <button class="btn btn-ignore" onclick="ignoreAlert(${alert.id})">Ignorar</button>
                            </div>
                        </div>
                    `);
                }
            });
            
            updateAlertsMetrics();
        } else {
            // Nenhum alerta ativo
            state.active = 0;
            state.critical = 0;
            updateAlertsMetrics();
            
            const activeList = $('#active-alerts-list');
            if (activeList) {
                activeList.innerHTML = `
                    <div style="text-align: center; padding: 40px; color: #7f8c8d;">
                        <i class="fas fa-check-circle" style="font-size: 48px; color: #27ae60; margin-bottom: 16px;"></i>
                        <p style="font-size: 18px; font-weight: 500;">Nenhum alerta ativo</p>
                        <p style="font-size: 14px; margin-top: 8px;">Sistema funcionando normalmente</p>
                    </div>
                `;
            }
        }
    };

    // Filtros
    $('#filter-type')?.addEventListener('change', filterAlerts);
    $('#filter-area')?.addEventListener('change', filterAlerts);

    const filterAlerts = () => {
        const typeFilter = $('#filter-type')?.value;
        const areaFilter = $('#filter-area')?.value;
        
        $$('#active-alerts-list .alert-item').forEach(alert => {
            const typeMatch = typeFilter === 'all' || alert.dataset.type === typeFilter;
            const areaMatch = areaFilter === 'all' || alert.dataset.area === areaFilter;
            alert.style.display = typeMatch && areaMatch ? 'flex' : 'none';
        });
    };

    // Carregar alertas inicialmente e atualizar a cada 30 segundos
    await loadAlerts();
    setInterval(loadAlerts, 30000);

    updateAlertsMetrics();
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
            
            if (trend) trend.textContent = 'Valor dentro da faixa segura';
        } else {
            status.textContent = 'Fora do ideal';
            status.className = 'metric-status status-danger';
            card.classList.remove('warning');
            card.classList.add('danger');
            
            if (trend) {
                if (value < min) {
                    trend.textContent = 'Valor abaixo do recomendado';
                } else {
                    trend.textContent = 'Valor acima do recomendado';
                }
            }
        }
    };

    // Atualizar a cada 30 segundos
    setInterval(updatePoolMetrics, 30000);
    await updatePoolMetrics();
}

// ========== PÁGINA CONTROLE DE ACESSO ==========
async function initControleAcessoPage() {
    if (!$('#ca-current-people')) return;
    
    console.log('🚀 Inicializando página Controle de Acesso...');
    
    const updateCALastUpdateIndicator = (lastReading) => {
        const indicator = $('#ca-last-update-indicator');
        
        if (!indicator) return;
        
        if (lastReading) {
            const date = new Date(lastReading);
            const now = new Date();
            const diff = Math.floor((now - date) / 1000 / 60); // minutos
            
            // Formatar data e hora: 31/10/2025 - 17:50
            const dia = String(date.getDate()).padStart(2, '0');
            const mes = String(date.getMonth() + 1).padStart(2, '0');
            const ano = date.getFullYear();
            const hora = String(date.getHours()).padStart(2, '0');
            const minuto = String(date.getMinutes()).padStart(2, '0');
            const dataFormatada = `${dia}/${mes}/${ano} - ${hora}:${minuto}`;
            
            let icon, textColor;
            if (diff < 5) {
                icon = '<i class="fas fa-check-circle"></i>';
                textColor = '#5efc82';
            } else if (diff < 30) {
                icon = '<i class="fas fa-clock"></i>';
                textColor = '#ffd54f';
            } else {
                icon = '<i class="fas fa-exclamation-triangle"></i>';
                textColor = '#ff8a80';
            }
            
            const text = `${icon} Atualizado: ${dataFormatada}`;
            indicator.innerHTML = text;
            indicator.style.color = textColor;
        } else {
            indicator.innerHTML = '<i class="fas fa-sync-alt"></i> Carregando...';
            indicator.style.color = '#b0bec5';
        }
    };
    
    const updateCAMetrics = async () => {
        console.log('📊 Atualizando métricas de Controle de Acesso...');
        
        // Buscar dados das APIs
        const stats = await fetchCurrentStats();
        const alerts = await fetchActiveAlerts();
        const peak = await fetchPeakPrediction();
        const advanced = await fetchAdvancedStats();
        
        console.log('📊 Stats CA:', stats);
        console.log('🔔 Alertas CA:', alerts);
        console.log('📈 Pico CA:', peak);
        console.log('📉 Avançadas CA:', advanced);
        
        // ========== CARD 1: PESSOAS NO CEU ==========
        if (stats) {
            $('#ca-current-people').textContent = stats.current_people;
            $('#ca-capacity-info').textContent = `${stats.current_people}/${stats.max_capacity} pessoas`;
            updateCALastUpdateIndicator(stats.last_reading);
            
            const capacityPercent = stats.capacity_percentage;
            const statusEl = $('#ca-capacity-status');
            const card1 = $('.metric-card:nth-child(1)');
            
            if (capacityPercent >= 80) {
                statusEl.textContent = 'Capacidade crítica';
                statusEl.className = 'metric-status status-danger';
                if (card1) card1.classList.add('danger');
            } else if (capacityPercent >= 60) {
                statusEl.textContent = 'Capacidade alta';
                statusEl.className = 'metric-status status-warning';
                if (card1) card1.classList.remove('danger');
            } else {
                statusEl.textContent = 'Capacidade normal';
                statusEl.className = 'metric-status status-success';
                if (card1) card1.classList.remove('danger');
            }
        }
        
        // ========== CARD 2: ENTRADAS HOJE ==========
        if (advanced) {
            $('#ca-entries-today').textContent = advanced.total_entries_today || 0;
            
            const trendPercent = advanced.trend_percentage || 0;
            const trendEl = $('#ca-entries-trend');
            const trendIcon = $('#ca-trend-icon');
            
            if (trendPercent > 0) {
                trendEl.textContent = `+${trendPercent.toFixed(1)}%`;
                trendEl.className = 'metric-trend trend-up';
                if (trendIcon) trendIcon.className = 'fas fa-arrow-up';
            } else {
                trendEl.textContent = `${trendPercent.toFixed(1)}%`;
                trendEl.className = 'metric-trend trend-down';
                if (trendIcon) trendIcon.className = 'fas fa-arrow-down';
            }
        }
        
        // ========== CARD 3: PRÓXIMO HORÁRIO DE PICO ==========
        if (peak) {
            $('#ca-next-peak').textContent = peak.peak_time || '--:--';
            $('#ca-peak-occupancy').textContent = `${peak.predicted_occupancy || 0} pessoas`;
            
            const peakDate = new Date();
            const [hours, minutes] = (peak.peak_time || '00:00').split(':');
            peakDate.setHours(parseInt(hours), parseInt(minutes), 0);
            
            const now = new Date();
            const diffMinutes = Math.floor((peakDate - now) / 1000 / 60);
            
            const peakStatus = $('#ca-peak-status');
            if (diffMinutes < 30 && diffMinutes > 0) {
                peakStatus.textContent = `Em ${diffMinutes} minutos`;
                peakStatus.className = 'metric-status status-warning';
            } else if (diffMinutes <= 0 && diffMinutes > -60) {
                peakStatus.textContent = 'Acontecendo agora';
                peakStatus.className = 'metric-status status-danger';
            } else {
                peakStatus.textContent = `Em ${Math.abs(Math.floor(diffMinutes / 60))}h`;
                peakStatus.className = 'metric-status status-success';
            }
        }
        
        // ========== CARD 4: ALERTAS ATIVOS ==========
        if (alerts) {
            const activeCount = Array.isArray(alerts) ? alerts.length : 0;
            $('#ca-active-alerts').textContent = activeCount;
            
            const alertStatus = $('#ca-alert-status');
            const card4 = $('.metric-card:nth-child(4)');
            
            if (activeCount === 0) {
                alertStatus.textContent = 'Nenhum alerta';
                alertStatus.className = 'metric-status status-success';
                if (card4) card4.classList.remove('warning');
            } else if (activeCount <= 2) {
                alertStatus.textContent = `${activeCount} pendente${activeCount > 1 ? 's' : ''}`;
                alertStatus.className = 'metric-status status-warning';
                if (card4) card4.classList.add('warning');
            } else {
                alertStatus.textContent = `${activeCount} críticos`;
                alertStatus.className = 'metric-status status-danger';
                if (card4) card4.classList.add('warning');
            }
            
            // Atualizar lista de alertas
            const alertsList = $('#ca-alerts-list');
            if (alertsList) {
                if (activeCount === 0) {
                    alertsList.innerHTML = `
                        <div class="alert-item alert-info">
                            <i class="fas fa-check-circle"></i>
                            <span>Nenhum alerta ativo no momento.</span>
                        </div>
                    `;
                } else {
                    alertsList.innerHTML = alerts.map(alert => {
                        const severityClass = alert.severity === 'high' ? 'alert-danger' : 
                                             alert.severity === 'medium' ? 'alert-warning' : 'alert-info';
                        const icon = alert.severity === 'high' ? 'fa-exclamation-circle' : 
                                    alert.severity === 'medium' ? 'fa-exclamation-triangle' : 'fa-info-circle';
                        
                        return `
                            <div class="alert-item ${severityClass}">
                                <i class="fas ${icon}"></i>
                                <div class="alert-content">
                                    <strong>${alert.area}</strong>
                                    <p>${alert.message}</p>
                                    <span class="alert-time">${new Date(alert.timestamp).toLocaleTimeString('pt-BR')}</span>
                                </div>
                            </div>
                        `;
                    }).join('');
                }
            }
        }
        
        // ========== GRÁFICO DE FLUXO ==========
        if (advanced && advanced.hourly_flow) {
            updateCAFlowChart(advanced.hourly_flow);
        }
    };
    
    const updateCAFlowChart = (hourlyFlow) => {
        const canvas = $('#ca-peopleFlowChart');
        if (!canvas) return;
        
        // Destruir gráfico existente se houver
        if (window.caFlowChart) {
            window.caFlowChart.destroy();
        }
        
        const ctx = canvas.getContext('2d');
        const labels = hourlyFlow.map(item => item.hour);
        const data = hourlyFlow.map(item => item.count);
        
        window.caFlowChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Pessoas',
                    data: data,
                    borderColor: '#4fc3f7',
                    backgroundColor: 'rgba(79, 195, 247, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
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
                        ticks: {
                            color: '#b0bec5'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    },
                    x: {
                        ticks: {
                            color: '#b0bec5'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    }
                }
            }
        });
    };
    
    // Atualizar métricas imediatamente e depois a cada 30 segundos
    await updateCAMetrics();
    setInterval(updateCAMetrics, 30000);
    
    console.log('✅ Página Controle de Acesso inicializada com sucesso!');
}

// ========== INICIALIZAÇÃO ==========
document.addEventListener('DOMContentLoaded', () => {
    if ($('#current-people')) initMainPage();
    else if ($('#ca-current-people')) initControleAcessoPage();
    else if ($('.areas-grid')) initAreasPage();
    else if ($('#active-alerts-list')) initAlertsPage();
    else if ($('#pool-occupancy')) initPoolPage();
});
