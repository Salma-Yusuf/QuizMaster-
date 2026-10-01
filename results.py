""" 
QuizMaster Advanced - Results Management

Handles:
- Saving quiz results
- Loading results
- Student result history
- Wrong-answer review
- Latest result retrieval
- Result summaries

Compatible with the existing QuizMaster project.
"""

import json
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------
# FILE LOCATION
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
RESULTS_FILE = BASE_DIR / "data" / "results.json"


class ResultsManager:
    """Object-oriented manager for QuizMaster results."""

    def __init__(self, results_file=RESULTS_FILE):
        self.results_file = Path(results_file)

    # -----------------------------------------------------
    # LOAD RESULTS
    # -----------------------------------------------------

    def load_results(self):
        """Load all saved quiz results."""

        if not self.results_file.exists():
            return []

        try:
            with self.results_file.open(
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                return data if isinstance(data, list) else []

        except (json.JSONDecodeError, OSError):
            return []

    # -----------------------------------------------------
    # SAVE ALL RESULTS
    # -----------------------------------------------------

    def save_results(self, results):
        """Save the complete results list."""

        self.results_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with self.results_file.open(
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                results,
                file,
                indent=4,
                ensure_ascii=False
            )

    # -----------------------------------------------------
    # SAVE ONE QUIZ RESULT
    # -----------------------------------------------------

    def save_quiz_result(self, result):
        """
        Save one completed quiz result.

        The original project already calls:
            save_quiz_result(result)
        """

        if not isinstance(result, dict):
            raise TypeError("result must be a dictionary.")

        saved_result = dict(result)

        saved_result.setdefault(
            "timestamp",
            datetime.now(timezone.utc).isoformat()
        )

        # Add useful result information if it isn't already
        # available.

        answers = saved_result.get("answers", [])

        if isinstance(answers, list):

            wrong_answers = [
                answer
                for answer in answers
                if isinstance(answer, dict)
                and answer.get("selected")
                != answer.get("correct")
            ]

            saved_result.setdefault(
                "correct",
                saved_result.get("score", 0)
            )

            saved_result.setdefault(
                "wrong",
                len(wrong_answers)
            )

            saved_result.setdefault(
                "unanswered",
                sum(
                    1
                    for answer in answers
                    if isinstance(answer, dict)
                    and not answer.get("selected")
                )
            )

        results = self.load_results()

        results.append(saved_result)

        self.save_results(results)

        return saved_result

    # -----------------------------------------------------
    # STUDENT RESULTS
    # -----------------------------------------------------

    def get_student_results(self, username):
        """Return all results for one student."""

        return [
            result
            for result in self.load_results()
            if result.get("username") == username
        ]

    # -----------------------------------------------------
    # LATEST RESULT
    # -----------------------------------------------------

    def get_latest_result(self, username):
        """Return the student's most recent result."""

        results = self.get_student_results(username)

        if not results:
            return None

        return results[-1]

    # -----------------------------------------------------
    # WRONG ANSWERS
    # -----------------------------------------------------

    def get_wrong_answers(self, username):
        """
        Get wrong answers from the student's latest quiz.
        """

        latest = self.get_latest_result(username)

        if not latest:
            return []

        answers = latest.get("answers", [])

        return [
            answer
            for answer in answers
            if isinstance(answer, dict)
            and answer.get("selected")
            != answer.get("correct")
        ]

    # -----------------------------------------------------
    # RESULT SUMMARY
    # -----------------------------------------------------

    def get_summary(self, username):
        """Create a summary of a student's latest result."""

        result = self.get_latest_result(username)

        if not result:
            return None

        return {
            "username": username,
            "score": result.get("score", 0),
            "total": result.get("total", 0),
            "percentage": result.get("percentage", 0),
            "performance": result.get(
                "performance",
                "Not classified"
            ),
            "source": result.get(
                "source",
                "Local"
            ),
            "timestamp": result.get(
                "timestamp",
                "N/A"
            ),
        }

    # -----------------------------------------------------
    # DELETE STUDENT RESULTS
    # -----------------------------------------------------

    def delete_student_results(self, username):
        """Delete all results belonging to a student."""

        results = self.load_results()

        remaining = [
            result
            for result in results
            if result.get("username") != username
        ]

        if len(remaining) == len(results):
            return False

        self.save_results(remaining)

        return True


# ---------------------------------------------------------
# SHARED RESULTS MANAGER
# ---------------------------------------------------------

results_manager = ResultsManager()


# ---------------------------------------------------------
# BACKWARD-COMPATIBLE FUNCTIONS
# ---------------------------------------------------------
# These are kept because main.py and leaderboard.py already
# use these functions.
# ---------------------------------------------------------


def load_results():
    """Load all results."""
    return results_manager.load_results()


def save_quiz_result(result):
    """Save a quiz result."""
    return results_manager.save_quiz_result(result)


def view_student_results(username):
    """Display a student's results."""

    results = results_manager.get_student_results(username)

    print("\n=== MY RESULTS ===")

    if not results:
        print("No quiz results available.")
        return

    for number, result in enumerate(results, 1):

        print(
            f"{number}. "
            f"{result.get('source', 'Local')} | "
            f"{result.get('score', 0)}/"
            f"{result.get('total', 0)} | "
            f"{result.get('percentage', 0):.2f}% | "
            f"{result.get('timestamp', 'N/A')}"
        )


def review_wrong_answers(username):
    """Display wrong answers from the latest quiz."""

    wrong = results_manager.get_wrong_answers(username)

    print("\n=== WRONG ANSWER REVIEW ===")

    if not wrong:
        print("No wrong answers in the latest quiz.")
        return

    for number, item in enumerate(wrong, 1):

        print(
            f"\n{number}. "
            f"{item.get('question', 'Unknown question')}"
        )

        print(
            f"Your answer: "
            f"{item.get('selected', 'No answer')}"
        )

        print(
            f"Correct answer: "
            f"{item.get('correct', 'Unknown')}"
        )


def get_latest_result(username):
    """Return the latest result for a student."""
    return results_manager.get_latest_result(username)


def get_result_summary(username):
    """Return a summary dictionary."""
    return results_manager.get_summary(username)


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    print("QuizMaster Results Manager")
    print("-" * 30)

    results = load_results()

    print(f"Saved results: {len(results)}")
