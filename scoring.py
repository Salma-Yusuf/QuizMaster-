def calculate_score(answers):
    score = sum(1 for item in answers if item.get("selected") == item.get("correct"))
    total = len(answers)
    percentage = (score / total * 100) if total else 0.0
    return score, percentage


def performance_classification(percentage):
    if percentage >= 80:
        return "Excellent"
    if percentage >= 60:
        return "Good"
    if percentage >= 40:
        return "Fair"
    return "Needs Improvement"


def get_wrong_answers(answers):
    return [item for item in answers if item.get("selected") != item.get("correct")]
