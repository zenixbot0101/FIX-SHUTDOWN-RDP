@echo off
setlocal

rem --- CONFIG ---
set "URL=https://raw.githubusercontent.com/zenixbot0101/FIX-SHUTDOWN-RDP/refs/heads/main/sleep.py"
set "DEST=%TEMP%\sleep.py"

echo Downloading script from:
echo %URL%
echo Target: %DEST%
echo.

rem --- Download using PowerShell ---
powershell -NoProfile -Command ^
  "try { Invoke-WebRequest -Uri '%URL%' -OutFile '%DEST%' -UseBasicParsing -ErrorAction Stop; exit 0 } catch { exit 1 }"
if errorlevel 1 (
  echo [!] Download failed.
  pause
  exit /b 1
)
echo [*] Download succeeded.

rem --- Find pythonw.exe or python.exe ---
where pythonw >nul 2>&1
if %ERRORLEVEL%==0 (
  for /f "delims=" %%I in ('where pythonw') do set "PY=%%I" & goto :gotpython
)
where python >nul 2>&1
if %ERRORLEVEL%==0 (
  for /f "delims=" %%I in ('where python') do set "PY=%%I" & goto :gotpython
)

echo [!] Python not found in PATH. Please install Python and add to PATH.
pause
exit /b 1

:gotpython
echo [*] Found Python interpreter: "%PY%"

rem --- Try to run elevated (UAC prompt) ---
echo [*] Launching script as Administrator (UAC prompt may appear)...
powershell -NoProfile -Command "Start-Process -FilePath '%PY%' -ArgumentList '%DEST%' -Verb RunAs"
if %ERRORLEVEL% neq 0 (
  echo [!] Failed to start elevated. Trying to run without elevation...
  "%PY%" "%DEST%"
)

endlocal
exit /b 0
