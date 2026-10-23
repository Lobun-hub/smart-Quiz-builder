import random
from datetime import date

import streamlit as st

import db
from quiz_engine import DOMAINS, load_questions

st.set_page_config(page_title="Flashcard Coach", page_icon="🧠", layout="centered")
db.init_db()

st.title("🧠 Flashcard Coach")
st.caption(
    "Spaced repetition: cards you know come back later, "
    "cards you miss come back sooner."
)

questions = load_questions()
by_id = {q["id"]: q for q in questions}
progress = db.get_card_progress()

domains = st.sidebar.multiselect("Domains", DOMAINS, default=DOMAINS)


def due_card_ids() -> list[int]:
    today = date.today().isoformat()
    ids = []
    for q in questions:
        if q["domain"] not in domains:
            continue
        p = progress.get(q["id"])
        if p is None or p["next_review"] <= today:
            ids.append(q["id"])
    random.shuffle(ids)
    return ids


# --- Deck statistics ---
in_scope = [q for q in questions if q["domain"] in domains]
mastered = sum(1 for q in in_scope if progress.get(q["id"], {}).get("box", 0) >= 4)
due_now = len(due_card_ids())
c1, c2, c3 = st.columns(3)
c1.metric("Cards in scope", len(in_scope))
c2.metric("Due today", due_now)
c3.metric("Mastered", mastered)

if st.sidebar.button("🚀 Start / refresh deck", use_container_width=True):
    st.session_state.deck = due_card_ids()
    st.session_state.pos = 0
    st.session_state.revealed = False
    st.rerun()

deck = st.session_state.get("deck")
if deck is None:
    st.info("👈 Click **Start / refresh deck** in the sidebar to begin.")
    st.stop()

pos = st.session_state.get("pos", 0)
if not deck:
    st.success("🎉 No cards are due right now. Come back later or take a quiz.")
    st.stop()
if pos >= len(deck):
    st.success("✅ Deck complete! Refresh the deck to see whether more cards are due.")
    st.stop()

card = by_id[deck[pos]]
st.progress(pos / len(deck), text=f"Card {pos + 1} of {len(deck)}  ·  {card['domain']}")

with st.container(border=True):
    st.markdown("### ❓ Question")
    st.write(card["question"])

    if not st.session_state.get("revealed"):
        if st.button("👀 Reveal answer"):
            st.session_state.revealed = True
            st.rerun()
    else:
        st.markdown("### ✅ Answer")
        st.success(card["options"][card["answer"]])
        st.info(f"💡 {card['explanation']}")

if st.session_state.get("revealed"):
    left, right = st.columns(2)
    if left.button("😅 Review again", use_container_width=True):
        db.update_card(card["id"], knew_it=False)
        st.session_state.pos = pos + 1
        st.session_state.revealed = False
        st.rerun()
    if right.button("😎 I knew it", use_container_width=True):
        db.update_card(card["id"], knew_it=True)
        st.session_state.pos = pos + 1
        st.session_state.revealed = False
        st.rerun()