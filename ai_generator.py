import json
import os
import re

from ai_client import ai_available, get_client  # ai_available is re-exported for app.py
from quiz_engine import is_valid_question


def generate_questions(domain: str, count: int = 5) -> list[dict]:
    """Ask the model for AZ-900 style multiple-choice questions as strict JSON."""
    client = get_client()
    model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5")

    prompt = f"""Create {count} AZ-900 (Microsoft Azure Fundamentals) multiple-choice questions
for the domain "{domain}". Each question has exactly 4 options and one correct answer.
Return ONLY a JSON array, no markdown. Each item must have the keys:
"domain" (exactly "{domain}"), "question", "options" (array of 4 strings),
"answer" (0-based index of the correct option), "explanation" (1-2 sentences)."""

    response = client.messages.create(
        model=model,
        max_tokens=2500,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text.strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.MULTILINE).strip()

    items = json.loads(text)
    valid = [q for q in items if is_valid_question(q)]
    if not valid:
        raise ValueError("The AI response contained no valid questions.")
    return valid