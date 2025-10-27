# 🔧 Correção de Nomes de Banco de Dados - Grafana

## Problema Identificado

Os documentos e scripts do Grafana estavam usando o nome incorreto do banco de dados:
- ❌ **Incorreto:** `ceu_tres_pontes`
- ✅ **Correto:** `smartceu_db` (banco principal) e `smartceu_report_db` (banco de relatórios)

---

## Arquivos Corrigidos

### 📚 Documentação

1. **GRAFANA_SETUP_GUIDE.md**
   - ✅ Seção de criação de usuário MySQL
   - ✅ Comandos de teste de conexão
   - ✅ Configuração de Data Source
   - ✅ Comandos de troubleshooting

2. **GRAFANA_QUICKSTART.md**
   - ✅ Comandos SQL de criação de usuário
   - ✅ Configuração de Data Source

3. **GRAFANA_IMPLEMENTATION_SUMMARY.md**
   - ✅ Checklist de preparação

### 🔧 Scripts

1. **configure_grafana_datasource.sh**
   - ✅ Variáveis de configuração
   - ✅ Comandos de criação de usuário
   - ✅ Mensagens de output
   - ✅ Arquivo de credenciais

2. **check_grafana.sh**
   - ✅ Verificação de bancos de dados

---

## Mudanças Principais

### Criação de Usuário MySQL

**Antes:**
```sql
GRANT SELECT ON ceu_tres_pontes.* TO 'grafana_reader'@'localhost';
```

**Depois:**
```sql
GRANT SELECT ON smartceu_db.* TO 'grafana_reader'@'localhost';
GRANT SELECT ON smartceu_report_db.* TO 'grafana_reader'@'localhost';
```

### Configuração do Data Source

**Antes:**
- Database: `ceu_tres_pontes`

**Depois:**
- Database Principal: `smartceu_db`
- Database Relatórios: `smartceu_report_db` (opcional)

### Script configure_grafana_datasource.sh

**Antes:**
```bash
DB_NAME="ceu_tres_pontes"
```

**Depois:**
```bash
DB_NAME="smartceu_db"
DB_REPORT="smartceu_report_db"
```

---

## Impacto nas Queries

As queries SQL nos documentos **NÃO foram alteradas** pois:
- Elas usam nomes de tabelas, não do banco
- O banco é selecionado no Data Source do Grafana
- As tabelas (`readings`, `sensors`, `pool_readings`, etc.) são as mesmas

---

## Próximos Passos

### Para Usuários que Já Instalaram

Se você já executou os scripts antigos:

```bash
# Conectar ao MySQL
sudo mysql -u root -p

# Remover usuário antigo (se existir)
DROP USER IF EXISTS 'grafana_reader'@'localhost';

# Criar novo usuário com permissões corretas
CREATE USER 'grafana_reader'@'localhost' IDENTIFIED BY 'sua_senha_forte';
GRANT SELECT ON smartceu_db.* TO 'grafana_reader'@'localhost';
GRANT SELECT ON smartceu_report_db.* TO 'grafana_reader'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

**No Grafana:**
1. Configuration → Data sources
2. Editar o data source existente
3. Alterar Database para: `smartceu_db`
4. Save & test

### Para Novos Usuários

Simplesmente execute os scripts corrigidos:
```bash
sudo bash configure_grafana_datasource.sh
```

O script agora cria o usuário com permissões nos **dois bancos** automaticamente.

---

## Benefícios da Correção

✅ **Dois bancos disponíveis:** Principal e Relatórios  
✅ **Nomes corretos:** Alinhados com a aplicação  
✅ **Flexibilidade:** Pode criar dashboards usando qualquer um dos bancos  
✅ **Separação:** Consultas de relatórios não impactam o banco principal  

---

## Estrutura dos Bancos

### smartceu_db (Banco Principal)
Usado pela aplicação em produção:
- `sensors` - Sensores cadastrados
- `readings` - Leituras dos sensores
- `users` - Usuários do sistema
- `alerts` - Alertas ativos
- `statistics` - Estatísticas gerais
- Outras tabelas da aplicação

### smartceu_report_db (Banco de Relatórios)
Usado para consultas pesadas e relatórios:
- Replica dos dados principais
- Otimizado para leitura
- Não impacta performance da aplicação
- Atualizado periodicamente

---

## Recomendação de Uso

### Para Dashboards em Tempo Real
✅ Use: **smartceu_db**
- Dados mais atualizados
- Tempo real
- Queries rápidas

### Para Relatórios e Análises Históricas
✅ Use: **smartceu_report_db**
- Não sobrecarrega o banco principal
- Pode ter queries mais pesadas
- Melhor para análises complexas

---

## Configurar Dois Data Sources

Você pode (e deve) configurar **ambos** os bancos no Grafana:

### Data Source 1: Banco Principal
```yaml
Name: SmartCEU DB (Principal)
Host: localhost:3306
Database: smartceu_db
User: grafana_reader
Password: [sua senha]
```

### Data Source 2: Banco de Relatórios
```yaml
Name: SmartCEU Report DB
Host: localhost:3306
Database: smartceu_report_db
User: grafana_reader
Password: [mesma senha]
```

Depois, ao criar painéis, você escolhe qual data source usar!

---

## Status da Correção

| Arquivo | Status | Observação |
|---------|--------|------------|
| GRAFANA_SETUP_GUIDE.md | ✅ Corrigido | Ambos os bancos |
| GRAFANA_QUERIES.md | ✅ OK | Não precisa alteração |
| GRAFANA_QUICKSTART.md | ✅ Corrigido | Ambos os bancos |
| GRAFANA_DASHBOARD_TEMPLATES.md | ✅ OK | Não precisa alteração |
| GRAFANA_IMPLEMENTATION_SUMMARY.md | ✅ Corrigido | Checklist atualizado |
| GRAFANA_INDEX.md | ✅ OK | Não precisa alteração |
| configure_grafana_datasource.sh | ✅ Corrigido | Ambos os bancos |
| install_grafana.sh | ✅ OK | Não precisa alteração |
| configure_grafana_nginx.sh | ✅ OK | Não precisa alteração |
| check_grafana.sh | ✅ Corrigido | Verifica ambos |

---

## Teste de Validação

Execute para validar que tudo está correto:

```bash
# Verificar se os bancos existem
mysql -u root -p -e "SHOW DATABASES LIKE 'smartceu%';"

# Deve mostrar:
# smartceu_db
# smartceu_report_db

# Testar usuário Grafana
mysql -u grafana_reader -p -h localhost smartceu_db -e "SELECT 'OK' as status;"
mysql -u grafana_reader -p -h localhost smartceu_report_db -e "SELECT 'OK' as status;"

# Ambos devem retornar: status = OK
```

---

## Perguntas Frequentes

### P: Por que dois bancos?
**R:** O banco principal é usado pela aplicação. O de relatórios é uma cópia otimizada para não sobrecarregar o sistema em produção com queries pesadas.

### P: Preciso dar acesso aos dois bancos?
**R:** Depende do seu caso:
- **Dashboards em tempo real:** Apenas `smartceu_db`
- **Relatórios complexos:** Adicione também `smartceu_report_db`
- **Recomendado:** Configurar ambos e escolher ao criar painéis

### P: As queries antigas ainda funcionam?
**R:** Sim! As queries usam nomes de tabelas, não do banco. O banco é selecionado no Data Source do Grafana.

### P: Preciso recriar meus dashboards?
**R:** Não! Se você já tem dashboards, apenas:
1. Edite o Data Source
2. Mude o database de `ceu_tres_pontes` para `smartceu_db`
3. Save & test

---

## Suporte

Se tiver problemas após a correção:

1. Execute: `bash check_grafana.sh`
2. Verifique os bancos: `SHOW DATABASES;`
3. Consulte: `docs/GRAFANA_SETUP_GUIDE.md`

---

**Correção aplicada em:** 25 de Outubro de 2025  
**Desenvolvido por:** UNIVESP - DRP14-PJI410-SALA-004-GRUPO-05  
**Sistema:** SmartCEU - CEU Tres Pontes
