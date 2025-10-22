# 🐬 Guia de Instalação MySQL 8.0 no Ubuntu
## Sistema de Controle de Acesso - CEU Tres Pontes

---

## 📋 Pré-requisitos

- Ubuntu Server (20.04 LTS ou superior)
- Acesso sudo
- Conexão com internet

---

## 🚀 Instalação do MySQL 8.0

### Passo 1: Atualizar Repositórios

```bash
# Atualizar lista de pacotes
sudo apt update

# Atualizar pacotes instalados (opcional)
sudo apt upgrade -y
```

### Passo 2: Instalar MySQL Server

```bash
# Instalar MySQL Server 8.0
sudo apt install mysql-server -y

# Verificar versão instalada
mysql --version
```

**Saída esperada:**
```
mysql  Ver 8.0.XX for Linux on x86_64 (Ubuntu)
```

### Passo 3: Verificar Status do Serviço

```bash
# Verificar se MySQL está rodando
sudo systemctl status mysql

# Se não estiver rodando, iniciar:
sudo systemctl start mysql

# Habilitar para iniciar automaticamente no boot
sudo systemctl enable mysql
```

---

## 🔒 Configuração de Segurança

### Passo 4: Executar Script de Segurança

```bash
# Executar script de configuração segura
sudo mysql_secure_installation
```

**Respostas recomendadas:**

1. **VALIDATE PASSWORD COMPONENT?**
   - `Y` (sim) - Recomendado para produção
   - Escolha o nível: `2` (STRONG)

2. **Set root password?**
   - `Y` (sim)
   - Digite uma senha forte e confirme

3. **Remove anonymous users?**
   - `Y` (sim)

4. **Disallow root login remotely?**
   - `Y` (sim) - Por segurança

5. **Remove test database?**
   - `Y` (sim)

6. **Reload privilege tables?**
   - `Y` (sim)

---

## 🗄️ Configuração do Banco de Dados

### Passo 5: Conectar ao MySQL

```bash
# Conectar como root
sudo mysql -u root -p
```

### Passo 6: Criar Banco de Dados e Usuário

```sql
-- Criar banco de dados
CREATE DATABASE ceu_tres_pontes_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Criar usuário (com acesso local)
CREATE USER 'ceu_tres_pontes'@'localhost' 
IDENTIFIED BY 'SuaSenhaSeguraAqui123!';

-- Dar todas as permissões no banco
GRANT ALL PRIVILEGES ON ceu_tres_pontes_db.* 
TO 'ceu_tres_pontes'@'localhost';

-- Se precisar de acesso remoto (cuidado!):
CREATE USER 'ceu_tres_pontes'@'%' 
IDENTIFIED BY 'SuaSenhaSeguraAqui123!';

GRANT ALL PRIVILEGES ON ceu_tres_pontes_db.* 
TO 'ceu_tres_pontes'@'%';

-- Aplicar mudanças
FLUSH PRIVILEGES;

-- Verificar usuários
SELECT user, host FROM mysql.user;

-- Verificar bancos
SHOW DATABASES;

-- Sair
EXIT;
```

### Passo 7: Testar Conexão com Novo Usuário

```bash
# Testar login
mysql -u ceu_tres_pontes -p

# Dentro do MySQL:
USE ceu_tres_pontes_db;
SHOW TABLES;
EXIT;
```

---

## 🌐 Configurar Acesso Remoto (Opcional)

### Passo 8: Editar Configuração do MySQL

```bash
# Editar arquivo de configuração
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```

**Procure e altere:**

```ini
# De:
bind-address = 127.0.0.1

# Para (aceitar conexões de qualquer IP):
bind-address = 0.0.0.0

# OU para IP específico do servidor:
bind-address = 192.168.1.100
```

**Salvar e sair:** `Ctrl + X`, depois `Y`, depois `Enter`

### Passo 9: Reiniciar MySQL

```bash
# Reiniciar serviço
sudo systemctl restart mysql

# Verificar se está rodando
sudo systemctl status mysql
```

### Passo 10: Configurar Firewall (UFW)

```bash
# Verificar status do firewall
sudo ufw status

# Permitir MySQL (porta 3306)
sudo ufw allow 3306/tcp

# OU permitir apenas de IP específico:
sudo ufw allow from 192.168.1.50 to any port 3306

# Recarregar firewall
sudo ufw reload

# Verificar regras
sudo ufw status numbered
```

---

## ⚙️ Otimizações de Performance

### Passo 11: Ajustar Configurações (Opcional)

```bash
# Editar configuração
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```

**Adicionar/ajustar no final do arquivo:**

```ini
[mysqld]
# Configurações básicas de performance
max_connections = 200
innodb_buffer_pool_size = 1G
innodb_log_file_size = 256M
innodb_flush_log_at_trx_commit = 2
innodb_flush_method = O_DIRECT

# Character set
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

# Timezone
default-time-zone = '-03:00'

# Logs
general_log = 0
slow_query_log = 1
slow_query_log_file = /var/log/mysql/mysql-slow.log
long_query_time = 2
```

**Salvar e reiniciar:**

```bash
sudo systemctl restart mysql
```

---

## 🧪 Testes e Verificações

### Testar Conexão Local

```bash
# Teste básico
mysql -u ceu_tres_pontes -p -e "SELECT VERSION();"

# Teste de banco
mysql -u ceu_tres_pontes -p -e "USE ceu_tres_pontes_db; SELECT DATABASE();"
```

### Testar Conexão Remota (do Windows)

```powershell
# Instalar MySQL Client no Windows (se não tiver)
choco install mysql-cli

# Testar conexão
mysql -h IP_DO_SERVIDOR_UBUNTU -u ceu_tres_pontes -p
```

**Exemplo:**
```powershell
mysql -h 192.168.1.100 -u ceu_tres_pontes -p
```

### Verificar Logs

```bash
# Ver logs de erro
sudo tail -f /var/log/mysql/error.log

# Ver logs de queries lentas
sudo tail -f /var/log/mysql/mysql-slow.log

# Ver status do MySQL
mysql -u root -p -e "SHOW STATUS LIKE '%connect%';"
mysql -u root -p -e "SHOW VARIABLES LIKE '%max_connections%';"
```

---

## 📊 Criar Tabelas do Projeto

### Opção 1: Via Flask (Recomendado)

```bash
# No servidor, na pasta do projeto
cd /caminho/do/projeto/backend

# Criar arquivo .env
nano .env
```

**Conteúdo do .env:**

```ini
DB_HOST=localhost
DB_PORT=3306
DB_USER=ceu_tres_pontes
DB_PASSWORD=SuaSenhaSeguraAqui123!
DB_NAME=ceu_tres_pontes_db
```

**Inicializar banco:**

```bash
# Criar tabelas
flask init-db

# Popular com dados de exemplo
flask seed-db
```

### Opção 2: Script SQL Manual

```bash
# Se quiser criar manualmente
mysql -u ceu_tres_pontes -p ceu_tres_pontes_db < schema.sql
```

---

## 🔧 Comandos Úteis

### Gerenciar Serviço

```bash
# Iniciar MySQL
sudo systemctl start mysql

# Parar MySQL
sudo systemctl stop mysql

# Reiniciar MySQL
sudo systemctl restart mysql

# Status
sudo systemctl status mysql

# Habilitar auto-start
sudo systemctl enable mysql

# Desabilitar auto-start
sudo systemctl disable mysql
```

### Backup e Restore

```bash
# Backup de banco de dados
mysqldump -u ceu_tres_pontes -p ceu_tres_pontes_db > backup_$(date +%Y%m%d).sql

# Backup de todas as bases
mysqldump -u root -p --all-databases > backup_all_$(date +%Y%m%d).sql

# Restore
mysql -u ceu_tres_pontes -p ceu_tres_pontes_db < backup_20251018.sql
```

### Monitoramento

```bash
# Processos MySQL
mysqladmin -u root -p processlist

# Status geral
mysqladmin -u root -p status

# Variáveis
mysqladmin -u root -p variables

# Ver conexões ativas
mysql -u root -p -e "SHOW PROCESSLIST;"

# Ver tamanho dos bancos
mysql -u root -p -e "SELECT table_schema AS 'Database', 
ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)' 
FROM information_schema.TABLES 
GROUP BY table_schema;"
```

---

## 🐛 Troubleshooting

### Problema: "Can't connect to MySQL server"

**Solução:**

```bash
# Verificar se está rodando
sudo systemctl status mysql

# Verificar portas
sudo netstat -tlnp | grep mysql

# Verificar logs
sudo tail -50 /var/log/mysql/error.log
```

### Problema: "Access denied for user"

**Solução:**

```bash
# Resetar senha do root
sudo mysql

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'nova_senha';
FLUSH PRIVILEGES;
EXIT;
```

### Problema: "Too many connections"

**Solução:**

```bash
# Aumentar max_connections
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf

# Adicionar:
max_connections = 500

# Reiniciar
sudo systemctl restart mysql
```

### Problema: Conexão remota não funciona

**Checklist:**

```bash
# 1. Verificar bind-address
grep bind-address /etc/mysql/mysql.conf.d/mysqld.cnf

# 2. Verificar firewall
sudo ufw status

# 3. Verificar usuário permite conexão remota
mysql -u root -p -e "SELECT user, host FROM mysql.user WHERE user='ceu_tres_pontes';"

# 4. Testar porta
telnet IP_SERVIDOR 3306
```

---

## 📈 Monitoramento de Performance

### Instalar ferramentas (opcional)

```bash
# Instalar mytop (monitor em tempo real)
sudo apt install mytop -y

# Usar
mytop -u root -p

# Instalar innotop (monitor InnoDB)
sudo apt install innotop -y

# Usar
innotop -u root -p
```

---

## 🔐 Boas Práticas de Segurança

### 1. Sempre use senhas fortes

```bash
# Gerar senha forte
openssl rand -base64 32
```

### 2. Limitar acesso por IP

```sql
-- Permitir apenas de IPs específicos
CREATE USER 'ceu_tres_pontes'@'192.168.1.50' IDENTIFIED BY 'senha';
```

### 3. Usar SSL/TLS (Produção)

```bash
# Verificar se SSL está habilitado
mysql -u root -p -e "SHOW VARIABLES LIKE '%ssl%';"
```

### 4. Backups regulares

```bash
# Criar script de backup automático
sudo nano /usr/local/bin/mysql_backup.sh
```

```bash
#!/bin/bash
# Backup automático MySQL
BACKUP_DIR="/backup/mysql"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
mysqldump -u ceu_tres_pontes -pSuaSenha ceu_tres_pontes_db | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Manter apenas últimos 7 dias
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete
```

```bash
# Dar permissão de execução
sudo chmod +x /usr/local/bin/mysql_backup.sh

# Agendar no cron (diário às 2h da manhã)
sudo crontab -e

# Adicionar:
0 2 * * * /usr/local/bin/mysql_backup.sh
```

---

## ✅ Checklist de Instalação

- [ ] MySQL 8.0 instalado
- [ ] Serviço MySQL rodando
- [ ] Script de segurança executado
- [ ] Banco `ceu_tres_pontes_db` criado
- [ ] Usuário `ceu_tres_pontes` criado
- [ ] Permissões configuradas
- [ ] Conexão local testada
- [ ] Firewall configurado (se necessário)
- [ ] Acesso remoto configurado (se necessário)
- [ ] Backups configurados
- [ ] Logs verificados

---

## 📞 Informações de Conexão

**Para uso no projeto (.env):**

```ini
DB_HOST=localhost  # ou IP do servidor
DB_PORT=3306
DB_USER=ceu_tres_pontes
DB_PASSWORD=SuaSenhaSeguraAqui123!
DB_NAME=ceu_tres_pontes_db
```

**String de conexão:**

```
mysql+pymysql://ceu_tres_pontes:SuaSenhaSeguraAqui123!@localhost:3306/ceu_tres_pontes_db
```

---

## 🎯 Próximos Passos

Após instalar o MySQL:

1. ✅ Configurar `.env` no backend Flask
2. ✅ Executar `flask init-db` para criar tabelas
3. ✅ Executar `flask seed-db` para dados iniciais
4. ✅ Testar conexão do Flask com MySQL
5. ✅ Continuar desenvolvimento da API

---

**Instalação concluída com sucesso!** 🎉

---

**Última atualização:** Outubro 2025  
**Versão MySQL:** 8.0.XX  
**Sistema:** Ubuntu Server 20.04+
