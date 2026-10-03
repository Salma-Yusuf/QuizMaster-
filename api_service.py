"""
QuizMaster V2 - Open Trivia DB API Integration

Handles:
- Connecting to Open Trivia DB
- Retrieving live multiple-choice questions
- Processing JSON responses
- Converting API questions to QuizMaster format
- Decoding API text
- Validating API inputs
- Handling API/network errors
"""

import html
import json
import random
import urllib.error
import urllib.parse
import urllib.request


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

BASE_URL = "https://opentdb.com/api.php"
CATEGORY_URL = "https://opentdb.com/api_category.php"

DEFAULT_AMOUNT = 5
MIN_AMOUNT = 1
MAX_AMOUNT = 50
REQUEST_TIMEOUT = 12

VALID_DIFFICULTIES = {
    "easy",
    "medium",
    "hard"
}


# ---------------------------------------------------------
# CUSTOM ERROR
# ---------------------------------------------------------

class APIServiceError(Exception):
    """Raised when the Open Trivia DB service cannot be used."""
    pass


# ---------------------------------------------------------
# TEXT / INPUT HELPERS
# ---------------------------------------------------------

def _decode_text(value):
    """Decode URL and HTML encoded text."""

    if value is None:
        return ""

    return html.unescape(
        urllib.parse.unquote(str(value))
    )


def _validate_amount(amount):
    """Validate the requested number of questions."""

    try:
        amount = int(amount)

    except (TypeError, ValueError):
        raise APIServiceError(
            "Number of questions must be a valid integer."
        )

    if not MIN_AMOUNT <= amount <= MAX_AMOUNT:
        raise APIServiceError(
            f"Number of questions must be between "
            f"{MIN_AMOUNT} and {MAX_AMOUNT}."
        )

    return amount


def _validate_difficulty(difficulty):
    """Validate optional difficulty."""

    if difficulty is None:
        return None

    difficulty = str(difficulty).strip().lower()

    if not difficulty:
        return None

    if difficulty not in VALID_DIFFICULTIES:
        raise APIServiceError(
            "Difficulty must be easy, medium, or hard."
        )

    return difficulty


def _validate_category(category_id):
    """Validate optional Open Trivia DB category ID."""

    if category_id is None or category_id == "":
        return None

    try:
        category_id = int(category_id)

    except (TypeError, ValueError):
        raise APIServiceError(
            "Category ID must be a valid integer."
        )

    if category_id <= 0:
        raise APIServiceError(
            "Category ID must be greater than zero."
        )

    return category_id


# ---------------------------------------------------------
# HTTP HELPER
# ---------------------------------------------------------

def _get_json(url):
    """Make a GET request and return decoded JSON."""

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "QuizMaster-V2/1.0"
        }
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=REQUEST_TIMEOUT
        ) as response:

            status = getattr(
                response,
                "status",
                200
            )

            if status != 200:
                raise APIServiceError(
                    f"Open Trivia DB returned HTTP {status}."
                )

            body = response.read().decode(
                "utf-8"
            )

    except urllib.error.HTTPError as exc:

        raise APIServiceError(
            f"Open Trivia DB HTTP error: {exc.code}."
        )

    except urllib.error.URLError as exc:

        raise APIServiceError(
            f"Could not connect to Open Trivia DB: "
            f"{exc.reason}"
        )

    except TimeoutError:

        raise APIServiceError(
            "Open Trivia DB request timed out."
        )

    except OSError as exc:

        raise APIServiceError(
            f"Network error while contacting "
            f"Open Trivia DB: {exc}"
        )

    try:

        return json.loads(body)

    except json.JSONDecodeError:

        raise APIServiceError(
            "Open Trivia DB returned invalid JSON."
        )


# ---------------------------------------------------------
# API RESPONSE CODES
# ---------------------------------------------------------

def _response_code_message(response_code):
    """Convert API response codes into useful messages."""

    messages = {
        0: "Success.",
        1: "Not enough questions are available.",
        2: "Invalid API parameters.",
        3: "Session token was not found.",
        4: "Session token has expired.",
        5: "Too many requests. Please try again later."
    }

    return messages.get(
        response_code,
        f"Unknown Open Trivia DB response code: "
        f"{response_code}"
    )


# ---------------------------------------------------------
# QUESTION CONVERSION
# ---------------------------------------------------------

def _convert_question(item):
    """
    Convert one Open Trivia DB question into
    QuizMaster format.
    """

    if not isinstance(item, dict):

        raise APIServiceError(
            "Invalid question received from "
            "Open Trivia DB."
        )

    question_text = _decode_text(
        item.get("question")
    )

    correct_answer = _decode_text(
        item.get("correct_answer")
    )

    incorrect_answers = [
        _decode_text(answer)
        for answer in item.get(
            "incorrect_answers",
            []
        )
    ]

    if not question_text:

        raise APIServiceError(
            "API returned a question without "
            "question text."
        )

    if not correct_answer:

        raise APIServiceError(
            "API returned a question without "
            "a correct answer."
        )

    if len(incorrect_answers) != 3:

        raise APIServiceError(
            "API did not return exactly three "
            "incorrect answers."
        )

    options = (
        incorrect_answers
        + [correct_answer]
    )

    random.shuffle(options)

    option_map = dict(
        zip(
            ("A", "B", "C", "D"),
            options
        )
    )

    answer_letter = next(
        letter
        for letter, value in option_map.items()
        if value == correct_answer
    )

    return {
        "question": question_text,

        "options": option_map,

        "answer": answer_letter,

        "category": _decode_text(
            item.get(
                "category",
                "General"
            )
        ),

        "difficulty": str(
            item.get(
                "difficulty",
                "medium"
            )
        ).capitalize()
    }


# ---------------------------------------------------------
# MAIN API FUNCTION
# ---------------------------------------------------------

def fetch_questions(
    amount=DEFAULT_AMOUNT,
    category_id=None,
    difficulty=None
):
    """
    Fetch live multiple-choice questions
    from Open Trivia DB.

    Returns:
        list: QuizMaster-formatted questions.
    """

    amount = _validate_amount(
        amount
    )

    category_id = _validate_category(
        category_id
    )

    difficulty = _validate_difficulty(
        difficulty
    )

    params = {
        "amount": amount,
        "type": "multiple",
        "encode": "url3986"
    }

    if category_id is not None:

        params["category"] = category_id

    if difficulty is not None:

        params["difficulty"] = difficulty

    url = (
        BASE_URL
        + "?"
        + urllib.parse.urlencode(params)
    )

    payload = _get_json(url)

    response_code = payload.get(
