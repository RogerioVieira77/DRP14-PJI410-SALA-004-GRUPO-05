# 🚀 Guia de Instalação - Ambiente de Desenvolvimento Local Windows 10

**Sistema de Controle de Acesso - CEU Tres Pontes**  
**Versão:** 1.0  
**Data:** Outubro 2025  
**Plataforma:** Windows 10/11

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Pré-requisitos](#pré-requisitos)
3. [Instalação do Python](#instalação-do-python)
4. [Instalação do Git](#instalação-do-git)
5. [Instalação do MySQL](#instalação-do-mysql)
6. [Instalação do Mosquitto MQTT](#instalação-do-mosquitto-mqtt)
7. [Clone do Projeto](#clone-do-projeto)
8. [Configuração do Ambiente Virtual Python](#configuração-do-ambiente-virtual-python)
9. [Instalação das Dependências](#instalação-das-dependências)
10. [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
11. [Configuração do MQTT](#configuração-do-mqtt)
12. [Configuração das Variáveis de Ambiente](#configuração-das-variáveis-de-ambiente)
13. [Testando o Ambiente](#testando-o-ambiente)
14. [IDEs Recomendadas](#ides-recomendadas)
15. [Ferramentas Adicionais](#ferramentas-adicionais)
16. [Resolução de Problemas](#resolução-de-problemas)

---

## 📖 Visão Geral

Este guia apresenta um passo a passo completo para configurar um ambiente de desenvolvimento limpo no Windows 10, desde a instalação do sistema operacional até a execução completa da aplicação.

### O que vamos instalar:

- **Python 3.12.3** - Linguagem principal do projeto
- **Git** - Controle de versão
- **MySQL 8.0** - Banco de dados
- **Mosquitto MQTT** - Broker de mensagens
- **VS Code** - IDE (recomendado)
- **Postman** - Testes de API (opcional)

---

## 🎯 Pré-requisitos

### Sistema Operacional
- Windows 10 (versão 1909 ou superior) ou Windows 11
- 8GB de RAM (mínimo 4GB)
- 10GB de espaço livre em disco
- Conexão com a Internet
- Permissões de Administrador

### Conhecimentos Necessários
- Conhecimento básico de linha de comando (PowerShell/CMD)
- Conceitos básicos de programação Python
- Familiaridade com Git (desejável)

---

## 🐍 Instalação do Python

### Passo 1: Download do Python

1. Acesse o site oficial: https://www.python.org/downloads/
2. Clique em **"Download Python 3.12.3"** (ou versão mais recente 3.12.x)
3. Aguarde o download do instalador `python-3.12.3-amd64.exe`

### Passo 2: Instalação

1. Execute o instalador como **Administrador** (clique com botão direito > "Executar como administrador")

2. **IMPORTANTE**: Na primeira tela, marque as opções:
   - ✅ **"Add Python 3.12 to PATH"**
   - ✅ **"Install launcher for all users"**

3. Clique em **"Customize installation"**

4. Na tela "Optional Features", certifique-se de marcar:
   - ✅ Documentation
   - ✅ pip
   - ✅ tcl/tk and IDLE
   - ✅ Python test suite
   - ✅ py launcher
   - ✅ for all users

5. Clique em **"Next"**

6. Na tela "Advanced Options", marque:
   - ✅ **Install for all users**
   - ✅ **Add Python to environment variables**
   - ✅ Precompile standard library
   - ✅ Download debugging symbols
   - ✅ Download debug binaries

7. Em "Customize install location", use:
   ```
   C:\Python312
   ```

8. Clique em **"Install"** e aguarde a conclusão

9. Clique em **"Disable path length limit"** (caso apareça)

10. Clique em **"Close"**

### Passo 3: Verificação

Abra o **PowerShell** (não precisa ser como administrador) e execute:

```powershell
python --version
```

**Saída esperada:**
```
Python 3.12.3
```

Verifique também o pip:

```powershell
pip --version
```

**Saída esperada:**
```
pip 24.x.x from C:\Python312\Lib\site-packages\pip (python 3.12)
```

### Passo 4: Atualizar pip

```powershell
python -m pip install --upgrade pip
```

---

## 🔧 Instalação do Git

### Passo 1: Download do Git

1. Acesse: https://git-scm.com/download/win
2. O download iniciará automaticamente
3. Aguarde o download de `Git-2.xx.x-64-bit.exe`

### Passo 2: Instalação

1. Execute o instalador como **Administrador**

2. Nas telas de configuração, use as seguintes opções:

   - **Select Components:**
     - ✅ Windows Explorer integration
     - ✅ Git Bash Here
     - ✅ Git GUI Here
     - ✅ Associate .git* configuration files with the default text editor
     - ✅ Associate .sh files to be run with Bash

   - **Choose default editor:** Selecione **"Use Visual Studio Code as Git's default editor"** (ou seu editor preferido)

   - **Adjust your PATH environment:** Selecione **"Git from the command line and also from 3rd-party software"**

   - **Choose HTTPS transport backend:** Selecione **"Use the OpenSSL library"**

   - **Configure line ending conversions:** Selecione **"Checkout Windows-style, commit Unix-style line endings"**

   - **Configure terminal emulator:** Selecione **"Use Windows' default console window"**

   - **Choose default behavior of `git pull`:** Selecione **"Default (fast-forward or merge)"**

   - **Choose credential helper:** Selecione **"Git Credential Manager"**

   - Demais opções: mantenha o padrão

3. Clique em **"Install"** e aguarde

4. Clique em **"Finish"**

### Passo 3: Configuração Inicial do Git

Abra o **PowerShell** ou **Git Bash** e configure seu nome e email:

```powershell
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@example.com"
```

Verifique a configuração:

```powershell
git config --list
```

### Passo 4: Verificação

```powershell
git --version
```

**Saída esperada:**
```
git version 2.xx.x.windows.1
```

---

## 🗄️ Instalação do MySQL

### Passo 1: Download do MySQL Installer

1. Acesse: https://dev.mysql.com/downloads/installer/
2. Baixe o **"MySQL Installer Community"** (mysql-installer-community-8.0.xx.msi)
3. Escolha a versão **"mysql-installer-web-community"** (menor, faz download durante instalação)

### Passo 2: Instalação

1. Execute o instalador como **Administrador**

2. Na tela de boas-vindas, escolha:
   - **"Developer Default"** (instala MySQL Server, Workbench, Shell, etc.)
   - Clique em **"Next"**

3. Na tela "Check Requirements":
   - Se aparecer avisos sobre componentes faltando, clique em **"Execute"** para instalá-los
   - Caso contrário, clique em **"Next"**

4. Na tela "Installation":
   - Clique em **"Execute"** para iniciar a instalação de todos os componentes
   - Aguarde a conclusão (pode demorar alguns minutos)
   - Clique em **"Next"**

5. Na tela "Product Configuration":
   - Clique em **"Next"** para começar a configuração

### Passo 3: Configuração do MySQL Server

1. **Type and Networking:**
   - Config Type: **"Development Computer"**
   - Connectivity: 
     - ✅ TCP/IP
     - Port: **3306** (padrão)
     - ✅ Open Windows Firewall ports for network access
     - ✅ Show Advanced and Logging Options
   - Clique em **"Next"**

2. **Authentication Method:**
   - Selecione: **"Use Strong Password Encryption for Authentication (RECOMMENDED)"**
   - Clique em **"Next"**

3. **Accounts and Roles:**
   - **MySQL Root Password:** Digite uma senha forte e **anote-a**
     - Exemplo: `MeuMySQL2025!`
   - **Repeat Password:** Digite novamente
   - **(Opcional)** Clique em **"Add User"** para criar usuário do projeto:
     - Username: `ceu_tres_pontes`
     - Host: `localhost`
     - Role: `DB Admin`
     - Password: `CeuTresPontes2025!` (anote também)
   - Clique em **"Next"**

4. **Windows Service:**
   - ✅ Configure MySQL Server as a Windows Service
   - Windows Service Name: **MySQL80** (padrão)
   - ✅ Start the MySQL Server at System Startup
   - Run Windows Service as: **Standard System Account**
   - Clique em **"Next"**

5. **Server File Permissions:**
   - Selecione: **"Yes, grant full access to the user running the Windows Service..."**
   - Clique em **"Next"**

6. **Apply Configuration:**
   - Clique em **"Execute"**
   - Aguarde todas as etapas serem concluídas (com ✅ verde)
   - Clique em **"Finish"**

7. Configuração de outros produtos (Router, etc.):
   - Mantenha as configurações padrão
   - Clique em **"Next"** até finalizar

8. **Connect To Server:**
   - Password: Digite a senha **root** que você definiu
   - Clique em **"Check"** para verificar conexão
   - Se OK, clique em **"Next"**

9. **Apply Configuration:**
   - Clique em **"Execute"**
   - Clique em **"Finish"**

10. Na tela final:
    - ✅ Start MySQL Workbench after Setup
    - ✅ Start MySQL Shell after Setup
    - Clique em **"Finish"**

### Passo 4: Verificação

1. Abra o **MySQL Workbench** (deve ter aberto automaticamente)

2. Clique na conexão **"Local instance MySQL80"**

3. Digite a senha **root**

4. Se conectar com sucesso, MySQL está instalado corretamente!

### Passo 5: Verificação via Linha de Comando

Abra o **PowerShell** e execute:

```powershell
mysql --version
```

Se não funcionar, adicione MySQL ao PATH:

1. Pressione `Win + Pause/Break` (ou clique com botão direito em "Este Computador" > "Propriedades")
2. Clique em **"Configurações avançadas do sistema"**
3. Clique em **"Variáveis de Ambiente"**
4. Em "Variáveis do sistema", selecione **"Path"** e clique em **"Editar"**
5. Clique em **"Novo"** e adicione:
   ```
   C:\Program Files\MySQL\MySQL Server 8.0\bin
   ```
6. Clique em **"OK"** em todas as janelas
7. **Feche e abra novamente o PowerShell**
8. Teste novamente: `mysql --version`

**Saída esperada:**
```
mysql  Ver 8.0.xx for Win64 on x86_64 (MySQL Community Server - GPL)
```

---

## 📡 Instalação do Mosquitto MQTT

### Método 1: Instalação via Chocolatey (Recomendado)

#### Instalar Chocolatey (se não tiver)

1. Abra o **PowerShell como Administrador** (clique com botão direito > "Executar como administrador")

2. Execute o seguinte comando:

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

3. Aguarde a instalação do Chocolatey

4. Verifique a instalação:

```powershell
choco --version
```

#### Instalar Mosquitto

No mesmo PowerShell (como Administrador):

```powershell
choco install mosquitto -y
```

### Método 2: Instalação Manual

1. Acesse: https://mosquitto.org/download/
2. Baixe o instalador para Windows (64-bit): `mosquitto-x.x.x-install-windows-x64.exe`
3. Execute o instalador como **Administrador**
4. Siga o assistente de instalação (mantenha as opções padrão)
5. Clique em **"Install"**
6. Clique em **"Finish"**

### Configuração do Mosquitto

1. Navegue até a pasta de instalação:
   ```powershell
   cd "C:\Program Files\mosquitto"
   ```

2. Crie um arquivo de configuração:
   ```powershell
   notepad mosquitto.conf
   ```

3. Adicione o seguinte conteúdo:
   ```ini
   # Configuração Mosquitto - CEU Tres Pontes
   # Ambiente de Desenvolvimento Local
   
   # Listeners
   listener 1883
   protocol mqtt
   
   # Permitir conexões anônimas (APENAS DESENVOLVIMENTO)
   allow_anonymous true
   
   # Logs
   log_dest file C:/Program Files/mosquitto/mosquitto.log
   log_type all
   
   # Persistência
   persistence true
   persistence_location C:/Program Files/mosquitto/data/
   
   # Autosave
   autosave_interval 60
   ```

4. Salve e feche (Ctrl+S, Alt+F4)

5. Crie a pasta de dados:
   ```powershell
   mkdir data
   ```

### Instalar e Iniciar o Serviço

No **PowerShell como Administrador**:

```powershell
# Instalar o serviço
mosquitto install

# Iniciar o serviço
net start mosquitto
```

### Adicionar Mosquitto ao PATH

Para usar os comandos `mosquitto_sub` e `mosquitto_pub`, precisamos adicionar o Mosquitto ao PATH:

#### Via Interface Gráfica (Recomendado)

1. Pressione **`Win + Pause/Break`** (ou clique com botão direito em "Este Computador" > "Propriedades")
2. Clique em **"Configurações avançadas do sistema"**
3. Clique em **"Variáveis de Ambiente..."**
4. Na seção **"Variáveis do sistema"**, selecione **"Path"** e clique em **"Editar..."**
5. Clique em **"Novo"** e adicione:
   ```
   C:\Program Files\mosquitto
   ```
6. Clique em **"OK"** em todas as janelas
7. **Feche e abra novamente o PowerShell**

#### Via PowerShell como Administrador (Alternativa)

```powershell
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\mosquitto", [EnvironmentVariableTarget]::Machine)
```

**Importante:** Feche e abra o PowerShell após adicionar ao PATH.

### Verificação

```powershell
# Verificar se o serviço está rodando
Get-Service mosquitto
```

**Saída esperada:**
```
Status   Name               DisplayName
------   ----               -----------
Running  mosquitto          Mosquitto Broker
```

Verificar se os comandos estão disponíveis:

```powershell
mosquitto_sub --help
mosquitto_pub --help
```

**Se aparecer erro "não é reconhecido como nome de cmdlet":**
- Você não adicionou ao PATH ou não fechou/abriu o PowerShell
- Use a solução temporária: `$env:Path += ";C:\Program Files\mosquitto"`

Teste de publicação/subscrição:

1. Abra **dois** PowerShells separados

2. No **PowerShell 1** (Subscriber):
   ```powershell
   mosquitto_sub -h localhost -t "test/topic"
   ```

3. No **PowerShell 2** (Publisher):
   ```powershell
   mosquitto_pub -h localhost -t "test/topic" -m "Hello MQTT!"
   ```

4. Você deve ver **"Hello MQTT!"** no PowerShell 1

Se funcionou, Mosquitto está instalado corretamente! Pressione **Ctrl+C** em ambos os PowerShells para sair.

---

## 📦 Clone do Projeto

### Passo 1: Criar Pasta de Desenvolvimento

Abra o **PowerShell** (não precisa ser Administrador):

```powershell
# Criar pasta de projetos (você pode escolher outro local)
mkdir C:\Dev
cd C:\Dev
```

### Passo 2: Clonar o Repositório

```powershell
# Clone via HTTPS
git clone https://github.com/RogerioVieira77/PI---IV---V1.git

# OU clone via SSH (se configurou chaves SSH)
# git clone git@github.com:RogerioVieira77/PI---IV---V1.git
```

### Passo 3: Entrar na Pasta do Projeto

```powershell
cd "PI---IV---V1"
```

Ou se foi clonado com o nome diferente:
```powershell
cd "PI - IV - V1"
```

---

## 🐍 Configuração do Ambiente Virtual Python

### Passo 1: Criar Ambiente Virtual

Dentro da pasta do projeto:

```powershell
# Criar ambiente virtual chamado 'venv'
python -m venv venv
```

Aguarde a criação do ambiente (pode levar alguns segundos).

### Passo 2: Ativar o Ambiente Virtual

```powershell
# Ativar o ambiente virtual
.\venv\Scripts\Activate.ps1
```

**IMPORTANTE:** Se aparecer erro de permissão, execute:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

E tente ativar novamente.

**Quando ativado corretamente, você verá `(venv)` no início da linha do PowerShell:**

```powershell
(venv) PS C:\Dev\PI---IV---V1>
```

### Passo 3: Atualizar pip no Ambiente Virtual

```powershell
python -m pip install --upgrade pip
```

**IMPORTANTE:** Sempre ative o ambiente virtual antes de trabalhar no projeto!

---

## 📚 Instalação das Dependências

Com o ambiente virtual **ativado** (deve ter `(venv)` no prompt):

### Fase 1 (Simuladores) - Sem dependências externas

Os simuladores já funcionam, não precisam de instalação adicional!

### Fase 2 (Gateway + MQTT)

```powershell
pip install -r backend\requirements-phase2.txt
```

### Fase 3 (Backend Flask + MySQL)

```powershell
pip install -r backend\requirements-phase3.txt
```

**⚠️ IMPORTANTE - Problema Comum no Windows:**

Se você receber erro ao instalar `mysqlclient` (erro `fatal error C1083: mysql.h: No such file or directory`), é porque este pacote precisa compilar código C e não encontra os arquivos de desenvolvimento do MySQL.

**Solução:** O arquivo `requirements-phase3.txt` já foi ajustado para usar apenas **PyMySQL** (Python puro, sem compilação). Se você ainda tiver o erro:

1. Edite `backend\requirements-phase3.txt`
2. Comente ou remova a linha `mysqlclient==2.2.0`
3. Execute novamente: `pip install -r backend\requirements-phase3.txt`

O PyMySQL funciona perfeitamente como driver MySQL para SQLAlchemy no Windows.

### Todas as Dependências (Recomendado)

Para instalar tudo de uma vez:

```powershell
pip install -r requirements.txt
```

### Verificação

Liste os pacotes instalados:

```powershell
pip list
```

Você deve ver pacotes como:
- paho-mqtt
- Flask
- SQLAlchemy
- PyMySQL
- etc.

---

## 🗃️ Configuração do Banco de Dados

### Passo 1: Criar o Banco de Dados

#### Via MySQL Workbench (Interface Gráfica)

1. Abra o **MySQL Workbench**
2. Conecte-se à instância local (senha root)
3. Clique em **"Create a new schema"** (ícone de cilindro com +)
4. Nome: `ceu_tres_pontes_db`
5. Charset: `utf8mb4`
6. Collation: `utf8mb4_unicode_ci`
7. Clique em **"Apply"**
8. Revise o SQL e clique em **"Apply"** novamente
9. Clique em **"Finish"**

#### Via Linha de Comando

Abra o PowerShell e execute:

```powershell
mysql -u root -p
```

Digite a senha root. No prompt do MySQL:

```sql
-- Criar banco de dados
CREATE DATABASE ceu_tres_pontes_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Criar usuário do projeto (se não criou durante instalação)
CREATE USER 'ceu_tres_pontes'@'localhost' IDENTIFIED BY 'CeuTresPontes2025!';

-- Se receber erro "ERROR 1396: Operation CREATE USER failed"
-- significa que o usuário JÁ EXISTE. Neste caso, use um dos comandos abaixo:

-- Opção 1: Apenas garantir as permissões (recomendado)
-- GRANT ALL PRIVILEGES ON ceu_tres_pontes_db.* TO 'ceu_tres_pontes'@'localhost';

-- Opção 2: Alterar a senha do usuário existente
-- ALTER USER 'ceu_tres_pontes'@'localhost' IDENTIFIED BY 'CeuTresPontes2025!';

-- Opção 3: Remover e recriar (se necessário)
-- DROP USER 'ceu_tres_pontes'@'localhost';
-- CREATE USER 'ceu_tres_pontes'@'localhost' IDENTIFIED BY 'CeuTresPontes2025!';

-- Conceder privilégios
GRANT ALL PRIVILEGES ON ceu_tres_pontes_db.* TO 'ceu_tres_pontes'@'localhost';

-- Aplicar mudanças
FLUSH PRIVILEGES;

-- Verificar
SHOW DATABASES;

-- Sair
EXIT;
```

### Passo 2: Testar Conexão com Usuário do Projeto

```powershell
mysql -u ceu_tres_pontes -p ceu_tres_pontes_db
```

Digite a senha: `CeuTresPontes2025!`

Se conectar, está OK! Digite `EXIT;` para sair.

### Passo 3: Inicializar as Tabelas (quando o backend estiver pronto)

Com o ambiente virtual **ativado**, na **raiz do projeto** (não na pasta backend):

```powershell
# IMPORTANTE: Certifique-se de estar na RAIZ do projeto
# Você deve estar em: C:\PI - IV - V1 (ou C:\Dev\PI---IV---V1)

# Configurar FLASK_APP
$env:FLASK_APP = "backend/app.py"

# OU criar arquivo .flaskenv (recomendado - só precisa fazer uma vez)
# notepad .flaskenv
# Adicione: FLASK_APP=backend/app.py

# Inicializar banco de dados
flask init-db

# OU usar Python diretamente (alternativa)
python backend\app.py init-db

# Popular com dados de exemplo (opcional)
flask seed-db
```

**IMPORTANTE:** Execute sempre da **raiz do projeto**, não da pasta `backend/`!

---

## ⚙️ Configuração das Variáveis de Ambiente

### Passo 1: Criar Arquivo .env

Na **raiz do projeto**, crie um arquivo `.env`:

```powershell
notepad .env
```

Adicione o seguinte conteúdo:

```env
# ==================================================
# Configuração de Ambiente - CEU Tres Pontes
# Ambiente: DESENVOLVIMENTO LOCAL
# ==================================================

# === FLASK ===
FLASK_APP=backend/app.py
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key-local-12345-change-in-production
JWT_SECRET_KEY=jwt-dev-secret-key-local-67890-change-in-production
JWT_ACCESS_TOKEN_EXPIRES=3600

# === DATABASE (MySQL) ===
DB_HOST=localhost
DB_PORT=3306
DB_USER=ceu_tres_pontes
DB_PASSWORD=CeuTresPontes2025!
DB_NAME=ceu_tres_pontes_db

# === MQTT (Mosquitto) ===
MQTT_BROKER_HOST=localhost
MQTT_BROKER_PORT=1883
MQTT_USERNAME=
MQTT_PASSWORD=
MQTT_BASE_TOPIC=ceu/tres_pontes

# === GATEWAY ===
GATEWAY_ID=gateway_dev_001
GATEWAY_NAME=Gateway Desenvolvimento Local
GATEWAY_LOCATION=Workstation Local

# === API ===
API_PREFIX=/api/v1
API_TITLE=CEU Tres Pontes API - Dev
API_VERSION=1.0.0

# === CORS ===
CORS_ORIGINS=http://localhost:3000,http://localhost:5000,http://127.0.0.1:3000,http://127.0.0.1:5000

# === LOGGING ===
LOG_LEVEL=DEBUG
LOG_FILE=logs/backend.log

# === PAGINATION ===
DEFAULT_PAGE_SIZE=50
MAX_PAGE_SIZE=1000

# === REDIS (Opcional - Para caching) ===
# REDIS_HOST=localhost
# REDIS_PORT=6379
# REDIS_DB=0

# === RABBITMQ (Opcional - Para filas) ===
# RABBITMQ_HOST=localhost
# RABBITMQ_PORT=5672
# RABBITMQ_USER=guest
# RABBITMQ_PASSWORD=guest
```

**Salve e feche** (Ctrl+S, Alt+F4)

**IMPORTANTE:** Ajuste as senhas conforme você definiu!

### Passo 2: Criar Pasta de Logs

```powershell
mkdir logs
```

### Passo 3: Adicionar .env ao .gitignore

Se o arquivo `.gitignore` ainda não existir, crie-o:

```powershell
notepad .gitignore
```

Adicione (ou verifique se já tem):

```gitignore
# Ambiente
.env
.env.local
.env.*.local

# Virtual Environment
venv/
env/
ENV/
.venv/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Logs
logs/
*.log

# Database
*.db
*.sqlite
*.sqlite3

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

---

## 🧪 Testando o Ambiente

### Teste 1: Simuladores (Fase 1)

Com ambiente virtual **ativado**:

```powershell
# Executar testes dos simuladores
python tests\test_simuladores.py
```

**Saída esperada:** Vários testes passando (✅) para LoRa, ZigBee, Sigfox e RFID.

### Teste 2: Gateway + MQTT (Fase 2)

#### Passo 1: Verificar se Mosquitto está rodando

```powershell
Get-Service mosquitto
```

Se não estiver rodando:

```powershell
net start mosquitto
```

#### Passo 2: Executar teste de integração MQTT

```powershell
python tests\test_mqtt_integration.py
```

**Saída esperada:** Mensagens de teste sendo publicadas e recebidas via MQTT.

### Teste 3: Backend Flask (Fase 3)

#### Passo 1: Inicializar banco de dados

```powershell
cd backend
flask init-db
```

#### Passo 2: Popular banco com dados de exemplo

```powershell
flask seed-db
```

#### Passo 3: Iniciar servidor Flask

```powershell
flask run
```

Ou:

```powershell
python app.py
```

**Saída esperada:**

```
 * Serving Flask app 'backend/app.py'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```

#### Passo 4: Testar API

Abra um **novo PowerShell** (sem fechar o anterior) e execute:

```powershell
# Testar endpoint de saúde
curl http://localhost:5000/api/v1/health
```

Ou abra o navegador: http://localhost:5000/api/v1/health

**Resposta esperada:**

```json
{
  "status": "healthy",
  "service": "CEU Tres Pontes API",
  "timestamp": "2025-10-19T12:00:00Z"
}
```

Para parar o servidor Flask, pressione **Ctrl+C** no PowerShell onde está rodando.

### Teste 4: Gateway Completo

Com Mosquitto rodando, execute:

```powershell
# Voltar para raiz do projeto
cd ..

# Rodar gateway
python backend\gateway\gateway.py
```

Você deve ver mensagens de sensores sendo coletadas e publicadas via MQTT.

Para parar, pressione **Ctrl+C**.

---

## 💻 IDEs Recomendadas

### Visual Studio Code (Recomendado)

#### Instalação

1. Baixe: https://code.visualstudio.com/
2. Execute o instalador
3. Marque todas as opções de integração com Windows Explorer
4. Instale

#### Extensões Recomendadas

Abra o VS Code e instale as seguintes extensões (Ctrl+Shift+X):

1. **Python** (Microsoft) - `ms-python.python`
2. **Pylance** (Microsoft) - `ms-python.vscode-pylance`
3. **Python Debugger** (Microsoft) - `ms-python.debugpy`
4. **Git Extension Pack** - Ferramentas Git
5. **MySQL** (cweijan) - `cweijan.vscode-mysql-client2`
6. **Thunder Client** - Testes de API (alternativa ao Postman)
7. **Better Comments** - Comentários coloridos
8. **GitLens** - Melhorias no Git
9. **Material Icon Theme** - Ícones bonitos
10. **Python Indent** - Indentação automática

#### Configuração do VS Code para o Projeto

1. Abra a pasta do projeto no VS Code:
   ```powershell
   code .
   ```

2. O VS Code deve detectar automaticamente o ambiente virtual `venv`

3. Selecione o interpretador Python:
   - Pressione **Ctrl+Shift+P**
   - Digite "Python: Select Interpreter"
   - Escolha `.\venv\Scripts\python.exe`

### PyCharm Community (Alternativa)

1. Baixe: https://www.jetbrains.com/pycharm/download/
2. Escolha a versão **Community** (gratuita)
3. Instale
4. Abra o projeto
5. Configure o interpretador Python para usar o `venv`

---

## 🔧 Ferramentas Adicionais

### Postman (Testes de API)

1. Baixe: https://www.postman.com/downloads/
2. Instale
3. Crie uma coleção para testar os endpoints da API

### MySQL Workbench

Já instalado junto com MySQL. Use para:
- Visualizar dados
- Executar queries SQL
- Gerenciar banco de dados

### MQTT Explorer (Cliente MQTT Gráfico)

1. Baixe: http://mqtt-explorer.com/
2. Instale
3. Configure conexão:
   - Host: `localhost`
   - Port: `1883`
   - Username/Password: (deixe vazio se allow_anonymous=true)
4. Conecte e visualize mensagens MQTT em tempo real

### Git GUI / GitKraken (Interface Gráfica para Git)

**Git GUI** (já vem com Git):
```powershell
git gui
```

**GitKraken** (mais avançado):
1. Baixe: https://www.gitkraken.com/
2. Instale
3. Abra o repositório do projeto

---

## 🐛 Resolução de Problemas

### Problema: Python não é reconhecido no PowerShell

**Solução:**

1. Verifique se Python foi adicionado ao PATH durante instalação
2. Se não, adicione manualmente:
   - Win + Pause/Break > Configurações avançadas > Variáveis de Ambiente
   - Em "Path" do usuário, adicione:
     - `C:\Python312`
     - `C:\Python312\Scripts`
3. Feche e abra novamente o PowerShell

### Problema: Erro ao ativar ambiente virtual

**Erro:** "execution of scripts is disabled on this system"

**Solução:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problema: MySQL não inicia

**Solução:**

```powershell
# Parar o serviço
net stop mysql80

# Iniciar novamente
net start mysql80
```

Se o erro persistir, verifique os logs em:
```
C:\ProgramData\MySQL\MySQL Server 8.0\Data\*.err
```

### Problema: Mosquitto não inicia

**Solução:**

```powershell
# Reinstalar o serviço
cd "C:\Program Files\mosquitto"
mosquitto uninstall
mosquitto install

# Iniciar
net start mosquitto
```

### Problema: Porta 3306 (MySQL) ou 1883 (MQTT) já está em uso

**Verificar qual processo está usando a porta:**

```powershell
netstat -ano | findstr :3306
# ou
netstat -ano | findstr :1883
```

Anote o PID (última coluna) e finalize o processo:

```powershell
taskkill /PID <número_do_pid> /F
```

### Problema: pip install falha com erro de SSL

**Solução:**

```powershell
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org <pacote>
```

### Problema: Flask não encontra o módulo app

**Solução:**

Certifique-se de estar na pasta correta e que o FLASK_APP está configurado:

```powershell
$env:FLASK_APP = "backend/app.py"
flask run
```

### Problema: Erro ao instalar mysqlclient no Windows

**Erro:** `fatal error C1083: Não é possível abrir arquivo incluir: 'mysql.h': No such file or directory`

**Causa:** O pacote `mysqlclient` precisa compilar código C e não encontra os arquivos de desenvolvimento (headers) do MySQL/MariaDB.

**Solução 1 (Recomendada):** Usar apenas PyMySQL

O arquivo `requirements-phase3.txt` já foi ajustado para comentar o `mysqlclient`. Se você ainda tiver o erro:

```powershell
# Editar o arquivo requirements
notepad backend\requirements-phase3.txt

# Comente ou remova a linha:
# mysqlclient==2.2.0

# Instale novamente
pip install -r backend\requirements-phase3.txt
```

**Solução 2:** Instalar MySQL Connector/C

Se você realmente precisar do `mysqlclient`:

1. Baixe o MySQL Connector/C: https://dev.mysql.com/downloads/connector/c/
2. Instale em `C:\mariadb-connector` ou `C:\mysql-connector`
3. Adicione às variáveis de ambiente:
   - `MYSQLCLIENT_CFLAGS=-I"C:\mysql-connector\include"`
   - `MYSQLCLIENT_LDFLAGS=-L"C:\mysql-connector\lib"`
4. Tente instalar novamente: `pip install mysqlclient`

**Solução 3:** Usar wheel pré-compilado

```powershell
# Baixe o wheel de https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
# Instale o arquivo .whl:
pip install mysqlclient-2.2.0-cp312-cp312-win_amd64.whl
```

**Nota:** Para este projeto, **PyMySQL é suficiente** e funciona perfeitamente no Windows sem necessidade de compilação.

### Problema: Erro ao instalar gunicorn no Windows

**Erro:** `gunicorn` não funciona no Windows (é específico para Unix/Linux)

**Solução:** Use **waitress** (já incluído no requirements-phase3.txt)

```powershell
pip install waitress
```

Para rodar o servidor em produção no Windows:

```powershell
# Ao invés de: gunicorn app:app
# Use:
waitress-serve --host=0.0.0.0 --port=5000 backend.app:app
```

### Problema: Erro de conexão com MySQL

**Erro:** `ERROR 1396 (HY000): Operation CREATE USER failed for 'ceu_tres_pontes'@'localhost'`

**Causa:** O usuário já existe no MySQL (provavelmente foi criado durante a instalação).

**Solução 1 (Recomendada):** Verificar e conceder permissões

No prompt do MySQL:

```sql
-- Verificar se o usuário existe
SELECT User, Host FROM mysql.user WHERE User = 'ceu_tres_pontes';

-- Se existir, apenas conceder permissões
GRANT ALL PRIVILEGES ON ceu_tres_pontes_db.* TO 'ceu_tres_pontes'@'localhost';
FLUSH PRIVILEGES;

-- Verificar as permissões
SHOW GRANTS FOR 'ceu_tres_pontes'@'localhost';
```

**Solução 2:** Alterar a senha

```sql
-- Se você não lembra a senha do usuário
ALTER USER 'ceu_tres_pontes'@'localhost' IDENTIFIED BY 'CeuTresPontes2025!';
GRANT ALL PRIVILEGES ON ceu_tres_pontes_db.* TO 'ceu_tres_pontes'@'localhost';
FLUSH PRIVILEGES;
```

**Solução 3:** Recriar o usuário

```sql
-- Remover e recriar
DROP USER 'ceu_tres_pontes'@'localhost';
CREATE USER 'ceu_tres_pontes'@'localhost' IDENTIFIED BY 'CeuTresPontes2025!';
GRANT ALL PRIVILEGES ON ceu_tres_pontes_db.* TO 'ceu_tres_pontes'@'localhost';
FLUSH PRIVILEGES;
```

**Testar a conexão:**

```powershell
mysql -u ceu_tres_pontes -p ceu_tres_pontes_db
# Digite a senha: CeuTresPontes2025!
```

### Problema: Erro de conexão com MySQL (outros casos)

**Verifique:**

1. MySQL está rodando: `Get-Service mysql80`
2. Credenciais no `.env` estão corretas
3. Banco de dados `ceu_tres_pontes_db` foi criado
4. Usuário `ceu_tres_pontes` tem permissões

**Teste a conexão:**

```powershell
mysql -u ceu_tres_pontes -p ceu_tres_pontes_db
```

### Problema: Flask não encontra o módulo app

**Erro:** `Error: Could not import 'app'` ou `Error: No such command 'init-db'`

**Causa:** Você está executando os comandos Flask da pasta errada ou a variável `FLASK_APP` não está configurada.

**Solução:**

```powershell
# 1. Voltar para RAIZ do projeto (não estar em backend/)
cd "C:\PI - IV - V1"

# 2. Verificar que ambiente virtual está ativado
# Deve ter (venv) no prompt

# 3. Configurar FLASK_APP
$env:FLASK_APP = "backend/app.py"

# 4. Verificar
flask --version

# 5. Executar comando
flask init-db
```

**Solução Permanente:** Criar arquivo `.flaskenv` na raiz:

```
FLASK_APP=backend/app.py
FLASK_ENV=development
FLASK_DEBUG=True
```

Depois instalar: `pip install python-dotenv`

**Alternativa:** Executar via Python diretamente:

```powershell
python backend\app.py init-db
```

### Problema: ModuleNotFoundError ao rodar testes

**Solução:**

Certifique-se de que:
1. Ambiente virtual está **ativado** (deve ter `(venv)` no prompt)
2. Dependências foram instaladas: `pip install -r requirements.txt`
3. Está na pasta raiz do projeto

---

## 📝 Checklist de Instalação Completa

Use este checklist para verificar se tudo foi instalado corretamente:

- [ ] ✅ Python 3.12.3 instalado e no PATH
- [ ] ✅ pip atualizado
- [ ] ✅ Git instalado e configurado
- [ ] ✅ MySQL 8.0 instalado e rodando
- [ ] ✅ Banco de dados `ceu_tres_pontes_db` criado
- [ ] ✅ Usuário MySQL `ceu_tres_pontes` criado
- [ ] ✅ Mosquitto MQTT instalado e rodando
- [ ] ✅ Projeto clonado do GitHub
- [ ] ✅ Ambiente virtual Python criado
- [ ] ✅ Ambiente virtual ativado
- [ ] ✅ Dependências Python instaladas
- [ ] ✅ Arquivo `.env` criado e configurado
- [ ] ✅ Pasta `logs` criada
- [ ] ✅ Testes dos simuladores passando
- [ ] ✅ Teste MQTT passando
- [ ] ✅ Backend Flask iniciando sem erros
- [ ] ✅ VS Code (ou outra IDE) instalado
- [ ] ✅ Extensões do VS Code instaladas

---

## 🎓 Próximos Passos

Agora que seu ambiente está configurado, você pode:

1. **Explorar o código:**
   - Simuladores em `sensores/`
   - Gateway em `backend/gateway/`
   - API Flask em `backend/app/`

2. **Desenvolver novas funcionalidades:**
   - Criar novos endpoints na API
   - Adicionar novos tipos de sensores
   - Implementar dashboards no frontend

3. **Executar testes:**
   ```powershell
   # Rodar todos os testes
   pytest tests/
   
   # Rodar com cobertura
   pytest --cov=backend tests/
   ```

4. **Estudar a documentação:**
   - Leia os arquivos em `docs/`
   - Veja o README.md principal
   - Consulte a documentação da API (quando disponível)

5. **Contribuir:**
   - Crie branches para novas features
   - Faça commits descritivos
   - Envie pull requests

---

## 📞 Suporte

Se encontrar problemas durante a instalação:

1. Consulte a seção "Resolução de Problemas" acima
2. Verifique a documentação em `docs/`
3. Consulte o arquivo `docs/TROUBLESHOOTING_PERMISSOES.md`
4. Verifique os logs do sistema:
   - MySQL: `C:\ProgramData\MySQL\MySQL Server 8.0\Data\*.err`
   - Mosquitto: `C:\Program Files\mosquitto\mosquitto.log`
   - Backend: `logs/backend.log`
   - Gateway: `logs/gateway.log`

---

## 📚 Documentação Adicional

- [README.md](README.md) - Visão geral do projeto
- [docs/README.md](docs/README.md) - Documentação completa
- [docs/FASE2_MQTT.md](docs/FASE2_MQTT.md) - Detalhes sobre MQTT e Gateway
- [QUICKSTART_FASE2.md](QUICKSTART_FASE2.md) - Guia rápido Fase 2
- [QUICKSTART_FASE3.md](QUICKSTART_FASE3.md) - Guia rápido Fase 3

---

## 📄 Licença

Este projeto é parte do Projeto Integrador IV - CEU Tres Pontes.

---

**Última atualização:** Outubro 2025  
**Versão do documento:** 1.0  
**Sistema:** CEU Tres Pontes - Sistema de Controle de Acesso

---

🎉 **Parabéns!** Seu ambiente de desenvolvimento está pronto!

Bom código! 🚀👨‍💻👩‍💻
