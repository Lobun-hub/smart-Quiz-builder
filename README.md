# AZ-900 Smart Quiz Builder

A Streamlit study suite for preparing for the Microsoft Azure Fundamentals
(AZ-900) exam. Practice with the included question bank, review flashcards,
track quiz results, and plan your study sessions.

## Features

- **Quiz Builder:** choose exam domains and take a 3- to 12-question quiz.
  Get an explanation after each answer, track elapsed time, flag questions for
  review, and see your score broken down by domain.
- **Question sources:** use the built-in question bank without an API key, or
  generate questions with the Anthropic API when a key is configured.
- **Flashcard Coach:** review due questions with spaced repetition. Cards you
  know move through Leitner boxes; cards you miss return sooner.
- **Readiness Tracker:** save quiz attempts, view score history and domain
  accuracy, and see an approximate readiness estimate and exam countdown.
- **Study Buddy:** use built-in explanations for five common AZ-900 topics
  offline, or enable Anthropic-generated answers with an API key. Offline
  answers cover IaaS/PaaS/SaaS, Availability Zones, Azure Policy vs. RBAC,
  the shared responsibility model, and CapEx vs. OpEx.
- **Study Planner:** create a day-by-day plan based on your exam date, study
  time, and weakest domains; download the plan as CSV.
- **Appearance:** select the Ocean, Forest, or Desert color theme and toggle
  light or dark mode from the sidebar. The selection is shared across pages
  for the current app session.

## Requirements

- Python 3.10 or newer
- Dependencies listed in `requirements.txt`
- An Anthropic API key is optional. Without one, the question bank, offline
  Study Buddy, flashcards, tracker, and planner remain available.

## Run locally

Create a virtual environment and install the application dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

On macOS or Linux, activate the environment with:

```bash
source .venv/bin/activate
```

Alternatively, on Windows run Streamlit through the environment directly:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the local URL printed by Streamlit (by default,
`http://localhost:8501`).

## Enable Anthropic features (optional)

Copy `.env.example` to `.env` in the project root and set your own API key:

```dotenv
ANTHROPIC_API_KEY=your_actual_key_here
ANTHROPIC_MODEL=claude-sonnet-5-5
```

Replace the placeholder with a key issued by Anthropic. Never commit or share
your real key. `.env` is excluded from Git; `.env.example` is a template, not a
working credential. Restart Streamlit after changing `.env`. For a hosted
deployment, configure the key as a private environment variable or secret.

The key enables AI-generated quiz questions and generated Study Buddy replies.
The built-in question bank and offline Study Buddy do not require it.

## Question bank and saved data

- The included AZ-900 practice questions are stored in
  `data/questions.json`. The bank is checked for valid JSON and valid question
  structure when loaded.
- Quiz attempts, domain scores, and flashcard review progress are stored in
  `data/progress.db`, a local SQLite database created automatically.
- Keep a backup of `data/progress.db` if you want to preserve local progress.
  It is excluded from Git.

## Run tests

Install the development dependency and run the test suite:

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest
```

## Tech stack

Python, Streamlit, SQLite, pandas, and the optional Anthropic API.

## Disclaimer

Practice material only; it is not affiliated with or endorsed by Microsoft.
Always confirm current exam objectives and product details on Microsoft Learn.
