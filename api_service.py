import html
import json
import random
import urllib.parse
import urllib.request 

BASE_URL = "https://opentdb.com/api.php"


def fetch_questions(amount=5, category_id=None, difficulty=None):
    params = {
        "amount": min(max(int(amount), 1), 50),
        "type": "multiple",
        "encode": "url3986"
    }

    if category_id:
        params["category"] = int(category_id)

    if difficulty:
        params["difficulty"] = difficulty.lower()

    url = BASE_URL + "?" + urllib.parse.urlencode(params)

    try:
        with urllib.request.urlopen(url, timeout=12) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        raise RuntimeError(f"API request failed: {e}")

    if data.get("response_code") != 0:
        raise RuntimeError("No questions available.")

    questions = []

    for item in data["results"]:
        correct = html.unescape(
            urllib.parse.unquote(item["correct_answer"])
        )

        options = [
            html.unescape(urllib.parse.unquote(x))
            for x in item["incorrect_answers"]
        ]

        options.append(correct)
        random.shuffle(options)

        answers = dict(zip("ABCD", options))

        questions.append({
            "question": html.unescape(
                urllib.parse.unquote(item["question"])
            ),
            "options": answers,
            "answer": next(
                letter for letter, value in answers.items()
                if value == correct
            ),
            "category": item["category"],
            "difficulty": item["difficulty"].capitalize()
        })

    return questions
