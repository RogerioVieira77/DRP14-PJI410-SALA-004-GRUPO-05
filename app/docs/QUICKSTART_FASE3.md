# ⚡ Quick Start - Fase 3: Backend Flask

## 🎯 Pré-requisitos

- Python 3.12+
- MySQL 8.0+ instalado e rodando
- Mosquitto MQTT (da Fase 2)

---

## 📦 Passo 1: Configurar MySQL

### Windows PowerShell

```powershell
# Conectar ao MySQL
mysql -u root -p

# Criar banco de dados
CREATE DATABASE ceu_tres_pontes_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Criar usuário
CREATE USER 'ceu_tres_pontes'@'localhost' IDENTIFIED BY 'seu_password_aqui';

# Dar permissões
GRANT ALL PRIVILEGES ON ceu_tres_pontes_db.* TO 'ceu_tres_pontes'@'localhost';
FLUSH PRIVILEGES;

# Verificar
SHOW DATABASES;
EXIT;
```

---

## 📦 Passo 2: Configurar Ambiente Python

```powershell
# Navegar até a pasta backend
cd "C:\PI - IV - V1\backend"

# Instalar dependências
pip install -r requirements-phase3.txt
```

---

## 📦 Passo 3: Configurar Variáveis de Ambiente

```powershell
# Copiar arquivo de exemplo
copy .env.example .env

# Editar .env com suas configurações
notepad .env
```

### Configurações importantes no `.env`:

```ini
# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=ceu_tres_pontes
DB_PASSWORD=seu_password_aqui
DB_NAME=ceu_tres_pontes_db

# Secret Keys (MUDE EM PRODUÇÃO!)
SECRET_KEY=sua-chave-secreta-super-segura
JWT_SECRET_KEY=sua-chave-jwt-super-segura

# Flask
FLASK_APP=app.py
FLASK_ENV=development
DEBUG=True
```

---

## 📦 Passo 4: Inicializar Banco de Dados

```powershell
# Criar todas as tabelas
flask init-db

# Popular com dados de exemplo (opcional)
flask seed-db
```

**Dados criados:**
- ✅ Usuário admin (username: `admin`, password: `admin123`)
- ✅ 6 sensores de exemplo

---

## 🚀 Passo 5: Executar o Backend

```powershell
# Executar servidor Flask
python app.py
```

**Servidor rodando em:** `http://localhost:5000`

---

## 🧪 Passo 6: Testar a API

### Health Check

```powershell
# Básico
curl http://localhost:5000/health

# Database
curl http://localhost:5000/health/db

# Detalhado
curl http://localhost:5000/health/detailed
```

### Criar usuário admin (se não usou seed-db)

```powershell
flask create-admin
```

---

## 📚 Endpoints Disponíveis

### Health (Não autenticado)
- `GET /health` - Health check básico
- `GET /health/db` - Status do banco de dados
- `GET /health/detailed` - Health check detalhado

### Autenticação (Em desenvolvimento)
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/register` - Registrar
- `GET /api/v1/auth/me` - Dados do usuário atual

### Sensores (Requer autenticação)
- `GET /api/v1/sensors` - Listar todos os sensores
- `GET /api/v1/sensors/:id` - Detalhes de um sensor
- `POST /api/v1/sensors` - Criar sensor (admin)
- `PUT /api/v1/sensors/:id` - Atualizar sensor (admin)
- `DELETE /api/v1/sensors/:id` - Remover sensor (admin)

### Leituras (Requer autenticação)
- `GET /api/v1/readings` - Listar leituras
- `GET /api/v1/readings/:id` - Detalhes de uma leitura

### Estatísticas (Requer autenticação)
- `GET /api/v1/statistics/daily/:date` - Estatísticas diárias
- `GET /api/v1/statistics/hourly/:date` - Estatísticas por hora
- `GET /api/v1/statistics/range` - Estatísticas de período

---

## 🔧 Comandos Flask CLI

```powershell
# Criar tabelas
flask init-db

# Remover todas as tabelas
flask drop-db

# Popular com dados de exemplo
flask seed-db

# Criar usuário admin
flask create-admin

# Shell interativo
flask shell
```

---

## 🐛 Troubleshooting

### Erro: "Access denied for user"

**Solução:**
1. Verificar credenciais no `.env`
2. Verificar permissões do usuário MySQL
3. Testar conexão: `mysql -u ceu_tres_pontes -p`

### Erro: "No module named 'app'"

**Solução:**
```powershell
# Certifique-se de estar na pasta backend
cd "C:\PI - IV - V1\backend"

# Definir PYTHONPATH
$env:PYTHONPATH = (Get-Location).Path
```

### Erro: "Cannot find module 'MySQLdb'"

**Solução:**
```powershell
# Instalar mysqlclient
pip install mysqlclient

# Se falhar, instalar PyMySQL (já está no requirements)
pip install PyMySQL
```

### Porta 5000 em uso

**Solução:**
```powershell
# Editar app.py e mudar a porta, ou:
$env:FLASK_RUN_PORT = "5001"
python app.py
```

---

## 📊 Próximos Passos

1. ✅ Backend iniciado
2. 🔄 Implementar rotas da API (em desenvolvimento)
3. 🔄 Implementar subscriber MQTT → Database
4. 📅 Frontend (Fase 4)

---

**Status:** Fase 3 em desenvolvimento  
**Última atualização:** Outubro 2025
