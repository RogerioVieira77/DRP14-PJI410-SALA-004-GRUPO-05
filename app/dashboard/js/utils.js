// utils.js - Funções utilitárias compartilhadas
// Helpers gerais para uso em todas as páginas

// ========== SELETORES DOM ==========
export const $ = (selector) => document.querySelector(selector);
export const $$ = (selector) => document.querySelectorAll(selector);

// ========== NÚMEROS ALEATÓRIOS ==========
export const randomBetweenFloat = (min, max) => {
    const value = Math.random() * (max - min) + min;
    return Number(value.toFixed(2));
};

export const randomBetween = (min, max) => Math.floor(Math.random() * (max - min) + min);

// ========== ATUALIZAÇÃO DE STATUS ==========
export function updateStatus(selector, value, warn, danger, normalText, warnText, dangerText) {
    const statusElement = $(selector);
    statusElement.classList.remove('status-normal', 'status-warning', 'status-danger');
    if (value >= danger) {
        statusElement.classList.add('status-danger');
        statusElement.textContent = dangerText;
    } else if (value >= warn) {
        statusElement.classList.add('status-warning');
        statusElement.textContent = warnText;
    } else {
        statusElement.classList.add('status-normal');
        statusElement.textContent = normalText;
    }
}

export function updateElement(status, card, text, type) {
    const cardElement = $(card);
    cardElement.classList.remove('metric-card', 'info', 'warning', 'danger');
    cardElement.classList.add('metric-card', type);
    const statusElement = cardElement.querySelector('.metric-status');
    if (statusElement) {
        statusElement.classList.remove('status-normal', 'status-warning', 'status-danger');
        statusElement.classList.add(`status-${type === 'metric-card' ? 'normal' : type}`);
        statusElement.textContent = text;
    }
}

// ========== FORMATAÇÃO ==========
export function formatTimestamp(isoString) {
    if (!isoString) return 'N/A';
    const date = new Date(isoString);
    return date.toLocaleString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

export function formatRelativeTime(isoString) {
    if (!isoString) return 'N/A';
    const date = new Date(isoString);
    const now = new Date();
    const diff = Math.floor((now - date) / 1000); // diferença em segundos
    
    if (diff < 60) return `${diff}s atrás`;
    if (diff < 3600) return `${Math.floor(diff / 60)}min atrás`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h atrás`;
    return `${Math.floor(diff / 86400)}d atrás`;
}
