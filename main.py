from auth import (
    register_user,
    login_user,
    admin_login,
)

from quiz_engine import start_quiz

from results import (
    save_quiz_result,
    view_student_results,
    review_wrong_answers,
    load_results,
)

from leaderboard import show_leaderboard
from admin import admin_dashboard
from question_bank import import_questions
from api_service import fetch_questions

from scoring import (
    calculate_score,
    performance_classification,
)


# ==========================================
# AI INTEGRATION
# ==========================================

try:
    from ai_assistant import (
        analyze_performance,
        explain_answer,
        generate_practice_questions,
        generate_study_plan,
        give_hint,
    )

    AI_AVAILABLE = True

except Exception as exc:
    AI_AVAILABLE = False
    AI_IMPORT_ERROR = exc


# ==========================================
# LOCAL QUIZ
# ==========================================

def run_local_quiz(username):

    category = (
        input(
            "Category (Enter for all): "
        ).strip()
        or None
    )

    difficulty = (
        input(
            "Difficulty Easy/Medium/Hard "
            "(Enter for all): "
        ).strip()
        or None
    )

    try:
        amount = int(
            input("Number of questions: ")
        )

        if not 1 <= amount <= 50:
            raise ValueError

    except ValueError:
        print(
            "Enter a valid number from 1 to 50."
        )
        return

    try:
        result = start_quiz(
            username,
            category,
            difficulty,
            amount,
            source="local",
        )

        if result:

            result["performance"] = (
                performance_classification(
                    result["percentage"]
                )
            )

            save_quiz_result(result)

            print(
                "\nQuiz completed successfully."
            )

    except Exception as exc:
        print(
            "Quiz error:",
            exc,
        )


# ==========================================
# ONLINE API QUIZ
# ==========================================

def run_api_quiz(username):

    print("\n=== ONLINE API QUIZ ===")

    try:

        amount = int(
            input(
                "Number of questions (1-50): "
            )
        )

        if not 1 <= amount <= 50:
            raise ValueError(
                "Amount must be between 1 and 50."
            )

        difficulty = (
            input(
                "Difficulty easy/medium/hard "
                "(Enter for all): "
            ).strip()
            or None
        )

        questions = fetch_questions(
            amount,
            difficulty=difficulty,
        )

        if not questions:
            print(
                "No questions returned."
            )
            return

        import quiz_engine

        answers = []

        for number, question in enumerate(
            questions,
            1,
        ):

            selected = quiz_engine._ask_question(
                question,
                number,
                len(questions),
            )

            answers.append(
                {
                    "question":
                        question["question"],

                    "selected":
                        selected,

                    "correct":
                        question["answer"],

                    "options":
                        question["options"],

                    "category":
                        question.get(
                            "category",
                            "General",
                        ),

                    "difficulty":
                        question.get(
                            "difficulty",
                            "Medium",
                        ),
                }
            )

        score, percentage = calculate_score(
            answers
        )

        result = {
            "username":
                username,

            "score":
                score,

            "total":
                len(questions),

            "percentage":
                percentage,

            "performance":
                performance_classification(
                    percentage
                ),

            "answers":
                answers,

            "source":
                "Open Trivia DB",
        }

        save_quiz_result(result)

        print(
            f"\nScore: {score}/"
            f"{len(questions)} "
            f"({percentage:.2f}%)"
        )

        print(
            "Performance:",
            result["performance"],
        )

    except Exception as exc:

        print(
            "Online quiz unavailable:",
            exc,
        )

        print(
            "You can use the local quiz instead."
        )


# ==========================================
# GET LATEST RESULT
# ==========================================

def _latest_result(username):

    try:
        results = load_results()

    except Exception as exc:
        print(
            "Could not load results:",
            exc,
        )
        return None

    user_results = [
        result
        for result in results
        if result.get("username") == username
    ]

    return (
        user_results[-1]
        if user_results
        else None
    )


# ==========================================
# GEMINI AI MENU
# ==========================================

def ai_menu(username):

    if not AI_AVAILABLE:

        print(
            "\nAI module is not available."
        )

        print(
            "Make sure you have installed:"
        )

        print(
            "pip install google-genai python-dotenv"
        )

        print(
            "Also make sure GEMINI_API_KEY "
            "is configured in your .env file."
        )

        return

    while True:

        print(
            "\n=== GEMINI AI ASSISTANT ==="
        )

        print(
            "1. Analyze latest performance"
        )

        print(
            "2. Explain latest wrong answers"
        )

        print(
            "3. Generate practice questions"
        )

        print(
            "4. Create a study plan"
        )

        print(
            "5. Get a hint for a question"
        )

        print(
            "6. Back"
        )

        choice = input(
            "Choose an option: "
        ).strip()


        # ==================================
        # 1. PERFORMANCE ANALYSIS
        # ==================================

        if choice == "1":

            result = _latest_result(
                username
            )

            if not result:

                print(
                    "No results available."
                )

                print(
                    "Take a quiz first."
                )

                continue

            try:

                analysis = (
                    analyze_performance(
                        result
                    )
                )

                print(
                    "\n=== AI PERFORMANCE ANALYSIS ==="
                )

                print(
                    analysis
                )

            except Exception as exc:

                print(
                    "Gemini AI error:",
                    exc,
                )


        # ==================================
        # 2. WRONG ANSWER EXPLANATION
        # ==================================

        elif choice == "2":

            result = _latest_result(
                username
            )

            if not result:

                print(
                    "No results available."
                )

                print(
                    "Take a quiz first."
                )

                continue

            wrong = [

                answer

                for answer
                in result.get(
                    "answers",
                    []
                )

                if answer.get("selected")
                != answer.get("correct")
            ]

            if not wrong:

                print(
                    "No wrong answers "
                    "in the latest quiz."
                )

                continue

            print(
                "\n=== AI WRONG-ANSWER EXPLANATIONS ==="
            )

            for number, item in enumerate(
                wrong,
                1,
            ):

                print(
                    f"\nQuestion {number}:"
                )

                print(
                    item.get(
                        "question",
                        ""
                    )
                )

                try:

                    explanation = (
                        explain_answer(
                            item["question"],
                            item.get(
                                "selected",
                                ""
                            ),
                            item.get(
                                "correct",
                                ""
                            ),
                            item.get(
                                "options",
                                {}
                            ),
                        )
                    )

                    print(
                        "\nAI Explanation:"
                    )

                    print(
                        explanation
                    )

                except Exception as exc:

                    print(
                        "Gemini AI error:",
                        exc,
                    )


        # ==================================
        # 3. AI PRACTICE QUESTIONS
        # ==================================

        elif choice == "3":

            topic = input(
                "Topic: "
            ).strip()

            if not topic:

                print(
                    "Topic cannot be empty."
                )

                continue

            difficulty = input(
                "Difficulty Easy/Medium/Hard: "
            ).strip() or "Medium"

            try:

                amount = int(
                    input(
                        "Number of questions "
                        "(1-10): "
                    )
                )

                if not 1 <= amount <= 10:

                    raise ValueError(
                        "Amount must be between 1 and 10."
                    )

                questions = (
                    generate_practice_questions(
                        topic,
                        difficulty,
                        amount,
                    )
                )

                if not questions:

                    print(
                        "No questions were generated."
                    )

                    continue

                added = import_questions(
                    questions
                )

                print(
                    f"\nGenerated {len(questions)} "
                    "AI practice question(s)."
                )

                print(
                    f"Added {added} "
                    "question(s) to the local bank."
                )

            except Exception as exc:

                print(
                    "Gemini AI error:",
                    exc,
                )


        # ==================================
        # 4. AI STUDY PLAN
        # ==================================

        elif choice == "4":

            result = _latest_result(
                username
            )

            if not result:

                print(
                    "Take a quiz first so AI "
                    "can build a study plan."
                )

                continue

            try:

                days = int(
                    input(
                        "Study plan length "
                        "(1-30 days): "
                    )
                )

                if not 1 <= days <= 30:

                    raise ValueError(
                        "Days must be between 1 and 30."
                    )

                plan = generate_study_plan(
                    result,
                    days,
                )

                print(
                    "\n=== AI STUDY PLAN ==="
                )

                print(
                    plan
                )

            except Exception as exc:

                print(
                    "Gemini AI error:",
                    exc,
                )


        # ==================================
        # 5. AI HINT
        # ==================================

        elif choice == "5":

            question = input(
                "Question: "
            ).strip()

            if not question:

                print(
                    "Question cannot be empty."
                )

                continue

            options = {
                "A": input(
                    "Option A: "
                ).strip(),

                "B": input(
                    "Option B: "
                ).strip(),

                "C": input(
                    "Option C: "
                ).strip(),

                "D": input(
                    "Option D: "
                ).strip(),
            }

            try:

                hint = give_hint(
                    question,
                    options,
                )

                print(
                    "\n=== AI HINT ==="
                )

                print(
                    hint
                )

            except Exception as exc:

                print(
                    "Gemini AI error:",
                    exc,
                )


        # ==================================
        # 6. BACK
        # ==================================

        elif choice == "6":

            break

        else:

            print(
                "Invalid choice."
            )


# ==========================================
# STUDENT DASHBOARD
# ==========================================

def student_dashboard(user):

    while True:

        print(
            "\n=== STUDENT DASHBOARD ==="
        )

        print(
            f"Welcome, {user['username']}!"
        )

        print(
            "1. Local Quiz"
        )

        print(
            "2. Online API Quiz"
        )

        print(
            "3. My Results"
        )

        print(
            "4. Review Wrong Answers"
        )

        print(
            "5. Leaderboard"
        )

        print(
            "6. Gemini AI Assistant"
        )

        print(
            "7. Logout"
        )

        choice = input(
            "Choose an option: "
        ).strip()


        if choice == "1":

            run_local_quiz(
                user["username"]
            )


        elif choice == "2":

            run_api_quiz(
                user["username"]
            )


        elif choice == "3":

            view_student_results(
                user["username"]
            )


        elif choice == "4":

            review_wrong_answers(
                user["username"]
            )


        elif choice == "5":

            show_leaderboard()


        elif choice == "6":

            ai_menu(
                user["username"]
            )


        elif choice == "7":

            print(
                "Logged out."
            )

            break


        else:

            print(
                "Invalid choice."
            )


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():

    while True:

        print(
            "\n================================"
        )

        print(
            "          QUIZMASTER V2"
        )

        print(
            "================================"
        )

        print(
            "1. Register"
        )

        print(
            "2. Student Login"
        )

        print(
            "3. Admin Login"
        )

        print(
            "4. Exit"
        )

        choice = input(
            "Choose an option: "
        ).strip()


        if choice == "1":

            register_user()


        elif choice == "2":

            user = login_user()

            if user:

                student_dashboard(
                    user
                )


        elif choice == "3":

            admin = admin_login()

            if admin:

                admin_dashboard()


        elif choice == "4":

            print(
                "Thank you for using QuizMaster."
            )

            break


        else:

            print(
                "Invalid choice."
            )


if __name__ == "__main__":
    main()

These two files now match

Your "ai_assistant.py" has exactly these functions:

analyze_performance()
explain_answer()
generate_practice_questions()
generate_study_plan()
give_hint()

And this "main.py" imports and uses exactly those five functions.

So on your "feature/ai-integration" branch:

1. Replace "ai_assistant.py" with the code you supplied.
2. Replace "main.py" with the code above.
3. Commit both changes.
4. Do not merge yet.
5. Then we'll check the branch before creating the AI Pull Request.

Also, leave "scoring.py" and "results.py" alone on this branch; this "main.py" simply uses their existing functions.
