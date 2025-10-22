# 📋 Configuração Específica do Servidor
## Informações Coletadas - SmartCEU Deploy

**Data da Análise:** 22 de Outubro de 2025  
**Servidor:** srv728514 @ Hostinger  
**IP:** 82.25.75.88

---

## 🖥️ Especificações do Servidor

### Sistema Operacional
```
Distribuição: Ubuntu 24.04.2 LTS (Noble)
Kernel: 6.8.0-58-generic
Arquitetura: x86_64
```

### Recursos Disponíveis
| Recurso | Total | Usado | Disponível | Status |
|---------|-------|-------|------------|--------|
| **vCPU** | 2 cores | - | 2 cores | ✅ Suficiente |
| **RAM** | 7.8 GB | 1.0 GB | 6.8 GB | ✅ Excelente |
| **Disco** | 96 GB | 5.4 GB | 91 GB | ✅ Ótimo |

---

## 🔌 Aplicação Existente

### Agasalho Aqui (Flask Application)

**Detalhes:**
- **Localização:** `/var/www/agasalho_aqui/`
- **Porta:** 8000 (127.0.0.1:8000)
- **Servidor:** Gunicorn (3 workers)
- **Gerenciamento:** Supervisor
- **Web Server:** NGINX (proxy reverso)
- **Usuário:** www-data

**Processos:**
```
PID 636735 - Master Gunicorn
PID 636738 - Worker 1
PID 636739 - Worker 2  
PID 636740 - Worker 3
```

**Configuração NGINX:**
```
Site ativo: /etc/nginx/sites-enabled/agasalho_aqui
Config: /etc/nginx/sites-available/agasalho_aqui
```

---

## 🗄️ Banco de Dados

### MySQL Existente

**Status:** ✅ Ativo e Operacional

```
Versão: MySQL 8.0.43 (Ubuntu)
Porta: 3306 (127.0.0.1:3306)
Porta X Protocol: 33060 (127.0.0.1:33060)
Service: mysql.service (enabled)
Status: Active (running) desde 01/10/2025
```

**Decisão:** Compartilhar MySQL entre aplicações
- ✅ Criar database separado: `smartceu_db`
- ✅ Criar usuário dedicado: `smartceu_user`
- ✅ Permissões isoladas por database

---

## 🔌 Portas em Uso vs Disponíveis

### Portas Ocupadas

| Porta | Serviço | Bind Address | Aplicação |
|-------|---------|--------------|-----------|
| 22 | SSH | 0.0.0.0 | systemd |
| 53 | DNS | 127.0.0.53/54 | systemd-resolved |
| 80 | HTTP | 0.0.0.0 | NGINX |
| 3306 | MySQL | 127.0.0.1 | mysqld |
| 8000 | Flask | 127.0.0.1 | Gunicorn (Agasalho Aqui) |
| 33060 | MySQL X | 127.0.0.1 | mysqld |
| 65529 | Monarx | 127.0.0.1 | monarx-agent |

### Portas para SmartCEU

| Serviço | Porta | Status |
|---------|-------|--------|
| **Frontend** (HTTP Server) | 8001 | ✅ Livre |
| **Backend** (Flask API) | 5001 | ✅ Livre |
| **MQTT** (Mosquitto) | 1884 | ✅ Livre |
| **MySQL** | 3306 | ✅ Compartilhado |

---

## 📂 Estrutura de Diretórios para SmartCEU

### Localização Proposta

```
/var/www/smartceu/
├── app/                        # Código do projeto (clone GitHub)
│   ├── backend/
│   ├── frontend/
│   ├── sensores/
│   └── ...
├── venv/                       # Ambiente virtual Python
├── logs/                       # Logs da aplicação
├── backups/                    # Backups do banco
└── config/                     # Configs locais

/etc/nginx/sites-available/
└── smartceu                    # Config NGINX

/etc/systemd/system/
├── smartceu-api.service        # Serviço Flask API
└── smartceu-simulators.service # Serviço simuladores (opcional)
```

**Motivo:** Seguir o mesmo padrão de `/var/www/agasalho_aqui/`

---

## 👤 Usuário e Permissões

### Estratégia de Isolamento

**Opção 1: Usar usuário www-data (Recomendado)**
- ✅ Mesmo usuário da aplicação existente
- ✅ NGINX já tem permissões
- ✅ Supervisor já configurado
- ⚠️ Menos isolamento entre apps

**Opção 2: Criar usuário smartceu**
- ✅ Isolamento total
- ✅ Permissões dedicadas
- ⚠️ Requer ajustes no NGINX
- ⚠️ Mais configuração

**DECISÃO:** Usar **www-data** com diretórios separados em `/var/www/`

---

## 🔒 Configuração de Segurança

### Firewall (UFW) - Não Ativo

```bash
# Verificar status
sudo ufw status
# Status: inactive

# Não precisa mexer - servidor gerenciado pela Hostinger
```

### Fail2Ban - Verificar

```bash
# Verificar se está instalado
sudo systemctl status fail2ban

# Se não estiver, instalar é opcional (Hostinger pode ter proteção própria)
```

### Monarx Agent

**Detectado:** Porta 65529
- Serviço de segurança/monitoramento
- **Ação:** Manter ativo, não interferir

---

## 🚀 Plano de Deploy Específico

### Fase 1: Preparação (5 min)

```bash
# 1. Criar estrutura de diretórios
sudo mkdir -p /var/www/smartceu/{app,venv,logs,backups,config}
sudo chown -R www-data:www-data /var/www/smartceu
sudo chmod 755 /var/www/smartceu

# 2. Criar ambiente virtual
cd /var/www/smartceu
sudo -u www-data python3 -m venv venv
```

### Fase 2: MySQL (5 min)

```bash
# Criar database e usuário
sudo mysql -u root -p << 'EOF'
CREATE DATABASE smartceu_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'smartceu_user'@'localhost' IDENTIFIED BY 'SmartCEU2025!Secure';
GRANT ALL PRIVILEGES ON smartceu_db.* TO 'smartceu_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
EOF
```

### Fase 3: Mosquitto MQTT (5 min)

```bash
# Instalar
sudo apt update
sudo apt install -y mosquitto mosquitto-clients

# Configurar porta 1884
sudo tee -a /etc/mosquitto/mosquitto.conf > /dev/null << 'EOF'

# SmartCEU Configuration
listener 1884
protocol mqtt
allow_anonymous true
log_dest file /var/log/mosquitto/mosquitto.log
log_type all
persistence true
persistence_location /var/lib/mosquitto/
EOF

# Reiniciar
sudo systemctl restart mosquitto
sudo systemctl enable mosquitto
```

### Fase 4: Clone do Projeto (2 min)

```bash
cd /var/www/smartceu
sudo -u www-data git clone https://github.com/RogerioVieira77/PI---IV---V1.git app
```

### Fase 5: Dependências Python (3 min)

```bash
cd /var/www/smartceu
sudo -u www-data venv/bin/pip install --upgrade pip
sudo -u www-data venv/bin/pip install -r app/requirements.txt
sudo -u www-data venv/bin/pip install -r app/backend/requirements-phase3.txt
```

### Fase 6: Configuração .env (2 min)

```bash
cd /var/www/smartceu/app/backend
sudo -u www-data cp .env.example .env

# Editar .env
sudo -u www-data nano .env
```

**Valores .env:**
```ini
DB_HOST=localhost
DB_PORT=3306
DB_USER=smartceu_user
DB_PASSWORD=SmartCEU2025!Secure
DB_NAME=smartceu_db

API_HOST=0.0.0.0
API_PORT=5001

MQTT_BROKER_HOST=localhost
MQTT_BROKER_PORT=1884

SECRET_KEY=[gerar com: python3 -c "import secrets; print(secrets.token_hex(32))"]
JWT_SECRET_KEY=[gerar com: python3 -c "import secrets; print(secrets.token_hex(32))"]
```

### Fase 7: Criar Tabelas (2 min)

```bash
cd /var/www/smartceu/app/backend
sudo -u www-data /var/www/smartceu/venv/bin/python3 << 'EOF'
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print("✅ Tabelas criadas com sucesso!")
EOF
```

### Fase 8: NGINX Config (5 min)

```bash
# Criar config
sudo nano /etc/nginx/sites-available/smartceu
```

**Conteúdo:**
```nginx
server {
    listen 80;
    server_name smartceu.82.25.75.88.nip.io;  # ou domínio real

    access_log /var/log/nginx/smartceu_access.log;
    error_log /var/log/nginx/smartceu_error.log;

    # Frontend estático
    location / {
        root /var/www/smartceu/app/frontend;
        index smart_ceu.html index.html;
        try_files $uri $uri/ =404;
    }

    # API Backend
    location /api/ {
        proxy_pass http://127.0.0.1:5001/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /health {
        proxy_pass http://127.0.0.1:5001/health;
        access_log off;
    }

    location /assets/ {
        alias /var/www/smartceu/app/frontend/assets/;
    }
}
```

```bash
# Habilitar site
sudo ln -s /etc/nginx/sites-available/smartceu /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Fase 9: Systemd Services (5 min)

**Serviço Flask API:**
```bash
sudo nano /etc/systemd/system/smartceu-api.service
```

```ini
[Unit]
Description=SmartCEU Flask API
After=network.target mysql.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/smartceu/app/backend
Environment="PATH=/var/www/smartceu/venv/bin"
ExecStart=/var/www/smartceu/venv/bin/python3 app.py
Restart=always
RestartSec=10
StandardOutput=append:/var/www/smartceu/logs/api.log
StandardError=append:/var/www/smartceu/logs/api_error.log

[Install]
WantedBy=multi-user.target
```

```bash
# Habilitar e iniciar
sudo systemctl daemon-reload
sudo systemctl enable smartceu-api
sudo systemctl start smartceu-api
sudo systemctl status smartceu-api
```

### Fase 10: Validação (3 min)

```bash
# Testar API
curl http://localhost:5001/health

# Testar via NGINX
curl http://82.25.75.88/health

# Ver logs
tail -f /var/www/smartceu/logs/api.log
```

---

## ✅ Checklist de Deploy

### Pré-Deploy
- [x] Servidor analisado
- [x] Aplicação existente identificada (Agasalho Aqui)
- [x] Portas definidas (5001, 8001, 1884)
- [x] MySQL disponível

### Durante Deploy
- [ ] Diretórios criados (/var/www/smartceu/)
- [ ] Venv criado
- [ ] MySQL database e user criados
- [ ] Mosquitto instalado (porta 1884)
- [ ] Código clonado do GitHub
- [ ] Dependências instaladas
- [ ] .env configurado
- [ ] Tabelas criadas
- [ ] NGINX configurado
- [ ] Serviços systemd criados

### Pós-Deploy
- [ ] API respondendo (curl http://82.25.75.88/health)
- [ ] Frontend carregando
- [ ] Login funcionando
- [ ] Dashboard atualizando
- [ ] Pool monitoring OK
- [ ] MQTT conectando
- [ ] Logs sendo escritos
- [ ] Backup configurado

---

## 🔧 Comandos Úteis

### Gerenciar SmartCEU
```bash
# Ver status
sudo systemctl status smartceu-api

# Reiniciar
sudo systemctl restart smartceu-api

# Ver logs em tempo real
tail -f /var/www/smartceu/logs/api.log
sudo journalctl -u smartceu-api -f

# Testar API localmente
curl http://localhost:5001/health
```

### Gerenciar NGINX
```bash
# Testar config
sudo nginx -t

# Recarregar
sudo systemctl reload nginx

# Ver logs
tail -f /var/log/nginx/smartceu_access.log
tail -f /var/log/nginx/smartceu_error.log
```

### Gerenciar MySQL
```bash
# Conectar
mysql -u smartceu_user -p smartceu_db

# Ver databases
mysql -u smartceu_user -p -e "SHOW DATABASES;"

# Backup
mysqldump -u smartceu_user -p smartceu_db | gzip > /var/www/smartceu/backups/backup_$(date +%Y%m%d).sql.gz
```

---

## 🌐 Acessos

### Após Deploy

**SmartCEU:**
- Frontend: http://82.25.75.88/ (ou http://smartceu.82.25.75.88.nip.io/)
- Pool Monitoring: http://82.25.75.88/monitoramento_piscina.html
- API Health: http://82.25.75.88/health
- API Docs: http://82.25.75.88/api/docs

**Agasalho Aqui (existente):**
- Continua funcionando normalmente na porta 80

---

## 📊 Estimativa de Tempo Total

| Fase | Tempo | Acumulado |
|------|-------|-----------|
| Preparação | 5 min | 5 min |
| MySQL | 5 min | 10 min |
| Mosquitto | 5 min | 15 min |
| Clone | 2 min | 17 min |
| Dependências | 3 min | 20 min |
| .env Config | 2 min | 22 min |
| Tabelas | 2 min | 24 min |
| NGINX | 5 min | 29 min |
| Systemd | 5 min | 34 min |
| Validação | 3 min | 37 min |

**TOTAL:** ~40 minutos (deploy manual completo)

---

## ⚠️ Avisos Importantes

1. **Não mexer em:**
   - Configuração do Agasalho Aqui (`/var/www/agasalho_aqui/`)
   - NGINX config existente (`/etc/nginx/sites-enabled/agasalho_aqui`)
   - MySQL databases existentes
   - Supervisor do Agasalho Aqui

2. **Testar primeiro:**
   - Fazer backup do MySQL antes de criar novas tabelas
   - Testar NGINX config antes de reload (`sudo nginx -t`)
   - Verificar portas antes de iniciar serviços

3. **Monitorar:**
   - Uso de RAM (atualmente 1GB/7.8GB)
   - Uso de disco (atualmente 5.4GB/96GB)
   - Logs de ambas aplicações

---

**Pronto para Deploy!** 🚀

Todas as informações necessárias foram coletadas e documentadas. O servidor está apto para receber o SmartCEU sem conflitos com a aplicação existente.
