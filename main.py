from auth import register_user, login_user, admin_login
from quiz_engine import start_quiz
from results import save_quiz_result, view_student_results, review_wrong_answers
from leaderboard import show_leaderboard
from admin import admin_dashboard
from question_bank import import_questions
from api_service import fetch_questions
from scoring import calculate_score, performance_classification

try:
    from ai_assistant import analyze_performance, explain_answer, generate_practice_questions
    AI_AVAILABLE = True
except Exception:
    AI_AVAILABLE = False


def run_local_quiz(username):
    category = input("Category (Enter for all): ").strip() or None
    difficulty = input("Difficulty Easy/Medium/Hard (Enter for all): ").strip() or None
    try:
        amount = int(input("Number of questions: "))
        if not 1 <= amount <= 50:
            raise ValueError
    except ValueError:
        print("Enter a valid number from 1 to 50.")
        return

    result = start_quiz(username, category, difficulty, amount, source="local")
    if result:
        result["performance"] = performance_classification(result["percentage"])
        save_quiz_result(result)


def run_api_quiz(username):
    print("\n=== ONLINE API QUIZ ===")
    try:
        amount = int(input("Number of questions (1-50): "))
        if not 1 <= amount <= 50:
            raise ValueError("Amount must be between 1 and 50.")
        difficulty = input("Difficulty easy/medium/hard (Enter for all): ").strip() or None
        questions = fetch_questions(amount, difficulty=difficulty)
        if not questions:
            print("No questions returned.")
            return

        import quiz_engine
        answers = []
        for number, question in enumerate(questions, 1):
            selected = quiz_engine._ask_question(question, number, len(questions))
            answers.append({
                "question": question["question"],
                "selected": selected,
                "correct": question["answer"],
                "options": question["options"],
                "category": question.get("category", "General"),
                "difficulty": question.get("difficulty", "Medium")
            })

        score, percentage = calculate_score(answers)
        result = {
            "username": username,
            "score": score,
            "total": len(questions),
            "percentage": percentage,
            "performance": performance_classification(percentage),
            "answers": answers,
            "source": "Open Trivia DB"
        }
        save_quiz_result(result)
        print(f"\nScore: {score}/{len(questions)} ({percentage:.2f}%)")
        print(f"Performance: {result['performance']}")
    except Exception as exc:
        print("Online quiz unavailable:", exc)
        print("You can use the local quiz instead.")


def ai_menu(username):
    if not AI_AVAILABLE:
        print("AI module is not available. Install the google-genai package.")
        return

    while True:
        print("\n=== GEMINI AI ASSISTANT ===")
        print("1. Analyze latest performance")
        print("2. Explain latest wrong answers")
        print("3. Generate practice questions")
        print("4. Back")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            from results import load_results
            results = [r for r in load_results() if r.get("username") == username]
            if not results:
                print("No results available.")
                continue
            try:
                print("\n" + analyze_performance(results[-1]))
            except Exception as exc:
                print("Gemini AI error:", exc)

        elif choice == "2":
            from results import load_results
            results = [r for r in load_results() if r.get("username") == username]
            if not results:
                print("No results available.")
                continue
            wrong = [a for a in results[-1].get("answers", []) if a.get("selected") != a.get("correct")]
            if not wrong:
                print("No wrong answers in the latest quiz.")
                continue
            for item in wrong:
                try:
                    print("\n" + explain_answer(
                        item["question"], item["selected"], item["correct"], item["options"]
                    ))
                except Exception as exc:
                    print("Gemini AI error:", exc)
                    break

        elif choice == "3":
            topic = input("Topic: ").strip()
            difficulty = input("Difficulty: ").strip() or "Medium"
            try:
                amount = int(input("Number of questions (1-10): "))
                questions = generate_practice_questions(topic, difficulty, amount)
                added = import_questions(questions)
                print(f"Added {added} AI-generated questions to the local bank.")
            except Exception as exc:
                print("Gemini AI error:", exc)

        elif choice == "4":
            break
        else:
            print("Invalid choice.")


def student_dashboard(user):
    while True:
        print("\n=== STUDENT DASHBOARD ===")
        print(f"Welcome, {user['username']}!")
        print("1. Local Quiz")
        print("2. Online API Quiz")
        print("3. My Results")
        print("4. Review Wrong Answers")
        print("5. Leaderboard")
        print("6. Gemini AI Assistant")
        print("7. Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            run_local_quiz(user["username"])
        elif choice == "2":
            run_api_quiz(user["username"])
        elif choice == "3":
            view_student_results(user["username"])
        elif choice == "4":
            review_wrong_answers(user["username"])
        elif choice == "5":
            show_leaderboard()
        elif choice == "6":
            ai_menu(user["username"])
        elif choice == "7":
            print("Logged out.")
            break
        else:
            print("Invalid choice.")


def main():
    while True:
        print("\n================================")
        print("          QUIZMASTER V2")
        print("================================")
        print("1. Register")
        print("2. Student Login")
        print("3. Admin Login")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            user = login_user()
            if user:
                student_dashboard(user)
        elif choice == "3":
            admin = admin_login()
            if admin:
                admin_dashboard()
        elif choice == "4":
            print("Thank you for using QuizMaster.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
