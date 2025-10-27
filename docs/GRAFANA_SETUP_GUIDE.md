# Guia Completo: Implementação de Dashboards com Grafana
## Sistema CEU Tres Pontes - Monitoramento e Visualização de Dados

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Pré-requisitos](#pré-requisitos)
3. [Instalação do Grafana](#instalação-do-grafana)
4. [Configuração Inicial](#configuração-inicial)
5. [Conexão com o Banco de Dados MySQL](#conexão-com-o-banco-de-dados-mysql)
6. [Criação dos Dashboards](#criação-dos-dashboards)
7. [Publicação e Acesso via Internet](#publicação-e-acesso-via-internet)
8. [Segurança e Boas Práticas](#segurança-e-boas-práticas)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral

Este guia detalha a implementação de dashboards de visualização usando Grafana para monitorar:
- Leituras de sensores (LoRa, ZigBee, Sigfox, RFID)
- Contagem de pessoas em tempo real
- Estatísticas de acesso
- Alertas e anomalias
- Ocupação das piscinas

---

## 📦 Pré-requisitos

### Servidor
- Ubuntu Server 20.04 LTS ou superior
- Mínimo 2GB RAM
- 20GB de espaço em disco
- Acesso root ou sudo

### Software Instalado
- MySQL 8.0+ rodando
- Nginx configurado
- Sistema CEU Tres Pontes em produção

### Conhecimentos
- Comandos básicos Linux
- SQL básico
- Conceitos de firewall e portas

---

## 🚀 Instalação do Grafana

### Passo 1: Adicionar Repositório Oficial do Grafana

```bash
# Instalar dependências
sudo apt-get update
sudo apt-get install -y apt-transport-https software-properties-common wget

# Adicionar chave GPG do Grafana
sudo mkdir -p /etc/apt/keyrings/
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null

# Adicionar repositório estável do Grafana
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
```

### Passo 2: Instalar o Grafana

```bash
# Atualizar lista de pacotes
sudo apt-get update

# Instalar Grafana OSS (Open Source)
sudo apt-get install -y grafana

# Verificar instalação
grafana-server -v
```

**Saída esperada:** `Version X.X.X (commit: xxxxx, branch: HEAD)`

### Passo 3: Configurar Serviço do Grafana

```bash
# Habilitar Grafana para iniciar no boot
sudo systemctl enable grafana-server

# Iniciar o Grafana
sudo systemctl start grafana-server

# Verificar status
sudo systemctl status grafana-server
```

**Status esperado:** `Active: active (running)`

### Passo 4: Verificar Instalação

```bash
# Verificar porta (padrão 3000)
sudo netstat -tulpn | grep 3000

# Verificar logs
sudo tail -f /var/log/grafana/grafana.log
```

---

## ⚙️ Configuração Inicial

### Passo 1: Configurar Arquivo Principal

```bash
# Editar configuração do Grafana
sudo nano /etc/grafana/grafana.ini
```

**Configurações importantes:**

```ini
[server]
# Protocolo (http ou https)
protocol = http

# IP do servidor (0.0.0.0 para aceitar todas as conexões)
http_addr = 0.0.0.0

# Porta do Grafana
http_port = 3000

# Domínio público (substitua pelo seu domínio ou IP)
domain = seu-servidor.com
root_url = %(protocol)s://%(domain)s/grafana/

# Permitir embedding em iframes
[security]
allow_embedding = true

# Configurações de autenticação
[auth.anonymous]
# Habilite apenas se quiser acesso sem login (não recomendado)
enabled = false

[auth]
# Desabilitar criação de conta por usuários
disable_signout_menu = false
```

**Salvar:** `Ctrl + O` → `Enter` → `Ctrl + X`

### Passo 2: Reiniciar Grafana

```bash
sudo systemctl restart grafana-server
```

### Passo 3: Primeiro Acesso

1. Abra o navegador e acesse: `http://SEU_IP:3000`
2. **Login padrão:**
   - Usuário: `admin`
   - Senha: `admin`
3. **Você será solicitado a alterar a senha** - escolha uma senha forte!

**✅ Checkpoint:** Se conseguiu acessar a interface do Grafana, a instalação está correta!

---

## 🔌 Conexão com o Banco de Dados MySQL

### Passo 1: Criar Usuário Específico para Grafana no MySQL

```bash
# Conectar ao MySQL
sudo mysql -u root -p
```

**No MySQL, executar:**

```sql
-- Criar usuário para Grafana (somente leitura)
CREATE USER 'grafana_reader'@'localhost' IDENTIFIED BY 'senha_forte_aqui';

-- Conceder permissões de LEITURA no banco principal SmartCEU
GRANT SELECT ON smartceu_db.* TO 'grafana_reader'@'localhost';

-- Conceder permissões de LEITURA no banco de relatórios (opcional)
GRANT SELECT ON smartceu_report_db.* TO 'grafana_reader'@'localhost';

-- Aplicar mudanças
FLUSH PRIVILEGES;

-- Verificar criação
SELECT user, host FROM mysql.user WHERE user='grafana_reader';

-- Sair
EXIT;
```

### Passo 2: Testar Conexão

```bash
# Testar login do usuário Grafana no banco principal
mysql -u grafana_reader -p -h localhost smartceu_db
```

**Teste básico:**
```sql
SHOW TABLES;
SELECT COUNT(*) FROM readings;
EXIT;
```

### Passo 3: Adicionar Data Source no Grafana

1. **Acessar o Grafana** → `http://SEU_IP:3000`
2. **Menu lateral** → ⚙️ **Configuration** → **Data sources**
3. **Clicar em** `Add data source`
4. **Selecionar** `MySQL`

**Configurações do Data Source:**

```yaml
Name: SmartCEU DB (Principal)
Host: localhost:3306
Database: smartceu_db
User: grafana_reader
Password: [senha do grafana_reader]
Max open connections: 100
Max idle connections: 2
Max lifetime: 14400
```

**Opcional - Adicionar também o banco de relatórios:**

```yaml
Name: SmartCEU Report DB
Host: localhost:3306
Database: smartceu_report_db
User: grafana_reader
Password: [senha do grafana_reader]
Max open connections: 100
Max idle connections: 2
Max lifetime: 14400
```

5. **Clicar em** `Save & test`

**✅ Sucesso:** Mensagem verde `Database Connection OK`

---

## 📊 Criação dos Dashboards

### Dashboard 1: Monitoramento em Tempo Real

#### Criar Novo Dashboard

1. **Menu lateral** → **+** → **Dashboard**
2. **Clicar em** `Add new panel`

#### Panel 1: Leituras Recentes por Tipo de Sensor

**Query SQL:**
```sql
SELECT
  UNIX_TIMESTAMP(r.timestamp) AS time_sec,
  s.sensor_type AS metric,
  COUNT(*) AS value
FROM readings r
JOIN sensors s ON r.sensor_id = s.id
WHERE $__timeFilter(r.timestamp)
GROUP BY 
  UNIX_TIMESTAMP(r.timestamp),
  s.sensor_type
ORDER BY time_sec ASC
```

**Configurações do Panel:**
- **Title:** Leituras por Tipo de Sensor
- **Visualization:** Time series
- **Legend:** Show / Bottom
- **Unit:** short
- **Color scheme:** By series

#### Panel 2: Contagem Total de Pessoas

**Query SQL:**
```sql
SELECT
  UNIX_TIMESTAMP(updated_at) AS time_sec,
  total_count AS value
FROM statistics
WHERE $__timeFilter(updated_at)
ORDER BY updated_at DESC
LIMIT 1
```

**Configurações do Panel:**
- **Title:** Total de Pessoas Atual
- **Visualization:** Stat
- **Color mode:** Value
- **Graph mode:** None
- **Text size:** Auto
- **Unit:** people

#### Panel 3: Ocupação por Local

**Query SQL:**
```sql
SELECT
  s.location AS metric,
  COUNT(*) AS value
FROM readings r
JOIN sensors s ON r.sensor_id = s.id
WHERE $__timeFilter(r.timestamp)
GROUP BY s.location
ORDER BY value DESC
```

**Configurações do Panel:**
- **Title:** Leituras por Local
- **Visualization:** Bar chart
- **Orientation:** Horizontal
- **Legend:** Hide

#### Panel 4: Alertas Ativos

**Query SQL:**
```sql
SELECT
  UNIX_TIMESTAMP(a.timestamp) AS time_sec,
  a.alert_type AS metric,
  1 AS value
FROM alerts a
WHERE 
  $__timeFilter(a.timestamp)
  AND a.status = 'active'
ORDER BY a.timestamp DESC
```

**Configurações do Panel:**
- **Title:** Alertas Ativos
- **Visualization:** Table
- **Columns:** Time, Type, Message

### Dashboard 2: Análise de Piscinas

#### Panel 1: Ocupação das Piscinas

**Query SQL:**
```sql
SELECT
  UNIX_TIMESTAMP(pr.timestamp) AS time_sec,
  pr.pool_name AS metric,
  pr.current_occupancy AS value
FROM pool_readings pr
WHERE $__timeFilter(pr.timestamp)
ORDER BY pr.timestamp ASC
```

**Configurações do Panel:**
- **Title:** Ocupação das Piscinas
- **Visualization:** Time series
- **Unit:** people
- **Thresholds:** 
  - 0-50: Green
  - 51-80: Yellow
  - 81-100: Red

#### Panel 2: Temperatura da Água

**Query SQL:**
```sql
SELECT
  UNIX_TIMESTAMP(pr.timestamp) AS time_sec,
  pr.pool_name AS metric,
  pr.water_temperature AS value
FROM pool_readings pr
WHERE $__timeFilter(pr.timestamp)
ORDER BY pr.timestamp ASC
```

**Configurações do Panel:**
- **Title:** Temperatura da Água
- **Visualization:** Time series
- **Unit:** celsius (°C)
- **Min:** 20
- **Max:** 35

#### Panel 3: pH da Água

**Query SQL:**
```sql
SELECT
  UNIX_TIMESTAMP(pr.timestamp) AS time_sec,
  pr.pool_name AS metric,
  pr.water_ph AS value
FROM pool_readings pr
WHERE $__timeFilter(pr.timestamp)
ORDER BY pr.timestamp ASC
```

**Configurações do Panel:**
- **Title:** pH da Água
- **Visualization:** Gauge
- **Min:** 6.0
- **Max:** 8.5
- **Thresholds:**
  - 7.0-7.6: Green (ideal)
  - Outros: Yellow/Red

### Dashboard 3: Estatísticas Gerais

#### Panel 1: Leituras por Hora

**Query SQL:**
```sql
SELECT
  UNIX_TIMESTAMP(DATE_FORMAT(r.timestamp, '%Y-%m-%d %H:00:00')) AS time_sec,
  COUNT(*) AS value
FROM readings r
WHERE $__timeFilter(r.timestamp)
GROUP BY DATE_FORMAT(r.timestamp, '%Y-%m-%d %H:00:00')
ORDER BY time_sec ASC
```

**Configurações do Panel:**
- **Title:** Leituras por Hora
- **Visualization:** Bar chart
- **Unit:** short

#### Panel 2: Média de Pessoas por Dia

**Query SQL:**
```sql
SELECT
  UNIX_TIMESTAMP(DATE(r.timestamp)) AS time_sec,
  AVG(r.person_count) AS value
FROM readings r
WHERE 
  $__timeFilter(r.timestamp)
  AND r.reading_type = 'COUNT'
GROUP BY DATE(r.timestamp)
ORDER BY time_sec ASC
```

**Configurações do Panel:**
- **Title:** Média Diária de Pessoas
- **Visualization:** Time series
- **Unit:** people

#### Panel 3: Sensores Mais Ativos

**Query SQL:**
```sql
SELECT
  s.sensor_id AS metric,
  s.location AS location,
  COUNT(*) AS value
FROM readings r
JOIN sensors s ON r.sensor_id = s.id
WHERE $__timeFilter(r.timestamp)
GROUP BY s.sensor_id, s.location
ORDER BY value DESC
LIMIT 10
```

**Configurações do Panel:**
- **Title:** Top 10 Sensores Mais Ativos
- **Visualization:** Table

### Salvar Dashboard

1. **Clicar no ícone de disquete** (💾) no topo
2. **Nome:** "CEU Tres Pontes - Monitoramento"
3. **Folder:** Criar uma pasta "CEU Dashboards"
4. **Clicar em** `Save`

---

## 🌐 Publicação e Acesso via Internet

### Opção 1: Configurar Proxy Reverso com Nginx (Recomendado)

#### Passo 1: Criar Configuração Nginx para Grafana

```bash
# Criar arquivo de configuração
sudo nano /etc/nginx/sites-available/grafana
```

**Conteúdo:**
```nginx
server {
    listen 80;
    server_name seu-dominio.com;  # Substitua pelo seu domínio
    
    # Redirecionar HTTP para HTTPS (opcional, mas recomendado)
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name seu-dominio.com;  # Substitua pelo seu domínio
    
    # Certificados SSL (configure com Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/seu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seu-dominio.com/privkey.pem;
    
    # Configurações SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Logs
    access_log /var/log/nginx/grafana-access.log;
    error_log /var/log/nginx/grafana-error.log;
    
    # Proxy para Grafana
    location /grafana/ {
        proxy_pass http://localhost:3000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
        proxy_read_timeout 300;
    }
    
    # API do Grafana
    location /grafana/api/ {
        proxy_pass http://localhost:3000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Passo 2: Ativar Configuração

```bash
# Criar link simbólico
sudo ln -s /etc/nginx/sites-available/grafana /etc/nginx/sites-enabled/

# Testar configuração
sudo nginx -t

# Recarregar Nginx
sudo systemctl reload nginx
```

#### Passo 3: Configurar SSL com Let's Encrypt (Opcional mas Recomendado)

```bash
# Instalar Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Obter certificado SSL
sudo certbot --nginx -d seu-dominio.com

# Configurar renovação automática
sudo certbot renew --dry-run
```

### Opção 2: Expor Porta Diretamente (Não Recomendado para Produção)

#### Abrir Porta no Firewall

```bash
# UFW
sudo ufw allow 3000/tcp
sudo ufw reload

# OU iptables
sudo iptables -A INPUT -p tcp --dport 3000 -j ACCEPT
sudo iptables-save | sudo tee /etc/iptables/rules.v4
```

**⚠️ Atenção:** Esta opção expõe o Grafana diretamente na porta 3000 sem SSL.

### Passo 4: Configurar Firewall e Portas

#### No Servidor (UFW)

```bash
# Permitir HTTP e HTTPS
sudo ufw allow 'Nginx Full'
sudo ufw reload
sudo ufw status
```

#### No Roteador/Cloud Provider

- Abrir portas 80 (HTTP) e 443 (HTTPS)
- Configurar port forwarding se necessário
- Verificar Security Groups (AWS/Azure/GCP)

### Passo 5: Testar Acesso Externo

1. **De um dispositivo externo** (celular com 4G, outro local)
2. **Acessar:** `https://seu-dominio.com/grafana/`
3. **Fazer login com suas credenciais**

**✅ Sucesso:** Dashboard carrega normalmente

---

## 🔐 Segurança e Boas Práticas

### 1. Gerenciamento de Usuários

#### Criar Usuários no Grafana

1. **Menu** → ⚙️ **Configuration** → **Users**
2. **Clicar em** `New user`
3. **Preencher:**
   - Name: Nome completo
   - Email: email@example.com
   - Username: usuario
   - Password: senha_forte
4. **Role:** 
   - **Viewer:** Apenas visualização (recomendado para usuários finais)
   - **Editor:** Pode editar dashboards
   - **Admin:** Controle total

#### Configurar Permissões de Dashboard

1. **Abrir o dashboard**
2. **⚙️ Settings** → **Permissions**
3. **Adicionar permissões por:**
   - Usuário específico
   - Equipe
   - Todos (público)

### 2. Autenticação Avançada

#### Configurar LDAP/Active Directory

```bash
sudo nano /etc/grafana/ldap.toml
```

**Exemplo:**
```toml
[[servers]]
host = "ldap.example.com"
port = 389
use_ssl = false
start_tls = false
ssl_skip_verify = false
bind_dn = "cn=admin,dc=grafana,dc=org"
bind_password = 'senha'
search_filter = "(cn=%s)"
search_base_dns = ["dc=grafana,dc=org"]

[servers.attributes]
name = "givenName"
surname = "sn"
username = "cn"
member_of = "memberOf"
email =  "email"
```

### 3. Backup Regular

#### Script de Backup Automático

```bash
# Criar script
sudo nano /usr/local/bin/backup_grafana.sh
```

**Conteúdo:**
```bash
#!/bin/bash
# Backup Grafana - CEU Tres Pontes

BACKUP_DIR="/backup/grafana"
DATE=$(date +%Y%m%d_%H%M%S)
GRAFANA_DB="/var/lib/grafana/grafana.db"

# Criar diretório se não existir
mkdir -p $BACKUP_DIR

# Backup do banco SQLite do Grafana
cp $GRAFANA_DB "$BACKUP_DIR/grafana_${DATE}.db"

# Backup das configurações
tar -czf "$BACKUP_DIR/grafana_config_${DATE}.tar.gz" /etc/grafana/

# Remover backups antigos (manter últimos 7 dias)
find $BACKUP_DIR -name "grafana_*.db" -mtime +7 -delete
find $BACKUP_DIR -name "grafana_config_*.tar.gz" -mtime +7 -delete

echo "Backup concluído: $DATE"
```

**Tornar executável e agendar:**
```bash
sudo chmod +x /usr/local/bin/backup_grafana.sh

# Adicionar ao cron (diariamente às 2h)
sudo crontab -e

# Adicionar linha:
0 2 * * * /usr/local/bin/backup_grafana.sh >> /var/log/grafana_backup.log 2>&1
```

### 4. Monitoramento de Logs

```bash
# Verificar logs de acesso
sudo tail -f /var/log/grafana/grafana.log

# Verificar logs do Nginx
sudo tail -f /var/log/nginx/grafana-access.log
sudo tail -f /var/log/nginx/grafana-error.log
```

### 5. Atualização do Grafana

```bash
# Atualizar Grafana
sudo apt-get update
sudo apt-get upgrade grafana

# Reiniciar serviço
sudo systemctl restart grafana-server
```

---

## 🐛 Troubleshooting

### Problema 1: Grafana não inicia

**Verificar status:**
```bash
sudo systemctl status grafana-server
```

**Verificar logs:**
```bash
sudo journalctl -u grafana-server -n 50
```

**Solução comum:**
```bash
# Verificar permissões
sudo chown -R grafana:grafana /var/lib/grafana
sudo chown -R grafana:grafana /var/log/grafana

# Reiniciar
sudo systemctl restart grafana-server
```

### Problema 2: Erro de conexão com MySQL

**Testar conexão manualmente:**
```bash
mysql -u grafana_reader -p -h localhost smartceu_db
```

**Verificar permissões:**
```sql
SHOW GRANTS FOR 'grafana_reader'@'localhost';
```

**Recriar usuário se necessário:**
```sql
DROP USER 'grafana_reader'@'localhost';
CREATE USER 'grafana_reader'@'localhost' IDENTIFIED BY 'nova_senha';
GRANT SELECT ON smartceu_db.* TO 'grafana_reader'@'localhost';
GRANT SELECT ON smartceu_report_db.* TO 'grafana_reader'@'localhost';
FLUSH PRIVILEGES;
```

### Problema 3: Queries não retornam dados

**Verificar formato do timestamp:**
```sql
-- No Grafana, usar UNIX_TIMESTAMP()
SELECT UNIX_TIMESTAMP(timestamp) AS time_sec, value
FROM readings
WHERE timestamp >= FROM_UNIXTIME($__from / 1000)
  AND timestamp <= FROM_UNIXTIME($__to / 1000)
```

**Verificar timezone:**
```bash
# No servidor
sudo timedatectl set-timezone America/Sao_Paulo

# No Grafana
sudo nano /etc/grafana/grafana.ini
# Adicionar:
[default_timezone]
default_timezone = America/Sao_Paulo
```

### Problema 4: Dashboard lento

**Otimizar queries:**
```sql
-- Adicionar índices nas colunas de timestamp
CREATE INDEX idx_readings_timestamp ON readings(timestamp);
CREATE INDEX idx_pool_readings_timestamp ON pool_readings(timestamp);
CREATE INDEX idx_statistics_updated ON statistics(updated_at);
```

**Limitar resultados:**
```sql
-- Adicionar LIMIT nas queries
SELECT ... FROM readings
WHERE $__timeFilter(timestamp)
ORDER BY timestamp DESC
LIMIT 1000;
```

### Problema 5: Acesso negado via Internet

**Verificar firewall:**
```bash
sudo ufw status verbose
sudo iptables -L -n
```

**Verificar Nginx:**
```bash
sudo nginx -t
sudo systemctl status nginx
sudo tail -f /var/log/nginx/error.log
```

**Verificar DNS:**
```bash
nslookup seu-dominio.com
ping seu-dominio.com
```

---

## 📚 Recursos Adicionais

### Documentação Oficial
- [Grafana Documentation](https://grafana.com/docs/)
- [MySQL Data Source](https://grafana.com/docs/grafana/latest/datasources/mysql/)
- [Dashboard Best Practices](https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/)

### Templates de Dashboard
- [Grafana Dashboard Gallery](https://grafana.com/grafana/dashboards/)

### Comunidade
- [Grafana Community Forums](https://community.grafana.com/)
- [Stack Overflow - Grafana Tag](https://stackoverflow.com/questions/tagged/grafana)

---

## ✅ Checklist Final

- [ ] Grafana instalado e rodando
- [ ] Usuário MySQL para Grafana criado
- [ ] Data source MySQL configurado e testado
- [ ] Dashboard de Monitoramento em Tempo Real criado
- [ ] Dashboard de Piscinas criado
- [ ] Dashboard de Estatísticas criado
- [ ] Nginx configurado como proxy reverso
- [ ] SSL/TLS configurado (Let's Encrypt)
- [ ] Firewall configurado (portas 80/443 abertas)
- [ ] Usuários do Grafana criados com permissões apropriadas
- [ ] Backup automático configurado
- [ ] Acesso externo testado e funcionando
- [ ] Documentação das queries salva

---

## 🎓 Dicas Finais

1. **Comece simples:** Crie um dashboard básico primeiro, depois adicione complexidade
2. **Use variáveis:** Crie dashboards dinâmicos com variáveis para filtrar dados
3. **Organize por pastas:** Agrupe dashboards relacionados em pastas
4. **Documente queries:** Adicione descrições nas queries para facilitar manutenção
5. **Teste performance:** Monitore o tempo de resposta das queries
6. **Use alertas:** Configure alertas para condições críticas
7. **Compartilhe snapshots:** Use snapshots para compartilhar visualizações específicas
8. **Atualize regularmente:** Mantenha o Grafana atualizado para segurança e novos recursos

---

**Desenvolvido por:** UNIVESP - DRP14-PJI410-SALA-004-GRUPO-05  
**Sistema:** CEU Tres Pontes - Controle de Acesso e Monitoramento  
**Data:** Outubro 2025  
**Versão:** 1.0

---

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação completa do projeto em `/docs/README.md`
