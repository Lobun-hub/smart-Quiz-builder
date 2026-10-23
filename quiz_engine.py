import json
import random
from collections import defaultdict
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "questions.json"

DOMAINS = [
    "Cloud Concepts",
    "Azure Architecture and Services",
    "Azure Management and Governance",
]


def load_questions(path: Path = DATA_PATH) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        questions = json.load(f)

    if not isinstance(questions, list):
        raise ValueError(f"Question data in {path} must be a JSON list.")

    for index, question in enumerate(questions, start=1):
        if not is_valid_question(question):
            raise ValueError(f"Invalid question at position {index} in {path}.")

    return questions


def build_quiz(questions: list[dict], domains: list[str], n: int) -> list[dict]:
    """Pick up to n random questions from the selected domains."""
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError("n must be a non-negative integer.")

    pool = []
    for index, question in enumerate(questions, start=1):
        if not is_valid_question(question):
            raise ValueError(f"Invalid question at position {index}.")
        if question["domain"] in domains:
            pool.append(question)

    random.shuffle(pool)
    return pool[:n]


def is_valid_question(q: dict) -> bool:
    if not isinstance(q, dict):
        return False
    question = q.get("question")
    options = q.get("options")
    answer = q.get("answer")
    explanation = q.get("explanation")
    domain = q.get("domain")

    return (
        isinstance(question, str)
        and bool(question.strip())
        and isinstance(options, list)
        and len(options) >= 2
        and all(isinstance(option, str) and option.strip() for option in options)
        and isinstance(answer, int)
        and not isinstance(answer, bool)
        and 0 <= answer < len(options)
        and isinstance(explanation, str)
        and domain in DOMAINS
    )


def score_by_domain(quiz: list[dict], results: dict[int, int]) -> dict[str, dict]:
    """results maps question index -> chosen option index."""
    stats = defaultdict(lambda: {"correct": 0, "total": 0})
    for i, q in enumerate(quiz):
        stats[q["domain"]]["total"] += 1
        if results.get(i) == q["answer"]:
            stats[q["domain"]]["correct"] += 1
    return dict(stats)


def readiness_message(percent: float) -> str:
    if percent >= 80:
        return (
            "🟢 Strong. You're approaching exam readiness "
            "(the real pass mark is 700/1000). Keep practicing."
        )
    if percent >= 60:
        return "🟡 Getting there. Review the weak domains below, then retake."
    return "🔴 More study needed. Focus on the lowest-scoring domain first."
