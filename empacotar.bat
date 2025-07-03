@echo off
cd src
pyinstaller --name=antepausa --onefile --noconsole --icon=../assets/automacao.ico antepausa.py
echo.
echo Executável gerado em dist\antepausa.exe
pause
