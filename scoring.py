 """
QuizMaster Advanced - Scoring System

Handles quiz scoring, performance classification,
wrong-answer detection, and score summaries.

Designed to remain compatible with quiz_engine.py
and main.py.
"""

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class ScoreResult:
    """Represents the complete result of a quiz."""

    score: int
    total: int
    percentage: float
    performance: str
    wrong_answers: List[Dict[str, Any]]

    @property
    def correct(self) -> int:
        """Number of correct answers."""
        return self.score

    @property
    def wrong(self) -> int:
        """Number of wrong answers."""
        return len(self.wrong_answers)


class ScoringService:
    """Object-oriented scoring service for QuizMaster."""

    @staticmethod
    def calculate_score(answers):
        """
        Calculate the number of correct answers and percentage.

        Returns:
            tuple: (score, percentage)
        """

        if not isinstance(answers, list):
            raise TypeError("answers must be a list.")

        total = len(answers)

        if total == 0:
            return 0, 0.0

        score = sum(
            1
            for item in answers
            if isinstance(item, dict)
            and item.get("selected") == item.get("correct")
        )

        percentage = (score / total) * 100

        return score, round(percentage, 2)

    @staticmethod
    def performance_classification(percentage):
        """
        Classify quiz performance.
        """

        try:
            percentage = float(percentage)
        except (TypeError, ValueError):
            percentage = 0.0

        if percentage >= 80:
            return "Excellent"

        if percentage >= 60:
            return "Good"

        if percentage >= 40:
            return "Fair"

        return "Needs Improvement"

    @staticmethod
    def get_wrong_answers(answers):
        """
        Return all incorrectly answered questions.
        """

        if not isinstance(answers, list):
            return []

        return [
            item
            for item in answers
            if isinstance(item, dict)
            and item.get("selected") != item.get("correct")
        ]

    @classmethod
    def generate_result(cls, answers):
        """
        Generate a complete ScoreResult object.
        """

        score, percentage = cls.calculate_score(answers)

        wrong_answers = cls.get_wrong_answers(answers)

        performance = cls.performance_classification(
            percentage
        )

        return ScoreResult(
            score=score,
            total=len(answers),
            percentage=percentage,
            performance=performance,
            wrong_answers=wrong_answers,
        )


# ---------------------------------------------------------
# BACKWARD-COMPATIBLE FUNCTIONS
# ---------------------------------------------------------
# These functions are kept because the existing project
# already imports them from scoring.py.
# ---------------------------------------------------------


def calculate_score(answers):
    """Calculate score while keeping the original API."""
    return ScoringService.calculate_score(answers)


def performance_classification(percentage):
    """Classify performance while keeping the original API."""
    return ScoringService.performance_classification(percentage)


def get_wrong_answers(answers):
    """Find wrong answers while keeping the original API."""
    return ScoringService.get_wrong_answers(answers)


def generate_score_result(answers):
    """
    Convenience function for the upgraded system.

    Returns:
        ScoreResult
    """

    return ScoringService.generate_result(answers)


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    sample_answers = [
        {
            "question": "What is 2 + 2?",
            "selected": "A",
            "correct": "A",
        },
        {
            "question": "What is Python?",
            "selected": "B",
            "correct": "C",
        },
    ]

    result = generate_score_result(sample_answers)

    print("QuizMaster Scoring Test")
    print("-" * 30)
    print(f"Score: {result.score}/{result.total}")
    print(f"Percentage: {result.percentage}%")
    print(f"Performance: {result.performance}")
    print(f"Wrong answers: {result.wrong}")
