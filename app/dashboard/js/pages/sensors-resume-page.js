/**
 * Resumo de Sensores Page Module
 * Gerencia a página de resumo detalhado dos sensores
 */

import { apiService } from './api.js';
import { chartManager } from './charts.js';

export const sensorsResumePage = {
    /**
     * Inicializa a página de resumo de sensores
     */
    async init() {
        console.log('📡 Inicializando página de Resumo de Sensores...');
        
        try {
            await this.loadSensorsData();
            this.setupAutoRefresh();
            this.initDistributionChart();
            console.log('✅ Página de Resumo de Sensores inicializada com sucesso');
        } catch (error) {
            console.error('❌ Erro ao inicializar página de sensores:', error);
        }
    },

    /**
     * Carrega os dados dos sensores
     */
    async loadSensorsData() {
        try {
            const sensors = await apiService.getSensors();
            
            if (!sensors || sensors.length === 0) {
                console.warn('⚠️ Nenhum sensor encontrado');
                return;
            }

            console.log(`📊 ${sensors.length} sensores carregados`);
            
            // Atualizar cards de resumo
            this.updateOverviewCards(sensors);
            
            // Atualizar estatísticas
            this.updateStatistics(sensors);
            
        } catch (error) {
            console.error('❌ Erro ao carregar dados dos sensores:', error);
        }
    },

    /**
     * Atualiza os cards de resumo
     */
    updateOverviewCards(sensors) {
        const totalSensors = sensors.length;
        const activeSensors = sensors.filter(s => s.status === 'ativo').length;
        
        // Total de leituras (somando de todos os sensores)
        const totalReadings = sensors.reduce((sum, sensor) => {
            return sum + (sensor.total_readings || 0);
        }, 0);
        
        // Protocolos únicos
        const protocols = [...new Set(sensors.map(s => s.protocol))];
        
        // Atualizar elementos DOM
        const totalEl = document.getElementById('total-sensors');
        const activeEl = document.getElementById('active-sensors');
        const readingsEl = document.getElementById('total-readings');
        const protocolsEl = document.getElementById('total-protocols');
        
        if (totalEl) totalEl.textContent = totalSensors;
        if (activeEl) activeEl.textContent = activeSensors;
        if (readingsEl) readingsEl.textContent = totalReadings.toLocaleString('pt-BR');
        if (protocolsEl) protocolsEl.textContent = protocols.length;
        
        console.log('📈 Cards de resumo atualizados:', {
            total: totalSensors,
            ativos: activeSensors,
            leituras: totalReadings,
            protocolos: protocols.length
        });
    },

    /**
     * Atualiza as estatísticas detalhadas
     */
    updateStatistics(sensors) {
        // Calcular distribuição por protocolo
        const protocolCount = {};
        sensors.forEach(sensor => {
            const protocol = sensor.protocol || 'Desconhecido';
            protocolCount[protocol] = (protocolCount[protocol] || 0) + 1;
        });
        
        console.log('📊 Distribuição por protocolo:', protocolCount);
        
        // Calcular status de bateria
        const batteryStats = {
            excellent: 0,  // 90-100%
            good: 0,       // 70-89%
            critical: 0    // <50%
        };
        
        sensors.forEach(sensor => {
            if (sensor.battery !== null && sensor.battery !== undefined) {
                if (sensor.battery >= 90) batteryStats.excellent++;
                else if (sensor.battery >= 70) batteryStats.good++;
                else if (sensor.battery < 50) batteryStats.critical++;
            }
        });
        
        console.log('🔋 Estatísticas de bateria:', batteryStats);
        
        // Calcular qualidade de sinal
        const signalStats = {
            excellent: 0,  // -40 a -60 dBm
            good: 0,       // -61 a -70 dBm
            poor: 0        // < -70 dBm
        };
        
        sensors.forEach(sensor => {
            if (sensor.signal_strength) {
                const signal = parseInt(sensor.signal_strength);
                if (signal >= -60 && signal <= -40) signalStats.excellent++;
                else if (signal >= -70 && signal <= -61) signalStats.good++;
                else if (signal < -70) signalStats.poor++;
            }
        });
        
        console.log('📶 Estatísticas de sinal:', signalStats);
    },

    /**
     * Inicializa o gráfico de distribuição de leituras
     */
    initDistributionChart() {
        const canvas = document.getElementById('sensorsDistributionChart');
        if (!canvas) {
            console.warn('⚠️ Canvas do gráfico de distribuição não encontrado');
            return;
        }

        // Dados mockados baseados na tabela
        const data = {
            labels: [
                'LORA-A1B2C3D4',
                'ZIGB-E5F6G7H8',
                'SIGF-I9J0K1L2',
                'RFID-M3N4O5P6',
                'LORA-Q7R8S9T0',
                'ZIGB-U1V2W3X4'
            ],
            datasets: [{
                label: 'Leituras por Sensor',
                data: [3619, 3703, 4036, 3528, 3428, 3762],
                backgroundColor: [
                    'rgba(155, 89, 182, 0.8)',  // LoRa - roxo
                    'rgba(39, 174, 96, 0.8)',   // Zigbee - verde
                    'rgba(230, 126, 34, 0.8)',  // Sigfox - laranja
                    'rgba(52, 152, 219, 0.8)',  // RFID - azul
                    'rgba(155, 89, 182, 0.8)',  // LoRa - roxo
                    'rgba(39, 174, 96, 0.8)'    // Zigbee - verde
                ],
                borderColor: [
                    'rgba(155, 89, 182, 1)',
                    'rgba(39, 174, 96, 1)',
                    'rgba(230, 126, 34, 1)',
                    'rgba(52, 152, 219, 1)',
                    'rgba(155, 89, 182, 1)',
                    'rgba(39, 174, 96, 1)'
                ],
                borderWidth: 2
            }]
        };

        const config = {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.parsed.y.toLocaleString('pt-BR') + ' leituras';
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return value.toLocaleString('pt-BR');
                            }
                        }
                    }
                }
            }
        };

        new Chart(canvas, config);
        console.log('📊 Gráfico de distribuição inicializado');
    },

    /**
     * Configura atualização automática
     */
    setupAutoRefresh() {
        // Atualizar a cada 60 segundos
        setInterval(() => {
            console.log('🔄 Atualizando dados dos sensores...');
            this.loadSensorsData();
        }, 60000);
    }
};
