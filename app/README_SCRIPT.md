# Script de Reinicialização de Serviços SmartCEU

## 📋 Descrição

Script bash para reiniciar os serviços do SmartCEU (Flask API e Nginx) de forma automatizada e com feedback visual.

## 📂 Localização

```bash
/var/www/smartceu/app/api_service_restart.sh
```

## 🚀 Como Usar

### Uso Básico

```bash
sudo /var/www/smartceu/app/api_service_restart.sh
```

Ou, se estiver na pasta `/var/www/smartceu/app`:

```bash
sudo ./api_service_restart.sh
```

### Criar Alias (Opcional)

Para facilitar o uso, adicione um alias ao seu `.bashrc`:

```bash
echo "alias restart-smartceu='sudo /var/www/smartceu/app/api_service_restart.sh'" >> ~/.bashrc
source ~/.bashrc
```

Depois, você pode usar simplesmente:

```bash
restart-smartceu
```

## ✨ Funcionalidades

### ✅ O que o script faz:

1. **Reinicia o SmartCEU Flask API**
   - Para e inicia o serviço `smartceu-api`
   - Aguarda 2 segundos para inicialização
   - Verifica o status do serviço

2. **Recarrega o Nginx**
   - Recarrega configurações sem derrubar conexões ativas
   - Verifica se está rodando corretamente

3. **Testes de Conectividade**
   - Testa localhost na porta 5001
   - Tenta testar IP público (se disponível)
   - Retorna código HTTP de resposta

4. **Informações Úteis**
   - Mostra URLs de acesso
   - Lista processos em execução
   - Exibe status detalhado dos serviços

### 🎨 Output Colorido

O script usa cores para facilitar a visualização:
- 🔵 **AZUL**: Informações
- 🟢 **VERDE**: Sucesso
- 🟡 **AMARELO**: Avisos
- 🔴 **VERMELHO**: Erros

## 📊 Exemplo de Saída

```
========================================
  SmartCEU - Reiniciar Serviços
========================================

[INFO] Reiniciando SmartCEU Flask API...
[✓] SmartCEU API reiniciada com sucesso
[INFO] Verificando status do SmartCEU API...
[✓] SmartCEU API está ativa
   Status: Active: active (running) since Sat 2025-11-01 15:49:02 -03; 2s ago
[INFO] Recarregando Nginx...
[✓] Nginx recarregado com sucesso
[INFO] Verificando status do Nginx...
[✓] Nginx está ativo
   Status: Active: active (running) since Sat 2025-11-01 07:52:31 -03; 7h ago

========================================
[✓] Todos os serviços foram reiniciados!
========================================

[INFO] Testando conectividade...

[✓] Localhost (5001): OK (200)
[✓] IP Público (82.25.75.88): OK (200)

[INFO] URLs de acesso:
   - Dashboard: http://localhost:5001/smartceu/dashboard/
   - Documentação: http://localhost:5001/smartceu/dashboard/documentacao
   - Mapeamento: http://localhost:5001/smartceu/dashboard/mapeamento-dados.html

[INFO] Processos em execução:
   PID 737: nginx: master process
   PID 36632: /var/www/smartceu/venv/bin/python3 app.py

[✓] Script finalizado com sucesso!
```

## ⚠️ Requisitos

- Permissões de root/sudo
- Serviço `smartceu-api` configurado no systemd
- Serviço `nginx` instalado e configurado

## 🔧 Solução de Problemas

### Erro: "Este script precisa ser executado com sudo ou como root"

**Solução**: Execute com `sudo`:
```bash
sudo ./api_service_restart.sh
```

### Erro: "Falha ao reiniciar SmartCEU API"

**Solução**: Verifique os logs:
```bash
sudo journalctl -u smartceu-api -n 50
```

### Erro: "Falha ao recarregar Nginx"

**Solução**: Teste a configuração do Nginx:
```bash
sudo nginx -t
sudo systemctl status nginx
```

## 📝 Logs

Para ver logs detalhados dos serviços:

### SmartCEU API
```bash
sudo journalctl -u smartceu-api -f
```

### Nginx
```bash
sudo journalctl -u nginx -f
```

## 🔄 Quando Usar

Use este script após:
- Modificar templates HTML
- Atualizar código Python do backend
- Alterar configurações do Nginx
- Atualizar arquivos estáticos
- Deploy de novas funcionalidades

## 📞 Suporte

Para problemas ou dúvidas, verifique:
- Logs do sistema: `/var/log/nginx/` e `journalctl`
- Documentação do projeto
- Status dos serviços: `systemctl status smartceu-api nginx`

---

**Última atualização**: 2025-11-01  
**Versão**: 1.0.0
