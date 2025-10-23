#!/bin/bash
#==============================================================================
# Script de Criação do Banco de Relatórios SmartCEU
# Descrição: Cria uma réplica do banco de dados para relatórios
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
DB_USER="smartceu_user"
DB_PASS="SmartCEU2025!Secure"
DB_SOURCE="smartceu_db"
DB_REPORT="smartceu_report_db"
BACKUP_DIR="/var/www/smartceu/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}  Criação do Banco de Dados de Relatórios - SmartCEU         ${BLUE}║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

#==============================================================================
# 1. Verificar se o banco de origem existe
#==============================================================================

echo -e "${YELLOW}▶ 1. Verificando banco de dados de origem...${NC}"

DB_EXISTS=$(mysql -u "$DB_USER" -p"$DB_PASS" -e "SHOW DATABASES LIKE '$DB_SOURCE';" | grep "$DB_SOURCE")

if [ -z "$DB_EXISTS" ]; then
    echo -e "${RED}✗ Banco de dados de origem '$DB_SOURCE' não encontrado!${NC}"
    exit 1
else
    echo -e "${GREEN}✓ Banco de dados '$DB_SOURCE' encontrado${NC}"
fi

#==============================================================================
# 2. Verificar se o banco de relatórios já existe
#==============================================================================

echo -e "${YELLOW}▶ 2. Verificando banco de dados de relatórios...${NC}"

REPORT_EXISTS=$(mysql -u "$DB_USER" -p"$DB_PASS" -e "SHOW DATABASES LIKE '$DB_REPORT';" | grep "$DB_REPORT")

if [ -n "$REPORT_EXISTS" ]; then
    echo -e "${YELLOW}⚠ Banco de dados '$DB_REPORT' já existe!${NC}"
    echo -e "${YELLOW}   Deseja recriar? (S/N)${NC}"
    read -r RECREATE
    
    if [[ "$RECREATE" =~ ^[Ss]$ ]]; then
        echo -e "${YELLOW}▶ Fazendo backup antes de recriar...${NC}"
        mkdir -p "$BACKUP_DIR"
        mysqldump -u "$DB_USER" -p"$DB_PASS" --no-tablespaces "$DB_REPORT" | gzip > "$BACKUP_DIR/${DB_REPORT}_backup_${TIMESTAMP}.sql.gz"
        echo -e "${GREEN}✓ Backup criado: ${DB_REPORT}_backup_${TIMESTAMP}.sql.gz${NC}"
        
        echo -e "${YELLOW}▶ Removendo banco existente...${NC}"
        mysql -u "$DB_USER" -p"$DB_PASS" -e "DROP DATABASE $DB_REPORT;"
        echo -e "${GREEN}✓ Banco '$DB_REPORT' removido${NC}"
    else
        echo -e "${YELLOW}✓ Mantendo banco existente${NC}"
        exit 0
    fi
fi

#==============================================================================
# 3. Criar banco de dados de relatórios
#==============================================================================

echo -e "${YELLOW}▶ 3. Criando banco de dados de relatórios...${NC}"

mysql -u "$DB_USER" -p"$DB_PASS" -e "CREATE DATABASE $DB_REPORT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Banco '$DB_REPORT' criado com sucesso${NC}"
else
    echo -e "${RED}✗ Erro ao criar banco de dados${NC}"
    exit 1
fi

#==============================================================================
# 4. Copiar estrutura e dados do banco de origem
#==============================================================================

echo -e "${YELLOW}▶ 4. Copiando estrutura e dados...${NC}"

# Criar arquivo temporário com dump
TEMP_DUMP="/tmp/smartceu_temp_dump_${TIMESTAMP}.sql"

mysqldump -u "$DB_USER" -p"$DB_PASS" --no-tablespaces "$DB_SOURCE" > "$TEMP_DUMP"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Estrutura e dados exportados${NC}"
    
    # Importar para banco de relatórios
    mysql -u "$DB_USER" -p"$DB_PASS" "$DB_REPORT" < "$TEMP_DUMP"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Dados importados para '$DB_REPORT'${NC}"
    else
        echo -e "${RED}✗ Erro ao importar dados${NC}"
        rm -f "$TEMP_DUMP"
        exit 1
    fi
    
    # Limpar arquivo temporário
    rm -f "$TEMP_DUMP"
else
    echo -e "${RED}✗ Erro ao exportar dados${NC}"
    exit 1
fi

#==============================================================================
# 5. Verificar tabelas criadas
#==============================================================================

echo -e "${YELLOW}▶ 5. Verificando tabelas criadas...${NC}"

TABLE_COUNT=$(mysql -u "$DB_USER" -p"$DB_PASS" -e "USE $DB_REPORT; SHOW TABLES;" | wc -l)
TABLE_COUNT=$((TABLE_COUNT - 1)) # Remover linha de cabeçalho

echo -e "${GREEN}✓ Total de tabelas criadas: $TABLE_COUNT${NC}"

# Listar tabelas
echo -e "${BLUE}Tabelas no banco '$DB_REPORT':${NC}"
mysql -u "$DB_USER" -p"$DB_PASS" -e "USE $DB_REPORT; SHOW TABLES;"

#==============================================================================
# 6. Verificar registros
#==============================================================================

echo -e "${YELLOW}▶ 6. Verificando registros...${NC}"

# Contar registros nas principais tabelas
echo -e "${BLUE}Contagem de registros:${NC}"

for table in users sensors sensor_readings pool_readings alerts statistics; do
    COUNT=$(mysql -u "$DB_USER" -p"$DB_PASS" -e "USE $DB_REPORT; SELECT COUNT(*) FROM $table;" 2>/dev/null | tail -1)
    if [ -n "$COUNT" ]; then
        echo -e "  • ${table}: ${GREEN}${COUNT}${NC} registros"
    fi
done

#==============================================================================
# RESUMO FINAL
#==============================================================================

echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}  ${GREEN}Banco de Dados de Relatórios Criado com Sucesso!${NC}         ${BLUE}║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${BLUE}Informações do Banco:${NC}"
echo -e "  • Nome: ${GREEN}${DB_REPORT}${NC}"
echo -e "  • Origem: ${GREEN}${DB_SOURCE}${NC}"
echo -e "  • Tabelas: ${GREEN}${TABLE_COUNT}${NC}"
echo -e "  • Charset: ${GREEN}utf8mb4${NC}"
echo -e "  • Collation: ${GREEN}utf8mb4_unicode_ci${NC}"
echo ""

echo -e "${BLUE}Próximos Passos:${NC}"
echo -e "  1. Configure a replicação automática com: ${GREEN}bash setup_replication.sh${NC}"
echo -e "  2. Execute sincronização manual com: ${GREEN}bash sync_report_db.sh${NC}"
echo -e "  3. Configure cron para sincronização diária"
echo ""

echo -e "${YELLOW}⚠ Importante:${NC}"
echo -e "  • Este banco é SOMENTE LEITURA para relatórios"
echo -e "  • Não faça alterações diretas neste banco"
echo -e "  • Use sempre o banco '${DB_SOURCE}' para gravações"
echo ""
