# 🦟 Guia de Instalação do Mosquitto MQTT Broker
## Sistema CEU Tres Pontes - Fase 2

---

## 📋 Sobre o Mosquitto

Mosquitto é um broker MQTT open-source, leve e amplamente utilizado para comunicação IoT.

**Site Oficial:** https://mosquitto.org/

---

## 🪟 Instalação no Windows

### Método 1: Instalador Oficial (Recomendado)

1. **Download:**
   - Acesse: https://mosquitto.org/download/
   - Baixe o instalador Windows (64-bit)
   - Versão recomendada: 2.0.18 ou superior

2. **Instalação:**
   ```powershell
   # Execute o instalador baixado
   # Siga o assistente de instalação
   # Instalar em: C:\Program Files\mosquitto
   ```

3. **Configuração:**
   ```powershell
   # Editar arquivo de configuração
   notepad "C:\Program Files\mosquitto\mosquitto.conf"
   ```

   Adicione as seguintes linhas:
   ```conf
   # Porta padrão
   listener 1883
   
   # Permitir conexões anônimas (apenas para desenvolvimento!)
   allow_anonymous true
   
   # Log
   log_dest file C:\Program Files\mosquitto\mosquitto.log
   log_type all
   ```

4. **Iniciar Serviço:**
   ```powershell
   # Como Administrador
   net start mosquitto
   
   # Ou iniciar manualmente
   cd "C:\Program Files\mosquitto"
   mosquitto.exe -c mosquitto.conf -v
   ```

### Método 2: Chocolatey

```powershell
# Instalar Chocolatey (se não tiver)
# Ver: https://chocolatey.org/install

# Instalar Mosquitto
choco install mosquitto -y

# Iniciar serviço
net start mosquitto
```

### Método 3: Docker (Alternativa)

```powershell
# Iniciar Mosquitto em container
docker run -d --name mosquitto `
  -p 1883:1883 `
  -p 9001:9001 `
  eclipse-mosquitto:latest

# Ver logs
docker logs -f mosquitto
```

---

## 🐧 Instalação no Linux (Ubuntu)

### Via APT (Recomendado)

```bash
# Atualizar repositórios
sudo apt update

# Instalar Mosquitto
sudo apt install -y mosquitto mosquitto-clients

# Iniciar serviço
sudo systemctl start mosquitto

# Habilitar na inicialização
sudo systemctl enable mosquitto

# Verificar status
sudo systemctl status mosquitto
```

### Configuração

```bash
# Editar configuração
sudo nano /etc/mosquitto/mosquitto.conf

# Adicionar:
listener 1883
allow_anonymous true

# Reiniciar serviço
sudo systemctl restart mosquitto
```

---

## ✅ Verificar Instalação

### Teste de Conexão

```powershell
# Terminal 1: Subscriber
mosquitto_sub -h localhost -t "test/topic" -v

# Terminal 2: Publisher
mosquitto_pub -h localhost -t "test/topic" -m "Hello MQTT!"
```

Se aparecer "Hello MQTT!" no Terminal 1, está funcionando! ✅

### Teste com Python

```python
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Conectado! Código: {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.connect("localhost", 1883, 60)
client.loop_start()

input("Pressione ENTER para sair...")
```

---

## 🔒 Configuração de Segurança (Produção)

### Criar Usuário e Senha

```bash
# Linux
sudo mosquitto_passwd -c /etc/mosquitto/passwd ceu_tres_pontes

# Windows
cd "C:\Program Files\mosquitto"
mosquitto_passwd.exe -c passwd.txt ceu_tres_pontes
```

### Editar Configuração

```conf
# Desabilitar anônimos
allow_anonymous false

# Arquivo de senhas
password_file C:\Program Files\mosquitto\passwd.txt
```

---

## 📊 Monitoramento

### Ver Logs

```powershell
# Windows
type "C:\Program Files\mosquitto\mosquitto.log"

# Linux
sudo tail -f /var/log/mosquitto/mosquitto.log
```

### Verificar Porta

```powershell
# Windows
netstat -an | findstr :1883

# Linux
netstat -tulpn | grep 1883
```

---

## 🛠️ Comandos Úteis

### Mosquitto CLI

```bash
# Publicar mensagem
mosquitto_pub -h localhost -t "ceu/sensores/test" -m '{"test": true}'

# Subscrever tópico
mosquitto_sub -h localhost -t "ceu/sensores/#" -v

# Subscrever todos os tópicos
mosquitto_sub -h localhost -t "#" -v

# Com autenticação
mosquitto_sub -h localhost -t "test" -u ceu_tres_pontes -P senha
```

### Gerenciar Serviço (Windows)

```powershell
# Iniciar
net start mosquitto

# Parar
net stop mosquitto

# Reiniciar
net stop mosquitto; net start mosquitto

# Status
sc query mosquitto
```

### Gerenciar Serviço (Linux)

```bash
# Iniciar
sudo systemctl start mosquitto

# Parar
sudo systemctl stop mosquitto

# Reiniciar
sudo systemctl restart mosquitto

# Status
sudo systemctl status mosquitto

# Logs em tempo real
sudo journalctl -u mosquitto -f
```

---

## 🐛 Troubleshooting

### Erro: "Address already in use"

```powershell
# Verificar o que está usando a porta 1883
netstat -ano | findstr :1883

# Matar processo (substitua PID)
taskkill /PID <PID> /F
```

### Erro: "Connection refused"

1. Verificar se o serviço está rodando
2. Verificar firewall
3. Verificar se a porta está correta no código

### Erro: "Not authorized"

1. Verificar usuário e senha no código
2. Verificar arquivo de senhas
3. Verificar `allow_anonymous` na configuração

---

## 📦 Instalar Cliente Python

```powershell
# Instalar paho-mqtt
pip install paho-mqtt

# Ou usar o requirements
pip install -r backend\requirements-phase2.txt
```

---

## 🔥 Firewall (se necessário)

### Windows

```powershell
# Abrir porta 1883
netsh advfirewall firewall add rule name="Mosquitto MQTT" dir=in action=allow protocol=TCP localport=1883
```

### Linux

```bash
# UFW
sudo ufw allow 1883/tcp

# Firewalld
sudo firewall-cmd --permanent --add-port=1883/tcp
sudo firewall-cmd --reload
```

---

## 📚 Recursos Adicionais

### Documentação

- **Mosquitto Docs:** https://mosquitto.org/documentation/
- **MQTT Protocol:** https://mqtt.org/
- **Paho Python:** https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php

### Ferramentas de Teste

- **MQTT Explorer:** http://mqtt-explorer.com/ (GUI para explorar tópicos)
- **MQTT.fx:** https://mqttfx.jensd.de/ (Cliente MQTT desktop)
- **HiveMQ WebSocket Client:** http://www.hivemq.com/demos/websocket-client/

---

## ✅ Checklist de Instalação

- [ ] Mosquitto instalado
- [ ] Serviço iniciado
- [ ] Porta 1883 aberta
- [ ] Teste de pub/sub funcionando
- [ ] Paho-mqtt instalado no Python
- [ ] Configuração ajustada conforme necessidade
- [ ] Logs acessíveis

---

## 🚀 Próximos Passos

Após instalar o Mosquitto:

1. **Testar Gateway:**
   ```powershell
   cd backend\gateway
   python gateway.py
   ```

2. **Testar Subscriber:**
   ```powershell
   cd backend\gateway
   python mqtt_subscriber.py
   ```

3. **Executar sistema completo:**
   ```powershell
   cd tests
   python test_mqtt_integration.py
   ```

---

**Última atualização:** Outubro 2025  
**Suporte:** Documentação do projeto CEU Tres Pontes
