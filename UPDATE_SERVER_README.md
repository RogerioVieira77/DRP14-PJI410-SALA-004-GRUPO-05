# 🔄 Script de Atualização do Servidor SmartCEU

## 📋 Descrição

Script automatizado para atualizar o servidor SmartCEU com as últimas mudanças do GitHub e reiniciar todos os serviços necessários.

## 🎯 O que o script faz

### 1. **Backup de Segurança**
- Cria backup do código atual
- Faz backup do banco de dados MySQL

### 2. **Atualização do Código**
- Descarta alterações locais não commitadas
- Faz pull do repositório GitHub (branch main)
- Registra número de arquivos atualizados

### 3. **Dependências Python**
- Verifica e atualiza pacotes Python (se necessário)

### 4. **Ajuste de Permissões**
- Configura proprietário www-data
- Ajusta permissões de arquivos e diretórios
- Torna scripts executáveis

### 5. **Reinício de Serviços**
- ✓ MySQL
- ✓ SmartCEU (Flask/Gunicorn)
- ✓ Nginx
- ✓ Mosquitto (MQTT Broker)

### 6. **Verificação de Saúde**
- Testa endpoint `/health` da API
- Verifica resposta do Nginx

### 7. **Limpeza**
- Remove cache Python
- Limpa logs antigos (>7 dias)

## 🚀 Como Usar

### Método 1: Executar diretamente no servidor

```bash
# Conectar ao servidor e navegar até a pasta
ssh root@82.25.75.88 -t "cd /var/www/smartceu && bash"

# Executar o script
sudo bash update_server.sh
```

### Método 2: Comando único via SSH (do Windows)

```powershell
ssh root@82.25.75.88 "cd /var/www/smartceu && sudo bash update_server.sh"
```

### Método 3: Após fazer pull manual

```bash
cd /var/www/smartceu
git pull origin main
sudo bash update_server.sh
```

## 📊 Exemplo de Saída

```
═══════════════════════════════════════════════════════════════
  ATUALIZAÇÃO DO SERVIDOR SMARTCEU
═══════════════════════════════════════════════════════════════

▶ 1. Criando backup de segurança...
✓ Backup do código criado em: /var/backups/smartceu_20251022_183000
✓ Backup do banco de dados MySQL criado

▶ 2. Atualizando código do GitHub...
✓ Alterações locais descartadas
✓ Código atualizado do GitHub (branch: main)

▶ 3. Verificando dependências Python...
✓ Dependências Python atualizadas

▶ 4. Ajustando permissões dos arquivos...
✓ Proprietário ajustado para www-data
✓ Permissões de diretórios ajustadas
✓ Scripts shell tornados executáveis

▶ 5. Reiniciando serviços da aplicação...
✓ MySQL reiniciado
✓ MySQL está ativo
✓ SmartCEU (Flask/Gunicorn) reiniciado
✓ SmartCEU está ativo
✓ Nginx reiniciado
✓ Nginx está ativo
✓ Mosquitto (MQTT) reiniciado
✓ Mosquitto está ativo

▶ 6. Verificando saúde da aplicação...
✓ API Health check OK (HTTP 200)
✓ Nginx respondendo OK (HTTP 200)

▶ 7. Limpeza de arquivos temporários...
✓ Cache Python limpo
✓ Logs antigos removidos

═══════════════════════════════════════════════════════════════
  RESUMO DA ATUALIZAÇÃO
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│  Data/Hora: 2025-10-22 18:30:00                             │
│  Diretório: /var/www/smartceu                               │
│  Branch: main                                               │
│  Arquivos atualizados: 11                                   │
└─────────────────────────────────────────────────────────────┘

Status dos Serviços:
  ✓ MySQL:      active
  ✓ SmartCEU:   active
  ✓ Nginx:      active
  ✓ Mosquitto:  active

Resumo de Operações:
  ✓ Backup do código criado
  ✓ Backup do banco de dados MySQL criado
  ✓ Alterações locais descartadas
  ✓ Código atualizado do GitHub
  [... mais operações ...]

┌─────────────────────────────────────────────────────────────┐
│  STATUS: ATUALIZAÇÃO CONCLUÍDA COM SUCESSO! ✓               │
│                                                             │
│  ✓ Operações bem-sucedidas: 18                             │
│  ✗ Operações com erro: 0                                   │
│  ⟳ Serviços reiniciados: 4                                 │
└─────────────────────────────────────────────────────────────┘

URLs de Acesso:
  • Dashboard:  http://82.25.75.88/smartceu
  • Pool:       http://82.25.75.88/smartceu/pool
  • Test Page:  http://82.25.75.88/smartceu/test_page.html
  • API Docs:   http://82.25.75.88/smartceu/doc_arq.html
  • API Health: http://82.25.75.88/health

Log completo salvo em: /var/log/smartceu_update.log
```

## 📝 Logs

O script gera logs detalhados em:
```
/var/log/smartceu_update.log
```

Para visualizar:
```bash
tail -f /var/log/smartceu_update.log
```

## ⚠️ Requisitos

- Acesso root ou sudo no servidor
- Git configurado com SSH ou HTTPS
- Todos os serviços devem estar instalados:
  - MySQL
  - Nginx
  - Python/Flask (serviço smartceu)
  - Mosquitto (opcional)

## 🔧 Troubleshooting

### Erro: "Diretório da aplicação não encontrado"
```bash
# Verificar se o caminho está correto
ls -la /var/www/smartceu
```

### Erro: "Serviço não encontrado"
```bash
# Verificar serviços instalados
systemctl list-units --type=service | grep -E 'mysql|nginx|smartceu|mosquitto'
```

### Erro de permissão Git
```bash
# Adicionar diretório como seguro
git config --global --add safe.directory /var/www/smartceu
```

## 🔐 Segurança

- O script requer privilégios de root/sudo
- Faz backup automático antes de atualizar
- Descarta alterações locais (use com cuidado!)
- Registra todas as operações em log

## 📞 Suporte

Para problemas ou dúvidas, consulte:
- Log do script: `/var/log/smartceu_update.log`
- Logs do sistema: `/var/log/nginx/`, `/var/log/mysql/`
- Status dos serviços: `systemctl status <serviço>`

## 🎯 Automação

Para executar automaticamente em horários agendados:

```bash
# Editar crontab
sudo crontab -e

# Executar todo dia às 3h da manhã
0 3 * * * cd /var/www/smartceu && bash update_server.sh >> /var/log/smartceu_cron.log 2>&1
```

---

**Última atualização:** 22/10/2025
**Versão:** 1.0
