#!/bin/bash

# ============================================
# Script de Instalação MySQL 8.0 - Ubuntu
# Sistema CEU Tres Pontes
# ============================================

set -e  # Parar em caso de erro

echo "=========================================="
echo "  Instalação MySQL 8.0 - CEU Tres Pontes"
echo "=========================================="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para printar com cor
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Verificar se é root ou tem sudo
if [[ $EUID -ne 0 ]] && ! sudo -v; then
   print_error "Este script precisa de permissões sudo"
   exit 1
fi

print_info "Iniciando instalação do MySQL 8.0..."
echo ""

# Passo 1: Atualizar repositórios
echo "Passo 1: Atualizando repositórios..."
sudo apt update -qq
print_success "Repositórios atualizados"
echo ""

# Passo 2: Instalar MySQL Server
echo "Passo 2: Instalando MySQL Server..."
if dpkg -l | grep -q mysql-server; then
    print_info "MySQL já está instalado"
    mysql --version
else
    sudo DEBIAN_FRONTEND=noninteractive apt install -y mysql-server
    print_success "MySQL Server instalado"
    mysql --version
fi
echo ""

# Passo 3: Iniciar e habilitar serviço
echo "Passo 3: Configurando serviço MySQL..."
sudo systemctl start mysql
sudo systemctl enable mysql
print_success "Serviço MySQL iniciado e habilitado"
echo ""

# Passo 4: Verificar status
echo "Passo 4: Verificando status..."
if sudo systemctl is-active --quiet mysql; then
    print_success "MySQL está rodando"
else
    print_error "MySQL não está rodando"
    exit 1
fi
echo ""

# Passo 5: Solicitar senha do root MySQL
echo "=========================================="
echo "  Configuração do Banco de Dados"
echo "=========================================="
echo ""

read -sp "Digite a senha para o usuário 'ceu_tres_pontes' do MySQL: " DB_PASSWORD
echo ""
read -sp "Confirme a senha: " DB_PASSWORD_CONFIRM
echo ""

if [ "$DB_PASSWORD" != "$DB_PASSWORD_CONFIRM" ]; then
    print_error "As senhas não coincidem!"
    exit 1
fi

if [ -z "$DB_PASSWORD" ]; then
    print_error "A senha não pode ser vazia!"
    exit 1
fi

print_success "Senha definida"
echo ""

# Passo 6: Criar banco e usuário
echo "Passo 5: Criando banco de dados e usuário..."

sudo mysql -e "CREATE DATABASE IF NOT EXISTS ceu_tres_pontes_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>/dev/null || true
print_success "Banco de dados 'ceu_tres_pontes_db' criado"

sudo mysql -e "CREATE USER IF NOT EXISTS 'ceu_tres_pontes'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';" 2>/dev/null || true
sudo mysql -e "GRANT ALL PRIVILEGES ON ceu_tres_pontes_db.* TO 'ceu_tres_pontes'@'localhost';" 2>/dev/null
sudo mysql -e "FLUSH PRIVILEGES;" 2>/dev/null
print_success "Usuário 'ceu_tres_pontes' criado e permissões configuradas"
echo ""

# Passo 7: Testar conexão
echo "Passo 6: Testando conexão..."
if mysql -u ceu_tres_pontes -p"${DB_PASSWORD}" -e "USE ceu_tres_pontes_db; SELECT 'Conexão OK' AS status;" 2>/dev/null; then
    print_success "Conexão com banco de dados funcionando"
else
    print_error "Erro ao conectar ao banco de dados"
    exit 1
fi
echo ""

# Passo 8: Criar arquivo .env (se não existir)
echo "Passo 7: Criando arquivo de configuração..."

ENV_FILE="/caminho/do/projeto/backend/.env"
ENV_EXAMPLE="/caminho/do/projeto/backend/.env.example"

# Você pode ajustar o caminho acima para o caminho real do seu projeto
# Por exemplo: ENV_FILE="/home/usuario/PI-IV-V1/backend/.env"

print_info "Arquivo .env deve ser criado manualmente em: backend/.env"
echo ""
echo "Conteúdo sugerido:"
echo "----------------------------------------"
echo "DB_HOST=localhost"
echo "DB_PORT=3306"
echo "DB_USER=ceu_tres_pontes"
echo "DB_PASSWORD=${DB_PASSWORD}"
echo "DB_NAME=ceu_tres_pontes_db"
echo "----------------------------------------"
echo ""

# Passo 9: Informações finais
echo "=========================================="
echo "  ✅ Instalação Concluída com Sucesso!"
echo "=========================================="
echo ""
echo "Informações do MySQL:"
echo "  • Serviço: mysql"
echo "  • Status: $(sudo systemctl is-active mysql)"
echo "  • Versão: $(mysql --version | awk '{print $5}' | sed 's/,//')"
echo ""
echo "Banco de Dados:"
echo "  • Nome: ceu_tres_pontes_db"
echo "  • Usuário: ceu_tres_pontes"
echo "  • Host: localhost"
echo "  • Porta: 3306"
echo ""
echo "Próximos passos:"
echo "  1. Configure o arquivo .env no backend"
echo "  2. Execute: flask init-db"
echo "  3. Execute: flask seed-db"
echo "  4. Inicie o backend: python app.py"
echo ""
echo "Comandos úteis:"
echo "  • Conectar: mysql -u ceu_tres_pontes -p"
echo "  • Status: sudo systemctl status mysql"
echo "  • Logs: sudo tail -f /var/log/mysql/error.log"
echo ""
print_success "MySQL configurado e pronto para uso!"
echo ""
