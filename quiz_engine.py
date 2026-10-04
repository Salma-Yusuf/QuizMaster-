"""
QuizMaster V2 - Quiz Engine

Handles:
- Loading local quiz questions
- Selecting questions by category/difficulty
- Displaying questions
- Collecting student answers
- Determining the correct answer
- Calculating quiz scores
- Returning results in the format expected by main.py
"""

import random
from typing import Any, Dict, List, Optional

from question_bank import load_questions
from scoring import calculate_score, performance_classification


LETTERS = ("A", "B", "C", "D")


def _normalise_options(question: Dict[str, Any]) -> Dict[str, str]:
    """
    Convert question options into a consistent A-D dictionary.
    """

    options = question.get("options", {})

    if isinstance(options, dict):
        return {
            letter: str(options.get(letter, ""))
            for letter in LETTERS
        }

    if isinstance(options, list):
        return {
            letter: str(options[index])
            if index < len(options)
            else ""
            for index, letter in enumerate(LETTERS)
        }

    return {letter: "" for letter in LETTERS}


def _find_correct_answer(question: Dict[str, Any]) -> str:
    """
    Determine the correct answer as A, B, C, or D.

    Supports both:
    - answer: "A"
    - correct_answer: "Python"
    """

    options = _normalise_options(question)

    # Preferred QuizMaster format
    answer = question.get("answer")

    if isinstance(answer, str):
        answer = answer.strip()

        if answer.upper() in LETTERS:
            return answer.upper()

        # If answer contains the actual option text,
        # find its corresponding letter.
        for letter, text in options.items():
            if answer.lower() == text.lower():
                return letter

    # Support question banks using correct_answer
    correct_answer = question.get("correct_answer")

    if isinstance(correct_answer, str):
        correct_answer = correct_answer.strip()

        if correct_answer.upper() in LETTERS:
            return correct_answer.upper()

        for letter, text in options.items():
            if correct_answer.lower() == text.lower():
                return letter

    return "A"


def _ask_question(
    question: Dict[str, Any],
    number: int = 1,
    total: int = 1,
) -> str:
    """
    Display one question and return the student's selected letter.
    """

    options = _normalise_options(question)

    print()
    print("=" * 60)
    print(f"Question {number}/{total}")
    print("=" * 60)
    print(question.get("question", "No question text available."))
    print()

    for letter in LETTERS:
        print(f"{letter}. {options[letter]}")

    print()

    while True:
        selected = input("Your answer (A-D): ").strip().upper()

        if selected in LETTERS:
            return selected

        print("Invalid answer. Please enter A, B, C, or D.")


def _matches_category(
    question: Dict[str, Any],
    category: Optional[str],
) -> bool:
    """Check whether a question matches the requested category."""

    if not category:
        return True

    question_category = str(
        question.get("category", "")
    ).strip().lower()

    return question_category == category.strip().lower()


def _matches_difficulty(
    question: Dict[str, Any],
    difficulty: Optional[str],
) -> bool:
    """Check whether a question matches the requested difficulty."""

    if not difficulty:
        return True

    question_difficulty = str(
        question.get("difficulty", "")
    ).strip().lower()

    return (
        question_difficulty
        == difficulty.strip().lower()
    )


def get_quiz_questions(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    amount: int = 10,
) -> List[Dict[str, Any]]:
    """
    Load and select local quiz questions.
    """

    if not isinstance(amount, int):
        raise TypeError("amount must be an integer.")

    if amount < 1:
        raise ValueError("amount must be at least 1.")

    questions = load_questions()

    if not isinstance(questions, list):
        return []

    filtered = [
        question
        for question in questions
        if isinstance(question, dict)
        and _matches_category(question, category)
        and _matches_difficulty(question, difficulty)
    ]

    random.shuffle(filtered)

    return filtered[:amount]


def start_quiz(
    username: str,
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    amount: int = 10,
    source: str = "local",
) -> Optional[Dict[str, Any]]:
    """
    Run a complete local quiz.

    Returns a result dictionary compatible with main.py
    and results.py.
    """

    questions = get_quiz_questions(
        category=category,
        difficulty=difficulty,
        amount=amount,
    )

    if not questions:
        print(
            "\nNo questions were found "
            "for the selected category/difficulty."
        )
        return None

    print()
    print("=" * 60)
    print("QUIZMASTER QUIZ")
    print("=" * 60)
    print(f"Student: {username}")
    print(f"Questions: {len(questions)}")

    if category:
        print(f"Category: {category}")

    if difficulty:
        print(f"Difficulty: {difficulty}")

    print("=" * 60)

    answers: List[Dict[str, Any]] = []

    for number, question in enumerate(
        questions,
        start=1,
    ):
        options = _normalise_options(question)

        # IMPORTANT:
        # The correct answer is determined from the
        # question itself, not from the option position.
        correct = _find_correct_answer(question)

        selected = _ask_question(
            question,
            number,
            len(questions),
        )

        answers.append(
            {
                "question": question.get(
                    "question",
                    "",
                ),
                "selected": selected,
                "correct": correct,
                "options": options,
                "category": question.get(
                    "category",
                    "General",
                ),
                "difficulty": question.get(
                    "difficulty",
                    "Medium",
                ),
            }
        )

    score, percentage = calculate_score(
        answers
    )

    result = {
        "username": username,
        "score": score,
        "total": len(questions),
        "percentage": percentage,
        "performance": performance_classification(
            percentage
        ),
        "answers": answers,
        "source": source,
    }

    print()
    print("=" * 60)
    print("QUIZ COMPLETE")
    print("=" * 60)
    print(
        f"Score: {score}/{len(questions)} "
        f"({percentage:.2f}%)"
    )
    print(
        "Performance:",
        result["performance"],
    )
    print("=" * 60)

    return result


if __name__ == "__main__":
    print("QuizMaster quiz_engine.py")
    print("Module loaded successfully.")