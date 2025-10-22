# 🔧 Troubleshooting - Problemas de Permissões

## 🚨 Problema: Permission Denied

Se você está recebendo erros como:

```
ERROR: Could not install packages due to an OSError: [Errno 13] Permission denied
Check the permissions.
```

```
File '/opt/iot-gateway/PI---IV---V1/backend/config/mqtt_config.ini' is unwritable
```

**Causa:** Os diretórios em `/opt/` foram criados com permissões de root, mas você está tentando usá-los como usuário comum.

---

## ✅ Solução Completa

### 1. Ajustar Proprietário do Diretório Principal

```bash
# Transferir propriedade de /opt/iot-gateway para seu usuário
sudo chown -R $USER:$USER /opt/iot-gateway

# Verificar (deve mostrar seu usuário, não root)
ls -la /opt/iot-gateway/
```

**Saída esperada:**
```
drwxr-xr-x  5 rogeriovieira rogeriovieira 4096 Oct 18 14:00 .
drwxr-xr-x 46 root          root          4096 Oct 18 13:44 ..
drwxr-xr-x  3 rogeriovieira rogeriovieira 4096 Oct 18 14:00 PI---IV---V1
drwxr-xr-x  5 rogeriovieira rogeriovieira 4096 Oct 18 14:00 venv
```

### 2. Ajustar Permissões

```bash
# Dar permissões de leitura/escrita/execução
sudo chmod -R 755 /opt/iot-gateway

# Verificar permissões de arquivos específicos
ls -la /opt/iot-gateway/PI---IV---V1/backend/config/
```

### 3. Testar Acesso

```bash
# Testar instalação de pacotes Python (SEM sudo)
cd /opt/iot-gateway
source venv/bin/activate
cd PI---IV---V1
pip install -r requirements.txt

# Testar edição de arquivo (SEM sudo)
nano backend/config/mqtt_config.ini
```

---

## 🔍 Diagnóstico de Permissões

### Verificar Proprietário dos Diretórios

```bash
# Verificar diretório principal
ls -la /opt/ | grep iot-gateway

# Verificar subdiretórios
ls -la /opt/iot-gateway/

# Verificar venv
ls -la /opt/iot-gateway/venv/ | head -20

# Verificar projeto
ls -la /opt/iot-gateway/PI---IV---V1/
```

### Verificar Permissões Numéricas

```bash
# Ver permissões em formato numérico
stat -c '%a %n' /opt/iot-gateway
stat -c '%a %n' /opt/iot-gateway/venv
stat -c '%a %n' /opt/iot-gateway/PI---IV---V1
```

**Permissões adequadas:**
- Diretórios: `755` (rwxr-xr-x)
- Arquivos Python: `644` (rw-r--r--)
- Scripts Shell: `755` (rwxr-xr-x)
- Arquivos de Config: `644` (rw-r--r--)

---

## 📋 Problemas Específicos

### 1. Erro ao instalar pacotes Python

**Erro:**
```
ERROR: Could not install packages due to an OSError: [Errno 13] Permission denied: 
'/opt/iot-gateway/venv/lib/python3.12/site-packages/six.py'
```

**Solução:**

```bash
# Opção 1: Corrigir permissões do venv
sudo chown -R $USER:$USER /opt/iot-gateway/venv
sudo chmod -R 755 /opt/iot-gateway/venv

# Opção 2: Recriar o venv (se opção 1 não funcionar)
cd /opt/iot-gateway
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r PI---IV---V1/requirements.txt
```

### 2. Arquivo de configuração não editável

**Erro:**
```
File '/opt/iot-gateway/PI---IV---V1/backend/config/mqtt_config.ini' is unwritable
```

**Solução:**

```bash
# Verificar proprietário
ls -la /opt/iot-gateway/PI---IV---V1/backend/config/mqtt_config.ini

# Corrigir proprietário
sudo chown $USER:$USER /opt/iot-gateway/PI---IV---V1/backend/config/mqtt_config.ini

# Corrigir permissões
chmod 644 /opt/iot-gateway/PI---IV---V1/backend/config/mqtt_config.ini

# Testar edição
nano /opt/iot-gateway/PI---IV---V1/backend/config/mqtt_config.ini
```

### 3. Scripts de deploy não executam

**Erro:**
```
Permission denied: ./setup_service.sh
```

**Solução:**

```bash
# Dar permissão de execução aos scripts
chmod +x /opt/iot-gateway/PI---IV---V1/deploy/*.sh

# Verificar
ls -la /opt/iot-gateway/PI---IV---V1/deploy/

# Agora pode executar
cd /opt/iot-gateway/PI---IV---V1/deploy
./setup_service.sh
```

### 4. Erro ao criar arquivo de log

**Erro:**
```
PermissionError: [Errno 13] Permission denied: '/opt/iot-gateway/logs/gateway.log'
```

**Solução:**

```bash
# Criar diretório de logs com permissões corretas
mkdir -p /opt/iot-gateway/logs
chmod 755 /opt/iot-gateway/logs

# Se já existir, corrigir proprietário
sudo chown -R $USER:$USER /opt/iot-gateway/logs
```

---

## 🔐 Entendendo Permissões no Linux

### Formato de Permissões

```
drwxr-xr-x  2 usuario grupo 4096 Oct 18 14:00 diretorio
-rw-r--r--  1 usuario grupo  256 Oct 18 14:00 arquivo.txt
```

**Breakdown:**
- `d`: diretório (`-` para arquivo)
- `rwx`: permissões do dono (read, write, execute)
- `r-x`: permissões do grupo (read, execute)
- `r-x`: permissões de outros (read, execute)
- `usuario`: proprietário
- `grupo`: grupo proprietário

### Permissões Numéricas

- `7` = rwx (read + write + execute) = 4+2+1
- `6` = rw- (read + write) = 4+2
- `5` = r-x (read + execute) = 4+1
- `4` = r-- (read only) = 4

**Exemplos:**
- `755` = rwxr-xr-x (dono: tudo; grupo/outros: ler e executar)
- `644` = rw-r--r-- (dono: ler/escrever; grupo/outros: só ler)
- `700` = rwx------ (só o dono tem acesso)

---

## ⚙️ Comandos Úteis de Permissões

```bash
# Alterar proprietário
chown usuario:grupo arquivo
sudo chown -R $USER:$USER /opt/iot-gateway

# Alterar permissões
chmod 755 diretorio
chmod 644 arquivo
sudo chmod -R 755 /opt/iot-gateway

# Ver permissões detalhadas
ls -la /caminho
stat /caminho

# Encontrar arquivos sem permissão de escrita
find /opt/iot-gateway -type f ! -writable

# Encontrar arquivos pertencentes ao root
find /opt/iot-gateway -user root

# Corrigir tudo de uma vez (USE COM CUIDADO!)
sudo chown -R $USER:$USER /opt/iot-gateway
sudo chmod -R u+rw /opt/iot-gateway
```

---

## 🛡️ Boas Práticas

### ✅ FAZER:

1. **Usar seu usuário** para desenvolvimento:
   ```bash
   sudo chown -R $USER:$USER /opt/iot-gateway
   ```

2. **Evitar sudo** para operações comuns:
   ```bash
   # ❌ NÃO FAÇA
   sudo pip install pacote
   
   # ✅ FAÇA
   source venv/bin/activate
   pip install pacote
   ```

3. **Criar diretórios com permissões corretas**:
   ```bash
   sudo mkdir /opt/iot-gateway
   sudo chown $USER:$USER /opt/iot-gateway
   ```

### ❌ NÃO FAZER:

1. **Nunca use `chmod 777`** (todos têm todas as permissões):
   ```bash
   # ❌ NUNCA FAÇA ISSO!
   sudo chmod -R 777 /opt/iot-gateway
   ```

2. **Não execute aplicações Python com sudo**:
   ```bash
   # ❌ NÃO FAÇA
   sudo python backend/gateway/gateway.py
   
   # ✅ FAÇA
   python backend/gateway/gateway.py
   ```

3. **Não instale pacotes Python no sistema com --break-system-packages**:
   ```bash
   # ❌ EVITE
   sudo pip3 install --break-system-packages pacote
   
   # ✅ USE VENV
   source venv/bin/activate
   pip install pacote
   ```

---

## 🔄 Script de Correção Automática

Crie um script para corrigir todas as permissões de uma vez:

```bash
# Criar script
nano /opt/iot-gateway/fix_permissions.sh
```

**Conteúdo:**

```bash
#!/bin/bash

echo "🔧 Corrigindo permissões do IoT Gateway..."

# Transferir propriedade para o usuário atual
sudo chown -R $USER:$USER /opt/iot-gateway

# Ajustar permissões de diretórios
find /opt/iot-gateway -type d -exec chmod 755 {} \;

# Ajustar permissões de arquivos Python/Config
find /opt/iot-gateway -type f -name "*.py" -exec chmod 644 {} \;
find /opt/iot-gateway -type f -name "*.ini" -exec chmod 644 {} \;
find /opt/iot-gateway -type f -name "*.txt" -exec chmod 644 {} \;
find /opt/iot-gateway -type f -name "*.md" -exec chmod 644 {} \;

# Ajustar permissões de scripts shell
find /opt/iot-gateway -type f -name "*.sh" -exec chmod 755 {} \;

# Verificar
echo ""
echo "✅ Permissões corrigidas!"
echo ""
echo "Verificação:"
ls -la /opt/iot-gateway/

echo ""
echo "Arquivos executáveis (.sh):"
find /opt/iot-gateway -type f -name "*.sh" -exec ls -lh {} \;
```

**Usar o script:**

```bash
# Dar permissão de execução
chmod +x /opt/iot-gateway/fix_permissions.sh

# Executar
/opt/iot-gateway/fix_permissions.sh
```

---

## 📞 Comandos Rápidos de Diagnóstico

```bash
# Verificar tudo de uma vez
echo "=== Proprietário de /opt/iot-gateway ==="
ls -la /opt/ | grep iot-gateway

echo ""
echo "=== Conteúdo de /opt/iot-gateway ==="
ls -la /opt/iot-gateway/

echo ""
echo "=== Arquivos do projeto ==="
ls -la /opt/iot-gateway/PI---IV---V1/

echo ""
echo "=== Config MQTT ==="
ls -la /opt/iot-gateway/PI---IV---V1/backend/config/mqtt_config.ini

echo ""
echo "=== Arquivos pertencentes ao root ==="
find /opt/iot-gateway -user root 2>/dev/null
```

---

## 🆘 Quando Pedir Ajuda

Se após todas as correções você ainda tiver problemas, colete estas informações:

```bash
# Informações do sistema
echo "=== Usuário atual ==="
whoami
id

echo ""
echo "=== Permissões do diretório ==="
ls -la /opt/iot-gateway/
ls -la /opt/iot-gateway/venv/
ls -la /opt/iot-gateway/PI---IV---V1/

echo ""
echo "=== Arquivos com problemas ==="
find /opt/iot-gateway -user root 2>/dev/null | head -20

echo ""
echo "=== Teste de escrita ==="
touch /opt/iot-gateway/test.txt && echo "✅ OK" || echo "❌ FALHOU"
rm -f /opt/iot-gateway/test.txt 2>/dev/null
```

---

**📅 Criado em**: 18 de Outubro de 2025  
**🎯 Problema Resolvido**: Permission Denied em /opt/iot-gateway  
**👤 Usuário**: rogeriovieira  
**🖥️ Servidor**: Ubuntu 24.04 LTS @ 192.168.0.194
