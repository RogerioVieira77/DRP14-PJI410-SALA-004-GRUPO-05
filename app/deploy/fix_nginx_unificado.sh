#!/bin/bash

echo "========================================"
echo "FIX NGINX - Unificando em um só bloco"
echo "========================================"

# Desabilitar SmartCEU temporariamente
rm -f /etc/nginx/sites-enabled/smartceu

# Criar configuração UNIFICADA no Agasalho Aqui
cat > /etc/nginx/sites-available/agasalho_aqui << 'EOF'
# Aplicações no Servidor: Agasalho Aqui + SmartCEU
server {
    listen 80 default_server;
    server_name 82.25.75.88;

    # Logs gerais
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    #############################################
    # SMARTCEU - Rotas específicas primeiro
    #############################################

    # Dashboard principal SmartCEU
    location = /smartceu {
        alias /var/www/smartceu/app/smart_ceu.html;
        access_log /var/log/nginx/smartceu_access.log;
    }

    # Página Pool Monitoring
    location = /smartceu/pool {
        alias /var/www/smartceu/app/monitoramento_piscina.html;
        access_log /var/log/nginx/smartceu_access.log;
    }

    # Assets do SmartCEU
    location /smartceu/assets/ {
        alias /var/www/smartceu/app/docs-web/assets/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log /var/log/nginx/smartceu_access.log;
    }

    # API SmartCEU
    location /smartceu/api/ {
        rewrite ^/smartceu/api/(.*)$ /api/$1 break;
        
        proxy_pass http://127.0.0.1:5000/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        access_log /var/log/nginx/smartceu_access.log;
        error_log /var/log/nginx/smartceu_error.log;
    }

    # Health check SmartCEU
    location = /smartceu/health {
        proxy_pass http://127.0.0.1:5000/health;
        proxy_set_header Host $host;
        access_log /var/log/nginx/smartceu_access.log;
    }

    #############################################
    # AGASALHO AQUI - Aplicação principal
    #############################################

    location /static {
        alias /var/www/agasalho_aqui/aplicacao/tem_agasalho_aqui/static;
        access_log /var/log/nginx/agasalho_access.log;
    }

    # Aplicação Agasalho Aqui (captura tudo que não for /smartceu)
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        access_log /var/log/nginx/agasalho_access.log;
        error_log /var/log/nginx/agasalho_error.log;
    }
}
EOF

echo ""
echo "✓ Configuração unificada criada"
echo ""

# Testar sintaxe
nginx -t

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Sintaxe OK - Recarregando NGINX..."
    systemctl reload nginx
    sleep 2
    
    echo ""
    echo "========================================"
    echo "TESTES:"
    echo "========================================"
    
    echo ""
    echo "1. Agasalho Aqui (raiz):"
    curl -I http://localhost/ 2>&1 | grep HTTP
    
    echo ""
    echo "2. SmartCEU Health Check:"
    curl -s http://localhost/smartceu/health
    
    echo ""
    echo "3. SmartCEU API Sensors:"
    curl -s http://localhost/smartceu/api/v1/sensors
    
    echo ""
    echo "4. SmartCEU Dashboard:"
    curl -I http://localhost/smartceu 2>&1 | grep HTTP
    
    echo ""
    echo "========================================"
    echo "✓ NGINX configurado com sucesso!"
    echo "========================================"
    
else
    echo ""
    echo "✗ ERRO na sintaxe!"
    exit 1
fi

echo ""
echo "URLs disponíveis:"
echo "  - http://82.25.75.88/            (Agasalho Aqui)"
echo "  - http://82.25.75.88/smartceu    (SmartCEU Dashboard)"
echo "  - http://82.25.75.88/smartceu/pool"
echo "  - http://82.25.75.88/smartceu/api/v1/..."
echo "  - http://82.25.75.88/smartceu/health"
echo ""
