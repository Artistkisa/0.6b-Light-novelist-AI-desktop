# Novelist Desktop - Release Notes

## 一键启动
双击 `start_llama.bat` 即可启动 llama-server + 自定义 WebUI，自动打开浏览器。

## 技术栈
- **Backend**: llama.cpp (llama-server) + CUDA 12
- **Model**: T1.gguf (Qwen3-0.6B-Instruct + LoRA)
- **Frontend**: llama-server 自带 WebUI（魔改版）

## 魔改内容
1. **标题**: `超轻量轻小说写手 - 仅0.6B写出14B效果`
2. **顶部横幅**: 紫色渐变标语条
3. **配色**: 侧边栏改为紫蓝渐变（#667eea → #764ba2），主背景改为淡灰蓝渐变
4. **默认配置**:
   - 系统提示: 轻小说写手人设
   - Temperature: 0.8
   - Max tokens: 1024
   - 禁用 reasoning parsing（小模型 thinking 内容直接显示在聊天中）

## 文件清单
```
T1.gguf                           # 模型 (1.14 GB)
llama-b8986-bin-win-cuda-12.4-x64/ # llama.cpp 二进制 + CUDA DLL (~1.2 GB)
webui/                             # 自定义 WebUI
  ├── index.html                   # 自定义标题 + CSS + 横幅
  ├── bundle.js                    # 原始 WebUI JS
  ├── bundle.css                   # 原始 WebUI CSS
  └── webui-config.json            # 默认配置覆盖
start_llama.bat                    # 一键启动脚本
```

## 体积
约 **2.3 GB**（模型 1.14GB + CUDA 运行时 0.75GB + ggml-cuda 0.46GB + 其他）

## 性能
- GPU: RTX 5070 → **~264 tok/s**
- CPU: ~40 tok/s（无 CUDA 时自动回退）

## 已知限制
- **0.6B 模型物理上限**: 即使 max_tokens=4096，实际输出通常 300-500 tokens 后自停
- **思考过程**: Qwen3 0.6B 容易陷入 thinking 模式，设置中已关闭 reasoning parsing 让 thinking 内容直接显示
- **逻辑/搞笑**: 模型不擅长复杂逻辑和幽默，擅长设定/世界观描述

## Gradio 双端（可选）
如果仍需 Gradio 定制 UI，运行 `start_all.bat`（先启动 llama-server，再启动 Gradio @ :7860）。
注意：需要 Python 环境 + `pip install -r requirements.txt`
