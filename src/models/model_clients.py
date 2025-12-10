import os
import requests
from typing import Optional, Dict, Any
from ..core.config import settings


class LLMClient:
    """
    Thin wrapper around a local/remote LLM endpoint.
    On GB10, you can point MODEL_ENDPOINT_URL to a NVIDIA NIM / DGX Spark model.
    """

    def __init__(self):
        self.base_url = settings.MODEL_ENDPOINT_URL
        self.api_key = settings.MODEL_API_KEY

    def is_configured(self) -> bool:
        return bool(self.base_url)

    def generate(self, prompt: str, max_tokens: int = 512) -> Optional[str]:
        if not self.is_configured():
            return None

        try:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            # Adjust payload according to the model server you use on GB10
            payload: Dict[str, Any] = {
                "model": "local-llm",
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": 0.2,
            }
            resp = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            # Adapt this depending on your model's schema
            return data.get("choices", [{}])[0].get("text", "").strip()
        except Exception as e:
            print(f"[LLM ERROR] {e}")
            return None


llm_client = LLMClient()