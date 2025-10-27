# Queries SQL Prontas para Dashboards Grafana
## Sistema CEU Tres Pontes - Monitoramento IoT

Este arquivo contém queries SQL prontas para usar nos dashboards do Grafana.

---

## 📊 Dashboard 1: Monitoramento em Tempo Real

### Panel: Leituras por Tipo de Sensor (Time Series)

**Descrição:** Mostra a quantidade de leituras por tipo de sensor ao longo do tempo

```sql
SELECT
  UNIX_TIMESTAMP(r.timestamp) AS time_sec,
  s.sensor_type AS metric,
  COUNT(*) AS value
FROM readings r
JOIN sensors s ON r.sensor_id = s.id
WHERE $__timeFilter(r.timestamp)
GROUP BY 
  UNIX_TIMESTAMP(DATE_FORMAT(r.timestamp, '%Y-%m-%d %H:%i:00')),
  s.sensor_type
ORDER BY time_sec ASC
```

**Configurações:**
- Visualization: Time series
- Unit: short (readings)
- Legend: Right side
- Fill opacity: 10

---

### Panel: Total de Pessoas Atual (Stat)

**Descrição:** Mostra o número total de pessoas no momento

```sql
SELECT
  UNIX_TIMESTAMP(NOW()) AS time_sec,
  total_count AS value
FROM statistics
ORDER BY updated_at DESC
LIMIT 1
```

**Configurações:**
- Visualization: Stat
- Color mode: Value
- Graph mode: Area
- Text size: Auto
- Unit: people

---

### Panel: Taxa de Entrada vs Saída (Time Series)

**Descrição:** Compara entradas e saídas ao longo do tempo

```sql
SELECT
  UNIX_TIMESTAMP(r.timestamp) AS time_sec,
  r.reading_type AS metric,
  SUM(r.person_count) AS value
FROM readings r
WHERE 
  $__timeFilter(r.timestamp)
  AND r.reading_type IN ('ENTRY', 'EXIT')
GROUP BY 
  UNIX_TIMESTAMP(DATE_FORMAT(r.timestamp, '%Y-%m-%d %H:%i:00')),
  r.reading_type
ORDER BY time_sec ASC
```

**Configurações:**
- Visualization: Time series
- Unit: people
- Series: Separate lines for ENTRY and EXIT

---

### Panel: Leituras por Local (Bar Gauge)

**Descrição:** Quantidade de leituras por localização

```sql
SELECT
  s.location AS metric,
  COUNT(*) AS value
FROM readings r
JOIN sensors s ON r.sensor_id = s.id
WHERE $__timeFilter(r.timestamp)
GROUP BY s.location
ORDER BY value DESC
LIMIT 15
```

**Configurações:**
- Visualization: Bar gauge
- Orientation: Horizontal
- Display mode: Gradient
- Unit: short

---

### Panel: Alertas Ativos (Table)

**Descrição:** Lista de alertas ativos no sistema

```sql
SELECT
  UNIX_TIMESTAMP(a.timestamp) AS "Time",
  a.alert_type AS "Tipo",
  a.message AS "Mensagem",
  a.severity AS "Severidade"
FROM alerts a
WHERE 
  $__timeFilter(a.timestamp)
  AND a.status = 'active'
ORDER BY a.timestamp DESC
LIMIT 50
```

**Configurações:**
- Visualization: Table
- Enable pagination
- Sort by Time (DESC)

---

### Panel: Sensores Offline (Stat)

**Descrição:** Número de sensores sem leituras recentes

```sql
SELECT
  UNIX_TIMESTAMP(NOW()) AS time_sec,
  COUNT(*) AS value
FROM sensors s
WHERE NOT EXISTS (
  SELECT 1 FROM readings r
  WHERE r.sensor_id = s.id
  AND r.timestamp > DATE_SUB(NOW(), INTERVAL 5 MINUTE)
)
AND s.status = 'active'
```

**Configurações:**
- Visualization: Stat
- Color: Red if > 0
- Unit: short

---

## 🏊 Dashboard 2: Monitoramento de Piscinas

### Panel: Ocupação das Piscinas (Time Series)

**Descrição:** Ocupação atual de cada piscina ao longo do tempo

```sql
SELECT
  UNIX_TIMESTAMP(pr.timestamp) AS time_sec,
  pr.pool_name AS metric,
  pr.current_occupancy AS value
FROM pool_readings pr
WHERE $__timeFilter(pr.timestamp)
ORDER BY pr.timestamp ASC
```

**Configurações:**
- Visualization: Time series
- Unit: people
- Max: 100 (capacity)
- Thresholds: 50 (yellow), 80 (red)

---

### Panel: Temperatura da Água (Gauge)

**Descrição:** Temperatura atual da água em cada piscina

```sql
SELECT
  UNIX_TIMESTAMP(pr.timestamp) AS time_sec,
  pr.pool_name AS metric,
  pr.water_temperature AS value
FROM pool_readings pr
WHERE $__timeFilter(pr.timestamp)
ORDER BY pr.timestamp DESC
LIMIT 10
```

**Configurações:**
- Visualization: Gauge
- Unit: celsius (°C)
- Min: 20
- Max: 35
- Thresholds: 24-28 (green), others (yellow/red)

---

### Panel: pH da Água (Time Series)

**Descrição:** Monitoramento do pH da água

```sql
SELECT
  UNIX_TIMESTAMP(pr.timestamp) AS time_sec,
  pr.pool_name AS metric,
  pr.water_ph AS value
FROM pool_readings pr
WHERE $__timeFilter(pr.timestamp)
ORDER BY pr.timestamp ASC
```

**Configurações:**
- Visualization: Time series
- Unit: pH
- Min: 6.0
- Max: 8.5
- Threshold: 7.0-7.6 (green)

---

### Panel: Nível de Cloro (Time Series)

**Descrição:** Monitoramento do nível de cloro

```sql
SELECT
  UNIX_TIMESTAMP(pr.timestamp) AS time_sec,
  pr.pool_name AS metric,
  pr.chlorine_level AS value
FROM pool_readings pr
WHERE $__timeFilter(pr.timestamp)
ORDER BY pr.timestamp ASC
```

**Configurações:**
- Visualization: Time series
- Unit: ppm
- Min: 0
- Max: 5
- Threshold: 1.0-3.0 (green)

---

### Panel: Turbidez da Água (Time Series)

**Descrição:** Nível de turbidez da água

```sql
SELECT
  UNIX_TIMESTAMP(pr.timestamp) AS time_sec,
  pr.pool_name AS metric,
  pr.turbidity AS value
FROM pool_readings pr
WHERE $__timeFilter(pr.timestamp)
ORDER BY timestamp ASC
```

**Configurações:**
- Visualization: Time series
- Unit: NTU
- Min: 0
- Max: 5
- Threshold: 0-1 (green), 1-2 (yellow)

---

### Panel: Taxa de Ocupação (%) por Piscina (Bar Gauge)

**Descrição:** Percentual de ocupação de cada piscina

```sql
SELECT
  pool_name AS metric,
  ROUND((AVG(current_occupancy) / MAX(max_capacity)) * 100, 2) AS value
FROM pool_readings
WHERE $__timeFilter(timestamp)
GROUP BY pool_name
ORDER BY value DESC
```

**Configurações:**
- Visualization: Bar gauge
- Unit: percent (0-100)
- Orientation: Horizontal
- Color: Gradient green to red

---

## 📈 Dashboard 3: Estatísticas e Análises

### Panel: Leituras por Hora do Dia (Heatmap)

**Descrição:** Mapa de calor mostrando padrões de tráfego

```sql
SELECT
  UNIX_TIMESTAMP(DATE_FORMAT(r.timestamp, '%Y-%m-%d %H:00:00')) AS time_sec,
  HOUR(r.timestamp) AS metric,
  COUNT(*) AS value
FROM readings r
WHERE $__timeFilter(r.timestamp)
GROUP BY 
  DATE(r.timestamp),
  HOUR(r.timestamp)
ORDER BY time_sec ASC
```

**Configurações:**
- Visualization: Heatmap
- X-axis: Time
- Y-axis: Hour (0-23)
- Color: Gradient

---

### Panel: Média de Pessoas por Dia da Semana (Bar Chart)

**Descrição:** Média de visitantes por dia da semana

```sql
SELECT
  CASE DAYOFWEEK(r.timestamp)
    WHEN 1 THEN 'Domingo'
    WHEN 2 THEN 'Segunda'
    WHEN 3 THEN 'Terça'
    WHEN 4 THEN 'Quarta'
    WHEN 5 THEN 'Quinta'
    WHEN 6 THEN 'Sexta'
    WHEN 7 THEN 'Sábado'
  END AS metric,
  AVG(r.person_count) AS value
FROM readings r
WHERE 
  $__timeFilter(r.timestamp)
  AND r.reading_type = 'COUNT'
GROUP BY DAYOFWEEK(r.timestamp)
ORDER BY DAYOFWEEK(r.timestamp)
```

**Configurações:**
- Visualization: Bar chart
- Unit: people
- Orientation: Vertical

---

### Panel: Top 10 Sensores Mais Ativos (Table)

**Descrição:** Sensores com mais leituras

```sql
SELECT
  s.sensor_id AS "Sensor ID",
  s.sensor_type AS "Tipo",
  s.location AS "Localização",
  COUNT(*) AS "Leituras",
  MAX(r.timestamp) AS "Última Leitura"
FROM readings r
JOIN sensors s ON r.sensor_id = s.id
WHERE $__timeFilter(r.timestamp)
GROUP BY s.sensor_id, s.sensor_type, s.location
ORDER BY COUNT(*) DESC
LIMIT 10
```

**Configurações:**
- Visualization: Table
- Column alignment: Left for text, right for numbers

---

### Panel: Comparação Mensal (Time Series)

**Descrição:** Compara total de acessos mês a mês

```sql
SELECT
  UNIX_TIMESTAMP(DATE_FORMAT(r.timestamp, '%Y-%m-01')) AS time_sec,
  'Total Acessos' AS metric,
  COUNT(*) AS value
FROM readings r
WHERE 
  $__timeFilter(r.timestamp)
  AND r.reading_type = 'ENTRY'
GROUP BY YEAR(r.timestamp), MONTH(r.timestamp)
ORDER BY time_sec ASC
```

**Configurações:**
- Visualization: Time series
- Unit: short
- Aggregation: Sum

---

### Panel: Tempo Médio de Permanência (Stat)

**Descrição:** Tempo médio que pessoas ficam no local

```sql
SELECT
  UNIX_TIMESTAMP(NOW()) AS time_sec,
  AVG(TIMESTAMPDIFF(MINUTE, entry_time, exit_time)) AS value
FROM (
  SELECT
    entry.timestamp AS entry_time,
    exit.timestamp AS exit_time
  FROM readings entry
  JOIN readings exit ON entry.sensor_id = exit.sensor_id
    AND entry.reading_type = 'ENTRY'
    AND exit.reading_type = 'EXIT'
    AND exit.timestamp > entry.timestamp
    AND exit.timestamp < DATE_ADD(entry.timestamp, INTERVAL 8 HOUR)
  WHERE $__timeFilter(entry.timestamp)
) AS times
```

**Configurações:**
- Visualization: Stat
- Unit: minutes
- Decimals: 0

---

### Panel: Taxa de Crescimento Semanal (Stat)

**Descrição:** Crescimento percentual em relação à semana anterior

```sql
SELECT
  UNIX_TIMESTAMP(NOW()) AS time_sec,
  ROUND(
    ((current_week.total - previous_week.total) / previous_week.total) * 100,
    2
  ) AS value
FROM
  (SELECT COUNT(*) AS total FROM readings 
   WHERE timestamp >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)) AS current_week,
  (SELECT COUNT(*) AS total FROM readings 
   WHERE timestamp >= DATE_SUB(CURDATE(), INTERVAL 14 DAY)
   AND timestamp < DATE_SUB(CURDATE(), INTERVAL 7 DAY)) AS previous_week
```

**Configurações:**
- Visualization: Stat
- Unit: percent
- Color: Green if positive, red if negative

---

## 🚨 Dashboard 4: Alertas e Segurança

### Panel: Alertas por Tipo (Pie Chart)

**Descrição:** Distribuição de alertas por tipo

```sql
SELECT
  a.alert_type AS metric,
  COUNT(*) AS value
FROM alerts a
WHERE $__timeFilter(a.timestamp)
GROUP BY a.alert_type
ORDER BY value DESC
```

**Configurações:**
- Visualization: Pie chart
- Legend: Right side
- Unit: short

---

### Panel: Tempo de Resposta a Alertas (Time Series)

**Descrição:** Tempo entre criação e resolução de alertas

```sql
SELECT
  UNIX_TIMESTAMP(a.created_at) AS time_sec,
  a.alert_type AS metric,
  TIMESTAMPDIFF(MINUTE, a.created_at, a.resolved_at) AS value
FROM alerts a
WHERE 
  $__timeFilter(a.created_at)
  AND a.resolved_at IS NOT NULL
ORDER BY a.created_at ASC
```

**Configurações:**
- Visualization: Time series
- Unit: minutes
- Legend: Bottom

---

### Panel: Alertas Críticos Pendentes (Table)

**Descrição:** Lista de alertas críticos não resolvidos

```sql
SELECT
  UNIX_TIMESTAMP(a.timestamp) AS "Time",
  a.alert_type AS "Tipo",
  a.message AS "Mensagem",
  TIMESTAMPDIFF(MINUTE, a.timestamp, NOW()) AS "Idade (min)"
FROM alerts a
WHERE 
  a.status = 'active'
  AND a.severity = 'critical'
ORDER BY a.timestamp DESC
```

**Configurações:**
- Visualization: Table
- Highlight rows with Idade > 30

---

## 🔧 Variáveis para Dashboards Dinâmicos

### Variável: Tipo de Sensor

**Query:**
```sql
SELECT DISTINCT sensor_type FROM sensors ORDER BY sensor_type
```

**Uso no dashboard:**
```sql
WHERE sensor_type = '$sensor_type'
```

---

### Variável: Localização

**Query:**
```sql
SELECT DISTINCT location FROM sensors ORDER BY location
```

**Uso no dashboard:**
```sql
WHERE location = '$location'
```

---

### Variável: Nome da Piscina

**Query:**
```sql
SELECT DISTINCT pool_name FROM pool_readings ORDER BY pool_name
```

**Uso no dashboard:**
```sql
WHERE pool_name = '$pool_name'
```

---

## 💡 Dicas de Otimização

### 1. Use Índices nas Colunas de Timestamp

```sql
CREATE INDEX idx_readings_timestamp ON readings(timestamp);
CREATE INDEX idx_pool_readings_timestamp ON pool_readings(timestamp);
CREATE INDEX idx_alerts_timestamp ON alerts(timestamp);
CREATE INDEX idx_statistics_updated ON statistics(updated_at);
```

### 2. Use LIMIT nas Queries de Tabelas

```sql
-- Sempre limite resultados em tabelas
SELECT * FROM readings r
WHERE $__timeFilter(r.timestamp)
ORDER BY r.timestamp DESC
LIMIT 1000;
```

### 3. Agregue Dados para Períodos Longos

```sql
-- Para períodos > 24h, agrupe por hora
-- Para períodos > 7 dias, agrupe por dia
SELECT
  UNIX_TIMESTAMP(DATE_FORMAT(r.timestamp, '%Y-%m-%d 00:00:00')) AS time_sec,
  COUNT(*) AS value
FROM readings r
WHERE $__timeFilter(r.timestamp)
GROUP BY DATE(r.timestamp)
```

### 4. Use Cache de Queries

No Grafana, configure:
- Query caching: Enabled
- Cache timeout: 60 seconds (para dados em tempo real)
- Cache timeout: 300 seconds (para dados históricos)

---

## 📚 Referências

- [Grafana Time Series Panel](https://grafana.com/docs/grafana/latest/panels/visualizations/time-series/)
- [MySQL Data Source](https://grafana.com/docs/grafana/latest/datasources/mysql/)
- [Dashboard Variables](https://grafana.com/docs/grafana/latest/variables/)
- [Query Inspector](https://grafana.com/docs/grafana/latest/panels/inspect/)

---

**Sistema:** CEU Tres Pontes - Controle de Acesso  
**Versão:** 1.0  
**Data:** Outubro 2025
