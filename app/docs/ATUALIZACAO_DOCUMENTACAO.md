# 📋 Atualização de Documentação - Permissões e Estrutura

**Data:** 18 de Outubro de 2025  
**Motivo:** Ajustes para estrutura Git e correção de problemas de permissões  
**Servidor:** Ubuntu 24.04 @ 192.168.0.194  

---

## 🎯 Problema Identificado

Usuário estava recebendo erros de permissão ao:
1. Instalar pacotes Python (`pip install`)
2. Editar arquivo de configuração MQTT
3. Executar scripts de deploy

**Causa:** Diretórios em `/opt/iot-gateway` criados com `sudo`, pertencendo ao root.

---

## ✅ Solução Implementada

### Comando de Correção

```bash
# Transferir propriedade para o usuário
sudo chown -R $USER:$USER /opt/iot-gateway

# Ajustar permissões
sudo chmod -R 755 /opt/iot-gateway
```

---

## 📝 Documentos Criados/Atualizados

### 1. ✅ Novos Documentos

| Arquivo | Descrição | Status |
|---------|-----------|--------|
| `FIX_PERMISSOES_RAPIDO.md` | Solução rápida (copy/paste) | ✅ Criado |
| `TROUBLESHOOTING_PERMISSOES.md` | Guia completo de permissões | ✅ Criado |
| `DEPLOY_ESTRUTURA_ATUALIZADA.md` | Guia com estrutura Git correta | ✅ Criado |

### 2. ✅ Documentos Atualizados

| Arquivo | Alterações | Status |
|---------|-----------|--------|
| `docs/SERVIDOR_UBUNTU_SETUP.md` | - Seção 4.1: Adicionado `chown` após criar `/opt/iot-gateway`<br>- Seção 7.1: Adicionado `chown` após git clone<br>- Seção Troubleshooting: Nova seção sobre permissões | ✅ Atualizado |
| `deploy/setup_service.sh` | - `PROJECT_DIR` agora aponta para `/opt/iot-gateway/PI---IV---V1`<br>- `VENV_DIR` separado em `/opt/iot-gateway/venv` | ✅ Atualizado |
| `deploy/deploy.sh` | - Variáveis `PROJECT_DIR` e `VENV_DIR` separadas<br>- Comandos ajustados para nova estrutura | ✅ Atualizado |

---

## 📁 Estrutura de Diretórios Definitiva

```
/opt/iot-gateway/
├── venv/                          # Ambiente virtual Python (criado manualmente)
│   ├── bin/
│   ├── lib/
│   └── ...
│
└── PI---IV---V1/                  # Repositório Git clonado
    ├── backend/
    │   ├── gateway/
    │   │   ├── gateway.py         # Script principal
    │   │   └── mqtt_client.py
    │   ├── config/
    │   │   └── mqtt_config.ini    # Configuração MQTT
    │   └── requirements-phase2.txt
    ├── frontend/
    ├── sensores/
    ├── tests/
    ├── deploy/
    │   ├── install_ubuntu.sh
    │   ├── setup_service.sh       # ✅ Atualizado
    │   └── deploy.sh              # ✅ Atualizado
    ├── docs/
    │   ├── SERVIDOR_UBUNTU_SETUP.md         # ✅ Atualizado
    │   └── TROUBLESHOOTING_PERMISSOES.md    # ✅ Novo
    ├── requirements.txt
    ├── DEPLOY_ESTRUTURA_ATUALIZADA.md       # ✅ Novo
    └── FIX_PERMISSOES_RAPIDO.md             # ✅ Novo
```

**Proprietário:** `rogeriovieira:rogeriovieira` (não root!)  
**Permissões:** `755` para diretórios, `644` para arquivos

---

## 🚀 Ações Necessárias no Servidor

### 1. Corrigir Permissões (URGENTE)

```bash
sudo chown -R $USER:$USER /opt/iot-gateway
sudo chmod -R 755 /opt/iot-gateway
```

### 2. Instalar Dependências

```bash
cd /opt/iot-gateway
source venv/bin/activate
cd PI---IV---V1
pip install -r requirements.txt
pip install -r backend/requirements-phase2.txt
```

### 3. Configurar MQTT

```bash
nano backend/config/mqtt_config.ini
```

Alterar:
```ini
broker_host = 192.168.0.194
```

### 4. Testar Gateway

```bash
python backend/gateway/gateway.py
```

### 5. Configurar Serviço Systemd

```bash
cd deploy
chmod +x setup_service.sh
sudo ./setup_service.sh
```

---

## 📊 Status da Instalação

| Etapa | Status | Observações |
|-------|--------|-------------|
| 1. Sistema atualizado | ✅ | - |
| 2. Ferramentas básicas | ✅ | - |
| 3. Python 3.x | ✅ | - |
| 4. Ambiente virtual | ✅ | `/opt/iot-gateway/venv` |
| 5. Mosquitto MQTT | ✅ | Rodando na porta 1883 |
| 6. Firewall UFW | ✅ | Portas 22, 1883, 8000 abertas |
| 7. Git clone | ✅ | `/opt/iot-gateway/PI---IV---V1/` |
| 8. **Permissões** | ⚠️ **PENDENTE** | Executar `chown` |
| 9. Dependências Python | ⏳ Próximo | Aguardando correção de permissões |
| 10. Config MQTT | ⏳ Próximo | Aguardando correção de permissões |
| 11. Teste manual | ⏳ Próximo | - |
| 12. Systemd service | ⏳ Próximo | - |

---

## 🔍 Verificação de Permissões

### Antes da Correção (Problema)

```bash
ls -la /opt/iot-gateway/
# drwxr-xr-x root root ...  # ❌ Pertence ao root
```

### Depois da Correção (Esperado)

```bash
ls -la /opt/iot-gateway/
# drwxr-xr-x rogeriovieira rogeriovieira ...  # ✅ Pertence ao usuário
```

---

## 📖 Guias de Referência

### Para o Usuário

1. **Solução Rápida:** `FIX_PERMISSOES_RAPIDO.md`
2. **Troubleshooting Completo:** `docs/TROUBLESHOOTING_PERMISSOES.md`
3. **Deploy com estrutura Git:** `DEPLOY_ESTRUTURA_ATUALIZADA.md`
4. **Setup completo:** `docs/SERVIDOR_UBUNTU_SETUP.md`

### Para Scripts Automatizados

1. **Instalação automática:** `deploy/install_ubuntu.sh` (já corrigido)
2. **Setup do serviço:** `deploy/setup_service.sh` (já corrigido)
3. **Deploy de updates:** `deploy/deploy.sh` (já corrigido)

---

## 🎓 Lições Aprendidas

### Problema

- Diretórios criados com `sudo` em `/opt/` pertencem ao root
- Usuário comum não consegue escrever sem `sudo`
- Usar `sudo pip` é má prática e pode quebrar o venv

### Solução

- Sempre ajustar proprietário após criar diretórios com `sudo`
- Usar `chown -R $USER:$USER` para transferir propriedade
- Nunca usar `sudo` para operações Python dentro do venv

### Prevenção

- Scripts de instalação agora incluem `chown` automaticamente
- Documentação atualizada com avisos sobre permissões
- Guia de troubleshooting criado para referência futura

---

## 🔄 Próximas Atualizações

### Documentação

- [ ] Adicionar seção sobre permissões no `README.md` principal
- [ ] Criar vídeo/GIF demonstrativo das correções
- [ ] Traduzir para inglês (opcional)

### Infraestrutura

- [ ] Adicionar verificação de permissões no `check_status.sh`
- [ ] Criar script de validação pré-deployment
- [ ] Adicionar testes automatizados de permissões

### Segurança

- [ ] Implementar autenticação MQTT (usuário/senha)
- [ ] Configurar SSL/TLS para Mosquitto
- [ ] Adicionar regras de firewall mais restritivas

---

## 📞 Comandos de Emergência

### Se algo der errado

```bash
# Resetar permissões de tudo
sudo chown -R $USER:$USER /opt/iot-gateway
sudo chmod -R 755 /opt/iot-gateway

# Recriar venv do zero
cd /opt/iot-gateway
rm -rf venv
python3 -m venv venv
source venv/bin/activate
cd PI---IV---V1
pip install -r requirements.txt
pip install -r backend/requirements-phase2.txt

# Ver logs de erro
sudo journalctl -u mosquitto -n 50
sudo journalctl -u iot-gateway -n 50

# Status dos serviços
sudo systemctl status mosquitto
sudo systemctl status iot-gateway
```

---

## ✅ Checklist de Validação

Após aplicar as correções, verificar:

- [ ] `ls -la /opt/iot-gateway/` mostra seu usuário (não root)
- [ ] `pip install` funciona SEM sudo
- [ ] `nano backend/config/mqtt_config.ini` abre sem erro
- [ ] `python backend/gateway/gateway.py` executa sem erro de permissão
- [ ] Scripts em `deploy/*.sh` são executáveis
- [ ] Venv ativa corretamente com `source venv/bin/activate`

---

**📅 Última atualização:** 18/10/2025 14:30  
**👤 Responsável:** GitHub Copilot  
**🎯 Status:** ✅ Documentação completa e atualizada  
**🖥️ Ambiente:** Ubuntu 24.04 LTS @ 192.168.0.194
