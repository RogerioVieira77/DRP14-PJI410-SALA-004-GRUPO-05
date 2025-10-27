#!/bin/bash
###############################################################################
# Script de Configuração do Data Source MySQL no Grafana
# CEU Tres Pontes - Sistema de Controle de Acesso
# 
# Este script cria o usuário MySQL para o Grafana e fornece instruções
# para configurar o data source
# 
# Uso: sudo bash configure_grafana_datasource.sh
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
echo "  Configuração do Data Source MySQL - Grafana"
echo "=========================================================="
echo ""

# Ler configurações do banco
DB_NAME="smartceu_db"
DB_REPORT="smartceu_report_db"
GRAFANA_USER="grafana_reader"

# Gerar senha aleatória segura
GRAFANA_PASS=$(openssl rand -base64 16)

log_info "Configurações do banco de dados:"
echo "   Database Principal: $DB_NAME"
echo "   Database Relatórios: $DB_REPORT"
echo "   Usuário: $GRAFANA_USER"
echo "   Senha: $GRAFANA_PASS"
echo ""

# Perguntar senha root do MySQL
read -sp "Digite a senha root do MySQL: " MYSQL_ROOT_PASS
echo ""

# Verificar conexão MySQL
log_info "Testando conexão com MySQL..."
if ! mysql -u root -p"$MYSQL_ROOT_PASS" -e "SELECT 1;" &> /dev/null; then
    log_error "Falha ao conectar ao MySQL. Verifique a senha root."
    exit 1
fi
log_success "Conexão com MySQL estabelecida"

# Verificar se banco existe
log_info "Verificando banco de dados..."
if ! mysql -u root -p"$MYSQL_ROOT_PASS" -e "USE $DB_NAME;" &> /dev/null; then
    log_error "Banco de dados '$DB_NAME' não encontrado!"
    log_info "Execute primeiro: python3 app/backend/init_db.py"
    exit 1
fi
log_success "Banco de dados encontrado"

# Verificar se usuário já existe
log_info "Verificando usuário existente..."
USER_EXISTS=$(mysql -u root -p"$MYSQL_ROOT_PASS" -sse "SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = '$GRAFANA_USER' AND host = 'localhost');")

if [ "$USER_EXISTS" = "1" ]; then
    log_warning "Usuário $GRAFANA_USER já existe!"
    read -p "Deseja recriar o usuário? (s/n): " RECREATE
    if [[ $RECREATE =~ ^[Ss]$ ]]; then
        log_info "Removendo usuário existente..."
        mysql -u root -p"$MYSQL_ROOT_PASS" -e "DROP USER '$GRAFANA_USER'@'localhost';"
        log_success "Usuário removido"
    else
        log_info "Operação cancelada"
        exit 0
    fi
fi

# Criar usuário Grafana
log_info "Criando usuário $GRAFANA_USER..."
mysql -u root -p"$MYSQL_ROOT_PASS" <<EOF
CREATE USER '$GRAFANA_USER'@'localhost' IDENTIFIED BY '$GRAFANA_PASS';
GRANT SELECT ON $DB_NAME.* TO '$GRAFANA_USER'@'localhost';
GRANT SELECT ON $DB_REPORT.* TO '$GRAFANA_USER'@'localhost';
FLUSH PRIVILEGES;
EOF
log_success "Usuário criado com permissões de leitura em ambos os bancos"

# Testar novo usuário
log_info "Testando novo usuário..."
if mysql -u "$GRAFANA_USER" -p"$GRAFANA_PASS" -e "USE $DB_NAME; SHOW TABLES;" &> /dev/null; then
    log_success "Usuário testado com sucesso!"
else
    log_error "Falha ao testar usuário"
    exit 1
fi

# Salvar credenciais em arquivo seguro
CREDS_FILE="/root/.grafana_mysql_credentials"
log_info "Salvando credenciais em $CREDS_FILE..."
cat > "$CREDS_FILE" <<EOF
# Credenciais MySQL para Grafana
# Gerado em: $(date)
# NÃO COMPARTILHE ESTE ARQUIVO!

Database Principal: $DB_NAME
Database Relatórios: $DB_REPORT
Host: localhost
Port: 3306
User: $GRAFANA_USER
Password: $GRAFANA_PASS
EOF
chmod 600 "$CREDS_FILE"
log_success "Credenciais salvas (apenas root pode ler)"

# Obter estatísticas do banco
log_info "Obtendo estatísticas do banco..."
TABLES=$(mysql -u root -p"$MYSQL_ROOT_PASS" -sse "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '$DB_NAME';")
READINGS=$(mysql -u root -p"$MYSQL_ROOT_PASS" -sse "SELECT COUNT(*) FROM $DB_NAME.readings;" 2>/dev/null || echo "0")
SENSORS=$(mysql -u root -p"$MYSQL_ROOT_PASS" -sse "SELECT COUNT(*) FROM $DB_NAME.sensors;" 2>/dev/null || echo "0")

echo ""
echo "=========================================================="
echo "  ✅ Configuração Concluída com Sucesso!"
echo "=========================================================="
echo ""
echo "📊 Estatísticas do Banco:"
echo "   Tabelas: $TABLES"
echo "   Sensores: $SENSORS"
echo "   Leituras: $READINGS"
echo ""
echo "🔐 Credenciais do Data Source:"
echo "   Host: localhost:3306"
echo "   Database Principal: $DB_NAME"
echo "   Database Relatórios: $DB_REPORT"
echo "   User: $GRAFANA_USER"
echo "   Password: $GRAFANA_PASS"
echo ""
echo "📝 Próximos Passos:"
echo ""
echo "1. Acesse o Grafana: http://$(hostname -I | awk '{print $1}'):3000"
echo ""
echo "2. Faça login (admin/admin e altere a senha)"
echo ""
echo "3. Adicione o Data Source PRINCIPAL:"
echo "   • Menu lateral → ⚙️ Configuration → Data sources"
echo "   • Clicar em 'Add data source'"
echo "   • Selecionar 'MySQL'"
echo "   • Name: SmartCEU DB (Principal)"
echo "   • Database: $DB_NAME"
echo "   • Preencher com as credenciais acima"
echo "   • Clicar em 'Save & test'"
echo ""
echo "4. (OPCIONAL) Adicione o Data Source de RELATÓRIOS:"
echo "   • Repetir processo acima"
echo "   • Name: SmartCEU Report DB"
echo "   • Database: $DB_REPORT"
echo ""
echo "5. Crie seus dashboards seguindo o guia:"
echo "   docs/GRAFANA_SETUP_GUIDE.md"
echo ""
echo "🔒 Segurança:"
echo "   • As credenciais estão salvas em: $CREDS_FILE"
echo "   • Arquivo protegido (apenas root)"
echo "   • NUNCA compartilhe este arquivo!"
echo ""
echo "📚 Para ver as credenciais novamente:"
echo "   sudo cat $CREDS_FILE"
echo ""
