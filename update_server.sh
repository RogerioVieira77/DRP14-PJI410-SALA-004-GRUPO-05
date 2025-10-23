#!/bin/bash
#==============================================================================
# Script de Atualização do Servidor SmartCEU
# Descrição: Atualiza código do GitHub e reinicia todos os serviços
# Autor: SmartCEU Team
# Data: 2025-10-22
#==============================================================================

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variáveis
APP_DIR="/var/www/smartceu"
LOG_FILE="/var/log/smartceu_update.log"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Contadores de status
SUCCESS_COUNT=0
ERROR_COUNT=0
SERVICES_RESTARTED=0

# Array para armazenar resultados
declare -a RESULTS

#==============================================================================
# Funções auxiliares
#==============================================================================

log_message() {
    echo "[${TIMESTAMP}] $1" | tee -a "$LOG_FILE"
}

print_header() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
}

print_step() {
    echo -e "${YELLOW}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
    RESULTS+=("${GREEN}✓${NC} $1")
    ((SUCCESS_COUNT++))
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
    RESULTS+=("${RED}✗${NC} $1")
    ((ERROR_COUNT++))
}

check_command() {
    if [ $? -eq 0 ]; then
        print_success "$1"
        return 0
    else
        print_error "$1"
        return 1
    fi
}

#==============================================================================
# Início do Script
#==============================================================================

clear
print_header "ATUALIZAÇÃO DO SERVIDOR SMARTCEU"

log_message "Iniciando atualização do servidor SmartCEU"

#==============================================================================
# 1. Backup antes da atualização
#==============================================================================

print_step "1. Criando backup de segurança..."

# Backup do código
if [ -d "$APP_DIR" ]; then
    BACKUP_DIR="/var/backups/smartceu_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    cp -r "$APP_DIR" "$BACKUP_DIR/" 2>/dev/null
    check_command "Backup do código criado em: $BACKUP_DIR"
else
    print_error "Diretório da aplicação não encontrado: $APP_DIR"
    exit 1
fi

# Backup do banco de dados
cd "$APP_DIR" && bash backup_db.sh >/dev/null 2>&1
check_command "Backup do banco de dados MySQL criado"

#==============================================================================
# 2. Atualização do código via GitHub
#==============================================================================

print_step "2. Atualizando código do GitHub..."

cd "$APP_DIR" || exit 1

# Verificar branch atual
CURRENT_BRANCH=$(git branch --show-current)
log_message "Branch atual: $CURRENT_BRANCH"

# Descartar alterações locais
git reset --hard HEAD >/dev/null 2>&1
check_command "Alterações locais descartadas"

# Fazer pull do GitHub
git pull origin main 2>&1 | tee -a "$LOG_FILE"
check_command "Código atualizado do GitHub (branch: main)"

# Verificar se há novos arquivos
NEW_FILES=$(git diff --name-only HEAD@{1} HEAD 2>/dev/null | wc -l)
log_message "Arquivos atualizados: $NEW_FILES"

#==============================================================================
# 3. Atualizar dependências Python (se necessário)
#==============================================================================

print_step "3. Verificando dependências Python..."

if [ -f "$APP_DIR/app/backend/requirements-phase3.txt" ]; then
    VENV_DIR="$APP_DIR/venv"
    if [ -d "$VENV_DIR" ]; then
        source "$VENV_DIR/bin/activate"
        pip install -q -r "$APP_DIR/app/backend/requirements-phase3.txt" 2>&1 | tee -a "$LOG_FILE"
        check_command "Dependências Python atualizadas"
        deactivate
    else
        print_error "Ambiente virtual não encontrado"
    fi
else
    print_success "Arquivo de requirements não encontrado (pulando)"
fi

#==============================================================================
# 4. Ajustar permissões (Modo Seguro)
#==============================================================================

print_step "4. Ajustando permissões dos arquivos..."

# 1. Proprietário (necessário para Nginx/Flask acessar os arquivos)
chown -R www-data:www-data "$APP_DIR" 2>/dev/null
check_command "Proprietário ajustado para www-data"

# 2. Permissões de diretórios (755 - permite navegação)
find "$APP_DIR" -type d -exec chmod 755 {} \; 2>/dev/null
check_command "Permissões de diretórios ajustadas (755)"

# 3. Permissões de arquivos regulares (644 - leitura apenas)
find "$APP_DIR" -type f -exec chmod 644 {} \; 2>/dev/null
check_command "Permissões de arquivos ajustadas (644)"

# 4. Tornar scripts executáveis (somente .sh)
find "$APP_DIR" -type f -name "*.sh" -exec chmod 755 {} \; 2>/dev/null
check_command "Scripts shell tornados executáveis (755)"

# 5. Proteger arquivos sensíveis (640 - apenas owner e group)
find "$APP_DIR" -type f \( -name ".env" -o -name "*.ini" -o -name "*.conf" \) -exec chmod 640 {} \; 2>/dev/null
check_command "Arquivos de configuração protegidos (640)"

#==============================================================================
# 5. Reiniciar serviços
#==============================================================================

print_step "5. Reiniciando serviços da aplicação..."

# MySQL
systemctl restart mysql 2>/dev/null
if check_command "MySQL reiniciado"; then
    ((SERVICES_RESTARTED++))
fi

# Verificar se MySQL está rodando
sleep 2
systemctl is-active --quiet mysql
check_command "MySQL está ativo"

# Flask/Gunicorn (serviço SmartCEU)
if systemctl list-units --full -all | grep -q smartceu.service; then
    # Flask rodando como serviço systemd
    systemctl restart smartceu.service 2>/dev/null
    if check_command "SmartCEU (Flask/Gunicorn) reiniciado via systemd"; then
        ((SERVICES_RESTARTED++))
    fi
    
    sleep 2
    systemctl is-active --quiet smartceu.service
    check_command "SmartCEU está ativo"
else
    # Flask rodando como processo (não é serviço)
    FLASK_PID=$(ps aux | grep 'python.*app.py' | grep '/var/www/smartceu' | grep -v grep | awk '{print $2}' | head -1)
    
    if [ -n "$FLASK_PID" ]; then
        # Matar processo Flask existente
        pkill -f '/var/www/smartceu.*app.py' 2>/dev/null
        sleep 2
        
        # Reiniciar Flask
        cd /var/www/smartceu/app/backend
        nohup /var/www/smartceu/venv/bin/python3 app.py > /var/log/smartceu_flask.log 2>&1 &
        sleep 3
        
        # Verificar se iniciou
        NEW_PID=$(ps aux | grep 'python.*app.py' | grep '/var/www/smartceu' | grep -v grep | awk '{print $2}' | head -1)
        if [ -n "$NEW_PID" ]; then
            if check_command "SmartCEU (Flask) reiniciado como processo (PID: $NEW_PID)"; then
                ((SERVICES_RESTARTED++))
            fi
        else
            print_error "Falha ao reiniciar SmartCEU (Flask)"
        fi
    else
        print_error "SmartCEU (Flask) não está rodando e não é um serviço systemd"
    fi
fi

# Nginx
systemctl restart nginx 2>/dev/null
if check_command "Nginx reiniciado"; then
    ((SERVICES_RESTARTED++))
fi

sleep 2
systemctl is-active --quiet nginx
check_command "Nginx está ativo"

# Mosquitto (MQTT Broker)
if systemctl list-units --full -all | grep -q mosquitto; then
    systemctl restart mosquitto 2>/dev/null
    if check_command "Mosquitto (MQTT) reiniciado"; then
        ((SERVICES_RESTARTED++))
    fi
    
    sleep 2
    systemctl is-active --quiet mosquitto
    check_command "Mosquitto está ativo"
else
    print_success "Mosquitto não configurado (pulando)"
fi

#==============================================================================
# 6. Verificação de saúde da aplicação
#==============================================================================

print_step "6. Verificando saúde da aplicação..."

# Testar endpoint de health
sleep 3
HEALTH_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health 2>/dev/null)
if [ "$HEALTH_RESPONSE" = "200" ]; then
    check_command "API Health check OK (HTTP 200)"
else
    print_error "API Health check falhou (HTTP $HEALTH_RESPONSE)"
fi

# Verificar se Nginx está respondendo
NGINX_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/smartceu 2>/dev/null)
if [ "$NGINX_RESPONSE" = "200" ]; then
    check_command "Nginx respondendo OK (HTTP 200)"
else
    print_error "Nginx não está respondendo corretamente (HTTP $NGINX_RESPONSE)"
fi

#==============================================================================
# 7. Limpeza
#==============================================================================

print_step "7. Limpeza de arquivos temporários..."

# Limpar cache Python
find "$APP_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
check_command "Cache Python limpo"

# Limpar logs antigos (manter últimos 7 dias)
find /var/log/nginx/ -name "*.log.*" -mtime +7 -delete 2>/dev/null
check_command "Logs antigos removidos"

#==============================================================================
# RESUMO FINAL
#==============================================================================

print_header "RESUMO DA ATUALIZAÇÃO"

echo -e "${BLUE}┌─────────────────────────────────────────────────────────────┐${NC}"
echo -e "${BLUE}│${NC}  Data/Hora: ${TIMESTAMP}                               ${BLUE}│${NC}"
echo -e "${BLUE}│${NC}  Diretório: ${APP_DIR}                    ${BLUE}│${NC}"
echo -e "${BLUE}│${NC}  Branch: ${CURRENT_BRANCH}                                          ${BLUE}│${NC}"
echo -e "${BLUE}│${NC}  Arquivos atualizados: ${NEW_FILES}                                ${BLUE}│${NC}"
echo -e "${BLUE}└─────────────────────────────────────────────────────────────┘${NC}"
echo ""

echo -e "${BLUE}Status dos Serviços:${NC}"
echo -e "  ${GREEN}✓${NC} MySQL:      $(systemctl is-active mysql)"
echo -e "  ${GREEN}✓${NC} SmartCEU:   $(systemctl is-active smartceu.service 2>/dev/null || echo 'N/A')"
echo -e "  ${GREEN}✓${NC} Nginx:      $(systemctl is-active nginx)"
echo -e "  ${GREEN}✓${NC} Mosquitto:  $(systemctl is-active mosquitto 2>/dev/null || echo 'N/A')"
echo ""

echo -e "${BLUE}Resumo de Operações:${NC}"
for result in "${RESULTS[@]}"; do
    echo "  $result"
done
echo ""

echo -e "${BLUE}┌─────────────────────────────────────────────────────────────┐${NC}"
if [ $ERROR_COUNT -eq 0 ]; then
    echo -e "${BLUE}│${NC}  ${GREEN}STATUS: ATUALIZAÇÃO CONCLUÍDA COM SUCESSO! ✓${NC}           ${BLUE}│${NC}"
else
    echo -e "${BLUE}│${NC}  ${YELLOW}STATUS: ATUALIZAÇÃO CONCLUÍDA COM AVISOS${NC}               ${BLUE}│${NC}"
fi
echo -e "${BLUE}│${NC}                                                             ${BLUE}│${NC}"
echo -e "${BLUE}│${NC}  ✓ Operações bem-sucedidas: ${GREEN}${SUCCESS_COUNT}${NC}                       ${BLUE}│${NC}"
echo -e "${BLUE}│${NC}  ✗ Operações com erro: ${RED}${ERROR_COUNT}${NC}                            ${BLUE}│${NC}"
echo -e "${BLUE}│${NC}  ⟳ Serviços reiniciados: ${YELLOW}${SERVICES_RESTARTED}${NC}                         ${BLUE}│${NC}"
echo -e "${BLUE}└─────────────────────────────────────────────────────────────┘${NC}"
echo ""

echo -e "${BLUE}URLs de Acesso:${NC}"
echo -e "  • Dashboard:  ${GREEN}http://82.25.75.88/smartceu${NC}"
echo -e "  • Pool:       ${GREEN}http://82.25.75.88/smartceu/pool${NC}"
echo -e "  • Test Page:  ${GREEN}http://82.25.75.88/smartceu/test_page.html${NC}"
echo -e "  • API Docs:   ${GREEN}http://82.25.75.88/smartceu/doc_arq.html${NC}"
echo -e "  • API Health: ${GREEN}http://82.25.75.88/health${NC}"
echo ""

echo -e "${BLUE}Log completo salvo em:${NC} ${LOG_FILE}"
echo ""

log_message "Atualização concluída. Sucesso: $SUCCESS_COUNT | Erros: $ERROR_COUNT"

# Retornar código de saída apropriado final
if [ $ERROR_COUNT -gt 0 ]; then
    exit 1
else
    exit 0
fi
