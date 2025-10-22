# ============================================================
# SMARTCEU - SISTEMA COMPLETO
# Inicializa TODOS os servidores do sistema
# ============================================================

Write-Host "`n╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║           SMARTCEU - INICIANDO SISTEMA COMPLETO           ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Ir para o diretório do projeto
Set-Location "C:\PI - IV - V1"

# Obter o IP da máquina na rede
$ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -notlike "127.*" -and $_.PrefixOrigin -eq "Dhcp"}).IPAddress

if (-not $ip) {
    $ip = "192.168.0.254"
    Write-Host "⚠️  IP não detectado automaticamente, usando: $ip" -ForegroundColor Yellow
}

Write-Host "📱 IP na rede local: $ip`n" -ForegroundColor Green

# ============================================================
# SERVIDOR 1: HTTP Server (Páginas Web - Porta 8000)
# ============================================================

Write-Host "[1/3] Iniciando Servidor HTTP (Páginas Web)..." -ForegroundColor Yellow
Write-Host "      Porta: 8000" -ForegroundColor Gray

Start-Job -Name "HTTPServer" -ScriptBlock {
    Set-Location "C:\PI - IV - V1"
    python -m http.server 8000
} | Out-Null

Start-Sleep -Seconds 2

# Verificar se o servidor HTTP está rodando
$httpRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000" -TimeoutSec 2 -ErrorAction SilentlyContinue
    $httpRunning = $true
} catch {
    $httpRunning = $false
}

if ($httpRunning) {
    Write-Host "      ✅ Servidor HTTP iniciado com sucesso!`n" -ForegroundColor Green
} else {
    Write-Host "      ⚠️  Servidor HTTP pode não ter iniciado corretamente`n" -ForegroundColor Yellow
}

# ============================================================
# SERVIDOR 2: Flask API (Backend - Porta 5000)
# ============================================================

Write-Host "[2/3] Iniciando API Flask (Backend)..." -ForegroundColor Yellow
Write-Host "      Porta: 5000" -ForegroundColor Gray

Start-Job -Name "FlaskAPI" -ScriptBlock {
    Set-Location "C:\PI - IV - V1"
    & .\venv\Scripts\Activate.ps1
    Set-Location "backend"
    python app.py
} | Out-Null

Start-Sleep -Seconds 3

# Verificar se a API Flask está rodando
$flaskRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/health" -TimeoutSec 3 -ErrorAction SilentlyContinue
    $flaskRunning = $true
} catch {
    $flaskRunning = $false
}

if ($flaskRunning) {
    Write-Host "      ✅ API Flask iniciada com sucesso!`n" -ForegroundColor Green
} else {
    Write-Host "      ⚠️  API Flask pode não ter iniciado corretamente`n" -ForegroundColor Yellow
}

# ============================================================
# SERVIDOR 3: Pool Simulators (Sensores da Piscina)
# ============================================================

Write-Host "[3/3] Iniciando Simuladores da Piscina..." -ForegroundColor Yellow
Write-Host "      Intervalo: 30 segundos" -ForegroundColor Gray

Start-Job -Name "PoolSimulators" -ScriptBlock {
    Set-Location "C:\PI - IV - V1"
    & .\venv\Scripts\Activate.ps1
    Set-Location "backend"
    python pool_simulators.py
} | Out-Null

Start-Sleep -Seconds 2

Write-Host "      ✅ Simuladores da piscina iniciados!`n" -ForegroundColor Green

# ============================================================
# RESUMO DE ACESSO
# ============================================================

Write-Host "`n╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                  🚀 SISTEMA ONLINE!                        ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝`n" -ForegroundColor Green

Write-Host "🌐 PÁGINAS WEB (Porta 8000):" -ForegroundColor Cyan
Write-Host "   📍 Página Principal:" -ForegroundColor White
Write-Host "      http://${ip}:8000/smart_ceu.html" -ForegroundColor Yellow
Write-Host "      http://localhost:8000/smart_ceu.html`n" -ForegroundColor Gray

Write-Host "   📚 Documentação:" -ForegroundColor White
Write-Host "      http://${ip}:8000/docs-web/doc_arq.html" -ForegroundColor Yellow
Write-Host "      http://localhost:8000/docs-web/doc_arq.html`n" -ForegroundColor Gray

Write-Host "   🧪 Página de Teste:" -ForegroundColor White
Write-Host "      http://${ip}:8000/test_page.html" -ForegroundColor Yellow
Write-Host "      http://localhost:8000/test_page.html`n" -ForegroundColor Gray

Write-Host "   🏊 Monitoramento da Piscina:" -ForegroundColor White
Write-Host "      http://${ip}:8000/monitoramento_piscina.html" -ForegroundColor Yellow
Write-Host "      http://localhost:8000/monitoramento_piscina.html`n" -ForegroundColor Gray

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray

Write-Host "`n🔌 API REST (Porta 5000):" -ForegroundColor Cyan
Write-Host "   ❤️  Health Check:" -ForegroundColor White
Write-Host "      http://${ip}:5000/health" -ForegroundColor Yellow
Write-Host "      http://localhost:5000/health`n" -ForegroundColor Gray

Write-Host "   📊 Estatísticas:" -ForegroundColor White
Write-Host "      http://${ip}:5000/api/v1/statistics/overview" -ForegroundColor Yellow
Write-Host "      http://localhost:5000/api/v1/statistics/overview`n" -ForegroundColor Gray

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray

Write-Host "`n🔑 CREDENCIAIS DE ACESSO:" -ForegroundColor Cyan
Write-Host "   Usuário: admin" -ForegroundColor White
Write-Host "   Senha:   admin123`n" -ForegroundColor White

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray

Write-Host "`n📱 COMPARTILHAR COM OUTROS DISPOSITIVOS:" -ForegroundColor Yellow
Write-Host "   1. Conecte o dispositivo à mesma rede Wi-Fi" -ForegroundColor White
Write-Host "   2. Acesse: http://${ip}:8000/smart_ceu.html`n" -ForegroundColor Green

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray

Write-Host "`n⚙️  GERENCIAR SERVIDORES:" -ForegroundColor Cyan
Write-Host "   📋 Ver status:       Get-Job" -ForegroundColor White
Write-Host "   🛑 Parar todos:      Get-Job | Stop-Job; Get-Job | Remove-Job" -ForegroundColor White
Write-Host "   📊 Ver logs HTTP:    Receive-Job -Name HTTPServer" -ForegroundColor White
Write-Host "   📊 Ver logs API:     Receive-Job -Name FlaskAPI" -ForegroundColor White
Write-Host "   🏊 Ver logs Piscina: Receive-Job -Name PoolSimulators`n" -ForegroundColor White

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray

Write-Host "`n🎯 LINK PRINCIPAL PARA ABRIR:" -ForegroundColor Green
Write-Host "   http://${ip}:8000/smart_ceu.html`n" -ForegroundColor Yellow -BackgroundColor DarkBlue

Write-Host "Pressione CTRL+C e depois execute: Get-Job | Stop-Job" -ForegroundColor Yellow
Write-Host "para parar todos os servidores.`n" -ForegroundColor Yellow

# Manter o PowerShell aberto e mostrando os jobs
Write-Host "Servidores rodando em background..." -ForegroundColor Green
Write-Host "Status dos servidores:`n" -ForegroundColor Cyan

# Loop para manter o script rodando e mostrar status
while ($true) {
    Start-Sleep -Seconds 10
    
    # Verificar status dos jobs
    $jobs = Get-Job
    $httpJob = $jobs | Where-Object { $_.Name -eq "HTTPServer" }
    $flaskJob = $jobs | Where-Object { $_.Name -eq "FlaskAPI" }
    $poolJob = $jobs | Where-Object { $_.Name -eq "PoolSimulators" }
    
    if ($httpJob.State -ne "Running" -or $flaskJob.State -ne "Running" -or $poolJob.State -ne "Running") {
        Write-Host "`n⚠️  ATENÇÃO: Um ou mais servidores pararam!" -ForegroundColor Red
        Write-Host "HTTP Server:      $($httpJob.State)" -ForegroundColor Yellow
        Write-Host "Flask API:        $($flaskJob.State)" -ForegroundColor Yellow
        Write-Host "Pool Simulators:  $($poolJob.State)" -ForegroundColor Yellow
        break
    }
}
