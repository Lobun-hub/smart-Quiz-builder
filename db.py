import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd

DB_PATH = Path(__file__).parent / "data" / "progress.db"

# Leitner boxes: days to wait before a card is shown again
BOX_INTERVALS = {1: 0, 2: 1, 3: 3, 4: 7, 5: 14}


def _conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    with _conn() as c:
        c.executescript(
            """
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                taken_at TEXT NOT NULL,
                correct INTEGER NOT NULL,
                total INTEGER NOT NULL,
                percent REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS domain_scores (
                attempt_id INTEGER NOT NULL,
                domain TEXT NOT NULL,
                correct INTEGER NOT NULL,
                total INTEGER NOT NULL,
                FOREIGN KEY (attempt_id) REFERENCES attempts(id)
            );
            CREATE TABLE IF NOT EXISTS card_progress (
                question_id INTEGER PRIMARY KEY,
                box INTEGER NOT NULL,
                next_review TEXT NOT NULL
            );
            """
        )


def save_attempt(correct: int, total: int, stats: dict) -> None:
    percent = correct / total * 100 if total else 0
    with _conn() as c:
        cur = c.execute(
            "INSERT INTO attempts (taken_at, correct, total, percent) VALUES (?, ?, ?, ?)",
            (datetime.now().isoformat(timespec="seconds"), correct, total, percent),
        )
        attempt_id = cur.lastrowid
        c.executemany(
            "INSERT INTO domain_scores (attempt_id, domain, correct, total) VALUES (?, ?, ?, ?)",
            [(attempt_id, d, s["correct"], s["total"]) for d, s in stats.items()],
        )


def get_attempts() -> pd.DataFrame:
    with _conn() as c:
        return pd.read_sql_query(
            "SELECT taken_at, correct, total, percent FROM attempts ORDER BY id", c
        )


def get_domain_totals() -> pd.DataFrame:
    with _conn() as c:
        df = pd.read_sql_query(
            "SELECT domain, SUM(correct) AS correct, SUM(total) AS total "
            "FROM domain_scores GROUP BY domain",
            c,
        )
    if not df.empty:
        df["accuracy"] = (df["correct"] / df["total"] * 100).round(1)
    return df


def get_card_progress() -> dict:
    with _conn() as c:
        rows = c.execute("SELECT question_id, box, next_review FROM card_progress").fetchall()
    return {r[0]: {"box": r[1], "next_review": r[2]} for r in rows}


def update_card(question_id: int, knew_it: bool) -> None:
    current = get_card_progress().get(question_id, {"box": 1})
    box = min(current["box"] + 1, 5) if knew_it else 1
    next_review = (date.today() + timedelta(days=BOX_INTERVALS[box])).isoformat()
    with _conn() as c:
        c.execute(
            "INSERT INTO card_progress (question_id, box, next_review) VALUES (?, ?, ?) "
            "ON CONFLICT(question_id) DO UPDATE SET box = excluded.box, next_review = excluded.next_review",
            (question_id, box, next_review),
        )