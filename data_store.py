"""JSON storage for users and quiz results (same approach as question_bank.py)."""
import json
import os
import threading
from datetime import datetime

USERS_FILE = "data/users.json"
RESULTS_FILE = "data/results.json"
_lock = threading.RLock()


def _read(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def _write(path, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    os.replace(tmp, path)          # atomic: a crash can't leave a half-written file


# ---------------------------------------------------------------- users
def get_users():
    return _read(USERS_FILE, {})


def get_user(username):
    return get_users().get(username)


def create_user(username, name, password_hash, role="student"):
    with _lock:
        users = get_users()
        if username in users:
            return False
        users[username] = {"name": name, "password": password_hash, "role": role,
                           "created": datetime.now().isoformat(timespec="seconds")}
        _write(USERS_FILE, users)
        return True


# ---------------------------------------------------------------- results
def _load_result(r):
    r = dict(r)
    r["taken_at"] = datetime.fromisoformat(r["taken_at"])
    return r


def get_results():
    return [_load_result(r) for r in _read(RESULTS_FILE, [])]


def get_result(result_id):
    return next((r for r in get_results() if r["id"] == result_id), None)


def add_result(result):
    """Assigns the next id, saves, and returns the stored result."""
    with _lock:
        rows = _read(RESULTS_FILE, [])
        result = dict(result)
        result["id"] = max([r["id"] for r in rows] or [0]) + 1
        result["taken_at"] = result["taken_at"].isoformat(timespec="seconds")
        rows.append(result)
        _write(RESULTS_FILE, rows)
        return _load_result(result)
