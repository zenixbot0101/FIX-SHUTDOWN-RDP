
@echo off
set "tmpfile=%TEMP%\save_temp.py"

powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/zenixbot0101/AUTO-SAVE-GAME/refs/heads/main/save.py' -OutFile '%tmpfile%'"

if exist "%tmpfile%" (
    python "%tmpfile%"
) else (
    echo Không thể tải file.
)

pause
