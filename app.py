import pandas as pd
import streamlit as st
import db
import time

from ai_generator import ai_available, generate_questions
from quiz_engine import (
    DOMAINS,
    build_quiz,
    load_questions,
    readiness_message,
    score_by_domain,
)

st.set_page_config(
    page_title="AZ-900 Smart Quiz Builder",
    page_icon="☁️",
    layout="centered",
)
db.init_db()


def init_state():
    defaults = {
        "quiz": [],
        "idx": 0,
        "results": {},
        "submitted": False,
        "finished": False,
        "flagged": set(),
        "started_at": None,
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)


def reset_quiz(quiz: list[dict]):
    st.session_state.quiz = quiz
    st.session_state.idx = 0
    st.session_state.results = {}
    st.session_state.submitted = False
    st.session_state.finished = False
    st.session_state.saved = False
    st.session_state.flagged = set()
    st.session_state.started_at = time.time()


def sidebar():
    st.sidebar.header("⚙️ Quiz settings")
    domains = st.sidebar.multiselect("Domains", DOMAINS, default=DOMAINS)
    n = st.sidebar.slider("Number of questions", 3, 12, 8)

    modes = ["📚 Question bank"]
    if ai_available():
        modes.append("🤖 AI-generated")
    mode = st.sidebar.radio("Question source", modes)
    if not ai_available():
        st.sidebar.caption(
            "Set ANTHROPIC_API_KEY in .env to unlock AI-generated questions."
        )

    if st.sidebar.button("🚀 Start new quiz", use_container_width=True):
        if not domains:
            st.sidebar.error("Pick at least one domain.")
            return
        if mode.startswith("🤖"):
            try:
                with st.spinner("Generating questions..."):
                    per_domain = max(1, n // len(domains))
                    quiz = []
                    for d in domains:
                        quiz += generate_questions(d, per_domain)
                reset_quiz(quiz[:n])
            except Exception as e:
                st.sidebar.error(f"AI generation failed: {e}")
        else:
            reset_quiz(build_quiz(load_questions(), domains, n))
        st.rerun()


def show_question():
    quiz = st.session_state.quiz
    i = st.session_state.idx
    q = quiz[i]

    st.progress(
        i / len(quiz),
        text=f"Question {i + 1} of {len(quiz)}  ·  {q['domain']}",
    )
    elapsed = int(time.time() - (st.session_state.started_at or time.time()))
    st.caption(f"⏱️ Elapsed: {elapsed // 60:02d}:{elapsed % 60:02d}")

    flagged = i in st.session_state.flagged
    if st.toggle("🚩 Flag for review", value=flagged, key=f"flag_{i}"):
        st.session_state.flagged.add(i)
    else:
        st.session_state.flagged.discard(i)
    st.subheader(q["question"])

    choice = st.radio(
        "Choose one answer:",
        range(len(q["options"])),
        format_func=lambda k: q["options"][k],
        index=None,
        key=f"radio_{i}",
        disabled=st.session_state.submitted,
    )

    if not st.session_state.submitted:
        if st.button("✅ Submit answer", disabled=choice is None):
            st.session_state.results[i] = choice
            st.session_state.submitted = True
            st.rerun()
    else:
        chosen = st.session_state.results[i]
        if chosen == q["answer"]:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Not quite. Correct answer: **{q['options'][q['answer']]}**")
        st.info(f"💡 {q['explanation']}")

        last = i == len(quiz) - 1
        if st.button("🏁 Finish quiz" if last else "➡️ Next question"):
            if last:
                st.session_state.finished = True
            else:
                st.session_state.idx += 1
                st.session_state.submitted = False
            st.rerun()


def show_summary():
    quiz, results = st.session_state.quiz, st.session_state.results
    correct = sum(1 for i, q in enumerate(quiz) if results.get(i) == q["answer"])
    percent = correct / len(quiz) * 100

    st.header("📊 Your results")
    st.metric("Score", f"{correct}/{len(quiz)}", f"{percent:.0f}%")
    st.write(readiness_message(percent))
    total_secs = int(time.time() - (st.session_state.started_at or time.time()))
    st.caption(f"⏱️ Total time: {total_secs // 60}m {total_secs % 60}s")

    if st.session_state.flagged:
        st.info("🚩 You flagged these questions:")
        for i in sorted(st.session_state.flagged):
            st.write(f"- {quiz[i]['question']}")

    stats = score_by_domain(quiz, results)
    # Streamlit reruns the script after interactions, so save this attempt once.
    if not st.session_state.get("saved"):
        db.save_attempt(correct, len(quiz), stats)
        st.session_state.saved = True
        st.toast("Score saved to your Readiness Tracker 📊")
    df = pd.DataFrame(
        [
            {
                "Domain": d,
                "Correct": s["correct"],
                "Total": s["total"],
                "Accuracy %": round(s["correct"] / s["total"] * 100),
            }
            for d, s in stats.items()
        ]
    ).set_index("Domain")
    st.bar_chart(df["Accuracy %"])
    st.dataframe(df)

    weak = df[df["Accuracy %"] < 70].index.tolist()
    if weak:
        st.warning("🎯 Focus your revision on: " + ", ".join(weak))

    with st.expander("🔍 Review all questions"):
        for i, q in enumerate(quiz):
            mark = "✅" if results.get(i) == q["answer"] else "❌"
            st.markdown(f"**{mark} {q['question']}**")
            st.caption(f"Answer: {q['options'][q['answer']]}. {q['explanation']}")

    if st.button("🔁 Retake with new questions"):
        reset_quiz([])
        st.rerun()


def main():
    init_state()
    st.title("☁️ AZ-900 Smart Quiz Builder")
    st.caption("Instant feedback and explanations for Azure Fundamentals prep.")
    sidebar()

    if not st.session_state.quiz:
        st.info("👈 Choose your settings in the sidebar and click **Start new quiz**.")
    elif st.session_state.finished:
        show_summary()
    else:
        show_question()


if __name__ == "__main__":
    main()