# 📤 Como Transferir Arquivos para o Servidor Ubuntu

## 🎯 Objetivo

Transferir os scripts de instalação e o código do projeto do Windows para o servidor Ubuntu (192.168.0.194).

---

## 🔧 Método 1: SCP (Recomendado para Scripts)

### Do Windows PowerShell

#### Transferir apenas os scripts de instalação

```powershell
# Navegar até o projeto
cd "c:\PI - IV - V1"

# Transferir scripts para /tmp (NÃO precisa de sudo)
scp deploy\install_ubuntu.sh usuario@192.168.0.194:/tmp/
scp deploy\setup_service.sh usuario@192.168.0.194:/tmp/
scp deploy\deploy.sh usuario@192.168.0.194:/tmp/
```

**Substitua `usuario` pelo seu usuário do Ubuntu!**

#### Transferir o projeto completo

```powershell
# Do diretório do projeto
cd "c:\PI - IV - V1"

# Transferir tudo (pode demorar)
scp -r . usuario@192.168.0.194:/tmp/iot-gateway-temp/
```

---

## 🌐 Método 2: Git (Recomendado para Código)

### No Servidor Ubuntu

```bash
# Conectar ao servidor
ssh usuario@192.168.0.194

# Navegar para o diretório de destino
cd /opt/iot-gateway

# Clonar o repositório
git clone https://github.com/RogerioVieira77/PI---IV---V1.git .

# OU se já existir, apenas atualizar
git pull origin main
```

**Vantagens:**
- ✅ Mais rápido
- ✅ Mantém histórico de versões
- ✅ Fácil de atualizar depois
- ✅ Não precisa transferir venv e __pycache__

---

## 📋 Método 3: WinSCP (Interface Gráfica)

### Passo a Passo

1. **Baixar WinSCP**
   - https://winscp.net/eng/download.php
   - Instalar no Windows

2. **Conectar ao Servidor**
   - File Protocol: `SFTP`
   - Host name: `192.168.0.194`
   - Port number: `22`
   - User name: `seu_usuario`
   - Password: `sua_senha`

3. **Transferir Arquivos**
   - Lado esquerdo: Windows (c:\PI - IV - V1)
   - Lado direito: Ubuntu (/tmp ou /opt/iot-gateway)
   - Arrastar e soltar

**Vantagens:**
- ✅ Interface gráfica amigável
- ✅ Visualização lado a lado
- ✅ Fácil para iniciantes

---

## 🚀 Método 4: Script PowerShell Automatizado

### Criar arquivo: `transfer.ps1`

```powershell
# Script de Transferência Automática
# Salve como: transfer.ps1

$SERVER_IP = "192.168.0.194"
$SERVER_USER = "seu_usuario"  # ALTERE AQUI
$PROJECT_DIR = "c:\PI - IV - V1"

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "Transferindo arquivos para servidor" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

# Verificar se está no diretório correto
if (!(Test-Path $PROJECT_DIR)) {
    Write-Host "Erro: Diretório não encontrado!" -ForegroundColor Red
    exit 1
}

Set-Location $PROJECT_DIR

Write-Host "`nTransferindo scripts de instalação..." -ForegroundColor Yellow

# Transferir scripts
scp deploy\install_ubuntu.sh "${SERVER_USER}@${SERVER_IP}:/tmp/"
scp deploy\setup_service.sh "${SERVER_USER}@${SERVER_IP}:/tmp/"
scp deploy\deploy.sh "${SERVER_USER}@${SERVER_IP}:/tmp/"

Write-Host "`nTransferindo código do projeto..." -ForegroundColor Yellow

# Transferir código (excluindo arquivos desnecessários)
$exclude = @(
    ".git",
    "venv",
    "__pycache__",
    "*.pyc",
    ".vscode",
    ".idea"
)

# Criar lista de exclusões para SCP
$excludeParams = $exclude | ForEach-Object { "--exclude='$_'" }

# Transferir
scp -r . "${SERVER_USER}@${SERVER_IP}:/tmp/iot-gateway-transfer/"

Write-Host "`n====================================" -ForegroundColor Green
Write-Host "Transferência concluída!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green

Write-Host "`nPróximos passos no servidor:" -ForegroundColor Cyan
Write-Host "1. ssh ${SERVER_USER}@${SERVER_IP}" -ForegroundColor White
Write-Host "2. cd /tmp" -ForegroundColor White
Write-Host "3. chmod +x install_ubuntu.sh" -ForegroundColor White
Write-Host "4. ./install_ubuntu.sh" -ForegroundColor White
```

### Executar

```powershell
# Dar permissão de execução
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Executar script
.\transfer.ps1
```

---

## 📦 O Que Transferir

### Arquivos Essenciais (Mínimo)

```
deploy/
├── install_ubuntu.sh       ⭐ ESSENCIAL
├── setup_service.sh        ⭐ ESSENCIAL
└── deploy.sh               ⭐ ESSENCIAL
```

### Projeto Completo (Recomendado)

```
PI - IV - V1/
├── backend/               ⭐
├── sensores/              ⭐
├── tests/                 ⭐
├── config/                ⭐
├── deploy/                ⭐
├── docs/                  ✅
├── requirements.txt       ⭐
└── README.md              ✅
```

**NÃO transferir:**
- ❌ `venv/` (será criado no servidor)
- ❌ `__pycache__/` (cache Python)
- ❌ `.git/` (se usar Git, clonar direto)
- ❌ `.vscode/`, `.idea/` (configurações do editor)
- ❌ `docs-web/` (apenas se for usar)

---

## ✅ Verificar Transferência

### No Servidor Ubuntu

```bash
# Conectar
ssh usuario@192.168.0.194

# Verificar se os scripts foram transferidos
ls -lh /tmp/*.sh

# Verificar tamanho dos arquivos
du -sh /tmp/iot-gateway-transfer/

# Contar arquivos transferidos
find /tmp/iot-gateway-transfer -type f | wc -l
```

---

## 🔍 Solução de Problemas

### Erro: Permission Denied

**Problema**: Não tem permissão para escrever no destino.

**Solução**:
```bash
# Transferir para /tmp primeiro (sempre funciona)
scp arquivo.sh usuario@192.168.0.194:/tmp/

# Depois mover com sudo no servidor
ssh usuario@192.168.0.194
sudo mv /tmp/arquivo.sh /opt/iot-gateway/
```

### Erro: Connection Refused

**Problema**: SSH não está rodando ou firewall bloqueando.

**Solução no servidor**:
```bash
# Verificar se SSH está rodando
sudo systemctl status ssh

# Iniciar SSH se necessário
sudo systemctl start ssh

# Verificar firewall
sudo ufw status
sudo ufw allow 22/tcp
```

### Erro: Host Key Verification Failed

**Problema**: Primeira conexão ou chave SSH mudou.

**Solução**:
```powershell
# Aceitar a nova chave
ssh-keyscan 192.168.0.194 >> ~/.ssh/known_hosts

# Ou remover a chave antiga
ssh-keygen -R 192.168.0.194
```

### Transferência Muito Lenta

**Problema**: Rede lenta ou muitos arquivos.

**Solução**:
```powershell
# Comprimir antes de transferir
Compress-Archive -Path "c:\PI - IV - V1\*" -DestinationPath "iot-gateway.zip"

# Transferir apenas o zip
scp iot-gateway.zip usuario@192.168.0.194:/tmp/

# No servidor, descomprimir
ssh usuario@192.168.0.194
cd /tmp
unzip iot-gateway.zip -d iot-gateway/
```

---

## 🎯 Fluxo Recomendado

### Para Primeira Instalação

```powershell
# 1. Transferir apenas os scripts
cd "c:\PI - IV - V1"
scp deploy\*.sh usuario@192.168.0.194:/tmp/

# 2. Conectar ao servidor
ssh usuario@192.168.0.194

# 3. Executar instalação
cd /tmp
chmod +x *.sh
./install_ubuntu.sh

# 4. Depois que a estrutura estiver criada, transferir código via Git
cd /opt/iot-gateway
git clone https://github.com/RogerioVieira77/PI---IV---V1.git .
```

### Para Atualizações

```bash
# No servidor, usar o script de deploy
cd /opt/iot-gateway
./deploy/deploy.sh

# Ele automaticamente faz git pull e reinicia
```

---

## 📚 Referências

### Comandos SCP Úteis

```powershell
# Transferir arquivo único
scp arquivo.txt user@host:/path/

# Transferir pasta
scp -r pasta/ user@host:/path/

# Transferir múltiplos arquivos
scp file1.txt file2.txt user@host:/path/

# Porta customizada
scp -P 2222 arquivo.txt user@host:/path/

# Verbose (ver progresso)
scp -v arquivo.txt user@host:/path/

# Comprimir durante transferência
scp -C arquivo.txt user@host:/path/
```

### Comandos SSH Úteis

```powershell
# Conectar
ssh user@host

# Executar comando remoto
ssh user@host "comando"

# Copiar chave SSH
ssh-copy-id user@host

# Conectar e executar script
ssh user@host "bash -s" < script.sh
```

---

## ✨ Dica Extra: Criar Alias

### No PowerShell Profile

```powershell
# Editar profile
notepad $PROFILE

# Adicionar aliases
function Connect-IoTServer {
    ssh usuario@192.168.0.194
}

function Transfer-IoTScripts {
    cd "c:\PI - IV - V1"
    scp deploy\*.sh usuario@192.168.0.194:/tmp/
}

# Usar
Connect-IoTServer
Transfer-IoTScripts
```

---

**🎉 Agora você tem várias formas de transferir os arquivos!**

**Escolha o método que preferir e boa instalação!**
