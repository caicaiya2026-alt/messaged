@echo off
chcp 65001 >nul
echo ========================================
echo    Cloudflare Tunnel 配置助手
echo ========================================
echo.

REM 检查 cloudflared 是否存在
if not exist "cloudflared.exe" (
    echo [错误] 未找到 cloudflared.exe
    echo 请先下载 cloudflared
    pause
    exit /b 1
)

echo [1/5] 登录 Cloudflare...
echo.
echo 这将打开浏览器，请登录你的 Cloudflare 账户
pause
.\cloudflared.exe tunnel login
if errorlevel 1 (
    echo [错误] 登录失败
    pause
    exit /b 1
)
echo.
echo [2/5] 创建 Tunnel...
.\cloudflared.exe tunnel create messaged-tunnel
if errorlevel 1 (
    echo [错误] 创建 Tunnel 失败
    pause
    exit /b 1
)
echo.
echo [3/5] 配置域名路由...
echo.
set /p DOMAIN="请输入你的域名（例如：example.com）: "
if "%DOMAIN%"=="" (
    echo [错误] 域名不能为空
    pause
    exit /b 1
)
.\cloudflared.exe tunnel route dns messaged-tunnel messaged.%DOMAIN%
if errorlevel 1 (
    echo [错误] 配置域名路由失败
    pause
    exit /b 1
)
echo.
echo [4/5] 创建配置文件...
echo.
echo tunnel: messaged-tunnel > config.yml
echo credentials-file: %USERPROFILE%\.cloudflared\%TUNNEL_ID%.json >> config.yml
echo. >> config.yml
echo ingress: >> config.yml
echo   - hostname: messaged.%DOMAIN% >> config.yml
echo     service: tcp://localhost:8765 >> config.yml
echo   - service: http_status:404 >> config.yml
echo.
echo 配置文件已创建: config.yml
echo.
echo [5/5] 启动 Tunnel...
echo.
echo Tunnel 将在以下地址可用:
echo    wss://messaged.%DOMAIN%
echo.
echo 按 Ctrl+C 停止 Tunnel
echo.
.\cloudflared.exe tunnel --config config.yml run
