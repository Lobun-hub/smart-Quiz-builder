import json
import os
import re

from ai_client import ai_available, get_client  # ai_available is re-exported for app.py
from quiz_engine import DOMAINS, is_valid_question


def generate_questions(domain: str, count: int = 5) -> list[dict]:
    """Ask the model for AZ-900 style multiple-choice questions as strict JSON."""
    if domain not in DOMAINS:
        raise ValueError(f"Unknown domain: {domain}")
    if isinstance(count, bool) or not isinstance(count, int) or count < 1:
        raise ValueError("count must be a positive integer.")

    client = get_client()
    model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5")

    prompt = (
        f'Create {count} AZ-900 (Microsoft Azure Fundamentals) multiple-choice '
        f'questions for "{domain}". Each question has exactly 4 options and one '
        "correct answer. Return ONLY a JSON array, no markdown. Each item must "
        'have the keys "domain" (exact match), "question", "options" (4 strings), '
        '"answer" (0-based index), and "explanation" (1-2 sentences).'
    )

    response = client.messages.create(
        model=model,
        max_tokens=2500,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text.strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.MULTILINE).strip()

    items = json.loads(text)
    if not isinstance(items, list) or len(items) != count or any(
        not is_valid_question(question)
        or question["domain"] != domain
        or len(question["options"]) != 4
        for question in items
    ):
        raise ValueError(
            "The AI response must contain exactly "
            f"{count} valid questions for {domain}."
        )
    return items