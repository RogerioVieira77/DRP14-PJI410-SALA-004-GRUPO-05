# Templates de Dashboard Grafana
## CEU Tres Pontes - Importação Rápida

Este documento contém templates prontos de dashboards que podem ser importados diretamente no Grafana.

---

## 📥 Como Importar

1. **Acesse o Grafana**
2. **Menu lateral** → **+** → **Import**
3. Cole o JSON do dashboard desejado
4. **Selecione o Data Source:** `CEU Tres Pontes DB`
5. **Clique em Import**

---

## 🎨 Dashboard Templates

### Template 1: Overview do Sistema

Este é um dashboard de visão geral com as principais métricas.

**Nome sugerido:** CEU Tres Pontes - Overview

**Descrição:** Dashboard principal com visão geral do sistema

**Tags:** overview, real-time, ceu

**Painéis incluídos:**
- Total de pessoas atual
- Leituras nas últimas 24h
- Sensores ativos
- Alertas críticos
- Gráfico de entradas/saídas
- Ocupação por local

**Instruções para criar manualmente:**

1. **Criar novo dashboard**
2. **Adicionar panels com as seguintes configurações:**

#### Panel 1: Total de Pessoas (Stat)
```json
{
  "query": "SELECT UNIX_TIMESTAMP(NOW()) AS time_sec, total_count AS value FROM statistics ORDER BY updated_at DESC LIMIT 1",
  "title": "Total de Pessoas Atual",
  "type": "stat",
  "unit": "people",
  "colorMode": "value"
}
```

#### Panel 2: Leituras 24h (Stat)
```json
{
  "query": "SELECT UNIX_TIMESTAMP(NOW()) AS time_sec, COUNT(*) AS value FROM readings WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)",
  "title": "Leituras (24h)",
  "type": "stat",
  "unit": "short"
}
```

#### Panel 3: Entradas vs Saídas (Time Series)
```json
{
  "query": "SELECT UNIX_TIMESTAMP(DATE_FORMAT(timestamp, '%Y-%m-%d %H:%i:00')) AS time_sec, reading_type AS metric, COUNT(*) AS value FROM readings WHERE $__timeFilter(timestamp) AND reading_type IN ('ENTRY', 'EXIT') GROUP BY time_sec, reading_type ORDER BY time_sec",
  "title": "Entradas vs Saídas",
  "type": "timeseries"
}
```

---

### Template 2: Monitoramento de Piscinas

Dashboard focado no monitoramento das piscinas.

**Nome sugerido:** CEU Tres Pontes - Piscinas

**Descrição:** Monitoramento de ocupação e qualidade da água das piscinas

**Tags:** piscinas, water-quality, occupancy

**Painéis incluídos:**
- Ocupação atual (gauge)
- Temperatura da água (time series)
- pH da água (gauge)
- Nível de cloro (time series)
- Turbidez (time series)
- Histórico de ocupação

#### Exemplo de configuração (JSON parcial):

```json
{
  "title": "Ocupação das Piscinas",
  "type": "gauge",
  "targets": [
    {
      "rawSql": "SELECT pool_name AS metric, current_occupancy AS value FROM pool_readings WHERE timestamp = (SELECT MAX(timestamp) FROM pool_readings)",
      "format": "table"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "people",
      "min": 0,
      "max": 100,
      "thresholds": {
        "mode": "absolute",
        "steps": [
          { "value": 0, "color": "green" },
          { "value": 50, "color": "yellow" },
          { "value": 80, "color": "red" }
        ]
      }
    }
  }
}
```

---

### Template 3: Análise Estatística

Dashboard com análises e estatísticas avançadas.

**Nome sugerido:** CEU Tres Pontes - Estatísticas

**Descrição:** Análises e estatísticas de uso do sistema

**Tags:** statistics, analysis, reports

**Painéis incluídos:**
- Média de visitantes por dia da semana
- Horários de pico
- Top 10 sensores mais ativos
- Comparação mensal
- Taxa de crescimento
- Heatmap de atividades

---

## 🔧 Variáveis Globais Recomendadas

Configure estas variáveis para tornar os dashboards dinâmicos:

### Variável: Intervalo de Tempo
```
Name: time_range
Type: Interval
Options: 5m,15m,30m,1h,6h,12h,1d,7d,30d
Auto: true
```

### Variável: Tipo de Sensor
```
Name: sensor_type
Type: Query
Query: SELECT DISTINCT sensor_type FROM sensors ORDER BY sensor_type
Multi-value: true
Include All: true
```

### Variável: Localização
```
Name: location
Type: Query
Query: SELECT DISTINCT location FROM sensors ORDER BY location
Multi-value: true
Include All: true
```

### Variável: Nome da Piscina
```
Name: pool_name
Type: Query
Query: SELECT DISTINCT pool_name FROM pool_readings ORDER BY pool_name
Multi-value: true
Include All: true
```

---

## 📋 Dashboard Completo (JSON)

Aqui está um dashboard completo de exemplo que você pode copiar e importar:

```json
{
  "dashboard": {
    "title": "CEU Tres Pontes - Monitoramento Geral",
    "tags": ["ceu", "iot", "monitoring"],
    "timezone": "America/Sao_Paulo",
    "schemaVersion": 38,
    "version": 1,
    "refresh": "30s",
    "time": {
      "from": "now-6h",
      "to": "now"
    },
    "panels": [
      {
        "id": 1,
        "type": "stat",
        "title": "Total de Pessoas",
        "gridPos": { "x": 0, "y": 0, "w": 6, "h": 4 },
        "targets": [
          {
            "rawSql": "SELECT UNIX_TIMESTAMP(NOW()) AS time_sec, total_count AS value FROM statistics ORDER BY updated_at DESC LIMIT 1",
            "format": "time_series"
          }
        ],
        "options": {
          "colorMode": "value",
          "graphMode": "area",
          "orientation": "auto",
          "reduceOptions": {
            "values": false,
            "calcs": ["lastNotNull"],
            "fields": ""
          }
        },
        "fieldConfig": {
          "defaults": {
            "unit": "people",
            "color": { "mode": "thresholds" },
            "thresholds": {
              "mode": "absolute",
              "steps": [
                { "value": 0, "color": "green" },
                { "value": 3000, "color": "yellow" },
                { "value": 4500, "color": "red" }
              ]
            }
          }
        }
      },
      {
        "id": 2,
        "type": "stat",
        "title": "Leituras (24h)",
        "gridPos": { "x": 6, "y": 0, "w": 6, "h": 4 },
        "targets": [
          {
            "rawSql": "SELECT UNIX_TIMESTAMP(NOW()) AS time_sec, COUNT(*) AS value FROM readings WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)",
            "format": "time_series"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "short",
            "color": { "mode": "palette-classic" }
          }
        }
      },
      {
        "id": 3,
        "type": "stat",
        "title": "Sensores Ativos",
        "gridPos": { "x": 12, "y": 0, "w": 6, "h": 4 },
        "targets": [
          {
            "rawSql": "SELECT UNIX_TIMESTAMP(NOW()) AS time_sec, COUNT(*) AS value FROM sensors WHERE status = 'active'",
            "format": "time_series"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "short",
            "color": { "mode": "thresholds" },
            "thresholds": {
              "mode": "absolute",
              "steps": [
                { "value": 0, "color": "red" },
                { "value": 10, "color": "yellow" },
                { "value": 15, "color": "green" }
              ]
            }
          }
        }
      },
      {
        "id": 4,
        "type": "stat",
        "title": "Alertas Ativos",
        "gridPos": { "x": 18, "y": 0, "w": 6, "h": 4 },
        "targets": [
          {
            "rawSql": "SELECT UNIX_TIMESTAMP(NOW()) AS time_sec, COUNT(*) AS value FROM alerts WHERE status = 'active'",
            "format": "time_series"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "short",
            "color": { "mode": "thresholds" },
            "thresholds": {
              "mode": "absolute",
              "steps": [
                { "value": 0, "color": "green" },
                { "value": 1, "color": "yellow" },
                { "value": 5, "color": "red" }
              ]
            }
          }
        }
      },
      {
        "id": 5,
        "type": "timeseries",
        "title": "Leituras por Tipo de Sensor",
        "gridPos": { "x": 0, "y": 4, "w": 24, "h": 8 },
        "targets": [
          {
            "rawSql": "SELECT UNIX_TIMESTAMP(DATE_FORMAT(r.timestamp, '%Y-%m-%d %H:%i:00')) AS time_sec, s.sensor_type AS metric, COUNT(*) AS value FROM readings r JOIN sensors s ON r.sensor_id = s.id WHERE $__timeFilter(r.timestamp) GROUP BY time_sec, s.sensor_type ORDER BY time_sec",
            "format": "time_series"
          }
        ],
        "options": {
          "legend": {
            "displayMode": "list",
            "placement": "bottom"
          }
        },
        "fieldConfig": {
          "defaults": {
            "unit": "short",
            "custom": {
              "drawStyle": "line",
              "lineInterpolation": "smooth",
              "fillOpacity": 10
            }
          }
        }
      }
    ]
  }
}
```

---

## 🎨 Temas de Cores Recomendados

### Esquema de Cores para Sensores
- **LoRa:** `#FF6B6B` (Vermelho claro)
- **ZigBee:** `#4ECDC4` (Turquesa)
- **Sigfox:** `#45B7D1` (Azul claro)
- **RFID:** `#FFA07A` (Salmão)

### Thresholds Padrão

#### Ocupação
- 0-50%: Verde (`#73BF69`)
- 51-80%: Amarelo (`#F2CC0C`)
- 81-100%: Vermelho (`#E02F44`)

#### Qualidade da Água (pH)
- 7.0-7.6: Verde (ideal)
- 6.5-7.0 ou 7.6-8.0: Amarelo (aceitável)
- < 6.5 ou > 8.0: Vermelho (crítico)

#### Temperatura da Água
- 24-28°C: Verde (ideal)
- 22-24°C ou 28-30°C: Amarelo
- < 22°C ou > 30°C: Vermelho

---

## 📊 Configurações de Display Recomendadas

### Time Series Panels
```json
{
  "custom": {
    "drawStyle": "line",
    "lineInterpolation": "smooth",
    "lineWidth": 2,
    "fillOpacity": 10,
    "gradientMode": "none",
    "showPoints": "never",
    "pointSize": 5,
    "stacking": {
      "mode": "none",
      "group": "A"
    }
  }
}
```

### Stat Panels
```json
{
  "colorMode": "value",
  "graphMode": "area",
  "orientation": "auto",
  "textMode": "auto",
  "reduceOptions": {
    "values": false,
    "calcs": ["lastNotNull"],
    "fields": ""
  }
}
```

### Table Panels
```json
{
  "showHeader": true,
  "sortBy": [
    {
      "displayName": "Time",
      "desc": true
    }
  ],
  "displayMode": "color-background"
}
```

---

## 🔄 Refresh Rates Recomendadas

- **Dashboard em Tempo Real:** 10s - 30s
- **Dashboard de Análise:** 1m - 5m
- **Dashboard de Relatórios:** 5m - 15m

---

## 📝 Notas Importantes

1. **Antes de importar**, certifique-se de que:
   - O data source está configurado
   - As tabelas do banco existem
   - Há dados para visualizar

2. **Após importar**:
   - Ajuste o timezone se necessário
   - Configure as variáveis
   - Personalize as cores e thresholds
   - Ajuste o refresh rate

3. **Para exportar** um dashboard:
   - Abra o dashboard
   - Settings (⚙️) → JSON Model
   - Copie o JSON
   - Salve em arquivo

---

## 🚀 Próximos Passos

1. Importe o dashboard básico
2. Personalize conforme suas necessidades
3. Adicione novos painéis
4. Configure alertas
5. Compartilhe com a equipe!

---

**Sistema:** CEU Tres Pontes - Controle de Acesso  
**Versão:** 1.0  
**Data:** Outubro 2025
