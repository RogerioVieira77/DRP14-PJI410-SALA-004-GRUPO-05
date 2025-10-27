#!/bin/bash

################################################################################
# Script de Configuração do Serviço Systemd - IoT Gateway
# Cria e configura o serviço para inicialização automática
################################################################################

set -e

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Configurando Serviço Systemd${NC}"
echo -e "${BLUE}========================================${NC}\n"

PROJECT_DIR="/opt/iot-gateway/PI---IV---V1"
SERVICE_NAME="iot-gateway"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

# Verificar se o diretório do projeto existe
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${YELLOW}⚠️  Diretório $PROJECT_DIR não encontrado!${NC}"
    exit 1
fi

# Obter usuário atual
CURRENT_USER=$USER

echo -e "${BLUE}ℹ️  Criando arquivo de serviço...${NC}"

# Criar arquivo de serviço
sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=IoT Gateway Service - MQTT Sensor Integration
Documentation=https://github.com/RogerioVieira77/PI---IV---V1
After=network.target mosquitto.service
Requires=mosquitto.service

[Service]
Type=simple
User=$CURRENT_USER
Group=$CURRENT_USER
WorkingDirectory=$PROJECT_DIR
Environment="PATH=/opt/iot-gateway/venv/bin:/usr/local/bin:/usr/bin:/bin"
Environment="PYTHONUNBUFFERED=1"

# Comando de execução
ExecStart=/opt/iot-gateway/venv/bin/python backend/gateway/gateway.py

# Reiniciar em caso de falha
Restart=on-failure
RestartSec=10

# Timeout
TimeoutStartSec=30
TimeoutStopSec=30

# Logs
StandardOutput=journal
StandardError=journal
SyslogIdentifier=iot-gateway

# Segurança (opcional - descomente se necessário)
# NoNewPrivileges=true
# PrivateTmp=true
# ProtectSystem=strict
# ProtectHome=read-only
# ReadWritePaths=$PROJECT_DIR

[Install]
WantedBy=multi-user.target
EOF

echo -e "${GREEN}✅ Arquivo de serviço criado: $SERVICE_FILE${NC}"

# Recarregar systemd
echo -e "${BLUE}ℹ️  Recarregando systemd...${NC}"
sudo systemctl daemon-reload

# Habilitar serviço
echo -e "${BLUE}ℹ️  Habilitando serviço...${NC}"
sudo systemctl enable $SERVICE_NAME.service

echo -e "${GREEN}✅ Serviço habilitado!${NC}"

# Perguntar se deseja iniciar agora
read -p "Deseja iniciar o serviço agora? (s/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo -e "${BLUE}ℹ️  Iniciando serviço...${NC}"
    sudo systemctl start $SERVICE_NAME.service
    
    # Aguardar um pouco
    sleep 2
    
    # Verificar status
    if sudo systemctl is-active --quiet $SERVICE_NAME; then
        echo -e "${GREEN}✅ Serviço iniciado com sucesso!${NC}"
    else
        echo -e "${YELLOW}⚠️  Serviço pode não ter iniciado corretamente.${NC}"
        echo -e "${BLUE}Verificando status...${NC}"
        sudo systemctl status $SERVICE_NAME.service
    fi
else
    echo -e "${YELLOW}⚠️  Serviço não foi iniciado.${NC}"
    echo -e "${BLUE}Para iniciar manualmente:${NC} sudo systemctl start $SERVICE_NAME.service"
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Configuração Concluída!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${BLUE}📋 Comandos Úteis:${NC}"
echo ""
echo -e "  ${YELLOW}Iniciar serviço:${NC}"
echo -e "    sudo systemctl start $SERVICE_NAME"
echo ""
echo -e "  ${YELLOW}Parar serviço:${NC}"
echo -e "    sudo systemctl stop $SERVICE_NAME"
echo ""
echo -e "  ${YELLOW}Reiniciar serviço:${NC}"
echo -e "    sudo systemctl restart $SERVICE_NAME"
echo ""
echo -e "  ${YELLOW}Status do serviço:${NC}"
echo -e "    sudo systemctl status $SERVICE_NAME"
echo ""
echo -e "  ${YELLOW}Ver logs em tempo real:${NC}"
echo -e "    sudo journalctl -u $SERVICE_NAME -f"
echo ""
echo -e "  ${YELLOW}Ver últimas 100 linhas de log:${NC}"
echo -e "    sudo journalctl -u $SERVICE_NAME -n 100"
echo ""
echo -e "  ${YELLOW}Desabilitar serviço:${NC}"
echo -e "    sudo systemctl disable $SERVICE_NAME"
echo ""
