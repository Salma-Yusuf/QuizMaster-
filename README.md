# QuizMaster V2 — Advanced Quiz Game

QuizMaster is a Python quiz application with local quizzes, an external quiz API, authentication, scoring, results, leaderboard, admin management, and Gemini AI features.

## Core features

- Student registration and login
- Admin login and question management
- Local quiz questions stored in JSON
- Online multiple-choice questions from Open Trivia DB
- Automatic scoring and performance classification
- Result history and wrong-answer review
- Leaderboard
- Gemini AI explanations and performance analysis
- Gemini AI-generated practice questions
- GitHub-ready project structure

## External services

### Open Trivia DB
Used for the Online API Quiz. The project requests multiple-choice questions and converts the JSON response into the QuizMaster question format.

### Google Gemini API
Used for:
- Performance analysis
- Explanations for wrong answers
- AI-generated practice questions

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env`.
3. Add your Gemini API key to `GEMINI_API_KEY`.
4. Change the optional admin credentials.
5. Run:

```bash
python main.py
```

## Security

Never commit `.env` or a real Gemini API key to GitHub. `.env` is excluded by `.gitignore`.

## GitHub team workflow

The repository uses one stable `main` branch and eight feature branches. Each member works on their assigned branch, commits changes, pushes the branch, opens a Pull Request, and the project leader reviews and merges the work.
