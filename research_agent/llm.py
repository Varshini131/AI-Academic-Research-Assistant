import os
from groq import Groq

def is_llm_configured() -> bool:
    return bool(os.getenv("GROQ_API_KEY"))

def generate_text(prompt: str) -> str:
    """Call Groq when configured; otherwise return setup guidance instead of failing."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return (
            "AI generation is not configured yet. Add your GROQ_API_KEY to the .env file, "
            "restart Streamlit, and try again. Paper search and PDF text extraction can work "
            "without the key, but summaries, Q&A, comparisons, and literature-review drafting need an LLM."
        )
    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a careful academic research assistant. Never fabricate evidence, bibliographic details, or citations."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        return completion.choices[0].message.content or "The model returned an empty response."
    except Exception as exc:
        return f"LLM request failed: {exc}\n\nCheck that your API key is valid and your selected model is available."
