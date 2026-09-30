"""Gemini connection for QuizMaster (uses Google's current `google-genai` SDK)."""
import os
import time
from collections import defaultdict, deque

SYSTEM_PROMPT = (
    "You are QuizMaster's study tutor for students. Explain clearly and briefly in plain language, "
    "use small examples, and stay on educational topics. If a student got a quiz question wrong, "
    "explain why the right answer is right and what the mix-up might have been. "
    "Do not use markdown headings; short paragraphs are fine."
)

# Tried in order. Put your preferred model first with GEMINI_MODEL (see Google AI Studio for current names).
DEFAULT_MODELS = ["gemini-2.5-flash", "gemini-flash-latest"]

_calls = defaultdict(deque)
RATE_LIMIT, RATE_WINDOW = 15, 60          # 15 AI requests per user per minute


def allow(user):
    """Simple per-user rate limit so one student can't burn the whole quota."""
    now, q = time.time(), _calls[user]
    while q and now - q[0] > RATE_WINDOW:
        q.popleft()
    if len(q) >= RATE_LIMIT:
        return False
    q.append(now)
    return True


def load_env_file(path):
    """Tiny .env reader (KEY=value per line) so you don't retype the key every session."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _models():
    chosen = os.environ.get("GEMINI_MODEL", "").strip()
    return [chosen] + [m for m in DEFAULT_MODELS if m != chosen] if chosen else DEFAULT_MODELS


def _generate(model, contents):
    """One call to Gemini. Kept separate so it is easy to test."""
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    resp = client.models.generate_content(
        model=model, contents=contents,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT,
                                           temperature=0.4, max_output_tokens=900))
    return resp.text


def ask_gemini(prompt, history=None):
    """Return Gemini's answer as text. Never raises: problems become readable messages."""
    if not (os.environ.get("GEMINI_API_KEY") or "").strip():
        return "Gemini is not connected yet. Add GEMINI_API_KEY to your .env file, then restart the app."
    contents = []
    for turn in (history or [])[-6:]:                         # last 6 turns keeps context small
        role = "user" if turn.get("role") == "user" else "model"
        text = str(turn.get("text", ""))[:2000]
        if text:
            contents.append({"role": role, "parts": [{"text": text}]})
    contents.append({"role": "user", "parts": [{"text": prompt[:6000]}]})

    last_error = None
    for model in _models():
        try:
            text = _generate(model, contents)
            return text.strip() if text else "Gemini returned no answer for that. Try rewording your question."
        except ImportError:
            return "The Gemini library is missing. Run: pip install google-genai"
        except Exception as exc:
            last_error = exc
            code = getattr(exc, "code", None)
            msg = str(exc).lower()
            if code == 404 or "not found" in msg or "is not supported" in msg:
                continue                                       # model name retired: try the next one
            if code in (400, 401, 403) and ("api key" in msg or "api_key" in msg or code in (401, 403)):
                return "Gemini rejected the API key. Check that GEMINI_API_KEY is correct and active."
            if code == 429 or "quota" in msg or "resource_exhausted" in msg:
                return "The AI service is busy or the free quota is used up. Please try again in a minute."
            break
    if last_error is not None and (getattr(last_error, "code", None) == 404 or "not found" in str(last_error).lower()):
        return "None of the configured Gemini models were found. Set GEMINI_MODEL to a current model name from Google AI Studio."
    return "Gemini could not answer right now. Please try again in a moment."
