#!/bin/bash
###############################################################################
# Script de Instalação do Grafana - CEU Tres Pontes
# Sistema de Controle de Acesso e Monitoramento
# 
# Este script automatiza a instalação do Grafana no servidor Ubuntu
# 
# Uso: sudo bash install_grafana.sh
###############################################################################

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções de log
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

echo "=============================================="
echo "  Instalação do Grafana - CEU Tres Pontes"
echo "=============================================="
echo ""

# Passo 1: Instalar dependências
log_info "Instalando dependências..."
apt-get update
apt-get install -y apt-transport-https software-properties-common wget gnupg2 curl
log_success "Dependências instaladas"

# Passo 2: Adicionar repositório do Grafana
log_info "Adicionando repositório oficial do Grafana..."
mkdir -p /etc/apt/keyrings/

# Baixar e adicionar chave GPG
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | tee /etc/apt/keyrings/grafana.gpg > /dev/null

# Adicionar repositório
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | tee /etc/apt/sources.list.d/grafana.list
log_success "Repositório adicionado"

# Passo 3: Instalar Grafana
log_info "Instalando Grafana OSS..."
apt-get update
apt-get install -y grafana
log_success "Grafana instalado"

# Passo 4: Verificar versão
GRAFANA_VERSION=$(grafana-server -v | head -n 1)
log_info "Versão instalada: $GRAFANA_VERSION"

# Passo 5: Configurar serviço
log_info "Configurando serviço do Grafana..."
systemctl daemon-reload
systemctl enable grafana-server
log_success "Serviço configurado para iniciar no boot"

# Passo 6: Iniciar Grafana
log_info "Iniciando Grafana..."
systemctl start grafana-server

# Aguardar inicialização
sleep 5

# Verificar status
if systemctl is-active --quiet grafana-server; then
    log_success "Grafana iniciado com sucesso!"
else
    log_error "Falha ao iniciar Grafana"
    log_info "Verificando logs..."
    journalctl -u grafana-server -n 20 --no-pager
    exit 1
fi

# Passo 7: Verificar porta
log_info "Verificando porta 3000..."
if netstat -tulpn | grep -q ":3000"; then
    log_success "Grafana está rodando na porta 3000"
else
    log_warning "Porta 3000 não está escutando"
fi

# Passo 8: Criar diretório para backups
log_info "Criando diretório para backups..."
mkdir -p /backup/grafana
chown grafana:grafana /backup/grafana
log_success "Diretório de backup criado"

# Passo 9: Configurar permissões
log_info "Configurando permissões..."
chown -R grafana:grafana /var/lib/grafana
chown -R grafana:grafana /var/log/grafana
chown -R grafana:grafana /etc/grafana
log_success "Permissões configuradas"

echo ""
echo "=============================================="
echo "  ✅ Instalação Concluída com Sucesso!"
echo "=============================================="
echo ""
echo "📊 Acesse o Grafana em: http://$(hostname -I | awk '{print $1}'):3000"
echo ""
echo "🔐 Credenciais padrão:"
echo "   Usuário: admin"
echo "   Senha: admin"
echo "   (Você será solicitado a alterar a senha no primeiro login)"
echo ""
echo "📝 Próximos passos:"
echo "   1. Acesse o Grafana pelo navegador"
echo "   2. Altere a senha padrão"
echo "   3. Execute o script: sudo bash configure_grafana_datasource.sh"
echo "   4. Configure o Nginx como proxy reverso"
echo ""
echo "📚 Documentação completa: docs/GRAFANA_SETUP_GUIDE.md"
echo ""
echo "🔍 Verificar status: sudo systemctl status grafana-server"
echo "📋 Ver logs: sudo journalctl -u grafana-server -f"
echo ""
