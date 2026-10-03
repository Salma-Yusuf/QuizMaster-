QuizMaster V2 — AI-Powered Quiz Management System

1. Project Overview
QuizMaster V2 is a Python-based quiz management system developed as a collaborative GitHub project.
The system supports:
Student registration and login
Admin login and administration
Local quiz questions stored in JSON
Online multiple-choice quizzes using the Open Trivia DB API
Automatic score calculation
Percentage and performance classification
Quiz result history
Wrong-answer review
Leaderboard and performance statistics
Google Gemini AI features
Importing questions into the local question bank
GitHub-based team development using feature branches
The project is designed to demonstrate Python programming, JSON/file handling, API integration, AI integration, authentication, modular programming, and Git/GitHub collaboration.

2. Technologies Used
Programming Language
Python 3
Data Storage
The project uses JSON files for local data:
data/
├── questions.json
├── users.json
└── results.json
External APIs
Open Trivia DB
Used for the Online API Quiz.
Open Trivia DB provides live multiple-choice questions. QuizMaster sends a request, receives the response as JSON, processes the response, and converts each question into the format used by the QuizMaster quiz engine.
Google Gemini API
Used for:
AI performance analysis
Explanations for wrong answers
AI-generated practice questions

3. Project Structure
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
├── .env.example
├── .gitignore
├── BRANCH_GUIDE.md
├── README.md
│
└── data/
    ├── questions.json
    ├── users.json
    └── results.json

4. What Each Python File Does
main.py
This is the main controller of the application.
It connects the major parts of QuizMaster and displays the main menus.
It provides access to:
Registration
Student login
Admin login
Local quizzes
Online API quizzes
Results
Wrong-answer review
Leaderboard
Gemini AI assistant
It imports the API function using:
from api_service import fetch_questions
This allows the main program to request online questions without needing to contain the API connection code itself.
auth.py
Handles user authentication.
Responsibilities include:
Student registration
Student login
Admin login
User information
quiz_engine.py
Controls the quiz interaction.
It is responsible for:
Displaying questions
Displaying answer options
Accepting the student's answer
Managing the quiz flow
The API questions are converted into the same general question structure expected by the quiz system.
question_bank.py
Handles the local question bank.
It supports operations such as:
Adding questions
Editing questions
Deleting questions
Viewing questions
Importing questions
Working with categories and difficulty levels
Local questions are stored in:
data/questions.json
scoring.py
Handles quiz scoring.
It calculates:
Number of correct answers
Total score
Percentage
Performance classification
The same scoring system can be used after a local quiz or an online API quiz.
results.py
Handles quiz results.
It can:
Save quiz results
Load previous results
Display student results
Review wrong answers
Display recent results
Provide result summaries
Results are stored in:
data/results.json
leaderboard.py
Uses saved quiz results to provide:
Leaderboard rankings
Student statistics
Performance statistics
The leaderboard uses the results saved by the quiz system.
admin.py
Provides administrator functionality.
The admin area can be used for question management and other administrative operations supported by the project.

5. API Integration
What API Integration Means in QuizMaster
API integration allows QuizMaster to communicate with an external online service.
For this project, the external service is:
Open Trivia DB
The basic flow is:
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
api_service.py
   ↓
QuizMaster question format
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

6. api_service.py
The API integration is kept in its own module so that the rest of the application does not need to deal directly with internet requests, JSON conversion, validation, or API errors.
Main API endpoints
BASE_URL = "https://opentdb.com/api.php"
This endpoint provides quiz questions.
CATEGORY_URL = "https://opentdb.com/api_category.php"
This endpoint provides available categories.
Main API Function
The main function is:
fetch_questions(
    amount=5,
    category_id=None,
    difficulty=None
)
It:
Validates the requested number of questions.
Validates the difficulty.
Validates the optional category.
Builds the API request.
Sends the request to Open Trivia DB.
Receives JSON data.
Checks the API response code.
Converts the questions into QuizMaster format.
Returns the usable questions.
Example:
questions = fetch_questions(
    amount=5,
    difficulty="easy"
)
This requests five easy multiple-choice questions.

7. Converting API Questions
Open Trivia DB provides information such as:
question
correct_answer
incorrect_answers
category
difficulty
QuizMaster converts that information into a structure such as:
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
The conversion is important because the rest of QuizMaster expects questions in its own format.

8. Answer Shuffling
The API provides one correct answer and three incorrect answers.
The code combines them and uses:
random.shuffle(options)
This randomly changes the order of the four options.
The program then finds the new letter containing the correct answer.
This prevents the correct answer from always appearing in the same position.

9. API Error Handling
The API integration includes handling for problems such as:
Invalid number of questions
Invalid difficulty
Invalid category
No internet connection
Timeout
HTTP errors
Invalid JSON
Open Trivia DB response errors
Not enough available questions
Too many requests
Invalid API parameters
The custom error class is:
class APIServiceError(Exception):
    pass
This allows API-related problems to be handled separately from other parts of the application.

10. API Test
api_service.py contains a direct test.
Run:
python api_service.py
If the API connection works, the program requests three easy questions and displays them.
Expected output begins similar to:
=============================================
QUIZMASTER V2 - API INTEGRATION TEST
=============================================

API connection successful.
Questions received: 3
An internet connection is required for this test.

11. How the API Quiz Works
When a student logs in, the student dashboard contains:
1. Local Quiz
2. Online API Quiz
3. My Results
4. Review Wrong Answers
5. Leaderboard
6. Gemini AI Assistant
7. Logout
When the student selects:
2. Online API Quiz
main.py calls:
fetch_questions()
from api_service.py.
The API questions are then displayed using the quiz interaction from quiz_engine.py.
After the student finishes:
API Questions
      ↓
Student Answers
      ↓
Score Calculation
      ↓
Performance Classification
      ↓
Result Saved
The online quiz result is marked with:
"source": "Open Trivia DB"

12. Local Quiz vs Online API Quiz
QuizMaster supports two question sources.
Local Quiz
Questions come from:
data/questions.json
Flow:
questions.json
     ↓
question_bank / quiz_engine
     ↓
student
     ↓
scoring
     ↓
results
Online API Quiz
Questions come from:
Open Trivia DB
Flow:
Open Trivia DB
     ↓
api_service.py
     ↓
quiz_engine.py
     ↓
student
     ↓
scoring.py
     ↓
results.py
Both quiz types use the same general scoring and result system.

13. Gemini AI Integration
Gemini is separate from the Open Trivia DB API.
The API is responsible for obtaining quiz questions.
Gemini is responsible for AI-based features.
The project currently uses Gemini for:
Performance analysis
The AI can analyze the student's latest quiz result and provide:
Strengths
Weak areas
Study recommendations
Wrong-answer explanations
The AI can explain:
The question
The student's selected answer
The correct answer
Why the correct answer is correct
Practice questions
The AI can generate multiple-choice practice questions based on:
Topic
Difficulty
Requested number of questions
Generated questions can then be imported into the local question bank.

14. Gemini Configuration
The project uses:
GEMINI_API_KEY
The API key should be stored in a .env file.
Example:
GEMINI_API_KEY=your_api_key_here
The project also supports an optional model setting:
GEMINI_MODEL=gemini-2.5-flash
Do not upload a real API key to GitHub.

15. Installation
Make sure Python 3 is installed.
From the project folder, run:
pip install -r requirements.txt
The current requirements include:
google-genai
python-dotenv
requests

16. Environment Setup
Create a .env file based on .env.example.
Add your Gemini API key:
GEMINI_API_KEY=your_api_key_here
Keep the .env file private.
The .gitignore file is used to prevent sensitive files such as .env from being committed to GitHub.

17. Running QuizMaster
From the project directory:
python main.py
The main menu appears:
================================
          QUIZMASTER V2
================================
1. Register
2. Student Login
3. Admin Login
4. Exit

18. Basic Testing
Test the API separately
Run:
python api_service.py
Test the complete application
Run:
python main.py
Then test:
Student registration
Student login
Local quiz
Online API quiz
Score calculation
Result saving
Wrong-answer review
Leaderboard
Gemini AI features
Admin login and administration

19. GitHub Branch Structure
The project uses a main branch and eight feature branches.
Member
Branch
Main Responsibility
Salma-Yusuf Yusuf
feature/authentication
Project leadership, authentication and final integration
Confidence Okobru
feature/question-bank
Question bank and data management
Islamiyah Ibrahim
feature/quiz-interface
Quiz interaction and interface
Oluwatosin Ajayi
feature/scoring-results
Scoring and results
Nentapomwa Wakijssa
feature/leaderboard
Leaderboard and statistics
Abdulhakim Ibrahim
feature/admin-panel
Admin panel
Abubakar Yusuf
feature/api-integration
Open Trivia DB API
Emmanuel Nweke
feature/ai-integration
Gemini AI integration

20. GitHub Workflow
Each member works on their assigned branch.
General workflow:
Create / use feature branch
        ↓
Write and test code
        ↓
Commit changes
        ↓
Push branch to GitHub
        ↓
Create Pull Request
        ↓
Code review
        ↓
Merge into main
For the API branch:
git checkout -b feature/api-integration
After completing the API work:
git add .
git commit -m "Upgrade Open Trivia DB API integration"
git push -u origin feature/api-integration
Then create a Pull Request into:
main

21. API Branch Responsibility
The API-integration branch is responsible for:
Open Trivia DB integration
Online multiple-choice quiz
JSON response processing
Converting API data into QuizMaster format
Input validation
API/network error handling
API integration testing
The API branch should not replace the responsibilities of the Gemini AI branch.

22. AI Branch Responsibility
The AI-integration branch is responsible for:
Google Gemini API
Performance analysis
Wrong-answer explanations
AI-generated practice questions
AI testing
This separation allows the team members to work independently and later combine their work through GitHub.

23. Data Flow of the Complete System
                     QUIZMASTER V2
                           |
             +-------------+-------------+
             |                           |
        LOCAL QUIZ                  ONLINE QUIZ
             |                           |
    questions.json               Open Trivia DB
             |                           |
             +-------------+-------------+
                           |
                    quiz_engine.py
                           |
                      Student Answers
                           |
                      scoring.py
                           |
                 Score + Percentage
                           |
                      results.py
                           |
                    results.json
                           |
                +----------+----------+
                |                     |
          leaderboard.py        AI Assistant
                                    |
                              Google Gemini

24. Security Notes
Never commit sensitive credentials.
Do not upload:
.env
or a real:
GEMINI_API_KEY
to GitHub.
Use .env.example to show the required variable names without exposing the real key.

25. Project Goal
The goal of QuizMaster V2 is to demonstrate how different Python components can work together in one modular application.
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

26. Quick Start
pip install -r requirements.txt
Configure .env:
GEMINI_API_KEY=your_api_key_here
Test the Open Trivia DB integration:
python api_service.py
Run QuizMaster:
python main.py

27. Important Files for the Updated API Integration
The main file added/upgraded for the online quiz is:
api_service.py
The existing application connects to it through:
from api_service import fetch_questions
The online quiz is started from main.py through the student's:
Online API Quiz
option.
The API integration therefore works as part of the existing QuizMaster system rather than as a separate application.
