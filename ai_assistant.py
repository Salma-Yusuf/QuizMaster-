import json
import os
import re
from typing import Any, Dict, List, Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    load_dotenv = None

try:
    from google import genai
except ImportError:
    genai = None


DEFAULT_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash"
)


def is_ai_package_available() -> bool:
    """Return True when the Gemini Python SDK is installed."""
    return genai is not None


def _client():
    """Create a Gemini client using GEMINI_API_KEY."""

    if genai is None:
        raise RuntimeError(
            "Gemini is not installed. "
            "Run: pip install google-genai"
        )

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Add it to your .env file."
        )

    return genai.Client(
        api_key=api_key
    )


def ask_ai(
    prompt: str,
    model: Optional[str] = None
) -> str:
    """Send a prompt to Gemini and return its text response."""

    if (
        not isinstance(prompt, str)
        or not prompt.strip()
    ):
        raise ValueError(
            "Prompt cannot be empty."
        )

    client = _client()

    selected_model = (
        model
        or DEFAULT_MODEL
    )

    try:
        response = client.models.generate_content(
            model=selected_model,
            contents=prompt.strip(),
        )

    except Exception as exc:
        raise RuntimeError(
            f"Gemini request failed: {exc}"
        ) from exc

    text = getattr(
        response,
        "text",
        None
    )

    if not text or not text.strip():
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()


def _clean_json_response(
    text: str
) -> str:
    """Remove common Markdown code fences around JSON."""

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
    """Explain a wrong answer in clear educational language."""

    prompt = (
        "You are QuizMaster's educational AI tutor.\n"
        "Explain this multiple-choice question "
        "briefly and clearly.\n"
        "Explain why the correct answer is correct "
        "and why the student's selected answer "
        "was not correct.\n"
        "Do not invent facts. "
        "If the question is ambiguous, say so.\n\n"

        f"Question: {question}\n"
        f"Options: "
        f"{json.dumps(options, ensure_ascii=False)}\n"
        f"Student answer: {selected}\n"
        f"Correct answer: {correct}\n"
    )

    return ask_ai(prompt)


def give_hint(
    question: str,
    options: Dict[str, Any],
) -> str:
    """Give a useful hint without revealing the answer."""

    prompt = (
        "You are QuizMaster's quiz tutor.\n"
        "Give ONE short helpful hint for "
        "the question below.\n"
        "Do not reveal the correct answer "
        "or answer letter.\n"
        "Do not eliminate all options.\n"
        "Help the student reason toward the answer.\n\n"

        f"Question: {question}\n"
        f"Options: "
        f"{json.dumps(options, ensure_ascii=False)}\n"
    )

    return ask_ai(prompt)


def analyze_performance(
    result: Dict[str, Any]
) -> str:
    """Analyze a student's latest quiz performance."""

    prompt = (
        "You are QuizMaster's educational "
        "performance assistant.\n"
        "Analyze the quiz result below.\n\n"

        "Return four short sections:\n"
        "1. Strengths\n"
        "2. Weak areas\n"
        "3. What to study next\n"
        "4. Three practical study actions\n\n"

        "Use only information supported "
        "by the result.\n\n"

        f"{json.dumps(result, indent=2, ensure_ascii=False)}"
    )

    return ask_ai(prompt)


def generate_study_plan(
    result: Dict[str, Any],
    days: int = 7,
) -> str:
    """Create a personalized study plan."""

    try:
        days = int(days)
    except (
        TypeError,
        ValueError
    ) as exc:
        raise ValueError(
            "Study plan days must be a number."
        ) from exc

    days = max(
        1,
        min(days, 30)
    )

    prompt = (
        f"Create a realistic {days}-day "
        "study plan for a quiz student.\n"
        "Use the quiz result to focus on "
        "weak areas and reinforce strengths.\n"
        "Keep each day concise and practical.\n"
        "Do not invent topics that cannot be "
        "inferred from the result.\n\n"

        f"Quiz result:\n"
        f"{json.dumps(result, indent=2, ensure_ascii=False)}"
    )

    return ask_ai(prompt)


def generate_practice_questions(
    topic: str,
    difficulty: str = "Medium",
    amount: int = 5,
) -> List[Dict[str, Any]]:
    """Generate validated multiple-choice questions."""

    topic = str(topic).strip()

    if not topic:
        raise ValueError(
            "Topic cannot be empty."
        )

    difficulty = (
        str(difficulty)
        .strip()
        .capitalize()
        or "Medium"
    )

    if difficulty not in {
        "Easy",
        "Medium",
        "Hard"
    }:
        difficulty = "Medium"

    try:
        amount = int(amount)
    except (
        TypeError,
        ValueError
    ) as exc:
        raise ValueError(
            "Question amount must be a number."
        ) from exc

    amount = max(
        1,
        min(amount, 10)
    )

    prompt = (
        f"Create {amount} multiple-choice "
        f"practice questions about {topic}.\n"
        f"Difficulty: {difficulty}.\n\n"

        "Return ONLY a JSON array.\n"

        "Each item must contain:\n"
        "- question: string\n"
        "- options: object with exactly A, B, C, D\n"
        "- answer: A, B, C, or D\n"
        "- category: string\n"
        "- difficulty: Easy, Medium, or Hard\n\n"
    )
