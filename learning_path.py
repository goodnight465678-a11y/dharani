from gemini_client import generate_text

def get_learning_recommendations(topic: str) -> str:
    prompt = f"""Create a personalized learning path for the topic below.\nOrganize it from beginner to intermediate to advanced.\nFor each stage include: concepts to learn, a suggested timeframe, practice activities, and useful resource types (videos, articles, books, documentation, or courses).\nKeep it practical and adaptable to a learner studying independently.\n\nTOPIC:\n{topic}"""
    return generate_text(prompt, temperature=0.35)
