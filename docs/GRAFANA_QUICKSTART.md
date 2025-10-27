# Grafana Dashboard - Guia Rápido
## CEU Tres Pontes - Sistema de Monitoramento

---

## 🚀 Início Rápido

### Instalação Automatizada

Execute os scripts na seguinte ordem:

```bash
# 1. Instalar Grafana
sudo bash install_grafana.sh

# 2. Configurar conexão com MySQL
sudo bash configure_grafana_datasource.sh

# 3. Configurar Nginx (proxy reverso)
sudo bash configure_grafana_nginx.sh
```

---

## 📋 Passo a Passo Manual

### 1️⃣ Instalar Grafana

```bash
# Adicionar repositório
sudo mkdir -p /etc/apt/keyrings/
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee /etc/apt/sources.list.d/grafana.list

# Instalar
sudo apt-get update
sudo apt-get install -y grafana

# Iniciar
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
```

**Acesso:** `http://SEU_IP:3000` (admin/admin)

---

### 2️⃣ Configurar MySQL

```sql
-- Conectar ao MySQL
sudo mysql -u root -p

-- Criar usuário
CREATE USER 'grafana_reader'@'localhost' IDENTIFIED BY 'sua_senha';
GRANT SELECT ON smartceu_db.* TO 'grafana_reader'@'localhost';
GRANT SELECT ON smartceu_report_db.* TO 'grafana_reader'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

### 3️⃣ Adicionar Data Source

1. Grafana → **Configuration** → **Data sources**
2. **Add data source** → **MySQL**
3. Configurar:
   - **Host:** `localhost:3306`
   - **Database:** `smartceu_db` (principal) ou `smartceu_report_db` (relatórios)
   - **User:** `grafana_reader`
   - **Password:** `[sua senha]`
4. **Save & test**

---

### 4️⃣ Criar Dashboard

1. **+** → **Dashboard** → **Add panel**
2. Selecione **MySQL Data Source**
3. Cole a query SQL (ver `docs/GRAFANA_QUERIES.md`)
4. Configure visualização
5. **Apply** → **Save dashboard**

---

## 📊 Dashboards Recomendados

### Dashboard 1: Tempo Real
- Leituras por tipo de sensor
- Total de pessoas atual
- Taxa entrada/saída
- Alertas ativos

### Dashboard 2: Piscinas
- Ocupação das piscinas
- Temperatura da água
- pH e cloro
- Turbidez

### Dashboard 3: Estatísticas
- Leituras por hora
- Média por dia da semana
- Top 10 sensores
- Comparação mensal

---

## 🌐 Publicar na Internet

### Opção A: Nginx (Recomendado)

```bash
# Criar configuração
sudo nano /etc/nginx/sites-available/grafana

# Conteúdo básico:
server {
    listen 80;
    server_name seu-dominio.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
    }
}

# Ativar
sudo ln -s /etc/nginx/sites-available/grafana /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Opção B: SSL com Let's Encrypt

```bash
# Instalar Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Obter certificado
sudo certbot --nginx -d seu-dominio.com

# Renovação automática
sudo systemctl enable certbot.timer
```

---

## 🔐 Segurança

### Criar Usuários

1. **Configuration** → **Users** → **New user**
2. Role:
   - **Viewer:** Apenas visualização ✅
   - **Editor:** Editar dashboards
   - **Admin:** Controle total

### Backup Automático

```bash
# Criar script
sudo nano /usr/local/bin/backup_grafana.sh

# Adicionar ao cron (diário às 2h)
sudo crontab -e
0 2 * * * /usr/local/bin/backup_grafana.sh
```

---

## 🛠️ Comandos Úteis

```bash
# Status
sudo systemctl status grafana-server

# Logs
sudo journalctl -u grafana-server -f
sudo tail -f /var/log/grafana/grafana.log

# Reiniciar
sudo systemctl restart grafana-server

# Verificar porta
sudo netstat -tulpn | grep 3000
```

---

## 🐛 Problemas Comuns

### Grafana não inicia
```bash
sudo chown -R grafana:grafana /var/lib/grafana
sudo systemctl restart grafana-server
```

### Erro de conexão MySQL
```sql
SHOW GRANTS FOR 'grafana_reader'@'localhost';
```

### Dashboard lento
```sql
-- Adicionar índices
CREATE INDEX idx_readings_timestamp ON readings(timestamp);
CREATE INDEX idx_pool_readings_timestamp ON pool_readings(timestamp);
```

---

## 📁 Arquivos Importantes

```
DRP14-PJI410-SALA-004-GRUPO-05/
├── install_grafana.sh                    # Script instalação
├── configure_grafana_datasource.sh       # Configurar MySQL
├── configure_grafana_nginx.sh            # Configurar Nginx
└── docs/
    ├── GRAFANA_SETUP_GUIDE.md           # Guia completo
    ├── GRAFANA_QUERIES.md               # Queries prontas
    └── GRAFANA_QUICKSTART.md            # Este arquivo
```

---

## 📚 Documentação Completa

- **Guia Completo:** `docs/GRAFANA_SETUP_GUIDE.md`
- **Queries SQL:** `docs/GRAFANA_QUERIES.md`
- **Grafana Docs:** https://grafana.com/docs/

---

## ✅ Checklist

- [ ] Grafana instalado
- [ ] Usuário MySQL criado
- [ ] Data source configurado
- [ ] Primeiro dashboard criado
- [ ] Nginx configurado
- [ ] SSL ativado
- [ ] Backup automático
- [ ] Usuários criados
- [ ] Acesso testado

---

## 🎯 Próximos Passos

1. ✅ Instale o Grafana
2. ✅ Configure o MySQL
3. ✅ Crie seu primeiro dashboard
4. ✅ Publique na internet
5. ✅ Configure alertas
6. 📊 Compartilhe com a equipe!

---

**Desenvolvido por:** UNIVESP - DRP14-PJI410-SALA-004-GRUPO-05  
**Sistema:** CEU Tres Pontes  
**Versão:** 1.0 - Outubro 2025
