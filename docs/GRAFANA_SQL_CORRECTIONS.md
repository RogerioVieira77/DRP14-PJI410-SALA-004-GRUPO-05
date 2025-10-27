# Correções de Sintaxe MySQL para Grafana

## 📋 Resumo das Correções

Este documento detalha as correções aplicadas nas queries SQL dos documentos de Grafana para garantir compatibilidade total com MySQL e o Grafana.

---

## 🔍 Problemas Identificados

### 1. **Aliases em GROUP BY**
❌ **Problema:** MySQL não permite usar aliases (apelidos) de colunas calculadas diretamente no GROUP BY.

```sql
-- INCORRETO
SELECT
  UNIX_TIMESTAMP(timestamp) AS time_sec,
  sensor_type AS metric,
  COUNT(*) AS value
FROM readings r
WHERE $__timeFilter(timestamp)
GROUP BY time_sec, metric  -- ❌ Não funciona no MySQL
```

✅ **Solução:** Repetir a expressão completa no GROUP BY.

```sql
-- CORRETO
SELECT
  UNIX_TIMESTAMP(r.timestamp) AS time_sec,
  s.sensor_type AS metric,
  COUNT(*) AS value
FROM readings r
JOIN sensors s ON r.sensor_id = s.id
WHERE $__timeFilter(r.timestamp)
GROUP BY 
  UNIX_TIMESTAMP(r.timestamp),  -- ✅ Expressão completa
  s.sensor_type                  -- ✅ Referência à tabela
ORDER BY time_sec ASC
```

---

### 2. **Referências Ambíguas de Colunas**
❌ **Problema:** Em queries com JOINs, colunas sem prefixo de tabela podem causar ambiguidade.

```sql
-- INCORRETO
SELECT
  location AS metric,
  COUNT(*) AS value
FROM readings r
JOIN sensors s ON r.sensor_id = s.id
WHERE $__timeFilter(timestamp)  -- ❌ Qual timestamp? De readings ou sensors?
GROUP BY location               -- ❌ De qual tabela?
```

✅ **Solução:** Sempre prefixar colunas com o alias da tabela.

```sql
-- CORRETO
SELECT
  s.location AS metric,
  COUNT(*) AS value
FROM readings r
JOIN sensors s ON r.sensor_id = s.id
WHERE $__timeFilter(r.timestamp)  -- ✅ Especifica r.timestamp
GROUP BY s.location               -- ✅ Especifica s.location
ORDER BY value DESC
```

---

### 3. **Uso Correto de $__timeFilter()**
❌ **Problema:** Macro do Grafana sem especificar a coluna de timestamp corretamente.

```sql
-- PODE CAUSAR PROBLEMAS
WHERE $__timeFilter(timestamp)  -- Se houver JOIN, pode ser ambíguo
```

✅ **Solução:** Sempre usar a referência completa com alias da tabela.

```sql
-- CORRETO
WHERE $__timeFilter(r.timestamp)    -- Para readings
WHERE $__timeFilter(pr.timestamp)   -- Para pool_readings
WHERE $__timeFilter(a.created_at)   -- Para alerts
```

---

## 📝 Arquivos Corrigidos

### 1. **GRAFANA_SETUP_GUIDE.md**
Total de correções: **8 queries**

- Panel: Leituras Recentes por Tipo de Sensor
- Panel: Ocupação por Local
- Panel: Alertas Ativos
- Panel: Ocupação das Piscinas
- Panel: Temperatura da Água
- Panel: pH da Água
- Panel: Leituras por Hora
- Panel: Média de Pessoas por Dia

### 2. **GRAFANA_QUERIES.md**
Total de correções: **15+ queries**

- Taxa de Entrada vs Saída
- Leituras por Local (já estava correto)
- Alertas Ativos (Table)
- Ocupação das Piscinas (múltiplas queries)
- Temperatura, pH, Cloro, Turbidez (pool_readings)
- Mapa de Calor de Tráfego
- Média por Dia da Semana
- Comparação Mensal
- Alertas por Tipo
- Tempo de Resposta a Alertas
- Alertas Críticos Pendentes
- Queries de otimização

---

## 🎯 Padrões de Boas Práticas Aplicados

### 1. **Sempre Use Aliases de Tabela**
```sql
-- BOM
FROM readings r
JOIN sensors s ON r.sensor_id = s.id

-- EVITE
FROM readings
JOIN sensors ON readings.sensor_id = sensors.id
```

### 2. **Sempre Qualifique Colunas em JOINs**
```sql
-- BOM
SELECT
  r.id,
  r.timestamp,
  s.sensor_type,
  s.location
FROM readings r
JOIN sensors s ON r.sensor_id = s.id

-- EVITE
SELECT
  id,           -- De qual tabela?
  timestamp,    -- De qual tabela?
  sensor_type,
  location
FROM readings r
JOIN sensors s ON r.sensor_id = s.id
```

### 3. **GROUP BY com Expressões Completas**
```sql
-- BOM
SELECT
  DATE_FORMAT(r.timestamp, '%Y-%m-%d') AS date,
  COUNT(*) AS total
FROM readings r
GROUP BY DATE_FORMAT(r.timestamp, '%Y-%m-%d')  -- Repete a expressão

-- EVITE
SELECT
  DATE_FORMAT(r.timestamp, '%Y-%m-%d') AS date,
  COUNT(*) AS total
FROM readings r
GROUP BY date  -- MySQL pode não aceitar em alguns modos SQL
```

### 4. **Funções de Data do MySQL**
```sql
-- Funções corretas do MySQL
DATE_FORMAT(timestamp, '%Y-%m-%d %H:00:00')  -- Formatação personalizada
UNIX_TIMESTAMP(timestamp)                     -- Converter para UNIX timestamp
DATE(timestamp)                               -- Extrair apenas data
HOUR(timestamp)                               -- Extrair apenas hora
DAYOFWEEK(timestamp)                          -- Dia da semana (1=Domingo, 7=Sábado)
TIMESTAMPDIFF(MINUTE, start, end)             -- Diferença em minutos
```

---

## ✅ Checklist de Validação de Queries

Antes de usar uma query no Grafana, verifique:

- [ ] Todas as colunas em JOINs estão prefixadas com alias da tabela
- [ ] $__timeFilter() usa referência completa: `$__timeFilter(r.timestamp)`
- [ ] GROUP BY repete expressões completas (não usa aliases)
- [ ] ORDER BY pode usar aliases (isso é permitido no MySQL)
- [ ] Funções de data são do MySQL (não PostgreSQL ou SQL Server)
- [ ] LIMIT está presente em queries de tabelas para evitar sobrecarga
- [ ] A query retorna as colunas esperadas pelo Grafana:
  - `time_sec` (UNIX_TIMESTAMP)
  - `metric` (nome da série)
  - `value` (valor numérico)

---

## 🧪 Testando Queries

### Teste 1: Verificar Sintaxe no MySQL
```bash
# Conectar ao MySQL
mysql -u grafana_reader -p -h localhost smartceu_db

# Testar query (substitua $__timeFilter por intervalo real)
SELECT
  UNIX_TIMESTAMP(r.timestamp) AS time_sec,
  s.sensor_type AS metric,
  COUNT(*) AS value
FROM readings r
JOIN sensors s ON r.sensor_id = s.id
WHERE r.timestamp >= NOW() - INTERVAL 1 HOUR
  AND r.timestamp <= NOW()
GROUP BY 
  UNIX_TIMESTAMP(r.timestamp),
  s.sensor_type
ORDER BY time_sec ASC;
```

### Teste 2: Verificar no Grafana
1. Abra o panel
2. Clique em "Edit"
3. Clique em "Query Inspector"
4. Veja a query expandida (com macros substituídas)
5. Copie e teste no MySQL diretamente

---

## 📚 Macros do Grafana para MySQL

### $__timeFilter(columnName)
```sql
-- Expande para:
columnName BETWEEN FROM_UNIXTIME(1234567890) AND FROM_UNIXTIME(1234567899)
```

### $__timeFrom() e $__timeTo()
```sql
-- Usados quando você precisa de controle manual
WHERE timestamp >= FROM_UNIXTIME($__timeFrom / 1000)
  AND timestamp <= FROM_UNIXTIME($__timeTo / 1000)
```

### $__timeGroup(columnName, interval)
```sql
-- Agrupa por intervalo de tempo
SELECT
  $__timeGroup(timestamp, '5m') AS time,
  COUNT(*) AS value
FROM readings
WHERE $__timeFilter(timestamp)
GROUP BY time
ORDER BY time
```

---

## 🔗 Diferenças SQL vs MySQL

| Recurso | SQL Padrão | MySQL | Usado nas Queries |
|---------|-----------|-------|-------------------|
| Timestamp Unix | varies | `UNIX_TIMESTAMP()` | ✅ Sim |
| Formatação Data | varies | `DATE_FORMAT()` | ✅ Sim |
| Extrair Data | `CAST(date)` | `DATE()` | ✅ Sim |
| Diferença Tempo | varies | `TIMESTAMPDIFF()` | ✅ Sim |
| Dia da Semana | varies | `DAYOFWEEK()` | ✅ Sim |
| Aliases em GROUP BY | Permitido | Depende do sql_mode | ❌ Evitado |

---

## 📝 Exemplo Completo: Antes e Depois

### ❌ ANTES (Incorreto)
```sql
SELECT
  UNIX_TIMESTAMP(timestamp) AS time_sec,
  sensor_type AS metric,
  COUNT(*) AS value
FROM readings r
JOIN sensors s ON r.sensor_id = s.id
WHERE $__timeFilter(timestamp)
GROUP BY time_sec, metric
ORDER BY time_sec ASC
```

**Problemas:**
1. `timestamp` sem prefixo (ambíguo)
2. `GROUP BY time_sec, metric` usando aliases (não funciona em todos os modos MySQL)
3. `$__timeFilter(timestamp)` sem prefixo

### ✅ DEPOIS (Correto)
```sql
SELECT
  UNIX_TIMESTAMP(r.timestamp) AS time_sec,
  s.sensor_type AS metric,
  COUNT(*) AS value
FROM readings r
JOIN sensors s ON r.sensor_id = s.id
WHERE $__timeFilter(r.timestamp)
GROUP BY 
  UNIX_TIMESTAMP(r.timestamp),
  s.sensor_type
ORDER BY time_sec ASC
```

**Correções aplicadas:**
1. ✅ Todas as colunas prefixadas (`r.timestamp`, `s.sensor_type`)
2. ✅ GROUP BY com expressões completas
3. ✅ $__timeFilter() com prefixo (`r.timestamp`)
4. ✅ ORDER BY pode usar alias (permitido no MySQL)

---

## 🚀 Próximos Passos

1. **Verificar todas as queries** nos dashboards existentes
2. **Testar queries** diretamente no MySQL antes de usar no Grafana
3. **Adicionar índices** nas colunas de timestamp para melhor performance:
   ```sql
   CREATE INDEX idx_readings_timestamp ON readings(timestamp);
   CREATE INDEX idx_pool_readings_timestamp ON pool_readings(timestamp);
   CREATE INDEX idx_alerts_timestamp ON alerts(timestamp);
   ```
4. **Monitorar performance** das queries no Grafana Query Inspector
5. **Documentar** novas queries seguindo os padrões corrigidos

---

## 📞 Suporte

Para dúvidas sobre sintaxe MySQL ou queries do Grafana:
- [MySQL 8.0 Reference Manual](https://dev.mysql.com/doc/refman/8.0/en/)
- [Grafana MySQL Data Source](https://grafana.com/docs/grafana/latest/datasources/mysql/)
- Documentação do projeto: `/docs/README.md`

---

**Desenvolvido por:** UNIVESP - DRP14-PJI410-SALA-004-GRUPO-05  
**Sistema:** CEU Tres Pontes - Controle de Acesso  
**Data:** Outubro 2025  
**Versão:** 1.0
