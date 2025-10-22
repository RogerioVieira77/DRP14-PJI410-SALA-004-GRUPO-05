// Navigation System
function navigateTo(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.classList.remove('active');
    });

    // Show target section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
        
        // Update URL hash
        window.location.hash = sectionId;
        
        // Update active nav links
        updateActiveNavLinks(sectionId);
    }
}

function updateActiveNavLinks(sectionId) {
    // Update header nav
    const headerLinks = document.querySelectorAll('.nav-link');
    headerLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${sectionId}`) {
            link.classList.add('active');
        }
    });

    // Update sidebar nav
    const sidebarItems = document.querySelectorAll('.nav-item');
    sidebarItems.forEach(item => {
        item.classList.remove('active');
    });
}

// Scope Selector
function handleScopeChange(scope) {
    console.log(`Scope changed to: ${scope}`);
    
    // Show notification
    showNotification(`Scope alterado para: ${scope}`, 'info');
    
    // Here you could filter content based on scope
    // For now, just log it
}

// Export Documentation
function exportDocs() {
    showNotification('Exportando documentação...', 'info');
    
    // Get current section
    const activeSection = document.querySelector('.content-section.active');
    const sectionTitle = activeSection.querySelector('h1')?.textContent || 'Documentação';
    
    // Create export content
    const content = activeSection.cloneNode(true);
    
    // Remove breadcrumb and interactive elements
    const breadcrumb = content.querySelector('.breadcrumb');
    if (breadcrumb) breadcrumb.remove();
    
    // Create a simple HTML document
    const exportHtml = `
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${sectionTitle} - IoT Gateway</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            color: #333;
        }
        h1, h2, h3 { color: #2563eb; }
        pre { background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }
        code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
        .card, .content-card { margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
    </style>
</head>
<body>
    ${content.innerHTML}
    <hr>
    <footer style="text-align: center; color: #666; margin-top: 40px;">
        <p>IoT Gateway - Documentação Arquitetônica | Exportado em ${new Date().toLocaleString('pt-BR')}</p>
    </footer>
</body>
</html>
    `;
    
    // Download as HTML file
    const blob = new Blob([exportHtml], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${sectionTitle.replace(/\s+/g, '_')}_${new Date().getTime()}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    setTimeout(() => {
        showNotification('Documentação exportada com sucesso!', 'success');
    }, 500);
}

// Notification System
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existing = document.querySelector('.notification');
    if (existing) {
        existing.remove();
    }
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas ${getNotificationIcon(type)}"></i>
        <span>${message}</span>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 90px;
        right: 20px;
        padding: 15px 20px;
        background: ${getNotificationColor(type)};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 10px;
        animation: slideIn 0.3s ease;
        max-width: 400px;
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function getNotificationIcon(type) {
    const icons = {
        'info': 'fa-info-circle',
        'success': 'fa-check-circle',
        'warning': 'fa-exclamation-triangle',
        'error': 'fa-times-circle'
    };
    return icons[type] || icons.info;
}

function getNotificationColor(type) {
    const colors = {
        'info': '#3b82f6',
        'success': '#10b981',
        'warning': '#f59e0b',
        'error': '#ef4444'
    };
    return colors[type] || colors.info;
}

// Search Functionality
function initSearch() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            performSearch(query);
        });
    }
}

function performSearch(query) {
    if (query.length < 2) return;
    
    const sections = document.querySelectorAll('.content-section');
    const results = [];
    
    sections.forEach(section => {
        const content = section.textContent.toLowerCase();
        if (content.includes(query)) {
            const title = section.querySelector('h1')?.textContent || 'Sem título';
            results.push({
                id: section.id,
                title: title,
                preview: content.substring(content.indexOf(query) - 50, content.indexOf(query) + 100)
            });
        }
    });
    
    displaySearchResults(results, query);
}

function displaySearchResults(results, query) {
    console.log(`Encontrados ${results.length} resultados para: ${query}`, results);
}

// Sidebar Toggle (for mobile)
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.classList.toggle('open');
    }
}

// Print Functionality
function printCurrentSection() {
    window.print();
}

// Copy Code Blocks
function initCodeBlockCopy() {
    const codeBlocks = document.querySelectorAll('.code-block');
    
    codeBlocks.forEach(block => {
        const copyBtn = document.createElement('button');
        copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copiar';
        copyBtn.className = 'copy-code-btn';
        copyBtn.style.cssText = `
            position: absolute;
            top: 10px;
            right: 10px;
            padding: 6px 12px;
            background: #3b82f6;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.85rem;
            opacity: 0;
            transition: opacity 0.3s;
        `;
        
        block.style.position = 'relative';
        block.appendChild(copyBtn);
        
        block.addEventListener('mouseenter', () => {
            copyBtn.style.opacity = '1';
        });
        
        block.addEventListener('mouseleave', () => {
            copyBtn.style.opacity = '0';
        });
        
        copyBtn.addEventListener('click', () => {
            const code = block.querySelector('code').textContent;
            navigator.clipboard.writeText(code).then(() => {
                copyBtn.innerHTML = '<i class="fas fa-check"></i> Copiado!';
                setTimeout(() => {
                    copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copiar';
                }, 2000);
            });
        });
    });
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    // Check for hash in URL
    const hash = window.location.hash.substring(1);
    if (hash) {
        navigateTo(hash);
    } else {
        navigateTo('home');
    }
    
    // Setup header nav links
    const headerLinks = document.querySelectorAll('.nav-link');
    headerLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = link.getAttribute('href').substring(1);
            navigateTo(target);
        });
    });
    
    // Setup scope selector
    const scopeSelector = document.getElementById('scopeSelector');
    if (scopeSelector) {
        scopeSelector.addEventListener('change', (e) => {
            handleScopeChange(e.target.value);
        });
    }
    
    // Initialize code block copy buttons
    initCodeBlockCopy();
    
    // Initialize search
    initSearch();
    
    // Add animation styles
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
        
        @media print {
            .sidebar, .main-header, .main-footer, .breadcrumb {
                display: none !important;
            }
            .main-content {
                margin-left: 0 !important;
                margin-top: 0 !important;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + K for search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.getElementById('searchInput');
            if (searchInput) searchInput.focus();
        }
        
        // Ctrl/Cmd + P for print
        if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
            e.preventDefault();
            printCurrentSection();
        }
        
        // Ctrl/Cmd + E for export
        if ((e.ctrlKey || e.metaKey) && e.key === 'e') {
            e.preventDefault();
            exportDocs();
        }
    });
    
    console.log('IoT Gateway Documentation loaded successfully!');
    console.log('Keyboard shortcuts:');
    console.log('- Ctrl/Cmd + E: Export current section');
    console.log('- Ctrl/Cmd + P: Print current section');
});

// Handle browser back/forward
window.addEventListener('popstate', () => {
    const hash = window.location.hash.substring(1);
    if (hash) {
        navigateTo(hash);
    }
});

// Smooth scroll for anchor links
document.addEventListener('click', (e) => {
    if (e.target.tagName === 'A' && e.target.getAttribute('href')?.startsWith('#')) {
        e.preventDefault();
        const target = e.target.getAttribute('href').substring(1);
        navigateTo(target);
    }
});

// Add loading indicator for async operations
function showLoading() {
    const loader = document.createElement('div');
    loader.id = 'loader';
    loader.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    `;
    loader.innerHTML = `
        <div style="background: white; padding: 30px; border-radius: 12px; text-align: center;">
            <div style="width: 50px; height: 50px; border: 4px solid #e5e7eb; border-top: 4px solid #3b82f6; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 15px;"></div>
            <p style="color: #64748b; font-weight: 600;">Carregando...</p>
        </div>
    `;
    document.body.appendChild(loader);
}

function hideLoading() {
    const loader = document.getElementById('loader');
    if (loader) loader.remove();
}

// Add spin animation
const spinAnimation = document.createElement('style');
spinAnimation.textContent = `
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
`;
document.head.appendChild(spinAnimation);
