# QuizMaster

QuizMaster is an interactive quiz application designed to provide
students with a complete quiz experience, including user authentication,
question management, online question integration, scoring, results, a
leaderboard, an administrator panel, and AI-powered assistance.

## Project Features

-   User registration and authentication
-   Quiz interface
-   Local question bank
-   Online question/API integration
-   Automatic scoring and performance classification
-   Results and performance tracking
-   Leaderboard
-   Administrator panel
-   AI-powered assistance using Gemini
-   Flask-based web application
-   GitHub-based collaborative development

## Project Structure

The project contains both the main Flask web application and supporting
modules for quiz management, scoring, authentication, storage, APIs,
administration, and AI features.

### Main Python Files

  -----------------------------------------------------------------------
  File                                Purpose
  ----------------------------------- -----------------------------------
  `app.py`                            Main Flask application that
                                      connects the different parts of
                                      QuizMaster

  `main.py`                           Console/command-line version of the
                                      application

  `auth.py`                           Handles authentication and user
                                      accounts

  `question_bank.py`                  Creates, stores, updates, searches
                                      and retrieves quiz questions

  `question_bank_modified1.py`        Duplicate/modified copy of the
                                      question-bank module

  `quiz_engine.py`                    Controls the console quiz process

  `scoring.py`                        Calculates scores and performance
                                      levels

  `results.py`                        Saves and manages quiz results

  `leaderboard.py`                    Generates rankings and performance
                                      statistics

  `admin.py`                          Provides administrator functions
                                      and question management

  `api_service.py`                    Connects the application to the
                                      online question API

  `ai_assistant.py`                   Provides AI-related quiz assistance

  `gemini_helper.py`                  Handles communication with Google's
                                      Gemini service

  `data_store.py`                     Stores and retrieves users and quiz
                                      results

  `config.py`                         Contains project configuration and
                                      settings
  -----------------------------------------------------------------------

## GitHub Branch Contributions

The project was developed collaboratively using separate GitHub feature branches.

| Team Member | Branch | Contribution |
|---|---|---|
| **Salma-Yusuf Yusuf** | `feature/authentication` | Authentication |
| **Confidence Okobru** | `feature/question-bank` | Question Bank |
| **Islamiyah Ibrahim** | `feature/quiz-interface` | Quiz Interface |
| **Oluwatosin Ajayi** | `feature/scoring-results` | Scoring & Results |
| **Nentapomwa Wakijssa** | `feature/leaderboard` | Leaderboard |
| **Abdulhakim Ibrahim** | `feature/admin-panel` | Administrator Panel |
| **Abubakar Yusuf** | `feature/api-integration` | API Integration |
| **Emmanuel Nweke** | `feature/ai-integration` | AI Integration |
| **Salma-Yusuf Yusuf** | `feature/final-integration-cleanup` | Final Integration & Cleanup |

## How the Main Components Work Together

``` text
User
  |
  v
app.py
  |
  +-- Authentication
  +-- Quiz Interface
  +-- Question Bank
  +-- API Integration
  +-- Scoring & Results
  +-- Leaderboard
  +-- Admin Panel
  +-- AI Assistant
  |
  v
Stored Data / External Services
```

### Authentication

Users can register and log in before accessing protected quiz features.

### Question Bank

QuizMaster can use questions stored locally and can also retrieve
questions through the online API.

### Quiz Interface

Students select quiz options and submit their answers through the
application interface.

### Scoring and Results

Submitted answers are checked, scores are calculated, performance is
classified, and results are stored for later viewing.

### Leaderboard

Student performance can be compared through rankings.

### Admin Panel

Administrators can manage quiz-related information and questions.

### AI Integration

The project includes Gemini-based AI functionality for assistance such
as explanations and other learning support.

## Technologies Used

-   Python
-   Flask
-   HTML/CSS
-   JSON
-   Git & GitHub
-   Open Trivia DB API
-   Google Gemini AI

## Running the Project

1.  Clone or download the repository.
2.  Install the required Python packages.
3.  Configure the required environment variables, including the Gemini
    API key where needed.
4.  Run the Flask application.
5.  Open the application in a web browser.

## Collaboration

GitHub feature branches were used to separate different areas of
development. Each contributor worked on specific functionality before
the features were integrated into the main project.

## Project Goal

The goal of QuizMaster is to provide a practical and user-friendly quiz
platform that combines traditional quiz functionality with online
question retrieval, automated scoring, performance tracking,
administration tools, and AI-assisted learning.
