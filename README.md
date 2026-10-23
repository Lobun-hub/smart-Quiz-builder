# Smart Quiz Builder

## Run on Windows

From the project folder in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
streamlit run app.py
```

The `.env` file is optional for the question bank. Add your `ANTHROPIC_API_KEY`
to enable AI-generated questions.

If PowerShell blocks virtual-environment activation, use the environment's
Python directly instead:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```
