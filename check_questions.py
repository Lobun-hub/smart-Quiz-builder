from collections import Counter

from quiz_engine import is_valid_question, load_questions

questions = load_questions()
problems = []

ids = Counter(q.get("id") for q in questions)
problems += [f"Duplicate id: {i}" for i, n in ids.items() if n > 1]

texts = Counter(q.get("question", "").strip().lower() for q in questions)
problems += [f"Duplicate question text: {t[:60]}..." for t, n in texts.items() if n > 1]

for q in questions:
    if not is_valid_question(q):
        problems.append(f"Invalid structure: id {q.get('id')}")

print(f"Questions: {len(questions)}")
print("Per domain:", dict(Counter(q["domain"] for q in questions)))
print("Correct-answer position spread:", dict(sorted(Counter(q["answer"] for q in questions).items())))

if problems:
    print("\n❌ Problems found:")
    for p in problems:
        print(" -", p)
    raise SystemExit(1)
print("\n✅ Question bank looks good.")