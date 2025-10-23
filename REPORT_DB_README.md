# Sistema de Replicação do Banco de Relatórios SmartCEU

## 📋 Visão Geral

Este sistema cria e mantém uma base de dados auxiliar (`smartceu_report_db`) para uso em relatórios e análises, separando a carga de consultas analíticas da base de aplicação principal (`smartceu_db`).

## 🎯 Objetivos

- **Separação de Cargas**: Isolar consultas de relatórios da aplicação principal
- **Performance**: Evitar impacto de queries pesadas na aplicação em produção
- **Segurança**: Base somente leitura para ferramentas de BI e relatórios
- **Disponibilidade**: Sincronização diária automatizada

## 📁 Arquivos do Sistema

### 1. `create_report_db.sh`
**Propósito**: Criação inicial do banco de relatórios

**Funcionalidades**:
- Verifica existência dos bancos de dados
- Cria backup antes de recriar (se já existir)
- Cria banco `smartceu_report_db` com charset utf8mb4
- Faz dump completo do banco principal
- Importa todos os dados
- Verifica integridade (contagem de tabelas e registros)

**Quando usar**:
- Primeira configuração do ambiente
- Recreação completa do banco de relatórios
- Recuperação após problemas de corrupção

**Uso**:
```bash
bash create_report_db.sh
```

### 2. `sync_report_db.sh`
**Propósito**: Sincronização diária dos dados

**Funcionalidades**:
- Cria backup de segurança antes da sincronização
- Coleta estatísticas antes/depois
- Remove e recria o banco de relatórios
- Importa dados atualizados do banco principal
- Otimiza tabelas após importação
- Remove backups com mais de 7 dias
- Registra operações em log

**Estratégia de Sincronização**:
- **Drop & Import**: Remove completamente e recria o banco
- **Vantagens**: 
  - Garante consistência total dos dados
  - Simples e confiável
  - Remove registros deletados automaticamente
- **Desvantagens**:
  - Não é incremental (reimporta tudo)
  - Tempo de execução proporcional ao tamanho do banco

**Quando usar**:
- Execução diária automática (via cron)
- Sincronização manual quando necessário

**Uso**:
```bash
bash sync_report_db.sh
```

**Log**: `/var/log/smartceu_report_sync.log`

### 3. `setup_report_cron.sh`
**Propósito**: Configuração do agendamento automático

**Funcionalidades**:
- Verifica arquivos e permissões
- Cria arquivo de log
- Configura cron job para execução às 3:00 AM
- Valida configuração
- Mostra próxima execução programada

**Horário Padrão**: 3:00 AM (todos os dias)

**Quando usar**:
- Primeira configuração do ambiente
- Alteração do horário de sincronização
- Reconfiguração após mudanças

**Uso**:
```bash
bash setup_report_cron.sh
```

## 🚀 Instalação Completa

### Passo 1: Transferir Scripts para o Servidor

```bash
# Na máquina local (Windows PowerShell)
scp create_report_db.sh root@82.25.75.88:/var/www/smartceu/
scp sync_report_db.sh root@82.25.75.88:/var/www/smartceu/
scp setup_report_cron.sh root@82.25.75.88:/var/www/smartceu/
```

### Passo 2: Conectar ao Servidor

```bash
ssh root@82.25.75.88
cd /var/www/smartceu
```

### Passo 3: Conceder Permissões de Execução

```bash
chmod +x create_report_db.sh
chmod +x sync_report_db.sh
chmod +x setup_report_cron.sh
```

### Passo 4: Criar o Banco de Relatórios

```bash
bash create_report_db.sh
```

**Saída esperada**:
- ✓ Verificação dos bancos
- ✓ Criação do banco de relatórios
- ✓ Exportação dos dados
- ✓ Importação no novo banco
- ✓ Contagem de tabelas (6 tabelas)
- ✓ Contagem de registros por tabela

### Passo 5: Testar Sincronização Manual

```bash
bash sync_report_db.sh
```

**Saída esperada**:
- ✓ Backup de segurança criado
- ✓ Estatísticas antes/depois
- ✓ Sincronização concluída
- ✓ Otimização realizada

### Passo 6: Configurar Execução Automática

```bash
bash setup_report_cron.sh
```

**Saída esperada**:
- ✓ Script encontrado
- ✓ Log configurado
- ✓ Cron job criado
- ✓ Próxima execução programada

## 📊 Estrutura do Banco de Relatórios

```
smartceu_report_db
├── users              (usuários do sistema)
├── sensors            (sensores cadastrados)
├── sensor_readings    (leituras dos sensores)
├── pool_readings      (leituras das piscinas)
├── alerts             (alertas gerados)
└── statistics         (estatísticas agregadas)
```

**Charset**: utf8mb4  
**Collation**: utf8mb4_unicode_ci

## 🔧 Configuração

### Credenciais (hardcoded nos scripts)
```bash
DB_USER="smartceu_user"
DB_PASS="SmartCEU2025)!"
DB_SOURCE="smartceu_db"
DB_REPORT="smartceu_report_db"
# Credenciais para o banco de relatórios (separadas)
DB_REPORT_USER="smart_ceu_report"
DB_REPORT_PASS="SmartCEU2025)!"
# Nota: O script usa as credenciais root temporariamente para criar/importar o banco.
# Root do MySQL no ambiente de relatório foi definido como:
DB_ROOT_USER="root"
DB_ROOT_PASS="SmartCEU2025)!"
```

### Diretórios e Arquivos
```bash
# Scripts
/var/www/smartceu/create_report_db.sh
/var/www/smartceu/sync_report_db.sh
/var/www/smartceu/setup_report_cron.sh

# Backups de sincronização
/var/www/smartceu/backups/report_sync/

# Log de sincronização
/var/log/smartceu_report_sync.log
```

### Horário de Sincronização

Para alterar o horário (padrão: 3:00 AM):

1. Editar `setup_report_cron.sh`:
```bash
CRON_TIME="0 3 * * *"  # Formato: minuto hora dia mês dia_semana
```

Exemplos:
- `0 2 * * *` → 2:00 AM todos os dias
- `30 4 * * *` → 4:30 AM todos os dias
- `0 3 * * 0` → 3:00 AM apenas aos domingos

2. Executar novamente:
```bash
bash setup_report_cron.sh
```

## 📋 Comandos Úteis

### Verificar Status da Sincronização
```bash
# Ver últimas linhas do log
tail -n 50 /var/log/smartceu_report_sync.log

# Acompanhar em tempo real
tail -f /var/log/smartceu_report_sync.log
```

### Verificar Cron Jobs
```bash
# Listar cron jobs
crontab -l

# Editar cron jobs
crontab -e
```

### Executar Sincronização Manual
```bash
cd /var/www/smartceu
bash sync_report_db.sh
```

### Verificar Tamanho dos Bancos
```bash
mysql -u smartceu_user -p'SmartCEU2025)!' -e "
SELECT 
    table_schema AS 'Banco',
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Tamanho (MB)'
FROM information_schema.tables
WHERE table_schema IN ('smartceu_db', 'smartceu_report_db')
GROUP BY table_schema;
"
```

### Comparar Registros entre Bancos
```bash
mysql -u smartceu_user -p'SmartCEU2025)!' -e "
SELECT 'users' AS tabela,
    (SELECT COUNT(*) FROM smartceu_db.users) AS producao,
    (SELECT COUNT(*) FROM smartceu_report_db.users) AS relatorio
UNION ALL
SELECT 'sensors',
    (SELECT COUNT(*) FROM smartceu_db.sensors),
    (SELECT COUNT(*) FROM smartceu_report_db.sensors)
UNION ALL
SELECT 'sensor_readings',
    (SELECT COUNT(*) FROM smartceu_db.sensor_readings),
    (SELECT COUNT(*) FROM smartceu_report_db.sensor_readings)
UNION ALL
SELECT 'pool_readings',
    (SELECT COUNT(*) FROM smartceu_db.pool_readings),
    (SELECT COUNT(*) FROM smartceu_report_db.pool_readings)
UNION ALL
SELECT 'alerts',
    (SELECT COUNT(*) FROM smartceu_db.alerts),
    (SELECT COUNT(*) FROM smartceu_report_db.alerts)
UNION ALL
SELECT 'statistics',
    (SELECT COUNT(*) FROM smartceu_db.statistics),
    (SELECT COUNT(*) FROM smartceu_report_db.statistics);
"
```

## 🔐 Segurança

### Permissões Recomendadas

```bash
# Scripts
chmod 750 create_report_db.sh
chmod 750 sync_report_db.sh
chmod 750 setup_report_cron.sh
chown root:www-data *.sh

# Diretório de backups
chmod 755 /var/www/smartceu/backups/report_sync
chown www-data:www-data /var/www/smartceu/backups/report_sync

# Log
chmod 664 /var/log/smartceu_report_sync.log
chown www-data:www-data /var/log/smartceu_report_sync.log
```

### Usuário de Banco Somente Leitura (Recomendado)

Para conectar ferramentas de BI ao banco de relatórios:

```sql
-- Criar usuário somente leitura
CREATE USER 'smartceu_report'@'%' IDENTIFIED BY 'SenhaSegura123!';

-- Conceder apenas SELECT
GRANT SELECT ON smartceu_report_db.* TO 'smartceu_report'@'%';

-- Aplicar mudanças
FLUSH PRIVILEGES;
```

## 🔍 Troubleshooting

### Problema: Sincronização não está executando
```bash
# Verificar se o cron job existe
crontab -l | grep sync_report_db

# Verificar se o serviço cron está rodando
systemctl status cron

# Ver log de erros do cron
tail -n 50 /var/log/syslog | grep CRON
```

### Problema: Erro de permissão no MySQL
```bash
# Verificar privilégios do usuário
mysql -u root -p -e "SHOW GRANTS FOR 'smartceu_user'@'localhost';"

# Se necessário, conceder privilégios
mysql -u root -p -e "GRANT ALL PRIVILEGES ON smartceu_report_db.* TO 'smartceu_user'@'localhost';"
```

### Problema: Espaço em disco insuficiente
```bash
# Verificar espaço disponível
df -h /var/www/smartceu

# Limpar backups antigos manualmente
find /var/www/smartceu/backups/report_sync -name "*.sql.gz" -mtime +7 -delete
```

### Problema: Sincronização muito lenta
```bash
# Verificar tamanho do banco
mysql -u smartceu_user -p'SmartCEU2025)!' -e "
SELECT table_name, 
       ROUND((data_length + index_length) / 1024 / 1024, 2) AS 'Tamanho (MB)'
FROM information_schema.tables
WHERE table_schema = 'smartceu_db'
ORDER BY (data_length + index_length) DESC;
"

# Considerar limpeza de dados antigos
# Exemplo: deletar leituras com mais de 1 ano
```

## 📈 Monitoramento

### Criar Dashboard de Sincronização

Adicionar ao banco de relatórios:

```sql
CREATE TABLE IF NOT EXISTS sync_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sync_date DATETIME NOT NULL,
    duration_seconds INT,
    records_synced INT,
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Modificar `sync_report_db.sh` para registrar histórico.

## 📝 Manutenção

### Rotina Semanal
- [ ] Verificar log de sincronização
- [ ] Validar espaço em disco
- [ ] Comparar contagens entre bancos

### Rotina Mensal
- [ ] Revisar tamanho dos backups
- [ ] Otimizar tabelas manualmente se necessário
- [ ] Verificar performance das consultas

### Rotina Trimestral
- [ ] Avaliar estratégia de retenção de dados
- [ ] Considerar arquivamento de dados antigos
- [ ] Revisar usuários com acesso ao banco

## 🆘 Suporte

Em caso de problemas:

1. Verificar log: `tail -n 100 /var/log/smartceu_report_sync.log`
2. Testar sincronização manual: `bash sync_report_db.sh`
3. Verificar conectividade MySQL: `mysql -u smartceu_user -p`
4. Verificar espaço em disco: `df -h`
5. Verificar processos MySQL: `ps aux | grep mysql`

## 📚 Referências

- [MySQL Replication](https://dev.mysql.com/doc/refman/8.0/en/replication.html)
- [Cron Job Guide](https://man7.org/linux/man-pages/man5/crontab.5.html)
- [MySQL Backup](https://dev.mysql.com/doc/refman/8.0/en/backup-methods.html)

---

**Versão**: 1.0  
**Data**: 2025-10-22  
**Autor**: SmartCEU Team
