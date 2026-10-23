# ☁️ AZ-900 Smart Quiz Builder

An AI-powered study suite for the Microsoft Azure Fundamentals (AZ-900) exam,
built for the Vibe Coding Hackathon: AZ-900 Exam Prep Edition.

## Features
- 📝 **Smart Quiz Builder**: instant feedback and explanations, optional AI-generated questions
- ⏱️ Exam timer and flag-for-review
- 🧠 **Flashcard Coach**: Leitner-box spaced repetition
- 📊 **Readiness Tracker**: saved scores, weighted readiness estimate, exam countdown
- 🤖 **Study Buddy**: built-in explanations work offline; an Anthropic API key
  enables generated answers
- 📅 **Study Planner**: day-by-day plan weighted toward your weak domains
- 🎨 **Color themes**: choose Ocean, Forest or Desert, with light and dark modes

Choose the color theme and toggle dark mode from the **Appearance** section in
the sidebar. Your selection is shared across the app pages for the current
session.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env     # optional: add ANTHROPIC_API_KEY
streamlit run app.py
```

## Tech stack
Python, Streamlit, SQLite, pandas, Anthropic API.

## Demo script (2 minutes)
1. Take an 8-question quiz and show the instant explanations.
2. Open the Readiness Tracker and show the saved score.
3. Open the Study Planner, enter an exam date, generate and download the plan.
4. Ask the AI Study Buddy to explain "Availability Zones".
5. Review cards in the Flashcard Coach.

## Disclaimer
Practice material only. Always confirm exam objectives on Microsoft Learn.