"""Inference engine client for llama-server (OpenAI-compatible API)."""
import json
import time
import urllib.request
import urllib.error
from typing import List, Dict, Tuple, Optional

from .config import config


class InferenceEngine:
    """HTTP client for llama-server OpenAI-compatible chat completions API."""

    def __init__(self, api_base: str = "http://127.0.0.1:8080", model: str = "T1", verbose: bool = False):
        self.api_base = api_base.rstrip("/")
        self.model = model
        self.verbose = verbose
        self._wait_for_server()

    def _wait_for_server(self, timeout: int = 60):
        """Poll /health until llama-server is ready."""
        url = f"{self.api_base}/health"
        start = time.time()
        print(f"[Engine] Waiting for llama-server at {self.api_base} ...")
        while time.time() - start < timeout:
            try:
                req = urllib.request.Request(url, method="GET")
                with urllib.request.urlopen(req, timeout=2) as resp:
                    if resp.status == 200:
                        print(f"[Engine] llama-server ready.")
                        return
            except urllib.error.HTTPError as e:
                # 503 = model still loading, keep waiting
                if e.code == 503:
                    time.sleep(0.5)
                    continue
                time.sleep(0.5)
            except Exception:
                time.sleep(0.5)
        raise ConnectionError(f"llama-server not responding at {self.api_base} after {timeout}s")

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = None,
        max_tokens: int = None,
    ) -> Tuple[str, Optional[str], float]:
        """
        Returns: (content, reasoning_content, elapsed_seconds)
        reasoning_content may be None if the model doesn't emit <think> tags.
        """
        temp = temperature if temperature is not None else config.get("model.temperature", 0.8)
        max_tok = max_tokens if max_tokens is not None else config.get("model.max_tokens", 1024)
        top_p = config.get("model.top_p", 0.9)
        repeat_penalty = config.get("model.repeat_penalty", 1.15)

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tok,
            "temperature": temp,
            "top_p": top_p,
            "repeat_penalty": repeat_penalty,
        }

        url = f"{self.api_base}/v1/chat/completions"
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        start = time.time()
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = resp.read().decode("utf-8")
        elapsed = time.time() - start

        result = json.loads(body)
        choice = result["choices"][0]["message"]
        content = choice.get("content", "") or ""
        reasoning = choice.get("reasoning_content")

        usage = result.get("usage", {})
        comp_tokens = usage.get("completion_tokens", 0)
        speed = comp_tokens / elapsed if elapsed > 0 else 0
        print(f"[Engine] Generated {comp_tokens} tokens in {elapsed:.2f}s ({speed:.1f} tok/s)")

        return content, reasoning, elapsed

    def get_device(self) -> str:
        return "llama.cpp GPU"
