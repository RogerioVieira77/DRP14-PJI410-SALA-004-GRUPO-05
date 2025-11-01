// charts.js - Módulo de gráficos Chart.js
// Funções para inicializar e atualizar gráficos

import { $ } from './utils.js';
import { fetchPeopleFlow, fetchAreasOccupation } from './api.js';

// ========== INICIALIZAÇÃO GERAL ==========
export function initCharts() {
    if ($('#peopleFlowChart')) initPeopleFlowChart();
    if ($('#occupationByAreaChart')) initOccupationByAreaChart();
    if ($('#poolOccupationChart')) initPoolOccupationChart();
    if ($('#waterQualityChart')) initWaterQualityChart();
    if ($('#alertsByTypeChart')) initAlertsByTypeChart();
}

// ========== GRÁFICO: FLUXO DE PESSOAS ==========
export async function initPeopleFlowChart() {
    const canvas = $('#peopleFlowChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const flowData = await fetchPeopleFlow();
    
    const labels = flowData?.labels || ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'];
    const data = flowData?.data || [25, 18, 85, 120, 180, 95];
    
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
                legend: { display: false }
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

// ========== GRÁFICO: OCUPAÇÃO POR ÁREA ==========
export async function initOccupationByAreaChart() {
    const canvas = $('#occupationByAreaChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const areasData = await fetchAreasOccupation();
    
    const labels = areasData?.areas?.map(area => area.name) || 
                   ['Piscinas', 'Auditórios', 'Salas', 'Quadras', 'Biblioteca', 'Convivência'];
    const data = areasData?.areas?.map(area => area.percentage) || 
                 [68, 35, 55, 45, 22, 38];
    
    const backgroundColors = data.map(value => {
        if (value > 70) return 'rgba(231, 76, 60, 0.7)';
        if (value > 50) return 'rgba(241, 196, 15, 0.7)';
        return 'rgba(46, 204, 113, 0.7)';
    });
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Ocupação (%)',
                data: data,
                backgroundColor: backgroundColors,
                borderColor: backgroundColors.map(color => color.replace('0.7', '1')),
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
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

// ========== GRÁFICO: OCUPAÇÃO DA PISCINA ==========
export async function initPoolOccupationChart() {
    const canvas = $('#poolOccupationChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Dados simulados para agora
    const labels = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00'];
    const data = [15, 22, 35, 48, 55, 62, 68, 70];
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Ocupação (%)',
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
                legend: { display: false }
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

// ========== GRÁFICO: QUALIDADE DA ÁGUA ==========
export function initWaterQualityChart() {
    const canvas = $('#waterQualityChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
            datasets: [
                {
                    label: 'pH',
                    data: [7.2, 7.3, 7.4, 7.5, 7.4, 7.3],
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    tension: 0.4,
                    yAxisID: 'y'
                },
                {
                    label: 'Cloro (ppm)',
                    data: [2.0, 2.1, 2.2, 2.1, 2.0, 2.1],
                    borderColor: '#2ecc71',
                    backgroundColor: 'rgba(46, 204, 113, 0.1)',
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
                intersect: false
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
                    max: 8.0
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
                    max: 4,
                    grid: {
                        drawOnChartArea: false
                    }
                }
            }
        }
    });
}

// ========== GRÁFICO: ALERTAS POR TIPO ==========
export function initAlertsByTypeChart() {
    const canvas = $('#alertsByTypeChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Críticos', 'Avisos', 'Informativos'],
            datasets: [{
                data: [3, 2, 5],
                backgroundColor: [
                    'rgba(231, 76, 60, 0.7)',
                    'rgba(241, 196, 15, 0.7)',
                    'rgba(52, 152, 219, 0.7)'
                ],
                borderColor: [
                    'rgb(231, 76, 60)',
                    'rgb(241, 196, 15)',
                    'rgb(52, 152, 219)'
                ],
                borderWidth: 2
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
