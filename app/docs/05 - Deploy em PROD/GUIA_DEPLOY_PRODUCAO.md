# 🚀 Guia Completo de Deploy em Produção
## SmartCEU - Sistema IoT de Monitoramento Inteligente

**Servidor:** Ubuntu 24.04 (Hostinger)  
**IP Público:** http://82.25.75.88/  
**Repositório:** https://github.com/RogerioVieira77/PI---IV---V1.git  
**Data:** Outubro 2025

---

## ⚠️ INFORMAÇÕES IMPORTANTES

### Ambiente de Produção
- **Servidor Virtual:** Hostinger
- **Sistema Operacional:** Ubuntu 24.04 LTS
- **Isolamento:** Aplicação isolada de outras no servidor
- **Repositório:** GitHub (sincronizado)

### ⚠️ ANTES DE COMEÇAR - INFORMAÇÕES NECESSÁRIAS

Complete as informações abaixo antes de prosseguir:

```
[ ] Acesso SSH configurado (usuário: __________, senha/chave: ________)
[ ] Aplicação existente identificada (porta: ________)
[ ] MySQL existente? (Sim/Não: ________)
[ ] Domínio personalizado? (URL: ________ ou usar IP)
[ ] SSL/HTTPS necessário? (Sim/Não: ________)
[ ] Recursos do servidor (vCPU: ____, RAM: ____ GB, Disco: ____ GB)
```

### Portas que Usaremos
```
Frontend:     8001  (ao invés de 8000)
Flask API:    5001  (ao invés de 5000)
MQTT Broker:  1884  (ao invés de 1883)
MySQL:        3306  (padrão, ou outra se MySQL já existe)
```

---

## 📋 Índice

1. [Pré-requisitos](#1-pré-requisitos)
2. [Preparação do Ambiente](#2-preparação-do-ambiente)
3. [Configuração do Usuário e Diretórios](#3-configuração-do-usuário-e-diretórios)
4. [Instalação de Dependências](#4-instalação-de-dependências)
5. [Configuração do MySQL](#5-configuração-do-mysql)
6. [Configuração do Mosquitto MQTT](#6-configuração-do-mosquitto-mqtt)
7. [Clone e Configuração do Projeto](#7-clone-e-configuração-do-projeto)
8. [Configuração do Backend Flask](#8-configuração-do-backend-flask)
9. [Configuração do Frontend](#9-configuração-do-frontend)
10. [Configuração do NGINX](#10-configuração-do-nginx)
11. [Configuração de Serviços Systemd](#11-configuração-de-serviços-systemd)
12. [Firewall e Segurança](#12-firewall-e-segurança)
13. [SSL/HTTPS (Opcional)](#13-ssl-https-opcional)
14. [Testes e Validação](#14-testes-e-validação)
15. [Monitoramento e Logs](#15-monitoramento-e-logs)
16. [Backup e Recuperação](#16-backup-e-recuperação)
17. [Troubleshooting](#17-troubleshooting)

---

## 1. Pré-requisitos

### 1.1 Acesso ao Servidor

```bash
# Conectar via SSH
ssh usuario@82.25.75.88

# Se usar chave SSH
ssh -i ~/.ssh/sua_chave.pem usuario@82.25.75.88
```

### 1.2 Verificar Sistema

```bash
# Verificar versão do Ubuntu
lsb_release -a
# Deve mostrar: Ubuntu 24.04 LTS

# Verificar recursos
free -h          # Memória
df -h            # Disco
nproc            # CPUs
```

### 1.3 Atualizar Sistema

```bash
# Atualizar lista de pacotes
sudo apt update

# Atualizar pacotes instalados
sudo apt upgrade -y

# Instalar ferramentas essenciais
sudo apt install -y git curl wget vim htop net-tools build-essential
```

---

## 2. Preparação do Ambiente

### 2.1 Verificar Aplicação Existente

```bash
# Verificar portas em uso
sudo netstat -tulpn | grep LISTEN

# Ou usar ss
sudo ss -tulpn | grep LISTEN

# Verificar serviços rodando
sudo systemctl list-units --type=service --state=running
```

**📝 ANOTAR:** Quais portas estão em uso e quais serviços existem.

### 2.2 Criar Usuário Dedicado (Recomendado)

```bash
# Criar usuário para a aplicação
sudo useradd -m -s /bin/bash smartceu

# Definir senha
sudo passwd smartceu

# Adicionar ao grupo sudo (se necessário)
sudo usermod -aG sudo smartceu

# Mudar para o usuário
sudo su - smartceu
```

### 2.3 Criar Estrutura de Diretórios

```bash
# Como usuário smartceu
mkdir -p ~/apps/smartceu
mkdir -p ~/apps/smartceu/logs
mkdir -p ~/apps/smartceu/backups
mkdir -p ~/apps/smartceu/config

# Verificar
ls -la ~/apps/smartceu/
```

---

## 3. Configuração do Usuário e Diretórios

### 3.1 Configurar Permissões

```bash
# Garantir propriedade correta
sudo chown -R smartceu:smartceu ~/apps/smartceu

# Permissões adequadas
chmod 755 ~/apps/smartceu
chmod 750 ~/apps/smartceu/config
chmod 750 ~/apps/smartceu/logs
```

### 3.2 Configurar Variáveis de Ambiente

```bash
# Editar .bashrc
vim ~/.bashrc

# Adicionar ao final:
export SMARTCEU_HOME=~/apps/smartceu
export PATH=$SMARTCEU_HOME/venv/bin:$PATH

# Recarregar
source ~/.bashrc
```

---

## 4. Instalação de Dependências

### 4.1 Python 3.12+

```bash
# Verificar versão atual
python3 --version

# Se não for 3.12+, instalar
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3.12-dev

# Verificar
python3.12 --version
```

### 4.2 Pip

```bash
# Instalar pip
sudo apt install -y python3-pip

# Atualizar pip
python3.12 -m pip install --upgrade pip
```

### 4.3 Criar Ambiente Virtual

```bash
# Navegar para diretório
cd ~/apps/smartceu

# Criar venv
python3.12 -m venv venv

# Ativar venv
source venv/bin/activate

# Verificar
which python
# Deve mostrar: ~/apps/smartceu/venv/bin/python
```

---

## 5. Configuração do MySQL

### 5.1 Verificar MySQL Existente

```bash
# Verificar se MySQL está instalado
sudo systemctl status mysql

# Verificar versão
mysql --version
```

### 5.2 Instalar MySQL (se necessário)

```bash
# Instalar MySQL Server
sudo apt install -y mysql-server

# Iniciar serviço
sudo systemctl start mysql
sudo systemctl enable mysql

# Verificar status
sudo systemctl status mysql
```

### 5.3 Configuração Inicial de Segurança

```bash
# Executar script de segurança
sudo mysql_secure_installation

# Responder:
# - Set root password? [Y/n] Y (defina senha forte)
# - Remove anonymous users? [Y/n] Y
# - Disallow root login remotely? [Y/n] Y
# - Remove test database? [Y/n] Y
# - Reload privilege tables? [Y/n] Y
```

### 5.4 Criar Database e Usuário

```bash
# Conectar ao MySQL
sudo mysql -u root -p

# Dentro do MySQL:
```

```sql
-- Criar database
CREATE DATABASE smartceu_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Criar usuário
CREATE USER 'smartceu_user'@'localhost' IDENTIFIED BY 'SENHA_FORTE_AQUI';

-- Conceder permissões
GRANT ALL PRIVILEGES ON smartceu_db.* TO 'smartceu_user'@'localhost';

-- Aplicar mudanças
FLUSH PRIVILEGES;

-- Verificar
SHOW DATABASES;
SELECT User, Host FROM mysql.user WHERE User = 'smartceu_user';

-- Sair
EXIT;
```

### 5.5 Testar Conexão

```bash
# Testar login com novo usuário
mysql -u smartceu_user -p smartceu_db

# Dentro do MySQL:
SHOW TABLES;
EXIT;
```

### 5.6 Criar Tabelas

**⚠️ IMPORTANTE:** As tabelas serão criadas via migrations do Flask. Por enquanto, apenas garanta que o database existe.

---

## 6. Configuração do Mosquitto MQTT

### 6.1 Instalar Mosquitto

```bash
# Instalar Mosquitto e cliente
sudo apt install -y mosquitto mosquitto-clients

# Verificar versão
mosquitto -h
```

### 6.2 Configurar Porta Customizada (1884)

```bash
# Backup da config original
sudo cp /etc/mosquitto/mosquitto.conf /etc/mosquitto/mosquitto.conf.backup

# Editar configuração
sudo vim /etc/mosquitto/mosquitto.conf
```

**Adicionar no final do arquivo:**

```conf
# SmartCEU Configuration
listener 1884
protocol mqtt

# Permitir anônimos (APENAS DESENVOLVIMENTO)
# Em produção, configurar autenticação
allow_anonymous true

# Logs
log_dest file /var/log/mosquitto/mosquitto.log
log_type all
log_timestamp true

# Persistência
persistence true
persistence_location /var/lib/mosquitto/

# Limites
max_connections 100
max_queued_messages 1000
```

### 6.3 Reiniciar Mosquitto

```bash
# Reiniciar serviço
sudo systemctl restart mosquitto

# Verificar status
sudo systemctl status mosquitto

# Verificar porta
sudo netstat -tulpn | grep 1884
```

### 6.4 Testar MQTT

```bash
# Terminal 1 - Subscribe
mosquitto_sub -h localhost -p 1884 -t "test/topic" -v

# Terminal 2 - Publish
mosquitto_pub -h localhost -p 1884 -t "test/topic" -m "Hello SmartCEU"

# Deve aparecer mensagem no Terminal 1
```

### 6.5 Configurar Autenticação (PRODUÇÃO)

```bash
# Criar arquivo de senhas
sudo mosquitto_passwd -c /etc/mosquitto/passwd smartceu_mqtt

# Digite senha quando solicitado

# Editar mosquitto.conf
sudo vim /etc/mosquitto/mosquitto.conf
```

**Atualizar:**

```conf
# Desabilitar anônimos
allow_anonymous false

# Habilitar autenticação
password_file /etc/mosquitto/passwd
```

```bash
# Reiniciar
sudo systemctl restart mosquitto
```

---

## 7. Clone e Configuração do Projeto

### 7.1 Configurar SSH do GitHub (se necessário)

```bash
# Gerar chave SSH
ssh-keygen -t ed25519 -C "seu_email@example.com"

# Exibir chave pública
cat ~/.ssh/id_ed25519.pub

# Copiar e adicionar no GitHub:
# https://github.com/settings/keys
```

### 7.2 Clonar Repositório

```bash
# Navegar para diretório
cd ~/apps/smartceu

# Clonar repositório
git clone https://github.com/RogerioVieira77/PI---IV---V1.git

# Renomear/mover para diretório app
mv PI---IV---V1 app

# Ou clonar direto:
git clone https://github.com/RogerioVieira77/PI---IV---V1.git app

# Verificar
ls -la app/
```

### 7.3 Estrutura Esperada

```bash
~/apps/smartceu/
├── venv/              # Ambiente virtual
├── app/               # Código do projeto (clonado)
│   ├── backend/
│   ├── frontend/
│   ├── sensores/
│   ├── tests/
│   ├── docs/
│   └── requirements.txt
├── logs/              # Logs da aplicação
├── backups/           # Backups
└── config/            # Configs locais
```

---

## 8. Configuração do Backend Flask

### 8.1 Instalar Dependências Python

```bash
# Ativar venv
cd ~/apps/smartceu
source venv/bin/activate

# Instalar dependências
cd app
pip install -r requirements.txt
pip install -r backend/requirements-phase3.txt

# Verificar instalação
pip list | grep -i flask
pip list | grep -i sqlalchemy
```

### 8.2 Configurar Variáveis de Ambiente

```bash
# Criar arquivo .env
cd ~/apps/smartceu/app/backend
cp .env.example .env

# Editar .env
vim .env
```

**Configuração do `.env`:**

```ini
# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=smartceu_user
DB_PASSWORD=SENHA_FORTE_AQUI
DB_NAME=smartceu_db

# Flask
FLASK_APP=app.py
FLASK_ENV=production
DEBUG=False
SECRET_KEY=GERAR_CHAVE_SECRETA_AQUI
JWT_SECRET_KEY=GERAR_CHAVE_JWT_AQUI

# API
API_HOST=0.0.0.0
API_PORT=5001

# MQTT
MQTT_BROKER_HOST=localhost
MQTT_BROKER_PORT=1884
MQTT_USERNAME=smartceu_mqtt
MQTT_PASSWORD=SENHA_MQTT_AQUI

# Logging
LOG_LEVEL=INFO
LOG_FILE=/home/smartceu/apps/smartceu/logs/app.log
```

### 8.3 Gerar Chaves Secretas

```bash
# Gerar chave secreta para Flask
python3 -c "import secrets; print(secrets.token_hex(32))"

# Copiar output e colar no SECRET_KEY e JWT_SECRET_KEY
```

### 8.4 Criar Tabelas do Banco

```bash
# Ativar venv
source ~/apps/smartceu/venv/bin/activate

# Navegar para backend
cd ~/apps/smartceu/app/backend

# Executar script de inicialização (se tiver)
# Ou usar Flask-Migrate
python3 << 'EOF'
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print("Tabelas criadas com sucesso!")
EOF
```

**OU criar script SQL:**

```bash
# Conectar ao MySQL
mysql -u smartceu_user -p smartceu_db

# Executar SQL de criação de tabelas
# (Copiar do arquivo de migration ou criar)
```

### 8.5 Testar Backend Localmente

```bash
# Ativar venv
source ~/apps/smartceu/venv/bin/activate

# Testar Flask
cd ~/apps/smartceu/app/backend
python3 app.py

# Em outro terminal, testar:
curl http://localhost:5001/health

# Deve retornar: {"status": "healthy"}

# Parar com Ctrl+C
```

---

## 9. Configuração do Frontend

### 9.1 Ajustar URLs da API

```bash
# Editar arquivos JavaScript do frontend
cd ~/apps/smartceu/app/frontend

# Encontrar arquivos com URLs da API
grep -r "localhost:5000" .

# Editar cada arquivo encontrado
# Substituir http://localhost:5000 por http://82.25.75.88:5001
# Ou se tiver domínio: https://seudominio.com/api
```

**Exemplo em `smart_ceu.html` ou arquivo JS:**

```javascript
// ANTES
const API_URL = 'http://localhost:5000/api/v1';

// DEPOIS (IP direto)
const API_URL = 'http://82.25.75.88:5001/api/v1';

// OU (domínio + proxy)
const API_URL = '/api/v1';  // NGINX fará proxy
```

### 9.2 Verificar Arquivos Estáticos

```bash
# Estrutura esperada
~/apps/smartceu/app/
├── frontend/
│   ├── smart_ceu.html
│   ├── monitoramento_piscina.html
│   ├── assets/
│   │   ├── css/
│   │   └── js/
│   └── docs-web/
```

---

## 10. Configuração do NGINX

### 10.1 Instalar NGINX

```bash
# Instalar
sudo apt install -y nginx

# Verificar versão
nginx -v

# Iniciar e habilitar
sudo systemctl start nginx
sudo systemctl enable nginx

# Verificar status
sudo systemctl status nginx
```

### 10.2 Criar Configuração do Site

```bash
# Criar arquivo de configuração
sudo vim /etc/nginx/sites-available/smartceu
```

**Conteúdo do arquivo:**

```nginx
# SmartCEU - Sistema IoT
server {
    listen 80;
    server_name 82.25.75.88;  # Ou seu domínio

    # Logs
    access_log /var/log/nginx/smartceu_access.log;
    error_log /var/log/nginx/smartceu_error.log;

    # Frontend - Servir arquivos estáticos
    location / {
        root /home/smartceu/apps/smartceu/app/frontend;
        index smart_ceu.html index.html;
        try_files $uri $uri/ =404;
    }

    # API Backend - Proxy reverso para Flask
    location /api/ {
        proxy_pass http://localhost:5001/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type' always;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check
    location /health {
        proxy_pass http://localhost:5001/health;
        access_log off;
    }

    # Assets estáticos
    location /assets/ {
        alias /home/smartceu/apps/smartceu/app/frontend/assets/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Documentação
    location /docs-web/ {
        alias /home/smartceu/apps/smartceu/app/frontend/docs-web/;
    }
}
```

### 10.3 Habilitar Site

```bash
# Criar symlink
sudo ln -s /etc/nginx/sites-available/smartceu /etc/nginx/sites-enabled/

# Testar configuração
sudo nginx -t

# Se OK, recarregar NGINX
sudo systemctl reload nginx
```

### 10.4 Ajustar Permissões para NGINX

```bash
# NGINX precisa ler arquivos do usuário smartceu
# Adicionar nginx ao grupo smartceu
sudo usermod -aG smartceu www-data

# Ajustar permissões do diretório
chmod 755 /home/smartceu
chmod 755 /home/smartceu/apps
chmod 755 /home/smartceu/apps/smartceu
chmod 755 /home/smartceu/apps/smartceu/app
chmod 755 /home/smartceu/apps/smartceu/app/frontend

# Recarregar NGINX
sudo systemctl restart nginx
```

---

## 11. Configuração de Serviços Systemd

### 11.1 Serviço Flask API

```bash
# Criar arquivo de serviço
sudo vim /etc/systemd/system/smartceu-api.service
```

**Conteúdo:**

```ini
[Unit]
Description=SmartCEU Flask API
After=network.target mysql.service

[Service]
Type=simple
User=smartceu
Group=smartceu
WorkingDirectory=/home/smartceu/apps/smartceu/app/backend
Environment="PATH=/home/smartceu/apps/smartceu/venv/bin"
ExecStart=/home/smartceu/apps/smartceu/venv/bin/python3 app.py
Restart=always
RestartSec=10
StandardOutput=append:/home/smartceu/apps/smartceu/logs/api.log
StandardError=append:/home/smartceu/apps/smartceu/logs/api_error.log

[Install]
WantedBy=multi-user.target
```

### 11.2 Serviço Pool Simulators (Opcional)

```bash
# Criar arquivo de serviço
sudo vim /etc/systemd/system/smartceu-pool-simulators.service
```

**Conteúdo:**

```ini
[Unit]
Description=SmartCEU Pool Simulators
After=network.target smartceu-api.service

[Service]
Type=simple
User=smartceu
Group=smartceu
WorkingDirectory=/home/smartceu/apps/smartceu/app/backend
Environment="PATH=/home/smartceu/apps/smartceu/venv/bin"
ExecStart=/home/smartceu/apps/smartceu/venv/bin/python3 pool_simulators.py
Restart=always
RestartSec=30
StandardOutput=append:/home/smartceu/apps/smartceu/logs/simulators.log
StandardError=append:/home/smartceu/apps/smartceu/logs/simulators_error.log

[Install]
WantedBy=multi-user.target
```

### 11.3 Habilitar e Iniciar Serviços

```bash
# Recarregar systemd
sudo systemctl daemon-reload

# Habilitar serviços
sudo systemctl enable smartceu-api
sudo systemctl enable smartceu-pool-simulators  # Opcional

# Iniciar serviços
sudo systemctl start smartceu-api
sudo systemctl start smartceu-pool-simulators   # Opcional

# Verificar status
sudo systemctl status smartceu-api
sudo systemctl status smartceu-pool-simulators
```

### 11.4 Comandos Úteis de Gerenciamento

```bash
# Ver logs em tempo real
sudo journalctl -u smartceu-api -f

# Ver últimas 50 linhas
sudo journalctl -u smartceu-api -n 50

# Reiniciar serviço
sudo systemctl restart smartceu-api

# Parar serviço
sudo systemctl stop smartceu-api

# Status
sudo systemctl status smartceu-api
```

---

## 12. Firewall e Segurança

### 12.1 Configurar UFW (Uncomplicated Firewall)

```bash
# Verificar status
sudo ufw status

# Se desabilitado, habilitar
sudo ufw enable

# Permitir SSH (IMPORTANTE!)
sudo ufw allow 22/tcp

# Permitir HTTP
sudo ufw allow 80/tcp

# Permitir HTTPS (se usar SSL)
sudo ufw allow 443/tcp

# MQTT (apenas se externo precisar acessar)
# sudo ufw allow 1884/tcp

# Recarregar
sudo ufw reload

# Verificar regras
sudo ufw status numbered
```

### 12.2 Fail2Ban (Proteção contra Brute Force)

```bash
# Instalar
sudo apt install -y fail2ban

# Copiar configuração padrão
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# Editar
sudo vim /etc/fail2ban/jail.local
```

**Configuração básica em `jail.local`:**

```ini
[DEFAULT]
bantime = 1h
findtime = 10m
maxretry = 5

[sshd]
enabled = true
port = 22
logpath = /var/log/auth.log

[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log
```

```bash
# Habilitar e iniciar
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Verificar status
sudo fail2ban-client status
```

---

## 13. SSL/HTTPS (Opcional)

### 13.1 Usando Let's Encrypt (Certbot)

**⚠️ REQUER DOMÍNIO PRÓPRIO** (não funciona com IP)

```bash
# Instalar Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obter certificado
sudo certbot --nginx -d seudominio.com -d www.seudominio.com

# Seguir instruções interativas

# Testar renovação automática
sudo certbot renew --dry-run
```

### 13.2 Atualizar NGINX para HTTPS

Certbot faz isso automaticamente, mas se precisar editar:

```bash
sudo vim /etc/nginx/sites-available/smartceu
```

**Adicionar:**

```nginx
server {
    listen 443 ssl http2;
    server_name seudominio.com;

    ssl_certificate /etc/letsencrypt/live/seudominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seudominio.com/privkey.pem;
    
    # ... resto da configuração ...
}

# Redirecionar HTTP para HTTPS
server {
    listen 80;
    server_name seudominio.com;
    return 301 https://$server_name$request_uri;
}
```

---

## 14. Testes e Validação

### 14.1 Verificar Serviços

```bash
# MySQL
sudo systemctl status mysql

# Mosquitto
sudo systemctl status mosquitto

# Flask API
sudo systemctl status smartceu-api

# NGINX
sudo systemctl status nginx
```

### 14.2 Testar API

```bash
# Health check
curl http://82.25.75.88/health
# Esperado: {"status": "healthy"}

# Testar endpoint
curl http://82.25.75.88/api/v1/statistics/overview
# Deve retornar JSON com estatísticas
```

### 14.3 Testar Frontend

```bash
# Abrir no navegador:
http://82.25.75.88/

# Deve carregar a página smart_ceu.html

# Testar pool monitoring:
http://82.25.75.88/monitoramento_piscina.html
```

### 14.4 Testar Autenticação

```bash
# Fazer login
curl -X POST http://82.25.75.88/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Deve retornar token JWT
```

### 14.5 Testar MQTT

```bash
# Subscribe
mosquitto_sub -h localhost -p 1884 -t "ceu/tres_pontes/#" -v

# Em outro terminal, publish
mosquitto_pub -h localhost -p 1884 -t "ceu/tres_pontes/test" -m "Hello Production"
```

---

## 15. Monitoramento e Logs

### 15.1 Localização dos Logs

```bash
# Logs da aplicação
tail -f ~/apps/smartceu/logs/api.log
tail -f ~/apps/smartceu/logs/simulators.log

# Logs do sistema
sudo journalctl -u smartceu-api -f
sudo journalctl -u smartceu-pool-simulators -f

# Logs do NGINX
sudo tail -f /var/log/nginx/smartceu_access.log
sudo tail -f /var/log/nginx/smartceu_error.log

# Logs do MySQL
sudo tail -f /var/log/mysql/error.log

# Logs do Mosquitto
sudo tail -f /var/log/mosquitto/mosquitto.log
```

### 15.2 Verificar Uso de Recursos

```bash
# Uso geral
htop

# Uso de disco
df -h

# Uso de memória
free -h

# Processos da aplicação
ps aux | grep python
ps aux | grep nginx
```

### 15.3 Configurar Logrotate

```bash
# Criar configuração
sudo vim /etc/logrotate.d/smartceu
```

**Conteúdo:**

```
/home/smartceu/apps/smartceu/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0644 smartceu smartceu
    sharedscripts
    postrotate
        systemctl reload smartceu-api > /dev/null 2>&1 || true
    endscript
}
```

---

## 16. Backup e Recuperação

### 16.1 Script de Backup do Banco

```bash
# Criar script
vim ~/apps/smartceu/backup_db.sh
```

**Conteúdo:**

```bash
#!/bin/bash

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/smartceu/apps/smartceu/backups"
DB_USER="smartceu_user"
DB_PASS="SENHA_DO_BANCO"
DB_NAME="smartceu_db"

# Criar backup
mysqldump -u $DB_USER -p$DB_PASS $DB_NAME | gzip > $BACKUP_DIR/smartceu_db_$DATE.sql.gz

# Manter apenas últimos 30 dias
find $BACKUP_DIR -name "smartceu_db_*.sql.gz" -mtime +30 -delete

echo "Backup concluído: smartceu_db_$DATE.sql.gz"
```

```bash
# Tornar executável
chmod +x ~/apps/smartceu/backup_db.sh

# Testar
~/apps/smartceu/backup_db.sh
```

### 16.2 Agendar Backup com Cron

```bash
# Editar crontab
crontab -e

# Adicionar linha para backup diário às 2h da manhã
0 2 * * * /home/smartceu/apps/smartceu/backup_db.sh >> /home/smartceu/apps/smartceu/logs/backup.log 2>&1
```

### 16.3 Restaurar Backup

```bash
# Descompactar e restaurar
gunzip < /home/smartceu/apps/smartceu/backups/smartceu_db_YYYYMMDD_HHMMSS.sql.gz | mysql -u smartceu_user -p smartceu_db
```

---

## 17. Troubleshooting

### 17.1 API não inicia

```bash
# Verificar logs
sudo journalctl -u smartceu-api -n 50

# Verificar portas
sudo netstat -tulpn | grep 5001

# Testar manualmente
cd ~/apps/smartceu/app/backend
source ../../venv/bin/activate
python3 app.py
```

### 17.2 Frontend não carrega

```bash
# Verificar NGINX
sudo nginx -t
sudo systemctl status nginx

# Verificar permissões
ls -la /home/smartceu/apps/smartceu/app/frontend/

# Ver logs de erro do NGINX
sudo tail -f /var/log/nginx/smartceu_error.log
```

### 17.3 Erro de conexão com banco

```bash
# Testar conexão
mysql -u smartceu_user -p smartceu_db

# Verificar .env
cat ~/apps/smartceu/app/backend/.env | grep DB_

# Verificar MySQL rodando
sudo systemctl status mysql
```

### 17.4 MQTT não conecta

```bash
# Verificar serviço
sudo systemctl status mosquitto

# Ver logs
sudo tail -f /var/log/mosquitto/mosquitto.log

# Testar conexão
mosquitto_sub -h localhost -p 1884 -t "test" -v
```

### 17.5 Erro 502 Bad Gateway

```bash
# API provavelmente está fora do ar
sudo systemctl status smartceu-api

# Reiniciar API
sudo systemctl restart smartceu-api

# Verificar logs
sudo journalctl -u smartceu-api -n 50
```

---

## 📋 Checklist Final

Após concluir todos os passos, verificar:

### Serviços
- [ ] MySQL rodando (`sudo systemctl status mysql`)
- [ ] Mosquitto rodando (`sudo systemctl status mosquitto`)
- [ ] Flask API rodando (`sudo systemctl status smartceu-api`)
- [ ] NGINX rodando (`sudo systemctl status nginx`)
- [ ] Simulators rodando (opcional) (`sudo systemctl status smartceu-pool-simulators`)

### Conectividade
- [ ] Health check OK (`curl http://82.25.75.88/health`)
- [ ] Frontend carrega (`http://82.25.75.88/`)
- [ ] Login funciona
- [ ] Dashboard atualiza dados
- [ ] Pool monitoring funciona

### Segurança
- [ ] Firewall configurado (`sudo ufw status`)
- [ ] Fail2Ban ativo (`sudo systemctl status fail2ban`)
- [ ] Senhas fortes definidas
- [ ] SSH seguro (chave, não senha)
- [ ] SSL/HTTPS configurado (se aplicável)

### Backup
- [ ] Script de backup criado
- [ ] Backup agendado no cron
- [ ] Backup testado e funcionando

### Logs
- [ ] Logs sendo escritos corretamente
- [ ] Logrotate configurado
- [ ] Sem erros críticos nos logs

---

## 🎉 Deploy Concluído!

Se todos os itens do checklist foram verificados, o sistema está em produção e operacional!

### Acessos:

**Frontend:**
- Dashboard: http://82.25.75.88/
- Pool Monitoring: http://82.25.75.88/monitoramento_piscina.html
- Documentação: http://82.25.75.88/docs-web/

**API:**
- Health: http://82.25.75.88/health
- Swagger Docs: http://82.25.75.88/api/docs

**Credenciais Padrão:**
- Usuário: `admin`
- Senha: `admin123`

⚠️ **IMPORTANTE:** Trocar senha padrão após primeiro login!

---

## 📞 Suporte

**Logs em caso de problemas:**
```bash
sudo journalctl -u smartceu-api -n 100 > ~/problema.log
sudo tail -100 /var/log/nginx/smartceu_error.log >> ~/problema.log
```

**Comandos rápidos de diagnóstico:**
```bash
# Status geral
sudo systemctl status smartceu-api nginx mysql mosquitto

# Uso de recursos
htop

# Verificar portas
sudo netstat -tulpn | grep -E '(5001|80|1884|3306)'
```

---

**Data do Deploy:** __________  
**Responsável:** __________  
**Versão do Sistema:** 3.2.0  
**Status:** ✅ EM PRODUÇÃO
