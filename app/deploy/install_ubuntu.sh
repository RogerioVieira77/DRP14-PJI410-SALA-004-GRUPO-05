#!/bin/bash

################################################################################
# Script de Instalação Completa - IoT Gateway (Ubuntu 24.04)
# Servidor: 192.168.0.194
# Descrição: Instala e configura todo o ambiente de testes
################################################################################

set -e  # Para em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções auxiliares
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Verificar se está rodando como root
if [ "$EUID" -eq 0 ]; then 
    print_error "Não execute este script como root. Use sudo apenas quando necessário."
    exit 1
fi

print_header "IoT Gateway - Setup Completo Ubuntu 24.04"
print_info "Servidor: 192.168.0.194"
print_info "Início da instalação: $(date)"

# Confirmação
read -p "Deseja continuar com a instalação completa? (s/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    print_warning "Instalação cancelada."
    exit 1
fi

################################################################################
# 1. ATUALIZAÇÃO DO SISTEMA
################################################################################

print_header "1. Atualizando Sistema Operacional"

print_info "Atualizando lista de pacotes..."
sudo apt update

print_info "Fazendo upgrade de pacotes..."
sudo apt upgrade -y

print_info "Fazendo dist-upgrade..."
sudo apt dist-upgrade -y

print_info "Removendo pacotes desnecessários..."
sudo apt autoremove -y
sudo apt autoclean

print_success "Sistema atualizado com sucesso!"

################################################################################
# 2. INSTALAÇÃO DE FERRAMENTAS BÁSICAS
################################################################################

print_header "2. Instalando Ferramentas Básicas"

sudo apt install -y \
    build-essential \
    git \
    curl \
    wget \
    vim \
    nano \
    htop \
    net-tools \
    software-properties-common \
    ca-certificates \
    gnupg \
    lsb-release \
    ufw \
    tree

print_success "Ferramentas básicas instaladas!"

# Verificar versões
print_info "Git: $(git --version)"
print_info "Curl: $(curl --version | head -n 1)"

################################################################################
# 3. INSTALAÇÃO DO PYTHON
################################################################################

print_header "3. Instalando Python 3.x e Dependências"

sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev

# Atualizar pip
print_info "Atualizando pip..."
python3 -m pip install --upgrade pip --break-system-packages 2>/dev/null || python3 -m pip install --upgrade pip

print_success "Python instalado!"
python3 --version
pip3 --version

################################################################################
# 4. CRIAR ESTRUTURA DE DIRETÓRIOS
################################################################################

print_header "4. Criando Estrutura de Diretórios"

PROJECT_DIR="/opt/iot-gateway"

if [ -d "$PROJECT_DIR" ]; then
    print_warning "Diretório $PROJECT_DIR já existe!"
    read -p "Deseja removê-lo e criar novo? (s/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        sudo rm -rf "$PROJECT_DIR"
        print_info "Diretório removido."
    fi
fi

print_info "Criando diretório do projeto..."
sudo mkdir -p "$PROJECT_DIR"
sudo chown -R $USER:$USER "$PROJECT_DIR"

cd "$PROJECT_DIR"
print_success "Diretório criado: $PROJECT_DIR"

################################################################################
# 5. CRIAR AMBIENTE VIRTUAL PYTHON
################################################################################

print_header "5. Criando Ambiente Virtual Python"

if [ -d "$PROJECT_DIR/venv" ]; then
    print_warning "Ambiente virtual já existe. Pulando..."
else
    python3 -m venv "$PROJECT_DIR/venv"
    print_success "Ambiente virtual criado!"
fi

print_info "Para ativar o ambiente virtual, execute:"
print_info "source $PROJECT_DIR/venv/bin/activate"

################################################################################
# 6. INSTALAÇÃO DO MOSQUITTO (MQTT BROKER)
################################################################################

print_header "6. Instalando Eclipse Mosquitto (MQTT Broker)"

sudo apt install -y mosquitto mosquitto-clients

print_success "Mosquitto instalado!"

# Preparar diretórios e permissões
print_info "Preparando diretórios do Mosquitto..."

# Criar diretórios necessários
sudo mkdir -p /var/log/mosquitto
sudo mkdir -p /var/lib/mosquitto
sudo mkdir -p /etc/mosquitto/conf.d

# Criar arquivo de log
sudo touch /var/log/mosquitto/mosquitto.log

# Ajustar proprietário e permissões
sudo chown -R mosquitto:mosquitto /var/log/mosquitto
sudo chown -R mosquitto:mosquitto /var/lib/mosquitto
sudo chmod 755 /var/log/mosquitto
sudo chmod 755 /var/lib/mosquitto
sudo chmod 644 /var/log/mosquitto/mosquitto.log

print_success "Diretórios configurados!"

# Criar configuração personalizada
print_info "Configurando Mosquitto..."

sudo tee /etc/mosquitto/conf.d/custom.conf > /dev/null <<EOF
# Configuração Mosquitto - IoT Gateway
# Escutar em todas as interfaces na porta 1883
listener 1883 0.0.0.0

# Permitir conexões anônimas (apenas para testes)
allow_anonymous true

# Logs
log_dest file /var/log/mosquitto/mosquitto.log
log_dest stdout
log_type error
log_type warning
log_type notice
log_type information

# Persistência de mensagens
persistence true
persistence_location /var/lib/mosquitto/

# Configurações de conexão
max_connections 1000
EOF

print_success "Configuração do Mosquitto criada!"

# Reiniciar e habilitar Mosquitto
print_info "Reiniciando Mosquitto..."
sudo systemctl restart mosquitto
sudo systemctl enable mosquitto

# Verificar status
if sudo systemctl is-active --quiet mosquitto; then
    print_success "Mosquitto está rodando!"
else
    print_error "Mosquitto não está rodando. Verifique os logs."
    sudo systemctl status mosquitto
fi

################################################################################
# 7. CONFIGURAÇÃO DO FIREWALL
################################################################################

print_header "7. Configurando Firewall (UFW)"

# Habilitar UFW se não estiver
if ! sudo ufw status | grep -q "Status: active"; then
    print_info "Habilitando firewall..."
    echo "y" | sudo ufw enable
fi

print_info "Configurando regras do firewall..."

# Permitir SSH (CRÍTICO!)
sudo ufw allow 22/tcp comment 'SSH'

# Permitir MQTT
sudo ufw allow 1883/tcp comment 'MQTT'

# Permitir HTTP/HTTPS
sudo ufw allow 80/tcp comment 'HTTP'
sudo ufw allow 443/tcp comment 'HTTPS'

# Permitir API (porta 8000 - FastAPI)
sudo ufw allow 8000/tcp comment 'API'

# Recarregar firewall
sudo ufw reload

print_success "Firewall configurado!"
sudo ufw status numbered

################################################################################
# 8. TESTAR MOSQUITTO
################################################################################

print_header "8. Testando Mosquitto"

print_info "Verificando se Mosquitto está escutando na porta 1883..."

if sudo netstat -tulpn | grep -q ":1883"; then
    print_success "Mosquitto está escutando na porta 1883!"
else
    print_error "Mosquitto NÃO está escutando na porta 1883!"
fi

print_info "Para testar MQTT manualmente:"
echo "  Terminal 1: mosquitto_sub -h 192.168.0.194 -t 'test' -v"
echo "  Terminal 2: mosquitto_pub -h 192.168.0.194 -t 'test' -m 'Hello'"

################################################################################
# 9. CRIAR SCRIPT DE STATUS
################################################################################

print_header "9. Criando Scripts Auxiliares"

cat > "$PROJECT_DIR/check_status.sh" <<'EOF'
#!/bin/bash

echo "======================================"
echo "IoT Gateway - Status do Sistema"
echo "======================================"
echo ""

echo "🌐 IP do Servidor:"
hostname -I

echo ""
echo "📊 Status dos Serviços:"
echo "----------------------"
systemctl is-active mosquitto >/dev/null 2>&1 && echo "✅ Mosquitto: ATIVO" || echo "❌ Mosquitto: INATIVO"
systemctl is-active iot-gateway >/dev/null 2>&1 && echo "✅ Gateway: ATIVO" || echo "❌ Gateway: INATIVO"

echo ""
echo "🔌 Portas Abertas:"
echo "----------------------"
sudo netstat -tulpn | grep -E ':(1883|8000)' || echo "Nenhuma porta MQTT/API aberta"

echo ""
echo "💾 Uso de Disco:"
echo "----------------------"
df -h /opt/iot-gateway 2>/dev/null || df -h /

echo ""
echo "🧠 Uso de Memória:"
echo "----------------------"
free -h

echo ""
echo "📝 Logs Recentes do Mosquitto:"
echo "----------------------"
sudo tail -n 5 /var/log/mosquitto/mosquitto.log 2>/dev/null || echo "Logs não disponíveis"

echo ""
echo "======================================"
EOF

chmod +x "$PROJECT_DIR/check_status.sh"

print_success "Script de status criado: $PROJECT_DIR/check_status.sh"

################################################################################
# 10. CRIAR SCRIPT DE BACKUP
################################################################################

cat > "$PROJECT_DIR/backup.sh" <<'EOF'
#!/bin/bash

# Script de Backup - IoT Gateway

BACKUP_DIR="/opt/backups/iot-gateway"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.tar.gz"

# Criar diretório de backup
mkdir -p "$BACKUP_DIR"

echo "Iniciando backup..."

# Fazer backup do código e configurações
tar -czf "$BACKUP_FILE" \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    /opt/iot-gateway

echo "Backup criado: $BACKUP_FILE"

# Manter apenas os 10 backups mais recentes
ls -t "$BACKUP_DIR"/backup_*.tar.gz | tail -n +11 | xargs -r rm

echo "Backups antigos removidos (mantidos os 10 mais recentes)"
echo "Backup concluído!"
EOF

chmod +x "$PROJECT_DIR/backup.sh"

print_success "Script de backup criado: $PROJECT_DIR/backup.sh"

################################################################################
# 11. INSTALAR FERRAMENTAS DE MONITORAMENTO
################################################################################

print_header "10. Instalando Ferramentas de Monitoramento"

sudo apt install -y glances

print_success "Glances instalado! Execute com: glances"

################################################################################
# RESUMO FINAL
################################################################################

print_header "INSTALAÇÃO CONCLUÍDA!"

cat << EOF

${GREEN}✅ Sistema atualizado
✅ Ferramentas básicas instaladas
✅ Python 3.x instalado
✅ Ambiente virtual criado em: $PROJECT_DIR/venv
✅ Eclipse Mosquitto instalado e configurado
✅ Firewall configurado (portas: 22, 1883, 8000, 80, 443)
✅ Scripts auxiliares criados${NC}

${BLUE}📂 Diretório do Projeto:${NC} $PROJECT_DIR

${BLUE}🔧 Próximos Passos:${NC}

1. ${YELLOW}Transferir código do projeto:${NC}
   ${BLUE}Do Windows (PowerShell):${NC}
   cd "c:\PI - IV - V1"
   scp -r . usuario@192.168.0.194:/opt/iot-gateway/
   
   ${BLUE}OU via Git:${NC}
   cd $PROJECT_DIR
   git clone https://github.com/RogerioVieira77/PI---IV---V1.git .

2. ${YELLOW}Instalar dependências Python:${NC}
   cd $PROJECT_DIR
   source venv/bin/activate
   pip install -r requirements.txt
   pip install -r backend/requirements-phase2.txt

3. ${YELLOW}Configurar arquivo MQTT:${NC}
   nano backend/config/mqtt_config.ini
   ${BLUE}# Ajustar broker_host = 192.168.0.194${NC}

4. ${YELLOW}Testar aplicação:${NC}
   python backend/gateway/gateway.py

5. ${YELLOW}Configurar serviço systemd (ver documentação)${NC}

${BLUE}📊 Scripts Úteis:${NC}
- Status do sistema: $PROJECT_DIR/check_status.sh
- Backup: $PROJECT_DIR/backup.sh
- Monitoramento: glances

${BLUE}🧪 Testar MQTT:${NC}
  mosquitto_sub -h 192.168.0.194 -t 'sensores/#' -v
  mosquitto_pub -h 192.168.0.194 -t 'test' -m 'Hello MQTT'

${BLUE}📚 Documentação Completa:${NC}
  Ver: docs/SERVIDOR_UBUNTU_SETUP.md

${GREEN}Instalação finalizada em: $(date)${NC}

EOF

print_info "Execute o script de status para verificar o sistema:"
print_info "$PROJECT_DIR/check_status.sh"
