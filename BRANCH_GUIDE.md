# QuizMaster V2 — 8-Member GitHub Branch Guide

## 1. Salma-Yusuf Yusuf — `feature/authentication`
- Project leader
- Student registration/login
- Admin login
- Password handling
- Final integration and Pull Request review

## 2. Confidence Okobru — `feature/question-bank`
- Add/edit/delete/view questions
- Categories and difficulty
- Local JSON question storage
- Question import support

## 3. Islamiyah Ibrahim — `feature/quiz-interface`
- Quiz interaction flow
- Question display
- Answer selection
- User-facing console interface improvements

## 4. Oluwatosin Ajayi — `feature/scoring-results`
- Score calculation
- Percentage
- Performance classification
- Result display and wrong-answer review

## 5. Nentapomwa Wakijssa — `feature/leaderboard`
- Leaderboard sorting
- Rankings
- Performance statistics display

## 6. Abdulhakim Ibrahim — `feature/admin-panel`
- Admin dashboard
- Add/view/edit/delete questions
- Admin access to leaderboard

## 7. Abubakar Yusuf — `feature/api-integration`
- Open Trivia DB integration
- Online multiple-choice quiz
- JSON response conversion
- API error handling

## 8. Emmanuel Nweke — `feature/ai-integration`
- Google Gemini API integration
- AI performance analysis
- AI explanations for wrong answers
- AI-generated practice questions
- AI testing

## Git workflow

Create a branch:
```bash
git checkout -b feature/api-integration
```

Commit:
```bash
git add .
git commit -m "Add Open Trivia DB integration"
```

Push:
```bash
git push -u origin feature/api-integration
```

Then create a Pull Request into `main`.
