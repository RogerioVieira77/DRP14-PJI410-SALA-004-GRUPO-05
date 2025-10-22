# 🚀 Scripts de Instalação e Configuração

Este diretório contém scripts automatizados para facilitar a instalação e configuração do sistema.

---

## 📜 Scripts Disponíveis

### `install_mysql_ubuntu.sh`

Script automatizado para instalar e configurar MySQL 8.0 no Ubuntu Server.

**O que faz:**
- ✅ Atualiza repositórios do sistema
- ✅ Instala MySQL Server 8.0
- ✅ Inicia e habilita o serviço MySQL
- ✅ Cria banco de dados `ceu_tres_pontes_db`
- ✅ Cria usuário `ceu_tres_pontes` com senha segura
- ✅ Configura permissões
- ✅ Testa a conexão

**Como usar:**

```bash
# 1. Dar permissão de execução
chmod +x scripts/install_mysql_ubuntu.sh

# 2. Executar o script
./scripts/install_mysql_ubuntu.sh

# 3. Seguir as instruções na tela
```

**Após a execução:**
- O MySQL estará instalado e rodando
- O banco de dados estará criado
- As credenciais estarão prontas para uso no `.env`

---

## ⚙️ Configuração Manual

Se preferir configurar manualmente, consulte:
- [`docs/MYSQL_SETUP_UBUNTU.md`](../docs/MYSQL_SETUP_UBUNTU.md) - Guia completo passo a passo

---

## 🐛 Troubleshooting

### Script não executa

```bash
# Verificar permissões
ls -l scripts/install_mysql_ubuntu.sh

# Dar permissão
chmod +x scripts/install_mysql_ubuntu.sh
```

### Erro de permissão

```bash
# Executar com sudo
sudo ./scripts/install_mysql_ubuntu.sh
```

### MySQL já instalado

O script detecta se o MySQL já está instalado e pula a etapa de instalação.

---

## 📝 Notas

- **Segurança:** Sempre use senhas fortes em produção
- **Backup:** Configure backups automáticos após instalação
- **Firewall:** Configure UFW se necessário acesso remoto
- **SSL:** Em produção, configure SSL/TLS para conexões

---

**Última atualização:** Outubro 2025
