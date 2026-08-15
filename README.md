# 🔍 PR Risk Detector

An AI-powered Pull Request risk analysis tool that evaluates GitHub Pull Requests using a combination of AI analysis and rule-based risk detection.

## 🚀 Live Demo

https://pr-risk-detector.streamlit.app/

## ✨ Features

- 🔗 Analyze Pull Requests directly from GitHub
- 🤖 AI-powered risk analysis
- 📊 Rule-based risk scoring
- 🎯 Combined final risk score
- 🔴🟠🟢 High / Medium / Low risk classification
- 🔍 Risk factors and recommendations
- 📈 Risk overview dashboard
- 🔎 Search analyzed Pull Requests
- 🏷️ Filter PRs by risk level
- 🔗 Direct links to GitHub Pull Requests
- 🌐 Supports different GitHub owners and repositories
- 💾 Stores analyzed PR results

## 🧠 How It Works

The application follows this pipeline:

GitHub Repository
        ↓
Pull Request Selection
        ↓
GitHub API
        ↓
AI Analysis + Rule-Based Analysis
        ↓
Risk Score Calculation
        ↓
Final Risk Level
        ↓
Dashboard

## 📊 Risk Scoring

The final score combines two sources:

- AI Risk Score → 60%
- Rule-Based Score → 40%

```text
Final Score = 0.6 × AI Score + 0.4 × Rule Score

| Score  | Risk Level |
| ------ | ---------- |
| 70–100 | HIGH       |
| 40–69  | MEDIUM     |
| 0–39   | LOW        |
🛠️ Tech Stack
Python
Streamlit
GitHub API
Google Gemini API
JSON
Git & GitHub
⚙️ Run Locally

Clone the repository:

git clone https://github.com/VedantTawari/pr-risk-detector.git
cd pr-risk-detector

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Create a .env file and add the required API keys.

Run the application:

streamlit run app.py
📁 Project Structure
pr-risk-detector/
│
├── app.py
├── analyzer.py
├── main.py
├── results.json
├── requirements.txt
├── README.md
├── .env
└── .gitignore
🎯 Why This Project?

Code reviews are an important part of software development, but identifying potentially risky Pull Requests manually can be time-consuming.

PR Risk Detector helps developers quickly identify potentially risky changes by combining AI-based reasoning with deterministic rule-based checks.

🔮 Future Improvements
GitHub webhook integration
Automatic PR analysis
Historical risk trends
Repository-level risk analytics
More advanced code-change analysis
Authentication and multi-user support
👨‍💻 Author

Vedant Tawari

GitHub: https://github.com/VedantTawari