import json
import os
import random
import html
import threading

QUESTIONS_FILE = "data/questions.json"
_write_lock = threading.Lock()


class ValidationError(Exception):
    """Raised when question data is invalid. Flask routes will catch this."""
    pass




def load_questions():
    if not os.path.exists(QUESTIONS_FILE):
        return []
    try:
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_questions(questions):
    with _write_lock:
        os.makedirs(os.path.dirname(QUESTIONS_FILE) or ".", exist_ok=True)
        temp_file = QUESTIONS_FILE + ".tmp"
        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(questions, file, indent=4, ensure_ascii=False)
        os.replace(temp_file, QUESTIONS_FILE)


def create_question(question_text, options, answer, category="General", difficulty="Medium"):
    questions = load_questions()

    question_text = question_text.strip()
    if not question_text:
        raise ValidationError("Question cannot be empty.")

    options = {key: value.strip() for key, value in options.items()}
    if set(options.keys()) != {"A", "B", "C", "D"}:
        raise ValidationError("Options must be A, B, C and D.")
    if any(not value for value in options.values()):
        raise ValidationError("All options are required.")

    answer = answer.upper().strip()
    if answer not in options:
        raise ValidationError("Invalid answer.")

    category = category.strip() or "General"
    difficulty = difficulty.capitalize().strip()
    if difficulty not in {"Easy", "Medium", "Hard"}:
        raise ValidationError("Invalid difficulty.")

    next_id = max([q.get("id", 0) for q in questions] or [0]) + 1
    new_question = {
        "id": next_id,
        "question": question_text,
        "options": options,
        "answer": answer,
        "category": category,
        "difficulty": difficulty
    }
    questions.append(new_question)
    save_questions(questions)
    return new_question


def get_all_questions():
    return load_questions()


def get_question_by_id(question_id):
    for q in load_questions():
        if q.get("id") == question_id:
            return q
    return None



def delete_question(question_id):
    questions = load_questions()
    remaining = [q for q in questions if q.get("id") != question_id]
    if len(remaining) == len(questions):
        raise ValidationError("Question not found.")
    save_questions(remaining)


def update_question(question_id, data):
    """`data` is a dict, e.g. {"question": "...", "options": {"A": "..."}, "answer": "B"}"""
    questions = load_questions()

    for q in questions:
        if q.get("id") != question_id:
            continue

        text = data.get("question", "").strip()
        if text:
            q["question"] = text

        for key, value in data.get("options", {}).items():
            value = value.strip()
            if key in q["options"] and value:
                q["options"][key] = value

        answer = data.get("answer", "").upper().strip()
        if answer:
            if answer not in q["options"]:
                raise ValidationError("Invalid answer.")
            q["answer"] = answer

        category = data.get("category", "").strip()
        if category:
            q["category"] = category

        difficulty = data.get("difficulty", "").capitalize().strip()
        if difficulty:
            if difficulty not in {"Easy", "Medium", "Hard"}:
                raise ValidationError("Invalid difficulty.")
            q["difficulty"] = difficulty

        save_questions(questions)
        return q

    raise ValidationError("Question not found.")


def get_categories():
    seen = {}
    for q in load_questions():
        name = q.get("category", "General")
        seen.setdefault(name.lower(), name)
    return sorted(seen.values())



def get_quiz_questions(category=None, difficulty=None, amount=5):
    questions = load_questions()
    if category:
        questions = [q for q in questions if q.get("category", "").lower() == category.lower()]
    if difficulty:
        questions = [q for q in questions if q.get("difficulty", "").lower() == difficulty.lower()]
    random.shuffle(questions)
    return questions[:max(1, amount)]

def search_questions(category=None, difficulty=None, keyword=None):
    questions = load_questions()
    if category:
        questions = [q for q in questions if q.get("category", "").lower() == category.lower()]
    if difficulty:
        questions = [q for q in questions if q.get("difficulty", "").lower() == difficulty.lower()]
    if keyword:
        questions = [q for q in questions if keyword.lower() in q.get("question", "").lower()]
    return questions

def convert_opentdb_question(item):
    """Convert one Open Trivia DB result into our question format."""
    correct = html.unescape(item["correct_answer"])
    choices = [html.unescape(c) for c in item["incorrect_answers"]] + [correct]
    random.shuffle(choices)

    options = dict(zip("ABCD", choices))
    answer = next(key for key, value in options.items() if value == correct)

    return {
        "question": html.unescape(item["question"]),
        "options": options,
        "answer": answer,
        "category": html.unescape(item.get("category", "General")),
        "difficulty": item.get("difficulty", "medium").capitalize()
    }



def import_questions(new_questions):
    questions = load_questions()
    existing_texts = {q["question"].lower() for q in questions}
    next_id = max([q.get("id", 0) for q in questions] or [0]) + 1
    added = 0

    for q in new_questions:
        text = q.get("question", "").strip()
        if not text or text.lower() in existing_texts:
            continue  # skip empty or duplicate questions
        if len(q.get("options", {})) != 4 or q.get("answer") not in q["options"]:
            continue  # skip badly shaped questions

        q = dict(q)
        q["id"] = next_id
        next_id += 1
        questions.append(q)
        existing_texts.add(text.lower())
        added += 1

    save_questions(questions)
    return added

