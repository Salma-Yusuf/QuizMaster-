# Admin Panel — QuizMaster V2

Branch: `feature/admin-panel`
Member: Abdulhakim Ibrahim

Covers all four tasks from the proposal:
- Create the admin dashboard
- Allow administrators to manage questions (view / add / delete)
- View quiz information
- Restrict administrative functions to authorized users

## Running it on its own (before merging into the team's repo)

```bash
pip install flask
python app.py
```

Open **http://127.0.0.1:5000/admin/login**

Login with:
- Username: `admin`
- Password: `admin123`

## How it's organized

```
admin.py                        → the actual admin panel (Blueprint)
app.py                          → standalone test runner — NOT part of the final app
data/questions.json             → sample question bank
data/quiz_results.json          → sample quiz attempt history
templates/admin/                → all admin HTML pages
static/css/admin.css            → styling
```

## Merging into the main app

Once `feature/authentication` is merged into `main`, two things need to happen:

1. **Delete the stub login** — the block in `admin.py` marked
   `STUB LOGIN ... END STUB LOGIN`, and delete `templates/admin/login.html`
   and `app.py`. The real login page belongs to the auth module.

2. **Register the blueprint** in the team's real `app.py`:

   ```python
   from admin import admin_bp
   app.register_blueprint(admin_bp)
   ```

That's it — every route in `admin.py` already checks
`session.get("role") == "admin"` through the `admin_required` decorator,
so as soon as the real login sets `session["role"] = "admin"` for admin
accounts, access control keeps working with no changes needed on my side.

## Data format my code expects

`data/questions.json` — a list of objects:
```json
{
  "id": 1,
  "question": "...",
  "options": ["...", "...", "..."],
  "correct_answer": "...",
  "category": "...",
  "difficulty": "easy"
}
```

If Confidence's `feature/question-bank` branch ends up using a different
shape for `questions.json`, the only place that needs updating is the
`load_json` / `save_json` calls in `admin.py` — the templates just loop
over whatever fields exist.

`data/quiz_results.json` — a list of objects:
```json
{
  "username": "...",
  "score": 8,
  "total_questions": 10,
  "percentage": 80.0,
  "category": "...",
  "date": "YYYY-MM-DD"
}
```

If the Scoring/Leaderboard branches write results in a different shape,
same note applies — only `quiz_info()` in `admin.py` needs adjusting.
