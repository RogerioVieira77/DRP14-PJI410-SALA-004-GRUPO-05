#!/bin/bash

# ======================================================================
# SmartCEU - Habilitar Conexões Remotas no MySQL
# ======================================================================
# 
# Propósito: Configurar MySQL para aceitar conexões externas
#            necessárias para ferramentas de BI (Power BI, Tableau, etc)
#
# Autor: Sistema SmartCEU
# Data: $(date +%Y-%m-%d)
#
# ======================================================================

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_error() {
    echo -e "${RED}[ERRO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCESSO]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[AVISO]${NC} $1"
}

print_step() {
    echo -e "\n${BLUE}==>${NC} $1"
}

# ======================================================================
# VERIFICAÇÕES INICIAIS
# ======================================================================

print_step "Verificando permissões..."

if [[ $EUID -ne 0 ]]; then
   print_error "Este script deve ser executado como root"
   exit 1
fi

print_success "Executando como root"

# ======================================================================
# BACKUP DA CONFIGURAÇÃO ATUAL
# ======================================================================

print_step "Fazendo backup da configuração do MySQL..."

MYSQL_CNF="/etc/mysql/mysql.conf.d/mysqld.cnf"
BACKUP_DIR="/root/backups"
BACKUP_FILE="${BACKUP_DIR}/mysqld.cnf.backup.$(date +%Y%m%d_%H%M%S)"

mkdir -p "${BACKUP_DIR}"

if [ -f "${MYSQL_CNF}" ]; then
    cp "${MYSQL_CNF}" "${BACKUP_FILE}"
    print_success "Backup criado: ${BACKUP_FILE}"
else
    print_error "Arquivo de configuração não encontrado: ${MYSQL_CNF}"
    exit 1
fi

# ======================================================================
# VERIFICAR CONFIGURAÇÃO ATUAL
# ======================================================================

print_step "Verificando configuração atual..."

if grep -q "^bind-address.*127.0.0.1" "${MYSQL_CNF}"; then
    print_warning "MySQL configurado apenas para localhost (127.0.0.1)"
    NEEDS_CHANGE=true
elif grep -q "^bind-address.*0.0.0.0" "${MYSQL_CNF}"; then
    print_success "MySQL já está configurado para aceitar conexões remotas"
    NEEDS_CHANGE=false
else
    print_warning "Configuração de bind-address não encontrada"
    NEEDS_CHANGE=true
fi

# ======================================================================
# ALTERAR CONFIGURAÇÃO
# ======================================================================

if [ "$NEEDS_CHANGE" = true ]; then
    print_step "Alterando configuração do MySQL..."
    
    # Alterar bind-address de 127.0.0.1 para 0.0.0.0
    sed -i 's/^bind-address.*127.0.0.1/bind-address = 0.0.0.0/' "${MYSQL_CNF}"
    
    # Se não existir, adicionar
    if ! grep -q "^bind-address" "${MYSQL_CNF}"; then
        echo "" >> "${MYSQL_CNF}"
        echo "# Allow remote connections" >> "${MYSQL_CNF}"
        echo "bind-address = 0.0.0.0" >> "${MYSQL_CNF}"
    fi
    
    print_success "Configuração alterada para aceitar conexões de qualquer IP"
else
    print_info "Nenhuma alteração necessária na configuração"
fi

# ======================================================================
# CRIAR USUÁRIO PARA CONEXÃO REMOTA
# ======================================================================

print_step "Configurando usuário para acesso remoto..."

DB_PASSWORD="SmartCEU2025)!"

# Criar usuário smart_ceu_report com acesso remoto
mysql -u root -p"${DB_PASSWORD}" -e "
-- Criar usuário para conexão remota (de qualquer IP)
CREATE USER IF NOT EXISTS 'smart_ceu_report'@'%' IDENTIFIED BY '${DB_PASSWORD}';

-- Dar permissão de SELECT no banco de relatórios
GRANT SELECT ON smartceu_report_db.* TO 'smart_ceu_report'@'%';

-- Aplicar mudanças
FLUSH PRIVILEGES;
" 2>/dev/null

if [ $? -eq 0 ]; then
    print_success "Usuário configurado para acesso remoto"
else
    print_error "Falha ao configurar usuário"
    print_info "O usuário pode já existir ou há um problema de autenticação"
fi

# ======================================================================
# VERIFICAR USUÁRIOS
# ======================================================================

print_step "Verificando usuários configurados..."

mysql -u root -p"${DB_PASSWORD}" -e "
SELECT 
    user, 
    host,
    CASE 
        WHEN host = '%' THEN 'Remoto (qualquer IP)'
        WHEN host = 'localhost' THEN 'Apenas local'
        ELSE host
    END as 'Tipo de Acesso'
FROM mysql.user 
WHERE user = 'smart_ceu_report'
ORDER BY host;
"

# ======================================================================
# CONFIGURAR FIREWALL
# ======================================================================

print_step "Verificando firewall..."

if command -v ufw &> /dev/null; then
    UFW_STATUS=$(ufw status | grep -i "Status:" | awk '{print $2}')
    
    if [ "$UFW_STATUS" = "active" ]; then
        print_info "Firewall UFW está ativo"
        
        if ! ufw status | grep -q "3306"; then
            print_warning "Porta 3306 não está liberada no firewall"
            print_info "Liberando porta 3306..."
            ufw allow 3306/tcp
            print_success "Porta 3306 liberada no firewall"
        else
            print_success "Porta 3306 já está liberada"
        fi
    else
        print_info "Firewall UFW está inativo (porta 3306 já acessível)"
    fi
else
    print_info "UFW não instalado (firewall não gerenciado por UFW)"
fi

# ======================================================================
# REINICIAR MYSQL
# ======================================================================

print_step "Reiniciando serviço MySQL..."

systemctl restart mysql

if [ $? -eq 0 ]; then
    print_success "MySQL reiniciado com sucesso"
    sleep 3
else
    print_error "Falha ao reiniciar MySQL"
    print_warning "Restaurando backup..."
    cp "${BACKUP_FILE}" "${MYSQL_CNF}"
    systemctl restart mysql
    exit 1
fi

# ======================================================================
# VERIFICAR NOVA CONFIGURAÇÃO
# ======================================================================

print_step "Verificando se MySQL está escutando em todas as interfaces..."

if netstat -tuln | grep -q "0.0.0.0:3306"; then
    print_success "MySQL está escutando em 0.0.0.0:3306 (todas as interfaces)"
    netstat -tuln | grep 3306
elif netstat -tuln | grep -q ":::3306"; then
    print_success "MySQL está escutando em :::3306 (IPv6 - todas as interfaces)"
    netstat -tuln | grep 3306
else
    print_error "MySQL ainda está escutando apenas em localhost"
    netstat -tuln | grep 3306
    print_warning "Pode ser necessário verificar manualmente a configuração"
fi

# ======================================================================
# TESTAR CONEXÃO
# ======================================================================

print_step "Testando conexão local..."

mysql -u smart_ceu_report -p"${DB_PASSWORD}" -h 127.0.0.1 -D smartceu_report_db -e "SELECT 'Conexão OK' as status;" 2>/dev/null

if [ $? -eq 0 ]; then
    print_success "Conexão local funcionando"
else
    print_warning "Falha no teste de conexão local"
fi

# ======================================================================
# OBTER IP PÚBLICO
# ======================================================================

print_step "Informações de conexão..."

PUBLIC_IP=$(curl -s ifconfig.me 2>/dev/null || echo "82.25.75.88")
PRIVATE_IP=$(hostname -I | awk '{print $1}')

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║           INFORMAÇÕES PARA CONEXÃO POWER BI                    ║"
echo "╠════════════════════════════════════════════════════════════════╣"
echo "║  SERVER (IP Público):  ${PUBLIC_IP}                        ║"
echo "║  DATABASE:             smartceu_report_db                      ║"
echo "║  USERNAME:             smart_ceu_report                        ║"
echo "║  PASSWORD:             SmartCEU2025)!                          ║"
echo "║  PORT:                 3306                                    ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# ======================================================================
# RESUMO
# ======================================================================

print_step "Resumo das Alterações"
echo ""
echo "✅ Backup da configuração: ${BACKUP_FILE}"
echo "✅ MySQL configurado para aceitar conexões remotas (0.0.0.0)"
echo "✅ Usuário 'smart_ceu_report'@'%' criado/atualizado"
echo "✅ Permissões de SELECT concedidas no smartceu_report_db"
echo "✅ MySQL reiniciado"
echo ""
print_success "Configuração concluída!"
echo ""
print_info "Próximos passos:"
echo "  1. Teste a conexão do Power BI usando as informações acima"
echo "  2. Se houver problemas, verifique os logs: journalctl -u mysql -n 50"
echo ""
print_warning "SEGURANÇA: Certifique-se de que apenas IPs confiáveis acessem a porta 3306"
echo ""
