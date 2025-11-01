// main.js - Ponto de entrada principal
// Detecta a página atual e inicializa o módulo apropriado

import { initCharts } from './charts.js';

// ========== DETECÇÃO DE PÁGINA ==========
function getCurrentPage() {
    const path = window.location.pathname;
    
    if (path.includes('/areas')) return 'areas';
    if (path.includes('/alertas')) return 'alertas';
    if (path.includes('/piscina')) return 'piscina';
    if (path.includes('/resumo-sensores')) return 'resumo-sensores';
    return 'index';
}

// ========== INICIALIZAÇÃO ==========
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 SmartCEU Dashboard - Inicializando...');
    
    const currentPage = getCurrentPage();
    console.log(`📄 Página atual: ${currentPage}`);
    
    // Inicializar gráficos (se houver)
    initCharts();
    
    // Carregar módulo específico da página
    try {
        switch (currentPage) {
            case 'index':
                const { initMainPage } = await import('./pages/main-page.js');
                await initMainPage();
                break;
            
            case 'areas':
                const { initAreasPage } = await import('./pages/areas-page.js');
                await initAreasPage();
                break;
            
            case 'alertas':
                const { initAlertsPage } = await import('./pages/alerts-page.js');
                await initAlertsPage();
                break;
            
            case 'piscina':
                const { initPoolPage } = await import('./pages/pool-page.js');
                await initPoolPage();
                break;
            
            case 'resumo-sensores':
                const { sensorsResumePage } = await import('./pages/sensors-resume-page.js');
                await sensorsResumePage.init();
                break;
            
            default:
                console.warn(`⚠️ Página desconhecida: ${currentPage}`);
        }
        
        console.log('✅ Dashboard inicializado com sucesso!');
    } catch (error) {
        console.error('❌ Erro ao inicializar página:', error);
    }
});
