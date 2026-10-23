from datetime import date

import streamlit as st

import db
from planner import build_plan
from quiz_engine import DOMAINS
from theme_manager import apply_theme

st.set_page_config(page_title="Study Planner", page_icon="📅", layout="centered")
apply_theme()
db.init_db()

st.title("📅 Personal Study Planner")
st.caption("A revision plan built from your exam date and your weakest domains.")

exam_date = st.date_input("Exam date", value=None, min_value=date.today())
minutes = st.slider("Study time per day (minutes)", 15, 180, 45, step=15)

domain_df = db.get_domain_totals()
accuracy = {}
if not domain_df.empty:
    accuracy = dict(zip(domain_df["domain"], domain_df["accuracy"]))

st.subheader("🎯 Your current accuracy")
cols = st.columns(len(DOMAINS))
for col, d in zip(cols, DOMAINS):
    value = accuracy.get(d)
    col.metric(d, f"{value:.0f}%" if value is not None else "Not tested")

if not accuracy:
    st.info("Tip: take a quiz first so the plan can focus on your weak domains. "
            "Until then, all domains are treated equally.")

if exam_date and st.button("🛠️ Generate my plan", use_container_width=True):
    plan = build_plan(exam_date, minutes, accuracy)
    if plan.empty:
        st.error("Pick an exam date in the future.")
    else:
        st.session_state.plan = plan

plan = st.session_state.get("plan")
if plan is not None and not plan.empty:
    st.subheader(f"🗓️ Your {len(plan)}-day plan")
    st.dataframe(plan, use_container_width=True, hide_index=True)
    st.download_button(
        "⬇️ Download plan as CSV",
        plan.to_csv(index=False).encode("utf-8"),
        file_name="az900_study_plan.csv",
        mime="text/csv",
    )