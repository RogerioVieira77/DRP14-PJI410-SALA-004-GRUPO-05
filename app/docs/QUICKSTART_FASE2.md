# ⚡ Quick Start - Fase 2: Gateway e MQTT

Guia rápido para testar o sistema completo de comunicação IoT.

---

## 🎯 Pré-requisitos

- Python 3.12+
- PowerShell (Windows)
- Conexão com internet (para instalar Mosquitto)

---

## 📦 Passo 1: Instalar Mosquitto MQTT Broker

### Opção A: Via Chocolatey (Recomendado)

```powershell
# Instalar Chocolatey (se ainda não tiver)
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Instalar Mosquitto
choco install mosquitto -y

# Iniciar serviço
net start mosquitto
```

### Opção B: Download Manual

1. Baixar: https://mosquitto.org/download/
2. Executar o instalador
3. Iniciar serviço:

```powershell
net start mosquitto
```

### Verificar Instalação

```powershell
# Verificar se está rodando
sc query mosquitto

# Ou testar conexão
mosquitto_sub -h localhost -t test
```

---

## 📦 Passo 2: Instalar Dependências Python

```powershell
# Navegar até a pasta do projeto
cd "C:\PI - IV - V1"

# Instalar pacotes
pip install -r backend\requirements-phase2.txt
```

**Pacotes instalados:**
- `paho-mqtt==1.6.1` - Cliente MQTT
- `python-dotenv==1.0.0` - Variáveis de ambiente

---

## 🚀 Passo 3: Executar Teste de Integração

```powershell
# Executar teste completo (60 segundos)
python tests\test_mqtt_integration.py
```

### O que o teste faz:

1. ✅ Cria 6 sensores (LoRa, ZigBee, Sigfox, RFID)
2. ✅ Inicia o Gateway
3. ✅ Inicia o Subscriber
4. ✅ Monitora por 60 segundos
5. ✅ Exibe estatísticas a cada 10 segundos
6. ✅ Valida comunicação
7. ✅ Exporta resultados para JSON

### Saída esperada:

```
==================== TESTE DE INTEGRAÇÃO - FASE 2 ====================

Criando sensores de teste...
✓ Criados 6 sensores

Iniciando Gateway...
✓ Gateway iniciado (gateway_001)

Iniciando Subscriber...
✓ Subscriber iniciado

Aguardando 3 segundos para estabilização...

========== INÍCIO DO MONITORAMENTO ==========

[00:10] Estatísticas:
  Gateway:
    - Leituras coletadas: 120
    - Leituras publicadas: 120
    - Alertas enviados: 0
    - Erros: 0
  
  Subscriber:
    - Leituras recebidas: 120
    - Status recebidos: 12
    - Alertas recebidos: 0
    - Erros: 0

[00:20] Estatísticas:
  Gateway:
    - Leituras coletadas: 240
    - Leituras publicadas: 240
...

========== FIM DO MONITORAMENTO ==========

Parando Gateway...
✓ Gateway parado

Parando Subscriber...
✓ Subscriber parado

==================== RESULTADOS FINAIS ====================
✅ Mensagens publicadas ≈ recebidas: 1200 ≈ 1200
✅ Taxa de sucesso: 100.0%
✅ Sem erros detectados

Dados exportados para: test_results_20251014_103000.json

==================== TESTE CONCLUÍDO COM SUCESSO! ====================
```

---

## 📊 Passo 4: Monitorar em Tempo Real

### Terminal 1: Subscriber de Sensores

```powershell
mosquitto_sub -h localhost -t "ceu/tres_pontes/sensores/#" -v
```

### Terminal 2: Status do Gateway

```powershell
mosquitto_sub -h localhost -t "ceu/tres_pontes/status" -v
```

### Terminal 3: Alertas

```powershell
mosquitto_sub -h localhost -t "ceu/tres_pontes/alertas" -v
```

### Exemplo de mensagens:

**Sensor:**
```
ceu/tres_pontes/sensores/LORA-12345 {"message_id": "gateway_001_1", "gateway_id": "gateway_001", "timestamp": "2025-10-14T10:30:00.123456", "sensor": {"serial_number": "LORA-12345", "protocol": "LoRa", "location": "Entrada Principal"}, "data": {"activity": 1, "timestamp": "2025-10-14T10:30:00", "total_detections": 42}, "metadata": {"rssi_dbm": -65.5, "battery_level": 98.5}}
```

**Status:**
```
ceu/tres_pontes/status {"gateway_id": "gateway_001", "timestamp": "2025-10-14T10:30:00", "status": "online", "details": {"sensors_connected": 6, "sensors_active": 2, "uptime_seconds": 3600}}
```

---

## 🛠️ Passo 5: Usar Programaticamente

### Exemplo 1: Gateway Simples

```python
from backend.gateway import Gateway
from sensores import LoRaSensor, ZigBeeSensor

# Criar gateway
gateway = Gateway()

# Registrar sensores
gateway.register_sensors([
    LoRaSensor(location="Entrada Principal"),
    ZigBeeSensor(location="Saída Norte")
])

# Iniciar (publicação automática)
gateway.start()

# Aguardar...
import time
time.sleep(60)

# Ver estatísticas
print(gateway.get_stats())

# Parar
gateway.stop()
```

### Exemplo 2: Subscriber Customizado

```python
from backend.gateway import MQTTSubscriber

# Criar subscriber
subscriber = MQTTSubscriber(client_id="meu_app")

# Callback para detecções
def on_pessoa_detectada(data):
    sensor = data['sensor']['location']
    if data['data']['activity'] == 1:
        print(f"🚶 Pessoa detectada em {sensor}!")

# Registrar callback
subscriber.set_callback('sensor', on_pessoa_detectada)

# Iniciar
subscriber.start()

# Aguardar...
import time
time.sleep(60)

# Ver dados coletados
recent = subscriber.get_recent_readings(limit=10)
for reading in recent:
    print(reading)

# Parar
subscriber.stop()
```

### Exemplo 3: Sistema Completo

```python
from backend.gateway import Gateway, MQTTSubscriber
from sensores import LoRaSensor, ZigBeeSensor, SigfoxSensor, RFIDSensor
import time

# Criar todos os sensores
sensores = [
    LoRaSensor(location="Entrada Principal"),
    LoRaSensor(location="Entrada Lateral"),
    ZigBeeSensor(location="Saída Norte"),
    ZigBeeSensor(location="Saída Sul"),
    SigfoxSensor(location="Banheiros"),
    RFIDSensor(location="Portaria")
]

# Gateway
gateway = Gateway(gateway_id="gateway_parque_001")
gateway.register_sensors(sensores)
gateway.start()

# Subscriber
subscriber = MQTTSubscriber(client_id="monitor_parque")

# Callbacks
def on_sensor_data(data):
    loc = data['sensor']['location']
    act = data['data']['activity']
    print(f"[{loc}] Atividade: {act}")

def on_alert(data):
    print(f"⚠️  ALERTA: {data['message']}")

subscriber.set_callback('sensor', on_sensor_data)
subscriber.set_callback('alert', on_alert)
subscriber.start()

# Rodar por 10 minutos
try:
    for i in range(10):
        time.sleep(60)
        print(f"\n=== Minuto {i+1}/10 ===")
        print("Gateway:", gateway.get_stats())
        print("Subscriber:", subscriber.get_stats())
except KeyboardInterrupt:
    print("\nInterrompido pelo usuário")

# Parar tudo
gateway.stop()
subscriber.stop()

# Exportar dados
subscriber.export_data("dados_parque.json")
print("✅ Dados exportados!")
```

---

## 🔧 Configuração Personalizada

### Editar: `backend/config/mqtt_config.ini`

```ini
[MQTT]
BROKER_HOST=localhost          # Endereço do broker
BROKER_PORT=1883               # Porta MQTT
QOS_LEVEL=1                    # Quality of Service (0, 1, 2)

[GATEWAY]
GATEWAY_ID=gateway_001         # ID único do gateway
PUBLISH_INTERVAL=2             # Segundos entre coletas
BATCH_SIZE=10                  # Leituras por lote

[TOPICS]
BASE_TOPIC=ceu/tres_pontes     # Tópico base

[LOGGING]
LOG_LEVEL=INFO                 # DEBUG, INFO, WARNING, ERROR
LOG_FILE=logs/gateway.log      # Arquivo de log
```

---

## 🐛 Troubleshooting

### Problema: "Connection refused [Errno 111]"

**Solução:**
```powershell
# Verificar se Mosquitto está rodando
sc query mosquitto

# Se não estiver, iniciar:
net start mosquitto
```

### Problema: "ModuleNotFoundError: No module named 'paho'"

**Solução:**
```powershell
pip install paho-mqtt
```

### Problema: Sensores não estão sendo detectados

**Solução:**
```powershell
# Verificar logs
type logs\gateway.log

# Aumentar nível de log para DEBUG
# Editar mqtt_config.ini:
# LOG_LEVEL=DEBUG
```

### Problema: Mensagens não chegam no Subscriber

**Solução:**
1. Verificar tópicos (case-sensitive)
2. Testar com mosquitto_sub:

```powershell
mosquitto_sub -h localhost -t "ceu/tres_pontes/#" -v
```

---

## 📚 Documentação Adicional

- **Documentação Completa Fase 2:** [`docs/FASE2_MQTT.md`](docs/FASE2_MQTT.md)
- **Guia de Instalação Mosquitto:** [`docs/MOSQUITTO_SETUP.md`](docs/MOSQUITTO_SETUP.md)
- **Roadmap do Projeto:** [`docs/ROADMAP.md`](docs/ROADMAP.md)

---

## ✅ Checklist de Sucesso

- [ ] Mosquitto instalado e rodando
- [ ] Dependências Python instaladas
- [ ] Teste de integração executado com sucesso
- [ ] Mensagens visíveis no mosquitto_sub
- [ ] Gateway e Subscriber funcionando
- [ ] Logs sendo gerados em `logs/gateway.log`
- [ ] Sem erros no console

---

## 🎉 Próximos Passos

Após confirmar que a Fase 2 está funcionando:

1. **Fase 3:** Backend Flask + MySQL
2. **Fase 4:** Frontend Web (Dashboard)
3. **Fase 5:** Integração PowerBI
4. **Fase 6:** Containerização (Docker)

---

**Precisa de ajuda?** Consulte a documentação completa ou os logs do sistema!

---

**Última atualização:** Outubro 2025  
**Versão:** 2.0.0
