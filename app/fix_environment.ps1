# Script para Corrigir Ambiente e Executar Testes
# CEU Tres Pontes - Correção Automática

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "CORREÇÃO AUTOMÁTICA DO AMBIENTE" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

# Verificar se venv existe
if (-Not (Test-Path ".\venv\Scripts\Activate.ps1")) {
    Write-Host "❌ Ambiente virtual não encontrado!" -ForegroundColor Red
    Write-Host "Execute: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Ambiente virtual encontrado" -ForegroundColor Green

# Ativar ambiente virtual
Write-Host "`n[1/4] Ativando ambiente virtual..." -ForegroundColor Cyan
& .\venv\Scripts\Activate.ps1

# Verificar ativação
$pythonPath = python -c "import sys; print(sys.executable)"
if ($pythonPath -like "*venv*") {
    Write-Host "✅ Ambiente virtual ativado: $pythonPath" -ForegroundColor Green
} else {
    Write-Host "⚠️  Aviso: Python pode não estar usando venv" -ForegroundColor Yellow
}

# Instalar dependências faltantes
Write-Host "`n[2/4] Instalando dependências faltantes..." -ForegroundColor Cyan
Write-Host "  - Flask-Migrate" -ForegroundColor Gray
Write-Host "  - Flask-JWT-Extended" -ForegroundColor Gray
Write-Host "  - Flask-Marshmallow" -ForegroundColor Gray
Write-Host "  - marshmallow-sqlalchemy" -ForegroundColor Gray
Write-Host "  - PyMySQL" -ForegroundColor Gray

pip install Flask-Migrate==4.0.5 Flask-JWT-Extended==4.5.3 Flask-Marshmallow==0.15.0 marshmallow-sqlalchemy==0.29.0 PyMySQL==1.1.0 -q --disable-pip-version-check

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependências instaladas com sucesso" -ForegroundColor Green
} else {
    Write-Host "❌ Erro ao instalar dependências" -ForegroundColor Red
    exit 1
}

# Verificar instalação
Write-Host "`n[3/4] Verificando instalação..." -ForegroundColor Cyan
$packages = @("flask_migrate", "flask_jwt_extended", "flask_marshmallow", "pymysql")
$allInstalled = $true

foreach ($package in $packages) {
    $result = python -c "import $package; print('OK')" 2>&1
    if ($result -like "*OK*") {
        Write-Host "  ✅ $package" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $package" -ForegroundColor Red
        $allInstalled = $false
    }
}

if (-Not $allInstalled) {
    Write-Host "`n❌ Algumas dependências falharam na instalação" -ForegroundColor Red
    exit 1
}

# Executar testes novamente
Write-Host "`n[4/4] Executando testes novamente..." -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

python test_aplicacao.py

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "CORREÇÃO CONCLUÍDA" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan
