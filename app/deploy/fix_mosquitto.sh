#!/bin/bash

################################################################################
# SmartCEU - Script de Correção do Mosquitto
# Fix para erro "exit code 13" (permissão)
################################################################################

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_step() {
    echo -e "${BLUE}>>> $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

MQTT_PORT="1884"

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}   Corrigindo Mosquitto MQTT - SmartCEU${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Parar serviço se estiver rodando
print_step "Parando serviço Mosquitto..."
systemctl stop mosquitto || true

# Backup da config atual
if [ -f /etc/mosquitto/mosquitto.conf ]; then
    cp /etc/mosquitto/mosquitto.conf /etc/mosquitto/mosquitto.conf.smartceu_backup
    print_success "Backup criado: mosquitto.conf.smartceu_backup"
fi

# Criar configuração correta
print_step "Criando nova configuração..."

# Apenas configurações específicas do SmartCEU (sem duplicar valores do mosquitto.conf)
cat > /etc/mosquitto/conf.d/smartceu.conf << 'EOF'
# SmartCEU MQTT Configuration
# Listener na porta customizada
listener 1884 0.0.0.0
protocol mqtt

# Permitir conexões anônimas (para desenvolvimento)
allow_anonymous true

# Log types (log_dest já definido no mosquitto.conf)
log_type error
log_type warning
log_type notice
log_type information

# Configurações de conexão
max_connections -1
max_keepalive 3600
EOF

# Restaurar config original do Mosquitto
cat > /etc/mosquitto/mosquitto.conf << 'EOF'
# Place your local configuration in /etc/mosquitto/conf.d/
#
# A full description of the configuration file is at
# /usr/share/doc/mosquitto/examples/mosquitto.conf.example

pid_file /run/mosquitto/mosquitto.pid

persistence true
persistence_location /var/lib/mosquitto/

log_dest file /var/log/mosquitto/mosquitto.log

include_dir /etc/mosquitto/conf.d
EOF

print_success "Configuração criada: /etc/mosquitto/conf.d/smartceu.conf"

# Garantir permissões corretas
print_step "Ajustando permissões..."

chown mosquitto:mosquitto /etc/mosquitto/conf.d/smartceu.conf
chmod 644 /etc/mosquitto/conf.d/smartceu.conf

# Garantir que diretórios de log e persistência existem
mkdir -p /var/log/mosquitto
mkdir -p /var/lib/mosquitto
chown -R mosquitto:mosquitto /var/log/mosquitto
chown -R mosquitto:mosquitto /var/lib/mosquitto
chmod 755 /var/log/mosquitto
chmod 755 /var/lib/mosquitto

print_success "Permissões ajustadas"

# Testar configuração (sem opção -t que não existe na versão 2.x)
print_step "Testando configuração..."
print_success "Configuração criada (validação será feita ao iniciar o serviço)"

# Reiniciar serviço
print_step "Reiniciando Mosquitto..."
systemctl daemon-reload
systemctl enable mosquitto
systemctl start mosquitto

# Aguardar inicialização
sleep 2

# Verificar status
if systemctl is-active --quiet mosquitto; then
    print_success "Mosquitto iniciado com sucesso!"
    
    # Verificar se está escutando na porta correta
    if netstat -tulpn | grep -q ":${MQTT_PORT}"; then
        print_success "Mosquitto escutando na porta ${MQTT_PORT}"
    else
        print_error "Mosquitto não está escutando na porta ${MQTT_PORT}"
    fi
    
    echo ""
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✅ Mosquitto corrigido e funcionando!${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Testar conexão:"
    echo "  mosquitto_sub -h localhost -p ${MQTT_PORT} -t 'test' -v"
    echo ""
    
else
    print_error "Falha ao iniciar Mosquitto"
    echo ""
    echo "Ver logs:"
    echo "  journalctl -xeu mosquitto.service"
    echo "  tail -f /var/log/mosquitto/mosquitto.log"
    exit 1
fi

exit 0
