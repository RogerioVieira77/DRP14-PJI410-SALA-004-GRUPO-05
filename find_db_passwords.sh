#!/bin/bash
#==============================================================================
# Script para Encontrar Senhas do MySQL
# Descrição: Busca senhas em arquivos de configuração e histórico
# Autor: SmartCEU Team
# Data: 2025-10-22
#==============================================================================

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}  Buscando Credenciais MySQL - SmartCEU                      ${BLUE}║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

#==============================================================================
# 1. Buscar em arquivos Python da aplicação
#==============================================================================

echo -e "${YELLOW}▶ 1. Buscando em arquivos Python...${NC}"

# Backend principal
if [ -f "/var/www/smartceu/app/backend/app.py" ]; then
    echo -e "${CYAN}Verificando app.py:${NC}"
    grep -i "password\|MYSQL_PASSWORD\|DB_PASS" /var/www/smartceu/app/backend/app.py | grep -v "^#" | head -5
fi

# Scripts de população
if [ -f "/var/www/smartceu/app/backend/populate_readings.py" ]; then
    echo -e "${CYAN}Verificando populate_readings.py:${NC}"
    grep -i "password\|MYSQL_PASSWORD\|DB_PASS" /var/www/smartceu/app/backend/populate_readings.py | grep -v "^#" | head -5
fi

if [ -f "/var/www/smartceu/app/backend/create_admin.py" ]; then
    echo -e "${CYAN}Verificando create_admin.py:${NC}"
    grep -i "password\|MYSQL_PASSWORD\|DB_PASS" /var/www/smartceu/app/backend/create_admin.py | grep -v "^#" | head -5
fi

echo ""

#==============================================================================
# 2. Buscar em arquivos de configuração
#==============================================================================

echo -e "${YELLOW}▶ 2. Buscando em arquivos de configuração...${NC}"

# Config.ini
if [ -f "/var/www/smartceu/app/config/config.ini" ]; then
    echo -e "${CYAN}Verificando config.ini:${NC}"
    grep -i "DB_PASS\|password" /var/www/smartceu/app/config/config.ini | grep -v "^#"
fi

# Arquivo .env se existir
if [ -f "/var/www/smartceu/.env" ]; then
    echo -e "${CYAN}Verificando .env:${NC}"
    grep -i "password\|DB_PASS" /var/www/smartceu/.env | grep -v "^#"
fi

# Arquivos de ambiente Python
if [ -f "/var/www/smartceu/venv/bin/activate" ]; then
    echo -e "${CYAN}Verificando venv/bin/activate:${NC}"
    grep -i "password\|DB_PASS" /var/www/smartceu/venv/bin/activate 2>/dev/null | grep -v "^#"
fi

echo ""

#==============================================================================
# 3. Buscar em scripts de deploy
#==============================================================================

echo -e "${YELLOW}▶ 3. Buscando em scripts de deploy...${NC}"

for script in /var/www/smartceu/app/deploy/*.sh; do
    if [ -f "$script" ]; then
        RESULT=$(grep -i "DB_PASS\|DB_PASSWORD\|MYSQL_PASSWORD" "$script" | grep -v "^#" | head -2)
        if [ -n "$RESULT" ]; then
            echo -e "${CYAN}$(basename $script):${NC}"
            echo "$RESULT"
        fi
    fi
done

echo ""

#==============================================================================
# 4. Verificar histórico MySQL root
#==============================================================================

echo -e "${YELLOW}▶ 4. Verificando histórico MySQL...${NC}"

if [ -f "/root/.mysql_history" ]; then
    echo -e "${CYAN}Buscando em .mysql_history:${NC}"
    grep -i "identified by\|password\|create user\|alter user" /root/.mysql_history 2>/dev/null | tail -10
else
    echo -e "${YELLOW}  Arquivo .mysql_history não encontrado${NC}"
fi

echo ""

#==============================================================================
# 5. Verificar arquivos de configuração MySQL
#==============================================================================

echo -e "${YELLOW}▶ 5. Verificando configurações MySQL...${NC}"

# Arquivo de credenciais Debian
if [ -f "/etc/mysql/debian.cnf" ]; then
    echo -e "${CYAN}Credenciais Debian MySQL (/etc/mysql/debian.cnf):${NC}"
    grep "password" /etc/mysql/debian.cnf 2>/dev/null
fi

# Arquivo .my.cnf do root
if [ -f "/root/.my.cnf" ]; then
    echo -e "${CYAN}Arquivo .my.cnf do root:${NC}"
    cat /root/.my.cnf 2>/dev/null
fi

echo ""

#==============================================================================
# 6. Verificar processos MySQL ativos
#==============================================================================

echo -e "${YELLOW}▶ 6. Verificando processos MySQL...${NC}"

ps aux | grep -i mysql | grep -v grep

echo ""

#==============================================================================
# 7. Tentar conexão com usuário da aplicação
#==============================================================================

echo -e "${YELLOW}▶ 7. Testando conexão com credenciais conhecidas...${NC}"

# Credenciais conhecidas da aplicação
APP_USER="smartceu_user"
APP_PASS="SmartCEU2025!Secure"

echo -e "${CYAN}Testando: ${APP_USER} / ${APP_PASS}${NC}"
if mysql -u "$APP_USER" -p"$APP_PASS" -e "SELECT 'OK' AS status;" 2>/dev/null; then
    echo -e "${GREEN}✓ Conexão OK com usuário da aplicação${NC}"
    
    # Verificar privilégios
    echo -e "${CYAN}Privilégios do usuário:${NC}"
    mysql -u "$APP_USER" -p"$APP_PASS" -e "SHOW GRANTS FOR CURRENT_USER();" 2>/dev/null
    
    # Tentar ver outros usuários (se tiver permissão)
    echo -e "${CYAN}Tentando listar usuários MySQL:${NC}"
    mysql -u "$APP_USER" -p"$APP_PASS" -e "SELECT User, Host, plugin FROM mysql.user;" 2>/dev/null
else
    echo -e "${RED}✗ Falha na conexão${NC}"
fi

echo ""

#==============================================================================
# 8. Buscar em logs
#==============================================================================

echo -e "${YELLOW}▶ 8. Verificando logs recentes...${NC}"

if [ -f "/var/log/mysql/error.log" ]; then
    echo -e "${CYAN}Últimas linhas do log de erro MySQL:${NC}"
    tail -20 /var/log/mysql/error.log 2>/dev/null | grep -i "password\|access denied"
fi

echo ""

#==============================================================================
# RESUMO
#==============================================================================

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}  RESUMO - CREDENCIAIS ENCONTRADAS                           ${BLUE}║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${GREEN}Credenciais da Aplicação (confirmadas):${NC}"
echo -e "  Usuário: ${CYAN}smartceu_user${NC}"
echo -e "  Senha:   ${CYAN}SmartCEU2025!Secure${NC}"
echo -e "  Banco:   ${CYAN}smartceu_db${NC}"
echo ""

echo -e "${YELLOW}Para descobrir a senha root do MySQL:${NC}"
echo -e "  1. Verifique os resultados acima"
echo -e "  2. Tente usar credenciais do debian.cnf"
echo -e "  3. Se necessário, reset via --skip-grant-tables"
echo ""

echo -e "${CYAN}Comandos úteis:${NC}"
echo -e "  # Tentar com debian-sys-maint:"
echo -e "  ${GREEN}mysql --defaults-file=/etc/mysql/debian.cnf${NC}"
echo ""
echo -e "  # Ver plugin de autenticação do root:"
echo -e "  ${GREEN}sudo mysql -u smartceu_user -p'SmartCEU2025!Secure' -e \"SELECT User, Host, plugin FROM mysql.user WHERE User='root';\"${NC}"
echo ""

exit 0
