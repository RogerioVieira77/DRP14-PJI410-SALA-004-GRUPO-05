# Deploy - Estrutura Atualizada com Repositório Git

## ✅ Status Atual

- **Servidor:** 192.168.0.194
- **Python venv:** `/opt/iot-gateway/venv` ✅
- **Mosquitto MQTT:** Rodando na porta 1883 ✅
- **Firewall UFW:** Configurado ✅
- **Repositório clonado:** `/opt/iot-gateway/PI---IV---V1/` ✅

## 📁 Estrutura de Diretórios

```
/opt/iot-gateway/
├── venv/                          # Ambiente virtual Python (criado manualmente)
└── PI---IV---V1/                  # Repositório Git clonado
    ├── backend/
    │   ├── gateway/
    │   │   ├── gateway.py
    │   │   ├── mqtt_client.py
    │   │   └── ...
    │   ├── config/
    │   │   └── mqtt_config.ini    # 👈 PRECISA CONFIGURAR
    │   └── requirements-phase2.txt
    ├── frontend/
    ├── sensores/
    │   ├── lora_sensor.py
    │   ├── zigbee_sensor.py
    │   └── ...
    ├── tests/
    │   ├── test_mqtt_integration.py
    │   └── test_simuladores.py
    ├── config/
    ├── docs/
    ├── deploy/                     # Scripts de deploy
    │   ├── setup_service.sh        # 👈 ATUALIZADO
    │   └── deploy.sh               # 👈 ATUALIZADO
    └── requirements.txt
```

---

## 🚀 Passo 7: Deploy da Aplicação

### 7.1 ✅ Repositório Já Clonado

Você já clonou o repositório! A estrutura está em:
```bash
/opt/iot-gateway/PI---IV---V1/
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

# Instalar dependências MQTT (Fase 2)
pip install -r backend/requirements-phase2.txt

# Verificar instalações importantes
pip list | grep -E "paho-mqtt|configparser"
```

**Saída esperada:**
```
paho-mqtt    x.x.x
```

### 7.3 Configurar MQTT para o Servidor

```bash
# Editar configuração MQTT
nano /opt/iot-gateway/PI---IV---V1/backend/config/mqtt_config.ini
```

**Conteúdo do arquivo (ajustar `broker_host`):**

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

**Salvar:** `Ctrl+O`, `Enter`, `Ctrl+X`

### 7.4 Testar Aplicação Manualmente

#### Terminal 1 - Gateway MQTT

```bash
# Ativar venv e navegar
cd /opt/iot-gateway
source venv/bin/activate
cd PI---IV---V1

# Executar gateway
python backend/gateway/gateway.py
```

**Saída esperada:**
```
🚀 Gateway MQTT Iniciado
📡 Conectado ao broker: 192.168.0.194:1883
📥 Inscrito em: sensores/#
⏳ Aguardando mensagens...
```

#### Terminal 2 - Simulador de Sensores (Abrir nova sessão SSH)

```bash
# Ativar venv e navegar
cd /opt/iot-gateway
source venv/bin/activate
cd PI---IV---V1

# Executar teste de integração
python tests/test_mqtt_integration.py
```

**Saída esperada:**
```
📡 Enviando dados LoRa...
📡 Enviando dados Zigbee...
📡 Enviando dados Sigfox...
📡 Enviando dados RFID...
✅ Teste concluído!
```

#### Terminal 3 - Subscriber de Teste (Opcional)

```bash
# Monitorar todos os tópicos
mosquitto_sub -h 192.168.0.194 -t 'sensores/#' -v
```

**Saída esperada (quando executar os testes):**
```
sensores/lora/dados {"temperatura": 25.3, "umidade": 60.2, ...}
sensores/zigbee/dados {"potencia": 120.5, "tensao": 220.0, ...}
...
```

---

## 🔧 Passo 8: Configurar Serviço Systemd

### 8.1 Usar Script Automatizado (RECOMENDADO)

Os scripts foram atualizados para a nova estrutura de diretórios:

```bash
# Navegar para os scripts
cd /opt/iot-gateway/PI---IV---V1/deploy

# Dar permissão de execução
chmod +x setup_service.sh

# Executar com sudo
sudo ./setup_service.sh
```

**O que o script faz:**
- ✅ Cria `/etc/systemd/system/iot-gateway.service`
- ✅ Configura `WorkingDirectory=/opt/iot-gateway/PI---IV---V1`
- ✅ Usa venv correto: `/opt/iot-gateway/venv/bin/python`
- ✅ Configura auto-restart em caso de falha
- ✅ Habilita inicialização automática

### 8.2 Verificar Serviço

```bash
# Verificar status
sudo systemctl status iot-gateway

# Ver logs em tempo real
sudo journalctl -u iot-gateway -f

# Parar serviço
sudo systemctl stop iot-gateway

# Iniciar serviço
sudo systemctl start iot-gateway

# Reiniciar serviço
sudo systemctl restart iot-gateway
```

---

## 🧪 Passo 9: Testes de Integração

### 9.1 Teste do Windows (Cliente MQTT)

**Instalar cliente MQTT no Windows:**

```powershell
# Opção 1: MQTT Explorer (GUI)
# Baixar: https://mqtt-explorer.com/

# Opção 2: Mosquitto CLI
# Baixar: https://mosquitto.org/download/
```

**Testar publicação do Windows:**

```powershell
# Publicar mensagem de teste
mosquitto_pub -h 192.168.0.194 -t "sensores/teste" -m "Teste do Windows"

# Subscrever em todos os tópicos
mosquitto_sub -h 192.168.0.194 -t "sensores/#" -v
```

### 9.2 Teste do Servidor

```bash
# Terminal 1: Subscriber
mosquitto_sub -h 192.168.0.194 -t 'sensores/#' -v

# Terminal 2: Publisher
cd /opt/iot-gateway
source venv/bin/activate
cd PI---IV---V1
python tests/test_mqtt_integration.py
```

---

## 📊 Passo 10: Monitoramento

### 10.1 Criar Script de Monitoramento

```bash
# Criar script
nano /opt/iot-gateway/check_status.sh
```

**Conteúdo:**

```bash
#!/bin/bash

echo "===================="
echo "Status do IoT Gateway"
echo "===================="
echo ""

echo "🔹 Serviço IoT Gateway:"
sudo systemctl status iot-gateway --no-pager | grep Active

echo ""
echo "🔹 Mosquitto MQTT:"
sudo systemctl status mosquitto --no-pager | grep Active

echo ""
echo "🔹 Portas abertas:"
sudo netstat -tlnp | grep -E "1883|8000"

echo ""
echo "🔹 Últimas 10 linhas do log:"
sudo journalctl -u iot-gateway -n 10 --no-pager

echo ""
echo "🔹 Uso de memória:"
ps aux | grep -E "python|mosquitto" | grep -v grep
```

**Dar permissão:**

```bash
chmod +x /opt/iot-gateway/check_status.sh
```

**Executar:**

```bash
/opt/iot-gateway/check_status.sh
```

### 10.2 Monitoramento em Tempo Real

```bash
# Ver logs do gateway
sudo journalctl -u iot-gateway -f

# Ver logs do mosquitto
sudo tail -f /var/log/mosquitto/mosquitto.log

# Ver conexões ativas
watch -n 2 'sudo netstat -anp | grep 1883'

# Monitor de recursos
htop
```

---

## 🔄 Deploy de Atualizações

### Quando fizer alterações no código:

```bash
# Navegar para o projeto
cd /opt/iot-gateway/PI---IV---V1

# Pull do Git
git pull origin main

# Atualizar dependências (se necessário)
source /opt/iot-gateway/venv/bin/activate
pip install -r requirements.txt
pip install -r backend/requirements-phase2.txt

# Reiniciar serviço
sudo systemctl restart iot-gateway

# Ver logs
sudo journalctl -u iot-gateway -f
```

### Ou usar o script automatizado:

```bash
cd /opt/iot-gateway/PI---IV---V1/deploy
sudo ./deploy.sh
```

---

## 📝 Checklist Final

- [ ] Python venv ativado e funcionando
- [ ] Mosquitto rodando na porta 1883
- [ ] Firewall configurado (portas 22, 1883, 8000)
- [ ] Repositório clonado em `/opt/iot-gateway/PI---IV---V1/`
- [ ] Dependências Python instaladas
- [ ] `mqtt_config.ini` configurado com IP 192.168.0.194
- [ ] Gateway executando manualmente (teste)
- [ ] Testes de integração funcionando
- [ ] Serviço systemd configurado
- [ ] Gateway iniciando automaticamente
- [ ] Teste de conexão do Windows funcionando
- [ ] Logs sendo gerados corretamente

---

## 🆘 Troubleshooting Rápido

### Gateway não inicia

```bash
# Ver erro específico
sudo journalctl -u iot-gateway -n 50 --no-pager

# Testar manualmente
cd /opt/iot-gateway
source venv/bin/activate
cd PI---IV---V1
python backend/gateway/gateway.py
```

### Não consegue publicar do Windows

```bash
# Verificar se Mosquitto está escutando em todas as interfaces
sudo netstat -tlnp | grep 1883

# Deve mostrar: 0.0.0.0:1883 (não 127.0.0.1:1883)

# Se não estiver, editar:
sudo nano /etc/mosquitto/conf.d/custom.conf

# Adicionar:
listener 1883 0.0.0.0
```

### Mensagens não chegam ao Gateway

```bash
# Verificar tópicos inscritos
mosquitto_sub -h 192.168.0.194 -t 'sensores/#' -v

# Ver logs do Mosquitto
sudo tail -f /var/log/mosquitto/mosquitto.log

# Ver se gateway está conectado
mosquitto_sub -h 192.168.0.194 -t '$SYS/broker/clients/connected' -v
```

---

## 🎯 Próximos Passos (Fase 3)

Após confirmar que tudo está funcionando:

1. ✅ Implementar API REST (FastAPI/Flask)
2. ✅ Adicionar banco de dados (SQLite/PostgreSQL)
3. ✅ Criar dashboard frontend
4. ✅ Implementar autenticação MQTT
5. ✅ Adicionar SSL/TLS
6. ✅ Configurar backup automático

---

**Data de Atualização:** 18/10/2025  
**Estrutura:** `/opt/iot-gateway/PI---IV---V1/`  
**Documentos atualizados:**
- ✅ `SERVIDOR_UBUNTU_SETUP.md`
- ✅ `deploy/setup_service.sh`
- ✅ `deploy/deploy.sh`
