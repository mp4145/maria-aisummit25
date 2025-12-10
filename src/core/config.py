import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "maria-aisumit25"
    API_V1_PREFIX: str = "/api"

    # LLM / model config (adjust on GB10)
    MODEL_ENDPOINT_URL: str = os.getenv("MODEL_ENDPOINT_URL", "")
    MODEL_API_KEY: str = os.getenv("MODEL_API_KEY", "")

settings = Settings()