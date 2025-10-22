# Guia de Integração Futura
# Sistema de Controle de Acesso - CEU Tres Pontes

## 🔌 Integrações Planejadas

### 1. Integração com MQTT (Fase 2)

```python
# Exemplo de como os sensores serão integrados com MQTT

from sensores import LoRaSensor
import paho.mqtt.client as mqtt
import json

# Criar sensor
sensor = LoRaSensor(location="Entrada Principal")

# Configurar cliente MQTT
client = mqtt.Client()
client.connect("localhost", 1883)

# Loop de leitura e publicação
while True:
    reading = sensor.simulate_detection()
    
    # Publicar no MQTT
    topic = f"ceu/sensores/lora/{sensor.serial_number}/data"
    payload = json.dumps(reading)
    client.publish(topic, payload, qos=1)
    
    time.sleep(5)
```

### 2. Integração com Backend Flask (Fase 3)

```python
# Exemplo de endpoint REST

from flask import Flask, jsonify
from sensores import LoRaSensor, ZigBeeSensor

app = Flask(__name__)

# Criar sensores
sensors = {
    'lora_1': LoRaSensor(location="Entrada Principal"),
    'zigbee_1': ZigBeeSensor(location="Saída Norte")
}

@app.route('/api/sensors', methods=['GET'])
def get_sensors():
    """Retorna lista de todos os sensores"""
    return jsonify([
        sensor.get_status() 
        for sensor in sensors.values()
    ])

@app.route('/api/sensors/<sensor_id>/reading', methods=['GET'])
def get_reading(sensor_id):
    """Retorna leitura de um sensor específico"""
    sensor = sensors.get(sensor_id)
    if sensor:
        reading = sensor.simulate_detection()
        return jsonify(reading)
    return jsonify({'error': 'Sensor not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
```

### 3. Integração com Banco de Dados (Fase 3)

```python
# Exemplo de persistência em MySQL

import mysql.connector
from sensores import LoRaSensor

# Conectar ao banco
db = mysql.connector.connect(
    host="localhost",
    user="ceu_admin",
    password="password",
    database="ceu_tres_pontes"
)
cursor = db.cursor()

# Criar sensor
sensor = LoRaSensor(location="Entrada Principal")

# Salvar leitura
reading = sensor.simulate_detection()

sql = """
INSERT INTO readings 
(sensor_id, activity, timestamp, metadata) 
VALUES (%s, %s, %s, %s)
"""
values = (
    sensor.serial_number,
    reading['activity'],
    reading['timestamp'],
    json.dumps(reading)
)

cursor.execute(sql, values)
db.commit()
```

### 4. Integração com WebSocket (Fase 4)

```javascript
// Exemplo de conexão WebSocket no frontend

const ws = new WebSocket('ws://localhost:5000/ws');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    if (data.activity === 1) {
        console.log(`Pessoa detectada em ${data.location}`);
        updateDashboard(data);
    }
};

function updateDashboard(data) {
    // Atualizar contador
    document.getElementById('total-count').textContent = data.total_detections;
    
    // Adicionar à lista
    const list = document.getElementById('recent-detections');
    const item = document.createElement('li');
    item.textContent = `${data.timestamp} - ${data.location}`;
    list.prepend(item);
}
```

### 5. Integração com RabbitMQ (Fase 3)

```python
# Exemplo de processamento assíncrono com RabbitMQ

import pika
import json
from sensores import LoRaSensor

# Conectar ao RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

# Declarar fila
channel.queue_declare(queue='sensor_data', durable=True)

# Criar sensor
sensor = LoRaSensor(location="Entrada Principal")

# Publicar mensagem
reading = sensor.simulate_detection()
message = json.dumps(reading)

channel.basic_publish(
    exchange='',
    routing_key='sensor_data',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,  # Mensagem persistente
    )
)

print(f"Mensagem enviada: {message}")
connection.close()
```

### 6. Dashboard em Tempo Real (Fase 4)

```html
<!-- Exemplo de dashboard HTML -->

<!DOCTYPE html>
<html>
<head>
    <title>CEU Tres Pontes - Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="dashboard">
        <h1>Parque CEU Tres Pontes</h1>
        
        <div class="stats">
            <div class="stat-card">
                <h3>Pessoas Agora</h3>
                <p id="current-count">0</p>
            </div>
            <div class="stat-card">
                <h3>Entradas Hoje</h3>
                <p id="entries-today">0</p>
            </div>
            <div class="stat-card">
                <h3>Saídas Hoje</h3>
                <p id="exits-today">0</p>
            </div>
        </div>
        
        <div class="chart-container">
            <canvas id="flowChart"></canvas>
        </div>
        
        <div class="sensors">
            <h2>Sensores Ativos</h2>
            <ul id="sensor-list"></ul>
        </div>
    </div>
    
    <script src="js/dashboard.js"></script>
</body>
</html>
```

### 7. Análise com Pandas (Fase 3)

```python
# Exemplo de análise de dados com Pandas

import pandas as pd
from sensores import LoRaSensor
import time

# Coletar dados
sensor = LoRaSensor(location="Entrada Principal")
data = []

for _ in range(100):
    reading = sensor.simulate_detection()
    data.append(reading)
    time.sleep(0.1)

# Criar DataFrame
df = pd.DataFrame(data)

# Análises
print(f"Total de detecções: {df['activity'].sum()}")
print(f"Taxa de detecção: {df['activity'].mean() * 100:.2f}%")
print(f"\nBateria média: {df['battery_level'].mean():.2f}%")
print(f"RSSI médio: {df['rssi_dbm'].mean():.2f} dBm")

# Agrupar por hora
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hour'] = df['timestamp'].dt.hour
hourly = df.groupby('hour')['activity'].sum()

print("\nDetecções por hora:")
print(hourly)
```

### 8. PowerBI - Conexão (Fase 5)

```python
# Script para preparar dados para PowerBI

import mysql.connector
import pandas as pd

# Conectar ao banco
conn = mysql.connector.connect(
    host="localhost",
    user="ceu_admin",
    password="password",
    database="ceu_tres_pontes"
)

# Query de agregação para PowerBI
query = """
SELECT 
    DATE(timestamp) as date,
    HOUR(timestamp) as hour,
    COUNT(*) as total_readings,
    SUM(activity) as total_detections,
    s.location,
    s.protocol
FROM readings r
JOIN sensors s ON r.sensor_id = s.id
WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY date, hour, s.location, s.protocol
ORDER BY date DESC, hour DESC
"""

# Carregar em DataFrame
df = pd.read_sql(query, conn)

# Exportar para CSV (PowerBI importará este arquivo)
df.to_csv('powerbi_data.csv', index=False)

print(f"Dados exportados: {len(df)} linhas")
```

### 9. Docker Compose (Fase 6)

```yaml
# docker-compose.yml - Exemplo de orquestração

version: '3.8'

services:
  mysql:
    image: mysql:8.0.43
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: ceu_tres_pontes
      MYSQL_USER: ceu_admin
      MYSQL_PASSWORD: adminpass
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"

  mosquitto:
    image: eclipse-mosquitto:latest
    volumes:
      - ./config/mosquitto.conf:/mosquitto/config/mosquitto.conf
    ports:
      - "1883:1883"
      - "9001:9001"

  rabbitmq:
    image: rabbitmq:3.13-management
    environment:
      RABBITMQ_DEFAULT_USER: ceu_user
      RABBITMQ_DEFAULT_PASS: rabbitpass
    ports:
      - "5672:5672"
      - "15672:15672"

  backend:
    build: ./backend
    depends_on:
      - mysql
      - mosquitto
      - rabbitmq
    environment:
      DB_HOST: mysql
      MQTT_HOST: mosquitto
      RABBIT_HOST: rabbitmq
    ports:
      - "5000:5000"

  nginx:
    image: nginx:1.29.1
    volumes:
      - ./frontend:/usr/share/nginx/html
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend
    ports:
      - "80:80"
      - "443:443"

volumes:
  mysql_data:
```

### 10. Monitoramento com Alertas (Fase 3)

```python
# Exemplo de sistema de alertas

from sensores import LoRaSensor

class AlertManager:
    def __init__(self):
        self.alert_threshold = 1000  # Capacidade máxima
        self.current_count = 0
    
    def check_alerts(self, sensor, reading):
        """Verifica condições de alerta"""
        
        # Alerta de capacidade
        if self.current_count >= self.alert_threshold:
            self.send_alert(
                type="CAPACITY",
                message=f"Parque atingiu capacidade máxima: {self.current_count}",
                severity="HIGH"
            )
        
        # Alerta de bateria baixa
        if 'battery_level' in reading and reading['battery_level'] < 20:
            self.send_alert(
                type="BATTERY",
                message=f"Bateria baixa no sensor {sensor.serial_number}",
                severity="MEDIUM"
            )
        
        # Alerta de sensor offline
        time_diff = (datetime.now() - sensor.timestamp).seconds
        if time_diff > 300:  # 5 minutos
            self.send_alert(
                type="OFFLINE",
                message=f"Sensor {sensor.serial_number} offline",
                severity="HIGH"
            )
    
    def send_alert(self, type, message, severity):
        """Envia alerta (email, SMS, push, etc)"""
        print(f"[{severity}] {type}: {message}")
        # Implementar envio real de notificações
```

---

## 📝 Notas de Implementação

### Performance
- Cache de leituras recentes em Redis
- Índices otimizados no MySQL
- Compressão de mensagens MQTT
- Rate limiting na API

### Segurança
- Autenticação JWT para API
- MQTT com TLS
- Validação de inputs
- Logs de auditoria

### Escalabilidade
- Load balancer (NGINX)
- Horizontal scaling do backend
- Particionamento de dados
- Queues para processamento assíncrono

---

Este arquivo será atualizado conforme o projeto avança.
```
