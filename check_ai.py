import os

import ai_client

print("API key found in .env:", ai_client.ai_available())
print("ANTHROPIC_AUTH_TOKEN set in system:", bool(os.getenv("ANTHROPIC_AUTH_TOKEN")))
print("ANTHROPIC_BASE_URL set in system:", os.getenv("ANTHROPIC_BASE_URL"))

if not ai_client.ai_available():
    raise SystemExit("No valid ANTHROPIC_API_KEY in .env (the placeholder does not count).")

try:
    client = ai_client.get_client()
    r = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5"),
        max_tokens=20,
        messages=[{"role": "user", "content": "Reply with the single word: ready"}],
    )
    print("✅ Connected. Model replied:", r.content[0].text)
except Exception as e:
    print("❌ Failed:", e)