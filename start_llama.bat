@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ==========================================
echo   轻小说模型服务 (llama.cpp + GPU)
echo ==========================================
echo 模型: T1.gguf (Qwen3-0.6B + LoRA)
echo 端口: http://127.0.0.1:8080
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

echo 正在启动 llama-server，首次加载模型需要几秒...
start "" http://127.0.0.1:8080

%LLAMA_DIR%\llama-server.exe -m %MODEL% --host 127.0.0.1 --port 8080 -ngl 99 -c 4096 --jinja --path webui --webui-config-file webui\webui-config.json --temp 0.6 --top-p 0.95 --top-k 20

pause
