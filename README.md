# QuizMaster

A web-based quiz system for students, built with Flask, HTML and CSS.
Students register, take local or online quizzes, see their results and a leaderboard.
Administrators manage the question bank.

## Run it (Windows PowerShell)

```
cd quizmaster
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000. Press `Ctrl + C` in the terminal to stop.
On Mac/Linux: `source venv/bin/activate` instead of the two Windows lines, and use `python3`.

**Default admin account:** `admin` / `admin123` (created on first run).
Set `ADMIN_PASSWORD` before the first run to choose your own.
Students create their own accounts on the Sign up page.

## Screens

| Screen | URL |
|---|---|
| Home | `/` |
| Login / Register | `/login`, `/register` |
| Student dashboard | `/dashboard` |
| Quiz setup (category, difficulty, amount) | `/quiz/setup/local`, `/quiz/setup/online` |
| Quiz | `/quiz` |
| Result (score, percentage, level, review) | `/result/<id>` |
| Past results / Leaderboard | `/results`, `/leaderboard` |
| AI Assistant | `/ai-assistant` |
| Administrator dashboard | `/admin` |

## Project layout

```
app.py             Flask routes: login, quiz flow, results, admin
question_bank.py   Question storage and validation (data/questions.json)
data_store.py      Users and results storage (data/users.json, data/results.json)
gemini_helper.py   AI connection - see "For the AI teammate" below
templates/         Jinja HTML pages (base.html is the shared layout)
static/css/        style.css - all styling
static/js/         quiz.js - quiz navigation, progress bar, timer
data/              JSON files (questions are included; users/results are created on first use)
```

## How it works

- **Quiz flow:** setup page -> questions are chosen and kept on the server -> the browser
  shows one question at a time -> on Finish, answers are marked on the server and saved.
  Correct answers are never sent to the browser during a quiz.
- **Local quiz:** uses `question_bank.get_quiz_questions()`.
- **Online quiz:** fetches from Open Trivia DB and converts with `convert_opentdb_question()`.
  These questions are used for that quiz only and are not saved to the bank. Needs internet.
- **Question format** (`data/questions.json`): `question`, `options` (A-D), `answer` (a letter),
  `category`, `difficulty` (Easy / Medium / Hard).
- **Performance levels:** 90%+ Excellent, 75%+ Very good, 50%+ Satisfactory, otherwise Needs practice
  (`performance_level()` in `app.py`).

## For the AI teammate

The interface is already built and calls one function:

```python
ask_gemini(prompt, history=None)   # in gemini_helper.py: text in, text out
```

- The chat page uses `/api/chat`; the "Explain with AI" buttons on the result page use `/api/explain`.
  Both are in `app.py` and already handle login, a per-user rate limit and error messages.
- You can change the model, the tutor instructions (`SYSTEM_PROMPT`) or the SDK inside
  `gemini_helper.py` without touching the interface. Keep the function name and inputs the same.
- A first version is included using the `google-genai` package, but it has **not been tested
  against the live Gemini service**. Please verify it with a real key.
- Put your key in a `.env` file next to `app.py` (see `env.example`). Never commit `.env`.
  Each person should use their own key.
- Without a key, the AI features show "Gemini is not connected yet" and nothing else breaks.

## Known limitations

- Data is stored in JSON files: fine for a class project, not for many simultaneous users.
- No CSRF protection on forms yet (add Flask-WTF before any public deployment).
- The admin can add and delete questions but not edit them (`update_question()` exists in
  `question_bank.py` if an edit page is needed).
- Change `SECRET_KEY` (environment variable) and the admin password before deploying anywhere public.
- Do not upload `.env`, `data/users.json` or `data/results.json` to a public repository.
