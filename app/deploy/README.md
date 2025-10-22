# 🚀 Scripts de Deploy - IoT Gateway

Pasta contendo scripts automatizados para deploy e configuração do servidor Ubuntu 24.04.

## 📂 Arquivos

### 1. `install_ubuntu.sh`
**Instalação completa do ambiente**

Script principal que:
- ✅ Atualiza o sistema Ubuntu
- ✅ Instala ferramentas básicas (git, curl, vim, etc)
- ✅ Instala Python 3.x e pip
- ✅ Cria ambiente virtual Python
- ✅ Instala e configura Eclipse Mosquitto (MQTT Broker)
- ✅ Configura firewall (UFW)
- ✅ Cria scripts auxiliares (status, backup)
- ✅ Instala ferramentas de monitoramento

**Uso:**
```bash
# No servidor Ubuntu (192.168.0.194)
cd /tmp
# Copie o arquivo do Windows ou baixe do Git
chmod +x install_ubuntu.sh
./install_ubuntu.sh
```

---

### 2. `setup_service.sh`
**Configuração do serviço systemd**

Cria e configura o serviço para:
- ✅ Inicialização automática do Gateway
- ✅ Reinício automático em caso de falha
- ✅ Logging via journalctl
- ✅ Dependência do serviço Mosquitto

**Uso:**
```bash
cd /opt/iot-gateway/deploy
chmod +x setup_service.sh
./setup_service.sh
```

---

### 3. `deploy.sh`
**Deploy/Atualização da aplicação**

Script para atualizar código e reiniciar:
- ✅ Cria backup automático
- ✅ Para o serviço
- ✅ Atualiza código (Git pull)
- ✅ Atualiza dependências Python
- ✅ Verifica configurações
- ✅ Reinicia serviço
- ✅ Mostra logs recentes

**Uso:**
```bash
cd /opt/iot-gateway
./deploy/deploy.sh
```

---

## 🎯 Fluxo de Instalação Completa

### Passo 1: Preparar Windows

No seu Windows, prepare os arquivos para transferência:

```powershell
# Navegar até o projeto
cd "c:\PI - IV - V1"

# Verificar se os scripts existem
ls deploy\*.sh
```

### Passo 2: Conectar ao Servidor

```powershell
# Conectar via SSH
ssh usuario@192.168.0.194

# Se não tiver SSH, instale:
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
```

### Passo 3: Transferir Scripts

**Opção A - Via SCP (do Windows):**

```powershell
# Transferir apenas os scripts de deploy
scp deploy\*.sh usuario@192.168.0.194:/tmp/

# Transferir o projeto completo
scp -r . usuario@192.168.0.194:/tmp/iot-gateway/
```

**Opção B - Via Git (Recomendado):**

```bash
# No servidor Ubuntu
cd /tmp
git clone https://github.com/RogerioVieira77/PI---IV---V1.git
cd PI---IV---V1
```

### Passo 4: Executar Instalação

```bash
# No servidor Ubuntu
cd /tmp
chmod +x install_ubuntu.sh
./install_ubuntu.sh
```

**Este script vai:**
- Atualizar o sistema
- Instalar todas as dependências
- Configurar Mosquitto
- Criar estrutura em `/opt/iot-gateway`

⏱️ **Tempo estimado:** 10-15 minutos

### Passo 5: Transferir Código

```bash
# Se usou SCP
mv /tmp/iot-gateway/* /opt/iot-gateway/

# Se usou Git
cd /opt/iot-gateway
git clone https://github.com/RogerioVieira77/PI---IV---V1.git .
```

### Passo 6: Instalar Dependências Python

```bash
cd /opt/iot-gateway
source venv/bin/activate
pip install -r requirements.txt
pip install -r backend/requirements-phase2.txt
```

### Passo 7: Configurar MQTT

```bash
nano backend/config/mqtt_config.ini
```

**Ajuste:**
```ini
[MQTT]
broker_host = 192.168.0.194
broker_port = 1883
```

### Passo 8: Configurar Serviço Systemd

```bash
cd /opt/iot-gateway
chmod +x deploy/setup_service.sh
./deploy/setup_service.sh
```

### Passo 9: Testar

```bash
# Ver status
sudo systemctl status iot-gateway

# Ver logs
sudo journalctl -u iot-gateway -f

# Testar MQTT
mosquitto_sub -h 192.168.0.194 -t "sensores/#" -v
```

---

## 🔄 Fluxo de Atualização (Deploy)

Quando você modificar o código no Windows e quiser atualizar o servidor:

### Do Windows:

```powershell
# Fazer commit e push (se estiver usando Git)
git add .
git commit -m "Atualização XYZ"
git push origin main
```

### No Servidor:

```bash
cd /opt/iot-gateway
./deploy/deploy.sh
```

O script automaticamente:
1. ✅ Faz backup
2. ✅ Para o serviço
3. ✅ Puxa atualizações do Git
4. ✅ Atualiza dependências
5. ✅ Reinicia serviço
6. ✅ Mostra logs

---

## 📋 Comandos Rápidos

### Gerenciar Serviço

```bash
# Iniciar
sudo systemctl start iot-gateway

# Parar
sudo systemctl stop iot-gateway

# Reiniciar
sudo systemctl restart iot-gateway

# Status
sudo systemctl status iot-gateway

# Logs em tempo real
sudo journalctl -u iot-gateway -f

# Últimas 100 linhas de log
sudo journalctl -u iot-gateway -n 100
```

### Testar MQTT

```bash
# Subscrever a todos os tópicos de sensores
mosquitto_sub -h 192.168.0.194 -t "sensores/#" -v

# Publicar mensagem de teste
mosquitto_pub -h 192.168.0.194 -t "sensores/test" -m '{"sensor":"test","value":123}'
```

### Scripts Auxiliares

```bash
# Ver status do sistema
/opt/iot-gateway/check_status.sh

# Fazer backup manual
/opt/iot-gateway/backup.sh

# Monitorar recursos
glances
```

---

## 🐛 Solução de Problemas

### Serviço não inicia

```bash
# Ver logs detalhados
sudo journalctl -u iot-gateway -n 50

# Testar manualmente
cd /opt/iot-gateway
source venv/bin/activate
python backend/gateway/gateway.py
```

### Mosquitto não conecta

```bash
# Verificar se está rodando
sudo systemctl status mosquitto

# Ver se está escutando
sudo netstat -tulpn | grep 1883

# Testar localmente
mosquitto_pub -h localhost -t test -m "teste"
```

### Permissões

```bash
# Ajustar proprietário
sudo chown -R $USER:$USER /opt/iot-gateway

# Dar permissão de execução aos scripts
chmod +x /opt/iot-gateway/deploy/*.sh
chmod +x /opt/iot-gateway/*.sh
```

### Firewall bloqueando

```bash
# Verificar regras
sudo ufw status numbered

# Permitir porta MQTT
sudo ufw allow 1883/tcp

# Recarregar
sudo ufw reload
```

---

## 📊 Monitoramento

### Logs em Tempo Real

```bash
# Gateway
sudo journalctl -u iot-gateway -f

# Mosquitto
sudo tail -f /var/log/mosquitto/mosquitto.log

# Sistema
sudo tail -f /var/log/syslog
```

### Status do Sistema

```bash
# Script personalizado
/opt/iot-gateway/check_status.sh

# Monitoramento completo
glances

# Simples
htop
```

### Verificar Conectividade (do Windows)

```powershell
# Ping
ping 192.168.0.194

# Testar porta MQTT
Test-NetConnection -ComputerName 192.168.0.194 -Port 1883

# Testar MQTT (se tiver cliente instalado)
mosquitto_sub -h 192.168.0.194 -t "sensores/#" -v
```

---

## 📚 Documentação Adicional

- **Guia Completo**: `docs/SERVIDOR_UBUNTU_SETUP.md`
- **Documentação do Projeto**: `README.md`
- **Fase 2 - MQTT**: `docs/FASE2_MQTT.md`

---

## ⚙️ Configurações Importantes

### Localizações dos Arquivos

```
/opt/iot-gateway/              # Diretório principal
├── backend/                    # Código do backend
│   ├── gateway/               # Gateway MQTT
│   └── config/                # Configurações
├── sensores/                  # Simuladores de sensores
├── tests/                     # Testes
├── venv/                      # Ambiente virtual Python
├── deploy/                    # Scripts de deploy
│   ├── install_ubuntu.sh     # Instalação completa
│   ├── setup_service.sh      # Configurar systemd
│   └── deploy.sh             # Deploy/atualização
├── check_status.sh           # Verificar status
└── backup.sh                 # Backup manual

/etc/systemd/system/
└── iot-gateway.service       # Serviço systemd

/etc/mosquitto/
├── mosquitto.conf            # Config principal
└── conf.d/
    └── custom.conf           # Config personalizada

/var/log/mosquitto/
└── mosquitto.log             # Logs do Mosquitto

/opt/backups/iot-gateway/     # Backups automáticos
```

---

## 🔐 Segurança (Próximas Fases)

Para ambiente de produção, implementar:

- [ ] Autenticação MQTT (usuário/senha)
- [ ] TLS/SSL para MQTT
- [ ] Certificados SSL
- [ ] Firewall mais restritivo
- [ ] Fail2ban
- [ ] Backups automáticos agendados
- [ ] Monitoramento com alertas

---

## ✅ Checklist de Deploy

- [ ] Servidor Ubuntu 24.04 instalado
- [ ] Acesso SSH configurado
- [ ] Script `install_ubuntu.sh` executado
- [ ] Mosquitto instalado e rodando
- [ ] Código transferido para `/opt/iot-gateway`
- [ ] Dependências Python instaladas
- [ ] Configuração MQTT ajustada (192.168.0.194)
- [ ] Serviço systemd configurado
- [ ] Gateway iniciado e funcionando
- [ ] Testes MQTT realizados
- [ ] Firewall configurado
- [ ] Backup testado
- [ ] Documentação lida

---

**📅 Criado em**: 17 de Outubro de 2025  
**🎯 Projeto**: IoT Gateway - Fase 3  
**🖥️ Servidor**: Ubuntu 24.04 @ 192.168.0.194
