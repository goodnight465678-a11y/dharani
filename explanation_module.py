from config import get_settings
from gemini_client import generate_text

_local_pipeline = None

def _local_explain(topic: str) -> str:
    global _local_pipeline
    if _local_pipeline is None:
        from transformers import pipeline
        _local_pipeline = pipeline(
            "text2text-generation",
            model=get_settings().local_explanation_model,
        )
    prompt = f"Explain this topic simply for a beginner: {topic}"
    result = _local_pipeline(prompt, max_new_tokens=220, do_sample=False)
    return result[0]["generated_text"].strip()

def explain_concept(topic: str) -> str:
    settings = get_settings()
    if settings.explanation_backend.lower() == "local":
        try:
            return _local_explain(topic)
        except Exception as exc:
            # A cloud fallback keeps the application usable when the optional local model
            # cannot be loaded because of RAM, PyTorch, or model-download constraints.
            try:
                return generate_text(
                    f"Explain the following concept to a beginner using simple language and one example:\n{topic}",
                    temperature=0.25,
                )
            except Exception:
                raise RuntimeError(f"Local explanation model failed: {exc}") from exc
    return generate_text(
        f"Explain the following concept to a beginner. Break it into simple steps and give one intuitive example.\n{topic}",
        temperature=0.25,
    )
