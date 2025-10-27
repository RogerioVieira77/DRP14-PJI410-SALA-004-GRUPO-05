# Sistema de Controle de Acesso - CEU Tres Pontes

Sistema IoT de controle de acesso e contagem de pessoas utilizando múltiplos protocolos de comunicação.

## 🎯 Fase Atual: FASE 2 - ✅

### Status Fase 1
- ✅ Simulador LoRa
- ✅ Simulador ZigBee  
- ✅ Simulador Sigfox
- ✅ Simulador RFID
- ✅ Testes Automatizados
- ✅ Documentação

### Status Fase 2
- ✅ Gateway implementado
- ✅ Cliente MQTT (Publisher/Subscriber)
- ✅ Formatador de mensagens JSON
- ✅ Subscriber com callbacks
- ✅ Integração com Mosquitto
- ✅ Testes de integração
- ✅ Documentação completa




## 📚 Documentação Completa

Veja a documentação detalhada em: [`docs/README.md`](docs/README.md)

## 🏗️ Estrutura do Projeto

```
PI - IV - V1/
├── sensores/          # Simuladores IoT (Fase 1) ✅
├── backend/
│   ├── gateway/       # Gateway e MQTT (Fase 2) ✅
│   └── config/        # Configurações MQTT ✅
├── frontend/          # Interface Web (Fase 3)
├── tests/             # Testes ✅
├── docs/              # Documentação ✅
└── logs/              # Logs do sistema
```

## 🌐 Protocolos Suportados

- **LoRa** - Longo alcance (até 15 km)
- **ZigBee** - Rede mesh
- **Sigfox** - LPWAN global
- **RFID** - Identificação por proximidade

## 🛠️ Tecnologias

- Python 3.12.3
- Mosquitto MQTT Broker
- paho-mqtt 1.6.1
- Flask
- MySQL 8.0.43
- Docker 27.5.1
- RabbitMQ 3.13
- Grafana (Dashboards)
- PowerBI

## 📊 Dashboards e Visualização

O projeto inclui dashboards interativos com Grafana para monitoramento em tempo real:

- **Monitoramento de Sensores** - Leituras por tipo, local e período
- **Análise de Piscinas** - Ocupação, temperatura, pH e qualidade da água
- **Estatísticas Gerais** - Padrões de acesso, média de visitantes, tendências
- **Alertas e Segurança** - Monitoramento de eventos críticos

### 🚀 Instalação Rápida do Grafana

```bash
# Instalar Grafana
sudo bash install_grafana.sh

# Configurar banco de dados
sudo bash configure_grafana_datasource.sh

# Configurar acesso via web
sudo bash configure_grafana_nginx.sh

# Verificar instalação
bash check_grafana.sh
```

### 📚 Documentação Grafana

- [Guia Completo de Instalação](docs/GRAFANA_SETUP_GUIDE.md)
- [Queries SQL Prontas](docs/GRAFANA_QUERIES.md)
- [Início Rápido](docs/GRAFANA_QUICKSTART.md)

---
**Desenvolvido: UNIVESP - DRP14-PJI410-SALA-004GRUPO-005**
