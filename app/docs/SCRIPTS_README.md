# 🚀 Scripts de Inicialização - SMARTCEU

## 📋 Scripts Disponíveis

### 1. **start_all_servers.ps1** ⭐ RECOMENDADO
**Inicia o sistema completo**

```powershell
.\start_all_servers.ps1
```

**O que faz:**
- ✅ Inicia servidor HTTP (porta 8000) para as páginas web
- ✅ Inicia API Flask (porta 5000) para o backend
- ✅ Detecta automaticamente o IP da rede
- ✅ Mostra todos os links de acesso
- ✅ Roda ambos servidores em background (Jobs do PowerShell)

**Serviços iniciados:**
- 🌐 Páginas Web: `http://192.168.0.254:8000/smart_ceu.html`
- 🔌 API REST: `http://192.168.0.254:5000`
- 📚 Documentação: `http://192.168.0.254:8000/docs-web/doc_arq.html`
- 🧪 Testes: `http://192.168.0.254:8000/test_page.html`

---

### 2. **start_server.ps1**
**Inicia APENAS a API Flask**

```powershell
.\start_server.ps1
```

**O que faz:**
- ✅ Inicia apenas API Flask (porta 5000)
- ❌ NÃO inicia servidor HTTP (páginas web não funcionarão)

**Use quando:**
- Você só precisa da API
- Vai usar outro servidor web (nginx, apache, etc.)

---

## 🎯 Uso Recomendado

### Iniciar Sistema Completo
```powershell
# Abra PowerShell na pasta do projeto
cd "C:\PI - IV - V1"

# Execute o script completo
.\start_all_servers.ps1
```

### Parar Todos os Servidores
```powershell
# Listar servidores rodando
Get-Job

# Parar todos
Get-Job | Stop-Job
Get-Job | Remove-Job
```

### Ver Logs dos Servidores
```powershell
# Logs do servidor HTTP
Receive-Job -Name HTTPServer

# Logs da API Flask
Receive-Job -Name FlaskAPI
```

---

## 📊 Status dos Servidores

Após iniciar com `start_all_servers.ps1`, você verá:

```
╔════════════════════════════════════════════════════════════╗
║                  🚀 SISTEMA ONLINE!                        ║
╚════════════════════════════════════════════════════════════╝

🌐 PÁGINAS WEB (Porta 8000):
   📍 Página Principal:
      http://192.168.0.254:8000/smart_ceu.html
      http://localhost:8000/smart_ceu.html

   📚 Documentação:
      http://192.168.0.254:8000/docs-web/doc_arq.html

   🧪 Página de Teste:
      http://192.168.0.254:8000/test_page.html

🔌 API REST (Porta 5000):
   ❤️  Health Check:
      http://192.168.0.254:5000/health

   📊 Estatísticas:
      http://192.168.0.254:5000/api/v1/statistics/overview

🔑 CREDENCIAIS:
   Usuário: admin
   Senha:   admin123
```

---

## 🔧 Solução de Problemas

### Erro: "Porta já em uso"
```powershell
# Ver processos usando a porta 8000
Get-NetTCPConnection -LocalPort 8000

# Ver processos usando a porta 5000
Get-NetTCPConnection -LocalPort 5000

# Matar processo específico
Stop-Process -Id [PID]
```

### Servidor não inicia
```powershell
# Verificar se Python está instalado
python --version

# Verificar se venv existe
Test-Path "C:\PI - IV - V1\venv"

# Reinstalar dependências
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Não consigo acessar de outro dispositivo
```powershell
# Liberar portas no firewall
New-NetFirewallRule -DisplayName "SMARTCEU HTTP" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
New-NetFirewallRule -DisplayName "SMARTCEU API" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow

# Verificar IP da máquina
ipconfig
```

---

## 📱 Acesso de Outros Dispositivos

1. **Conecte o dispositivo à mesma rede Wi-Fi**
2. **Abra o navegador**
3. **Digite:** `http://192.168.0.254:8000/smart_ceu.html`

Substitua `192.168.0.254` pelo IP mostrado ao executar o script.

---

## 🎓 Exemplos de Uso

### Desenvolvimento Local
```powershell
# Inicia tudo localmente
.\start_all_servers.ps1

# Acessa no navegador
start http://localhost:8000/smart_ceu.html
```

### Demonstração em Rede
```powershell
# Inicia sistema completo
.\start_all_servers.ps1

# Compartilha o link com outros (mesmo Wi-Fi):
# http://192.168.0.254:8000/smart_ceu.html
```

### Apenas Backend (para testes de API)
```powershell
# Inicia só a API
.\start_server.ps1

# Testa com curl ou Postman
curl http://localhost:5000/health
```

---

## 📚 Documentação Adicional

- **LINKS_ACESSO_REDE.md**: Todos os endpoints e links de acesso
- **README.md**: Documentação geral do projeto
- **docs-web/**: Documentação técnica completa

---

**Última atualização:** 20 de Outubro de 2025  
**Versão:** 2.0.0 - Sistema Completo
