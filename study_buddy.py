import os

from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are an AZ-900 (Microsoft Azure Fundamentals) study buddy.
Explain cloud concepts in simple, friendly language for beginners.
Rules:
- Start with a one-sentence plain-English definition.
- Then give a short real-world analogy.
- Then add 2-3 bullet points on what the AZ-900 exam typically tests about it.
- Keep answers under 200 words unless the learner asks for more depth.
- If you are unsure about a recent Azure change (names, pricing, limits), say so and
  point the learner to Microsoft Learn rather than guessing.
- Politely steer off-topic questions back to Azure or cloud fundamentals."""


def buddy_available() -> bool:
    return bool(os.getenv("ANTHROPIC_API_KEY"))


def ask_buddy(history: list[dict]) -> str:
    """history is a list of {"role": "user"|"assistant", "content": str}."""
    import anthropic

    client = anthropic.Anthropic()
    model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5")
    response = client.messages.create(
        model=model,
        max_tokens=800,
        system=SYSTEM_PROMPT,
        messages=history,
    )
    return response.content[0].text