# ✅ CHECKLIST - Instalação Servidor Ubuntu 24.04

**Projeto**: IoT Gateway - Ambiente de Testes  
**Servidor**: 192.168.0.194  
**Data de Instalação**: ___/___/2025

---

## 📋 PRÉ-INSTALAÇÃO

- [ ] Servidor Ubuntu 24.04 instalado
- [ ] IP configurado: 192.168.0.194
- [ ] Acesso SSH funcionando (testado do Windows)
- [ ] Usuário com privilégios sudo criado
- [ ] Documentação lida (`docs/SERVIDOR_UBUNTU_SETUP.md`)
- [ ] Scripts de deploy transferidos para o servidor

---

## 🚀 FASE 1: INSTALAÇÃO BASE

### Sistema Operacional

- [ ] Conectado ao servidor via SSH
- [ ] Sistema atualizado (`sudo apt update && upgrade`)
- [ ] Reboot realizado (se necessário)

### Ferramentas Básicas

- [ ] Git instalado (versão: ________)
- [ ] Curl instalado
- [ ] Vim/Nano instalado
- [ ] Htop instalado
- [ ] Net-tools instalado

### Python

- [ ] Python 3.x instalado (versão: ________)
- [ ] Pip instalado e atualizado (versão: ________)
- [ ] Python3-venv instalado
- [ ] Python3-dev instalado

### Estrutura de Diretórios

- [ ] Diretório `/opt/iot-gateway` criado
- [ ] Permissões ajustadas para o usuário
- [ ] Ambiente virtual criado em `/opt/iot-gateway/venv`
- [ ] Ambiente virtual testado (ativação funcionando)

---

## 🔌 FASE 2: MQTT (MOSQUITTO)

### Instalação

- [ ] Eclipse Mosquitto instalado
- [ ] Mosquitto-clients instalado
- [ ] Versão verificada: ________

### Configuração

- [ ] Arquivo `/etc/mosquitto/conf.d/custom.conf` criado
- [ ] Configuração para porta 1883 em todas as interfaces
- [ ] Conexões anônimas permitidas (teste)
- [ ] Logs configurados
- [ ] Persistência habilitada

### Serviço

- [ ] Mosquitto reiniciado
- [ ] Mosquitto habilitado (auto-start)
- [ ] Status verificado: ATIVO
- [ ] Porta 1883 escutando (netstat confirmado)

### Testes

- [ ] mosquitto_sub funcionando localmente
- [ ] mosquitto_pub funcionando localmente
- [ ] Teste pub/sub bem-sucedido
- [ ] Logs do Mosquitto sem erros

---

## 🔥 FASE 3: FIREWALL (UFW)

- [ ] UFW instalado
- [ ] UFW habilitado
- [ ] Porta 22 (SSH) permitida ⚠️ CRÍTICO
- [ ] Porta 1883 (MQTT) permitida
- [ ] Porta 8000 (API) permitida
- [ ] Porta 80 (HTTP) permitida
- [ ] Porta 443 (HTTPS) permitida
- [ ] Firewall recarregado
- [ ] Regras verificadas (`sudo ufw status numbered`)
- [ ] SSH ainda funciona após ativar firewall ✅

---

## 📦 FASE 4: CÓDIGO DA APLICAÇÃO

### Transferência

- [ ] Código transferido via Git OU SCP
- [ ] Todos os arquivos presentes em `/opt/iot-gateway`
- [ ] Estrutura de pastas correta:
  - [ ] `backend/`
  - [ ] `sensores/`
  - [ ] `tests/`
  - [ ] `deploy/`
  - [ ] `config/`

### Dependências Python

- [ ] Ambiente virtual ativado
- [ ] `requirements.txt` instalado
- [ ] `backend/requirements-phase2.txt` instalado
- [ ] Pacotes verificados (`pip list`)
- [ ] Paho-MQTT presente na lista

### Configurações

- [ ] Arquivo `backend/config/mqtt_config.ini` existe
- [ ] IP do broker ajustado para `192.168.0.194`
- [ ] Porta ajustada para `1883`
- [ ] Topics configurados corretamente
- [ ] QoS definido (1 ou 2)

---

## ⚙️ FASE 5: SERVIÇO SYSTEMD

### Criação

- [ ] Script `deploy/setup_service.sh` executável
- [ ] Script `setup_service.sh` executado
- [ ] Arquivo `/etc/systemd/system/iot-gateway.service` criado
- [ ] Usuário correto no arquivo de serviço
- [ ] Caminho do Python correto (venv)

### Configuração

- [ ] Systemd daemon recarregado
- [ ] Serviço habilitado (`enable`)
- [ ] Serviço iniciado (`start`)
- [ ] Status verificado: ATIVO
- [ ] Logs sem erros (`journalctl -u iot-gateway -n 50`)

---

## 🧪 FASE 6: TESTES

### Testes Locais (no servidor)

- [ ] Gateway inicia manualmente (sem systemd)
- [ ] Gateway conecta ao Mosquitto
- [ ] Mensagens MQTT publicadas com sucesso
- [ ] Logs mostram sensores simulados funcionando

### Testes Remotos (do Windows)

- [ ] Ping ao servidor: `ping 192.168.0.194` → OK
- [ ] Porta MQTT acessível: `Test-NetConnection -Port 1883` → OK
- [ ] mosquitto_sub do Windows conecta ao servidor
- [ ] mosquitto_pub do Windows publica no servidor
- [ ] Mensagens recebidas corretamente

### Testes de Integração

- [ ] Simuladores de sensores executados
- [ ] Mensagens de todos os tipos de sensores (LoRa, Zigbee, Sigfox, RFID)
- [ ] Subscriber recebe mensagens em `/sensores/#`
- [ ] Formato JSON correto
- [ ] Timestamps corretos

---

## 📊 FASE 7: SCRIPTS AUXILIARES

- [ ] Script `check_status.sh` criado
- [ ] Script `check_status.sh` executável
- [ ] Script `check_status.sh` testado e funcionando
- [ ] Script `backup.sh` criado
- [ ] Script `backup.sh` executável
- [ ] Script `backup.sh` testado (backup criado)
- [ ] Diretório de backups `/opt/backups/iot-gateway/` existe

---

## 📈 FASE 8: MONITORAMENTO

### Ferramentas

- [ ] Glances instalado
- [ ] Glances testado
- [ ] Htop funcionando

### Logs

- [ ] Logs do Gateway acessíveis via journalctl
- [ ] Logs do Mosquitto em `/var/log/mosquitto/`
- [ ] Logs sem erros críticos
- [ ] Rotação de logs configurada (systemd padrão)

### Status

- [ ] Comando `systemctl status iot-gateway` → ATIVO
- [ ] Comando `systemctl status mosquitto` → ATIVO
- [ ] CPU em uso aceitável (< 50%)
- [ ] Memória em uso aceitável (< 70%)
- [ ] Disco com espaço livre (> 10GB)

---

## 🔄 FASE 9: DEPLOY AUTOMATIZADO

- [ ] Script `deploy/deploy.sh` executável
- [ ] Script `deploy.sh` testado
- [ ] Backup automático funcionando
- [ ] Git pull funcionando (se usando Git)
- [ ] Reinício automático do serviço
- [ ] Logs mostrados após deploy

---

## ✅ VALIDAÇÃO FINAL

### Checklist de Validação

- [ ] Servidor responde ao ping
- [ ] SSH funciona
- [ ] Mosquitto rodando e acessível
- [ ] Gateway rodando como serviço
- [ ] Testes MQTT do Windows funcionando
- [ ] Firewall ativo e configurado
- [ ] Logs sem erros
- [ ] Backup testado

### Testes de Resiliência

- [ ] Reiniciar servidor: `sudo reboot`
- [ ] Aguardar boot completo
- [ ] Reconectar via SSH
- [ ] Verificar se Mosquitto iniciou automaticamente
- [ ] Verificar se Gateway iniciou automaticamente
- [ ] Testar MQTT novamente

### Documentação

- [ ] IPs documentados
- [ ] Usuários documentados
- [ ] Senhas armazenadas com segurança
- [ ] Comandos úteis anotados
- [ ] Procedimentos de backup documentados

---

## 📝 INFORMAÇÕES REGISTRADAS

**Preenchido em**: ___/___/2025

### Dados do Servidor

- IP: `192.168.0.194`
- Hostname: ________________
- Usuário: ________________
- SO: Ubuntu 24.04 LTS
- Versão Python: ________________
- Versão Mosquitto: ________________

### Portas Configuradas

- SSH: 22 ✅
- MQTT: 1883 ✅
- API: 8000 ✅
- HTTP: 80 ✅
- HTTPS: 443 ✅

### Diretórios

- Projeto: `/opt/iot-gateway`
- Backups: `/opt/backups/iot-gateway`
- Logs Mosquitto: `/var/log/mosquitto/`
- Config Mosquitto: `/etc/mosquitto/conf.d/`

### Comandos Úteis Personalizados

```bash
# Status completo
alias iot-status="/opt/iot-gateway/check_status.sh"

# Logs em tempo real
alias iot-logs="sudo journalctl -u iot-gateway -f"

# Reiniciar gateway
alias iot-restart="sudo systemctl restart iot-gateway"

# Backup manual
alias iot-backup="/opt/iot-gateway/backup.sh"
```

---

## 🎯 PRÓXIMOS PASSOS

- [ ] Implementar autenticação MQTT
- [ ] Configurar TLS/SSL para MQTT
- [ ] Instalar banco de dados (PostgreSQL/MongoDB)
- [ ] Desenvolver API REST (FastAPI)
- [ ] Criar frontend web (React/Vue)
- [ ] Implementar dashboard de monitoramento
- [ ] Configurar backup automático agendado (cron)
- [ ] Documentar procedimentos de recuperação
- [ ] Configurar alertas de monitoramento

---

## ✍️ OBSERVAÇÕES

```
_________________________________________________________________

_________________________________________________________________

_________________________________________________________________

_________________________________________________________________

_________________________________________________________________
```

---

## 👥 RESPONSÁVEIS

**Instalação realizada por**: ____________________________

**Data**: ___/___/2025

**Revisado por**: ____________________________

**Data da revisão**: ___/___/2025

---

**✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!**

**Total de itens verificados**: _____/_____ (____%)

---

**Assinatura**: ____________________________

**Data**: ___/___/2025
