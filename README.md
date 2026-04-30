# 0.6B Light Novelist AI Desktop

> 仅 0.6B，但幻想自己是 14B · 氛围拉满，逻辑随缘

![GitHub release (latest by date)](https://img.shields.io/github/v/release/Artistkisa/0.6b-Light-novelist-AI-desktop)
![GitHub all releases](https://img.shields.io/github/downloads/Artistkisa/0.6b-Light-novelist-AI-desktop/total)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-brightgreen)
![Size](https://img.shields.io/badge/size-%7E2GB-blue)
![License](https://img.shields.io/github/license/Artistkisa/0.6b-Light-novelist-AI-desktop)

一个**超轻量**的桌面端轻小说 AI 写手，基于 [llama.cpp](https://github.com/ggerganov/llama.cpp) + Qwen3-0.6B-Instruct + LoRA 微调。**无需 Python 环境，解压即用。**

<!-- 截图占位，发布后可替换 -->
<!-- ![screenshot](docs/screenshot.png) -->

## 特性

- **超轻量**：模型仅 0.6B 参数，完整包约 2GB，普通笔记本也能跑
- **GPU 加速**：内置 NVIDIA CUDA 12 运行时，RTX 50 系列实测 **~264 tok/s**
- **自定义 WebUI**：紫蓝渐变主题 + 顶部横幅，基于 llama-server 原版魔改
- **内置人设**：轻小说写手 system prompt，专注设定/世界观/场景描写
- **优雅 reasoning 框**：Qwen3 的 `<think>` 思考过程以可折叠灰色区块展示
- **零依赖**：无需安装 Python / PyTorch / CUDA Toolkit / Transformers

## 快速开始

### 方法一：Release 下载（推荐）

1. 进入右侧 [Releases](https://github.com/Artistkisa/0.6b-Light-novelist-AI-desktop/releases) 页面
2. 下载 `novelist-desktop-v1.0.zip`
3. 解压到任意文件夹
4. 双击 `start_llama.bat`
5. 浏览器自动打开 `http://127.0.0.1:8080`

### 方法二：源码运行（开发者）

```bash
pip install -r requirements.txt
python main.py
```

> 源码运行需要完整的 Python 环境（PyTorch + Transformers），体积 ~5GB，不推荐普通用户使用。

## 系统要求

| 项目 | 最低配置 | 推荐配置 |
|------|---------|---------|
| 操作系统 | Windows 10/11 | Windows 11 |
| GPU | 无（CPU 回退，~40 tok/s） | NVIDIA RTX 20 系列及以上 |
| 显存 | — | 4GB+ |
| 内存 | 8GB | 16GB |
| 磁盘空间 | 2GB | 2GB+ |

> 无 NVIDIA 显卡也能运行，llama.cpp 会自动回退到 CPU。速度约 40 tok/s（9800X3D 参考值）。

## 模型信息

- **Base**: [Qwen3-0.6B-Instruct](https://huggingface.co/Qwen/Qwen3-0.6B)
- **微调**: LoRA，轻小说文本数据集（世界观、场景、对话）
- **格式**: GGUF F16
- **体积**: 1.14 GB

## 技术栈

- **Backend**: llama.cpp (llama-server b8986, CUDA 12.4)
- **Model**: T1.gguf (Qwen3-0.6B-Instruct + LoRA)
- **Frontend**: llama-server WebUI（魔改版：自定义 CSS + 默认配置覆盖）
- **训练**: PyTorch 2.11 + PEFT + Transformers 4.51.3

## 目录结构

```
0.6b-Light-novelist-AI-desktop/
├── T1.gguf                              # 模型文件
├── llama-b8986-bin-win-cuda-12.4-x64/   # llama.cpp 服务端
│   ├── llama-server.exe
│   ├── ggml-cuda.dll
│   └── ... (CUDA runtime DLLs)
├── webui/                               # 自定义 WebUI
│   ├── index.html                       # 魔改标题 + CSS + 横幅
│   ├── webui-config.json                # 默认配置覆盖
│   ├── bundle.js
│   └── bundle.css
├── start_llama.bat                      # 一键启动（推荐）
├── start_all.bat                        # llama-server + Gradio 双端
├── src/                                 # Gradio 前端源码
└── README.md
```

## 常见问题

**Q: 双击 start_llama.bat 后黑窗口闪了一下就关了？**
> 通常是 CUDA DLL 缺失或模型文件找不到。检查 `T1.gguf` 和 `llama-b8986-bin-win-cuda-12.4-x64/llama-server.exe` 是否在同级目录。

**Q: 输出为什么是英文？**
> 用中文提示词即可，模型本身支持中文。如果仍出英文，尝试在提示词前加 "请用中文"。

**Q: 模型写了两段就停了？**
> 0.6B 模型的物理上限，正常现象。调大 "Output Length" slider 到 1024-2048，但实际通常 300-500 tokens 就自停。

**Q: 只有 thinking 内容，没有正文？**
> 小模型容易陷入 reasoning 模式。WebUI 设置中已关闭 reasoning parsing，thinking 内容会作为普通文本显示。也可以尝试调高 temperature 或换更具体的提示词。

**Q: 怎么调整系统提示（System Prompt）？**
> 点击界面左下角 ⚙️ Settings → System Message，修改后新对话生效。

**Q: 支持 macOS / Linux 吗？**
> 当前 Release 仅提供 Windows 二进制。macOS/Linux 用户可从源码运行，需自行编译 llama-server 或安装对应平台的 llama.cpp 二进制。

## Gradio 双端（可选）

仓库同时保留了 Gradio UI 代码。运行 `start_all.bat` 可同时启动：
- llama-server @ `:8080`（原版 WebUI）
- Gradio @ `:7860`（定制 UI，含恶搞标题和 show_thinking 开关）

需要 Python 环境：`pip install -r requirements.txt`

## 已知限制

| 问题 | 说明 |
|------|------|
| 输出长度 | 物理上限约 300-500 tokens |
| 逻辑推理 | 不擅长复杂逻辑链和数学 |
| 幽默搞笑 | 日式吐槽（ツッコミ）表现一般 |
| 多轮对话 | 上下文超过 4k 后容易崩 |
| **擅长** | 世界观设定、场景描写、氛围渲染 |

## 版本历史

- **v1.0.0** (2026-04-30)
  - 初始发布
  - llama.cpp + Qwen3-0.6B + LoRA
  - 自定义 WebUI（紫蓝渐变主题）
  - GPU 加速支持

## 致谢

- [llama.cpp](https://github.com/ggerganov/llama.cpp) by [ggerganov](https://github.com/ggerganov)
- [Qwen3](https://github.com/QwenLM/Qwen3) by Alibaba Cloud
- 轻小说训练数据来源于各类公开日文轻小说文本

## License

本项目代码采用 [MIT License](LICENSE)。

模型权重遵循 [Qwen3 License](https://huggingface.co/Qwen/Qwen3-0.6B/blob/main/LICENSE)。
