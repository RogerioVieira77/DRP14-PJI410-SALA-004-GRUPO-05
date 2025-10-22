# 🚀 Guia de Setup - Servidor Ubuntu 24.04 (Ambiente de Testes)

## 📋 Informações do Servidor

- **Sistema Operacional**: Ubuntu 24.04 LTS
- **IP do Servidor**: `192.168.0.194`
- **Rede**: Local (mesma rede)
- **Finalidade**: Ambiente de validação/testes - Projeto IoT Gateway

---

## 📝 Índice

1. [Acesso Inicial ao Servidor](#1-acesso-inicial-ao-servidor)
2. [Atualização do Sistema](#2-atualização-do-sistema)
3. [Instalação de Ferramentas Básicas](#3-instalação-de-ferramentas-básicas)
4. [Instalação do Python 3.x](#4-instalação-do-python-3x)
5. [Instalação do Eclipse Mosquitto (MQTT Broker)](#5-instalação-do-eclipse-mosquitto-mqtt-broker)
6. [Configuração do Firewall](#6-configuração-do-firewall)
7. [Deploy da Aplicação IoT Gateway](#7-deploy-da-aplicação-iot-gateway)
8. [Configuração de Serviços Systemd](#8-configuração-de-serviços-systemd)
9. [Testes e Validação](#9-testes-e-validação)
10. [Monitoramento](#10-monitoramento)

---

## 1. Acesso Inicial ao Servidor

### 1.1 Via SSH (do Windows)

```powershell
# Conectar ao servidor via SSH
ssh usuario@192.168.0.194
```

**Substitua `usuario` pelo nome do usuário criado no Ubuntu.**

### 1.2 Se não tiver cliente SSH no Windows

```powershell
# Habilitar OpenSSH Client no Windows (PowerShell como Administrador)
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
```

### 1.3 Alternativa: PuTTY

Se preferir interface gráfica:
1. Baixe o PuTTY: https://www.putty.org/
2. Host Name: `192.168.0.194`
3. Port: `22`
4. Connection type: `SSH`
5. Clique em "Open"

---

## 2. Atualização do Sistema

**Execute no servidor Ubuntu:**

```bash
# Atualizar lista de pacotes
sudo apt update

# Atualizar todos os pacotes instalados
sudo apt upgrade -y

# Atualizar pacotes de distribuição
sudo apt dist-upgrade -y

# Remover pacotes desnecessários
sudo apt autoremove -y
sudo apt autoclean

# Reiniciar o servidor (se necessário)
sudo reboot
```

**Aguarde alguns minutos e reconecte via SSH.**

---

## 3. Instalação de Ferramentas Básicas

```bash
# Instalar ferramentas essenciais
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
    lsb-release

# Verificar instalação
git --version
curl --version
```

---

## 4. Instalação do Python 3.x

Ubuntu 24.04 já vem com Python 3, mas vamos configurar corretamente:

```bash
# Verificar versão do Python
python3 --version

# Instalar pip e ferramentas Python
sudo apt install -y \
    python3-pip \
    python3-venv \
    python3-dev

# Atualizar pip
python3 -m pip install --upgrade pip

# Verificar instalações
python3 --version
pip3 --version
```

### 4.1 Criar ambiente virtual (recomendado)

```bash
# Criar diretório para o projeto (com sudo)
sudo mkdir -p /opt/iot-gateway

# IMPORTANTE: Ajustar proprietário para seu usuário
# Substitua 'rogeriovieira' pelo seu usuário
sudo chown -R $USER:$USER /opt/iot-gateway

# Verificar permissões
ls -la /opt/iot-gateway/

# Navegar para o diretório
cd /opt/iot-gateway

# Criar ambiente virtual (agora sem sudo)
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Verificar
which python
# Deve mostrar: /opt/iot-gateway/venv/bin/python
```

**⚠️ ATENÇÃO:** Sempre que criar diretórios com `sudo` em `/opt/`, ajuste as permissões para seu usuário!

---

## 5. Instalação do Eclipse Mosquitto (MQTT Broker)

### 5.1 Instalar Mosquitto

```bash
# Instalar Mosquitto e cliente
sudo apt install -y mosquitto mosquitto-clients

# Verificar instalação
mosquitto -h

# Verificar status do serviço
sudo systemctl status mosquitto
```

### 5.2 Configurar Mosquitto

**IMPORTANTE: Primeiro, preparar diretórios e permissões:**

```bash
# Criar diretórios necessários
sudo mkdir -p /var/log/mosquitto
sudo mkdir -p /var/lib/mosquitto

# Criar arquivo de log
sudo touch /var/log/mosquitto/mosquitto.log

# Ajustar proprietário e permissões
sudo chown -R mosquitto:mosquitto /var/log/mosquitto
sudo chown -R mosquitto:mosquitto /var/lib/mosquitto

# Dar permissões adequadas
sudo chmod 755 /var/log/mosquitto
sudo chmod 755 /var/lib/mosquitto
sudo chmod 644 /var/log/mosquitto/mosquitto.log

# Verificar
ls -la /var/log/mosquitto/
ls -la /var/lib/mosquitto/
```

**Agora, criar a configuração:**

```bash
# Backup da configuração original
sudo cp /etc/mosquitto/mosquitto.conf /etc/mosquitto/mosquitto.conf.backup

# Criar configuração personalizada
sudo nano /etc/mosquitto/conf.d/custom.conf
```

**Adicione o seguinte conteúdo:**

```conf
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
```

### 5.3 Reiniciar Mosquitto

```bash
# Reiniciar serviço
sudo systemctl restart mosquitto

# Habilitar inicialização automática
sudo systemctl enable mosquitto

# Verificar status
sudo systemctl status mosquitto

# Verificar logs
sudo tail -f /var/log/mosquitto/mosquitto.log
```

### 5.4 Testar Mosquitto

**Terminal 1 - Subscriber:**
```bash
mosquitto_sub -h 192.168.0.194 -t "test/topic" -v
```

**Terminal 2 - Publisher:**
```bash
mosquitto_pub -h 192.168.0.194 -t "test/topic" -m "Hello MQTT!"
```

Se você ver a mensagem no Terminal 1, está funcionando! ✅

---

## 6. Configuração do Firewall

```bash
# Verificar status do firewall
sudo ufw status

# Se não estiver ativo, ativar
sudo ufw enable

# Permitir SSH (IMPORTANTE!)
sudo ufw allow 22/tcp

# Permitir MQTT (porta 1883)
sudo ufw allow 1883/tcp

# Permitir HTTP (se for usar frontend web)
sudo ufw allow 80/tcp

# Permitir HTTPS
sudo ufw allow 443/tcp

# Permitir API (porta 8000 - FastAPI planejada)
sudo ufw allow 8000/tcp

# Recarregar firewall
sudo ufw reload

# Verificar regras
sudo ufw status numbered
```

---

## 7. Deploy da Aplicação IoT Gateway

### 7.1 Clonar Repositório Git

**No servidor Ubuntu:**

```bash
# Navegar para o diretório base
cd /opt/iot-gateway

# Clonar repositório (estrutura final: /opt/iot-gateway/PI---IV---V1/)
git clone https://github.com/RogerioVieira77/PI---IV---V1.git

# IMPORTANTE: Garantir permissões corretas após o clone
sudo chown -R $USER:$USER /opt/iot-gateway/PI---IV---V1

# Verificar estrutura e permissões
ls -la /opt/iot-gateway/
ls -la /opt/iot-gateway/PI---IV---V1/
```

**Estrutura resultante:**
```
/opt/iot-gateway/
├── venv/                          # Ambiente virtual Python
└── PI---IV---V1/                  # Repositório clonado
    ├── backend/
    ├── frontend/
    ├── sensores/
    ├── tests/
    ├── config/
    ├── docs/
    ├── requirements.txt
    └── ...
```

### 7.2 Instalar Dependências Python

```bash
# Ativar ambiente virtual
cd /opt/iot-gateway
source venv/bin/activate

# Navegar para o diretório do projeto
cd PI---IV---V1

# Instalar dependências principais
pip install -r requirements.txt

# Instalar dependências da fase 2 (MQTT)
pip install -r backend/requirements-phase2.txt

# Verificar instalações
pip list | grep -E "paho-mqtt|configparser"
```

### 7.3 Configurar Arquivos de Configuração

```bash
# Editar configuração MQTT para usar IP do servidor
nano /opt/iot-gateway/PI---IV---V1/backend/config/mqtt_config.ini
```

**Ajustar para:**

```ini
[MQTT]
broker_host = 192.168.0.194
broker_port = 1883
qos = 1
client_id = iot_gateway_server

[TOPICS]
base_topic = sensores
lora_topic = sensores/lora/dados
zigbee_topic = sensores/zigbee/dados
sigfox_topic = sensores/sigfox/dados
rfid_topic = sensores/rfid/dados
```

### 7.4 Testar Aplicação Manualmente

```bash
# Ativar ambiente virtual e navegar para o projeto
cd /opt/iot-gateway
source venv/bin/activate
cd PI---IV---V1

# Executar gateway
python backend/gateway/gateway.py
```

**Abra outro terminal SSH e execute os simuladores:**

```bash
# Ativar ambiente virtual
cd /opt/iot-gateway
source venv/bin/activate
cd PI---IV---V1

# Executar testes
python tests/test_mqtt_integration.py
```

---

## 8. Configuração de Serviços Systemd

Para executar automaticamente na inicialização:

### 8.1 Criar Serviço do Gateway

```bash
sudo nano /etc/systemd/system/iot-gateway.service
```

**Conteúdo:**

```ini
[Unit]
Description=IoT Gateway Service
After=network.target mosquitto.service
Requires=mosquitto.service

[Service]
Type=simple
User=rogeriovieira
WorkingDirectory=/opt/iot-gateway/PI---IV---V1
Environment="PATH=/opt/iot-gateway/venv/bin"
ExecStart=/opt/iot-gateway/venv/bin/python backend/gateway/gateway.py
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**IMPORTANTE:** Ajuste o `User=` para seu usuário do servidor!

### 8.2 Ativar e Iniciar Serviço

```bash
# Recarregar systemd
sudo systemctl daemon-reload

# Habilitar serviço
sudo systemctl enable iot-gateway.service

# Iniciar serviço
sudo systemctl start iot-gateway.service

# Verificar status
sudo systemctl status iot-gateway.service

# Ver logs
sudo journalctl -u iot-gateway.service -f
```

### 8.3 Comandos Úteis do Serviço

```bash
# Parar serviço
sudo systemctl stop iot-gateway.service

# Reiniciar serviço
sudo systemctl restart iot-gateway.service

# Ver logs das últimas 100 linhas
sudo journalctl -u iot-gateway.service -n 100

# Ver logs em tempo real
sudo journalctl -u iot-gateway.service -f
```

---

## 9. Testes e Validação

### 9.1 Testar Conectividade

**Do Windows:**

```powershell
# Ping ao servidor
ping 192.168.0.194

# Testar porta MQTT
Test-NetConnection -ComputerName 192.168.0.194 -Port 1883
```

### 9.2 Testar MQTT do Windows

**Instale o cliente MQTT no Windows:**

```powershell
# Via Chocolatey (se tiver)
choco install mosquitto

# Ou baixe de: https://mosquitto.org/download/
```

**Teste publicar mensagem:**

```powershell
# Publicar mensagem
mosquitto_pub -h 192.168.0.194 -t "sensores/lora/dados" -m '{"sensor_id":"test","temperatura":25.5}'

# Subscrever tópico
mosquitto_sub -h 192.168.0.194 -t "sensores/#" -v
```

### 9.3 Verificar Logs

```bash
# Logs do Mosquitto
sudo tail -f /var/log/mosquitto/mosquitto.log

# Logs do Gateway
sudo journalctl -u iot-gateway.service -f

# Logs do sistema
sudo tail -f /var/log/syslog
```

---

## 10. Monitoramento

### 10.1 Monitorar Recursos do Sistema

```bash
# CPU, Memória, Processos
htop

# Uso de disco
df -h

# Espaço por diretório
du -sh /opt/iot-gateway/*

# Processos Python
ps aux | grep python

# Conexões de rede
sudo netstat -tulpn | grep 1883
```

### 10.2 Instalar Ferramentas de Monitoramento (Opcional)

```bash
# Instalar Glances (monitor completo)
sudo apt install -y glances

# Executar
glances
```

### 10.3 Criar Script de Status

```bash
nano /opt/iot-gateway/check_status.sh
```

**Conteúdo:**

```bash
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
systemctl is-active mosquitto && echo "✅ Mosquitto: ATIVO" || echo "❌ Mosquitto: INATIVO"
systemctl is-active iot-gateway && echo "✅ Gateway: ATIVO" || echo "❌ Gateway: INATIVO"

echo ""
echo "🔌 Portas Abertas:"
echo "----------------------"
sudo netstat -tulpn | grep -E ':(1883|8000)' || echo "Nenhuma porta MQTT/API aberta"

echo ""
echo "💾 Uso de Disco:"
echo "----------------------"
df -h /opt/iot-gateway

echo ""
echo "🧠 Uso de Memória:"
echo "----------------------"
free -h

echo ""
echo "======================================"
```

**Tornar executável:**

```bash
chmod +x /opt/iot-gateway/check_status.sh

# Executar
/opt/iot-gateway/check_status.sh
```

---

## 🎯 Checklist de Instalação

Use este checklist para garantir que tudo foi instalado:

- [ ] Sistema atualizado (`sudo apt update && sudo apt upgrade`)
- [ ] Ferramentas básicas instaladas (git, curl, etc)
- [ ] Python 3.x instalado e pip atualizado
- [ ] Ambiente virtual criado em `/opt/iot-gateway/venv`
- [ ] Eclipse Mosquitto instalado e rodando
- [ ] Firewall configurado (portas 22, 1883, 8000, 80, 443)
- [ ] Código da aplicação transferido para `/opt/iot-gateway`
- [ ] Dependências Python instaladas
- [ ] Configuração MQTT ajustada para `192.168.0.194`
- [ ] Serviço systemd criado e habilitado
- [ ] Gateway iniciado e funcionando
- [ ] Testes MQTT realizados com sucesso
- [ ] Logs sendo gerados corretamente

---

## 🚨 Solução de Problemas

### Erro de permissões (Permission Denied)

**Sintoma:** Erros ao instalar pacotes Python ou editar arquivos:
```
ERROR: [Errno 13] Permission denied
File is unwritable
```

**Solução:**

```bash
# Ajustar proprietário de todo o diretório para seu usuário
sudo chown -R $USER:$USER /opt/iot-gateway

# Dar permissões adequadas
sudo chmod -R 755 /opt/iot-gateway

# Verificar permissões
ls -la /opt/iot-gateway/
ls -la /opt/iot-gateway/venv/
ls -la /opt/iot-gateway/PI---IV---V1/

# Agora você pode usar sem sudo
cd /opt/iot-gateway
source venv/bin/activate
cd PI---IV---V1
pip install -r requirements.txt  # Sem sudo!
nano backend/config/mqtt_config.ini  # Sem sudo!
```

**Explicação:** Quando você cria diretórios em `/opt/` com `sudo`, eles pertencem ao root. Use `chown` para transferir a propriedade para seu usuário.

---

### Mosquitto não inicia

```bash
# Verificar logs detalhados
sudo journalctl -u mosquitto -n 50 --no-pager

# Testar configuração manualmente
sudo mosquitto -c /etc/mosquitto/conf.d/custom.conf -v

# Verificar permissões dos diretórios
ls -la /var/log/mosquitto/
ls -la /var/lib/mosquitto/

# Corrigir permissões se necessário
sudo mkdir -p /var/log/mosquitto /var/lib/mosquitto
sudo touch /var/log/mosquitto/mosquitto.log
sudo chown -R mosquitto:mosquitto /var/log/mosquitto
sudo chown -R mosquitto:mosquitto /var/lib/mosquitto
sudo chmod 755 /var/log/mosquitto /var/lib/mosquitto
sudo chmod 644 /var/log/mosquitto/mosquitto.log

# Verificar se o usuário mosquitto existe
id mosquitto

# Reiniciar após corrigir
sudo systemctl restart mosquitto
sudo systemctl status mosquitto
```

### Gateway não conecta ao MQTT

```bash
# Verificar se Mosquitto está escutando
sudo netstat -tulpn | grep 1883

# Testar conexão local
mosquitto_pub -h localhost -t test -m "teste"

# Verificar firewall
sudo ufw status
```

### Erro de permissões

```bash
# Ajustar proprietário do diretório
sudo chown -R $USER:$USER /opt/iot-gateway

# Dar permissões de execução
chmod +x /opt/iot-gateway/*.sh
```

---

## 📚 Próximos Passos

1. ✅ **Servidor configurado e testado**
2. 🔄 **Configurar backup automático**
3. 🔒 **Implementar segurança MQTT (usuário/senha)**
4. 📊 **Configurar banco de dados (PostgreSQL/MongoDB)**
5. 🌐 **Deploy do frontend web**
6. 🔐 **Configurar HTTPS/SSL**
7. 📈 **Implementar dashboard de monitoramento**

---

## 📞 Comandos Rápidos de Referência

```bash
# Conectar ao servidor
ssh usuario@192.168.0.194

# Status dos serviços
sudo systemctl status mosquitto
sudo systemctl status iot-gateway

# Reiniciar serviços
sudo systemctl restart mosquitto
sudo systemctl restart iot-gateway

# Ver logs em tempo real
sudo journalctl -u mosquitto -f
sudo journalctl -u iot-gateway -f

# Testar MQTT
mosquitto_sub -h 192.168.0.194 -t "sensores/#" -v
mosquitto_pub -h 192.168.0.194 -t "test" -m "teste"

# Status do sistema
/opt/iot-gateway/check_status.sh
```

---

**📅 Criado em**: 17 de Outubro de 2025  
**🎯 Projeto**: IoT Gateway - Fase 3 (Ambiente de Testes)  
**🖥️ Servidor**: Ubuntu 24.04 LTS @ 192.168.0.194
