"""
QuizMaster Advanced - AI Assistant

Gemini-powered features:
- Explain wrong answers
- Analyze quiz performance
- Generate practice questions
- Generate personalized study plans
- Give short hints without revealing the answer
"""

import json
import os
import re
from typing import Any, Dict, List, Optional

try:
    from google import genai
except ImportError:
    genai = None

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def _client():
    """Create a Gemini client using GEMINI_API_KEY."""
    if genai is None:
        raise RuntimeError(
            "Gemini is not installed. Run: pip install google-genai"
        )

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Add it to your environment or .env file."
        )

    return genai.Client(api_key=api_key)


def ask_ai(prompt: str, model: Optional[str] = None) -> str:
    """Send a prompt to Gemini and return clean text."""

    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    client = _client()
    selected_model = model or DEFAULT_MODEL

    try:
        response = client.models.generate_content(
            model=selected_model,
            contents=prompt.strip(),
        )
    except Exception as exc:
        raise RuntimeError(
            f"Gemini request failed: {exc}"
        ) from exc

    text = getattr(response, "text", None)

    if not text or not text.strip():
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()


def _clean_json_response(text: str) -> str:
    """Remove Markdown code fences around JSON."""

    cleaned = text.strip()

    cleaned = re.sub(
        r"^```(?:json)?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    cleaned = re.sub(
        r"\s*```$",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    return cleaned.strip()


def explain_answer(
    question: str,
    selected: str,
    correct: str,
    options: Dict[str, Any],
) -> str:
    """Explain why the correct answer is right."""

    prompt = (
        "You are QuizMaster's educational AI tutor.\n"
        "Explain this multiple-choice question in simple language.\n"
        "State why the correct answer is correct and briefly explain "
        "why the student's selected answer is incorrect.\n"
        "Do not invent facts. If the question is ambiguous, say so.\n\n"

        f"Question: {question}\n"
        f"Options: {json.dumps(options, ensure_ascii=False)}\n"
        f"Student answer: {selected}\n"
        f"Correct answer: {correct}\n"
    )

    return ask_ai(prompt)


def give_hint(
    question: str,
    options: Dict[str, Any],
) -> str:
    """Give a hint without revealing the correct answer."""

    prompt = (
        "You are a quiz tutor.\n"
        "Give ONE short helpful hint for the question below.\n"
        "Do not reveal the correct answer or answer letter.\n"
        "Do not eliminate all options.\n"
        "Encourage the student to reason.\n\n"

        f"Question: {question}\n"
        f"Options: {json.dumps(options, ensure_ascii=False)}\n"
    )

    return ask_ai(prompt)


def analyze_performance(
    result: Dict[str, Any],
) -> str:
    """Analyze quiz performance."""

    prompt = (
        "You are QuizMaster's educational performance assistant.\n"
        "Analyze the quiz result below.\n\n"

        "Return four short sections:\n"
        "1. Strengths\n"
        "2. Weak areas\n"
        "3. What to study next\n"
        "4. Three practical study actions\n\n"

        "Use only information supported by the result.\n\n"

        f"{json.dumps(result, indent=2, ensure_ascii=False)}"
    )

    return ask_ai(prompt)


def generate_study_plan(
    result: Dict[str, Any],
    days: int = 7,
) -> str:
    """Create a personalized study plan."""

    days = max(1, min(int(days), 30))

    prompt = (
        f"Create a realistic {days}-day study plan "
        "for a quiz student.\n"

        "Use the quiz result to focus on weak areas "
        "and reinforce strengths.\n"

        "Keep each day concise and practical.\n"

        "Do not invent topics that cannot be inferred "
        "from the result.\n\n"

        f"{json.dumps(result, indent=2, ensure_ascii=False)}"
    )

    return ask_ai(prompt)


def generate_practice_questions(
    topic: str,
    difficulty: str = "Medium",
    amount: int = 5,
) -> List[Dict[str, Any]]:
    """Generate multiple-choice practice questions."""

    topic = str(topic).strip()

    if not topic:
        raise ValueError("Topic cannot be empty.")

    difficulty = (
        str(difficulty).strip().capitalize()
        or "Medium"
    )

    if difficulty not in {"Easy", "Medium", "Hard"}:
        difficulty = "Medium"

    amount = max(1, min(int(amount), 10))

    prompt = (
        f"Create {amount} multiple-choice practice questions "
        f"about {topic}.\n"

        f"Difficulty: {difficulty}.\n\n"

        "Return ONLY a JSON array.\n\n"

        "Each item must contain:\n"
        "- question: string\n"
        "- options: object with exactly A, B, C, D\n"
        "- answer: A, B, C, or D\n"
        "- category: string\n"
        "- difficulty: Easy, Medium, or Hard\n\n"

        "Do not include Markdown, explanations, "
        "or extra text."
    )

    text = _clean_json_response(
        ask_ai(prompt)
    )

    try:
        questions = json.loads(text)

    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Gemini returned invalid JSON. "
            "Please try again."
        ) from exc

    if not isinstance(questions, list):
        raise RuntimeError(
            "Gemini did not return a JSON list."
        )

    cleaned: List[Dict[str, Any]] = []

    for item in questions:

        if not isinstance(item, dict):
            continue

        question = item.get("question")
        options = item.get("options")
        answer = str(
            item.get("answer", "")
        ).upper().strip()

        if not isinstance(question, str):
            continue

        if not question.strip():
            continue

        if not isinstance(options, dict):
            continue

        if not all(
            key in options
            for key in ("A", "B", "C", "D")
        ):
            continue

        if answer not in {"A", "B", "C", "D"}:
            continue

        cleaned.append(
            {
                "question": question.strip(),

                "options": {
                    key: str(options[key]).strip()
                    for key in ("A", "B", "C", "D")
                },

                "answer": answer,

                "category": str(
                    item.get("category") or topic
                ).strip(),

                "difficulty": str(
                    item.get("difficulty") or difficulty
                ).capitalize(),
            }
        )

    if not cleaned:
        raise RuntimeError(
            "Gemini did not return usable quiz questions."
        )

    return cleaned
