@echo off
setlocal
chcp 65001 >nul
if /I not "%~d0"=="D:" if /I not "%~d0"=="E:" (
  echo Hãy giải nén thư mục này vào ổ D hoặc E rồi mở lại.
  pause
  exit /b 1
)
cd /d "%~dp0"
set "PYTHONUTF8=1"
set "PYTHONDONTWRITEBYTECODE=1"
if exist "%~dp0.venv\Scripts\python.exe" (
  "%~dp0.venv\Scripts\python.exe" launcher.py
  goto finished
)
if exist "D:\Codex\Python312\python.exe" (
  "D:\Codex\Python312\python.exe" launcher.py
  goto finished
)
if exist "E:\Codex\Python312\python.exe" (
  "E:\Codex\Python312\python.exe" launcher.py
  goto finished
)
where py.exe >nul 2>nul
if not errorlevel 1 (
  py -3.12 -c "import sys; sys.exit(0 if sys.version_info >= (3,11) else 1)" >nul 2>nul
  if not errorlevel 1 (
    py -3.12 launcher.py
    goto finished
  )
  py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3,11) else 1)" >nul 2>nul
  if not errorlevel 1 (
    py -3 launcher.py
    goto finished
  )
)
if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" (
  "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" launcher.py
  goto finished
)
for /f "delims=" %%P in ('where python.exe 2^>nul ^| findstr /V /I "WindowsApps"') do (
  "%%P" launcher.py
  goto finished
)
echo Chưa tìm thấy Python. Xem mục Dashboard Streamlit trong ..\HUONG_DAN_MO_BAI.md.
pause
exit /b 1
:finished
if errorlevel 1 (
  echo.
  echo Xem ..\HUONG_DAN_MO_BAI.md để xử lý hoặc gửi lại thông báo lỗi.
  pause
)
