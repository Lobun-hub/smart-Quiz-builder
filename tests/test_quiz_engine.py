from quiz_engine import (
    DOMAINS,
    build_quiz,
    is_valid_question,
    load_questions,
    readiness_message,
    score_by_domain,
)


def test_bank_is_valid_and_ids_unique():
    qs = load_questions()
    assert all(is_valid_question(q) for q in qs)
    assert len({q["id"] for q in qs}) == len(qs)


def test_build_quiz_respects_domain_and_count():
    qs = load_questions()
    quiz = build_quiz(qs, ["Cloud Concepts"], 5)
    assert len(quiz) == 5
    assert all(q["domain"] == "Cloud Concepts" for q in quiz)


def test_build_quiz_caps_at_pool_size():
    qs = load_questions()
    assert len(build_quiz(qs, DOMAINS, 10_000)) == len(qs)


def test_score_by_domain():
    quiz = [
        {"domain": "Cloud Concepts", "answer": 1},
        {"domain": "Cloud Concepts", "answer": 0},
        {"domain": "Azure Architecture and Services", "answer": 2},
    ]
    stats = score_by_domain(quiz, {0: 1, 1: 3, 2: 2})
    assert stats["Cloud Concepts"] == {"correct": 1, "total": 2}
    assert stats["Azure Architecture and Services"] == {"correct": 1, "total": 1}


def test_readiness_message_bands():
    assert readiness_message(85).startswith("🟢")
    assert readiness_message(65).startswith("🟡")
    assert readiness_message(30).startswith("🔴")


def test_invalid_question_detected():
    bad = {"question": "x", "options": ["a", "b"], "answer": 5,
           "explanation": "e", "domain": "Cloud Concepts"}
    assert not is_valid_question(bad)