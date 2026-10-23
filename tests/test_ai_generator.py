import json
from types import SimpleNamespace

import pytest

import ai_client
import ai_generator
from quiz_engine import DOMAINS


def make_question(domain: str) -> dict:
    return {
        "domain": domain,
        "question": "Which service provides virtual machines?",
        "options": [
            "Azure Virtual Machines",
            "Azure Policy",
            "Azure Monitor",
            "Azure DNS",
        ],
        "answer": 0,
        "explanation": "Azure Virtual Machines provides scalable virtualized compute.",
    }


class FakeMessages:
    def __init__(self, response_text: str):
        self.response_text = response_text

    def create(self, **kwargs):
        return SimpleNamespace(
            content=[SimpleNamespace(text=self.response_text)]
        )


class FakeClient:
    def __init__(self, response_text: str):
        self.messages = FakeMessages(response_text)


def test_generate_questions_validates_domain_and_count_before_api_call(monkeypatch):
    def unexpected_api_call():
        raise AssertionError("The API should not be called for invalid input.")

    monkeypatch.setattr(ai_generator, "get_client", unexpected_api_call)

    with pytest.raises(ValueError, match="Unknown domain"):
        ai_generator.generate_questions("Unknown domain")
    with pytest.raises(ValueError, match="positive integer"):
        ai_generator.generate_questions(DOMAINS[0], 0)


def test_generate_questions_rejects_response_with_wrong_count(monkeypatch):
    response = json.dumps([make_question(DOMAINS[0])])
    monkeypatch.setattr(ai_generator, "get_client", lambda: FakeClient(response))

    with pytest.raises(ValueError, match="exactly 2 valid questions"):
        ai_generator.generate_questions(DOMAINS[0], 2)


def test_generate_questions_returns_valid_response(monkeypatch):
    response = json.dumps([make_question(DOMAINS[0]) for _ in range(2)])
    monkeypatch.setattr(ai_generator, "get_client", lambda: FakeClient(response))

    questions = ai_generator.generate_questions(DOMAINS[0], 2)

    assert len(questions) == 2
    assert all(question["domain"] == DOMAINS[0] for question in questions)


def test_get_client_requires_api_key(monkeypatch):
    monkeypatch.setattr(ai_client, "get_api_key", lambda: None)

    with pytest.raises(ValueError, match="ANTHROPIC_API_KEY is not set"):
        ai_client.get_client()
