import json
import os
import re

from dotenv import load_dotenv

from quiz_engine import DOMAINS, is_valid_question

load_dotenv()


def ai_available() -> bool:
    return bool(os.getenv("ANTHROPIC_API_KEY"))


def generate_questions(domain: str, count: int = 5) -> list[dict]:
    """Ask the model for AZ-900 style multiple-choice questions as strict JSON."""
    if domain not in DOMAINS:
        raise ValueError(f"Unknown domain: {domain}")
    if isinstance(count, bool) or not isinstance(count, int) or count < 1:
        raise ValueError("count must be a positive integer.")

    import anthropic

    prompt = (
        f'Create {count} AZ-900 questions for "{domain}", each with exactly four options, '
        "one correct answer, and a 1-2 sentence explanation. Return only a JSON array "
        'with "domain" (exact match), "question", "options", "answer" (zero-based), '
        "and \"explanation\" keys."
    )

    response = anthropic.Anthropic().messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5"),
        max_tokens=2500,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text.strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.MULTILINE).strip()
    items = json.loads(text)

    if not isinstance(items, list) or len(items) != count or any(
        not is_valid_question(q)
        or q["domain"] != domain
        or len(q["options"]) != 4
        for q in items
    ):
        raise ValueError(f"The AI response must contain exactly {count} valid questions for {domain}.")
    return items
