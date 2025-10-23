#!/bin/bash
# Backup automático do banco SmartCEU

BACKUP_DIR="/var/www/smartceu/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/smartceu_${DATE}.sql.gz"

# Criar diretório se não existir
mkdir -p ${BACKUP_DIR}

# Remover backups com mais de 7 dias
find ${BACKUP_DIR} -name "smartceu_*.sql.gz" -mtime +7 -delete

# Fazer backup (sem tablespaces para evitar warning)
mysqldump -u smartceu_user -p'SmartCEU2025)!' --no-tablespaces smartceu_db | gzip > ${BACKUP_FILE}

echo "Backup criado: ${BACKUP_FILE}"
