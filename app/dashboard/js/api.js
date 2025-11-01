// api.js - Módulo de comunicação com API
// Centraliza todas as chamadas à API do backend

const API_BASE = '/smartceu/api/v1/dashboard';

// ========== ESTATÍSTICAS GERAIS ==========
export async function fetchCurrentStats() {
    try {
        const response = await fetch(`${API_BASE}/current-stats`);
        if (!response.ok) throw new Error('Erro ao buscar estatísticas');
        return await response.json();
    } catch (error) {
        console.error('Erro em fetchCurrentStats:', error);
        return null;
    }
}

export async function fetchAdvancedStats() {
    try {
        const response = await fetch(`${API_BASE}/advanced-stats`);
        if (!response.ok) throw new Error('Erro ao buscar estatísticas avançadas');
        return await response.json();
    } catch (error) {
        console.error('Erro em fetchAdvancedStats:', error);
        return null;
    }
}

// ========== FLUXO DE PESSOAS ==========
export async function fetchPeopleFlow() {
    try {
        const response = await fetch(`${API_BASE}/people-flow`);
        if (!response.ok) throw new Error('Erro ao buscar fluxo de pessoas');
        return await response.json();
    } catch (error) {
        console.error('Erro em fetchPeopleFlow:', error);
        return null;
    }
}

export async function fetchPeakPrediction() {
    try {
        const response = await fetch(`${API_BASE}/peak-prediction`);
        if (!response.ok) throw new Error('Erro ao buscar previsão de pico');
        return await response.json();
    } catch (error) {
        console.error('Erro em fetchPeakPrediction:', error);
        return null;
    }
}

// ========== ÁREAS ==========
export async function fetchAreasOccupation() {
    try {
        const response = await fetch(`${API_BASE}/areas-occupation`);
        if (!response.ok) throw new Error('Erro ao buscar ocupação por área');
        return await response.json();
    } catch (error) {
        console.error('Erro em fetchAreasOccupation:', error);
        return null;
    }
}

// ========== PISCINA ==========
export async function fetchPoolCurrent() {
    try {
        const response = await fetch(`${API_BASE}/pool/current`);
        if (!response.ok) throw new Error('Erro ao buscar status da piscina');
        return await response.json();
    } catch (error) {
        console.error('Erro em fetchPoolCurrent:', error);
        return null;
    }
}

export async function fetchPoolQuality() {
    try {
        const response = await fetch(`${API_BASE}/pool/quality`);
        if (!response.ok) throw new Error('Erro ao buscar qualidade da água');
        return await response.json();
    } catch (error) {
        console.error('Erro em fetchPoolQuality:', error);
        return null;
    }
}

// ========== ALERTAS ==========
export async function fetchActiveAlerts() {
    try {
        const response = await fetch(`${API_BASE}/alerts/active`);
        if (!response.ok) throw new Error('Erro ao buscar alertas');
        return await response.json();
    } catch (error) {
        console.error('Erro em fetchActiveAlerts:', error);
        return null;
    }
}
