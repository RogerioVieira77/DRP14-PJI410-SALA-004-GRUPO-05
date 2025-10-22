# 🚀 Correção Rápida - Permissões do IoT Gateway

## ⚡ Solução Express (Copy & Paste)

Execute estes comandos **no servidor** (via SSH):

```bash
# 1. Corrigir proprietário de TODO o diretório /opt/iot-gateway
sudo chown -R $USER:$USER /opt/iot-gateway

# 2. Ajustar permissões adequadas
sudo chmod -R 755 /opt/iot-gateway

# 3. Verificar (deve mostrar seu usuário, NÃO root)
ls -la /opt/iot-gateway/
```

**Pronto!** Agora você pode fazer tudo **SEM sudo**:

```bash
# Instalar dependências Python
cd /opt/iot-gateway
source venv/bin/activate
cd PI---IV---V1
pip install -r requirements.txt
pip install -r backend/requirements-phase2.txt

# Editar configurações
nano backend/config/mqtt_config.ini

# Executar scripts
chmod +x deploy/*.sh
./deploy/setup_service.sh
```

---

## 🎯 Próximos Passos

Agora siga o passo **7.2** da documentação:

```bash
# Passo 7.2: Instalar Dependências
cd /opt/iot-gateway
source venv/bin/activate
cd PI---IV---V1

pip install -r requirements.txt
pip install -r backend/requirements-phase2.txt

# Verificar instalação do paho-mqtt
pip list | grep paho-mqtt
```

```bash
# Passo 7.3: Configurar MQTT
nano backend/config/mqtt_config.ini
```

**Altere a linha:**
```ini
broker_host = 192.168.0.194
```

**Salve:** `Ctrl+O`, `Enter`, `Ctrl+X`

```bash
# Passo 7.4: Testar manualmente
python backend/gateway/gateway.py
```

---

## 📚 Documentação Completa

Para mais detalhes sobre permissões, veja:
- `docs/TROUBLESHOOTING_PERMISSOES.md` - Guia completo de permissões
- `docs/SERVIDOR_UBUNTU_SETUP.md` - Guia de instalação atualizado
- `DEPLOY_ESTRUTURA_ATUALIZADA.md` - Guia de deploy com estrutura correta

---

**Data:** 18/10/2025  
**Problema:** Permission Denied em `/opt/iot-gateway`  
**Solução:** `sudo chown -R $USER:$USER /opt/iot-gateway`
