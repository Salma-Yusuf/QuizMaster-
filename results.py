import json
import os
from datetime import datetime, timezone

RESULTS_FILE = "data/results.json"


def load_results():
    if not os.path.exists(RESULTS_FILE):
        return []
    try:
        with open(RESULTS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_quiz_result(result):
    results = load_results()
    result = dict(result)
    result.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
    results.append(result)
    os.makedirs("data", exist_ok=True)
    with open(RESULTS_FILE, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)


def view_student_results(username):
    results = [r for r in load_results() if r.get("username") == username]
    print("\n=== MY RESULTS ===")
    if not results:
        print("No quiz results available.")
        return
    for number, result in enumerate(results, 1):
        print(
            f"{number}. {result.get('source', 'Local')} | "
            f"{result.get('score', 0)}/{result.get('total', 0)} | "
            f"{result.get('percentage', 0):.2f}% | "
            f"{result.get('timestamp', 'N/A')}"
        )


def review_wrong_answers(username):
    results = [r for r in load_results() if r.get("username") == username]
    print("\n=== WRONG ANSWER REVIEW ===")
    if not results:
        print("No quiz results available.")
        return

    answers = results[-1].get("answers", [])
    wrong = [a for a in answers if a.get("selected") != a.get("correct")]
    if not wrong:
        print("No wrong answers in the latest quiz.")
        return

    for number, item in enumerate(wrong, 1):
        print(f"\n{number}. {item.get('question')}")
        print(f"Your answer: {item.get('selected')}")
        print(f"Correct answer: {item.get('correct')}")
