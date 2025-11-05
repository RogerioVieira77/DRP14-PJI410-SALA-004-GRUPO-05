#!/bin/bash

###############################################################################
# Script de Reinicialização dos Serviços SmartCEU
# Descrição: Reinicia os serviços Flask API e Nginx
# Autor: Sistema SmartCEU
# Data: 2025-11-01
###############################################################################

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Cabeçalho
echo ""
echo "========================================"
echo "  SmartCEU - Reiniciar Serviços"
echo "========================================"
echo ""

# Verificar se está rodando como root ou com sudo
if [ "$EUID" -ne 0 ]; then 
    print_error "Este script precisa ser executado com sudo ou como root"
    echo "Uso: sudo $0"
    exit 1
fi

# Reiniciar SmartCEU API (Flask)
print_info "Reiniciando SmartCEU Flask API..."
if systemctl restart smartceu-api; then
    print_success "SmartCEU API reiniciada com sucesso"
else
    print_error "Falha ao reiniciar SmartCEU API"
    exit 1
fi

# Aguardar alguns segundos para o serviço inicializar
sleep 2

# Verificar status do SmartCEU API
print_info "Verificando status do SmartCEU API..."
if systemctl is-active --quiet smartceu-api; then
    print_success "SmartCEU API está ativa"
    API_STATUS=$(systemctl status smartceu-api --no-pager | grep "Active:" | sed 's/^[[:space:]]*//')
    echo "   Status: $API_STATUS"
else
    print_error "SmartCEU API não está ativa!"
    echo ""
    print_warning "Mostrando últimas 10 linhas do log:"
    journalctl -u smartceu-api --no-pager -n 10
    exit 1
fi

# Recarregar Nginx
print_info "Recarregando Nginx..."
if systemctl reload nginx; then
    print_success "Nginx recarregado com sucesso"
else
    print_error "Falha ao recarregar Nginx"
    exit 1
fi

# Verificar status do Nginx
print_info "Verificando status do Nginx..."
if systemctl is-active --quiet nginx; then
    print_success "Nginx está ativo"
    NGINX_STATUS=$(systemctl status nginx --no-pager | grep "Active:" | sed 's/^[[:space:]]*//')
    echo "   Status: $NGINX_STATUS"
else
    print_error "Nginx não está ativo!"
    exit 1
fi

echo ""
echo "========================================"
print_success "Todos os serviços foram reiniciados!"
echo "========================================"
echo ""

# Testes de conectividade
print_info "Testando conectividade..."
echo ""

# Teste localhost
LOCALHOST_TEST=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/smartceu/dashboard/ 2>/dev/null)
if [ "$LOCALHOST_TEST" = "200" ]; then
    print_success "Localhost (5001): OK ($LOCALHOST_TEST)"
else
    print_warning "Localhost (5001): FALHOU ($LOCALHOST_TEST)"
fi

# Teste IP público (se disponível)
PUBLIC_IP=$(curl -s ifconfig.me 2>/dev/null)
if [ ! -z "$PUBLIC_IP" ]; then
    PUBLIC_TEST=$(curl -s -o /dev/null -w "%{http_code}" http://$PUBLIC_IP/smartceu/dashboard/ 2>/dev/null)
    if [ "$PUBLIC_TEST" = "200" ]; then
        print_success "IP Público ($PUBLIC_IP): OK ($PUBLIC_TEST)"
    else
        print_warning "IP Público ($PUBLIC_IP): FALHOU ($PUBLIC_TEST)"
    fi
fi

echo ""
print_info "URLs de acesso:"
echo "   - Dashboard: http://localhost:5001/smartceu/dashboard/"
echo "   - Documentação: http://localhost:5001/smartceu/dashboard/documentacao"
echo "   - Mapeamento: http://localhost:5001/smartceu/dashboard/mapeamento-dados.html"
echo ""

# Mostrar processos
print_info "Processos em execução:"
ps aux | grep -E "(python3.*app.py|nginx: master)" | grep -v grep | awk '{print "   PID " $2 ": " $11 " " $12 " " $13}'
echo ""

print_success "Script finalizado com sucesso!"
echo ""
