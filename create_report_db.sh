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

# Configurações - Banco de Origem
DB_USER="smartceu_user"
DB_PASS="SmartCEU2025)!"
DB_SOURCE="smartceu_db"

# Configurações - Banco de Relatórios
DB_REPORT="smartceu_report_db"
DB_REPORT_USER="smart_ceu_report"
DB_REPORT_PASS="SmartCEUrep@)@%1"
DB_ROOT_USER="root"
DB_ROOT_PASS="SmartCEUrep@)@%1"

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

# Garantir que a senha root do MySQL esteja definida para o valor desejado.
# Tentamos primeiro via socket (sudo mysql) — funciona em instalações padrão Ubuntu/MySQL.
echo -e "${YELLOW}▶ Ajustando senha do usuário root do MySQL para uso do script...${NC}"
if sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '${DB_ROOT_PASS}'; FLUSH PRIVILEGES;" 2>/dev/null; then
    echo -e "${GREEN}✓ Senha root atualizada via sudo mysql${NC}"
else
    echo -e "${YELLOW}⚠ Não foi possível alterar via sudo mysql. Tentando usar senha atual do root...${NC}"
    read -s -p "Senha atual do MySQL root (deixe vazio para cancelar): " CURRENT_ROOT_PASS
    echo ""
    if [ -n "$CURRENT_ROOT_PASS" ]; then
        if mysql -u root -p"$CURRENT_ROOT_PASS" -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '${DB_ROOT_PASS}'; FLUSH PRIVILEGES;" 2>/dev/null; then
            echo -e "${GREEN}✓ Senha root atualizada com a senha fornecida${NC}"
        else
            echo -e "${RED}✗ Falha ao alterar senha root com a senha fornecida${NC}"
            echo -e "${YELLOW}→ Por favor, configure a senha manualmente e execute o script novamente:${NC}"
            echo -e "   sudo mysql -e \"ALTER USER 'root'@'localhost' IDENTIFIED BY '${DB_ROOT_PASS}'; FLUSH PRIVILEGES;\""
            exit 1
        fi
    else
        echo -e "${RED}✗ Operação cancelada pelo usuário. Não foi possível definir senha root.${NC}"
        echo -e "${YELLOW}→ Para configurar manualmente execute:${NC}"
        echo -e "   sudo mysql -e \"ALTER USER 'root'@'localhost' IDENTIFIED BY '${DB_ROOT_PASS}'; FLUSH PRIVILEGES;\""
        exit 1
    fi
fi

# Agora podemos usar root com a nova senha para criar o banco
mysql -u "$DB_ROOT_USER" -p"$DB_ROOT_PASS" -e "CREATE DATABASE $DB_REPORT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Banco '$DB_REPORT' criado com sucesso${NC}"
else
    echo -e "${RED}✗ Erro ao criar banco de dados${NC}"
    exit 1
fi

#==============================================================================
# 4. Criar usuário de relatórios com permissões somente leitura
#==============================================================================

echo -e "${YELLOW}▶ 4. Configurando usuário de relatórios...${NC}"

# Criar usuário (ou atualizar senha se já existir)
mysql -u "$DB_ROOT_USER" -p"$DB_ROOT_PASS" <<EOF 2>/dev/null
-- Remover usuário se já existir
DROP USER IF EXISTS '${DB_REPORT_USER}'@'localhost';
DROP USER IF EXISTS '${DB_REPORT_USER}'@'%';

-- Criar novo usuário
CREATE USER '${DB_REPORT_USER}'@'localhost' IDENTIFIED BY '${DB_REPORT_PASS}';
CREATE USER '${DB_REPORT_USER}'@'%' IDENTIFIED BY '${DB_REPORT_PASS}';

-- Conceder apenas permissões de leitura (SELECT)
GRANT SELECT ON ${DB_REPORT}.* TO '${DB_REPORT_USER}'@'localhost';
GRANT SELECT ON ${DB_REPORT}.* TO '${DB_REPORT_USER}'@'%';

-- Aplicar mudanças
FLUSH PRIVILEGES;
EOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Usuário '$DB_REPORT_USER' criado com permissões SELECT${NC}"
    echo -e "   ${BLUE}→ Usuário: ${DB_REPORT_USER}${NC}"
    echo -e "   ${BLUE}→ Permissões: SELECT (somente leitura)${NC}"
    echo -e "   ${BLUE}→ Bancos: ${DB_REPORT}${NC}"
else
    echo -e "${RED}✗ Erro ao criar usuário de relatórios${NC}"
    exit 1
fi

#==============================================================================
# 5. Copiar estrutura e dados do banco de origem
#==============================================================================

echo -e "${YELLOW}▶ 5. Copiando estrutura e dados...${NC}"

# Criar arquivo temporário com dump
TEMP_DUMP="/tmp/smartceu_temp_dump_${TIMESTAMP}.sql"

mysqldump -u "$DB_USER" -p"$DB_PASS" --no-tablespaces "$DB_SOURCE" > "$TEMP_DUMP" 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Estrutura e dados exportados${NC}"
    
    # Importar para banco de relatórios usando usuário root
    mysql -u "$DB_ROOT_USER" -p"$DB_ROOT_PASS" "$DB_REPORT" < "$TEMP_DUMP" 2>/dev/null
    
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
# 6. Verificar tabelas criadas
#==============================================================================

echo -e "${YELLOW}▶ 6. Verificando tabelas criadas...${NC}"

TABLE_COUNT=$(mysql -u "$DB_ROOT_USER" -p"$DB_ROOT_PASS" -e "USE $DB_REPORT; SHOW TABLES;" 2>/dev/null | wc -l)
TABLE_COUNT=$((TABLE_COUNT - 1)) # Remover linha de cabeçalho

echo -e "${GREEN}✓ Total de tabelas criadas: $TABLE_COUNT${NC}"

# Listar tabelas
echo -e "${BLUE}Tabelas no banco '$DB_REPORT':${NC}"
mysql -u "$DB_ROOT_USER" -p"$DB_ROOT_PASS" -e "USE $DB_REPORT; SHOW TABLES;" 2>/dev/null

#==============================================================================
# 7. Verificar registros
#==============================================================================

echo -e "${YELLOW}▶ 7. Verificando registros...${NC}"

# Contar registros nas principais tabelas
echo -e "${BLUE}Contagem de registros:${NC}"

for table in users sensors sensor_readings pool_readings alerts statistics; do
    COUNT=$(mysql -u "$DB_ROOT_USER" -p"$DB_ROOT_PASS" -e "USE $DB_REPORT; SELECT COUNT(*) FROM $table;" 2>/dev/null | tail -1)
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

echo -e "${BLUE}Credenciais de Acesso:${NC}"
echo -e "  • Usuário: ${GREEN}${DB_REPORT_USER}${NC}"
echo -e "  • Senha: ${GREEN}${DB_REPORT_PASS}${NC}"
echo -e "  • Permissões: ${YELLOW}SELECT (somente leitura)${NC}"
echo -e "  • Host: ${GREEN}localhost ou % (qualquer)${NC}"
echo ""

echo -e "${BLUE}Exemplo de Conexão:${NC}"
echo -e "  ${GREEN}mysql -u ${DB_REPORT_USER} -p'${DB_REPORT_PASS}' -h localhost ${DB_REPORT}${NC}"
echo ""

echo -e "${BLUE}Próximos Passos:${NC}"
echo -e "  1. Configure a sincronização automática: ${GREEN}bash setup_report_cron.sh${NC}"
echo -e "  2. Execute sincronização manual: ${GREEN}bash sync_report_db.sh${NC}"
echo -e "  3. Configure ferramentas de BI com usuário '${DB_REPORT_USER}'"
echo ""

echo -e "${YELLOW}⚠ Importante:${NC}"
echo -e "  • Este banco é SOMENTE LEITURA para relatórios"
echo -e "  • Não faça alterações diretas neste banco"
echo -e "  • Use sempre o banco '${DB_SOURCE}' para gravações"
echo -e "  • Usuário '${DB_REPORT_USER}' tem apenas permissão SELECT"
echo ""
