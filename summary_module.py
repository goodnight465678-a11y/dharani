from gemini_client import generate_text

def summarize_text(text: str) -> str:
    prompt = f"""Summarize the following educational text for quick revision.\nKeep the important facts, concepts, relationships, and terminology.\nUse concise bullet points followed by a one-sentence takeaway.\nDo not add facts that are not supported by the input.\n\nTEXT:\n{text}"""
    return generate_text(prompt, temperature=0.2)
