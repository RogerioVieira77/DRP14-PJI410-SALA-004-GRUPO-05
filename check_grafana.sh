#!/bin/bash
###############################################################################
# Script de Verificação da Instalação Grafana
# CEU Tres Pontes - Sistema de Controle de Acesso
# 
# Este script verifica se o Grafana está instalado e configurado corretamente
# 
# Uso: bash check_grafana.sh
###############################################################################

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

check_pass=0
check_fail=0

log_check() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $2"
        ((check_pass++))
    else
        echo -e "${RED}✗${NC} $2"
        ((check_fail++))
    fi
}

echo "=============================================="
echo "  Verificação Grafana - CEU Tres Pontes"
echo "=============================================="
echo ""

# 1. Verificar se Grafana está instalado
echo "📦 Verificando instalação..."
if command -v grafana-server &> /dev/null; then
    VERSION=$(grafana-server -v | head -n 1)
    log_check 0 "Grafana instalado: $VERSION"
else
    log_check 1 "Grafana não está instalado"
fi

# 2. Verificar serviço
echo ""
echo "🔧 Verificando serviço..."
if systemctl is-active --quiet grafana-server; then
    log_check 0 "Serviço Grafana está rodando"
else
    log_check 1 "Serviço Grafana NÃO está rodando"
fi

if systemctl is-enabled --quiet grafana-server; then
    log_check 0 "Serviço configurado para iniciar no boot"
else
    log_check 1 "Serviço NÃO está configurado para boot"
fi

# 3. Verificar porta
echo ""
echo "🌐 Verificando conectividade..."
if netstat -tulpn 2>/dev/null | grep -q ":3000" || ss -tulpn 2>/dev/null | grep -q ":3000"; then
    log_check 0 "Porta 3000 está escutando"
else
    log_check 1 "Porta 3000 NÃO está escutando"
fi

# Testar conexão HTTP
if curl -s http://localhost:3000/api/health &> /dev/null; then
    log_check 0 "API Grafana respondendo"
else
    log_check 1 "API Grafana NÃO está respondendo"
fi

# 4. Verificar arquivos e diretórios
echo ""
echo "📁 Verificando arquivos..."
if [ -f /etc/grafana/grafana.ini ]; then
    log_check 0 "Arquivo de configuração existe"
else
    log_check 1 "Arquivo de configuração NÃO encontrado"
fi

if [ -d /var/lib/grafana ]; then
    log_check 0 "Diretório de dados existe"
else
    log_check 1 "Diretório de dados NÃO encontrado"
fi

if [ -d /var/log/grafana ]; then
    log_check 0 "Diretório de logs existe"
else
    log_check 1 "Diretório de logs NÃO encontrado"
fi

# 5. Verificar permissões
echo ""
echo "🔐 Verificando permissões..."
GRAFANA_USER=$(stat -c '%U' /var/lib/grafana 2>/dev/null)
if [ "$GRAFANA_USER" = "grafana" ]; then
    log_check 0 "Permissões do diretório de dados corretas"
else
    log_check 1 "Permissões do diretório de dados incorretas (owner: $GRAFANA_USER)"
fi

# 6. Verificar MySQL
echo ""
echo "🗄️  Verificando MySQL..."
if command -v mysql &> /dev/null; then
    log_check 0 "MySQL instalado"
    
    # Verificar banco de dados principal
    if mysql -e "USE smartceu_db;" 2>/dev/null; then
        log_check 0 "Banco de dados 'smartceu_db' existe"
    else
        log_check 1 "Banco de dados 'smartceu_db' NÃO encontrado"
    fi
    
    # Verificar banco de dados de relatórios
    if mysql -e "USE smartceu_report_db;" 2>/dev/null; then
        log_check 0 "Banco de dados 'smartceu_report_db' existe"
    else
        log_check 1 "Banco de dados 'smartceu_report_db' NÃO encontrado"
    fi
    
    # Verificar usuário Grafana
    if [ -f /root/.grafana_mysql_credentials ]; then
        log_check 0 "Credenciais MySQL para Grafana encontradas"
    else
        log_check 1 "Credenciais MySQL NÃO encontradas"
    fi
else
    log_check 1 "MySQL não está instalado"
fi

# 7. Verificar Nginx
echo ""
echo "🌍 Verificando Nginx..."
if command -v nginx &> /dev/null; then
    log_check 0 "Nginx instalado"
    
    if [ -f /etc/nginx/sites-available/grafana ]; then
        log_check 0 "Configuração Nginx para Grafana existe"
        
        if [ -L /etc/nginx/sites-enabled/grafana ]; then
            log_check 0 "Configuração Nginx ativada"
        else
            log_check 1 "Configuração Nginx NÃO está ativada"
        fi
    else
        log_check 1 "Configuração Nginx para Grafana NÃO encontrada"
    fi
    
    if systemctl is-active --quiet nginx; then
        log_check 0 "Nginx está rodando"
    else
        log_check 1 "Nginx NÃO está rodando"
    fi
else
    log_check 1 "Nginx não está instalado"
fi

# 8. Verificar firewall
echo ""
echo "🔥 Verificando firewall..."
if command -v ufw &> /dev/null; then
    if ufw status | grep -q "Status: active"; then
        log_check 0 "UFW está ativo"
        
        if ufw status | grep -q "3000"; then
            log_check 0 "Porta 3000 permitida no UFW"
        else
            log_check 1 "Porta 3000 NÃO permitida no UFW"
        fi
    else
        log_check 0 "UFW desativado (firewall não está ativo)"
    fi
else
    log_check 0 "UFW não instalado (sem firewall ativo)"
fi

# 9. Verificar logs recentes
echo ""
echo "📋 Verificando logs..."
if [ -f /var/log/grafana/grafana.log ]; then
    ERROR_COUNT=$(grep -i "error" /var/log/grafana/grafana.log 2>/dev/null | tail -n 20 | wc -l)
    if [ "$ERROR_COUNT" -eq 0 ]; then
        log_check 0 "Sem erros recentes nos logs"
    else
        log_check 1 "Encontrados $ERROR_COUNT erros recentes nos logs"
    fi
else
    log_check 1 "Arquivo de log NÃO encontrado"
fi

# 10. Verificar backup
echo ""
echo "💾 Verificando backup..."
if [ -d /backup/grafana ]; then
    log_check 0 "Diretório de backup existe"
    
    BACKUP_COUNT=$(ls -1 /backup/grafana/*.db 2>/dev/null | wc -l)
    if [ "$BACKUP_COUNT" -gt 0 ]; then
        log_check 0 "Encontrados $BACKUP_COUNT backups"
    else
        log_check 1 "Nenhum backup encontrado"
    fi
else
    log_check 1 "Diretório de backup NÃO existe"
fi

# Resumo
echo ""
echo "=============================================="
echo "  Resumo da Verificação"
echo "=============================================="
echo ""
echo -e "${GREEN}Aprovado:${NC} $check_pass"
echo -e "${RED}Falhou:${NC} $check_fail"
echo ""

if [ $check_fail -eq 0 ]; then
    echo -e "${GREEN}✓ Tudo está funcionando perfeitamente!${NC}"
    echo ""
    echo "🌐 Acesse o Grafana em:"
    echo "   http://$(hostname -I | awk '{print $1}'):3000"
    
    # Verificar se tem Nginx configurado
    if [ -f /etc/nginx/sites-enabled/grafana ]; then
        DOMAIN=$(grep "server_name" /etc/nginx/sites-available/grafana | head -n 1 | awk '{print $2}' | sed 's/;//g')
        if [ -n "$DOMAIN" ]; then
            echo "   ou"
            if [ -d /etc/letsencrypt/live ]; then
                echo "   https://$DOMAIN"
            else
                echo "   http://$DOMAIN"
            fi
        fi
    fi
    
    echo ""
    echo "📚 Documentação:"
    echo "   • Guia completo: docs/GRAFANA_SETUP_GUIDE.md"
    echo "   • Queries prontas: docs/GRAFANA_QUERIES.md"
    echo "   • Guia rápido: docs/GRAFANA_QUICKSTART.md"
    
    exit 0
elif [ $check_fail -lt 5 ]; then
    echo -e "${YELLOW}⚠ Alguns itens precisam de atenção${NC}"
    echo ""
    echo "Verifique os itens marcados com ✗ acima"
    echo "Consulte a documentação em docs/GRAFANA_SETUP_GUIDE.md"
    exit 1
else
    echo -e "${RED}✗ Vários problemas detectados!${NC}"
    echo ""
    echo "Recomendações:"
    echo "1. Execute o script de instalação: sudo bash install_grafana.sh"
    echo "2. Configure o MySQL: sudo bash configure_grafana_datasource.sh"
    echo "3. Configure o Nginx: sudo bash configure_grafana_nginx.sh"
    echo "4. Consulte a documentação: docs/GRAFANA_SETUP_GUIDE.md"
    exit 2
fi
