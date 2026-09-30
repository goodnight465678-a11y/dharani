from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    app_name: str = os.getenv("APP_NAME", "EduGenie")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    explanation_backend: str = os.getenv("EXPLANATION_BACKEND", "gemini")
    local_explanation_model: str = os.getenv(
        "LOCAL_EXPLANATION_MODEL", "MBZUAI/LaMini-Flan-T5-783M"
    )
    max_input_chars: int = int(os.getenv("MAX_INPUT_CHARS", "20000"))

@lru_cache
def get_settings() -> Settings:
    return Settings()
