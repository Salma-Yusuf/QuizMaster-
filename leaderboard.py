from results import load_results 

def get_performance_label(percentage):
"""Return performance category based on percentage."""

if percentage >= 80:
    return "Excellent"
elif percentage >= 60:
    return "Good"
elif percentage >= 40:
    return "Fair"
else:
    return "Needs Improvement"

def get_leaderboard():
"""Return ranked leaderboard."""

results = load_results()

ranked_results = sorted(
    results,
    key=lambda x: (
        x.get("percentage", 0),
        x.get("score", 0)
    ),
    reverse=True
)

leaderboard = []

for rank, result in enumerate(ranked_results, start=1):
    percentage = result.get("percentage", 0)

    leaderboard.append({
        "rank": rank,
        "username": result.get("username", "Unknown"),
        "score": result.get("score", 0),
        "total": result.get("total", 0),
        "percentage": percentage,
        "performance": get_performance_label(percentage)
    })

return leaderboard

def show_leaderboard(limit=None):
"""Display leaderboard."""

leaderboard = get_leaderboard()

if limit is not None:
    leaderboard = leaderboard[:limit]

print("\n===== QUIZMASTER LEADERBOARD =====")

if not leaderboard:
    print("No quiz results found.")
    return

print(
    f"{'Rank':<6}"
    f"{'Student':<20}"
    f"{'Score':<12}"
    f"{'Percent':<12}"
    f"{'Performance'}"
)

print("-" * 70)

for student in leaderboard:
    score_text = (
        f"{student['score']}/{student['total']}"
    )

    percentage_text = (
        f"{student['percentage']:.2f}%"
    )

    print(
        f"{student['rank']:<6}"
        f"{student['username']:<20}"
        f"{score_text:<12}"
        f"{percentage_text:<12}"
        f"{student['performance']}"
    )

def get_student_statistics(username):
"""Get statistics for one student."""

results = [
    r
    for r in load_results()
    if r.get("username") == username
]

if not results:
    return None

percentages = [
    r.get("percentage", 0)
    for r in results
]

scores = [
    r.get("score", 0)
    for r in results
]

# Count actual answered questions.
questions_answered = 0

for result in results:
    answers = result.get("answers", [])

    if isinstance(answers, list):
        questions_answered += sum(
            1
            for answer in answers
            if isinstance(answer, dict)
            and answer.get("selected")
        )

average_percentage = (
    sum(percentages) / len(percentages)
)

average_score = (
    sum(scores) / len(scores)
)

return {
    "username": username,
    "quizzes_taken": len(results),
    "average_percentage": average_percentage,
    "highest_percentage": max(percentages),
    "lowest_percentage": min(percentages),
    "average_score": average_score,
    "questions_answered": questions_answered,
    "performance": get_performance_label(
        average_percentage
    )
}

def show_student_statistics(username):
"""Display student statistics."""

stats = get_student_statistics(username)

if not stats:
    print("\nNo records found.")
    return

print("\n===== STUDENT STATISTICS =====")

print(
    f"Student: {stats['username']}"
)

print(
    f"Quizzes Taken: "
    f"{stats['quizzes_taken']}"
)

print(
    f"Average Score: "
    f"{stats['average_score']:.2f}"
)

print(
    f"Average Percentage: "
    f"{stats['average_percentage']:.2f}%"
)

print(
    f"Highest Percentage: "
    f"{stats['highest_percentage']:.2f}%"
)

print(
    f"Lowest Percentage: "
    f"{stats['lowest_percentage']:.2f}%"
)

print(
    f"Questions Answered: "
    f"{stats['questions_answered']}"
)

print(
    f"Performance: "
    f"{stats['performance']}"
)

def get_overall_statistics():
"""Get overall quiz statistics."""

results = load_results()

if not results:
    return None

percentages = [
    r.get("percentage", 0)
    for r in results
]

students = {
    r.get("username")
    for r in results
    if r.get("username")
}

total_questions = 0
questions_answered = 0

for result in results:
    answers = result.get("answers", [])

    if isinstance(answers, list):
        total_questions += len(answers)

        questions_answered += sum(
            1
            for answer in answers
            if isinstance(answer, dict)
            and answer.get("selected")
        )

return {
    "total_students": len(students),
    "total_quizzes": len(results),
    "average_percentage": (
        sum(percentages) / len(percentages)
    ),
    "highest_percentage": max(percentages),
    "lowest_percentage": min(percentages),
    "total_questions": total_questions,
    "questions_answered": questions_answered
}

def show_overall_statistics():
"""Display overall quiz statistics."""

stats = get_overall_statistics()

if not stats:
    print("\nNo quiz records found.")
    return

print("\n===== OVERALL STATISTICS =====")

print(
    f"Total Students: "
    f"{stats['total_students']}"
)

print(
    f"Total Quizzes: "
    f"{stats['total_quizzes']}"
)

print(
    f"Average Percentage: "
    f"{stats['average_percentage']:.2f}%"
)

print(
    f"Highest Percentage: "
    f"{stats['highest_percentage']:.2f}%"
)

print(
    f"Lowest Percentage: "
    f"{stats['lowest_percentage']:.2f}%"
)

print(
    f"Total Questions: "
    f"{stats['total_questions']}"
)

print(
    f"Questions Answered: "
    f"{stats['questions_answered']}"
)

if name == "main":
print("QuizMaster Leaderboard")
print("-" * 30)

show_leaderboard()

print()
show_overall_statistics()
