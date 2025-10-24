// script.js - CEU Monitor (Versão Otimizada)

// ========== FUNÇÕES UTILITÁRIAS ==========
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