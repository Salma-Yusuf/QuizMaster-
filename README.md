# QuizMaster V2 — Advanced Quiz Game

## Project Summary

**QuizMaster V2** is a Python-based, AI-powered quiz management system. It provides students with an interactive quiz experience while also giving administrators tools to manage questions and view quiz information.

The project supports **local quizzes**, **online quizzes using the Open Trivia DB API**, **user authentication**, **automatic scoring**, **result tracking**, **leaderboards**, **administrator functions**, and **Google Gemini AI assistance**.

The project was developed collaboratively using GitHub feature branches and then integrated into the main project.

---

## Key Features

- Student registration and login
- Authentication and protected pages
- Local question bank stored in JSON
- Online multiple-choice questions through Open Trivia DB
- Quiz setup by category and difficulty
- Interactive quiz interface
- Automatic score calculation
- Percentage and performance classification
- Quiz result history
- Wrong-answer review
- Leaderboard and performance statistics
- Administrator panel
- Question management
- Gemini AI assistance
- AI explanations for wrong answers
- AI performance analysis
- AI-generated practice questions
- JSON/file-based data storage
- GitHub collaborative development

---

## Technologies Used

- **Python**
- **Flask**
- **HTML/CSS/JavaScript**
- **JSON**
- **Git & GitHub**
- **Open Trivia DB API**
- **Google Gemini API**
- **python-dotenv**
- **Requests**

---

## Project Structure

```text
QuizMaster--main/
│
├── app.py
├── main.py
├── auth.py
├── question_bank.py
├── question_bank_modified1.py
├── quiz_engine.py
├── scoring.py
├── results.py
├── leaderboard.py
├── admin.py
├── api_service.py
├── ai_assistant.py
├── gemini_helper.py
├── data_store.py
├── config.py
│
├── requirements.txt
├── README.md
├── BRANCH_GUIDE.md
├── env.example
├── .gitignore
│
├── data/
│   ├── questions.json
│   └── quiz_results.json
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── admin.css
│   └── js/
│       └── quiz.js
│
└── templates/
    ├── base.html
    ├── home.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── quiz.html
    ├── quiz_setup.html
    ├── result.html
    ├── results.html
    ├── leaderboard.html
    ├── ai_assistant.html
    └── admin/
```

---

## Main Python Files

| File | Purpose |
|---|---|
| `app.py` | Main Flask web application that connects the major parts of QuizMaster |
| `main.py` | Console/command-line entry point for the non-web version |
| `auth.py` | Handles registration, login, password handling and authentication |
| `question_bank.py` | Manages local quiz questions |
| `question_bank_modified1.py` | Duplicate/modified copy of the question-bank module present in the project |
| `quiz_engine.py` | Controls the quiz flow for the console version |
| `scoring.py` | Calculates scores, percentages and performance classification |
| `results.py` | Saves, loads and reviews quiz results |
| `leaderboard.py` | Creates rankings and performance statistics |
| `admin.py` | Provides administrator functions and question management |
| `api_service.py` | Connects the project to the Open Trivia DB API |
| `ai_assistant.py` | Provides AI-powered quiz assistance |
| `gemini_helper.py` | Handles communication with Google Gemini |
| `data_store.py` | Provides storage and retrieval of application data |
| `config.py` | Contains project configuration and settings |

---

# GitHub Branch Assignment vs. Actual Contributors

The project was originally organized around eight feature branches. The table below compares the **assigned contributor** for each branch with the **person who actually worked on the branch**, based on the team's contribution record.

| Branch | Assigned Contributor | Actual Contributor(s) |
|---|---|---|
| `main` | — | — |
| `feature/authentication` | **Salma-Yusuf Yusuf** | **Salma-Yusuf Yusuf** |
| `feature/question-bank` | **Confidence Okobru** | **Confidence** |
| `feature/quiz-interface` | **Islamiyah Ibrahim** | **Confidence** |
| `feature/scoring-results` | **Oluwatosin Ajayi** | **Salma-Yusuf Yusuf** |
| `feature/leaderboard` | **Nentapomwa Wakijssa** | **Nentapomwa Wakijssa** |
| `feature/admin-panel` | **Abdulhakim Ibrahim** | **Islamiyah** |
| `feature/api-integration` | **Abubakar Yusuf** | **Abdulhakim Ibrahim** |
| `feature/ai-integration` | **Emmanuel Nweke** | **Salma-Yusuf Yusuf** |
| `feature/final-integration-cleanup` | — | **Salma-Yusuf Yusuf** |

### Actual Contributions

#### Salma-Yusuf Yusuf
- Authentication
- Scoring & Results
- AI Integration
- Final Integration & Cleanup

#### Confidence Okobru
- Question Bank
- Quiz Interface

#### Islamiyah Ibrahim
- Admin Panel

#### Abdulhakim Ibrahim
- API Integration

#### Nentapomwa Wakijssa
- Leaderboard

---

# How QuizMaster Works

## 1. Authentication

A student first registers or logs into the application. Authentication protects features that should only be available to logged-in users.

## 2. Quiz Setup

The student can select the type of quiz and relevant options such as category and difficulty.

## 3. Questions

Questions can come from the local question bank or from the Open Trivia DB API.

## 4. Quiz Interface

The selected questions are displayed through the application's user interface. The student selects answers and submits the quiz.

## 5. Scoring

The selected answers are checked against the correct answers. QuizMaster calculates:

- Score
- Total questions
- Percentage
- Performance classification
- Wrong answers

## 6. Results

The student's result can be saved and reviewed later. Wrong answers can also be reviewed.

## 7. Leaderboard

Quiz results are used to produce rankings and performance statistics.

## 8. Administrator Functions

The administrator can manage quiz questions and access administrative features.

## 9. AI Assistance

Gemini AI provides additional educational assistance, including explanations, performance analysis and practice-question generation.

---

# Online API Integration

QuizMaster uses the **Open Trivia DB API** to retrieve online multiple-choice questions.

The basic flow is:

```text
Student
   ↓
Quiz Setup
   ↓
api_service.py
   ↓
Open Trivia DB
   ↓
JSON Response
   ↓
Question Conversion
   ↓
Quiz
   ↓
Student Answers
   ↓
Scoring
   ↓
Results
```

The API service also handles validation and errors such as:

- Invalid question amount
- Invalid category
- Invalid difficulty
- Network errors
- Request timeouts
- HTTP errors
- Invalid JSON responses
- API response errors
- Too many requests
- Not enough available questions

---

# Gemini AI Integration

Google Gemini is used to provide AI-powered educational assistance.

The AI functionality includes:

- Performance analysis
- Explanations for wrong answers
- AI-assisted learning support
- AI-generated practice questions
- Study assistance

The project separates the AI integration from the online quiz API:

| Integration | Service | Purpose |
|---|---|---|
| API Integration | Open Trivia DB | Retrieves online quiz questions |
| AI Integration | Google Gemini | Provides AI learning assistance |

---

# Local Question Bank

Local questions are stored in JSON format.

The question bank supports operations such as:

- Creating questions
- Viewing questions
- Updating questions
- Deleting questions
- Searching questions
- Filtering by category
- Filtering by difficulty
- Importing questions

A typical QuizMaster question contains:

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

---

# Scoring and Performance

After a quiz is submitted, QuizMaster evaluates the student's answers.

The scoring system produces:

- Correct answers
- Wrong answers
- Total score
- Percentage
- Performance classification

The performance classification is based on the student's percentage.

---

# Results and Leaderboard

QuizMaster stores quiz results so students can review their previous performance.

The leaderboard uses quiz performance to create rankings and statistics.

This allows students to see how they are performing compared with other quiz participants.

---

# Administrator Panel

The administrator section provides tools for managing the quiz system.

Administrative functionality includes:

- Admin access
- Dashboard
- Question management
- Adding questions
- Viewing questions
- Editing/managing questions
- Deleting questions
- Quiz information

---

# Running the Project

## 1. Install Python

Make sure Python is installed on your computer.

## 2. Install Dependencies

From the project folder, run:

```bash
pip install -r requirements.txt
```

## 3. Configure Environment Variables

Use the provided environment example file:

```text
env.example
```

Add the required API configuration, including the Gemini API key where required.

## 4. Start the Flask Application

Run:

```bash
python app.py
```

Then open the local Flask address shown in the terminal in a web browser.

---

# Requirements

The project uses packages including:

```text
flask
google-genai
python-dotenv
requests
```

See `requirements.txt` for the project's dependency list.

---

# GitHub Workflow

The project was developed using feature branches.

The general workflow was:

```text
Create Feature Branch
        ↓
Develop Feature
        ↓
Commit Changes
        ↓
Push Branch
        ↓
Create Pull Request
        ↓
Review
        ↓
Merge into main
```

This approach allowed different parts of QuizMaster to be developed separately before being integrated into the main project.

---

# Project Goal

The goal of QuizMaster V2 is to create a complete and practical quiz platform that combines traditional quiz functionality with:

- Online question retrieval
- Automated scoring
- Result tracking
- Leaderboards
- Administration tools
- AI-powered educational assistance

The project demonstrates the use of Python, Flask, APIs, JSON data management, authentication, GitHub collaboration, and AI integration in one application.

---

# Contributors

### Salma-Yusuf Yusuf
Authentication • Scoring & Results • AI Integration • Final Integration & Cleanup

### Confidence Okobru
Question Bank • Quiz Interface

### Islamiyah Ibrahim
Admin Panel

### Abdulhakim Ibrahim
API Integration

### Nentapomwa Wakijssa
Leaderboard
