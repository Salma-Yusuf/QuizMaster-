# QuizMaster V2 — Advanced Quiz Game

QuizMaster V2 is a Python-based AI-powered quiz management system with local quizzes, an external quiz API, authentication, scoring, results, leaderboard statistics, administrator management, and Gemini AI features.

The project combines locally stored questions with questions retrieved from the Open Trivia DB API and uses Google Gemini for AI-powered educational assistance.

## Core features

- Student registration and login
- Admin login and question management
- Local quiz questions stored in JSON
- Online multiple-choice questions from Open Trivia DB
- Automatic scoring and performance classification
- Percentage calculation
- Result history
- Wrong-answer review
- Leaderboard and performance statistics
- Gemini AI performance analysis
- Gemini AI explanations for wrong answers
- Gemini AI-generated practice questions
- Question-bank management
- JSON/file handling
- GitHub collaborative development

## Project structure

```text
QuizMaster_Advanced_Updated/
│
├── main.py
├── auth.py
├── quiz_engine.py
├── question_bank.py
├── scoring.py
├── results.py
├── leaderboard.py
├── admin.py
├── api_service.py
├── ai_assistant.py
├── config.py
│
├── requirements.txt
├── README.md
├── BRANCH_GUIDE.md
├── .env.example
├── .gitignore
│
└── data/
    ├── questions.json
    ├── users.json
    └── results.json
```

## Main Python files

| File | Purpose |
|---|---|
| `main.py` | Main controller that connects the major parts of QuizMaster |
| `auth.py` | Handles student registration, login, and admin login |
| `quiz_engine.py` | Displays questions and collects student answers |
| `question_bank.py` | Manages the local question bank |
| `scoring.py` | Calculates scores, percentages, and performance classification |
| `results.py` | Saves, loads, and reviews quiz results |
| `leaderboard.py` | Displays rankings and performance statistics |
| `admin.py` | Provides administrator functions |
| `api_service.py` | Connects QuizMaster to the Open Trivia DB API |
| `ai_assistant.py` | Connects QuizMaster to Google Gemini AI |
| `config.py` | Stores project configuration and settings |

## External services

### Open Trivia DB

Used for the Online API Quiz.

The project sends a request to Open Trivia DB, receives questions in JSON format, processes the response, and converts the questions into the QuizMaster format.

Official resources:

- [Open Trivia DB](https://opentdb.com/)
- [Open Trivia DB API documentation](https://opentdb.com/api_config.php)

### Google Gemini API

Used for:

- Performance analysis
- Explanations for wrong answers
- AI-generated practice questions
- AI study assistance

Official documentation:

- [Google Gemini API](https://ai.google.dev/gemini-api/docs)

### Python

The project is developed using Python.

- [Python Official Website](https://www.python.org/)

## API integration flow

```text
Student
   ↓
main.py
   ↓
api_service.py
   ↓
Open Trivia DB
   ↓
JSON response
   ↓
Question conversion
   ↓
quiz_engine.py
   ↓
Student answers
   ↓
scoring.py
   ↓
results.py
   ↓
leaderboard.py
```

The API integration is responsible for retrieving online questions, processing JSON responses, converting questions into the QuizMaster format, validating inputs, and handling API/network errors.

## API question format

Open Trivia DB provides information such as:

```text
question
correct_answer
incorrect_answers
category
difficulty
```

QuizMaster converts this into:

```python
{
    "question": "Example question",
    "options": {
        "A": "Option one",
        "B": "Option two",
        "C": "Option three",
        "D": "Option four"
    },
    "answer": "B",
    "category": "General Knowledge",
    "difficulty": "Easy"
}
```

The answer options are shuffled so the correct answer is not always in the same position.

## API error handling

The API service handles:

- Invalid question amounts
- Invalid difficulty
- Invalid category
- Internet connection problems
- Request timeouts
- HTTP errors
- Invalid JSON responses
- Open Trivia DB response errors
- Not enough available questions
- Too many API requests

The project uses a custom API error:

```python
class APIServiceError(Exception):
    pass
```

## Gemini AI integration

Gemini AI is handled separately from the Open Trivia DB API.

The two external services have different responsibilities:

| Integration | Service | Main purpose |
|---|---|---|
| API Integration | Open Trivia DB | Retrieve online quiz questions |
| AI Integration | Google Gemini | Analysis, explanations, study assistance, and practice questions |

## Local quiz and online API quiz

### Local quiz

Local questions are stored in:

```text
data/questions.json
```

The basic flow is:

```text
questions.json
      ↓
quiz_engine.py
      ↓
Student answers
      ↓
scoring.py
      ↓
results.py
```

### Online API quiz

The online quiz uses Open Trivia DB:

```text
Open Trivia DB
      ↓
api_service.py
      ↓
quiz_engine.py
      ↓
Student answers
      ↓
scoring.py
      ↓
results.py
```

Both quiz types use the QuizMaster scoring and result system.

## Scoring, results and leaderboard

After a quiz:

```text
Student answers
      ↓
scoring.py
      ↓
Score + percentage
      ↓
Performance classification
      ↓
results.py
      ↓
data/results.json
      ↓
leaderboard.py
```

Online API quiz results can identify their source as:

```python
"source": "Open Trivia DB"
```

## Authentication

`auth.py` handles:

- Student registration
- Student login
- Admin login
- User information

User data is stored in:

```text
data/users.json
```

## Administrator module

`admin.py` provides administrator functionality, including supported question-management and administrative operations.

## Requirements

The project includes:

```text
requirements.txt
```

Install the project dependencies with:

```bash
pip install -r requirements.txt
```

## Setup

1. Install the dependencies:

```bash
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env`.

3. Add your Gemini API key:

```text
GEMINI_API_KEY=your_api_key_here
```

4. Run the application:

```bash
python main.py
```

## Testing the API integration

The upgraded `api_service.py` includes a direct API test.

Run:

```bash
python api_service.py
```

The test requests three easy questions from Open Trivia DB.

A successful test begins similar to:

```text
=============================================
QUIZMASTER V2 - API INTEGRATION TEST
=============================================

API connection successful.
Questions received: 3
```

An internet connection is required.

## Security

Never commit `.env` or a real Gemini API key to GitHub.

Use `.env.example` as the safe template for required environment variables.

The `.gitignore` file is used to help prevent sensitive files from being committed.

## GitHub team workflow

The repository uses one stable `main` branch and eight feature branches.

Each member:

1. Works on their assigned branch.
2. Develops their assigned module.
3. Tests the code.
4. Commits the changes.
5. Pushes the branch.
6. Opens a Pull Request.
7. Receives code review.
8. Has the completed work merged into `main`.

## 8-member team structure

| No. | Member | GitHub Branch | Role | Main Responsibility |
|---:|---|---|---|---|
| 1 | Salma-Yusuf Yusuf | `feature/authentication` | Project Leader & Authentication | Repository management, authentication, roles, Pull Request review, merge coordination |
| 2 | Confidence Okobru | `feature/question-bank` | Question Bank & Data Management | Questions, categories, difficulty levels, JSON question data |
| 3 | Islamiyah Ibrahim | `feature/quiz-interface` | Quiz Interface / UI | Quiz pages, questions, answer options, navigation and interface |
| 4 | Oluwatosin Ajayi | `feature/scoring-results` | Scoring & Results | Scores, percentages, performance and result handling |
| 5 | Nentapomwa Wakijssa | `feature/leaderboard` | Leaderboard & Performance Statistics | Rankings, previous results and performance statistics |
| 6 | Abdulhakim Ibrahim | `feature/admin-panel` | Administrator Panel | Admin dashboard and question management |
| 7 | Abubakar Yusuf | `feature/api-integration` | External API Integration | Open Trivia DB, JSON processing, question conversion and API error handling |
| 8 | Emmanuel Nweke | `feature/ai-integration` | Gemini AI Integration & AI Testing | Gemini API, AI explanations, study feedback, practice questions and AI testing |

## Complete system flow

```text
                         QUIZMASTER V2
                              │
             ┌────────────────┴────────────────┐
             │                                 │
        LOCAL QUIZ                        ONLINE QUIZ
             │                                 │
    data/questions.json                 Open Trivia DB
             │                                 │
             └────────────────┬────────────────┘
                              │
                       quiz_engine.py
                              │
                       Student answers
                              │
                         scoring.py
                              │
                    Score + performance
                              │
                         results.py
                              │
                       results.json
                              │
                ┌─────────────┴─────────────┐
                │                           │
          leaderboard.py              ai_assistant.py
                                            │
                                      Google Gemini
```

## GitHub development flow

```text
GitHub Main Repository
          ↓
     Member Branch
          ↓
       Coding
          ↓
       Testing
          ↓
        Commit
          ↓
        Push
          ↓
    Pull Request
          ↓
     Code Review
          ↓
        Merge
          ↓
         main
```

## Project goal

QuizMaster V2 combines:

```text
Python
+
Flask / Web Application
+
JSON
+
Authentication
+
Quiz Engine
+
Scoring
+
Results
+
Leaderboard
+
Open Trivia DB API
+
Google Gemini AI
+
Git/GitHub Collaboration
```

The project demonstrates how these components can work together in a modular quiz management system.

## Important project files

| File | Importance |
|---|---|
| `README.md` | Project documentation |
| `BRANCH_GUIDE.md` | Team branch and responsibility guide |
| `requirements.txt` | Python package dependencies |
| `config.py` | Project configuration |
| `.env.example` | Environment-variable template |
| `.gitignore` | Files that should not be committed |
| `api_service.py` | Open Trivia DB API integration |
| `ai_assistant.py` | Gemini AI integration |
