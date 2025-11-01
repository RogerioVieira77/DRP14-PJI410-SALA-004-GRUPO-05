// indicators.js - Módulo para gerenciar indicadores de última leitura
// Parte do projeto SmartCEU - Dashboard

/**
 * Inicializa o indicador de última leitura
 * @param {string} elementId - ID do elemento HTML (padrão: 'last-update-indicator')
 * @param {string} apiUrl - URL da API para buscar dados (padrão: '/smartceu/api/v1/dashboard/current-stats')
 * @param {number} updateInterval - Intervalo de atualização em ms (padrão: 30000 = 30s)
 */
function initLastReadingIndicator(
    elementId = 'last-update-indicator',
    apiUrl = '/smartceu/api/v1/dashboard/current-stats',
    updateInterval = 30000
) {
    // Obter cores das variáveis CSS
    const root = getComputedStyle(document.documentElement);
    const colors = {
        bg: root.getPropertyValue('--indicator-bg').trim() || '#1565C0',
        success: root.getPropertyValue('--indicator-success').trim() || '#5efc82',
        warning: root.getPropertyValue('--indicator-warning').trim() || '#ffd54f',
        danger: root.getPropertyValue('--indicator-danger').trim() || '#ff8a80'
    };

    /**
     * Atualiza o conteúdo visual do indicador
     * @param {string} lastReading - Timestamp da última leitura (formato ISO)
     */
    function updateIndicator(lastReading) {
        const indicator = document.querySelector(`#${elementId}`);
        if (!indicator) {
            console.warn(`⚠️ Elemento #${elementId} não encontrado`);
            return;
        }

        // Sem dados
        if (!lastReading) {
            indicator.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Sem dados';
            indicator.style.color = colors.danger;
            indicator.style.background = colors.bg;
            return;
        }

        try {
            const date = new Date(lastReading);
            const now = new Date();
            const diffMinutes = Math.floor((now - date) / 1000 / 60);

            // Formatar data (DD/MM/YYYY HH:MM)
            const dia = String(date.getDate()).padStart(2, '0');
            const mes = String(date.getMonth() + 1).padStart(2, '0');
            const ano = date.getFullYear();
            const hora = String(date.getHours()).padStart(2, '0');
            const minuto = String(date.getMinutes()).padStart(2, '0');
            const dataFormatada = `${dia}/${mes}/${ano} ${hora}:${minuto}`;

            // Determinar ícone e cor baseado na idade dos dados
            let icon, color;
            if (diffMinutes < 5) {
                icon = 'fa-check-circle';
                color = colors.success;
            } else if (diffMinutes < 30) {
                icon = 'fa-clock';
                color = colors.warning;
            } else {
                icon = 'fa-exclamation-triangle';
                color = colors.danger;
            }

            // Atualizar HTML e estilos
            indicator.innerHTML = `<i class="fas ${icon}"></i> Última Leitura: ${dataFormatada}`;
            indicator.style.color = color;
            indicator.style.background = colors.bg;

            console.log(`⏰ Última leitura: ${dataFormatada} (${diffMinutes}min atrás)`);
        } catch (error) {
            console.error('❌ Erro ao formatar data:', error);
            indicator.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Erro na data';
            indicator.style.color = colors.danger;
            indicator.style.background = colors.bg;
        }
    }

    /**
     * Busca dados da API e atualiza o indicador
     */
    async function fetchAndUpdate() {
        try {
            console.log(`🔄 Buscando dados de: ${apiUrl}`);
            const response = await fetch(apiUrl);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            console.log('✅ Dados recebidos:', data);
            
            updateIndicator(data.last_reading);
        } catch (error) {
            console.error('❌ Erro ao buscar dados da API:', error);
            updateIndicator(null); // Exibir "Sem dados"
        }
    }

    // Inicializar: buscar imediatamente e configurar atualização periódica
    console.log(`🚀 Inicializando indicador #${elementId}`);
    fetchAndUpdate();
    setInterval(fetchAndUpdate, updateInterval);
    
    console.log(`✅ Indicador configurado (atualização a cada ${updateInterval/1000}s)`);
}

// Exportar para uso global
window.initLastReadingIndicator = initLastReadingIndicator;
