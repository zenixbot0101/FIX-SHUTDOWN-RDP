@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Dang yeu cau quyen Administrator...
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit /b
)

echo [*] Dang tai sleep.py tu GitHub...
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/zenixbot0101/FIX-SHUTDOWN-RDP/refs/heads/main/sleep.py' -OutFile 'C:\sleep.py'" >nul 2>&1

if exist C:\sleep.py (
    echo [+] Tai thanh cong: C:\sleep.py
) else (
    echo [-] Loi: Khong the tai file tu GitHub.
    pause
    exit /b
)

echo [*] Dang khoi dong AFK MODE...
python C:\sleep.py
pause
