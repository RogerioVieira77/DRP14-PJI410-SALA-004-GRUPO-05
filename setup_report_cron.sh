#!/bin/bash
#==============================================================================
# Script de Configuração do Cron para Sincronização de Relatórios
# Descrição: Configura execução automática diária da sincronização
# Autor: SmartCEU Team
# Data: 2025-10-22
#==============================================================================

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configurações
SCRIPT_PATH="/var/www/smartceu/sync_report_db.sh"
CRON_TIME="0 3 * * *"  # 3:00 AM todos os dias
LOG_FILE="/var/log/smartceu_report_sync.log"

print_header() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_header "CONFIGURAÇÃO DO CRON - SINCRONIZAÇÃO DE RELATÓRIOS"

#==============================================================================
# 1. Verificar se o script existe
#==============================================================================

echo -e "${YELLOW}▶ 1. Verificando arquivos...${NC}"

if [ ! -f "$SCRIPT_PATH" ]; then
    print_error "Script não encontrado: $SCRIPT_PATH"
    echo -e "${YELLOW}Execute: cp sync_report_db.sh /var/www/smartceu/${NC}"
    exit 1
fi
print_success "Script encontrado"

# Verificar permissão de execução
if [ ! -x "$SCRIPT_PATH" ]; then
    echo -e "${YELLOW}   Concedendo permissão de execução...${NC}"
    chmod +x "$SCRIPT_PATH"
    print_success "Permissão de execução concedida"
fi

#==============================================================================
# 2. Criar arquivo de log se não existir
#==============================================================================

echo -e "${YELLOW}▶ 2. Configurando arquivo de log...${NC}"

if [ ! -f "$LOG_FILE" ]; then
    touch "$LOG_FILE"
    chown www-data:www-data "$LOG_FILE"
    chmod 664 "$LOG_FILE"
    print_success "Arquivo de log criado"
else
    print_success "Arquivo de log já existe"
fi

#==============================================================================
# 3. Configurar cron job
#==============================================================================

echo -e "${YELLOW}▶ 3. Configurando cron job...${NC}"

# Linha do cron job
CRON_JOB="$CRON_TIME bash $SCRIPT_PATH >> $LOG_FILE 2>&1"

# Verificar se já existe
EXISTING_CRON=$(crontab -l 2>/dev/null | grep -F "$SCRIPT_PATH")

if [ -n "$EXISTING_CRON" ]; then
    print_warning "Cron job já existe:"
    echo -e "   ${YELLOW}${EXISTING_CRON}${NC}"
    echo ""
    echo -e "${YELLOW}Deseja substituir? (s/N):${NC} "
    read -r REPLACE
    
    if [[ ! "$REPLACE" =~ ^[sS]$ ]]; then
        echo -e "${BLUE}Operação cancelada${NC}"
        exit 0
    fi
    
    # Remover cron job existente
    crontab -l 2>/dev/null | grep -vF "$SCRIPT_PATH" | crontab -
    print_success "Cron job antigo removido"
fi

# Adicionar novo cron job
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

if [ $? -eq 0 ]; then
    print_success "Cron job configurado com sucesso"
else
    print_error "Falha ao configurar cron job"
    exit 1
fi

#==============================================================================
# 4. Verificar configuração
#==============================================================================

echo -e "${YELLOW}▶ 4. Verificando configuração...${NC}"

echo -e "${BLUE}Cron jobs ativos:${NC}"
crontab -l | grep -F "$SCRIPT_PATH" | while read -r line; do
    echo -e "   ${GREEN}${line}${NC}"
done

#==============================================================================
# 5. Informações sobre horário
#==============================================================================

echo -e "${YELLOW}▶ 5. Informações sobre execução...${NC}"

echo -e "${BLUE}Configuração atual:${NC}"
echo -e "   • Horário: ${GREEN}03:00 AM${NC} (todos os dias)"
echo -e "   • Script: ${GREEN}${SCRIPT_PATH}${NC}"
echo -e "   • Log: ${GREEN}${LOG_FILE}${NC}"
echo ""

# Calcular próxima execução
CURRENT_HOUR=$(date +%H)
if [ "$CURRENT_HOUR" -lt 3 ]; then
    NEXT_RUN="hoje às 03:00"
else
    NEXT_RUN="amanhã às 03:00"
fi
echo -e "   ${BLUE}Próxima execução: ${GREEN}${NEXT_RUN}${NC}"

#==============================================================================
# RESUMO FINAL
#==============================================================================

echo ""
print_header "CONFIGURAÇÃO CONCLUÍDA"

echo -e "${BLUE}Comandos úteis:${NC}"
echo -e "   • Ver log em tempo real:"
echo -e "     ${GREEN}tail -f $LOG_FILE${NC}"
echo ""
echo -e "   • Testar sincronização manualmente:"
echo -e "     ${GREEN}bash $SCRIPT_PATH${NC}"
echo ""
echo -e "   • Verificar cron jobs:"
echo -e "     ${GREEN}crontab -l${NC}"
echo ""
echo -e "   • Editar cron jobs:"
echo -e "     ${GREEN}crontab -e${NC}"
echo ""
echo -e "   • Remover sincronização automática:"
echo -e "     ${GREEN}crontab -l | grep -v sync_report_db.sh | crontab -${NC}"
echo ""

echo -e "${GREEN}✓ Sincronização automática configurada com sucesso!${NC}"
echo ""

exit 0
