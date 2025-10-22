# 📦 Instalação MySQL no Servidor Ubuntu - Guia Rápido

---

## 🎯 Duas Opções de Instalação

### Opção 1: Script Automatizado (Mais Rápido) ⚡

```bash
# 1. Fazer upload do script para o servidor Ubuntu
# (use SCP, FTP, ou cole o conteúdo manualmente)

# 2. Dar permissão de execução
chmod +x scripts/install_mysql_ubuntu.sh

# 3. Executar
./scripts/install_mysql_ubuntu.sh

# 4. Seguir as instruções (será solicitada senha para o banco)
```

**O script fará automaticamente:**
- ✅ Atualização de pacotes
- ✅ Instalação do MySQL 8.0
- ✅ Criação do banco `ceu_tres_pontes_db`
- ✅ Criação do usuário `ceu_tres_pontes`
- ✅ Configuração de permissões
- ✅ Teste de conexão

---

### Opção 2: Manual (Passo a Passo) 📋

Se preferir fazer manualmente, siga o guia completo em:
**`docs/MYSQL_SETUP_UBUNTU.md`**

**Comandos principais:**

```bash
# 1. Atualizar sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar MySQL
sudo apt install mysql-server -y

# 3. Verificar instalação
mysql --version
sudo systemctl status mysql

# 4. Executar configuração de segurança
sudo mysql_secure_installation

# 5. Conectar ao MySQL
sudo mysql -u root -p

# 6. Criar banco e usuário (dentro do MySQL)
CREATE DATABASE ceu_tres_pontes_db 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'ceu_tres_pontes'@'localhost' 
IDENTIFIED BY 'SuaSenhaSeguraAqui123!';

GRANT ALL PRIVILEGES ON ceu_tres_pontes_db.* 
TO 'ceu_tres_pontes'@'localhost';

FLUSH PRIVILEGES;
EXIT;

# 7. Testar conexão
mysql -u ceu_tres_pontes -p
```

---

## 🔧 Após a Instalação

### 1. Anotar Credenciais

```
Host: localhost (ou IP do servidor)
Porta: 3306
Usuário: ceu_tres_pontes
Senha: [a senha que você definiu]
Banco: ceu_tres_pontes_db
```

### 2. Configurar Acesso Remoto (Se necessário)

```bash
# Editar configuração
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf

# Mudar:
# bind-address = 127.0.0.1
# Para:
# bind-address = 0.0.0.0

# Salvar: Ctrl+X, Y, Enter

# Reiniciar MySQL
sudo systemctl restart mysql

# Liberar firewall
sudo ufw allow 3306/tcp
```

**Criar usuário para acesso remoto:**

```bash
sudo mysql -u root -p
```

```sql
CREATE USER 'ceu_tres_pontes'@'%' 
IDENTIFIED BY 'SuaSenhaSeguraAqui123!';

GRANT ALL PRIVILEGES ON ceu_tres_pontes_db.* 
TO 'ceu_tres_pontes'@'%';

FLUSH PRIVILEGES;
EXIT;
```

### 3. Testar do Windows

```powershell
# Instalar MySQL Client (se necessário)
choco install mysql-cli

# Testar conexão
mysql -h IP_DO_SERVIDOR_UBUNTU -u ceu_tres_pontes -p

# Exemplo:
mysql -h 192.168.1.100 -u ceu_tres_pontes -p
```

---

## 🚀 Configurar Backend Flask

### No servidor Ubuntu:

```bash
# 1. Navegar até o projeto
cd /caminho/do/projeto/backend

# 2. Criar arquivo .env
nano .env
```

**Conteúdo do .env:**

```ini
# Flask
FLASK_APP=app.py
FLASK_ENV=development
DEBUG=True

# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=ceu_tres_pontes
DB_PASSWORD=SuaSenhaSeguraAqui123!
DB_NAME=ceu_tres_pontes_db

# Secret Keys
SECRET_KEY=gere-uma-chave-aleatoria-super-segura
JWT_SECRET_KEY=outra-chave-diferente-tambem-segura

# MQTT (da Fase 2)
MQTT_BROKER_HOST=localhost
MQTT_BROKER_PORT=1883
MQTT_USERNAME=ceu_tres_pontes
MQTT_PASSWORD=secure_password
```

**Salvar:** `Ctrl+X`, `Y`, `Enter`

### Gerar chaves secretas:

```bash
# Gerar SECRET_KEY
python3 -c "import secrets; print(secrets.token_hex(32))"

# Gerar JWT_SECRET_KEY
python3 -c "import secrets; print(secrets.token_hex(32))"

# Copiar e colar no .env
```

### Instalar dependências Python:

```bash
# Instalar pip (se necessário)
sudo apt install python3-pip -y

# Instalar dependências do projeto
pip3 install -r requirements-phase3.txt
```

### Inicializar banco de dados:

```bash
# Criar tabelas
flask init-db

# Popular com dados de exemplo
flask seed-db
```

**Dados criados:**
- ✅ Usuário admin (username: `admin`, password: `admin123`)
- ✅ 6 sensores de exemplo

### Testar backend:

```bash
# Iniciar servidor Flask
python3 app.py

# OU com flask run
flask run --host=0.0.0.0 --port=5000
```

**Testar do Windows:**

```powershell
# Health check
curl http://IP_DO_SERVIDOR:5000/health

# Health check detalhado
curl http://IP_DO_SERVIDOR:5000/health/detailed
```

---

## ✅ Checklist de Verificação

### MySQL:
- [ ] MySQL 8.0 instalado
- [ ] Serviço rodando (`sudo systemctl status mysql`)
- [ ] Banco `ceu_tres_pontes_db` criado
- [ ] Usuário `ceu_tres_pontes` criado
- [ ] Conexão local funciona
- [ ] Conexão remota funciona (se configurado)

### Backend:
- [ ] Dependências Python instaladas
- [ ] Arquivo `.env` criado e configurado
- [ ] Comando `flask init-db` executado com sucesso
- [ ] Comando `flask seed-db` executado com sucesso
- [ ] Servidor Flask inicia sem erros
- [ ] Endpoint `/health` responde

---

## 🐛 Problemas Comuns

### "Can't connect to MySQL server"

```bash
# Verificar se está rodando
sudo systemctl status mysql

# Iniciar se necessário
sudo systemctl start mysql
```

### "Access denied for user"

```bash
# Resetar senha
sudo mysql
ALTER USER 'ceu_tres_pontes'@'localhost' IDENTIFIED BY 'nova_senha';
FLUSH PRIVILEGES;
EXIT;
```

### Firewall bloqueando

```bash
# Verificar firewall
sudo ufw status

# Permitir MySQL
sudo ufw allow 3306/tcp

# Permitir Flask (se necessário)
sudo ufw allow 5000/tcp
```

### ImportError no Python

```bash
# Instalar mysqlclient (pode ser necessário)
sudo apt install python3-dev default-libmysqlclient-dev build-essential -y
pip3 install mysqlclient

# OU usar PyMySQL (já no requirements)
pip3 install PyMySQL
```

---

## 📞 Informações Importantes

### Credenciais MySQL:
```
Host: localhost (local) ou IP do servidor (remoto)
Porta: 3306
Usuário: ceu_tres_pontes
Senha: [definida na instalação]
Banco: ceu_tres_pontes_db
```

### String de Conexão:
```
mysql+pymysql://ceu_tres_pontes:senha@localhost:3306/ceu_tres_pontes_db
```

### Usuário Admin do Sistema:
```
Username: admin
Password: admin123
Role: admin
```

⚠️ **IMPORTANTE:** Mude a senha do admin em produção!

---

## 🎯 Próximos Passos

Após instalar MySQL e configurar o backend:

1. ✅ MySQL instalado e configurado
2. ✅ Backend Flask conectado ao MySQL
3. 🔄 Continuar desenvolvimento das rotas da API
4. 🔄 Implementar MQTT Subscriber → Database
5. 📅 Desenvolver Frontend (Fase 4)

---

**Precisa de ajuda?** Consulte os documentos detalhados em `docs/` ou me avise! 🚀

---

**Última atualização:** 18 de Outubro de 2025
