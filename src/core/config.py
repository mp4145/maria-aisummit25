from pydantic import BaseSettings


class Settings(BaseSettings):
    # You can extend this with NVIDIA/GB10 model endpoints later
    MODEL_BACKEND: str = "local_stub"  # or "nvidia_gb10"
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()