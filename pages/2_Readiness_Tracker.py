from datetime import date

import streamlit as st
import db
from quiz_engine import DOMAINS
from quiz_engine import DOMAINS
from theme_manager import apply_theme

st.set_page_config(page_title="Readiness Tracker", page_icon="📊", layout="centered")
apply_theme()
db.init_db()

# Approximate AZ-900 skills-measured weights (midpoints of Microsoft's ranges).
# Check the official AZ-900 study guide, because Microsoft updates these.
WEIGHTS = {
    "Cloud Concepts": 0.28,
    "Azure Architecture and Services": 0.37,
    "Azure Management and Governance": 0.35,
}

st.title("📊 Readiness Tracker")
st.caption("Your saved quiz scores, turned into a readiness estimate.")

attempts = db.get_attempts()
if attempts.empty:
    st.info(
        "No attempts yet. Finish a quiz on the main page "
        "and your score will appear here."
    )
    st.stop()

domain_df = db.get_domain_totals().set_index("domain")

# Recent form: average of the last 3 attempts
recent = attempts.tail(3)["percent"].mean()

# Weighted score across the domains you have practiced
covered = [d for d in DOMAINS if d in domain_df.index]
weight_sum = sum(WEIGHTS[d] for d in covered)
weighted = (
    sum(WEIGHTS[d] * domain_df.loc[d, "accuracy"] for d in covered) / weight_sum
)

estimate = round(0.5 * recent + 0.5 * weighted, 1)

c1, c2, c3 = st.columns(3)
c1.metric("Readiness estimate", f"{estimate}%")
c2.metric("Last 3 quizzes", f"{recent:.0f}%")
c3.metric("Attempts", len(attempts))

if len(attempts) < 3:
    st.warning("Take at least 3 quizzes for a more reliable estimate.")
if estimate >= 80:
    st.success(
        "🟢 Looking ready. Do a final review of any weak domain "
        "and book the exam."
    )
elif estimate >= 65:
    st.warning("🟡 Almost there. Target your weakest domain, then retest.")
else:
    st.error(
        "🔴 Not ready yet. Study the weakest domain below "
        "and use the Flashcard Coach daily."
    )

st.subheader("📈 Score history")
st.line_chart(attempts.set_index("taken_at")["percent"])

st.subheader("🎯 Accuracy by domain")
st.bar_chart(domain_df["accuracy"])
weakest = domain_df["accuracy"].idxmin()
st.write(
    f"Weakest domain so far: **{weakest}** "
    f"({domain_df.loc[weakest, 'accuracy']}%)."
)

st.subheader("📅 Exam countdown")
exam_date = st.date_input("When is your exam?", value=None, min_value=date.today())
if exam_date:
    days_left = (exam_date - date.today()).days
    st.metric("Days left", days_left)
    if estimate < 80 and days_left > 0:
        st.write(
            "To close the gap, aim for roughly one quiz per day "
            "plus a daily flashcard "
            f"round, focusing on **{weakest}** first."
        )

with st.expander("🗂️ Raw attempt log"):
    st.dataframe(attempts, use_container_width=True)