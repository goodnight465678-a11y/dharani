from functools import lru_cache
from config import get_settings

class GeminiError(RuntimeError):
    pass

@lru_cache
def get_client():
    settings = get_settings()
    if not settings.gemini_api_key:
        raise GeminiError("GEMINI_API_KEY is not configured. Add it to .env.")
    from google import genai
    return genai.Client(api_key=settings.gemini_api_key)

def generate_text(prompt: str, *, temperature: float = 0.3) -> str:
    try:
        response = get_client().models.generate_content(
            model=get_settings().gemini_model,
            contents=prompt,
            config=__import__("google.genai", fromlist=["types"]).types.GenerateContentConfig(temperature=temperature),
        )
        text = getattr(response, "text", None)
        if not text:
            raise GeminiError("Gemini returned an empty response.")
        return text.strip()
    except GeminiError:
        raise
    except Exception as exc:
        raise GeminiError(f"Gemini request failed: {exc}") from exc

def generate_json(prompt: str, schema: dict):
    import json
    try:
        response = get_client().models.generate_content(
            model=get_settings().gemini_model,
            contents=prompt,
            config=__import__("google.genai", fromlist=["types"]).types.GenerateContentConfig(
                temperature=0.2,
                response_mime_type="application/json",
                response_schema=schema,
            ),
        )
        raw = getattr(response, "text", None)
        if not raw:
            raise GeminiError("Gemini returned an empty JSON response.")
        return json.loads(raw)
    except GeminiError:
        raise
    except Exception as exc:
        raise GeminiError(f"Gemini JSON request failed: {exc}") from exc
