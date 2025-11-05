# 📊 MAPEAMENTO DE DADOS - SISTEMA SMARTCEU

## 📡 Visão Geral do Sistema de Sensores

Este documento detalha como os dados fluem desde os sensores IoT até os indicadores no Dashboard.

---

## 🗄️ ESTRUTURA DAS TABELAS DO BANCO DE DADOS

### 1️⃣ Tabela: `sensors`
Armazena informações cadastrais e de status dos sensores físicos.

| Campo              | Tipo         | NULL | Descrição                                    |
|--------------------|--------------|------|----------------------------------------------|
| `id`               | INTEGER      | NOT NULL (PK) | Identificador único do sensor         |
| `serial_number`    | VARCHAR(50)  | NOT NULL | Número de série único (ex: LORA-A1B2C3D4) |
| `protocol`         | VARCHAR(20)  | NOT NULL | Protocolo de comunicação (LoRa/Zigbee/Sigfox/RFID) |
| `location`         | VARCHAR(100) | NOT NULL | Localização física do sensor          |
| `description`      | TEXT         | NULL | Descrição adicional do sensor                |
| `status`           | VARCHAR(11)  | NOT NULL | Status operacional (active/inactive/maintenance/error) |
| `protocol_config`  | JSON         | NULL | Configurações específicas do protocolo       |
| `firmware_version` | VARCHAR(20)  | NULL | Versão do firmware do sensor                 |
| `battery_level`    | FLOAT        | NULL | Nível de bateria em % (0-100)               |
| `signal_strength`  | FLOAT        | NULL | Força do sinal em dBm (ex: -60)             |
| `total_readings`   | INTEGER      | NULL | Contador total de leituras                  |
| `last_reading_at`  | DATETIME     | NULL | Timestamp da última leitura recebida        |
| `created_at`       | DATETIME     | NOT NULL | Data de criação do registro          |
| `updated_at`       | DATETIME     | NOT NULL | Data da última atualização           |

**Índices:**
- `idx_protocol_status` (protocol, status)
- `idx_status_created` (status, created_at)

---

### 2️⃣ Tabela: `readings`
Armazena cada leitura individual dos sensores de presença/movimento.

| Campo              | Tipo         | NULL | Descrição                                    |
|--------------------|--------------|------|----------------------------------------------|
| `id`               | BIGINT       | NOT NULL (PK) | Identificador único da leitura        |
| `sensor_id`        | INTEGER      | NOT NULL (FK) | Referência ao sensor (sensors.id)     |
| `activity`         | SMALLINT     | NOT NULL | Atividade detectada (0=nada, 1=presença) |
| `timestamp`        | DATETIME     | NOT NULL | Momento exato da leitura              |
| `sensor_metadata`  | JSON         | NULL | Metadados adicionais (bateria, RSSI, temperatura) |
| `message_id`       | VARCHAR(100) | NULL | ID da mensagem MQTT                          |
| `gateway_id`       | VARCHAR(50)  | NULL | ID do gateway que recebeu a mensagem        |
| `created_at`       | DATETIME     | NOT NULL | Timestamp de inserção no banco       |

**Índices:**
- `idx_sensor_timestamp` (sensor_id, timestamp)
- `idx_timestamp_activity` (timestamp, activity)
- `idx_sensor_activity` (sensor_id, activity)
- `idx_gateway_timestamp` (gateway_id, timestamp)

**Exemplo de `sensor_metadata`:**
```json
{
  "battery_level": 95.0,
  "rssi_dbm": -55.0,
  "temperature": 26.5,
  "humidity": 65.0
}
```

---

### 3️⃣ Tabela: `pool_readings`
Armazena leituras específicas dos sensores de monitoramento da piscina.

| Campo            | Tipo           | NULL | Descrição                                |
|------------------|----------------|------|------------------------------------------|
| `id`             | BIGINT         | NOT NULL (PK) | Identificador único da leitura   |
| `sensor_type`    | VARCHAR(20)    | NOT NULL | Tipo do sensor (water_temp/ambient_temp/water_quality) |
| `reading_date`   | DATE           | NOT NULL | Data da leitura                  |
| `reading_time`   | TIME           | NOT NULL | Hora da leitura                  |
| `temperature`    | NUMERIC(5,2)   | NULL | Temperatura em Celsius (20-40°C)        |
| `water_quality`  | VARCHAR(20)    | NULL | Qualidade da água (Ótima/Boa/Regular/Imprópria) |
| `created_at`     | DATETIME       | NOT NULL | Timestamp de criação             |
| `updated_at`     | DATETIME       | NOT NULL | Timestamp de atualização         |

**Tipos de Sensores:**
- `water_temp` → Temperatura da água da piscina
- `ambient_temp` → Temperatura ambiente da área da piscina
- `water_quality` → Qualidade da água (pH, cloro, alcalinidade)

---

## 📊 SENSORES CADASTRADOS NO SISTEMA

| ID | Serial Number   | Protocolo | Localização        | Bateria | Sinal    | Total Leituras | Total Detecções |
|----|-----------------|-----------|--------------------|---------|---------:|---------------:|----------------:|
| 1  | LORA-A1B2C3D4   | LoRa      | Entrada Principal  | 100%    | -60 dBm  | 5.464          | 2.308           |
| 2  | ZIGB-E5F6G7H8   | Zigbee    | Quadra Esportiva   | 95%     | -55 dBm  | 5.610          | 2.541           |
| 3  | SIGF-I9J0K1L2   | Sigfox    | Playground         | 88%     | -70 dBm  | 5.891          | 2.191           |
| 4  | RFID-M3N4O5P6   | RFID      | Biblioteca         | N/A     | N/A      | 5.357          | 2.557           |
| 5  | LORA-Q7R8S9T0   | LoRa      | Área da Piscina    | 92%     | -65 dBm  | 5.254          | 2.761           |
| 6  | ZIGB-U1V2W3X4   | Zigbee    | Saída Lateral      | 90%     | -58 dBm  | 5.608          | 2.600           |

**Total Geral:** 33.184 leituras | 14.958 detecções (45.08% taxa de detecção)

---

## 🔄 FLUXO DE DADOS: SENSOR → BANCO → DASHBOARD

### 1️⃣ Captura de Dados (Sensor)

```
[Sensor IoT] → [Gateway MQTT] → [Backend Flask] → [Banco de Dados]
```

**Processo:**
1. Sensor detecta presença/movimento
2. Envia mensagem via protocolo (LoRa/Zigbee/Sigfox/RFID)
3. Gateway recebe e publica no broker MQTT
4. Backend Flask consome mensagem MQTT
5. Processa e insere no banco de dados

### 2️⃣ Armazenamento no Banco

**Inserção de Leitura:**
```python
# Classe: Reading.create_from_mqtt()
reading = Reading(
    sensor_id=1,                    # FK para sensors
    activity=1,                     # 0 ou 1
    timestamp='2025-11-01 14:30:00', # Momento da leitura
    sensor_metadata={
        'battery_level': 95.0,
        'rssi_dbm': -55.0
    }
)
```

**Atualização de Estatísticas:**
```python
# Atualiza automaticamente ao inserir leitura
sensor.total_readings += 1
sensor.last_reading_at = reading.timestamp
sensor.battery_level = metadata['battery_level']
sensor.signal_strength = metadata['rssi_dbm']
```

### 3️⃣ Recuperação via API

**Endpoint:** `GET /api/v1/sensors`
```json
{
  "id": 1,
  "serial_number": "LORA-A1B2C3D4",
  "protocol": "LoRa",
  "location": "Entrada Principal",
  "status": "active",
  "battery_level": 100.0,
  "signal_strength": -60.0,
  "total_readings": 5464,
  "last_reading_at": "2025-10-28T01:27:02"
}
```

**Endpoint:** `GET /api/v1/readings?sensor_id=1&limit=100`
```json
{
  "id": 123456,
  "sensor_id": 1,
  "activity": 1,
  "timestamp": "2025-11-01T14:30:00",
  "sensor_metadata": {
    "battery_level": 100.0,
    "rssi_dbm": -60.0
  }
}
```

### 4️⃣ Exibição no Dashboard

#### 📱 **Painel Principal (index.html)**

**Card: "Entradas Hoje"**
- **Fonte:** `readings` table
- **Query:** `SELECT COUNT(*) FROM readings WHERE activity=1 AND DATE(timestamp)=CURDATE()`
- **Campo:** `activity = 1` (detecções)
- **Exibição:** Contador total de pessoas detectadas
- **JavaScript:** `main-page.js → updateMainMetrics()`

**Card: "Sensores Ativos"**
- **Fonte:** `sensors` table
- **Query:** `SELECT COUNT(*) FROM sensors WHERE status='active'`
- **Campo:** `status = 'active'`
- **Exibição:** Total de sensores operacionais
- **JavaScript:** `main-page.js → updateMainMetrics()`

**Card: "Média de Ocupação"**
- **Fonte:** `readings` table (agregação)
- **Cálculo:** Média de detecções por hora nas últimas 24h
- **Query:** Agrupa detecções por intervalo de tempo
- **Exibição:** Porcentagem de ocupação média
- **JavaScript:** `main-page.js → updateMainMetrics()`

**Seção: "Status dos Sensores"**
- **Fonte:** `sensors` table (JOIN com `readings`)
- **Campos:**
  - `serial_number` → Nome do sensor
  - `protocol` → Badge colorido
  - `location` → Localização
  - `battery_level` → Indicador de bateria
  - `signal_strength` → Qualidade do sinal
  - `last_reading_at` → Última comunicação
- **JavaScript:** `indicators.js → updateLastReading()`

**Gráfico: "Fluxo de Pessoas - 24h"**
- **Fonte:** `readings` table
- **Query:** Agrupa `activity=1` por hora
- **Campos:** `timestamp`, `activity`
- **Biblioteca:** Chart.js
- **JavaScript:** `charts.js → createLineChart()`

---

#### 🗺️ **Página de Áreas (areas.html)**

**Cards de Ocupação por Área**
- **Fonte:** `readings` table (filtrado por `sensor.location`)
- **Query:** Conta detecções em sensores de cada área
- **Campos:**
  - `sensor.location` → Identificação da área
  - COUNT(`activity=1`) → Pessoas detectadas
  - Capacidade máxima (hardcoded)
- **Cálculo:** `(detecções / capacidade) * 100`
- **Exibição:** 
  - Círculo percentual
  - Contagem de pessoas
  - Badge de status (normal/warning/danger)
- **JavaScript:** `areas-page.js → updateAreaOccupation()`

**Gráfico: "Histórico de Ocupação"**
- **Fonte:** `readings` table (agregado por área)
- **Query:** Agrupa detecções por área e hora
- **JavaScript:** `charts.js → createBarChart()`

---

#### 🔔 **Página de Alertas (alertas.html)**

**Card: "Alertas Críticos"**
- **Fonte:** `readings` + `sensors` (lógica de negócio)
- **Condições para alerta:**
  - Sensor offline (last_reading_at > 5 minutos)
  - Bateria baixa (battery_level < 20%)
  - Capacidade excedida (detecções > capacidade)
  - Sinal fraco (signal_strength < -80 dBm)
- **Campos:**
  - `sensor.status` → Status operacional
  - `sensor.battery_level` → Nível de bateria
  - `sensor.last_reading_at` → Última comunicação
  - COUNT(`readings`) → Taxa de leituras
- **JavaScript:** `alerts-page.js → checkAlerts()`

**Lista de Alertas Ativos**
- **Fonte:** Gerado dinamicamente baseado em regras
- **Prioridades:** Crítico / Aviso / Informativo
- **JavaScript:** `alerts-page.js → renderAlerts()`

---

#### 🏊 **Página de Piscina (piscina.html)**

**Card: "Ocupação Atual"**
- **Fonte:** `readings` (sensor 5: LORA-Q7R8S9T0)
- **Query:** `SELECT COUNT(*) FROM readings WHERE sensor_id=5 AND activity=1 AND timestamp > NOW() - INTERVAL 15 MINUTE`
- **Campo:** `activity = 1` em sensor da piscina
- **Exibição:** Porcentagem de ocupação
- **JavaScript:** `pool-page.js → updatePoolOccupation()`

**Card: "Temperatura da Água"**
- **Fonte:** `pool_readings` table
- **Query:** `SELECT temperature FROM pool_readings WHERE sensor_type='water_temp' ORDER BY reading_date DESC, reading_time DESC LIMIT 1`
- **Campos:**
  - `sensor_type = 'water_temp'`
  - `temperature` → Valor em °C
- **Exibição:** Temperatura atual + faixa ideal
- **JavaScript:** `pool-page.js → updateWaterTemp()`

**Card: "Temperatura Ambiente"**
- **Fonte:** `pool_readings` table
- **Query:** Similar ao anterior com `sensor_type='ambient_temp'`
- **Exibição:** Temperatura do ar + sensação térmica
- **JavaScript:** `pool-page.js → updateAmbientTemp()`

**Cards de Qualidade da Água**
- **Fonte:** `pool_readings` table
- **Query:** `SELECT * FROM pool_readings WHERE sensor_type='water_quality' ORDER BY created_at DESC LIMIT 1`
- **Campos:**
  - `temperature` (usado como pH)
  - `water_quality` → Classificação
- **Exibição:**
  - pH: 7.4 (ideal: 7.2-7.6)
  - Cloro: 2.1 ppm (ideal: 1.0-3.0)
  - Alcalinidade: 100 ppm (ideal: 80-120)
- **JavaScript:** `pool-page.js → updateWaterQuality()`

**Gráfico: "Qualidade da Água - 24h"**
- **Fonte:** `pool_readings` table (últimas 24h)
- **Query:** Agrupa leituras por hora
- **JavaScript:** `charts.js → createMultiLineChart()`

---

#### 📡 **Página de Resumo de Sensores (resumo-sensores.html)**

**Cards de Resumo Geral**
- **Total de Sensores:**
  - **Fonte:** `SELECT COUNT(*) FROM sensors`
  - **Exibição:** 6 sensores
  
- **Sensores Ativos:**
  - **Fonte:** `SELECT COUNT(*) FROM sensors WHERE status='active'`
  - **Exibição:** 6 (100%)
  
- **Total de Leituras:**
  - **Fonte:** `SELECT SUM(total_readings) FROM sensors`
  - **Exibição:** 33.184 leituras
  
- **Protocolos Ativos:**
  - **Fonte:** `SELECT DISTINCT protocol FROM sensors`
  - **Exibição:** 4 protocolos

**Tabela de Sensores**
- **Fonte:** `sensors` table (JOIN com agregação de `readings`)
- **Colunas:**
  - `id` → ID do sensor
  - `serial_number` → Serial
  - `protocol` → Badge colorido
  - `location` → Localização com ícone
  - `battery_level` → Barra de progresso
  - `signal_strength` → Indicador de barras
  - `total_readings` → Contador

**Cards de Estatísticas**
- **Distribuição por Protocolo:**
  - **Query:** `SELECT protocol, COUNT(*) FROM sensors GROUP BY protocol`
  - **Exibição:** LoRa: 2 (33.3%), Zigbee: 2 (33.3%), etc.
  
- **Status de Bateria:**
  - **Query:** Agrupa sensores por faixa de bateria
  - **Exibição:** Excelente: 5, Bom: 1, Crítico: 0
  
- **Qualidade de Sinal:**
  - **Query:** Agrupa sensores por força do sinal
  - **Exibição:** Ótimo: 3, Bom: 2, Fraco: 0

**Gráfico: "Distribuição de Leituras"**
- **Fonte:** `sensors` table
- **Campo:** `total_readings` por sensor
- **Tipo:** Gráfico de barras
- **JavaScript:** `sensors-resume-page.js → initDistributionChart()`

---

## 🔍 QUERIES PRINCIPAIS USADAS NO DASHBOARD

### 1. Sensores Ativos
```sql
SELECT * FROM sensors 
WHERE status = 'active' 
ORDER BY location;
```

### 2. Leituras do Dia
```sql
SELECT COUNT(*) as total, 
       SUM(CASE WHEN activity = 1 THEN 1 ELSE 0 END) as detections
FROM readings 
WHERE DATE(timestamp) = CURDATE();
```

### 3. Ocupação por Área (Últimas 24h)
```sql
SELECT s.location, 
       COUNT(CASE WHEN r.activity = 1 THEN 1 END) as detections
FROM sensors s
LEFT JOIN readings r ON s.id = r.sensor_id 
WHERE r.timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
GROUP BY s.location;
```

### 4. Histórico de Detecções (Por Hora)
```sql
SELECT HOUR(timestamp) as hour, 
       COUNT(*) as detections
FROM readings 
WHERE activity = 1 
  AND DATE(timestamp) = CURDATE()
GROUP BY HOUR(timestamp)
ORDER BY hour;
```

### 5. Status de Bateria dos Sensores
```sql
SELECT serial_number, 
       protocol, 
       location, 
       battery_level,
       CASE 
           WHEN battery_level >= 90 THEN 'Excelente'
           WHEN battery_level >= 70 THEN 'Bom'
           WHEN battery_level >= 50 THEN 'Regular'
           ELSE 'Crítico'
       END as battery_status
FROM sensors 
WHERE battery_level IS NOT NULL
ORDER BY battery_level DESC;
```

### 6. Última Leitura de Cada Sensor
```sql
SELECT s.serial_number, 
       s.location, 
       MAX(r.timestamp) as last_reading,
       TIMESTAMPDIFF(MINUTE, MAX(r.timestamp), NOW()) as minutes_ago
FROM sensors s
LEFT JOIN readings r ON s.id = r.sensor_id
GROUP BY s.id
ORDER BY last_reading DESC;
```

### 7. Temperatura da Piscina (Última)
```sql
SELECT temperature, 
       reading_date, 
       reading_time
FROM pool_readings 
WHERE sensor_type = 'water_temp' 
ORDER BY created_at DESC 
LIMIT 1;
```

### 8. Qualidade da Água (Última)
```sql
SELECT water_quality, 
       reading_date, 
       reading_time
FROM pool_readings 
WHERE sensor_type = 'water_quality' 
ORDER BY created_at DESC 
LIMIT 1;
```

---

## 📈 ENDPOINTS DA API REST

### Sensores
- `GET /api/v1/sensors` → Lista todos os sensores
- `GET /api/v1/sensors/{id}` → Detalhes de um sensor
- `GET /api/v1/sensors/{id}/readings` → Leituras de um sensor

### Leituras
- `GET /api/v1/readings` → Lista leituras (com filtros)
- `POST /api/v1/readings` → Insere nova leitura
- `GET /api/v1/readings/hourly` → Leituras agrupadas por hora

### Estatísticas
- `GET /api/v1/statistics/overview` → Visão geral do sistema
- `GET /api/v1/statistics/activity` → Estatísticas de atividade
- `GET /api/v1/statistics/sensors` → Estatísticas por sensor

### Piscina
- `GET /api/v1/pool/latest` → Últimas leituras da piscina
- `GET /api/v1/pool/statistics` → Estatísticas da piscina
- `POST /api/v1/pool/readings` → Insere leitura da piscina

---

## 🎨 MAPEAMENTO DE PROTOCOLOS → CORES NO DASHBOARD

| Protocolo | Cor Principal | Gradiente                                    | Uso               |
|-----------|---------------|----------------------------------------------|-------------------|
| LoRa      | 🟣 Roxo       | linear-gradient(135deg, #9b59b6, #8e44ad)  | Badges, Badges    |
| Zigbee    | 🟢 Verde      | linear-gradient(135deg, #27ae60, #229954)  | Badges, Cards     |
| Sigfox    | 🟠 Laranja    | linear-gradient(135deg, #e67e22, #d35400)  | Badges, Icons     |
| RFID      | 🔵 Azul       | linear-gradient(135deg, #3498db, #2980b9)  | Badges, Headers   |

---

## 🔄 ATUALIZAÇÃO EM TEMPO REAL

### JavaScript Auto-Refresh
```javascript
// main-page.js - Atualiza a cada 30 segundos
setInterval(() => {
    loadMainDashboardData();
}, 30000);

// areas-page.js - Atualiza a cada 30 segundos
setInterval(() => {
    updateAreasData();
}, 30000);

// sensors-resume-page.js - Atualiza a cada 60 segundos
setInterval(() => {
    loadSensorsData();
}, 60000);
```

---

## 📊 RESUMO DO FLUXO DE DADOS

```
┌─────────────────────────────────────────────────────────────────┐
│                        SENSOR FÍSICO                            │
│  (LoRa, Zigbee, Sigfox, RFID)                                  │
│  Coleta: Presença, Bateria, RSSI                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GATEWAY MQTT                                 │
│  Recebe mensagens dos sensores                                  │
│  Publica no broker MQTT                                         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND FLASK                                │
│  - Consome mensagens MQTT                                       │
│  - Processa e valida dados                                      │
│  - Insere no banco de dados                                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                 BANCO DE DADOS MySQL                            │
│  Tabelas: sensors, readings, pool_readings                      │
│  Total: 33.184 leituras | 6 sensores ativos                    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API REST                                   │
│  Endpoints: /api/v1/sensors, /api/v1/readings, etc.           │
│  Formato: JSON                                                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              DASHBOARD (Frontend)                               │
│  - JavaScript ES6 (10 módulos)                                  │
│  - Chart.js para gráficos                                       │
│  - Auto-refresh (30-60s)                                        │
│  - 5 páginas: Principal, Áreas, Alertas, Piscina, Sensores    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📝 NOTAS IMPORTANTES

1. **Sensores RFID** não possuem medição de bateria e sinal (alimentação externa)
2. **activity = 0** significa "nenhuma detecção" e **activity = 1** significa "presença detectada"
3. **Timestamps** são armazenados em UTC e convertidos para hora local no frontend
4. **Capacidades máximas** das áreas são hardcoded no frontend (devem ser parametrizadas)
5. **Auto-refresh** pode ser configurado por página (30s ou 60s)
6. **Índices do banco** otimizam queries por sensor_id, timestamp e activity
7. **Alertas** são gerados dinamicamente baseados em regras de negócio (não há tabela de alertas)

---

**Documento gerado em:** 01/11/2025  
**Versão do Sistema:** 1.0  
**Total de Sensores:** 6 ativos  
**Total de Leituras:** 33.184  
**Dashboard:** 5 páginas funcionais


---

## 📐 DIAGRAMA DETALHADO DO FLUXO DE DADOS

### 🔵 Exemplo Completo: Sensor LoRa detecta presença

```
┌─────────────────────────────────────────────────────────────────────┐
│ ETAPA 1: SENSOR FÍSICO                                              │
│ Sensor: LORA-A1B2C3D4 @ Entrada Principal                           │
│ Evento: Pessoa detectada às 14:30:00                                │
│ Dados coletados:                                                     │
│   • Presença: SIM (activity=1)                                       │
│   • Bateria: 100%                                                    │
│   • RSSI: -60 dBm                                                    │
│   • Temperatura: 26.5°C                                              │
└─────────────────────────┬───────────────────────────────────────────┘
                          │ [Transmissão LoRa]
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│ ETAPA 2: GATEWAY MQTT                                               │
│ Gateway ID: gateway_001                                              │
│ Mensagem MQTT recebida:                                              │
│ {                                                                    │
│   "sensor_id": "LORA-A1B2C3D4",                                      │
│   "timestamp": "2025-11-01T14:30:00Z",                               │
│   "activity": 1,                                                     │
│   "metadata": {                                                      │
│     "battery_level": 100.0,                                          │
│     "rssi_dbm": -60.0,                                               │
│     "temperature": 26.5,                                             │
│     "humidity": 65.0                                                 │
│   }                                                                  │
│ }                                                                    │
│ Tópico MQTT: smartceu/sensors/lora/LORA-A1B2C3D4                    │
└─────────────────────────┬───────────────────────────────────────────┘
                          │ [Publish MQTT]
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│ ETAPA 3: BACKEND FLASK                                              │
│ Arquivo: app/models/reading.py                                       │
│ Método: Reading.create_from_mqtt(mqtt_message)                       │
│                                                                      │
│ 1. Busca sensor por serial_number:                                  │
│    sensor = Sensor.query.filter_by(                                 │
│              serial_number='LORA-A1B2C3D4').first()                 │
│    sensor.id = 1                                                     │
│                                                                      │
│ 2. Cria registro de leitura:                                         │
│    reading = Reading(                                                │
│      sensor_id=1,                    # FK para sensors              │
│      activity=1,                     # Presença detectada           │
│      timestamp=datetime(2025,11,1,14,30,0),                         │
│      sensor_metadata={               # JSON                         │
│        'battery_level': 100.0,                                       │
│        'rssi_dbm': -60.0,                                            │
│        'temperature': 26.5,                                          │
│        'humidity': 65.0                                              │
│      },                                                              │
│      message_id='msg_12345',                                         │
│      gateway_id='gateway_001'                                        │
│    )                                                                 │
│                                                                      │
│ 3. Atualiza estatísticas do sensor:                                 │
│    sensor.total_readings += 1        # 5464 → 5465                  │
│    sensor.last_reading_at = timestamp                                │
│    sensor.battery_level = 100.0                                      │
│    sensor.signal_strength = -60.0                                    │
│                                                                      │
│ 4. Commit no banco:                                                  │
│    db.session.add(reading)                                           │
│    db.session.commit()                                               │
└─────────────────────────┬───────────────────────────────────────────┘
                          │ [SQL INSERT]
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│ ETAPA 4: BANCO DE DADOS MySQL                                       │
│                                                                      │
│ ╔═══════════════════════════════════════════════════════════╗       │
│ ║ Tabela: sensors (ATUALIZADA)                              ║       │
│ ╠═══════════════════════════════════════════════════════════╣       │
│ ║ id: 1                                                     ║       │
│ ║ serial_number: 'LORA-A1B2C3D4'                            ║       │
│ ║ protocol: 'LoRa'                                          ║       │
│ ║ location: 'Entrada Principal'                             ║       │
│ ║ status: 'active'                                          ║       │
│ ║ battery_level: 100.0          ← ATUALIZADO               ║       │
│ ║ signal_strength: -60.0        ← ATUALIZADO               ║       │
│ ║ total_readings: 5465          ← INCREMENTADO             ║       │
│ ║ last_reading_at: 2025-11-01 14:30:00  ← ATUALIZADO       ║       │
│ ╚═══════════════════════════════════════════════════════════╝       │
│                                                                      │
│ ╔═══════════════════════════════════════════════════════════╗       │
│ ║ Tabela: readings (NOVA LINHA INSERIDA)                   ║       │
│ ╠═══════════════════════════════════════════════════════════╣       │
│ ║ id: 123456                                                ║       │
│ ║ sensor_id: 1                  (FK → sensors.id)          ║       │
│ ║ activity: 1                   (1=presença detectada)     ║       │
│ ║ timestamp: 2025-11-01 14:30:00                           ║       │
│ ║ sensor_metadata: {            (JSON)                     ║       │
│ ║   "battery_level": 100.0,                                ║       │
│ ║   "rssi_dbm": -60.0,                                     ║       │
│ ║   "temperature": 26.5,                                   ║       │
│ ║   "humidity": 65.0                                       ║       │
│ ║ }                                                        ║       │
│ ║ message_id: 'msg_12345'                                  ║       │
│ ║ gateway_id: 'gateway_001'                                ║       │
│ ║ created_at: 2025-11-01 14:30:01                          ║       │
│ ╚═══════════════════════════════════════════════════════════╝       │
└─────────────────────────┬───────────────────────────────────────────┘
                          │ [Query API]
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│ ETAPA 5: API REST                                                   │
│                                                                      │
│ GET /api/v1/sensors/1                                                │
│ Response:                                                            │
│ {                                                                    │
│   "id": 1,                                                           │
│   "serial_number": "LORA-A1B2C3D4",                                  │
│   "protocol": "LoRa",                                                │
│   "location": "Entrada Principal",                                   │
│   "status": "active",                                                │
│   "battery_level": 100.0,        ← Valor atualizado                 │
│   "signal_strength": -60.0,      ← Valor atualizado                 │
│   "total_readings": 5465,        ← Valor incrementado               │
│   "last_reading_at": "2025-11-01T14:30:00"  ← Timestamp atualizado  │
│ }                                                                    │
│                                                                      │
│ GET /api/v1/readings?sensor_id=1&limit=1                             │
│ Response:                                                            │
│ {                                                                    │
│   "data": [{                                                         │
│     "id": 123456,                                                    │
│     "sensor_id": 1,                                                  │
│     "activity": 1,               ← Presença detectada               │
│     "timestamp": "2025-11-01T14:30:00",                              │
│     "sensor_metadata": {                                             │
│       "battery_level": 100.0,                                        │
│       "rssi_dbm": -60.0,                                             │
│       "temperature": 26.5,                                           │
│       "humidity": 65.0                                               │
│     }                                                                │
│   }],                                                                │
│   "total": 5465                                                      │
│ }                                                                    │
└─────────────────────────┬───────────────────────────────────────────┘
                          │ [Fetch API]
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│ ETAPA 6: DASHBOARD (Frontend)                                       │
│                                                                      │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ 🏠 PÁGINA: Painel Principal (index.html)                        │ │
│ ├─────────────────────────────────────────────────────────────────┤ │
│ │ Card: "Entradas Hoje"                                           │ │
│ │ ┌────────────────────┐                                          │ │
│ │ │   📊 2.308         │  ← COUNT(readings WHERE activity=1)      │ │
│ │ │   Pessoas          │     AND sensor_id=1 AND DATE=hoje        │ │
│ │ └────────────────────┘                                          │ │
│ │                                                                 │ │
│ │ Card: "Sensor LORA-A1B2C3D4"                                    │ │
│ │ ┌────────────────────────────────────────────────┐             │ │
│ │ │ 🟣 LoRa | Entrada Principal                    │             │ │
│ │ │ ──────────────────────────────────────────────── │             │ │
│ │ │ 🔋 Bateria: 100% [████████████████████] Verde  │ ← battery   │ │
│ │ │ 📡 Sinal: -60 dBm [█████░░] Excelente          │ ← rssi      │ │
│ │ │ 🕐 Última leitura: há 5 segundos               │ ← timestamp │ │
│ │ │ 📊 Total: 5.465 leituras                       │ ← counter   │ │
│ │ └────────────────────────────────────────────────┘             │ │
│ │                                                                 │ │
│ │ JavaScript: indicators.js → updateLastReading()                 │ │
│ │ Auto-refresh: 30 segundos                                       │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ 📡 PÁGINA: Resumo de Sensores (resumo-sensores.html)           │ │
│ ├─────────────────────────────────────────────────────────────────┤ │
│ │ Tabela de Sensores:                                             │ │
│ │ ┌──┬──────────────┬────────┬──────────────┬─────────┬────────┐ │ │
│ │ │ID│ Serial       │Protocol│Location      │Battery  │Leituras│ │ │
│ │ ├──┼──────────────┼────────┼──────────────┼─────────┼────────┤ │ │
│ │ │1 │LORA-A1B2C3D4 │🟣LoRa  │📍Entrada Prin│█████100%│ 5,465  │ │ │
│ │ │  │              │        │              │ -60 dBm │        │ │ │
│ │ └──┴──────────────┴────────┴──────────────┴─────────┴────────┘ │ │
│ │                                                                 │ │
│ │ JavaScript: sensors-resume-page.js → loadSensorsData()          │ │
│ │ Auto-refresh: 60 segundos                                       │ │
│ └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔀 TABELA COMPLETA DE MAPEAMENTO DE CAMPOS

| Dado Coletado        | Origem (Sensor) | Armazenamento (DB)           | Campo DB           | API Endpoint            | Dashboard            | Componente UI           |
|----------------------|-----------------|------------------------------|--------------------|-------------------------|----------------------|-------------------------|
| **ID do Sensor**     | Serial físico   | `sensors.id`                 | INTEGER PK         | `/api/v1/sensors`       | Todas as páginas     | Cards, Tabelas          |
| **Número de Série**  | Firmware        | `sensors.serial_number`      | VARCHAR(50)        | `/api/v1/sensors`       | Painel, Resumo       | Badge, Título           |
| **Protocolo**        | Tipo físico     | `sensors.protocol`           | VARCHAR(20)        | `/api/v1/sensors`       | Todas as páginas     | Badge colorido          |
| **Localização**      | Instalação      | `sensors.location`           | VARCHAR(100)       | `/api/v1/sensors`       | Todas as páginas     | Texto com ícone         |
| **Status**           | Lógica backend  | `sensors.status`             | VARCHAR(11)        | `/api/v1/sensors`       | Painel, Resumo       | Badge (ativo/inativo)   |
| **Nível de Bateria** | Sensor IoT      | `sensors.battery_level`      | FLOAT              | `/api/v1/sensors`       | Painel, Resumo       | Barra de progresso      |
| **Força do Sinal**   | RSSI do sensor  | `sensors.signal_strength`    | FLOAT              | `/api/v1/sensors`       | Painel, Resumo       | Indicador de barras     |
| **Total de Leituras**| Contador auto   | `sensors.total_readings`     | INTEGER            | `/api/v1/sensors`       | Painel, Resumo       | Contador numérico       |
| **Última Leitura**   | Timestamp auto  | `sensors.last_reading_at`    | DATETIME           | `/api/v1/sensors`       | Painel, Resumo       | Texto "há X minutos"    |
| **Presença/Movimento**| Sensor PIR/LoRa| `readings.activity`          | SMALLINT (0 ou 1)  | `/api/v1/readings`      | Todas as páginas     | Contador de pessoas     |
| **Timestamp Leitura**| RTC sensor      | `readings.timestamp`         | DATETIME           | `/api/v1/readings`      | Gráficos             | Eixo X dos charts       |
| **Metadados JSON**   | Payload sensor  | `readings.sensor_metadata`   | JSON               | `/api/v1/readings`      | Detalhes             | Tooltip, Modal          |
| **ID Gateway**       | Infra MQTT      | `readings.gateway_id`        | VARCHAR(50)        | `/api/v1/readings`      | Logs                 | Tabela de diagnóstico   |
| **Temperatura Água** | Sensor NTC      | `pool_readings.temperature`  | NUMERIC(5,2)       | `/api/v1/pool/latest`   | Piscina              | Card com termômetro     |
| **Temp. Ambiente**   | Sensor DHT22    | `pool_readings.temperature`  | NUMERIC(5,2)       | `/api/v1/pool/latest`   | Piscina              | Card com ícone sol      |
| **Qualidade Água**   | Sensor pH/Cl    | `pool_readings.water_quality`| VARCHAR(20)        | `/api/v1/pool/latest`   | Piscina              | Cards de qualidade      |
| **Taxa de Detecção** | Cálculo API     | N/A (agregação)              | N/A                | `/api/v1/statistics`    | Áreas, Painel        | Porcentagem em cards    |
| **Ocupação %**       | Cálculo frontend| N/A (calculado)              | N/A                | N/A                     | Áreas, Piscina       | Círculo de progresso    |

---

## ⚙️ CONFIGURAÇÕES E CONSTANTES

### Intervalos de Atualização
```javascript
// frontend/js/modules/main-page.js
const REFRESH_INTERVAL_MAIN = 30000;  // 30 segundos

// frontend/js/modules/areas-page.js
const REFRESH_INTERVAL_AREAS = 30000;  // 30 segundos

// frontend/js/modules/sensors-resume-page.js
const REFRESH_INTERVAL_SENSORS = 60000;  // 60 segundos

// frontend/js/modules/pool-page.js
const REFRESH_INTERVAL_POOL = 30000;  // 30 segundos
```

### Capacidades Máximas (Hardcoded - TODO: Parametrizar)
```javascript
const CAPACITIES = {
  'Entrada Principal': 50,
  'Quadra Esportiva': 100,
  'Playground': 80,
  'Biblioteca': 60,
  'Área da Piscina': 40,
  'Saída Lateral': 30
};
```

### Thresholds de Alertas
```javascript
const ALERT_THRESHOLDS = {
  BATTERY_CRITICAL: 20,        // % de bateria
  BATTERY_WARNING: 50,
  SIGNAL_WEAK: -80,            // dBm
  SIGNAL_GOOD: -70,
  OFFLINE_MINUTES: 5,          // Minutos sem leitura
  CAPACITY_WARNING: 0.8,       // 80% da capacidade
  CAPACITY_DANGER: 0.95        // 95% da capacidade
};
```

### Faixas de Qualidade
```javascript
// Bateria
const BATTERY_LEVELS = {
  EXCELLENT: { min: 90, max: 100, color: 'success', label: 'Excelente' },
  GOOD: { min: 70, max: 89, color: 'info', label: 'Bom' },
  FAIR: { min: 50, max: 69, color: 'warning', label: 'Regular' },
  CRITICAL: { min: 0, max: 49, color: 'danger', label: 'Crítico' }
};

// Sinal (RSSI em dBm)
const SIGNAL_LEVELS = {
  EXCELLENT: { min: -60, max: 0, bars: 5, label: 'Excelente' },
  GOOD: { min: -70, max: -61, bars: 4, label: 'Bom' },
  FAIR: { min: -80, max: -71, bars: 3, label: 'Regular' },
  WEAK: { min: -90, max: -81, bars: 2, label: 'Fraco' },
  VERY_WEAK: { min: -120, max: -91, bars: 1, label: 'Muito Fraco' }
};
```

---

## 🔐 SEGURANÇA E VALIDAÇÕES

### Validações no Backend
```python
# app/schemas/reading.py
class ReadingCreateSchema(Schema):
    sensor_id = fields.Integer(required=True)
    activity = fields.Integer(
        required=True,
        validate=validate.OneOf([0, 1])  # Apenas 0 ou 1
    )
    timestamp = fields.DateTime(required=True)
    sensor_metadata = fields.Dict(keys=fields.Str(), values=fields.Raw())
    
    @validates('timestamp')
    def validate_timestamp(self, value):
        """Não permite timestamps futuros"""
        if value > datetime.utcnow():
            raise ValidationError('Timestamp cannot be in the future')
```

### Validações no Frontend
```javascript
// frontend/js/modules/utils.js
function validateSensorData(data) {
  if (!data.sensor_id || data.sensor_id <= 0) {
    throw new Error('Invalid sensor_id');
  }
  
  if (![0, 1].includes(data.activity)) {
    throw new Error('Activity must be 0 or 1');
  }
  
  if (data.battery_level && (data.battery_level < 0 || data.battery_level > 100)) {
    throw new Error('Battery level must be between 0 and 100');
  }
  
  return true;
}
```

---

**Última atualização:** 01/11/2025 15:45  
**Versão do documento:** 1.1  
**Autor:** Grupo PI-IV (DRP14-PJI410-SALA-004-GRUPO-05)
