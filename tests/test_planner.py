from datetime import date, timedelta

from planner import build_plan
from quiz_engine import DOMAINS

START = date(2026, 11, 1)


def test_plan_length_and_exam_day():
    exam = START + timedelta(days=10)
    plan = build_plan(exam, 45, {}, start=START)
    assert len(plan) == 10
    assert plan.iloc[-1]["Date"] == exam.isoformat()
    assert plan.iloc[-1]["Focus domain"] == "All domains"


def test_past_or_same_day_exam_gives_empty_plan():
    assert build_plan(START, 45, {}, start=START).empty
    assert build_plan(START - timedelta(days=3), 45, {}, start=START).empty


def test_weaker_domain_gets_more_days():
    accuracy = {
        "Cloud Concepts": 30.0,
        "Azure Architecture and Services": 90.0,
        "Azure Management and Governance": 90.0,
    }
    plan = build_plan(START + timedelta(days=21), 45, accuracy, start=START)
    counts = plan["Focus domain"].value_counts()
    assert counts["Cloud Concepts"] > counts["Azure Architecture and Services"]
    assert counts["Cloud Concepts"] > counts["Azure Management and Governance"]


def test_every_domain_appears_when_time_allows():
    plan = build_plan(START + timedelta(days=14), 45, {}, start=START)
    assert all(d in set(plan["Focus domain"]) for d in DOMAINS)