from gemini_client import generate_json

QUIZ_SCHEMA = {
    "type": "array",
    "minItems": 3,
    "maxItems": 3,
    "items": {
        "type": "object",
        "properties": {
            "question": {"type": "string"},
            "options": {"type": "array", "minItems": 4, "maxItems": 4, "items": {"type": "string"}},
            "correct_answer": {"type": "string"},
            "explanation": {"type": "string"},
        },
        "required": ["question", "options", "correct_answer", "explanation"],
    },
}

def generate_quiz(content: str):
    prompt = f"""Create exactly 3 multiple-choice questions from the educational content below.\nEach question must have exactly 4 options, exactly one correct answer, and a short explanation.\nThe correct_answer must exactly match one option.\nReturn only data matching the requested JSON schema.\n\nCONTENT:\n{content}"""
    quiz = generate_json(prompt, QUIZ_SCHEMA)
    if not isinstance(quiz, list) or len(quiz) != 3:
        raise RuntimeError("Quiz generation returned an invalid number of questions.")
    for item in quiz:
        if len(item.get("options", [])) != 4 or item["correct_answer"] not in item["options"]:
            raise RuntimeError("Quiz generation returned invalid options.")
    return quiz
