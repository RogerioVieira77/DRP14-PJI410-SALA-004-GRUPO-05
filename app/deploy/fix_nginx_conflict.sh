#!/bin/bash

################################################################################
# SmartCEU - Reconfigurar NGINX para conviver com Agasalho Aqui
# Usa prefixo /smartceu para evitar conflitos
################################################################################

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_step() {
    echo -e "${BLUE}>>> $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}   Reconfigurando NGINX - SmartCEU com prefixo /smartceu${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

# Backup da config atual
print_step "Fazendo backup da configuração atual..."
cp /etc/nginx/sites-available/agasalho_aqui /etc/nginx/sites-available/agasalho_aqui.backup_$(date +%Y%m%d_%H%M%S)
print_success "Backup criado"

# Reescrever configuração do Agasalho Aqui (manter como está, mas documentar)
print_step "Atualizando configuração do Agasalho Aqui..."
cat > /etc/nginx/sites-available/agasalho_aqui << 'EOF'
# Agasalho Aqui - Aplicação Principal
# Captura todas as requisições que não sejam /smartceu
server {
    listen 80 default_server;
    server_name 82.25.75.88;

    # Logs
    access_log /var/log/nginx/agasalho_access.log;
    error_log /var/log/nginx/agasalho_error.log;

    location /static {
        alias /var/www/agasalho_aqui/aplicacao/tem_agasalho_aqui/static;
    }

    # Aplicação principal
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

print_success "Configuração do Agasalho Aqui atualizada"

# Criar nova configuração do SmartCEU com prefixo
print_step "Criando nova configuração do SmartCEU..."
cat > /etc/nginx/sites-available/smartceu << 'EOF'
# SmartCEU - Sistema de Monitoramento
# Acessível via prefixo /smartceu
server {
    listen 80;
    server_name 82.25.75.88;

    # Logs
    access_log /var/log/nginx/smartceu_access.log;
    error_log /var/log/nginx/smartceu_error.log;

    # Frontend SmartCEU - Dashboard Principal
    location /smartceu {
        alias /var/www/smartceu/app/frontend;
        index smart_ceu.html index.html;
        try_files $uri $uri/ =404;
    }

    # Página específica - Pool Monitoring
    location /smartceu/pool {
        alias /var/www/smartceu/app/frontend;
        try_files /monitoramento_piscina.html =404;
    }

    # Assets estáticos do SmartCEU
    location /smartceu/assets/ {
        alias /var/www/smartceu/app/frontend/assets/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # API SmartCEU
    location /smartceu/api/ {
        proxy_pass http://127.0.0.1:5001/api/;
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
    location /smartceu/health {
        proxy_pass http://127.0.0.1:5001/health;
        access_log off;
    }
}
EOF

print_success "Configuração do SmartCEU criada com prefixo /smartceu"

# Testar configuração
print_step "Testando configuração do NGINX..."
if nginx -t 2>&1 | grep -q "successful"; then
    print_success "Configuração válida"
else
    print_error "Erro na configuração do NGINX"
    nginx -t
    exit 1
fi

# Recarregar NGINX
print_step "Recarregando NGINX..."
systemctl reload nginx

if [ $? -eq 0 ]; then
    print_success "NGINX recarregado com sucesso"
else
    print_error "Falha ao recarregar NGINX"
    exit 1
fi

# Verificar se serviços estão rodando
print_step "Verificando serviços..."

if systemctl is-active --quiet smartceu-api; then
    print_success "SmartCEU API: Rodando"
else
    print_error "SmartCEU API: Não está ativo"
fi

if curl -s http://localhost:8000 >/dev/null; then
    print_success "Agasalho Aqui: Respondendo"
else
    print_error "Agasalho Aqui: Não está respondendo"
fi

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Reconfiguração Concluída!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}🌐 Acessos Atualizados:${NC}"
echo ""
echo -e "${YELLOW}Agasalho Aqui (principal):${NC}"
echo "   http://82.25.75.88/"
echo ""
echo -e "${YELLOW}SmartCEU (com prefixo):${NC}"
echo "   • Dashboard: http://82.25.75.88/smartceu/smart_ceu.html"
echo "   • Pool Monitor: http://82.25.75.88/smartceu/pool"
echo "   • API Health: http://82.25.75.88/smartceu/health"
echo "   • API Sensors: http://82.25.75.88/smartceu/api/sensors"
echo ""
echo -e "${BLUE}📝 Testes:${NC}"
echo "   curl http://82.25.75.88/"
echo "   curl http://82.25.75.88/smartceu/health"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

exit 0
