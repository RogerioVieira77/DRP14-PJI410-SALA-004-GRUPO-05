# 📖 Índice da Documentação
## Sistema de Controle de Acesso - CEU Tres Pontes

---

## 🚀 INÍCIO RÁPIDO

### Para Começar Imediatamente:
1. **[README Principal](../README.md)** - Visão geral e quick start
2. **[Exemplo de Uso](../tests/exemplo_uso.py)** - Execute para ver funcionando
3. **[Testes Completos](../tests/test_simuladores.py)** - Testes detalhados

---

## 📚 DOCUMENTAÇÃO COMPLETA

### 📖 Documentos Principais

#### **[README.md](README.md)** - Documentação Técnica Completa
- Visão geral do sistema
- Arquitetura detalhada
- Descrição de todos os sensores
- Estrutura de arquivos
- Guia de uso completo
- Stack tecnológico

#### **[ROADMAP.md](ROADMAP.md)** - Planejamento de 7 Fases
- Fase 1: Simuladores ✅
- Fase 2: Gateway e MQTT 📅
- Fase 3: Backend (Flask, MySQL)
- Fase 4: Frontend (Dashboard Web)
- Fase 5: Analytics (PowerBI)
- Fase 6: Deployment (Docker)
- Fase 7: Go-Live
- Cronograma detalhado
- Tarefas por fase

#### **[INTEGRATION.md](INTEGRATION.md)** - Guia de Integrações Futuras
- Exemplos de código MQTT
- Integração com Flask
- Conexão com MySQL
- WebSocket frontend
- RabbitMQ workers
- Docker Compose
- PowerBI queries
- Sistema de alertas

#### **[RESUMO_EXECUTIVO.md](RESUMO_EXECUTIVO.md)** - Resumo do Projeto
- Objetivos alcançados
- Entregáveis da Fase 1
- Características técnicas
- Métricas de qualidade
- Estrutura do projeto
- Próximos passos
- Estatísticas completas

#### **[APRESENTACAO.md](APRESENTACAO.md)** - Apresentação Visual
- Visão geral simplificada
- Arquitetura em diagramas
- Sensores ilustrados
- Dashboard mockup
- Benefícios do sistema
- Tecnologias utilizadas
- Quick start visual

#### **[CHECKLIST.md](CHECKLIST.md)** - Status do Projeto
- Desenvolvimento completo
- Testes realizados
- Documentação criada
- Estrutura de arquivos
- Qualidade de código
- Métricas finais
- Status de entrega

---

## 🔧 CÓDIGO FONTE

### Simuladores de Sensores

#### **[base_sensor.py](../sensores/base_sensor.py)** - Classe Base
- `BaseSensor` - Classe abstrata
- Métodos comuns a todos os sensores
- Sistema de histórico
- Serialização JSON
- ~180 linhas

#### **[lora_sensor.py](../sensores/lora_sensor.py)** - Sensor LoRa
- `LoRaSensor` - Implementação LoRa
- Spreading Factor (SF7-SF12)
- RSSI, SNR, Bateria
- Estimativa de alcance
- ~150 linhas

#### **[zigbee_sensor.py](../sensores/zigbee_sensor.py)** - Sensor ZigBee
- `ZigBeeSensor` - Implementação ZigBee
- Rede Mesh
- LQI, PAN ID
- Descoberta de vizinhos
- ~180 linhas

#### **[sigfox_sensor.py](../sensores/sigfox_sensor.py)** - Sensor Sigfox
- `SigfoxSensor` - Implementação Sigfox
- Device ID, PAC Code
- Limite de 140 mensagens/dia
- Estimativa vida útil bateria
- ~190 linhas

#### **[rfid_sensor.py](../sensores/rfid_sensor.py)** - Sensor RFID
- `RFIDSensor` - Implementação RFID
- 3 frequências (LF, HF, UHF)
- Tags passivas/ativas
- Leitura múltiplas tags
- ~210 linhas

---

## 🧪 TESTES E EXEMPLOS

### Scripts de Teste

#### **[test_simuladores.py](../tests/test_simuladores.py)**
- Testes individuais de cada sensor
- Teste de monitoramento contínuo
- Geração de relatórios JSON
- ~200 linhas

#### **[exemplo_uso.py](../tests/exemplo_uso.py)**
- Exemplos simples de cada sensor
- Monitoramento de múltiplos sensores
- Código didático
- ~100 linhas

---

## ⚙️ CONFIGURAÇÃO

### Arquivos de Config

#### **[config.ini](../config/config.ini)**
- Configurações de sensores
- MQTT (Fase 2)
- Backend (Fase 3)
- Frontend (Fase 4)
- Banco de dados
- Parque (dados gerais)

#### **[requirements.txt](../requirements.txt)**
- Dependências Python (Fase 1)
- Pacotes planejados (Fases futuras)
- Versões específicas
- Containers Docker

#### **[.gitignore](../.gitignore)**
- Arquivos Python ignorados
- Cache e logs
- Configurações sensíveis
- Arquivos temporários

---

## 📊 NAVEGAÇÃO POR TEMA

### Por Fase do Projeto

| Fase | Documento Principal | Código |
|------|-------------------|--------|
| **Fase 1** ✅ | [README.md](README.md) | [sensores/](../sensores/) |
| **Fase 2** 📅 | [ROADMAP.md](ROADMAP.md)#fase-2 | backend/gateway/ |
| **Fase 3** 📅 | [ROADMAP.md](ROADMAP.md)#fase-3 | backend/app/ |
| **Fase 4** 📅 | [ROADMAP.md](ROADMAP.md)#fase-4 | frontend/ |
| **Fase 5** 📅 | [ROADMAP.md](ROADMAP.md)#fase-5 | analytics/ |

### Por Tecnologia

| Tecnologia | Documentação | Implementação |
|-----------|--------------|---------------|
| **Python** | [README.md](README.md) | Toda `/sensores` |
| **LoRa** | [README.md](README.md#lora) | [lora_sensor.py](../sensores/lora_sensor.py) |
| **ZigBee** | [README.md](README.md#zigbee) | [zigbee_sensor.py](../sensores/zigbee_sensor.py) |
| **Sigfox** | [README.md](README.md#sigfox) | [sigfox_sensor.py](../sensores/sigfox_sensor.py) |
| **RFID** | [README.md](README.md#rfid) | [rfid_sensor.py](../sensores/rfid_sensor.py) |
| **MQTT** | [INTEGRATION.md](INTEGRATION.md#mqtt) | (Fase 2) |
| **Flask** | [INTEGRATION.md](INTEGRATION.md#flask) | (Fase 3) |

### Por Objetivo

| Objetivo | Onde Encontrar |
|----------|----------------|
| **Entender o Projeto** | [README Principal](../README.md), [APRESENTACAO.md](APRESENTACAO.md) |
| **Ver Código Funcionando** | [exemplo_uso.py](../tests/exemplo_uso.py) |
| **Implementar Sensor** | [base_sensor.py](../sensores/base_sensor.py) |
| **Testar Sistema** | [test_simuladores.py](../tests/test_simuladores.py) |
| **Planejar Futuro** | [ROADMAP.md](ROADMAP.md) |
| **Integrar com Backend** | [INTEGRATION.md](INTEGRATION.md) |
| **Apresentar Projeto** | [APRESENTACAO.md](APRESENTACAO.md) |
| **Status Atual** | [CHECKLIST.md](CHECKLIST.md) |

---

## 🎯 GUIAS ESPECÍFICOS

### Para Desenvolvedores

```
1. Ler: README.md (técnico)
2. Estudar: base_sensor.py (arquitetura)
3. Explorar: Um sensor específico
4. Testar: exemplo_uso.py
5. Contribuir: Seguir ROADMAP.md
```

### Para Gestores

```
1. Ler: APRESENTACAO.md (visão geral)
2. Revisar: RESUMO_EXECUTIVO.md (métricas)
3. Planejar: ROADMAP.md (cronograma)
4. Acompanhar: CHECKLIST.md (status)
```

### Para Alunos/Aprendizes

```
1. Começar: README Principal
2. Aprender: exemplo_uso.py (executar)
3. Praticar: Modificar sensores existentes
4. Expandir: Criar novo tipo de sensor
5. Integrar: Seguir INTEGRATION.md
```

---

## 🔍 BUSCA RÁPIDA

### Conceitos Principais

- **Sensores IoT**: [README.md](README.md#sensores-implementados)
- **Protocolos**: [README.md](README.md#protocolos-suportados)
- **Arquitetura**: [README.md](README.md#arquitetura-do-sistema)
- **Testes**: [CHECKLIST.md](CHECKLIST.md#testes)
- **Deploy**: [ROADMAP.md](ROADMAP.md#fase-6)

### Comandos Úteis

```bash
# Executar testes
python tests/test_simuladores.py

# Executar exemplos
python tests/exemplo_uso.py

# Ver estrutura
tree /F /A
```

---

## 📞 INFORMAÇÕES

**Projeto:** Sistema de Controle de Acesso  
**Local:** Parque CEU Tres Pontes  
**Fase Atual:** 1 (Simuladores) ✅  
**Versão Documentação:** 1.0.0  
**Última Atualização:** Outubro 2025

---

## 🗺️ MAPA DO PROJETO

```
PI - IV - V1/
│
├── 📄 README.md                    ← Início aqui!
├── 📄 requirements.txt
├── 📄 .gitignore
│
├── 📁 sensores/                    ← Código principal
│   ├── base_sensor.py
│   ├── lora_sensor.py
│   ├── zigbee_sensor.py
│   ├── sigfox_sensor.py
│   └── rfid_sensor.py
│
├── 📁 tests/                       ← Execute estes!
│   ├── test_simuladores.py
│   └── exemplo_uso.py
│
├── 📁 docs/                        ← Você está aqui
│   ├── INDEX.md                    ← Este arquivo
│   ├── README.md                   ← Doc técnica
│   ├── ROADMAP.md                  ← 7 fases
│   ├── INTEGRATION.md              ← Código futuro
│   ├── RESUMO_EXECUTIVO.md         ← Métricas
│   ├── APRESENTACAO.md             ← Visual
│   └── CHECKLIST.md                ← Status
│
├── 📁 config/
│   └── config.ini
│
├── 📁 backend/                     ← Fase 2-3
└── 📁 frontend/                    ← Fase 4
```

---

**💡 Dica:** Comece pelo [README Principal](../README.md) e depois volte aqui para navegação detalhada!

**🚀 Pronto para começar?** Execute: `python tests/exemplo_uso.py`
