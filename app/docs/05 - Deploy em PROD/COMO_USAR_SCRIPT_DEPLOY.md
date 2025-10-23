# 🚀 Script de Deploy Automatizado - SmartCEU

## 📋 Informações do Script

**Arquivo:** `deploy_smartceu.sh`  
**Localização:** `c:\PI - IV - V1\deploy\deploy_smartceu.sh`  
**Tempo Estimado:** 5-10 minutos  
**Sistema:** Ubuntu 24.04 LTS

---

## ✅ Pré-requisitos Confirmados

Todas as informações necessárias foram coletadas:

| Item | Status | Valor |
|------|--------|-------|
| **Servidor** | ✅ | 82.25.75.88 |
| **Sistema** | ✅ | Ubuntu 24.04.2 LTS |
| **Usuário SSH** | ✅ | root@82.25.75.88 |
| **Chave SSH** | ✅ | ssh-ed25519 AAAA...HpwfD |
| **MySQL Root** | ✅ | Ceu@)@%01 |
| **Domínio** | ✅ | Não necessário (usará IP) |
| **Recursos** | ✅ | 2 vCPU, 7.8GB RAM, 91GB livre |

---

## 🎯 O Que o Script Faz

### Etapas Automatizadas (13 no total)

1. **Criar estrutura de diretórios** (`/var/www/smartceu/`)
2. **Instalar dependências do sistema** (Python, Git, Mosquitto, etc)
3. **Criar ambiente virtual Python**
4. **Configurar MySQL** (database `smartceu_db` + usuário)
5. **Configurar Mosquitto MQTT** (porta 1884)
6. **Clonar repositório GitHub**
7. **Instalar dependências Python** (Flask, PyMySQL, etc)
8. **Configurar variáveis de ambiente** (.env com secrets gerados)
9. **Criar tabelas do banco de dados**
10. **Configurar NGINX** (proxy reverso)
11. **Criar serviço systemd** (auto-start da API)
12. **Configurar backup automático** (cron diário às 2h)
13. **Executar testes de validação**

---

## 📦 Configurações Incluídas

### Portas Configuradas
- **API Flask:** 5001
- **MQTT Broker:** 1884
- **NGINX:** 80 (proxy para API)

### Credenciais MySQL
- **Database:** smartceu_db
- **User:** smartceu_user
- **Password:** SmartCEU2025)!

### Credenciais MQTT
- **User:** smartceu_mqtt
- **Password:** smartceu_user
- **Allow Anonymous:** true (para facilitar desenvolvimento)

### Secrets Flask
- **SECRET_KEY:** Gerado automaticamente (32 bytes hex)
- **JWT_SECRET_KEY:** Gerado automaticamente (32 bytes hex)

---

## 🚀 Como Usar

### Opção 1: Upload e Execução Manual

#### 1. Transferir o script para o servidor

**No Windows (PowerShell):**
```powershell
# Navegar até a pasta do projeto
cd "C:\PI - IV - V1\deploy"

# Transferir via SCP
scp deploy_smartceu.sh root@82.25.75.88:/root/
```

#### 2. Conectar via SSH

```powershell
ssh root@82.25.75.88
```

#### 3. Executar o script

```bash
# Dar permissão de execução
chmod +x /root/deploy_smartceu.sh

# Executar como root
sudo bash /root/deploy_smartceu.sh
```

---

### Opção 2: Execução Remota (Recomendado)

**Um único comando no PowerShell:**

```powershell
cd "C:\PI - IV - V1\deploy"

# Transferir e executar remotamente
scp deploy_smartceu.sh root@82.25.75.88:/tmp/; ssh root@82.25.75.88 "chmod +x /tmp/deploy_smartceu.sh && sudo bash /tmp/deploy_smartceu.sh"
```

---

## 📊 Durante a Execução

O script irá:

1. ✅ Mostrar banner do SmartCEU
2. ⚠️ Pedir confirmação para continuar
3. 📝 Exibir cada etapa com mensagens coloridas:
   - 🔵 Azul: Início de etapa
   - 🟢 Verde: Sucesso
   - 🟡 Amarelo: Avisos
   - 🔴 Vermelho: Erros

### Exemplo de Output:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
>>> ETAPA 1/10: Criando estrutura de diretórios
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Diretórios criados em: /var/www/smartceu

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
>>> ETAPA 2/10: Instalando dependências do sistema
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
...
```

---

## ✅ Após o Deploy

### Validações Automáticas

O script testará automaticamente:
- ✅ Conectividade MySQL
- ✅ Mosquitto MQTT
- ✅ API Flask (http://localhost:5001/health)
- ✅ NGINX (http://82.25.75.88/health)

### Mensagem Final

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ DEPLOY CONCLUÍDO COM SUCESSO! ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Resumo da Instalação:
   • Tempo de deploy: 7m 23s
   • Diretório: /var/www/smartceu
   • API Port: 5001
   • MQTT Port: 1884
   • Database: smartceu_db

🌐 Acessos:
   • Frontend: http://82.25.75.88/
   • Pool Monitor: http://82.25.75.88/monitoramento_piscina.html
   • API Health: http://82.25.75.88/health
```

---

## 🔧 Comandos Úteis Pós-Deploy

### Gerenciar API
```bash
# Ver status
systemctl status smartceu-api

# Reiniciar
systemctl restart smartceu-api

# Parar
systemctl stop smartceu-api

# Ver logs em tempo real
tail -f /var/www/smartceu/logs/api.log

# Ver logs de erro
tail -f /var/www/smartceu/logs/api_error.log
```

### Gerenciar NGINX
```bash
# Testar configuração
nginx -t

# Recarregar configuração
systemctl reload nginx

# Ver logs de acesso
tail -f /var/log/nginx/smartceu_access.log

# Ver logs de erro
tail -f /var/log/nginx/smartceu_error.log
```

### Gerenciar MySQL
```bash
# Conectar ao banco
mysql -u smartceu_user -p smartceu_db

# Ver tabelas
mysql -u smartceu_user -p -e "USE smartceu_db; SHOW TABLES;"

# Backup manual
/var/www/smartceu/backup_db.sh
```

### Gerenciar MQTT
```bash
# Testar conexão
mosquitto_sub -h localhost -p 1884 -t '#' -v

# Publicar mensagem teste
mosquitto_pub -h localhost -p 1884 -t 'test' -m 'Hello SmartCEU'

# Ver status
systemctl status mosquitto
```

---

## 🔍 Troubleshooting

### API não está respondendo

```bash
# 1. Verificar se o serviço está rodando
systemctl status smartceu-api

# 2. Ver logs de erro
tail -n 50 /var/www/smartceu/logs/api_error.log

# 3. Tentar iniciar manualmente
cd /var/www/smartceu/app/backend
/var/www/smartceu/venv/bin/python3 app.py
```

### NGINX retorna 502 Bad Gateway

```bash
# 1. Verificar se API está rodando
curl http://localhost:5001/health

# 2. Testar configuração NGINX
nginx -t

# 3. Ver logs
tail -f /var/log/nginx/smartceu_error.log
```

### Erro de conexão MySQL

```bash
# 1. Verificar se MySQL está rodando
systemctl status mysql

# 2. Testar credenciais
mysql -u smartceu_user -p'SmartCEU2025)!' smartceu_db -e "SELECT 1;"

# 3. Ver logs
tail -f /var/log/mysql/error.log
```

### MQTT não conecta

```bash
# 1. Verificar se Mosquitto está rodando
systemctl status mosquitto

# 2. Testar porta
netstat -tulpn | grep 1884

# 3. Ver logs
tail -f /var/log/mosquitto/mosquitto.log
```

---

## 🔄 Atualizar a Aplicação

```bash
# Parar API
systemctl stop smartceu-api

# Atualizar código
cd /var/www/smartceu/app
sudo -u www-data git pull origin main

# Atualizar dependências (se necessário)
/var/www/smartceu/venv/bin/pip install -r requirements.txt

# Reiniciar API
systemctl start smartceu-api
```

---

## 🗑️ Desinstalar (se necessário)

```bash
# Parar serviços
systemctl stop smartceu-api
systemctl disable smartceu-api

# Remover configurações
rm /etc/systemd/system/smartceu-api.service
rm /etc/nginx/sites-enabled/smartceu
rm /etc/nginx/sites-available/smartceu

# Remover arquivos
rm -rf /var/www/smartceu

# Remover banco de dados
mysql -u root -p -e "DROP DATABASE smartceu_db; DROP USER 'smartceu_user'@'localhost';"

# Recarregar serviços
systemctl daemon-reload
systemctl reload nginx
```

---

## 📞 Suporte

Se encontrar problemas:

1. **Ver logs:** Sempre comece verificando os logs
2. **Testar conectividade:** Use `curl` para testar endpoints
3. **Verificar recursos:** `htop` para ver CPU/RAM
4. **Verificar portas:** `netstat -tulpn` para ver o que está usando cada porta

---

## 📝 Notas Importantes

1. **Senha MySQL Root:** O script usa a senha fornecida (`Ceu@)@%01`)
2. **Secrets Flask:** São gerados automaticamente e salvos no `.env`
3. **Backup Automático:** Configurado para rodar diariamente às 2h da manhã
4. **Logs:** Todos os logs ficam em `/var/www/smartceu/logs/`
5. **Isolamento:** A aplicação roda com usuário `www-data`, mesma do Agasalho Aqui
6. **Porta 80:** NGINX gerencia múltiplos sites (Agasalho Aqui continua funcionando)

---

## ✅ Status Final

- ✅ Script criado e pronto para uso
- ✅ Todas as credenciais configuradas
- ✅ Portas definidas sem conflitos (5001, 1884)
- ✅ Backup automático incluído
- ✅ Testes de validação automáticos
- ✅ Documentação completa

**O script está pronto para ser executado!** 🚀
