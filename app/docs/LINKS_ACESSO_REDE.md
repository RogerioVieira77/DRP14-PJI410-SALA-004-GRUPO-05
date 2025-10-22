# 🌐 Links de Acesso via Rede Local

**IP da Máquina:** `192.168.0.254`  
**Data:** 20 de Outubro de 2025

---

## 📱 Páginas Web (Porta 8000)

### 📍 Página Principal - SMARTCEU
```
http://192.168.0.254:8000/smart_ceu.html
```

### 📚 Documentação da Arquitetura
```
http://192.168.0.254:8000/docs-web/doc_arq.html
```

### 🧪 Página de Teste da API
```
http://192.168.0.254:8000/test_page.html
```

---

## 🔌 API REST (Flask - Porta 5000)

### ❤️ Health Check
```
GET http://192.168.0.254:5000/health
```

### 🔐 Autenticação

**Login:**
```
POST http://192.168.0.254:5000/api/v1/auth/login
Body: {"username": "admin", "password": "admin123"}
```

**Registrar Usuário:**
```
POST http://192.168.0.254:5000/api/v1/auth/register
```

**Perfil do Usuário:**
```
GET http://192.168.0.254:5000/api/v1/auth/me
Header: Authorization: Bearer {token}
```

### 📡 Sensores

**Listar Sensores:**
```
GET http://192.168.0.254:5000/api/v1/sensors
Header: Authorization: Bearer {token}
```

**Obter Sensor Específico:**
```
GET http://192.168.0.254:5000/api/v1/sensors/{id}
Header: Authorization: Bearer {token}
```

**Criar Sensor:**
```
POST http://192.168.0.254:5000/api/v1/sensors
Header: Authorization: Bearer {token}
```

**Atualizar Sensor:**
```
PUT http://192.168.0.254:5000/api/v1/sensors/{id}
Header: Authorization: Bearer {token}
```

**Deletar Sensor:**
```
DELETE http://192.168.0.254:5000/api/v1/sensors/{id}
Header: Authorization: Bearer {token}
```

### 📊 Leituras

**Listar Leituras:**
```
GET http://192.168.0.254:5000/api/v1/readings
Query params: ?sensor_id=1&start_date=2025-10-01&limit=100
Header: Authorization: Bearer {token}
```

**Criar Leitura:**
```
POST http://192.168.0.254:5000/api/v1/readings
Header: Authorization: Bearer {token}
Body: {
  "sensor_id": 1,
  "activity": 1,
  "timestamp": "2025-10-20T10:30:00",
  "sensor_metadata": {"battery_level": 85}
}
```

**Criar Leituras em Lote:**
```
POST http://192.168.0.254:5000/api/v1/readings/bulk
Header: Authorization: Bearer {token}
```

**Obter Leitura Específica:**
```
GET http://192.168.0.254:5000/api/v1/readings/{id}
Header: Authorization: Bearer {token}
```

### 📈 Estatísticas

**Visão Geral:**
```
GET http://192.168.0.254:5000/api/v1/statistics/overview
Header: Authorization: Bearer {token}
```

**Atividade por Período:**
```
GET http://192.168.0.254:5000/api/v1/statistics/activity
Query params: ?start_date=2025-10-01&end_date=2025-10-20
Header: Authorization: Bearer {token}
```

**Estatísticas por Sensor:**
```
GET http://192.168.0.254:5000/api/v1/statistics/sensors
Header: Authorization: Bearer {token}
```

**Estatísticas de Capacidade:**
```
GET http://192.168.0.254:5000/api/v1/statistics/capacity
Header: Authorization: Bearer {token}
```

---

## 📡 MQTT Broker (Mosquitto - Porta 1883)

**Conexão:**
```
Host: 192.168.0.254
Port: 1883
```

**Topics:**
```
sensores/lora/dados
sensores/zigbee/dados
sensores/sigfox/dados
sensores/rfid/dados
```

**Exemplo de Subscrição (Python):**
```python
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("192.168.0.254", 1883, 60)
client.subscribe("sensores/+/dados")
client.loop_forever()
```

---

## ⚙️ Como Iniciar os Serviços

### 1️⃣ Servidor HTTP para Páginas Web

```powershell
cd "C:\PI - IV - V1"
python -m http.server 8000
```

Acesse: `http://192.168.0.254:8000/smart_ceu.html`

### 2️⃣ API Flask (Backend)

```powershell
cd "C:\PI - IV - V1\backend"
venv\Scripts\activate
python app.py
```

API disponível em: `http://192.168.0.254:5000`

### 3️⃣ MQTT Broker (Mosquitto)

```powershell
mosquitto -v
```

Broker disponível em: `192.168.0.254:1883`

### 4️⃣ Gateway MQTT (Opcional)

```powershell
cd "C:\PI - IV - V1"
venv\Scripts\activate
python backend/gateway/gateway.py
```

---

## 📱 Acessando de Outros Dispositivos

### Smartphones/Tablets
1. Conecte o dispositivo à **mesma rede Wi-Fi**
2. Abra o navegador
3. Digite: `http://192.168.0.254:8000/smart_ceu.html`

### Outros Computadores
1. Conecte à **mesma rede**
2. Abra qualquer navegador
3. Digite: `http://192.168.0.254:8000/smart_ceu.html`

### Ferramentas de Teste de API
- **Postman:** Importe os endpoints acima
- **Insomnia:** Configure base URL como `http://192.168.0.254:5000`
- **cURL:** Use os comandos direto no terminal

---

## 🔒 Firewall do Windows

Se não conseguir acessar de outros dispositivos, libere as portas:

```powershell
# Liberar porta 8000 (HTTP Server)
New-NetFirewallRule -DisplayName "Python HTTP Server" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow

# Liberar porta 5000 (Flask API)
New-NetFirewallRule -DisplayName "Flask API" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow

# Liberar porta 1883 (MQTT)
New-NetFirewallRule -DisplayName "MQTT Broker" -Direction Inbound -LocalPort 1883 -Protocol TCP -Action Allow
```

---

## 📊 Status dos Serviços

| Serviço | Porta | Status | URL |
|---------|-------|--------|-----|
| Páginas Web | 8000 | ⚠️ Requer python -m http.server | http://192.168.0.254:8000 |
| API Flask | 5000 | ✅ Rodando | http://192.168.0.254:5000 |
| MQTT Broker | 1883 | ✅ Rodando | 192.168.0.254:1883 |
| MySQL | 3306 | ✅ Local | localhost:3306 |

---

## 🎯 Link Rápido Principal

**Para compartilhar com outros usuários:**

```
🏠 Acesse o SMARTCEU:
http://192.168.0.254:8000/smart_ceu.html

👤 Login:
Usuário: admin
Senha: admin123
```

---

**Última atualização:** 20 de Outubro de 2025  
**Versão:** 2.0.0 - Fase 3 Completa + Refatoração
