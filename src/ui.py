"""Gradio UI for Novelist Desktop."""
from pathlib import Path

import gradio as gr

from .config import config
from .engine import InferenceEngine
from .model_manager import ensure_model

THEME_CSS = """
body { font-family: 'Segoe UI', sans-serif !important; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important; }
.gradio-container { background: transparent !important; }
.message-row { padding: 8px 12px !important; }
.message-bubble {
    border-radius: 16px !important; padding: 12px 16px !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08) !important;
}
.message-row.user .message-bubble {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%) !important;
    border-bottom-right-radius: 4px !important;
}
.message-row.bot .message-bubble {
    background: #ffffff !important;
    border-bottom-left-radius: 4px !important;
    border: 1px solid #e0e0e0;
}
.input-textbox textarea {
    border-radius: 20px !important; border: 2px solid #667eea !important;
    padding: 12px 18px !important; background: white !important;
}
button.primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important; border-radius: 20px !important; color: white !important;
}
.app-header {
    text-align: center; padding: 16px 0;
}
.app-header h1 {
    margin: 0; font-size: 1.6em; color: #4a5568;
}
.app-header p {
    margin: 4px 0 0; color: #718096; font-size: 0.9em;
}
.message-row.bot .message-bubble blockquote {
    background: #f3f4f6;
    border-left: 3px solid #9ca3af;
    margin: 0 0 10px 0;
    padding: 8px 12px;
    border-radius: 6px;
    color: #6b7280;
    font-size: 0.88em;
}
.message-row.bot .message-bubble blockquote p { margin: 0; }
"""

SYSTEM_PROMPT = config.get("system_prompt", "")
DEFAULT_MAX_TOKENS = config.get("model.max_tokens", 1024)
APP_TITLE = config.get("ui.title", "Novelist")


class NovelistApp:
    def __init__(self):
        self.engine = None
        self._init_backend()

    def _init_backend(self):
        try:
            ensure_model()
            self.engine = InferenceEngine()
            print("[App] Ready.")
        except Exception as e:
            print(f"[App] Init failed: {e}")
            self.engine = None

    @staticmethod
    def _format_response(content: str, reasoning: str | None, show_thinking: bool) -> str:
        content = (content or "").strip()
        if not reasoning or not show_thinking:
            return content
        reasoning = reasoning.strip()
        think_lines = reasoning.splitlines()
        quoted = '\n'.join([f'> {line}' for line in think_lines])
        return f"> 💭 思考过程\n{quoted}\n\n{content}"

    def chat(self, message: str, history: list, max_tokens: int = DEFAULT_MAX_TOKENS, show_thinking: bool = False):
        if not self.engine:
            history = history or []
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": "[Error] llama-server not connected."})
            yield history
            return

        if not message.strip():
            yield history
            return

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        recent = (history or [])[-16:]
        for msg in recent:
            if isinstance(msg, dict) and msg.get("role") in ("user", "assistant"):
                messages.append(msg)
        messages.append({"role": "user", "content": message.strip()})

        try:
            content, reasoning, _ = self.engine.chat(messages, max_tokens=max_tokens)
            response = self._format_response(content, reasoning, show_thinking)
        except Exception as e:
            history = history or []
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": f"[Error] {str(e)[:120]}"})
            yield history
            return

        history = history or []
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})
        yield history

    def get_status(self) -> str:
        if not self.engine:
            return "Offline"
        return self.engine.get_device()

    def build_ui(self):
        with gr.Blocks(title=APP_TITLE) as demo:
            # Force-set document.title via JS to bypass any cache issues
            gr.HTML(f"""
                <script>document.title = "{APP_TITLE}";</script>
                <div class="app-header">
                    <h1>📝 超轻量轻小说写手</h1>
                    <p>仅0.6B，但幻想自己是14B · 氛围拉满，逻辑随缘</p>
                    <p>听说写世界观设定比较厉害？（存疑）</p>
                </div>
            """)

            status = gr.Textbox(
                value=self.get_status(), show_label=False,
                interactive=False, container=False,
            )

            chatbot = gr.Chatbot(
                height=560, buttons=["copy"], layout="bubble",
            )

            with gr.Row():
                msg = gr.Textbox(
                    placeholder="Describe your scene, characters, or plot idea...",
                    show_label=False, container=False, scale=6,
                    elem_classes=["input-textbox"],
                )
                send = gr.Button("Generate", scale=1, variant="primary")
                clear = gr.Button("Clear", scale=1, variant="secondary")

            with gr.Row():
                max_tokens_slider = gr.Slider(
                    minimum=128, maximum=4096, step=128,
                    value=DEFAULT_MAX_TOKENS,
                    label="Output Length (tokens)", scale=3,
                )
                show_thinking_cb = gr.Checkbox(
                    label="显示思考过程",
                    value=False,
                    scale=1,
                )
                status_label = gr.Textbox(
                    value=self.get_status(), show_label=False,
                    interactive=False, container=False, scale=2,
                )

            def respond(message, history, max_tokens, show_thinking):
                for h in self.chat(message, history, max_tokens, show_thinking):
                    yield h

            msg.submit(respond, [msg, chatbot, max_tokens_slider, show_thinking_cb], [chatbot]).then(
                lambda: (None, self.get_status()), outputs=[msg, status_label]
            )
            send.click(respond, [msg, chatbot, max_tokens_slider, show_thinking_cb], [chatbot]).then(
                lambda: (None, self.get_status()), outputs=[msg, status_label]
            )
            clear.click(lambda: ([],), outputs=[chatbot])

        return demo


def main():
    app = NovelistApp()
    demo = app.build_ui()
    demo.launch(
        server_name="127.0.0.1",
        share=False,
        show_error=True,
        inbrowser=True,
        css=THEME_CSS,
    )


if __name__ == "__main__":
    main()
