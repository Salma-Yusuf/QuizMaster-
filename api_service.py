import html
import json
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
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        raise RuntimeError(f"API request failed: {exc}")

    if payload.get("response_code") != 0:
        raise RuntimeError(
            f"Open Trivia DB returned response code {payload.get('response_code')}"
        )

    converted = []
    for item in payload.get("results", []):
        correct = html.unescape(urllib.parse.unquote(item["correct_answer"]))
        incorrect = [
            html.unescape(urllib.parse.unquote(value))
            for value in item["incorrect_answers"]
        ]

        options = incorrect + [correct]
        # Avoid importing random globally just for this small shuffle.
        import random
        random.shuffle(options)

        option_map = dict(zip(["A", "B", "C", "D"], options))
        answer_letter = next(k for k, v in option_map.items() if v == correct)

        converted.append({
            "question": html.unescape(urllib.parse.unquote(item["question"])),
            "options": option_map,
            "answer": answer_letter,
            "category": html.unescape(urllib.parse.unquote(item["category"])),
            "difficulty": item["difficulty"].capitalize()
        })

    return converted
