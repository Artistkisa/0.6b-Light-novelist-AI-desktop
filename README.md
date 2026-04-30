# 📝 超轻量轻小说写手

**仅0.6B写出14B效果 —— 是蒸馏模型**

A local light novel writer powered by Qwen3-0.6B with LoRA fine-tuning.

## Features

- ✍️ Japanese-style light novel generation
- 🎭 Anime-style character dialogue
- 🏃 Dramatic plot developments
- 💭 Inner monologues and comedic timing
- 💻 Fully offline, zero data upload
- 🎚️ Adjustable output length (128-2048 tokens)

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 4 cores | 8 cores+ |
| RAM | 4 GB | 8 GB+ |
| Disk | 2 GB | 3 GB+ |
| GPU | Optional | NVIDIA 4GB+ |

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

Or double-click `start.bat` on Windows.

## Model Setup

Place your model files in a `T1/` folder next to the executable:

```
T1/
  model.safetensors      # Base model (Qwen3-0.6B)
  config.json
  tokenizer.json
  adapter/               # LoRA adapter (optional)
    adapter_config.json
    adapter_model.safetensors
```

## GPU Acceleration

By default runs on CPU. For NVIDIA GPU support:

```bash
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

## License

MIT
