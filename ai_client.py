import os
from pathlib import Path

from dotenv import load_dotenv

# override=True makes the project's .env win over variables already set on your system
load_dotenv(Path(__file__).parent / ".env", override=True)

API_URL = "https://api.anthropic.com"


def get_api_key() -> str | None:
    key = (os.getenv("ANTHROPIC_API_KEY") or "").strip().strip('"').strip("'")
    if not key or key == "your_key_here":
        return None
    return key


def ai_available() -> bool:
    return get_api_key() is not None


def get_client():
    """Build a client that always authenticates with the API key from .env."""
    api_key = get_api_key()
    if api_key is None:
        raise ValueError(
            "ANTHROPIC_API_KEY is not set. Add your key to the project-root .env file."
        )

    import anthropic

    # A leftover bearer token in your environment overrides the API key and causes 401.
    os.environ.pop("ANTHROPIC_AUTH_TOKEN", None)
    return anthropic.Anthropic(api_key=api_key, base_url=API_URL)