@echo off

echo ======================================
echo Iniciando SIEM
echo ======================================

start "SIEM" cmd /k "python main.py"

timeout /t 2 > nul

start "API" cmd /k "python -m uvicorn api.server:app --reload"

timeout /t 2 > nul

start "Dashboard" cmd /k "python -m streamlit run dashboard/dashboard_principal.py"

echo.
echo Sistema iniciado correctamente.
pause
