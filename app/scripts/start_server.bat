@echo off
echo ========================================
echo CEU TRES PONTES - INICIANDO SERVIDOR
echo ========================================
echo.

cd /d "C:\PI - IV - V1"

echo [1/3] Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo [2/3] Configurando Flask...
set FLASK_APP=backend/app.py
set FLASK_ENV=development
set FLASK_DEBUG=1

echo [3/3] Iniciando servidor Flask...
echo.
echo ========================================
echo SERVIDOR RODANDO EM:
echo   - http://localhost:5000
echo   - http://127.0.0.1:5000
echo ========================================
echo.
echo Pressione CTRL+C para parar o servidor
echo.

flask run --host=0.0.0.0 --port=5000

pause
