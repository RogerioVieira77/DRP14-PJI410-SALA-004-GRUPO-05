#!/bin/bash

echo "========================================"
echo "FIX NGINX - SmartCEU vs Agasalho Aqui"
echo "========================================"

# Backup das configurações
cp /etc/nginx/sites-available/agasalho_aqui /etc/nginx/sites-available/agasalho_aqui.backup
cp /etc/nginx/sites-available/smartceu /etc/nginx/sites-available/smartceu.backup

# Criar configuração do Agasalho Aqui com EXCEÇÃO para /smartceu
cat > /etc/nginx/sites-available/agasalho_aqui << 'EOF'
# Agasalho Aqui - Aplicação Principal
server {
    listen 80 default_server;
    server_name 82.25.75.88;

    # Logs
    access_log /var/log/nginx/agasalho_access.log;
    error_log /var/log/nginx/agasalho_error.log;

    # EXCEÇÃO: Rotas /smartceu são tratadas pelo outro server block
    # Este location tem maior prioridade que location /
    location /smartceu {
        return 404 "Rota gerenciada pelo SmartCEU server block";
    }

    location /static {
        alias /var/www/agasalho_aqui/aplicacao/tem_agasalho_aqui/static;
    }

    # Aplicação principal - captura tudo exceto /smartceu
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Criar configuração SmartCEU corrigida (SEM default_server, mas com MAIOR especificidade)
cat > /etc/nginx/sites-available/smartceu << 'EOF'
# SmartCEU - Sistema de Monitoramento
server {
    listen 80;
    server_name 82.25.75.88;

    # Logs
    access_log /var/log/nginx/smartceu_access.log;
    error_log /var/log/nginx/smartceu_error.log;

    # Dashboard principal SmartCEU
    location = /smartceu {
        alias /var/www/smartceu/app/smart_ceu.html;
    }

    # Página específica - Pool Monitoring
    location = /smartceu/pool {
        alias /var/www/smartceu/app/monitoramento_piscina.html;
    }

    # Assets do docs-web
    location /smartceu/assets/ {
        alias /var/www/smartceu/app/docs-web/assets/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # API SmartCEU
    location /smartceu/api/ {
        # Remove /smartceu do path antes de passar para API
        rewrite ^/smartceu/api/(.*)$ /api/$1 break;

        proxy_pass http://127.0.0.1:5000/;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check SmartCEU
    location = /smartceu/health {
        proxy_pass http://127.0.0.1:5000/health;
        proxy_set_header Host $host;
        access_log off;
    }

    # Qualquer outra rota /smartceu/* que não foi capturada acima
    location /smartceu/ {
        return 404 "Rota SmartCEU não encontrada";
    }
}
EOF

echo ""
echo "✓ Configurações criadas"
echo ""

# Testar sintaxe NGINX
echo "Testando sintaxe do NGINX..."
nginx -t

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Sintaxe OK - Recarregando NGINX..."
    systemctl reload nginx
    
    echo ""
    echo "========================================"
    echo "NGINX recarregado com sucesso!"
    echo "========================================"
    echo ""
    echo "Testando as aplicações:"
    echo ""
    
    echo "1. Agasalho Aqui (raiz):"
    curl -I http://localhost/ 2>&1 | grep HTTP
    
    echo ""
    echo "2. SmartCEU Health:"
    curl -s http://localhost/smartceu/health | head -3
    
    echo ""
    echo "3. SmartCEU API:"
    curl -s http://localhost/smartceu/api/v1/sensors | head -5
    
else
    echo ""
    echo "✗ ERRO na sintaxe do NGINX!"
    echo "Restaurando backups..."
    cp /etc/nginx/sites-available/agasalho_aqui.backup /etc/nginx/sites-available/agasalho_aqui
    cp /etc/nginx/sites-available/smartceu.backup /etc/nginx/sites-available/smartceu
    systemctl reload nginx
    exit 1
fi

echo ""
echo "========================================"
echo "URLs disponíveis:"
echo "========================================"
echo "Agasalho Aqui:  http://82.25.75.88/"
echo "SmartCEU:       http://82.25.75.88/smartceu"
echo "SmartCEU Pool:  http://82.25.75.88/smartceu/pool"
echo "SmartCEU API:   http://82.25.75.88/smartceu/api/v1/sensors"
echo "Health Check:   http://82.25.75.88/smartceu/health"
echo "========================================"
