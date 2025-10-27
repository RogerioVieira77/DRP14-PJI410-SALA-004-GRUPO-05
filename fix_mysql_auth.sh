#!/bin/bash

# ======================================================================
# SmartCEU - Corrigir Autenticação MySQL para Power BI
# ======================================================================
# 
# Propósito: Ajustar plugin de autenticação para compatibilidade
#            com clientes externos (Power BI, ODBC, etc)
#
# Erro resolvido: "Internal connection fatal error. Error state: 18"
#
# ======================================================================

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_error() { echo -e "${RED}[ERRO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCESSO]${NC} $1"; }
print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[AVISO]${NC} $1"; }
print_step() { echo -e "\n${BLUE}==>${NC} $1"; }

# ======================================================================
# CONFIGURAÇÕES
# ======================================================================

DB_PASSWORD="SmartCEU2025)!"

# ======================================================================
# VERIFICAR PLUGIN ATUAL
# ======================================================================

print_step "Verificando plugin de autenticação atual..."

mysql -u root -p"${DB_PASSWORD}" -e "
SELECT 
    user, 
    host,
    plugin as 'Plugin de Autenticação'
FROM mysql.user 
WHERE user IN ('smart_ceu_report', 'smartceu_user', 'root')
ORDER BY user, host;
"

# ======================================================================
# CORRIGIR PLUGIN DE AUTENTICAÇÃO
# ======================================================================

print_step "Ajustando plugin de autenticação para mysql_native_password..."

print_info "Isso resolve problemas de compatibilidade com Power BI e outras ferramentas"

mysql -u root -p"${DB_PASSWORD}" << 'EOF'

-- Alterar usuário de relatórios para usar mysql_native_password
ALTER USER 'smart_ceu_report'@'%' 
    IDENTIFIED WITH mysql_native_password BY 'SmartCEU2025)!';

ALTER USER 'smart_ceu_report'@'localhost' 
    IDENTIFIED WITH mysql_native_password BY 'SmartCEU2025)!';

-- Também ajustar usuário da aplicação
ALTER USER 'smartceu_user'@'localhost' 
    IDENTIFIED WITH mysql_native_password BY 'SmartCEU2025)!';

-- Aplicar mudanças
FLUSH PRIVILEGES;

-- Verificar
SELECT 
    user, 
    host,
    plugin,
    CASE 
        WHEN plugin = 'mysql_native_password' THEN '✓ Compatível'
        WHEN plugin = 'caching_sha2_password' THEN '✗ Pode ter problemas'
        ELSE plugin
    END as 'Status'
FROM mysql.user 
WHERE user IN ('smart_ceu_report', 'smartceu_user', 'root')
ORDER BY user, host;

EOF

if [ $? -eq 0 ]; then
    print_success "Plugin de autenticação atualizado com sucesso!"
else
    print_error "Falha ao atualizar plugin de autenticação"
    exit 1
fi

# ======================================================================
# VERIFICAR CONFIGURAÇÃO DO MYSQL
# ======================================================================

print_step "Verificando configuração do MySQL..."

MYSQL_VERSION=$(mysql --version | grep -oP '\d+\.\d+\.\d+' | head -1)
print_info "Versão do MySQL: ${MYSQL_VERSION}"

# Verificar se default_authentication_plugin está configurado
print_info "Verificando plugin de autenticação padrão..."

DEFAULT_AUTH=$(mysql -u root -p"${DB_PASSWORD}" -Nse "SHOW VARIABLES LIKE 'default_authentication_plugin';" | awk '{print $2}')

if [ -n "$DEFAULT_AUTH" ]; then
    print_info "Plugin padrão: ${DEFAULT_AUTH}"
    
    if [ "$DEFAULT_AUTH" != "mysql_native_password" ]; then
        print_warning "Plugin padrão não é mysql_native_password"
        print_info "Recomenda-se adicionar ao arquivo de configuração:"
        echo "    [mysqld]"
        echo "    default_authentication_plugin=mysql_native_password"
    fi
fi

# ======================================================================
# TESTAR CONEXÃO
# ======================================================================

print_step "Testando conexão com o usuário de relatórios..."

# Teste 1: Conexão local via TCP (simula conexão remota)
print_info "Teste 1: Conexão via TCP (localhost)..."
mysql -u smart_ceu_report -p"${DB_PASSWORD}" -h 127.0.0.1 -P 3306 smartceu_report_db -e "SELECT 'Conexão OK' as status, DATABASE() as banco, USER() as usuario;" 2>/dev/null

if [ $? -eq 0 ]; then
    print_success "Conexão TCP local funcionando!"
else
    print_error "Falha na conexão TCP local"
    print_info "Verificando se o banco existe..."
    
    DB_EXISTS=$(mysql -u root -p"${DB_PASSWORD}" -Nse "SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME='smartceu_report_db';")
    
    if [ -z "$DB_EXISTS" ]; then
        print_error "Banco smartceu_report_db NÃO existe!"
        print_info "Execute o script: bash create_report_db.sh"
    else
        print_success "Banco smartceu_report_db existe"
        print_warning "Pode haver outro problema com as permissões"
    fi
fi

# ======================================================================
# VERIFICAR PERMISSÕES
# ======================================================================

print_step "Verificando permissões do usuário..."

mysql -u root -p"${DB_PASSWORD}" -e "
SHOW GRANTS FOR 'smart_ceu_report'@'%';
" 2>/dev/null

# ======================================================================
# INFORMAÇÕES PARA CONEXÃO
# ======================================================================

print_step "Informações para conexão Power BI..."

PUBLIC_IP=$(curl -s ifconfig.me 2>/dev/null || echo "82.25.75.88")

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         CREDENCIAIS CORRIGIDAS PARA POWER BI                   ║"
echo "╠════════════════════════════════════════════════════════════════╣"
echo "║  Conector:       MySQL database                                ║"
echo "║  Server:         ${PUBLIC_IP}                             ║"
echo "║  Port:           3306                                          ║"
echo "║  Database:       smartceu_report_db                            ║"
echo "║  Username:       smart_ceu_report                              ║"
echo "║  Password:       SmartCEU2025)!                                ║"
echo "║                                                                ║"
echo "║  Autenticação:   Database                                      ║"
echo "║  Plugin:         mysql_native_password (CORRIGIDO)             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# ======================================================================
# INSTRUÇÕES ADICIONAIS
# ======================================================================

print_step "Instruções para Power BI"
echo ""
print_info "1. No Power BI Desktop, vá em: Obter Dados > Mais..."
print_info "2. Procure por: MySQL database"
print_info "3. Preencha:"
echo "      - Server: ${PUBLIC_IP}"
echo "      - Database: smartceu_report_db"
print_info "4. Clique em OK"
print_info "5. Escolha autenticação: Database"
print_info "6. Digite:"
echo "      - User name: smart_ceu_report"
echo "      - Password: SmartCEU2025)!"
print_info "7. Clique em Conectar"
echo ""

print_warning "Se ainda houver erro, pode ser necessário instalar o conector MySQL:"
echo "  - MySQL Connector/ODBC 8.0 ou superior"
echo "  - Download: https://dev.mysql.com/downloads/connector/odbc/"
echo ""

# ======================================================================
# VERIFICAR SE BANCO EXISTE
# ======================================================================

print_step "Verificando se o banco de relatórios existe..."

DB_EXISTS=$(mysql -u root -p"${DB_PASSWORD}" -Nse "SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME='smartceu_report_db';")

if [ -z "$DB_EXISTS" ]; then
    print_error "Banco smartceu_report_db NÃO EXISTE!"
    echo ""
    print_warning "AÇÃO NECESSÁRIA: Criar o banco de relatórios"
    echo ""
    print_info "Execute o seguinte comando:"
    echo "    cd /var/www/smartceu"
    echo "    bash create_report_db.sh"
    echo ""
else
    print_success "Banco smartceu_report_db existe"
    
    # Contar tabelas
    TABLE_COUNT=$(mysql -u root -p"${DB_PASSWORD}" -Nse "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='smartceu_report_db';")
    print_info "Número de tabelas: ${TABLE_COUNT}"
    
    if [ "$TABLE_COUNT" -gt 0 ]; then
        print_success "Banco está populado com ${TABLE_COUNT} tabelas"
    else
        print_warning "Banco existe mas não tem tabelas (vazio)"
    fi
fi

# ======================================================================
# RESUMO
# ======================================================================

print_step "Resumo da Correção"
echo ""
echo "✅ Plugin de autenticação alterado para mysql_native_password"
echo "✅ Usuários atualizados: smart_ceu_report@% e smart_ceu_report@localhost"
echo "✅ Compatibilidade com Power BI corrigida"
echo ""

if [ -n "$DB_EXISTS" ]; then
    print_success "Pronto para conectar no Power BI!"
else
    print_error "Ainda é necessário criar o banco de relatórios"
    print_info "Execute: bash create_report_db.sh"
fi

echo ""
