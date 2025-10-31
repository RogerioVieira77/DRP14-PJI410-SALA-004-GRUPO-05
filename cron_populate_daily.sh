#!/bin/bash
# Script para popular dados diários automaticamente
# Executado via cron todo dia às 00:05

# Diretório do projeto
PROJECT_DIR="/var/www/smartceu/app/backend"
VENV="/var/www/smartceu/venv/bin/python"
LOG_FILE="/var/www/smartceu/logs/cron_populate.log"

# Criar diretório de logs se não existir
mkdir -p /var/www/smartceu/logs

# Registrar início
echo "========================================" >> "$LOG_FILE"
echo "$(date '+%Y-%m-%d %H:%M:%S') - Iniciando população automática" >> "$LOG_FILE"

# Popular leituras de sensores (readings) - 1200 leituras por dia
echo "$(date '+%Y-%m-%d %H:%M:%S') - Populando readings..." >> "$LOG_FILE"
cd "$PROJECT_DIR" && "$VENV" populate_readings_today.py --quantidade 1200 >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ✅ Readings populadas com sucesso" >> "$LOG_FILE"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ❌ Erro ao popular readings" >> "$LOG_FILE"
fi

# Popular dados da piscina (pool_readings)
echo "$(date '+%Y-%m-%d %H:%M:%S') - Populando pool_readings..." >> "$LOG_FILE"
cd "$PROJECT_DIR" && echo "s" | "$VENV" populate_pool_readings.py >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ✅ Pool readings populadas com sucesso" >> "$LOG_FILE"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ❌ Erro ao popular pool_readings" >> "$LOG_FILE"
fi

echo "$(date '+%Y-%m-%d %H:%M:%S') - Processo concluído" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
