"""QuizMaster - Flask app wiring for the quiz interface.

Questions: question_bank.py (data/questions.json).
Users and results: data_store.py (data/users.json, data/results.json).
"""
import json
import os
import urllib.parse
import urllib.request
import uuid
from datetime import datetime
from functools import wraps

from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   session, url_for, abort)
from werkzeug.security import check_password_hash, generate_password_hash

import data_store as store
import gemini_helper
from gemini_helper import ask_gemini
import question_bank as qb

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-me-in-production")

# ---------------------------------------------------------------- question bank
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
qb.QUESTIONS_FILE = os.path.join(BASE_DIR, "data", "questions.json")   # works from any folder

gemini_helper.load_env_file(os.path.join(BASE_DIR, ".env"))   # reads GEMINI_API_KEY etc.
store.USERS_FILE = os.path.join(BASE_DIR, "data", "users.json")
store.RESULTS_FILE = os.path.join(BASE_DIR, "data", "results.json")

# first run: create the admin account (set ADMIN_PASSWORD to choose your own)
if not any(u["role"] == "admin" for u in store.get_users().values()):
    store.create_user("admin", "Administrator",
                      generate_password_hash(os.environ.get("ADMIN_PASSWORD", "admin123")), "admin")

ACTIVE_QUIZZES = {}   # token -> list of normalised questions (answers stay on the server)

# Open Trivia DB category ids offered for online quizzes
ONLINE_CATEGORIES = {"General Knowledge": 9, "Science & Nature": 17, "Computer Science": 18,
                     "Mathematics": 19, "Geography": 22, "History": 23}


def normalize(q):
    """Convert QuizMaster questions to the format used by the Flask app."""
    letters = "ABCD"

    options = q.get("options", {})

    if isinstance(options, dict):
        normalized_options = [options[k] for k in letters]
    elif isinstance(options, list):
        normalized_options = options
    else:
        normalized_options = []

    answer = q.get("answer", q.get("correct_answer", "A"))

    if isinstance(answer, str) and answer in letters:
        answer_index = letters.index(answer)
    elif isinstance(answer, int):
        answer_index = answer
    else:
        answer_index = 0

    return {
        "id": q.get("id"),
        "text": q["question"],
        "options": normalized_options,
        "answer": answer_index,
        "category": q.get("category", "General"),
        "difficulty": q.get("difficulty", "Medium"),
        "explanation": q.get("explanation", "")
    }

def get_categories(mode="local"):
    return sorted(ONLINE_CATEGORIES) if mode == "online" else qb.get_categories()


def fetch_online_questions(category, difficulty, count):
    """Pull questions from Open Trivia DB and convert them with your converter."""
    params = {"amount": count, "type": "multiple"}
    if category != "all" and category in ONLINE_CATEGORIES:
        params["category"] = ONLINE_CATEGORIES[category]
    if difficulty != "all":
        params["difficulty"] = difficulty.lower()
    url = "https://opentdb.com/api.php?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=8) as resp:
        data = json.load(resp)
    if data.get("response_code") != 0:
        return []
    out = []
    for i, item in enumerate(data["results"], start=1):
        q = qb.convert_opentdb_question(item)
        q["id"] = -i                      # temporary ids, never saved to your bank
        out.append(normalize(q))
    return out


def fetch_questions(mode, category, difficulty, count):
    if mode == "online":
        try:
            return fetch_online_questions(category, difficulty, count)
        except Exception:
            return None                   # caller shows a friendly message
    qs = qb.get_quiz_questions(None if category == "all" else category,
                               None if difficulty == "all" else difficulty, count)
    return [normalize(q) for q in qs]


# ---------------------------------------------------------------- helpers
def login_required(view):
    @wraps(view)
    def wrapper(*a, **kw):
        if "user" not in session:
            flash("Please log in to continue.", "info")
            return redirect(url_for("login", next=request.path))
        return view(*a, **kw)
    return wrapper


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapper(*a, **kw):
        if session.get("role") != "admin":
            abort(403)
        return view(*a, **kw)
    return wrapper


def performance_level(pct):
    if pct >= 90: return "Excellent"
    if pct >= 75: return "Very good"
    if pct >= 50: return "Satisfactory"
    return "Needs practice"


def leaderboard_rows():
    best = {}
    users = store.get_users()
    for r in store.get_results():
        cur = best.get(r["user"])
        if not cur or r["percentage"] > cur["percentage"]:
            best[r["user"]] = r
    rows = sorted(best.values(), key=lambda r: (-r["percentage"], r["taken_at"]))
    return [{"rank": i + 1, "name": users.get(r["user"], {}).get("name", r["user"]), "percentage": r["percentage"],
             "score": r["score"], "total": r["total"], "category": r["category_label"]}
            for i, r in enumerate(rows)]


@app.context_processor
def inject_globals():
    return {"current_user": session.get("user"), "current_name": session.get("name"),
            "is_admin": session.get("role") == "admin"}


# ---------------------------------------------------------------- public pages
@app.route("/")
def home():
    return render_template("home.html", question_count=len(qb.get_all_questions()), category_count=len(qb.get_categories()))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        username = request.form.get("username", "").strip().lower()
        pw, pw2 = request.form.get("password", ""), request.form.get("confirm", "")
        error = None
        if not (name and username and pw):
            error = "Fill in every field."
        elif store.get_user(username):
            error = "That username is taken. Try another."
        elif len(pw) < 6:
            error = "Use a password with at least 6 characters."
        elif pw != pw2:
            error = "The two passwords don't match."
        if error:
            flash(error, "error")
            return render_template("register.html", form=request.form), 400
        if not store.create_user(username, name, generate_password_hash(pw)):
            flash("That username is taken. Try another.", "error")
            return render_template("register.html", form=request.form), 400
        flash("Account created. You can log in now.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form={})


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        user = store.get_user(username)
        if user and check_password_hash(user["password"], request.form.get("password", "")):
            session.clear()
            session.update(user=username, name=user["name"], role=user["role"])
            nxt = request.args.get("next")
            if nxt and nxt.startswith("/"):
                return redirect(nxt)
            return redirect(url_for("admin_dashboard" if user["role"] == "admin" else "dashboard"))
        flash("Username or password is incorrect.", "error")
        return render_template("login.html", username=username), 401
    return render_template("login.html", username="")


@app.route("/logout")
def logout():
    session.clear()
    flash("You're logged out.", "info")
    return redirect(url_for("home"))


# ---------------------------------------------------------------- student area
@app.route("/dashboard")
@login_required
def dashboard():
    mine = [r for r in store.get_results() if r["user"] == session["user"]]
    return render_template("dashboard.html", attempts=len(mine),
                           best=max((r["percentage"] for r in mine), default=None),
                           last=mine[-1] if mine else None)


@app.route("/quiz/setup/<mode>", methods=["GET", "POST"])
@login_required
def quiz_setup(mode):
    if mode not in ("local", "online"):
        abort(404)
    if request.method == "POST":
        category = request.form.get("category", "all")
        difficulty = request.form.get("difficulty", "all")
        try:
            count = min(max(int(request.form.get("count", 10)), 1), 50)
        except ValueError:
            count = 10
        qs = fetch_questions(mode, category, difficulty, count)
        if qs is None:
            flash("Couldn't reach the online question source. Check your connection or try a local quiz.", "error")
            return redirect(url_for("quiz_setup", mode=mode))
        if not qs:
            flash("No questions match that choice. Try another category or difficulty.", "error")
            return redirect(url_for("quiz_setup", mode=mode))
        token = uuid.uuid4().hex
        ACTIVE_QUIZZES[token] = qs
        session["quiz"] = {"token": token, "mode": mode, "category": category, "difficulty": difficulty}
        return redirect(url_for("quiz"))
    return render_template("quiz_setup.html", mode=mode, categories=get_categories(mode))


@app.route("/quiz")
@login_required
def quiz():
    state = session.get("quiz")
    questions = ACTIVE_QUIZZES.get(state["token"]) if state else None
    if not questions:
        session.pop("quiz", None)
        flash("That quiz has expired. Start a new one.", "info")
        return redirect(url_for("dashboard"))
    # never send the answer key to the browser
    safe = [{k: q[k] for k in ("id", "text", "options", "category", "difficulty")} for q in questions]
    return render_template("quiz.html", questions=safe, state=state)


@app.route("/quiz/submit", methods=["POST"])
@login_required
def submit_quiz():
    state = session.pop("quiz", None)
    questions = ACTIVE_QUIZZES.pop(state["token"], None) if state else None
    if not questions:
        return redirect(url_for("dashboard"))
    review, score = [], 0
    for q in questions:
        raw = request.form.get(f"q{q['id']}")
        chosen = int(raw) if raw is not None and raw.isdigit() and int(raw) < 4 else None
        correct = chosen == q["answer"]
        score += correct
        review.append({"id": q["id"], "text": q["text"], "options": q["options"], "chosen": chosen,
                       "answer": q["answer"], "correct": correct, "explanation": q["explanation"]})
    total = len(review)
    pct = round(score / total * 100) if total else 0
    cat = state["category"]
    result = {"user": session["user"], "mode": state["mode"],
              "category_label": "All categories" if cat == "all" else cat,
              "difficulty_label": "Any difficulty" if state["difficulty"] == "all" else state["difficulty"],
              "score": score, "total": total, "wrong": total - score, "percentage": pct,
              "level": performance_level(pct), "review": review,
              "taken_at": datetime.now()}
    result = store.add_result(result)
    return redirect(url_for("result", result_id=result["id"]))


def _own_result(result_id):
    r = store.get_result(result_id)
    if not r or (r["user"] != session["user"] and session.get("role") != "admin"):
        abort(404)
    return r


@app.route("/result/<int:result_id>")
@login_required
def result(result_id):
    return render_template("result.html", r=_own_result(result_id))


@app.route("/results")
@login_required
def results():
    mine = [r for r in reversed(store.get_results()) if r["user"] == session["user"]]
    return render_template("results.html", results=mine)


@app.route("/leaderboard")
@login_required
def leaderboard():
    return render_template("leaderboard.html", rows=leaderboard_rows())


@app.route("/ai-assistant")
@login_required
def ai_assistant():
    return render_template("ai_assistant.html")


@app.post("/api/chat")
@login_required
def api_chat():
    data = request.get_json(silent=True) or {}
    msg = str(data.get("message", "")).strip()
    if not msg:
        return jsonify(reply="Type a question first."), 400
    if not gemini_helper.allow(session["user"]):
        return jsonify(reply="You're sending questions very quickly. Wait a moment and try again."), 429
    history = data.get("history") if isinstance(data.get("history"), list) else []
    return jsonify(reply=ask_gemini(msg, history))


@app.post("/api/explain")
@login_required
def api_explain():
    data = request.get_json(silent=True) or {}
    try:
        r = _own_result(int(data.get("result_id", 0)))
    except (TypeError, ValueError):
        return jsonify(reply="That result could not be found."), 400
    if not gemini_helper.allow(session["user"]):
        return jsonify(reply="You're asking very quickly. Wait a moment and try again."), 429
    items = r["review"]
    if data.get("question_id"):
        items = [i for i in items if str(i["id"]) == str(data["question_id"])]
    else:
        wrong = [i for i in items if not i["correct"]]
        items = wrong or items          # focus the overall explanation on what was missed
    lines = []
    for i in items[:15]:
        mine = i["options"][i["chosen"]] if i["chosen"] is not None else "(no answer)"
        lines.append(f"Question: {i['text']}\nStudent answered: {mine}\nCorrect answer: {i['options'][i['answer']]}")
    prompt = ("For each question below, explain in simple terms why the correct answer is right and, "
              "if the student was wrong, what the misunderstanding may be. Keep each explanation to 2-3 sentences.\n\n"
              + "\n\n".join(lines))
    return jsonify(reply=ask_gemini(prompt))


# ---------------------------------------------------------------- admin
@app.route("/admin")
@admin_required
def admin_dashboard():
    questions = [normalize(q) for q in qb.get_all_questions()]
    return render_template("admin_dashboard.html", questions=questions, categories=qb.get_categories(),
                           rows=leaderboard_rows()[:10], students=sum(1 for u in store.get_users().values() if u["role"] == "student"),
                           attempts=len(store.get_results()))


@app.post("/admin/questions")
@admin_required
def admin_add_question():
    f = request.form
    options = {k: f.get(f"opt{i}", "") for i, k in enumerate("ABCD")}
    try:
        qb.create_question(f.get("text", ""), options, "ABCD"[int(f.get("answer", 0)) % 4],
                           f.get("category", "General"), f.get("difficulty", "Medium"))
        flash("Question added.", "success")
    except qb.ValidationError as exc:
        flash(str(exc), "error")
    return redirect(url_for("admin_dashboard"))


@app.post("/admin/questions/<int:qid>/delete")
@admin_required
def admin_delete_question(qid):
    try:
        qb.delete_question(qid)
        flash("Question deleted.", "success")
    except qb.ValidationError as exc:
        flash(str(exc), "error")
    return redirect(url_for("admin_dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
