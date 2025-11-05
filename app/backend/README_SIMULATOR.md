# 🎯 Simulador de Eventos de Sensores - SmartCEU

## 📋 Descrição

Script Python para simular eventos em tempo real de todos os sensores do parque CEU Três Pontes, gerando leituras realistas nas tabelas `readings` e `pool_readings` como se fossem atividades reais acontecendo no parque.

## 📂 Localização

```bash
/var/www/smartceu/app/backend/simulate_sensor_events.py
```

## 🎪 Tipos de Eventos Simulados

### Sensores Normais (tabela `readings`)
- **LoRa**: Detecção de presença por radiofrequência
- **Zigbee**: Sensores PIR (presença infravermelha)
- **Sigfox**: Temperatura e umidade (DHT22)
- **RFID**: Qualidade do ar (MQ135)

### Sensores da Piscina (tabela `pool_readings`)
- **water_temp**: Temperatura da água (26-28°C)
- **ambient_temp**: Temperatura ambiente (20-34°C)
- **water_quality**: Qualidade da água (pH, cloro, alcalinidade)

## 🚀 Como Usar

### Instalação

O script usa o ambiente virtual do projeto:

```bash
cd /var/www/smartceu/app/backend
source /var/www/smartceu/venv/bin/activate
```

### Uso Básico

#### 1. Gerar eventos continuamente (Ctrl+C para parar)
```bash
python3 simulate_sensor_events.py
```

#### 2. Gerar eventos por um período específico
```bash
# Executar por 1 hora
python3 simulate_sensor_events.py --duration 60

# Executar por 30 minutos
python3 simulate_sensor_events.py --duration 30
```

#### 3. Ajustar intervalo entre eventos
```bash
# Eventos a cada 15 segundos
python3 simulate_sensor_events.py --interval 15

# Eventos a cada 60 segundos (1 minuto)
python3 simulate_sensor_events.py --interval 60
```

#### 4. Modo Batch (gerar N eventos de uma vez)
```bash
# Gerar 100 eventos
python3 simulate_sensor_events.py --batch 100

# Gerar 500 eventos
python3 simulate_sensor_events.py --batch 500
```

#### 5. Combinar opções
```bash
# 2 horas de simulação com eventos a cada 20 segundos
python3 simulate_sensor_events.py --duration 120 --interval 20
```

## 📊 Exemplos de Saída

```
======================================================================
🎯 SIMULADOR DE EVENTOS DE SENSORES - SmartCEU
======================================================================

⏱️  Intervalo: 30 segundos
♾️  Duração: Infinito (Ctrl+C para parar)
🎚️  Filtro: all

======================================================================

[0001] 16:10:35 (+0s) - Quadra de Esportes [LORA-A1B2C3D4] - LORA - ✓ Presença - 75.3 - 🔋89%
[0002] 16:11:05 (+30s) - 🌊 Piscina - Temp. Água: 27.5°C
[0003] 16:11:35 (+60s) - Biblioteca [SIGF-I9J0K1L2] - DHT22 - ○ Vazio - 23.4 - 🔋92%
[0004] 16:12:05 (+90s) - 🌡️ Piscina - Temp. Ambiente: 28.7°C
[0005] 16:12:35 (+120s) - Área da Piscina [LORA-Q7R8S9T0] - LORA - ✓ Presença - 82.1 - 🔋95%
[0006] 16:13:05 (+150s) - 💧 Piscina - Qualidade: pH 7.4, Cloro 2.1ppm
[0007] 16:13:35 (+180s) - Quadra de Esportes [ZIGB-E5F6G7H8] - PIR - ○ Vazio - 0.0 - 🔋88%

... (Ctrl+C para parar)

======================================================================
📊 ESTATÍSTICAS DA SIMULAÇÃO
======================================================================
🎯 Total de eventos: 247
⏱️  Duração: 7410 segundos (123m 30s)
⚡ Taxa: 2.0 eventos/minuto
======================================================================

✅ Simulação finalizada com sucesso!
```

## 🎛️ Opções Disponíveis

| Opção | Tipo | Padrão | Descrição |
|-------|------|--------|-----------|
| `--interval` | int | 30 | Intervalo entre eventos em segundos |
| `--duration` | int | 0 | Duração da simulação em minutos (0 = infinito) |
| `--batch` | int | 0 | Gerar N eventos e sair (modo batch) |
| `--sensor` | str | all | Tipo de sensor (all, pool, presence, environment) |

## 🕐 Padrões de Atividade

O simulador ajusta a geração de eventos baseado no horário:

### Horários de Pico (multiplicador 1.5x)
- **9h-11h**: Manhã movimentada
- **14h-17h**: Tarde intensa

### Horário Normal (multiplicador 1.0x)
- **7h-9h**: Início das atividades
- **11h-14h**: Meio do dia
- **17h-20h**: Fim de tarde/noite

### Horário Baixo (multiplicador 0.3x)
- **6h-7h**: Abertura
- **20h-22h**: Encerrando

### CEU Fechado (multiplicador 0.0x)
- **22h-6h**: Sem eventos gerados

## 📈 Dados Gerados

### Sensores Normais (readings)

Campos preenchidos:
- `sensor_id`: ID do sensor (1-6)
- `activity`: 0 (sem detecção) ou 1 (presença detectada)
- `timestamp`: Data/hora atual
- `sensor_metadata`: JSON com:
  - `battery_level`: 55-100%
  - `protocol`: Tipo de protocolo
  - `value`: Valor da leitura
  - Dados específicos por tipo

### Sensores da Piscina (pool_readings)

Campos preenchidos:
- `sensor_type`: water_temp, ambient_temp, water_quality
- `reading_date`: Data atual
- `reading_time`: Hora atual
- `temperature`: Temperatura medida (quando aplicável)
- `water_quality`: Classificação (Ótima, Boa, Regular, Imprópria)

## 🎪 Cenários de Uso

### 1. Teste Rápido (gerar dados para visualizar no dashboard)
```bash
python3 simulate_sensor_events.py --batch 50
```

### 2. Simulação de Dia Inteiro (executar em background)
```bash
nohup python3 simulate_sensor_events.py --duration 960 --interval 10 > simulation.log 2>&1 &
```

### 3. Demonstração ao Vivo
```bash
python3 simulate_sensor_events.py --interval 5
```

### 4. Popular Banco com Muitos Dados
```bash
python3 simulate_sensor_events.py --batch 1000
```

### 5. Teste de Carga
```bash
python3 simulate_sensor_events.py --interval 1 --duration 10
```

## 🔍 Verificar Dados Gerados

### Via MySQL
```bash
mysql -u smartceu_user -p smartceu_db -e "SELECT COUNT(*) as total FROM readings;"
mysql -u smartceu_user -p smartceu_db -e "SELECT COUNT(*) as total FROM pool_readings;"
```

### Via Dashboard
Acesse: http://82.25.75.88/smartceu/dashboard/

## 🛠️ Troubleshooting

### Erro: "No module named 'app'"

**Solução**: Certifique-se de estar executando do diretório backend:
```bash
cd /var/www/smartceu/app/backend
```

### Erro: "connection refused"

**Solução**: Verifique se o MySQL está rodando:
```bash
sudo systemctl status mysql
```

### Erro: "sensor_id not found"

**Solução**: Verifique se os sensores estão cadastrados:
```bash
python3 -c "from app import create_app, db; from app.models.sensor import Sensor; app = create_app(); app.app_context().push(); print(f'Sensores: {Sensor.query.count()}')"
```

## 📝 Logs

Os eventos são exibidos em tempo real no terminal. Para salvar em arquivo:

```bash
python3 simulate_sensor_events.py --batch 100 > eventos.log 2>&1
```

## 🔄 Integração com o Sistema

O simulador gera eventos que são imediatamente visíveis em:

1. **Dashboard Principal**: Contadores e estatísticas
2. **Página de Áreas**: Ocupação por área
3. **Página de Alertas**: Detecções recentes
4. **Página de Piscina**: Temperatura e qualidade da água
5. **Resumo de Sensores**: Status e leituras de todos os sensores

## ⚙️ Configuração Avançada

Para modificar os padrões de comportamento, edite o arquivo `simulate_sensor_events.py`:

- `get_activity_multiplier()`: Ajustar horários de pico
- `generate_*_reading()`: Modificar rangesdos valores gerados
- `AREAS`: Adicionar/remover áreas e sensores

## 📊 Estatísticas Realistas

O simulador gera dados baseados em padrões reais:

- **Temperatura da água**: 26-28°C (variação mínima)
- **Temperatura ambiente**: 20-34°C (varia com o horário)
- **pH da água**: 7.1-7.7 (ideal: 7.2-7.6)
- **Cloro livre**: 0.8-3.5 ppm (ideal: 1.0-3.0)
- **Alcalinidade**: 75-125 ppm (ideal: 80-120)
- **Bateria dos sensores**: 55-100%
- **Detecção de presença**: Varia com horário e área

---

**Desenvolvido para**: SmartCEU - Sistema de Monitoramento CEU Três Pontes  
**Versão**: 1.0.0  
**Data**: 2025-11-01
