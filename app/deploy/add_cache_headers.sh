#!/bin/bash
# Adicionar headers para desabilitar cache em páginas HTML do SmartCEU

CONFIG_FILE="/etc/nginx/sites-available/agasalho_aqui"

echo "📝 Adicionando headers de cache control..."

# Backup
cp $CONFIG_FILE ${CONFIG_FILE}.bak_$(date +%Y%m%d_%H%M%S)

# Criar configuração atualizada
cat > $CONFIG_FILE << 'NGINX_CONFIG'
server {
    listen 80 default_server;
    server_name 82.25.75.88;
    
    # Logs
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    # SmartCEU - Página Principal
    location = /smartceu {
        alias /var/www/smartceu/app/smart_ceu.html;
        default_type text/html;
        add_header Content-Type "text/html; charset=UTF-8";
        add_header Cache-Control "no-store, no-cache, must-revalidate, max-age=0";
        add_header Pragma "no-cache";
        access_log /var/log/nginx/smartceu_access.log;
    }

    # SmartCEU - Monitoramento Piscina
    location = /smartceu/pool {
        alias /var/www/smartceu/app/monitoramento_piscina.html;
        default_type text/html;
        add_header Content-Type "text/html; charset=UTF-8";
        add_header Cache-Control "no-store, no-cache, must-revalidate, max-age=0";
        add_header Pragma "no-cache";
        access_log /var/log/nginx/smartceu_access.log;
    }

    # Página de Teste da API
    location = /smartceu/test_page.html {
        alias /var/www/smartceu/app/test_page.html;
        default_type text/html;
        add_header Content-Type "text/html; charset=UTF-8";
        add_header Cache-Control "no-store, no-cache, must-revalidate, max-age=0";
        add_header Pragma "no-cache";
        access_log /var/log/nginx/smartceu_access.log;
    }

    # Documentação Arquitetura
    location = /smartceu/doc_arq.html {
        alias /var/www/smartceu/app/docs-web/doc_arq.html;
        default_type text/html;
        add_header Content-Type "text/html; charset=UTF-8";
        add_header Cache-Control "no-store, no-cache, must-revalidate, max-age=0";
        add_header Pragma "no-cache";
        access_log /var/log/nginx/smartceu_access.log;
    }

    # Assets (CSS, JS, imagens)
    location /smartceu/assets/ {
        alias /var/www/smartceu/app/docs-web/assets/;
        access_log /var/log/nginx/smartceu_access.log;
    }

    # API do SmartCEU
    location /smartceu/api/ {
        proxy_pass http://127.0.0.1:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Content-Type $content_type;
        
        # CORS headers - Apenas se necessário
        add_header Access-Control-Allow-Origin * always;
        add_header Access-Control-Allow-Methods 'GET, POST, PUT, DELETE, OPTIONS' always;
        add_header Access-Control-Allow-Headers 'Content-Type, Authorization' always;
        
        # Handle OPTIONS
        if ($request_method = 'OPTIONS') {
            return 204;
        }
    }

    # Health check direto
    location = /smartceu/health {
        proxy_pass http://127.0.0.1:5000/health;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        
        add_header Access-Control-Allow-Origin *;
    }

    # Agasalho Aqui - Catch all (última prioridade)
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGINX_CONFIG

echo "✓ Configuração atualizada"

# Testar configuração
if nginx -t; then
    echo "✓ Configuração válida"
    systemctl reload nginx
    echo "✓ NGINX recarregado com headers anti-cache"
    echo ""
    echo "🌐 Teste agora (Ctrl+F5 para forçar reload):"
    echo "   http://82.25.75.88/smartceu/pool"
else
    echo "✗ Erro na configuração - restaurando backup"
    mv ${CONFIG_FILE}.bak_$(date +%Y%m%d_%H%M%S) $CONFIG_FILE
    exit 1
fi
