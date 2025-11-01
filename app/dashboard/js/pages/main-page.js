// main-page.js - Lógica da página principal (index)
// Atualiza métricas e gráficos do dashboard principal

import { $, updateStatus } from '../utils.js';
import { fetchCurrentStats, fetchAdvancedStats, fetchPeakPrediction, fetchActiveAlerts } from '../api.js';

export async function initMainPage() {
    console.log('📊 Inicializando página principal...');
    
    // Atualizar dados iniciais
    await updateMainPageData();
    
    // Atualizar a cada 30 segundos
    setInterval(updateMainPageData, 30000);
    
    console.log('✅ Página principal inicializada com sucesso!');
}

async function updateMainPageData() {
    console.log('🔄 Atualizando dados do dashboard...');
    
    try {
        // Buscar dados da API
        const [stats, advancedStats, peakData, alertsData] = await Promise.all([
            fetchCurrentStats(),
            fetchAdvancedStats(),
            fetchPeakPrediction(),
            fetchActiveAlerts()
        ]);
        
        console.log('📊 Dados recebidos:', { stats, advancedStats, peakData, alertsData });
        
        // Atualizar métricas principais
        if (stats) {
            updateMainMetrics(stats);
        }
        
        // Estatísticas avançadas
        if (advancedStats) {
            updateAdvancedStats(advancedStats, stats);
        }
        
        // Horário de pico
        if (peakData) {
            updatePeakData(peakData);
        }
        
        // Alertas ativos
        if (alertsData) {
            updateAlerts(alertsData);
        }
        
        console.log('✅ Dados atualizados com sucesso!');
    } catch (error) {
        console.error('❌ Erro ao atualizar dados:', error);
    }
}

function updateMainMetrics(stats) {
    // Pessoas no CEU
    const peopleElement = $('#current-people');
    if (peopleElement) {
        peopleElement.textContent = stats.current_people || 0;
    }
    
    // Capacidade
    const capacityElement = $('#capacity-info');
    if (capacityElement) {
        capacityElement.textContent = `Capacidade: ${stats.current_people || 0}/${stats.max_capacity || 300}`;
    }
    
    // Entradas hoje
    const entriesElement = $('#entries-today');
    if (entriesElement) {
        entriesElement.textContent = stats.entries_today || 0;
        console.log(`📥 Entradas hoje: ${stats.entries_today}`);
    }
}

function updateAdvancedStats(advancedStats, stats) {
    // Média diária
    const avgElement = $('#daily-average');
    if (avgElement) {
        avgElement.textContent = `Média: ${advancedStats.daily_average || 0}/dia`;
    }
    
    // Taxa de ocupação
    const occupationElement = $('#occupation-rate');
    if (occupationElement) {
        const percentage = stats?.capacity_percentage || 0;
        occupationElement.textContent = `${percentage.toFixed(1)}%`;
    }
    
    // Tempo médio (calculado)
    const avgTimeElement = $('#avg-time');
    if (avgTimeElement) {
        const avgMinutes = advancedStats.average_stay_minutes || 120;
        const hours = Math.floor(avgMinutes / 60);
        const minutes = avgMinutes % 60;
        avgTimeElement.textContent = hours > 0 ? `${hours}h${minutes}min` : `${minutes}min`;
    }
    
    // Pico de hoje
    const todayPeakElement = $('#today-peak');
    if (todayPeakElement) {
        todayPeakElement.textContent = advancedStats.today_peak || stats?.current_people || 0;
    }
}

function updatePeakData(peakData) {
    // Horário de pico
    const peakElement = $('#next-peak');
    if (peakElement) {
        peakElement.textContent = peakData.peak_hour || '--:--';
        console.log(`⏰ Horário de pico: ${peakData.peak_hour}`);
    }
    
    // Previsão
    const predictionElement = $('#peak-prediction');
    if (predictionElement) {
        const capacity = peakData.capacity_prediction || 0;
        predictionElement.textContent = `Prev. ${capacity.toFixed(0)}% de ocupação`;
    }
}

function updateAlerts(alertsData) {
    // Total de alertas
    const alertsElement = $('#active-alerts');
    if (alertsElement) {
        alertsElement.textContent = alertsData.total || 0;
        console.log(`🔔 Alertas ativos: ${alertsData.total}`);
    }
    
    // Contagem por severidade
    const alerts = alertsData.alerts || [];
    const criticalCount = alerts.filter(a => a.severity === 'critical').length;
    const warningCount = alerts.filter(a => a.severity === 'warning').length;
    
    const breakdownElement = $('#alerts-breakdown');
    if (breakdownElement) {
        breakdownElement.textContent = `${criticalCount} críticos, ${warningCount} avisos`;
    }
    
    // Atualizar lista de alertas
    updateAlertsList(alerts);
}

function updateAlertsList(alerts) {
    const alertsList = $('#alerts-list');
    if (!alertsList) return;
    
    if (alerts.length === 0) {
        alertsList.innerHTML = `
            <div class="alert-quick info">
                <div class="alert-quick-icon">
                    <i class="fas fa-check-circle" style="color: #38ef7d;"></i>
                </div>
                <div class="alert-quick-content">
                    <h4>Sistema Operacional</h4>
                    <p>Nenhum alerta ativo no momento</p>
                    <div class="alert-quick-time">Atualizado agora</div>
                </div>
            </div>
        `;
        return;
    }
    
    alertsList.innerHTML = alerts.slice(0, 5).map(alert => {
        const severityClass = alert.severity === 'critical' ? 'critical' : 
                             alert.severity === 'warning' ? 'warning' : 'info';
        const icon = alert.severity === 'critical' ? 'fa-exclamation-triangle' :
                    alert.severity === 'warning' ? 'fa-exclamation-circle' : 'fa-info-circle';
        
        return `
            <div class="alert-quick ${severityClass}">
                <div class="alert-quick-icon">
                    <i class="fas ${icon}"></i>
                </div>
                <div class="alert-quick-content">
                    <h4>${alert.alert_type || 'Alerta'}</h4>
                    <p>${alert.message || 'Sem descrição'}</p>
                    <div class="alert-quick-time">${formatTimestamp(alert.timestamp)}</div>
                </div>
            </div>
        `;
    }).join('');
}

function formatTimestamp(timestamp) {
    if (!timestamp) return 'Agora';
    
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 1) return 'Agora';
    if (diffMins < 60) return `Há ${diffMins} minuto${diffMins > 1 ? 's' : ''}`;
    
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `Há ${diffHours} hora${diffHours > 1 ? 's' : ''}`;
    
    return date.toLocaleDateString('pt-BR');
}
