#!/bin/bash

################################################################################
# Script de Deploy - IoT Gateway
# Atualiza o código e reinicia os serviços
################################################################################

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PROJECT_DIR="/opt/iot-gateway/PI---IV---V1"
VENV_DIR="/opt/iot-gateway/venv"
SERVICE_NAME="iot-gateway"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Deploy IoT Gateway${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Verificar se está no diretório do projeto
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}❌ Diretório $PROJECT_DIR não encontrado!${NC}"
    exit 1
fi

cd "$PROJECT_DIR"

################################################################################
# 1. FAZER BACKUP
################################################################################

echo -e "${BLUE}1. Criando backup...${NC}"

BACKUP_DIR="/opt/backups/iot-gateway"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.tar.gz"

mkdir -p "$BACKUP_DIR"

tar -czf "$BACKUP_FILE" \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.git' \
    "$PROJECT_DIR" 2>/dev/null

echo -e "${GREEN}✅ Backup criado: $BACKUP_FILE${NC}"

################################################################################
# 2. PARAR SERVIÇO (SE ESTIVER RODANDO)
################################################################################

echo -e "\n${BLUE}2. Verificando serviço...${NC}"

if sudo systemctl is-active --quiet $SERVICE_NAME 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Parando serviço $SERVICE_NAME...${NC}"
    sudo systemctl stop $SERVICE_NAME
    sleep 2
    echo -e "${GREEN}✅ Serviço parado${NC}"
else
    echo -e "${BLUE}ℹ️  Serviço não está rodando${NC}"
fi

################################################################################
# 3. ATUALIZAR CÓDIGO
################################################################################

echo -e "\n${BLUE}3. Atualizando código...${NC}"

# Verificar se é um repositório Git
if [ -d ".git" ]; then
    echo -e "${BLUE}ℹ️  Repositório Git detectado${NC}"
    
    # Salvar alterações locais (se houver)
    if ! git diff-index --quiet HEAD --; then
        echo -e "${YELLOW}⚠️  Há alterações locais. Fazendo stash...${NC}"
        git stash
    fi
    
    # Atualizar
    echo -e "${BLUE}ℹ️  Fazendo git pull...${NC}"
    git pull origin main || git pull origin master
    
    echo -e "${GREEN}✅ Código atualizado via Git${NC}"
else
    echo -e "${YELLOW}⚠️  Não é um repositório Git${NC}"
    echo -e "${BLUE}ℹ️  Para atualizar manualmente, use SCP do Windows:${NC}"
    echo -e "   scp -r \"c:\\PI - IV - V1\\*\" usuario@192.168.0.194:$PROJECT_DIR/"
fi

################################################################################
# 4. ATUALIZAR DEPENDÊNCIAS
################################################################################

echo -e "\n${BLUE}4. Verificando dependências Python...${NC}"

if [ -f "requirements.txt" ]; then
    echo -e "${BLUE}ℹ️  Ativando ambiente virtual...${NC}"
    source $VENV_DIR/bin/activate
    
    echo -e "${BLUE}ℹ️  Instalando/atualizando dependências...${NC}"
    pip install -r requirements.txt --upgrade
    
    if [ -f "backend/requirements-phase2.txt" ]; then
        pip install -r backend/requirements-phase2.txt --upgrade
    fi
    
    echo -e "${GREEN}✅ Dependências atualizadas${NC}"
else
    echo -e "${YELLOW}⚠️  Arquivo requirements.txt não encontrado${NC}"
fi

################################################################################
# 5. VERIFICAR CONFIGURAÇÕES
################################################################################

echo -e "\n${BLUE}5. Verificando configurações...${NC}"

MQTT_CONFIG="backend/config/mqtt_config.ini"

if [ -f "$MQTT_CONFIG" ]; then
    if grep -q "192.168.0.194" "$MQTT_CONFIG"; then
        echo -e "${GREEN}✅ Configuração MQTT correta (192.168.0.194)${NC}"
    else
        echo -e "${YELLOW}⚠️  Configuração MQTT pode estar incorreta${NC}"
        echo -e "${BLUE}ℹ️  Verifique: $MQTT_CONFIG${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Arquivo de configuração MQTT não encontrado${NC}"
fi

################################################################################
# 6. REINICIAR SERVIÇO
################################################################################

echo -e "\n${BLUE}6. Reiniciando serviço...${NC}"

if sudo systemctl list-unit-files | grep -q "$SERVICE_NAME.service"; then
    sudo systemctl start $SERVICE_NAME
    sleep 3
    
    if sudo systemctl is-active --quiet $SERVICE_NAME; then
        echo -e "${GREEN}✅ Serviço iniciado com sucesso!${NC}"
    else
        echo -e "${RED}❌ Falha ao iniciar serviço${NC}"
        echo -e "${BLUE}ℹ️  Verificando logs...${NC}"
        sudo journalctl -u $SERVICE_NAME -n 20 --no-pager
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  Serviço systemd não configurado${NC}"
    echo -e "${BLUE}ℹ️  Execute: ./deploy/setup_service.sh${NC}"
fi

################################################################################
# 7. VERIFICAR STATUS
################################################################################

echo -e "\n${BLUE}7. Verificando status do sistema...${NC}"

# Status do Mosquitto
if sudo systemctl is-active --quiet mosquitto; then
    echo -e "${GREEN}✅ Mosquitto: ATIVO${NC}"
else
    echo -e "${RED}❌ Mosquitto: INATIVO${NC}"
fi

# Status do Gateway
if sudo systemctl is-active --quiet $SERVICE_NAME; then
    echo -e "${GREEN}✅ Gateway: ATIVO${NC}"
else
    echo -e "${RED}❌ Gateway: INATIVO${NC}"
fi

# Portas abertas
echo -e "\n${BLUE}Portas abertas:${NC}"
sudo netstat -tulpn | grep -E ':(1883|8000)' || echo -e "${YELLOW}Nenhuma porta MQTT/API detectada${NC}"

################################################################################
# 8. LOGS RECENTES
################################################################################

echo -e "\n${BLUE}8. Últimas linhas de log:${NC}"
echo -e "${BLUE}========================================${NC}"
sudo journalctl -u $SERVICE_NAME -n 10 --no-pager
echo -e "${BLUE}========================================${NC}"

################################################################################
# RESUMO
################################################################################

echo -e "\n${BLUE}========================================${NC}"
echo -e "${GREEN}Deploy Concluído!${NC}"
echo -e "${BLUE}========================================${NC}\n"

echo -e "${BLUE}📊 Para monitorar logs em tempo real:${NC}"
echo -e "   sudo journalctl -u $SERVICE_NAME -f"
echo ""
echo -e "${BLUE}📋 Para verificar status:${NC}"
echo -e "   sudo systemctl status $SERVICE_NAME"
echo ""
echo -e "${BLUE}🔄 Para reiniciar:${NC}"
echo -e "   sudo systemctl restart $SERVICE_NAME"
echo ""
echo -e "${BLUE}🧪 Para testar MQTT:${NC}"
echo -e "   mosquitto_pub -h 192.168.0.194 -t 'test' -m 'Hello'"
echo ""
