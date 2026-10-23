from datetime import date, timedelta

import db


def test_attempts_and_domain_scores_persist(monkeypatch, tmp_path):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "progress.db")
    db.init_db()

    db.save_attempt(
        2,
        3,
        {"Cloud Concepts": {"correct": 2, "total": 3}},
    )

    attempts = db.get_attempts()
    assert len(attempts) == 1
    assert attempts.iloc[0]["correct"] == 2
    assert attempts.iloc[0]["total"] == 3
    assert round(attempts.iloc[0]["percent"], 1) == 66.7

    totals = db.get_domain_totals().set_index("domain")
    assert totals.loc["Cloud Concepts", "correct"] == 2
    assert totals.loc["Cloud Concepts", "total"] == 3
    assert totals.loc["Cloud Concepts", "accuracy"] == 66.7


def test_flashcard_progress_advances_and_resets(monkeypatch, tmp_path):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "progress.db")
    db.init_db()

    question_id = 123
    db.update_card(question_id, knew_it=True)
    progress = db.get_card_progress()[question_id]
    assert progress["box"] == 2
    assert progress["next_review"] == (date.today() + timedelta(days=1)).isoformat()

    db.update_card(question_id, knew_it=False)
    progress = db.get_card_progress()[question_id]
    assert progress["box"] == 1
    assert progress["next_review"] == date.today().isoformat()
