"""
admin.py
--------
Administrator Panel module for QuizMaster V2 (feature/admin-panel branch).

Responsibilities covered here (from the project proposal, section 16.0):
    - Create the admin dashboard
    - Allow administrators to manage questions
    - Add / delete questions
    - View quiz information
    - Restrict administrative functions to authorized users

This is written as a Flask Blueprint so it can be registered into the
team's main app.py without clashing with anyone else's routes:

    from admin import admin_bp
    app.register_blueprint(admin_bp)

INTEGRATION NOTE FOR THE TEAM (read this before merging):
    Salma-Yusuf's authentication module (feature/authentication) owns the
    real login system and session handling. Until that's merged, this file
    includes a *stub* login route (marked clearly below) so the admin panel
    can be built and tested independently. Once auth is merged, delete the
    stub section and make sure login() in the auth module sets:
        session['username'] = <username>
        session['role']     = 'admin'  (or 'student')
    That's the only thing admin_required() below depends on.

Data storage: plain JSON files, per the proposal (section 14.0), so this
matches the rest of the team's approach. The question bank is normally
owned by Confidence's feature/question-bank branch — this file simply
reads/writes data/questions.json so it works standalone today and will
read whatever format that branch settles on, as long as it's a JSON list
of objects with at least: id, question, options, correct_answer.
"""

import json
import os
from functools import wraps
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash
)

# ---------------------------------------------------------------------------
# Blueprint setup
# ---------------------------------------------------------------------------
admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
    template_folder="templates/admin",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_FILE = os.path.join(BASE_DIR, "data", "questions.json")
RESULTS_FILE = os.path.join(BASE_DIR, "data", "quiz_results.json")


# ---------------------------------------------------------------------------
# JSON file helpers
# ---------------------------------------------------------------------------
def load_json(path):
    """Read a JSON file and return its contents, or [] if it doesn't exist
    yet / is empty. Keeps the rest of the code from crashing on first run."""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        return json.loads(content) if content else []


def save_json(path, data):
    """Write data back to a JSON file, pretty-printed for easy diffing
    in Git (important since 8 people are sharing this repo)."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def next_question_id(questions):
    """Generate the next question ID (max existing id + 1, or 1 if empty)."""
    if not questions:
        return 1
    return max(q["id"] for q in questions) + 1


# ---------------------------------------------------------------------------
# Access control — "Restrict administrative functions to authorized users"
# ---------------------------------------------------------------------------
def admin_required(view_func):
    """Decorator that blocks any route unless the logged-in user's session
    role is 'admin'. Put this on every admin-only route.

    This is the piece that satisfies your fourth task item directly:
    it does not just hide the admin links in the UI — it refuses the
    request at the route level, so no one can reach admin pages just by
    typing the URL.
    """
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if session.get("role") != "admin":
            flash("You must be logged in as an administrator to view that page.", "error")
            return redirect(url_for("admin.admin_login"))
        return view_func(*args, **kwargs)
    return wrapped


# ---------------------------------------------------------------------------
# STUB LOGIN — remove this block once feature/authentication is merged.
# It exists only so this branch can be tested in isolation before then.
# ---------------------------------------------------------------------------
STUB_ADMIN_USERNAME = "admin"
STUB_ADMIN_PASSWORD = "admin123"


@admin_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == STUB_ADMIN_USERNAME and password == STUB_ADMIN_PASSWORD:
            session["username"] = username
            session["role"] = "admin"
            flash("Logged in as administrator.", "success")
            return redirect(url_for("admin.dashboard"))
        flash("Invalid administrator credentials.", "error")
    return render_template("admin/login.html")


@admin_bp.route("/logout")
def admin_logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("admin.admin_login"))
# ---------------------------------------------------------------------------
# END STUB LOGIN
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Admin dashboard — "Create the admin dashboard"
# ---------------------------------------------------------------------------
@admin_bp.route("/")
@admin_required
def dashboard():
    questions = load_json(QUESTIONS_FILE)
    results = load_json(RESULTS_FILE)

    stats = {
        "total_questions": len(questions),
        "total_attempts": len(results),
        "average_score": (
            round(sum(r["percentage"] for r in results) / len(results), 1)
            if results else 0
        ),
    }
    return render_template("admin/dashboard.html", stats=stats, username=session.get("username"))


# ---------------------------------------------------------------------------
# Manage questions — "manage questions" + "Add/delete questions"
# ---------------------------------------------------------------------------
@admin_bp.route("/questions")
@admin_required
def manage_questions():
    questions = load_json(QUESTIONS_FILE)
    return render_template("admin/manage_questions.html", questions=questions)


@admin_bp.route("/questions/add", methods=["GET", "POST"])
@admin_required
def add_question():
    if request.method == "POST":
        question_text = request.form.get("question", "").strip()
        option1 = request.form.get("option1", "").strip()
        option2 = request.form.get("option2", "").strip()
        option3 = request.form.get("option3", "").strip()
        option4 = request.form.get("option4", "").strip()
        correct_answer = request.form.get("correct_answer", "").strip()
        category = request.form.get("category", "General").strip()
        difficulty = request.form.get("difficulty", "easy")

        options = [o for o in [option1, option2, option3, option4] if o]

        # Basic validation — a student project still needs this so a bad
        # form submission doesn't quietly corrupt the shared JSON file.
        if not question_text or len(options) < 2 or not correct_answer:
            flash("Please fill in the question, at least two options, and the correct answer.", "error")
            return render_template("admin/add_question.html")

        if correct_answer not in options:
            flash("The correct answer must match one of the options exactly.", "error")
            return render_template("admin/add_question.html")

        questions = load_json(QUESTIONS_FILE)
        new_question = {
            "id": next_question_id(questions),
            "question": question_text,
            "options": options,
            "correct_answer": correct_answer,
            "category": category,
            "difficulty": difficulty,
        }
        questions.append(new_question)
        save_json(QUESTIONS_FILE, questions)

        flash(f'Question "{question_text}" added successfully.', "success")
        return redirect(url_for("admin.manage_questions"))

    return render_template("admin/add_question.html")


@admin_bp.route("/questions/delete/<int:question_id>", methods=["POST"])
@admin_required
def delete_question(question_id):
    questions = load_json(QUESTIONS_FILE)
    remaining = [q for q in questions if q["id"] != question_id]

    if len(remaining) == len(questions):
        flash("Question not found — it may have already been deleted.", "error")
    else:
        save_json(QUESTIONS_FILE, remaining)
        flash("Question deleted.", "success")

    return redirect(url_for("admin.manage_questions"))


# ---------------------------------------------------------------------------
# View quiz information — "View quiz information"
# ---------------------------------------------------------------------------
@admin_bp.route("/quiz-info")
@admin_required
def quiz_info():
    results = load_json(RESULTS_FILE)
    # Most recent attempts first, so admins see current activity at a glance.
    results_sorted = sorted(results, key=lambda r: r.get("date", ""), reverse=True)
    return render_template("admin/quiz_info.html", results=results_sorted)
