@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    python -m venv .venv
    if errorlevel 1 goto error
)
if not exist ".venv\listo" (
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 goto error
    echo listo>".venv\listo"
)
".venv\Scripts\python.exe" -m coco %*
if errorlevel 1 goto error
pause
exit /b 0
:error
echo No se pudo iniciar CoCo. Revisa el error anterior y que Python este instalado.
pause
exit /b 1
