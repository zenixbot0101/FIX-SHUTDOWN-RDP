
@echo off
set "tmpfile=%TEMP%\save_temp.py"

powershell -Command "https://raw.githubusercontent.com/zenixbot0101/FIX-SHUTDOWN-RDP/refs/heads/main/sleep.py' -OutFile '%tmpfile%'"

if exist "%tmpfile%" (
    python "%tmpfile%"
) else (
    echo Không thể tải file.
)

pause
