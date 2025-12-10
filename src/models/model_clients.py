from typing import Optional
from src.core.config import settings


def call_llm(prompt: str, max_tokens: int = 512) -> str:
    """
    Placeholder LLM client.

    For the Hackathon:
      - Replace this with calls to NVIDIA / GB10 models
        exposed via Docker containers or HTTP endpoints.

    For now, just echo a simple deterministic stub so the system runs
    even without external connectivity.
    """
    if settings.MODEL_BACKEND == "local_stub":
        # Extremely naive: just returns a trimmed version of the prompt.
        # Enough to keep the pipeline functional.
        return (
            "Reasoned summary (stub): based on the provided crash and injury "
            "details, the injuries appear clinically plausible with some "
            "caveats that require human review."
        )

    # Example placeholder for future:
    # elif settings.MODEL_BACKEND == "nvidia_gb10":
    #     return call_nvidia_model(prompt, max_tokens=max_tokens)

    return "LLM backend not configured."