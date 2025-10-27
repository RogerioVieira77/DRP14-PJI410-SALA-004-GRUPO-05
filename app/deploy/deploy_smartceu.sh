#!/bin/bash

################################################################################
# SmartCEU - Script de Deploy Automatizado
# Ubuntu 24.04 LTS @ Hostinger VPS (82.25.75.88)
# 
# Este script automatiza todo o processo de deploy do SmartCEU em produção
# Tempo estimado: 5-10 minutos
#
# Uso: sudo bash deploy_smartceu.sh
################################################################################

set -e  # Exit on error

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configurações
PROJECT_NAME="smartceu"
PROJECT_DIR="/var/www/smartceu"
APP_USER="www-data"
GIT_REPO="https://github.com/RogerioVieira77/PI---IV---V1.git"

# Portas
API_PORT="5001"
MQTT_PORT="1884"

# MySQL
MYSQL_ROOT_PASS="Ceu@)@%01"
DB_NAME="smartceu_db"
DB_USER="smartceu_user"
DB_PASS="SmartCEU2025)!"

# MQTT
MQTT_USER="smartceu_mqtt"
MQTT_PASS="smartceu_user"

# Funções auxiliares
print_step() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}>>> $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

check_root() {
    if [ "$EUID" -ne 0 ]; then 
        print_error "Este script precisa ser executado como root (sudo)"
        exit 1
    fi
}

# Início do script
clear
echo -e "${GREEN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ███████╗███╗   ███╗ █████╗ ██████╗ ████████╗ ██████╗███████╗██╗   ██╗ ║
║   ██╔════╝████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██╔════╝██║   ██║ ║
║   ███████╗██╔████╔██║███████║██████╔╝   ██║   ██║     █████╗  ██║   ██║ ║
║   ╚════██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║   ██║     ██╔══╝  ██║   ██║ ║
║   ███████║██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   ╚██████╗███████╗╚██████╔╝ ║
║   ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝╚══════╝ ╚═════╝  ║
║                                                               ║
║              Deploy Automatizado - Versão 1.0                ║
║                     Ubuntu 24.04 LTS                          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

check_root

print_warning "Este script irá instalar o SmartCEU em: $PROJECT_DIR"
print_warning "MySQL Database: $DB_NAME | User: $DB_USER"
print_warning "API Port: $API_PORT | MQTT Port: $MQTT_PORT"
echo ""
read -p "Deseja continuar? (s/N): " -r
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    print_error "Deploy cancelado pelo usuário"
    exit 1
fi

START_TIME=$(date +%s)

################################################################################
# ETAPA 1: Criar estrutura de diretórios
################################################################################
print_step "ETAPA 1/10: Criando estrutura de diretórios"

mkdir -p ${PROJECT_DIR}/{app,venv,logs,backups,config}
chown -R ${APP_USER}:${APP_USER} ${PROJECT_DIR}
chmod 755 ${PROJECT_DIR}

print_success "Diretórios criados em: ${PROJECT_DIR}"

################################################################################
# ETAPA 2: Instalar dependências do sistema
################################################################################
print_step "ETAPA 2/10: Instalando dependências do sistema"

apt update -qq
apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    git \
    mosquitto \
    mosquitto-clients \
    build-essential \
    libssl-dev \
    libffi-dev \
    libmysqlclient-dev \
    pkg-config

print_success "Dependências instaladas"

################################################################################
# ETAPA 3: Criar ambiente virtual Python
################################################################################
print_step "ETAPA 3/10: Criando ambiente virtual Python"

cd ${PROJECT_DIR}
sudo -u ${APP_USER} python3 -m venv venv

print_success "Ambiente virtual criado: ${PROJECT_DIR}/venv"

################################################################################
# ETAPA 4: Configurar MySQL
################################################################################
print_step "ETAPA 4/10: Configurando MySQL"

# Verificar se MySQL está rodando
systemctl is-active --quiet mysql || systemctl start mysql

# Criar database e usuário
mysql -u root -p"${MYSQL_ROOT_PASS}" << EOF
-- Remover usuário se existir
DROP USER IF EXISTS '${DB_USER}'@'localhost';

-- Criar database
CREATE DATABASE IF NOT EXISTS ${DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Criar usuário
CREATE USER '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASS}';

-- Conceder permissões
GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';

-- Aplicar mudanças
FLUSH PRIVILEGES;
EOF

print_success "MySQL configurado: Database '${DB_NAME}' e usuário '${DB_USER}' criados"

################################################################################
# ETAPA 5: Configurar Mosquitto MQTT
################################################################################
print_step "ETAPA 5/10: Configurando Mosquitto MQTT"

# Parar serviço se estiver rodando
systemctl stop mosquitto || true

# Backup da config original
if [ -f /etc/mosquitto/mosquitto.conf ] && [ ! -f /etc/mosquitto/mosquitto.conf.backup ]; then
    cp /etc/mosquitto/mosquitto.conf /etc/mosquitto/mosquitto.conf.backup
fi

# Criar configuração principal (sem duplicações)
cat > /etc/mosquitto/mosquitto.conf << 'EOF'
# Place your local configuration in /etc/mosquitto/conf.d/
#
# A full description of the configuration file is at
# /usr/share/doc/mosquitto/examples/mosquitto.conf.example

pid_file /run/mosquitto/mosquitto.pid

persistence true
persistence_location /var/lib/mosquitto/

log_dest file /var/log/mosquitto/mosquitto.log

include_dir /etc/mosquitto/conf.d
EOF

# Criar configuração específica do SmartCEU (sem duplicar valores)
cat > /etc/mosquitto/conf.d/smartceu.conf << EOF
# SmartCEU MQTT Configuration
# Listener na porta customizada
listener ${MQTT_PORT} 0.0.0.0
protocol mqtt

# Permitir conexões anônimas (para desenvolvimento)
allow_anonymous true

# Log types (log_dest já definido no mosquitto.conf)
log_type error
log_type warning
log_type notice
log_type information

# Configurações de conexão
max_connections -1
max_keepalive 3600
EOF

# Ajustar permissões
chown mosquitto:mosquitto /etc/mosquitto/conf.d/smartceu.conf
chmod 644 /etc/mosquitto/conf.d/smartceu.conf

# Garantir que diretórios existem com permissões corretas
mkdir -p /var/log/mosquitto
mkdir -p /var/lib/mosquitto
chown -R mosquitto:mosquitto /var/log/mosquitto
chown -R mosquitto:mosquitto /var/lib/mosquitto
chmod 755 /var/log/mosquitto
chmod 755 /var/lib/mosquitto

# Reiniciar serviço
systemctl daemon-reload
systemctl enable mosquitto
systemctl start mosquitto

# Aguardar MQTT iniciar
sleep 3

# Testar MQTT
if systemctl is-active --quiet mosquitto; then
    print_success "Mosquitto MQTT configurado na porta ${MQTT_PORT}"
else
    print_error "Falha ao iniciar Mosquitto"
    echo "Ver logs: journalctl -xeu mosquitto.service"
    systemctl status mosquitto
    exit 1
fi

################################################################################
# ETAPA 6: Clonar repositório do GitHub
################################################################################
print_step "ETAPA 6/10: Clonando repositório do GitHub"

if [ -d "${PROJECT_DIR}/app/.git" ]; then
    print_warning "Repositório já existe. Atualizando..."
    cd ${PROJECT_DIR}/app
    sudo -u ${APP_USER} git pull origin main
else
    cd ${PROJECT_DIR}
    sudo -u ${APP_USER} git clone ${GIT_REPO} app
fi

print_success "Código clonado: ${PROJECT_DIR}/app"

################################################################################
# ETAPA 7: Instalar dependências Python
################################################################################
print_step "ETAPA 7/10: Instalando dependências Python"

cd ${PROJECT_DIR}

# Upgrade pip
sudo -u ${APP_USER} venv/bin/pip install --upgrade pip setuptools wheel

# Instalar requirements
if [ -f app/requirements.txt ]; then
    sudo -u ${APP_USER} venv/bin/pip install -r app/requirements.txt
fi

if [ -f app/backend/requirements-phase3.txt ]; then
    sudo -u ${APP_USER} venv/bin/pip install -r app/backend/requirements-phase3.txt
fi

# Instalar pacotes adicionais necessários
sudo -u ${APP_USER} venv/bin/pip install \
    gunicorn \
    pymysql \
    cryptography \
    paho-mqtt

print_success "Dependências Python instaladas"

################################################################################
# ETAPA 8: Configurar variáveis de ambiente (.env)
################################################################################
print_step "ETAPA 8/10: Configurando variáveis de ambiente"

# Gerar secrets
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
JWT_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

# Criar arquivo .env
cat > ${PROJECT_DIR}/app/backend/.env << EOF
# SmartCEU - Configuração de Produção
# Gerado automaticamente em: $(date)

# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=${DB_USER}
DB_PASSWORD=${DB_PASS}
DB_NAME=${DB_NAME}

# API Flask
API_HOST=0.0.0.0
API_PORT=${API_PORT}
FLASK_ENV=production
FLASK_DEBUG=0

# MQTT Broker
MQTT_BROKER_HOST=localhost
MQTT_BROKER_PORT=${MQTT_PORT}
MQTT_TOPIC_PREFIX=smartceu

# Security Keys (gerados automaticamente)
SECRET_KEY=${SECRET_KEY}
JWT_SECRET_KEY=${JWT_SECRET_KEY}

# Logging
LOG_LEVEL=INFO
LOG_FILE=${PROJECT_DIR}/logs/app.log

# CORS (ajustar conforme necessário)
CORS_ORIGINS=*
EOF

chown ${APP_USER}:${APP_USER} ${PROJECT_DIR}/app/backend/.env
chmod 600 ${PROJECT_DIR}/app/backend/.env

print_success "Arquivo .env criado e configurado"
print_warning "SECRET_KEY: ${SECRET_KEY:0:16}... (truncado)"
print_warning "JWT_SECRET_KEY: ${JWT_SECRET_KEY:0:16}... (truncado)"

################################################################################
# ETAPA 9: Criar tabelas do banco de dados
################################################################################
print_step "ETAPA 9/10: Criando tabelas do banco de dados"

cd ${PROJECT_DIR}/app/backend

sudo -u ${APP_USER} ${PROJECT_DIR}/venv/bin/python3 << 'PYEOF'
import sys
sys.path.insert(0, '/var/www/smartceu/app/backend')

try:
    from app import create_app, db
    
    app = create_app()
    with app.app_context():
        # Criar todas as tabelas
        db.create_all()
        print("✅ Tabelas criadas com sucesso!")
        
        # Listar tabelas criadas
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"📊 Tabelas criadas: {', '.join(tables)}")
        
except Exception as e:
    print(f"❌ Erro ao criar tabelas: {str(e)}")
    sys.exit(1)
PYEOF

print_success "Banco de dados inicializado"

################################################################################
# ETAPA 10: Configurar NGINX
################################################################################
print_step "ETAPA 10/10: Configurando NGINX"

# Criar configuração do site
cat > /etc/nginx/sites-available/smartceu << 'NGINXCONF'
server {
    listen 80;
    server_name 82.25.75.88;

    # Logs
    access_log /var/log/nginx/smartceu_access.log;
    error_log /var/log/nginx/smartceu_error.log;

    # Frontend estático
    location / {
        root /var/www/smartceu/app/frontend;
        index smart_ceu.html index.html;
        try_files $uri $uri/ =404;
        
        # Cache para assets estáticos
        location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # API Backend
    location /api/ {
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

    # Health check endpoint
    location /health {
        proxy_pass http://127.0.0.1:5001/health;
        access_log off;
    }

    # Assets do frontend
    location /assets/ {
        alias /var/www/smartceu/app/frontend/assets/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Monitoramento de piscina
    location /monitoramento_piscina.html {
        root /var/www/smartceu/app/frontend;
    }

    # Bloquear acesso a arquivos sensíveis
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }

    location ~ /\.env {
        deny all;
    }
}
NGINXCONF

# Habilitar site
ln -sf /etc/nginx/sites-available/smartceu /etc/nginx/sites-enabled/smartceu

# Testar configuração
nginx -t

if [ $? -eq 0 ]; then
    systemctl reload nginx
    print_success "NGINX configurado e recarregado"
else
    print_error "Erro na configuração do NGINX"
    exit 1
fi

################################################################################
# ETAPA 11: Criar serviço systemd para API
################################################################################
print_step "EXTRA 1/3: Criando serviço systemd para API"

cat > /etc/systemd/system/smartceu-api.service << EOF
[Unit]
Description=SmartCEU Flask API
Documentation=https://github.com/RogerioVieira77/PI---IV---V1
After=network.target mysql.service mosquitto.service

[Service]
Type=simple
User=${APP_USER}
Group=${APP_USER}
WorkingDirectory=${PROJECT_DIR}/app/backend
Environment="PATH=${PROJECT_DIR}/venv/bin"
ExecStart=${PROJECT_DIR}/venv/bin/python3 app.py
Restart=always
RestartSec=10

# Logs
StandardOutput=append:${PROJECT_DIR}/logs/api.log
StandardError=append:${PROJECT_DIR}/logs/api_error.log

# Security
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

# Recarregar systemd
systemctl daemon-reload

# Habilitar e iniciar serviço
systemctl enable smartceu-api
systemctl start smartceu-api

# Aguardar serviço iniciar
sleep 3

# Verificar status
if systemctl is-active --quiet smartceu-api; then
    print_success "Serviço smartceu-api iniciado"
else
    print_error "Falha ao iniciar serviço smartceu-api"
    systemctl status smartceu-api
    exit 1
fi

################################################################################
# ETAPA 12: Configurar backup automático
################################################################################
print_step "EXTRA 2/3: Configurando backup automático"

# Criar script de backup
cat > ${PROJECT_DIR}/backup_db.sh << 'BACKUPSCRIPT'
#!/bin/bash
# Backup automático do banco SmartCEU

BACKUP_DIR="/var/www/smartceu/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/smartceu_${DATE}.sql.gz"

# Remover backups com mais de 7 dias
find ${BACKUP_DIR} -name "smartceu_*.sql.gz" -mtime +7 -delete

# Fazer backup
mysqldump -u smartceu_user -p'SmartCEU2025)!' smartceu_db | gzip > ${BACKUP_FILE}

echo "Backup criado: ${BACKUP_FILE}"
BACKUPSCRIPT

chmod +x ${PROJECT_DIR}/backup_db.sh
chown ${APP_USER}:${APP_USER} ${PROJECT_DIR}/backup_db.sh

# Adicionar ao crontab
(crontab -u ${APP_USER} -l 2>/dev/null | grep -v "backup_db.sh"; echo "0 2 * * * ${PROJECT_DIR}/backup_db.sh >> ${PROJECT_DIR}/logs/backup.log 2>&1") | crontab -u ${APP_USER} -

print_success "Backup automático configurado (diário às 2h)"

################################################################################
# ETAPA 13: Testes de validação
################################################################################
print_step "EXTRA 3/3: Executando testes de validação"

echo "1. Testando conectividade MySQL..."
if mysql -u ${DB_USER} -p"${DB_PASS}" -e "USE ${DB_NAME}; SELECT 1;" &>/dev/null; then
    print_success "MySQL: OK"
else
    print_error "MySQL: FALHA"
fi

echo "2. Testando Mosquitto MQTT..."
if timeout 2 mosquitto_sub -h localhost -p ${MQTT_PORT} -t test -C 1 &>/dev/null; then
    print_success "MQTT: OK"
else
    print_warning "MQTT: Timeout (normal se não houver mensagens)"
fi

echo "3. Testando API Flask..."
sleep 2
API_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:${API_PORT}/health || echo "000")
if [ "$API_RESPONSE" = "200" ]; then
    print_success "API Flask: OK (HTTP 200)"
else
    print_warning "API Flask: HTTP $API_RESPONSE (aguarde alguns segundos e teste novamente)"
fi

echo "4. Testando NGINX..."
NGINX_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/health || echo "000")
if [ "$NGINX_RESPONSE" = "200" ]; then
    print_success "NGINX: OK (HTTP 200)"
else
    print_warning "NGINX: HTTP $NGINX_RESPONSE"
fi

################################################################################
# FINALIZAÇÃO
################################################################################
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
MINUTES=$((DURATION / 60))
SECONDS=$((DURATION % 60))

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ DEPLOY CONCLUÍDO COM SUCESSO! ✅${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}📊 Resumo da Instalação:${NC}"
echo "   • Tempo de deploy: ${MINUTES}m ${SECONDS}s"
echo "   • Diretório: ${PROJECT_DIR}"
echo "   • API Port: ${API_PORT}"
echo "   • MQTT Port: ${MQTT_PORT}"
echo "   • Database: ${DB_NAME}"
echo ""
echo -e "${BLUE}🌐 Acessos:${NC}"
echo "   • Frontend: http://82.25.75.88/"
echo "   • Pool Monitor: http://82.25.75.88/monitoramento_piscina.html"
echo "   • API Health: http://82.25.75.88/health"
echo "   • API Docs: http://82.25.75.88/api/docs (se disponível)"
echo ""
echo -e "${BLUE}📝 Comandos Úteis:${NC}"
echo "   • Ver logs API: tail -f ${PROJECT_DIR}/logs/api.log"
echo "   • Status serviço: systemctl status smartceu-api"
echo "   • Reiniciar API: systemctl restart smartceu-api"
echo "   • Logs NGINX: tail -f /var/log/nginx/smartceu_access.log"
echo "   • Backup manual: ${PROJECT_DIR}/backup_db.sh"
echo ""
echo -e "${BLUE}🔐 Credenciais:${NC}"
echo "   • MySQL User: ${DB_USER}"
echo "   • MySQL DB: ${DB_NAME}"
echo "   • MQTT Port: ${MQTT_PORT}"
echo ""
echo -e "${YELLOW}⚠️  Próximos Passos:${NC}"
echo "   1. Testar login no frontend"
echo "   2. Verificar dashboard e monitoramento de piscina"
echo "   3. Testar simuladores de sensores"
echo "   4. Configurar alertas se necessário"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Exibir status dos serviços
echo -e "${BLUE}📌 Status dos Serviços:${NC}"
systemctl status smartceu-api --no-pager -l | head -n 8

exit 0
