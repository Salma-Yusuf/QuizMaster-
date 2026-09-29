import json
import os
import re

try:
    from google import genai
except ImportError:
    genai = None


def _client():
    if genai is None:
        raise RuntimeError("Install the Gemini package with: pip install google-genai")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    return genai.Client(api_key=api_key)


def ask_ai(prompt, model=None):
    client = _client()
    model = model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    response = client.models.generate_content(model=model, contents=prompt)
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()


def explain_answer(question, selected, correct, options):
    prompt = (
        "You are QuizMaster's educational quiz tutor. Explain the following multiple-choice "
        "question briefly and clearly. Explain why the correct answer is correct and why the "
        "student's answer was not correct. Do not invent facts.\n\n"
        f"Question: {question}\n"
        f"Options: {json.dumps(options, ensure_ascii=False)}\n"
        f"Student answer: {selected}\n"
        f"Correct answer: {correct}\n"
    )
    return ask_ai(prompt)


def analyze_performance(result):
    prompt = (
        "You are QuizMaster's educational performance assistant. Analyze this quiz result "
        "and provide concise feedback with strengths, weak areas, and three practical study "
        "recommendations. Do not make unsupported claims.\n\n"
        f"{json.dumps(result, indent=2, ensure_ascii=False)}"
    )
    return ask_ai(prompt)


def generate_practice_questions(topic, difficulty="Medium", amount=5):
    amount = max(1, min(int(amount), 10))
    prompt = (
        f"Create {amount} multiple-choice practice questions about {topic}. "
        f"Difficulty: {difficulty}. Return ONLY a JSON array. Each item must have "
        "question, options (object with A/B/C/D), answer (A/B/C/D), category, and difficulty. "
        "Do not include explanations or markdown."
    )
    text = ask_ai(prompt)
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE)
    try:
        questions = json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Gemini returned invalid JSON. Try again.") from exc

    if not isinstance(questions, list):
        raise RuntimeError("Gemini did not return a JSON list of questions.")

    cleaned = []
    for item in questions:
        if not isinstance(item, dict):
            continue
        options = item.get("options")
        answer = str(item.get("answer", "")).upper().strip()
        if (
            isinstance(item.get("question"), str)
            and isinstance(options, dict)
            and set(options.keys()) >= {"A", "B", "C", "D"}
            and answer in {"A", "B", "C", "D"}
        ):
            cleaned.append({
                "question": item["question"].strip(),
                "options": {k: str(options[k]) for k in "ABCD"},
                "answer": answer,
                "category": str(item.get("category") or topic),
                "difficulty": str(item.get("difficulty") or difficulty).capitalize()
            })
    if not cleaned:
        raise RuntimeError("Gemini did not return usable quiz questions.")
    return cleaned
