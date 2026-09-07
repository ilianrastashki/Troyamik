@echo off
REM ---------------------------------------------------------------
REM  Стартира локалната MySQL инстанция за Троямик на порт 3307.
REM  Услугата MySQL80 заема 3306 и иска парола, затова проектът
REM  ползва собствена инстанция със собствена datadir папка.
REM  Ако вече работи, скриптът не прави нищо.
REM ---------------------------------------------------------------

netstat -an | findstr /C:"127.0.0.1:3307" | findstr /C:"LISTENING" >nul 2>&1
if %ERRORLEVEL%==0 (
    echo MySQL vece raboti na port 3307.
    exit /b 0
)

if not exist "%LOCALAPPDATA%\TroyamikMySQL\data" (
    echo GRESHKA: lipsva "%LOCALAPPDATA%\TroyamikMySQL\data"
    echo Bazata ne e inicializirana.
    exit /b 1
)

"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld.exe" --no-defaults ^
  --datadir="%LOCALAPPDATA%\TroyamikMySQL\data" ^
  --port=3307 --bind-address=127.0.0.1 ^
  --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
