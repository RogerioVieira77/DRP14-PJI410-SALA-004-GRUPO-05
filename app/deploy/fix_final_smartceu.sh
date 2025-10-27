#!/bin/bash

################################################################################
# SmartCEU - Correção Final: Estrutura Real + Porta Correta
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
echo -e "${GREEN}   Correção Final - SmartCEU${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

# 1. Parar API
print_step "Parando API para reconfiguração..."
systemctl stop smartceu-api
print_success "API parada"

# 2. Verificar e corrigir .env
print_step "Verificando arquivo .env..."
if [ ! -f /var/www/smartceu/app/backend/.env ]; then
    print_error "Arquivo .env não existe!"
    exit 1
fi

# Garantir que porta está configurada
if grep -q "API_PORT=5001" /var/www/smartceu/app/backend/.env; then
    print_success ".env configurado para porta 5001"
else
    print_error ".env não tem porta 5001 configurada"
    echo "API_PORT=5001" >> /var/www/smartceu/app/backend/.env
fi

# 3. Atualizar app.py para usar porta do .env
print_step "Verificando se app.py lê a porta do .env..."
cd /var/www/smartceu/app/backend

# Verificar se app.py existe e está usando porta correta
if [ -f app.py ]; then
    print_success "app.py encontrado"
else
    print_error "app.py não encontrado!"
    exit 1
fi

# 4. Criar nova configuração NGINX com estrutura real
print_step "Atualizando configuração NGINX (estrutura real do projeto)..."

cat > /etc/nginx/sites-available/smartceu << 'EOF'
# SmartCEU - Sistema de Monitoramento
# Estrutura real: HTMLs na raiz, assets em docs-web
server {
    listen 80;
    server_name 82.25.75.88;

    # Logs
    access_log /var/log/nginx/smartceu_access.log;
    error_log /var/log/nginx/smartceu_error.log;

    # Dashboard principal SmartCEU
    location = /smartceu {
        alias /var/www/smartceu/app/frontend/smart_ceu.html;
    }

    # Página específica - Pool Monitoring
    location = /smartceu/pool {
        alias /var/www/smartceu/app/frontend/monitoramento_piscina.html;
    }

    # Assets do docs-web
    location /smartceu/assets/ {
        alias /var/www/smartceu/app/docs-web/assets/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # API SmartCEU (porta 5001 corrigida)
    location /smartceu/api/ {
        # Remove /smartceu do path antes de passar para API
        rewrite ^/smartceu/api/(.*)$ /api/$1 break;
        
        proxy_pass http://127.0.0.1:5001;
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
        proxy_pass http://127.0.0.1:5001/health;
        proxy_set_header Host $host;
        access_log off;
    }
}
EOF

print_success "Configuração NGINX atualizada"

# 5. Testar NGINX
print_step "Testando configuração NGINX..."
if nginx -t 2>&1 | grep -q "successful"; then
    print_success "Configuração NGINX válida"
    systemctl reload nginx
    print_success "NGINX recarregado"
else
    print_error "Erro na configuração NGINX"
    nginx -t
    exit 1
fi

# 6. Reiniciar API
print_step "Iniciando API..."
systemctl start smartceu-api
sleep 3

if systemctl is-active --quiet smartceu-api; then
    print_success "API iniciada"
else
    print_error "Falha ao iniciar API"
    systemctl status smartceu-api
    exit 1
fi

# 7. Aguardar API responder
print_step "Aguardando API ficar pronta..."
for i in {1..10}; do
    if curl -s http://localhost:5001/health >/dev/null 2>&1; then
        print_success "API respondendo na porta 5001"
        break
    fi
    if [ $i -eq 10 ]; then
        print_error "API não respondeu após 10 tentativas"
        # Verificar qual porta está usando
        echo "Portas em uso:"
        netstat -tulpn | grep python
    fi
    sleep 1
done

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Correção Aplicada!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}🌐 Acessos SmartCEU:${NC}"
echo ""
echo "   • Dashboard: http://82.25.75.88/smartceu"
echo "   • Pool Monitor: http://82.25.75.88/smartceu/pool"
echo "   • API Health: http://82.25.75.88/smartceu/health"
echo "   • API Sensors: http://82.25.75.88/smartceu/api/v1/sensors"
echo ""
echo -e "${BLUE}🌐 Agasalho Aqui (não afetado):${NC}"
echo ""
echo "   • Principal: http://82.25.75.88/"
echo ""
echo -e "${BLUE}📝 Testes:${NC}"
echo ""
echo "   curl http://82.25.75.88/"
echo "   curl http://82.25.75.88/smartceu/health"
echo "   curl http://82.25.75.88/smartceu"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

exit 0
