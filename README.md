#QuizMaster V2 — AI-Powered Quiz Management System

A modular Python quiz management system for students and administrators. QuizMaster combines local and online quizzes, authentication, scoring, results, leaderboard statistics, Open Trivia DB API integration, and Google Gemini AI features.
QuizMaster V2 is a Python-based quiz management system developed as a collaborative GitHub project.
The system combines local quiz questions, online questions from the Open Trivia DB API, automated scoring and results, leaderboard statistics, authentication, administration, and Google Gemini AI features.
Features
Student registration and login
Admin login and administration
Local quiz questions stored in JSON
Online multiple-choice quizzes using the Open Trivia DB API
Automatic score calculation
Percentage and performance classification
Quiz result history
Wrong-answer review
Leaderboard and performance statistics
Google Gemini AI performance analysis
AI explanations for wrong answers
AI-generated practice questions
Question-bank management
JSON/file handling
Git/GitHub collaborative development
Technologies
Python 3
JSON
Open Trivia DB API
Google Gemini API
Git & GitHub
Official resources
Python
Open Trivia DB
Open Trivia DB API documentation
Google Gemini API documentation
Project Structure
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
Main Python Files
File
Purpose
main.py
Main controller that connects the major parts of QuizMaster
auth.py
Handles student registration, login, and admin login
quiz_engine.py
Displays questions and collects student answers
question_bank.py
Manages the local question bank
scoring.py
Calculates scores, percentages, and performance classifications
results.py
Saves, loads, and reviews quiz results
leaderboard.py
Displays rankings and performance statistics
admin.py
Provides administrator functions
api_service.py
Connects QuizMaster to the Open Trivia DB API
ai_assistant.py
Connects QuizMaster to Google Gemini AI
config.py
Stores project configuration/settings
Local Quiz and Online API Quiz
QuizMaster supports two main sources of quiz questions.
Local Quiz
Questions are loaded from:
data/questions.json
Basic flow:
questions.json
      ↓
quiz_engine.py
      ↓
Student answers
      ↓
scoring.py
      ↓
results.py
Online API Quiz
Questions are retrieved from Open Trivia DB.
Basic flow:
main.py
   ↓
api_service.py
   ↓
Open Trivia DB
   ↓
JSON response
   ↓
QuizMaster question format
   ↓
quiz_engine.py
   ↓
scoring.py
   ↓
results.py
   ↓
leaderboard.py
Open Trivia DB API Integration
The API integration is implemented in:
api_service.py
The main endpoint is:
https://opentdb.com/api.php
The category endpoint is:
https://opentdb.com/api_category.php
main.py imports the main API function:
from api_service import fetch_questions
The main function is:
fetch_questions(
    amount=5,
    category_id=None,
    difficulty=None
)
It:
Validates the number of questions.
Validates the difficulty.
Validates the optional category.
Builds the API request.
Sends the request to Open Trivia DB.
Receives the JSON response.
Checks the API response code.
Converts the questions into QuizMaster format.
Returns the usable questions.
API Question Conversion
Open Trivia DB returns information such as:
question
correct_answer
incorrect_answers
category
difficulty
QuizMaster converts this into its question structure:
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
The answer options are shuffled so that the correct answer is not always displayed in the same position.
API Error Handling
The API service handles problems such as:
Invalid question amount
Invalid difficulty
Invalid category
Internet connection errors
Timeouts
HTTP errors
Invalid JSON responses
Open Trivia DB response errors
Not enough available questions
Too many API requests
A custom error class is used:
class APIServiceError(Exception):
    pass
Google Gemini AI Integration
Gemini AI is handled separately in:
ai_assistant.py
The AI features include:
Performance analysis
Wrong-answer explanations
AI-generated practice questions
AI testing
The API and AI integrations have separate responsibilities:
Integration
Service
Main Purpose
API Integration
Open Trivia DB
Retrieve online quiz questions
AI Integration
Google Gemini
Analysis, explanations, and practice questions
Gemini API Key
The project uses an environment variable:
GEMINI_API_KEY
A .env file can contain:
GEMINI_API_KEY=your_api_key_here
Do not commit a real API key to GitHub.
The .env.example file can be used as a template.
Scoring and Results
After a student answers a quiz:
Student answers
      ↓
scoring.py
      ↓
Score + Percentage
      ↓
Performance classification
      ↓
results.py
      ↓
data/results.json
The result can then be used by the leaderboard and AI features.
For an online API quiz, the result also records:
"source": "Open Trivia DB"
Leaderboard
leaderboard.py uses saved results to provide:
Leaderboard rankings
Student statistics
Overall performance statistics
The leaderboard therefore works from the results generated by the quiz system rather than directly communicating with the Open Trivia DB API.
Authentication
auth.py handles:
Student registration
Student login
Admin login
User information
User data is stored in:
data/users.json
Administration
admin.py provides administrator functionality, including project-supported question and administrative operations.
Requirements
The project includes:
requirements.txt
This file lists the external Python packages required by the project.
Install the requirements with:
pip install -r requirements.txt
Do not create another requirements.txt if the existing project file is already present.
Running the Project
From the QuizMaster project directory, run:
python main.py
The application then provides the available QuizMaster menus.
Testing the API Integration
The upgraded api_service.py contains a direct API test.
Run:
python api_service.py
The test requests three easy questions.
A successful test begins with output similar to:
=============================================
QUIZMASTER V2 - API INTEGRATION TEST
=============================================

API connection successful.
Questions received: 3
An internet connection is required.
GitHub Branch Structure
The project uses separate feature branches for team development.
Member
GitHub Branch
Responsibility
Salma-Yusuf Yusuf
feature/authentication
Project Leader & Authentication
Confidence Okobru
feature/question-bank
Question Bank & Data Management
Islamiyah Ibrahim
feature/quiz-interface
Quiz Interface / UI
Oluwatosin Ajayi
feature/scoring-results
Scoring & Results
Nentapomwa Wakijssa
feature/leaderboard
Leaderboard & Performance Statistics
Abdulhakim Ibrahim
feature/admin-panel
Administrator Panel
Abubakar Yusuf
feature/api-integration
Open Trivia DB API Integration
Emmanuel Nweke
feature/ai-integration
Gemini AI Integration & AI Testing
GitHub Workflow
The general team workflow is:
Feature branch
      ↓
Develop code
      ↓
Test code
      ↓
Commit changes
      ↓
Push branch
      ↓
Create Pull Request
      ↓
Code review
      ↓
Merge into main
The API integration work belongs to:
feature/api-integration
The Gemini AI work belongs to:
feature/ai-integration
Project-wide files such as README.md, requirements.txt, config.py, and BRANCH_GUIDE.md support the overall project and can be included in the final main branch.
Complete System Flow
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
Security
Do not upload sensitive credentials to GitHub.
Never commit a real:
.env
file containing your Gemini API key.
Use:
.env.example
to show the required environment variables without exposing the real credentials.
Quick Start
1. Install dependencies
pip install -r requirements.txt
2. Configure Gemini
Create a .env file and add:
GEMINI_API_KEY=your_api_key_here
3. Test the Open Trivia DB API
python api_service.py
4. Run QuizMaster
python main.py
Project Goal
QuizMaster V2 demonstrates how several Python components can work together as one modular application.
The project combines:
Python
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
Each module has a specific responsibility while main.py connects the major features into the overall application.
