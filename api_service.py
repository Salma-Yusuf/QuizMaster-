import html
import json
import random
import urllib.error
import urllib.parse
import urllib.request


BASE_URL = "https://opentdb.com/api.php"
CATEGORY_URL = "https://opentdb.com/api_category.php"

MIN_AMOUNT = 1
MAX_AMOUNT = 50
TIMEOUT = 12

VALID_DIFFICULTIES = {"easy", "medium", "hard"}


class APIServiceError(Exception):
    """Raised when the Open Trivia DB service cannot be used."""
    pass


def _decode_text(value):
    """Decode URL and HTML encoded text."""
    if value is None:
        return ""

    return html.unescape(
        urllib.parse.unquote(str(value))
    )


def _get_json(url):
    """Send a GET request and return decoded JSON."""
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as response:
            return json.loads(response.read().decode("utf-8"))

    except urllib.error.HTTPError as exc:
        raise APIServiceError(
            f"Open Trivia DB HTTP error: {exc.code}"
        ) from exc

    except urllib.error.URLError as exc:
        raise APIServiceError(
            f"Unable to connect to Open Trivia DB: {exc.reason}"
        ) from exc

    except json.JSONDecodeError as exc:
        raise APIServiceError(
            "Open Trivia DB returned invalid JSON."
        ) from exc

    except Exception as exc:
        raise APIServiceError(
            f"API request failed: {exc}"
        ) from exc


def _validate_amount(amount):
    """Validate the requested number of questions."""
    try:
        amount = int(amount)
    except (TypeError, ValueError) as exc:
        raise APIServiceError(
            "Number of questions must be a valid integer."
        ) from exc

    if not MIN_AMOUNT <= amount <= MAX_AMOUNT:
        raise APIServiceError(
            f"Number of questions must be between "
            f"{MIN_AMOUNT} and {MAX_AMOUNT}."
        )

    return amount


def validate_difficulty(difficulty):
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
    except (TypeError, ValueError) as exc:
        raise APIServiceError(
            "Category ID must be a valid integer."
        ) from exc

    if category_id <= 0:
        raise APIServiceError(
            "Category ID must be greater than zero."
        )

    return category_id


def _response_error_message(response_code):
    """Convert Open Trivia DB response codes into useful messages."""
    messages = {
        1: "No results were returned for the requested quiz.",
        2: "The API request contained an invalid parameter.",
        3: "The requested session token was not found.",
        4: "The session token has returned all available questions.",
        5: "Too many requests were made to the API. Please try again later.",
    }

    return messages.get(
        response_code,
        f"Open Trivia DB returned response code {response_code}."
    )


def _convert_question(item):
    """Convert one Open Trivia DB question to QuizMaster format."""
    if not isinstance(item, dict):
        raise APIServiceError("Invalid question received from API.")

    question_text = _decode_text(item.get("question"))
    correct = _decode_text(item.get("correct_answer"))

    incorrect_values = item.get("incorrect_answers", [])

    if not isinstance(incorrect_values, list):
        raise APIServiceError("Invalid incorrect answer data.")

    incorrect = [
        _decode_text(value)
        for value in incorrect_values
    ]

    if len(incorrect) != 3 or not correct:
        raise APIServiceError(
            "Only multiple-choice questions with four options are supported."
        )

    options = incorrect + [correct]
    random.shuffle(options)

    option_letters = ["A", "B", "C", "D"]
    option_map = dict(zip(option_letters, options))

    answer_letter = next(
        letter
        for letter, value in option_map.items()
        if value == correct
    )

    return {
        "question": question_text,
        "options": option_map,
        "answer": answer_letter,
        "category": _decode_text(item.get("category")),
        "difficulty": str(
            item.get("difficulty", "medium")
        ).capitalize(),
    }


def fetch_questions(amount=5, category_id=None, difficulty=None):
    """Fetch multiple-choice questions from Open Trivia DB."""
    amount = _validate_amount(amount)
    category_id = _validate_category(category_id)
    difficulty = validate_difficulty(difficulty)

    params = {
        "amount": amount,
        "type": "multiple",
        "encode": "url3986",
    }

    if category_id is not None:
        params["category"] = category_id

    if difficulty is not None:
        params["difficulty"] = difficulty

    url = BASE_URL + "?" + urllib.parse.urlencode(params)

    payload = _get_json(url)

    response_code = payload.get("response_code")

    if response_code != 0:
        raise APIServiceError(
            _response_error_message(response_code)
        )

    results = payload.get("results", [])

    if not isinstance(results, list):
        raise APIServiceError(
            "Invalid question data was returned by Open Trivia DB."
        )

    converted_questions = []

    for item in results:
        try:
            converted_questions.append(
                _convert_question(item)
            )
        except APIServiceError:
            continue

    if not converted_questions:
        raise APIServiceError(
            "No usable multiple-choice questions were returned."
        )

    return converted_questions


def fetch_categories():
    """Retrieve available Open Trivia DB categories."""
    payload = _get_json(CATEGORY_URL)

    categories = payload.get("trivia_categories", [])

    if not isinstance(categories, list):
        raise APIServiceError(
            "Invalid category data was returned by Open Trivia DB."
        )

    return categories


if __name__ == "__main__":
    print("QUIZMASTER V2 - API INTEGRATION TEST")
    print("-" * 45)

    try:
        questions = fetch_questions(
            amount=3,
            difficulty="easy"
        )

        print("API connection successful.")
        print(f"Questions received: {len(questions)}")

        for number, question in enumerate(questions, start=1):
            print(f"\nQuestion {number}:")
            print(question["question"])

            for letter, option in question["options"].items():
                print(f"{letter}. {option}")

            print(f"Correct option: {question['answer']}")
            print(f"Category: {question['category']}")
            print(f"Difficulty: {question['difficulty']}")

    except APIServiceError as exc:
        print(f"API test failed: {exc}")
