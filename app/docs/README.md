# Sistema de Controle de Acesso - CEU Tres Pontes

## 📋 Visão Geral

Sistema de controle de acesso e contagem de pessoas para o parque "CEU Tres Pontes", utilizando simuladores de sensores IoT com diferentes protocolos de comunicação.

---

## 🎯 Objetivos do Sistema

- Contar quantas pessoas entraram e saíram do parque
- Monitorar fluxo de pessoas em tempo real
- Suportar múltiplos protocolos de comunicação IoT
- Fornecer dados para análise e tomada de decisão

---

## 🏗️ Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    PARQUE CEU TRES PONTES                    │
│                                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   LoRa   │  │  ZigBee  │  │  Sigfox  │  │   RFID   │   │
│  │  Sensor  │  │  Sensor  │  │  Sensor  │  │  Sensor  │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │             │              │             │          │
└───────┼─────────────┼──────────────┼─────────────┼──────────┘
        │             │              │             │
        └─────────────┴──────────────┴─────────────┘
                           │
                    ┌──────▼──────┐
                    │   Gateway   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ MQTT Broker │
                    │ (Mosquitto) │
                    └──────┬──────┘
                           │
            ┌──────────────┴──────────────┐
            │                             │
     ┌──────▼──────┐             ┌───────▼────────┐
     │   Backend   │             │   RabbitMQ     │
     │   (Flask)   │◄────────────┤  Message Queue │
     └──────┬──────┘             └────────────────┘
            │
     ┌──────▼──────┐
     │    MySQL    │
     │   Database  │
     └──────┬──────┘
            │
     ┌──────▼──────┐
     │  Dashboard  │
     │  (PowerBI)  │
     └─────────────┘
```

---

## 📦 FASE 1: Simuladores de Sensores

### Status: ✅ CONCLUÍDA

### Descrição
Implementação de simuladores para os 4 tipos de sensores IoT que serão utilizados no sistema.

### Tecnologias
- **Linguagem:** Python 3.12.3
- **Padrão de Design:** Orientação a Objetos (Abstract Base Class)

### Sensores Implementados

#### 1. 🌐 LoRa (Long Range)
- **Protocolo:** LoRaWAN
- **Frequência:** 915 MHz (Brasil)
- **Alcance:** 2-15 km (dependendo do SF)
- **Características:**
  - Spreading Factor ajustável (SF7-SF12)
  - Simulação de RSSI e SNR
  - Monitoramento de bateria
  - Baixo consumo de energia

**Arquivo:** `sensores/lora_sensor.py`

#### 2. 🔗 ZigBee
- **Protocolo:** IEEE 802.15.4
- **Frequência:** 2.4 GHz
- **Alcance:** 10-100 metros
- **Características:**
  - Rede Mesh (malha)
  - Tipos de nó: Coordinator, Router, End Device
  - Link Quality Indicator (LQI)
  - Descoberta de vizinhos

**Arquivo:** `sensores/zigbee_sensor.py`

#### 3. 📡 Sigfox
- **Protocolo:** LPWAN
- **Frequência:** 902 MHz (RCZ4 - Brasil)
- **Alcance:** Até 50 km
- **Características:**
  - Limite de 140 mensagens/dia
  - Payload de 12 bytes
  - Consumo ultra-baixo
  - Estimativa de vida útil da bateria

**Arquivo:** `sensores/sigfox_sensor.py`

#### 4. 📱 RFID
- **Protocolo:** ISO 14443/15693/18000-6C
- **Frequências:** LF (125 kHz), HF (13.56 MHz), UHF (915 MHz)
- **Alcance:** 0.1-100 metros (dependendo do tipo)
- **Características:**
  - Tags passivas e ativas
  - Leitura de múltiplas tags
  - Identificação única por EPC/UID
  - Controle de potência do leitor

**Arquivo:** `sensores/rfid_sensor.py`

---

## 📁 Estrutura de Arquivos

```
PI - IV - V1/
│
├── sensores/                    # Módulo de simuladores
│   ├── __init__.py             # Inicialização do módulo
│   ├── base_sensor.py          # Classe abstrata base
│   ├── lora_sensor.py          # Simulador LoRa
│   ├── zigbee_sensor.py        # Simulador ZigBee
│   ├── sigfox_sensor.py        # Simulador Sigfox
│   └── rfid_sensor.py          # Simulador RFID
│
├── tests/                       # Scripts de teste
│   └── test_simuladores.py     # Teste completo dos simuladores
│
├── backend/                     # Backend (Fase 2)
├── frontend/                    # Frontend (Fase 2)
├── config/                      # Configurações (Fase 2)
└── docs/                        # Documentação
    └── README.md               # Este arquivo
```

---

## 🚀 Como Usar os Simuladores

### Instalação
```bash
# Nenhuma dependência externa necessária para Fase 1
# Python 3.12+ já possui todas as bibliotecas necessárias
```

### Exemplo Básico

```python
from sensores import LoRaSensor, ZigBeeSensor, SigfoxSensor, RFIDSensor

# Criar sensores
lora = LoRaSensor(location="Entrada Principal")
zigbee = ZigBeeSensor(location="Saída Lateral", node_type="Router")
sigfox = SigfoxSensor(location="Portão Emergência")
rfid = RFIDSensor(location="Catraca", frequency_type="HF")

# Simular detecção
reading = lora.simulate_detection()
print(f"Atividade: {reading['activity']}")
print(f"Timestamp: {reading['timestamp']}")

# Obter status
status = lora.get_status()
print(f"Total de detecções: {status['total_detections']}")
```

### Executar Testes Completos

```bash
cd tests
python test_simuladores.py
```

---

## 📊 Dados Gerados

Cada sensor gera os seguintes dados:

### Dados Comuns (todos os sensores)
- `serial_number`: Número de série único
- `protocol`: Protocolo de comunicação
- `location`: Localização no parque
- `activity`: Detecção binária (0 ou 1)
- `timestamp`: Data/hora da leitura (ISO 8601)
- `total_detections`: Contador total de detecções

### Dados Específicos por Protocolo

**LoRa:**
- RSSI, SNR, Spreading Factor, Battery Level

**ZigBee:**
- LQI, Node Type, PAN ID, Neighbor Count, Hop Count

**Sigfox:**
- Device ID, Messages Sent, Battery Life Estimate

**RFID:**
- Tag ID, Tag Type, Read Range, Unique Tags Count

---

## 🔄 Próximas Fases

### Fase 2: Gateway e Comunicação MQTT
- [ ] Implementar gateway para coletar dados dos sensores
- [ ] Configurar Broker MQTT (Mosquitto)
- [ ] Protocolo de comunicação sensor → gateway → broker

### Fase 3: Backend
- [ ] API REST com Flask
- [ ] Integração com RabbitMQ
- [ ] Persistência em MySQL
- [ ] Docker containers

### Fase 4: Frontend
- [ ] Interface web (HTML5, CSS3, JavaScript)
- [ ] Dashboard em tempo real
- [ ] Visualização de dados

### Fase 5: Analytics e Dashboard
- [ ] Integração com PowerBI
- [ ] Relatórios e análises
- [ ] Exportação de dados

### Fase 6: Deployment
- [ ] Configuração Ubuntu Server
- [ ] NGINX como reverse proxy
- [ ] Orquestração com Docker Compose
- [ ] Monitoramento e logs

---

## 🛠️ Stack Tecnológico Completo

### Infraestrutura
- **SO:** Ubuntu 25.04
- **Servidor Web:** NGINX 1.29.1
- **Containers:** Docker 27.5.1

### Backend
- **Linguagem:** Python 3.12.3
- **Framework:** Flask
- **Message Broker:** RabbitMQ 3.13
- **MQTT Broker:** Mosquitto
- **Bibliotecas:** Pandas, NumPy, PySpark

### Banco de Dados
- **SGBD:** MySQL 8.0.43

### Frontend
- **HTML5, CSS3, JavaScript**

### Analytics
- **PowerBI**

### Protocolos IoT
- **LoRa / LoRaWAN**
- **ZigBee (IEEE 802.15.4)**
- **Sigfox**
- **RFID**

---

## 📝 Convenções de Código

### Python
- PEP 8 Style Guide
- Type hints quando apropriado
- Docstrings para classes e métodos
- Nomes descritivos em português/inglês

### Git
- Commits descritivos
- Branches por feature
- Pull requests para revisão

---

## 🤝 Contribuindo

Este é um projeto acadêmico. Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Projeto Acadêmico - CEU Tres Pontes

---

## 👥 Autores

Desenvolvido como parte do projeto de Internet das Coisas (IoT)

---

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação ou entre em contato com a equipe do projeto.

---

**Última atualização:** Outubro 2025
**Versão:** 1.0.0 (Fase 1 Completa)
