# 🚀 Deploy Local - SmartCEU

## Guia Completo de Instalação e Execução Local

Este documento descreve o passo a passo para executar a aplicação SmartCEU localmente no Windows, conectando-se ao banco de dados remoto do servidor de produção.

---

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Preparação do Ambiente](#preparação-do-ambiente)
3. [Configuração do Banco de Dados Remoto](#configuração-do-banco-de-dados-remoto)
4. [Instalação das Dependências](#instalação-das-dependências)
5. [Configuração da Aplicação](#configuração-da-aplicação)
6. [Execução da Aplicação](#execução-da-aplicação)
7. [Testes e Verificação](#testes-e-verificação)
8. [Troubleshooting](#troubleshooting)
9. [Comandos Úteis](#comandos-úteis)

---

## 🎯 Pré-requisitos

Antes de começar, certifique-se de ter instalado em seu Windows:

### Obrigatórios

- ✅ **Python 3.12.3 ou superior**
  - Download: https://www.python.org/downloads/
  - ⚠️ Marcar "Add Python to PATH" durante a instalação

- ✅ **Git**
  - Download: https://git-scm.com/download/win
  - Ou usar GitHub Desktop

- ✅ **Editor de Código** (recomendado)
  - VS Code: https://code.visualstudio.com/
  - PyCharm Community: https://www.jetbrains.com/pycharm/

### Opcionais (para testes completos)

- ⚪ **Mosquitto MQTT Broker** (para testar Gateway IoT)
  - Download: https://mosquitto.org/download/
  - Versão Windows instalador

- ⚪ **Postman** (para testar API)
  - Download: https://www.postman.com/downloads/

---

## 📂 Preparação do Ambiente

### Passo 1: Clonar o Repositório

Abra o **PowerShell** ou **Terminal** e execute:

```powershell
# Navegar para o diretório onde deseja clonar
cd c:\

# Clonar o repositório (se ainda não tiver)
git clone https://github.com/RogerioVieira77/DRP14-PJI410-SALA-004-GRUPO-05.git

# Entrar no diretório
cd DRP14-PJI410-SALA-004-GRUPO-05
```

**Se já tem o repositório clonado:**

```powershell
# Navegar para o diretório
cd c:\DRP14-PJI410-SALA-004-GRUPO-05

# Atualizar com as últimas mudanças
git pull origin main
```

---

### Passo 2: Verificar Instalação do Python

```powershell
# Verificar versão do Python
python --version
# Saída esperada: Python 3.12.3 ou superior

# Verificar pip
pip --version
# Saída esperada: pip 24.x.x ou superior

# Se pip não estiver disponível
python -m ensurepip --upgrade
```

---

### Passo 3: Criar Ambiente Virtual Python

O ambiente virtual isola as dependências do projeto:

```powershell
# Navegar para a pasta do backend
cd app\backend

# Criar ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
.\venv\Scripts\Activate.ps1

# Você verá (venv) no início da linha do prompt
```

**⚠️ Erro de Política de Execução?**

Se aparecer erro de política de execução, execute:

```powershell
# Permitir scripts temporariamente
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Tentar ativar novamente
.\venv\Scripts\Activate.ps1
```

---

## 🗄️ Configuração do Banco de Dados Remoto

### Passo 4: Verificar Conectividade com o Servidor

Antes de configurar, vamos testar se conseguimos acessar o servidor:

```powershell
# Testar ping ao servidor
ping 82.25.75.88

# Testar conexão na porta MySQL (3306)
Test-NetConnection -ComputerName 82.25.75.88 -Port 3306
```

**Resultado Esperado:**
- Ping: Resposta com tempo < 100ms
- Port 3306: TcpTestSucceeded = True

**⚠️ Se a porta 3306 não estiver acessível:**

O servidor pode estar com firewall bloqueando acesso externo ao MySQL. Neste caso, você tem 3 opções:

**Opção A: Solicitar Liberação do IP no Servidor** (Recomendado)
```bash
# No servidor (via SSH), executar:
sudo ufw allow from SEU_IP_PUBLICO to any port 3306

# Descobrir seu IP público:
# Acesse: https://www.whatismyip.com/
```

**Opção B: Usar Túnel SSH**
```powershell
# Criar túnel SSH para MySQL
ssh -L 3306:localhost:3306 usuario@82.25.75.88

# Depois configurar conexão para localhost:3306
```

**Opção C: Usar Banco Local** (para testes)
```powershell
# Instalar MySQL localmente
# Download: https://dev.mysql.com/downloads/installer/

# Restaurar backup do banco
# (solicitar dump do servidor)
```

---

### Passo 5: Criar Arquivo de Configuração `.env`

Crie o arquivo `.env` na pasta `app\backend\`:

```powershell
# Certifique-se de estar em app\backend
cd c:\DRP14-PJI410-SALA-004-GRUPO-05\app\backend

# Criar arquivo .env
New-Item -Path .env -ItemType File

# Abrir com Notepad
notepad .env
```

**Conteúdo do arquivo `.env`:**

```ini
# ============================================
# CONFIGURAÇÃO DE DESENVOLVIMENTO LOCAL
# SmartCEU - Conexão com Banco Remoto
# ============================================

# Ambiente
FLASK_ENV=development
FLASK_APP=app.py
FLASK_DEBUG=1

# Secret Keys (para desenvolvimento)
SECRET_KEY=dev-local-secret-key-change-in-production
JWT_SECRET_KEY=dev-local-jwt-secret-key-change-in-production

# JWT Configuration
JWT_ACCESS_TOKEN_EXPIRES=86400  # 24 horas em segundos

# ============================================
# BANCO DE DADOS REMOTO (Servidor Produção)
# ============================================

DB_HOST=82.25.75.88
DB_PORT=3306
DB_USER=smartceu_user
DB_PASSWORD=SUA_SENHA_MYSQL_AQUI
DB_NAME=smartceu_db

# ⚠️ IMPORTANTE: Substituir SUA_SENHA_MYSQL_AQUI pela senha real
# Solicite a senha ao administrador do servidor

# ============================================
# Se usar túnel SSH, alterar para:
# DB_HOST=localhost
# DB_PORT=3306
# ============================================

# ============================================
# MQTT Configuration (Opcional - para Gateway)
# ============================================

MQTT_BROKER_HOST=82.25.75.88
MQTT_BROKER_PORT=1883
MQTT_BASE_TOPIC=ceu/tres_pontes
GATEWAY_ID=gateway_local_dev

# ============================================
# API Configuration
# ============================================

API_PREFIX=/api/v1
API_TITLE=CEU Tres Pontes API
API_VERSION=1.0.0

# CORS - Permitir todas as origens em dev
CORS_ORIGINS=*

# Pagination
DEFAULT_PAGE_SIZE=50
MAX_PAGE_SIZE=1000

# Logging
LOG_LEVEL=DEBUG
LOG_FILE=logs/backend_local.log

# ============================================
# Opcionais (não necessários para dev local)
# ============================================

# Redis (se estiver usando cache)
# REDIS_HOST=localhost
# REDIS_PORT=6379
# REDIS_DB=0

# RabbitMQ (se estiver usando filas)
# RABBITMQ_HOST=localhost
# RABBITMQ_PORT=5672
# RABBITMQ_USER=guest
# RABBITMQ_PASSWORD=guest
```

**⚠️ Salvar e Fechar o Notepad**

---

### Passo 6: Obter Credenciais do Banco de Dados

**Opção A: Perguntar ao Administrador**

Entre em contato com o administrador do servidor e solicite:
- Usuário MySQL: `smartceu_user`
- Senha MySQL: `************`
- Confirme que seu IP está liberado no firewall

**Opção B: Acessar via SSH** (se tiver acesso)

```bash
# Conectar ao servidor
ssh usuario@82.25.75.88

# Ver configuração MySQL
sudo cat /etc/mysql/mysql.conf.d/mysqld.cnf | grep bind-address

# Se bind-address = 127.0.0.1, precisa alterar para 0.0.0.0
# sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
# bind-address = 0.0.0.0

# Criar usuário remoto (se necessário)
sudo mysql -u root -p

# No MySQL:
CREATE USER 'smartceu_user'@'%' IDENTIFIED BY 'sua_senha_segura';
GRANT ALL PRIVILEGES ON smartceu_db.* TO 'smartceu_user'@'%';
FLUSH PRIVILEGES;
EXIT;

# Reiniciar MySQL
sudo systemctl restart mysql

# Liberar porta no firewall
sudo ufw allow 3306/tcp
```

---

## 📦 Instalação das Dependências

### Passo 7: Instalar Dependências Python

```powershell
# Certifique-se de que o venv está ativado
# Você deve ver (venv) no início da linha

# Atualizar pip
python -m pip install --upgrade pip

# Instalar dependências da Fase 3 (Backend Flask)
pip install -r requirements-phase3.txt

# Instalar cryptography (necessário para autenticação MySQL moderna)
pip install cryptography

# Verificar instalação
pip list
```

**Pacotes Principais que serão instalados:**
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-JWT-Extended 4.5.3
- PyMySQL 1.1.0
- Marshmallow 3.20.1
- paho-mqtt 1.6.1
- cryptography (para autenticação MySQL moderna)

**⚠️ Possíveis Erros:**

**Erro: Microsoft C++ Build Tools**
```
Se aparecer erro sobre compilação C++, é porque alguns pacotes precisam compilar.
Solução: O requirements-phase3.txt já usa PyMySQL que não precisa compilar.
Se ainda assim aparecer erro, instale manualmente:
pip install PyMySQL Flask Flask-SQLAlchemy Flask-JWT-Extended marshmallow
```

**Erro: Timeout na instalação**
```powershell
# Aumentar timeout
pip install -r requirements-phase3.txt --timeout=300
```

---

### Passo 8: Verificar Dependências Instaladas

```powershell
# Listar pacotes instalados
pip list

# Verificar versões específicas
pip show Flask
pip show PyMySQL
pip show Flask-SQLAlchemy

# Verificar se há conflitos
pip check
```

---

## ⚙️ Configuração da Aplicação

### Passo 9: Testar Conexão com o Banco de Dados

Crie um script de teste:

```powershell
# Criar arquivo de teste
notepad test_db_connection.py
```

**Conteúdo do `test_db_connection.py`:**

```python
"""
Teste de Conexão com o Banco de Dados Remoto
"""
import pymysql
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

print("=" * 50)
print("TESTE DE CONEXÃO COM BANCO DE DADOS REMOTO")
print("=" * 50)

# Configurações do banco
config = {
    'host': os.getenv('DB_HOST', '82.25.75.88'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'smartceu_user'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME', 'smartceu_db'),
    'charset': 'utf8mb4',
    'connect_timeout': 10
}

print(f"\nConfigurações:")
print(f"  Host: {config['host']}")
print(f"  Port: {config['port']}")
print(f"  User: {config['user']}")
print(f"  Database: {config['database']}")
print(f"  Password: {'*' * len(config['password']) if config['password'] else 'NÃO CONFIGURADA'}")

if not config['password']:
    print("\n❌ ERRO: Senha do banco não está configurada no .env")
    exit(1)

print("\n🔄 Tentando conectar...")

try:
    # Tentar conectar
    connection = pymysql.connect(**config)
    print("✅ Conexão estabelecida com sucesso!")
    
    # Testar query
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"\n📊 Versão do MySQL: {version[0]}")
        
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"\n📋 Tabelas no banco ({len(tables)}):")
        for table in tables:
            print(f"  - {table[0]}")
            
        # Contar registros
        cursor.execute("SELECT COUNT(*) FROM sensors")
        sensors_count = cursor.fetchone()[0]
        print(f"\n📡 Sensores cadastrados: {sensors_count}")
        
        cursor.execute("SELECT COUNT(*) FROM readings")
        readings_count = cursor.fetchone()[0]
        print(f"📊 Leituras registradas: {readings_count}")
        
        cursor.execute("SELECT COUNT(*) FROM pool_readings")
        pool_count = cursor.fetchone()[0]
        print(f"🏊 Leituras de piscina: {pool_count}")
    
    connection.close()
    print("\n✅ TESTE CONCLUÍDO COM SUCESSO!")
    print("=" * 50)

except pymysql.err.OperationalError as e:
    print(f"\n❌ ERRO DE CONEXÃO: {e}")
    print("\n💡 Possíveis causas:")
    print("  1. Firewall bloqueando porta 3306")
    print("  2. Senha incorreta no arquivo .env")
    print("  3. Usuário não tem permissão remota")
    print("  4. MySQL não está aceitando conexões remotas")
    print("\n🔧 Soluções:")
    print("  - Verifique a senha no arquivo .env")
    print("  - Solicite liberação do seu IP no servidor")
    print("  - Use túnel SSH como alternativa")
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")

print("\n" + "=" * 50)
```

**Executar o teste:**

```powershell
# Executar teste
python test_db_connection.py
```

**Resultados Esperados:**

✅ **Sucesso:**
```
✅ Conexão estabelecida com sucesso!
📊 Versão do MySQL: 8.0.43
📋 Tabelas no banco (5):
  - sensors
  - readings
  - pool_readings
  - users
  - alerts
📡 Sensores cadastrados: 6
📊 Leituras registradas: 6026
🏊 Leituras de piscina: 150
```

❌ **Falha:** Ver seção [Troubleshooting](#troubleshooting)

---

### Passo 10: Configurar Estrutura de Logs

```powershell
# Criar diretório de logs
New-Item -ItemType Directory -Path "logs" -Force

# Criar arquivo de log vazio
New-Item -ItemType File -Path "logs\backend_local.log" -Force
```

---

## 🚀 Execução da Aplicação

### Passo 11: Inicializar o Banco de Dados (se necessário)

**⚠️ ATENÇÃO:** Como estamos usando o banco remoto que já está populado, **NÃO execute** `flask db init` ou `flask db migrate`, pois isso pode sobrescrever dados.

Apenas verifique se as tabelas existem (já fizemos no Passo 9).

---

### Passo 12: Iniciar o Servidor Flask

```powershell
# Certifique-se de estar em app\backend com venv ativado
cd c:\DRP14-PJI410-SALA-004-GRUPO-05\app\backend

# Verificar se venv está ativado (deve aparecer (venv))
# Se não estiver, ativar:
.\venv\Scripts\Activate.ps1

# Iniciar servidor Flask
python app.py
```

**Saída Esperada:**

```
==================================================
CEU Tres Pontes Backend iniciado
Ambiente: development
Debug: True
==================================================
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://0.0.0.0:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 123-456-789
```

**🎉 SUCESSO! A aplicação está rodando!**

---

### Passo 13: Verificar Acesso à Aplicação

**Abrir em outro Terminal ou Navegador:**

```powershell
# Em outro PowerShell (sem fechar o servidor)
# Testar health check
curl http://localhost:5000/health

# Ou abrir no navegador:
# http://localhost:5000/health
```

**Resposta Esperada:**

```json
{
  "status": "healthy",
  "timestamp": "2025-10-27T10:30:00",
  "version": "1.0.0"
}
```

---

## ✅ Testes e Verificação

### Passo 14: Testar Endpoints da API

#### **A. Teste de Health Check**

```powershell
# Health básico
curl http://localhost:5000/health

# Health detalhado
curl http://localhost:5000/health/detailed
```

#### **B. Teste de Autenticação**

```powershell
# Login (usuário padrão)
$body = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:5000/api/v1/auth/login" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

# Guardar token
$token = $response.access_token
Write-Host "Token: $token"
```

#### **C. Teste de Sensores**

```powershell
# Listar sensores
$headers = @{
    "Authorization" = "Bearer $token"
}

Invoke-RestMethod -Uri "http://localhost:5000/api/v1/sensors" `
    -Method GET `
    -Headers $headers
```

#### **D. Teste de Leituras**

```powershell
# Leituras recentes
Invoke-RestMethod -Uri "http://localhost:5000/api/v1/readings/recent?limit=10" `
    -Method GET `
    -Headers $headers
```

#### **E. Teste de Estatísticas**

```powershell
# Overview do sistema
Invoke-RestMethod -Uri "http://localhost:5000/api/v1/statistics/overview" `
    -Method GET `
    -Headers $headers
```

#### **F. Teste de Piscina**

```powershell
# Últimas leituras da piscina
Invoke-RestMethod -Uri "http://localhost:5000/api/v1/pool/latest" `
    -Method GET `
    -Headers $headers
```

---

### Passo 15: Acessar Interface Web

**Opção A: Servir Frontend Localmente**

```powershell
# Em outro terminal, navegar para frontend
cd c:\DRP14-PJI410-SALA-004-GRUPO-05\app\frontend

# Iniciar servidor HTTP simples
python -m http.server 8080

# Acessar no navegador:
# http://localhost:8080/smart_ceu.html
# http://localhost:8080/test_page.html
# http://localhost:8080/monitoramento_piscina.html
```

**Opção B: Abrir diretamente os arquivos HTML**

```powershell
# Abrir com navegador padrão
start chrome "c:\DRP14-PJI410-SALA-004-GRUPO-05\app\frontend\smart_ceu.html"
# ou
start firefox "c:\DRP14-PJI410-SALA-004-GRUPO-05\app\frontend\smart_ceu.html"
```

**⚠️ Ajustar URLs no frontend:**

Os arquivos HTML apontam para o servidor remoto. Para testar localmente, edite os arquivos:

```javascript
// Procurar por:
const API_URL = 'http://82.25.75.88/smartceu/api/v1';

// Alterar para:
const API_URL = 'http://localhost:5000/api/v1';
```

---

### Passo 16: Testar com Postman (Opcional)

**Importar Collection:**

1. Abrir Postman
2. File → Import
3. Criar nova collection "SmartCEU Local"
4. Adicionar requests:

**Login:**
```
POST http://localhost:5000/api/v1/auth/login
Body (JSON):
{
    "username": "admin",
    "password": "admin123"
}
```

**Copiar `access_token` da resposta**

**Listar Sensores:**
```
GET http://localhost:5000/api/v1/sensors
Headers:
Authorization: Bearer SEU_TOKEN_AQUI
```

**Collection completa em:** `docs/postman/SmartCEU.postman_collection.json` (se existir)

---

## 🐛 Troubleshooting

### Problema 1: Erro de autenticação MySQL (cryptography)

**Erro:** `'cryptography' package is required for sha256_password or caching_sha2_password auth methods`

**Causa:** O MySQL 8.0+ usa métodos de autenticação modernos que requerem o pacote `cryptography`.

**Solução:**

```powershell
# Com venv ativado, instalar cryptography
pip install cryptography

# Ou reinstalar PyMySQL com suporte a criptografia
pip install PyMySQL[rsa]

# Verificar instalação
pip show cryptography

# Executar novamente o teste
python test_db_connection.py
```

---

### Problema 2: Não consigo conectar ao banco remoto

**Erro:** `OperationalError: (2003, "Can't connect to MySQL server on '82.25.75.88'")`

**Soluções:**

```powershell
# 1. Verificar conectividade
Test-NetConnection -ComputerName 82.25.75.88 -Port 3306

# 2. Se falhar, usar túnel SSH
ssh -L 3306:localhost:3306 usuario@82.25.75.88

# 3. Alterar .env para usar localhost
# DB_HOST=localhost
```

---

### Problema 3: Erro de senha do banco

**Erro:** `Access denied for user 'smartceu_user'@'xxx.xxx.xxx.xxx'`

**Soluções:**

1. Verificar senha no arquivo `.env`
2. Testar senha manualmente:
```powershell
# Instalar MySQL Client (opcional)
# https://dev.mysql.com/downloads/mysql/

mysql -h 82.25.75.88 -u smartceu_user -p smartceu_db
```

3. Solicitar reset de senha ao administrador

---

### Problema 4: Porta 5000 já está em uso

**Erro:** `OSError: [WinError 10048] Only one usage of each socket address`

**Soluções:**

```powershell
# 1. Verificar processo usando a porta
netstat -ano | findstr :5000

# 2. Matar processo (substitua PID)
taskkill /PID <numero_do_pid> /F

# 3. Ou usar outra porta
# No app.py, alterar:
# app.run(host='0.0.0.0', port=5001)
```

---

### Problema 5: Módulo não encontrado

**Erro:** `ModuleNotFoundError: No module named 'flask'`

**Soluções:**

```powershell
# 1. Verificar se venv está ativado
# Deve aparecer (venv) no prompt

# 2. Se não estiver, ativar
.\venv\Scripts\Activate.ps1

# 3. Reinstalar dependências
pip install -r requirements-phase3.txt

# 4. Verificar que está usando o Python do venv
Get-Command python
# Deve mostrar caminho em ...\venv\Scripts\python.exe
```

---

### Problema 6: Erro de CORS no frontend

**Erro:** `Access to fetch at 'http://localhost:5000/api/v1/...' from origin 'null' has been blocked by CORS policy`

**Soluções:**

1. Verificar se CORS está habilitado no backend (já está em `app/__init__.py`)

2. Servir frontend via HTTP server (não abrir arquivo direto):
```powershell
cd app\frontend
python -m http.server 8080
# Acessar http://localhost:8080/test_page.html
```

3. Usar extensão de browser para desabilitar CORS (desenvolvimento apenas)

---

### Problema 7: Erro de SQL ou Migration

**Erro:** `sqlalchemy.exc.OperationalError: (1146, "Table 'smartceu_db.xxx' doesn't exist")`

**Causa:** Banco remoto pode estar desatualizado ou tabela não existe

**Soluções:**

```powershell
# NÃO executar migrations no banco remoto!
# Apenas verificar estrutura

# Executar script de verificação
python test_db_connection.py

# Se tabela realmente não existir, solicitar ao admin criar
```

---

### Problema 8: Token JWT expirado

**Erro:** `{"msg": "Token has expired"}`

**Solução:**

Fazer login novamente:

```powershell
# Gerar novo token
$body = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:5000/api/v1/auth/login" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

$token = $response.access_token
```

---

## 📝 Comandos Úteis

### Gerenciar Ambiente Virtual

```powershell
# Ativar venv
.\venv\Scripts\Activate.ps1

# Desativar venv
deactivate

# Recriar venv (se corrompido)
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements-phase3.txt
```

---

### Gerenciar Servidor Flask

```powershell
# Iniciar servidor
python app.py

# Iniciar com porta específica
# Editar app.py: app.run(host='0.0.0.0', port=5001)

# Parar servidor
# Pressionar CTRL+C no terminal

# Reiniciar (após mudanças no código)
# Com debug=True, reinicia automaticamente
# Ou CTRL+C e executar python app.py novamente
```

---

### Testar API via PowerShell

```powershell
# GET simples
Invoke-RestMethod -Uri "http://localhost:5000/health"

# POST com JSON
$body = @{ username = "admin"; password = "admin123" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/api/v1/auth/login" `
    -Method POST -Body $body -ContentType "application/json"

# GET com Authorization Header
$headers = @{ Authorization = "Bearer $token" }
Invoke-RestMethod -Uri "http://localhost:5000/api/v1/sensors" `
    -Headers $headers
```

---

### Ver Logs

```powershell
# Logs do Flask (console)
# Aparecem no terminal onde rodou python app.py

# Logs em arquivo
Get-Content logs\backend_local.log -Tail 50 -Wait

# Limpar logs
Clear-Content logs\backend_local.log
```

---

### Atualizar Código do GitHub

```powershell
# Parar servidor (CTRL+C)

# Atualizar código
git pull origin main

# Reinstalar dependências (se houve mudanças)
pip install -r requirements-phase3.txt

# Reiniciar servidor
python app.py
```

---

### Backup do Código Local

```powershell
# Criar backup
$date = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = "c:\Backups\SmartCEU_$date"
Copy-Item -Path "c:\DRP14-PJI410-SALA-004-GRUPO-05" `
    -Destination $backupDir -Recurse

Write-Host "Backup criado em: $backupDir"
```

---

## 🎓 Próximos Passos

Após ter a aplicação rodando localmente:

### Para Desenvolvimento:

1. **Criar branch para suas mudanças:**
```powershell
git checkout -b feature/minha-feature
```

2. **Fazer suas modificações**

3. **Testar localmente**

4. **Commit e push:**
```powershell
git add .
git commit -m "Descrição das mudanças"
git push origin feature/minha-feature
```

5. **Criar Pull Request no GitHub**

---

### Para Testar Gateway MQTT (Opcional):

```powershell
# 1. Instalar Mosquitto no Windows
# Download: https://mosquitto.org/download/

# 2. Iniciar Mosquitto
# Serviço já inicia automaticamente após instalação

# 3. Testar publicação
mosquitto_pub -h localhost -t "ceu/tres_pontes/test" -m "teste"

# 4. Testar subscrição
mosquitto_sub -h localhost -t "ceu/tres_pontes/#" -v

# 5. Executar Gateway
cd c:\DRP14-PJI410-SALA-004-GRUPO-05\app\backend
python gateway\gateway.py
```

---

### Para Executar Simuladores de Sensores:

```powershell
# Navegar para pasta de sensores
cd c:\DRP14-PJI410-SALA-004-GRUPO-05\app\sensores

# Executar simulador LoRa
python lora_sensor.py

# Executar todos juntos (em terminais separados)
# Terminal 1: python lora_sensor.py
# Terminal 2: python zigbee_sensor.py
# Terminal 3: python sigfox_sensor.py
# Terminal 4: python rfid_sensor.py
```

---

## 📊 Verificação Final

Execute este checklist para confirmar que tudo está funcionando:

- [ ] Python 3.12+ instalado e no PATH
- [ ] Repositório clonado e atualizado
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas sem erros
- [ ] Arquivo `.env` criado e configurado
- [ ] Conexão com banco remoto testada e funcionando
- [ ] Servidor Flask iniciado sem erros
- [ ] Health check retorna `{"status": "healthy"}`
- [ ] Login funciona e retorna token
- [ ] Endpoints de sensores, leituras e estatísticas funcionam
- [ ] Frontend carrega corretamente
- [ ] Logs sendo gerados em `logs/backend_local.log`

---

## 🎯 Resumo Rápido (TL;DR)

Para quem já tem experiência, o resumo:

```powershell
# 1. Clonar/Atualizar
cd c:\DRP14-PJI410-SALA-004-GRUPO-05
git pull origin main

# 2. Criar venv
cd app\backend
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Instalar dependências
pip install -r requirements-phase3.txt

# 4. Configurar .env
# Criar .env com credenciais do banco remoto
# DB_HOST=82.25.75.88
# DB_USER=ceu_tres_pontes
# DB_PASSWORD=sua_senha

# 5. Testar conexão
python test_db_connection.py

# 6. Iniciar servidor
python app.py

# 7. Testar
curl http://localhost:5000/health

# 8. Acessar frontend
cd ..\frontend
python -m http.server 8080
# http://localhost:8080/smart_ceu.html
```

---

## 📞 Suporte

### Em caso de problemas:

1. **Verificar logs:**
```powershell
Get-Content logs\backend_local.log -Tail 100
```

2. **Verificar issues do GitHub:**
https://github.com/RogerioVieira77/DRP14-PJI410-SALA-004-GRUPO-05/issues

3. **Consultar documentação completa:**
- `README.md` - Visão geral do projeto
- `app/README.md` - Documentação da aplicação
- `docs/` - Documentação técnica detalhada

4. **Contatar equipe:**
- Criar issue no GitHub com detalhes do erro
- Incluir logs relevantes
- Descrever passos para reproduzir o problema

---

## 📝 Notas Importantes

### ⚠️ Segurança

- **NÃO** commite o arquivo `.env` no Git
- **NÃO** compartilhe credenciais do banco publicamente
- Use senhas fortes em produção
- Token JWT expira em 24 horas

### 💡 Boas Práticas

- Sempre ative o ambiente virtual antes de trabalhar
- Mantenha o código atualizado (`git pull`)
- Teste localmente antes de fazer push
- Documente suas mudanças nos commits

### 🔒 Banco de Dados

- **NÃO** execute migrations no banco remoto
- **NÃO** delete ou altere dados sem backup
- Use apenas SELECT em produção
- Para testes destrutivos, use banco local

---

## 📈 Performance Local

Para melhor performance em desenvolvimento:

```python
# No .env, ajustar:
SQLALCHEMY_ECHO=False  # Desabilitar log SQL no console
SQLALCHEMY_POOL_SIZE=5  # Reduzir pool para economizar conexões
LOG_LEVEL=INFO  # Menos logs no console
```

---

## 🎉 Conclusão

Seguindo este guia, você terá:

✅ Ambiente de desenvolvimento local configurado  
✅ Aplicação rodando conectada ao banco remoto  
✅ Todos os endpoints da API funcionando  
✅ Frontend acessível para testes  
✅ Ferramentas de debug e troubleshooting  

**Bom desenvolvimento! 🚀**

---

**Documento criado em:** 27 de Outubro de 2025  
**Versão:** 1.0  
**Projeto:** SmartCEU - Sistema de Controle de Acesso CEU Três Pontes  
**Desenvolvido por:** UNIVESP - DRP14-PJI410-SALA-004-GRUPO-05

---

## 📄 Licença

Este documento faz parte do projeto SmartCEU e está sob a mesma licença do projeto.

---

**Última atualização:** 27/10/2025
