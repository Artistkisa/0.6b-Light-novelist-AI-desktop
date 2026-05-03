@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ==========================================
echo   超轻量轻小说写手 - 一键启动
echo ==========================================
echo.

set LLAMA_DIR=llama-b8986-bin-win-cuda-12.4-x64
set MODEL=T1.gguf

if not exist %MODEL% (
    echo [错误] 找不到模型文件 %MODEL%
    pause
    exit /b 1
)

if not exist %LLAMA_DIR%\llama-server.exe (
    echo [错误] 找不到 llama-server.exe
    pause
    exit /b 1
)

echo [1/3] 启动 llama-server (GPU加速)...
start /b "" %LLAMA_DIR%\llama-server.exe -m %MODEL% --host 127.0.0.1 --port 8080 -ngl 99 -c 4096 --jinja --path webui --webui-config-file webui\webui-config.json --temp 0.6 --top-p 0.95 --top-k 20 > llama-server.log 2>&1

echo [2/3] 等待模型加载...
:wait_loop
ping 127.0.0.1 -n 2 >nul
powershell -Command "try { Invoke-WebRequest -Uri 'http://127.0.0.1:8080/health' -UseBasicParsing -TimeoutSec 1 | Out-Null; exit 0 } catch { exit 1 }"
if errorlevel 1 goto wait_loop

echo        就绪! GPU加速已启用
echo.
echo [3/3] 启动 Gradio UI...
echo.
echo 访问地址:
echo   Gradio UI (定制版): http://127.0.0.1:7860
echo   WebUI (原版):       http://127.0.0.1:8080
echo.
start http://127.0.0.1:7860

python main.py

echo.
echo 正在关闭 llama-server...
taskkill /F /IM llama-server.exe >nul 2>&1
echo 已退出。
pause
