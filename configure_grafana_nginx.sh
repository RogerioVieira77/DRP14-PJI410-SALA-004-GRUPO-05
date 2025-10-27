#!/bin/bash
###############################################################################
# Script de Configuração do Nginx para Grafana
# CEU Tres Pontes - Sistema de Controle de Acesso
# 
# Este script configura o Nginx como proxy reverso para o Grafana
# 
# Uso: sudo bash configure_grafana_nginx.sh
###############################################################################

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar se está rodando como root
if [[ $EUID -ne 0 ]]; then
   log_error "Este script deve ser executado como root (use sudo)"
   exit 1
fi

echo "=========================================================="
echo "  Configuração Nginx para Grafana - CEU Tres Pontes"
echo "=========================================================="
echo ""

# Verificar se Nginx está instalado
if ! command -v nginx &> /dev/null; then
    log_error "Nginx não está instalado!"
    log_info "Instale o Nginx primeiro: sudo apt-get install nginx"
    exit 1
fi
log_success "Nginx encontrado"

# Verificar se Grafana está rodando
if ! systemctl is-active --quiet grafana-server; then
    log_error "Grafana não está rodando!"
    log_info "Inicie o Grafana: sudo systemctl start grafana-server"
    exit 1
fi
log_success "Grafana está rodando"

# Solicitar informações
echo ""
log_info "Digite as informações do servidor:"
echo ""
read -p "Domínio ou IP público (ex: grafana.ceutrespontes.com): " DOMAIN

if [ -z "$DOMAIN" ]; then
    log_error "Domínio é obrigatório!"
    exit 1
fi

# Perguntar sobre SSL
echo ""
read -p "Deseja configurar SSL com Let's Encrypt? (s/n): " USE_SSL

# Criar configuração do Nginx
NGINX_CONF="/etc/nginx/sites-available/grafana"
log_info "Criando configuração do Nginx..."

if [[ $USE_SSL =~ ^[Ss]$ ]]; then
    # Configuração com SSL
    cat > "$NGINX_CONF" <<EOF
# Configuração Nginx para Grafana - CEU Tres Pontes
# Gerado em: $(date)

# Redirecionar HTTP para HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name $DOMAIN;
    
    # Redirecionar para HTTPS
    return 301 https://\$server_name\$request_uri;
}

# Servidor HTTPS
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name $DOMAIN;
    
    # Certificados SSL (serão configurados com certbot)
    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;
    
    # Configurações SSL modernas
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Logs
    access_log /var/log/nginx/grafana-access.log;
    error_log /var/log/nginx/grafana-error.log;
    
    # Headers de segurança
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Proxy para Grafana
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Forwarded-Host \$host;
        proxy_set_header X-Forwarded-Port \$server_port;
        
        # WebSocket support para live updates
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
        proxy_read_timeout 300;
        send_timeout 300;
    }
    
    # API do Grafana
    location /api/ {
        proxy_pass http://localhost:3000/api/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
else
    # Configuração sem SSL
    cat > "$NGINX_CONF" <<EOF
# Configuração Nginx para Grafana - CEU Tres Pontes
# Gerado em: $(date)
# ⚠️ ATENÇÃO: Esta configuração NÃO usa SSL/HTTPS
# Para produção, recomenda-se configurar SSL

server {
    listen 80;
    listen [::]:80;
    server_name $DOMAIN;
    
    # Logs
    access_log /var/log/nginx/grafana-access.log;
    error_log /var/log/nginx/grafana-error.log;
    
    # Proxy para Grafana
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
        proxy_read_timeout 300;
    }
    
    # API do Grafana
    location /api/ {
        proxy_pass http://localhost:3000/api/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF
fi

log_success "Configuração criada"

# Criar link simbólico
log_info "Ativando configuração..."
ln -sf "$NGINX_CONF" /etc/nginx/sites-enabled/grafana
log_success "Configuração ativada"

# Testar configuração
log_info "Testando configuração do Nginx..."
if nginx -t 2>&1 | tee /tmp/nginx_test.log; then
    log_success "Configuração válida"
else
    log_error "Erro na configuração do Nginx"
    cat /tmp/nginx_test.log
    exit 1
fi

# Recarregar Nginx
log_info "Recarregando Nginx..."
systemctl reload nginx
log_success "Nginx recarregado"

# Configurar SSL se solicitado
if [[ $USE_SSL =~ ^[Ss]$ ]]; then
    echo ""
    log_info "Configurando SSL com Let's Encrypt..."
    
    # Verificar se certbot está instalado
    if ! command -v certbot &> /dev/null; then
        log_info "Instalando Certbot..."
        apt-get update
        apt-get install -y certbot python3-certbot-nginx
        log_success "Certbot instalado"
    fi
    
    # Obter certificado
    log_info "Obtendo certificado SSL para $DOMAIN..."
    log_warning "Certifique-se de que o domínio aponta para este servidor!"
    echo ""
    
    certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos --register-unsafely-without-email || {
        log_warning "Falha ao obter certificado SSL automaticamente"
        log_info "Execute manualmente: sudo certbot --nginx -d $DOMAIN"
    }
    
    # Configurar renovação automática
    log_info "Configurando renovação automática..."
    systemctl enable certbot.timer
    systemctl start certbot.timer
    log_success "Renovação automática configurada"
fi

# Configurar firewall
log_info "Configurando firewall..."
if command -v ufw &> /dev/null; then
    ufw allow 'Nginx Full'
    ufw reload
    log_success "Firewall configurado (UFW)"
elif command -v iptables &> /dev/null; then
    iptables -A INPUT -p tcp --dport 80 -j ACCEPT
    iptables -A INPUT -p tcp --dport 443 -j ACCEPT
    iptables-save > /etc/iptables/rules.v4 2>/dev/null || true
    log_success "Firewall configurado (iptables)"
else
    log_warning "Firewall não detectado - configure manualmente"
fi

# Atualizar configuração do Grafana
log_info "Atualizando configuração do Grafana..."
GRAFANA_INI="/etc/grafana/grafana.ini"

# Backup da configuração original
cp "$GRAFANA_INI" "${GRAFANA_INI}.backup.$(date +%Y%m%d_%H%M%S)"

# Atualizar configurações
sed -i "s|^;domain =.*|domain = $DOMAIN|" "$GRAFANA_INI"

if [[ $USE_SSL =~ ^[Ss]$ ]]; then
    sed -i "s|^;root_url =.*|root_url = https://$DOMAIN/|" "$GRAFANA_INI"
else
    sed -i "s|^;root_url =.*|root_url = http://$DOMAIN/|" "$GRAFANA_INI"
fi

log_success "Configuração do Grafana atualizada"

# Reiniciar Grafana
log_info "Reiniciando Grafana..."
systemctl restart grafana-server
sleep 3

if systemctl is-active --quiet grafana-server; then
    log_success "Grafana reiniciado"
else
    log_error "Falha ao reiniciar Grafana"
    exit 1
fi

echo ""
echo "=========================================================="
echo "  ✅ Configuração Concluída com Sucesso!"
echo "=========================================================="
echo ""

if [[ $USE_SSL =~ ^[Ss]$ ]]; then
    echo "🌐 Acesse o Grafana em: https://$DOMAIN"
else
    echo "🌐 Acesse o Grafana em: http://$DOMAIN"
fi

echo ""
echo "🔐 Credenciais:"
echo "   Usuário: admin"
echo "   Senha: [sua senha alterada]"
echo ""
echo "📝 Arquivos criados:"
echo "   • Nginx config: $NGINX_CONF"
echo "   • Backup Grafana: ${GRAFANA_INI}.backup.*"
echo ""
echo "🔍 Comandos úteis:"
echo "   • Ver logs Nginx: sudo tail -f /var/log/nginx/grafana-access.log"
echo "   • Ver logs Grafana: sudo journalctl -u grafana-server -f"
echo "   • Status Nginx: sudo systemctl status nginx"
echo "   • Status Grafana: sudo systemctl status grafana-server"
echo ""

if [[ ! $USE_SSL =~ ^[Ss]$ ]]; then
    log_warning "Você está usando HTTP sem SSL!"
    echo "   Para adicionar SSL depois: sudo certbot --nginx -d $DOMAIN"
    echo ""
fi

echo "📚 Documentação completa: docs/GRAFANA_SETUP_GUIDE.md"
echo ""
