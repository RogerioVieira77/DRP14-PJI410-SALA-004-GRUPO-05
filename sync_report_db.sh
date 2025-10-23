#!/bin/bash
#==============================================================================
# Script de Sincronização do Banco de Relatórios SmartCEU
# Descrição: Sincroniza dados do banco principal para o banco de relatórios
# Autor: SmartCEU Team
# Data: 2025-10-22
# Uso: Executar diariamente via cron
#==============================================================================

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configurações - Banco de Origem
DB_USER="smartceu_user"
DB_PASS="SmartCEU2025)!"
DB_SOURCE="smartceu_db"

# Configurações - Banco de Relatórios
DB_REPORT="smartceu_report_db"
DB_ROOT_USER="root"
DB_ROOT_PASS="SmartCEU2025)!"

BACKUP_DIR="/var/www/smartceu/backups/report_sync"
LOG_FILE="/var/log/smartceu_report_sync.log"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
TIMESTAMP_FILE=$(date +"%Y%m%d_%H%M%S")

# Criar diretórios se não existirem
mkdir -p "$BACKUP_DIR"

#==============================================================================
# Funções auxiliares
#==============================================================================

log_message() {
    echo "[${TIMESTAMP}] $1" | tee -a "$LOG_FILE"
}

print_header() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
    log_message "SUCCESS: $1"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
    log_message "ERROR: $1"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
    log_message "WARNING: $1"
}

#==============================================================================
# Início da Sincronização
#==============================================================================

print_header "SINCRONIZAÇÃO DO BANCO DE RELATÓRIOS"
log_message "Iniciando sincronização: $DB_SOURCE → $DB_REPORT"

#==============================================================================
# 1. Verificar bancos de dados
#==============================================================================

echo -e "${YELLOW}▶ 1. Verificando bancos de dados...${NC}"

# Verificar banco de origem
SOURCE_EXISTS=$(mysql -u "$DB_USER" -p"$DB_PASS" -e "SHOW DATABASES LIKE '$DB_SOURCE';" 2>/dev/null | grep "$DB_SOURCE")
if [ -z "$SOURCE_EXISTS" ]; then
    print_error "Banco de origem '$DB_SOURCE' não encontrado"
    exit 1
fi
print_success "Banco de origem verificado"

# Verificar banco de relatórios
REPORT_EXISTS=$(mysql -u "$DB_USER" -p"$DB_PASS" -e "SHOW DATABASES LIKE '$DB_REPORT';" 2>/dev/null | grep "$DB_REPORT")
if [ -z "$REPORT_EXISTS" ]; then
    print_error "Banco de relatórios '$DB_REPORT' não encontrado"
    echo -e "${YELLOW}Execute primeiro: bash create_report_db.sh${NC}"
    exit 1
fi
print_success "Banco de relatórios verificado"

#==============================================================================
# 2. Backup do banco de relatórios antes da sincronização
#==============================================================================

echo -e "${YELLOW}▶ 2. Criando backup de segurança...${NC}"

BACKUP_FILE="${BACKUP_DIR}/${DB_REPORT}_presync_${TIMESTAMP_FILE}.sql.gz"
mysqldump -u "$DB_ROOT_USER" -p"$DB_ROOT_PASS" --no-tablespaces "$DB_REPORT" 2>/dev/null | gzip > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    print_success "Backup criado: ${BACKUP_SIZE} - ${BACKUP_FILE##*/}"
else
    print_error "Falha ao criar backup"
    exit 1
fi

#==============================================================================
# 3. Obter estatísticas antes da sincronização
#==============================================================================

echo -e "${YELLOW}▶ 3. Coletando estatísticas...${NC}"

# Função para contar registros
count_records() {
    local db=$1
    local table=$2
    mysql -u "$DB_ROOT_USER" -p"$DB_ROOT_PASS" -e "USE $db; SELECT COUNT(*) FROM $table;" 2>/dev/null | tail -1
}

# Tabelas para sincronizar
TABLES=(users sensors sensor_readings pool_readings alerts statistics)

echo -e "${BLUE}Registros ANTES da sincronização:${NC}"
declare -A BEFORE_COUNTS
for table in "${TABLES[@]}"; do
    COUNT=$(count_records "$DB_REPORT" "$table")
    BEFORE_COUNTS[$table]=$COUNT
    echo -e "  • ${table}: ${COUNT} registros"
done

#==============================================================================
# 4. Sincronização (Estratégia: Drop & Import)
#==============================================================================

echo -e "${YELLOW}▶ 4. Sincronizando dados...${NC}"

# Criar dump temporário do banco de origem
TEMP_DUMP="/tmp/smartceu_sync_${TIMESTAMP_FILE}.sql"
echo -e "${YELLOW}   Exportando dados do banco principal...${NC}"

mysqldump -u "$DB_USER" -p"$DB_PASS" --no-tablespaces "$DB_SOURCE" > "$TEMP_DUMP" 2>/dev/null

if [ $? -eq 0 ]; then
    DUMP_SIZE=$(du -h "$TEMP_DUMP" | cut -f1)
    print_success "Dados exportados (${DUMP_SIZE})"
else
    print_error "Falha ao exportar dados"
    rm -f "$TEMP_DUMP"
    exit 1
fi

# Remover banco de relatórios
echo -e "${YELLOW}   Removendo banco de relatórios antigo...${NC}"
mysql -u "$DB_ROOT_USER" -p"$DB_ROOT_PASS" -e "DROP DATABASE IF EXISTS $DB_REPORT;" 2>/dev/null
print_success "Banco antigo removido"

# Recriar banco
echo -e "${YELLOW}   Recriando banco de relatórios...${NC}"
mysql -u "$DB_ROOT_USER" -p"$DB_ROOT_PASS" -e "CREATE DATABASE $DB_REPORT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>/dev/null
print_success "Banco recriado"

# Importar dados
echo -e "${YELLOW}   Importando dados atualizados...${NC}"
mysql -u "$DB_ROOT_USER" -p"$DB_ROOT_PASS" "$DB_REPORT" < "$TEMP_DUMP" 2>/dev/null

if [ $? -eq 0 ]; then
    print_success "Dados importados com sucesso"
else
    print_error "Falha ao importar dados"
    rm -f "$TEMP_DUMP"
    exit 1
fi

# Limpar arquivo temporário
rm -f "$TEMP_DUMP"

#==============================================================================
# 5. Verificar sincronização
#==============================================================================

echo -e "${YELLOW}▶ 5. Verificando sincronização...${NC}"

echo -e "${BLUE}Registros DEPOIS da sincronização:${NC}"
SYNC_SUCCESS=true
for table in "${TABLES[@]}"; do
    BEFORE=${BEFORE_COUNTS[$table]}
    AFTER=$(count_records "$DB_REPORT" "$table")
    DIFF=$((AFTER - BEFORE))
    
    if [ $DIFF -ge 0 ]; then
        echo -e "  • ${table}: ${GREEN}${AFTER}${NC} registros (${GREEN}+${DIFF}${NC})"
    else
        echo -e "  • ${table}: ${YELLOW}${AFTER}${NC} registros (${RED}${DIFF}${NC})"
        print_warning "Tabela '$table' tem menos registros após sincronização"
    fi
done

#==============================================================================
# 6. Otimizar banco de dados
#==============================================================================

echo -e "${YELLOW}▶ 6. Otimizando banco de relatórios...${NC}"

for table in "${TABLES[@]}"; do
    mysql -u "$DB_USER" -p"$DB_PASS" -e "USE $DB_REPORT; OPTIMIZE TABLE $table;" 2>/dev/null >/dev/null
done
print_success "Otimização concluída"

#==============================================================================
# 7. Limpar backups antigos (manter últimos 7 dias)
#==============================================================================

echo -e "${YELLOW}▶ 7. Limpando backups antigos...${NC}"

DELETED=$(find "$BACKUP_DIR" -name "*.sql.gz" -mtime +7 -delete -print | wc -l)
print_success "Backups antigos removidos: $DELETED arquivos"

#==============================================================================
# RESUMO FINAL
#==============================================================================

echo ""
print_header "RESUMO DA SINCRONIZAÇÃO"

echo -e "${BLUE}Informações:${NC}"
echo -e "  • Data/Hora: ${TIMESTAMP}"
echo -e "  • Origem: ${GREEN}${DB_SOURCE}${NC}"
echo -e "  • Destino: ${GREEN}${DB_REPORT}${NC}"
echo -e "  • Backup: ${GREEN}${BACKUP_FILE##*/}${NC}"
echo ""

echo -e "${BLUE}Status: ${GREEN}✓ SINCRONIZAÇÃO CONCLUÍDA COM SUCESSO${NC}"
echo ""

log_message "Sincronização concluída com sucesso"

exit 0
