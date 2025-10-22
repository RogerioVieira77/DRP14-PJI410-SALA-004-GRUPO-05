# ⚡ Quick Start - Deploy Servidor Ubuntu

## 🎯 Objetivo
Configurar servidor Ubuntu 24.04 (192.168.0.194) como ambiente de testes para IoT Gateway.

---

## 📝 Pré-requisitos

- ✅ Servidor Ubuntu 24.04 instalado
- ✅ IP: 192.168.0.194
- ✅ Acesso SSH configurado
- ✅ Usuário com privilégios sudo

---

## 🚀 Instalação em 5 Passos

### 1️⃣ Conectar ao Servidor

**Do Windows (PowerShell):**
```powershell
ssh usuario@192.168.0.194
```

---

### 2️⃣ Executar Script de Instalação

**No Servidor Ubuntu:**
```bash
# Baixar ou criar o script
cd /tmp

# Se tiver o script localmente, transfira do Windows:
# scp deploy/install_ubuntu.sh usuario@192.168.0.194:/tmp/

# Dar permissão de execução
chmod +x install_ubuntu.sh

# Executar
./install_ubuntu.sh
```

**⏱️ Tempo:** ~10-15 minutos

**O que será instalado:**
- ✅ Atualizações do sistema
- ✅ Python 3.x + pip
- ✅ Eclipse Mosquitto (MQTT)
- ✅ Firewall configurado
- ✅ Ferramentas de monitoramento

---

### 3️⃣ Transferir Código

**Opção A - Via Git (Recomendado):**
```bash
cd /opt/iot-gateway
git clone https://github.com/RogerioVieira77/PI---IV---V1.git .
```

**Opção B - Via SCP do Windows:**
```powershell
cd "c:\PI - IV - V1"
scp -r . usuario@192.168.0.194:/opt/iot-gateway/
```

---

### 4️⃣ Instalar Dependências Python

```bash
cd /opt/iot-gateway
source venv/bin/activate
pip install -r requirements.txt
pip install -r backend/requirements-phase2.txt
```

---

### 5️⃣ Configurar e Iniciar

```bash
# Editar configuração MQTT
nano backend/config/mqtt_config.ini
# Ajustar: broker_host = 192.168.0.194

# Configurar serviço systemd
chmod +x deploy/setup_service.sh
./deploy/setup_service.sh

# Iniciar serviço
sudo systemctl start iot-gateway
```

---

## ✅ Testar

### Verificar Status

```bash
sudo systemctl status iot-gateway
sudo systemctl status mosquitto
```

### Testar MQTT

**Terminal 1 - Subscriber:**
```bash
mosquitto_sub -h 192.168.0.194 -t "sensores/#" -v
```

**Terminal 2 - Publisher:**
```bash
mosquitto_pub -h 192.168.0.194 -t "sensores/test" -m '{"test":123}'
```

---

## 🔄 Atualizar Código (Deploy)

Quando modificar o código:

```bash
cd /opt/iot-gateway
./deploy/deploy.sh
```

---

## 📊 Monitoramento

```bash
# Status do sistema
/opt/iot-gateway/check_status.sh

# Logs em tempo real
sudo journalctl -u iot-gateway -f

# Recursos do sistema
glances
```

---

## 🆘 Comandos Úteis

### Gerenciar Serviço
```bash
sudo systemctl start iot-gateway    # Iniciar
sudo systemctl stop iot-gateway     # Parar
sudo systemctl restart iot-gateway  # Reiniciar
sudo systemctl status iot-gateway   # Status
```

### Ver Logs
```bash
sudo journalctl -u iot-gateway -f         # Tempo real
sudo journalctl -u iot-gateway -n 100     # Últimas 100 linhas
sudo tail -f /var/log/mosquitto/mosquitto.log  # Mosquitto
```

### Testar do Windows
```powershell
# Ping
ping 192.168.0.194

# Testar porta MQTT
Test-NetConnection -ComputerName 192.168.0.194 -Port 1883
```

---

## 📚 Documentação Completa

- **Guia Detalhado**: `docs/SERVIDOR_UBUNTU_SETUP.md`
- **Scripts Deploy**: `deploy/README.md`
- **Fase 2 MQTT**: `docs/FASE2_MQTT.md`

---

## 🐛 Problemas Comuns

### Serviço não inicia
```bash
sudo journalctl -u iot-gateway -n 50
```

### Mosquitto não conecta
```bash
sudo systemctl restart mosquitto
sudo netstat -tulpn | grep 1883
```

### Firewall bloqueando
```bash
sudo ufw allow 1883/tcp
sudo ufw reload
```

---

**✨ Pronto! Ambiente de testes configurado!**

**Próximos passos**: Ver `docs/SERVIDOR_UBUNTU_SETUP.md` para configurações avançadas.
