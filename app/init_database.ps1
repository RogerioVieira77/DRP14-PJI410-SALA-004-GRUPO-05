# Script PowerShell para inicializar o banco de dados
# Garante que o ambiente virtual está ativado

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Inicialização do Banco de Dados" -ForegroundColor Cyan
Write-Host "CEU Tres Pontes - Sistema de Controle" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Verificar se estamos na raiz do projeto
if (-not (Test-Path ".\venv")) {
    Write-Host "❌ Erro: Ambiente virtual (venv) não encontrado!" -ForegroundColor Red
    Write-Host "Execute este script da raiz do projeto." -ForegroundColor Yellow
    exit 1
}

Write-Host "📦 Ativando ambiente virtual..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host "✅ Ambiente virtual ativado`n" -ForegroundColor Green

Write-Host "🔧 Instalando dependências faltantes..." -ForegroundColor Yellow
pip install Flask-Migrate alembic -q

Write-Host "`n🗄️  Inicializando banco de dados..." -ForegroundColor Yellow
python backend\init_db.py

Write-Host "`n✅ Concluído!" -ForegroundColor Green
