# 🛡️ PR Risk Detector

AI-powered GitHub Pull Request risk analysis tool that combines **Google Gemini AI** with **rule-based analysis** to identify potentially risky Pull Requests.

The system analyzes Pull Request metadata, code changes, dependency updates, and other risk indicators to generate an overall risk score and recommendation.

---

## 🚀 Features

- 🔍 Fetch Pull Requests from GitHub
- 🤖 AI-powered Pull Request analysis using Google Gemini
- 📊 Rule-based risk scoring
- 🧮 Combined AI + rule-based final risk score
- 🔴 HIGH / 🟠 MEDIUM / 🟢 LOW risk classification
- 🔎 Search Pull Requests by number or title
- 🎯 Filter Pull Requests by risk level
- 📈 Risk overview dashboard
- 💡 AI-generated recommendations
- ⚡ Analyze individual Pull Requests on demand
- 🔐 Secure API key management using environment variables

---

## 🧠 How It Works

The application uses two different approaches to analyze a Pull Request.

### 1. Rule-Based Analysis

The system checks predefined risk factors such as:

- Number of changed files
- Number of additions and deletions
- Extremely large code changes
- Security-related changes
- Bug fixes
- Dependabot updates
- Large diffs

These checks generate a **Rule Score** between 0 and 100.

### 2. AI Analysis

The Pull Request information and code diff are sent to **Google Gemini**.

Gemini analyzes the Pull Request and returns:

- AI Risk Score
- Risk Level
- Risk Factors
- Recommendation

### 3. Final Risk Score

The final score combines both approaches:

```text
Final Score = (0.6 × AI Risk Score) + (0.4 × Rule Score)

| Final Score | Risk Level |
| ----------- | ---------- |
| 0 - 39      | 🟢 LOW     |
| 40 - 69     | 🟠 MEDIUM  |
| 70 - 100    | 🔴 HIGH    |

🏗️ System Architecture
                  GitHub Repository
                         │
                         ▼
                   GitHub REST API
                         │
                         ▼
                Pull Request Data
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
       Rule-Based Analysis     Gemini AI Analysis
              │                     │
              ▼                     ▼
         Rule Score             AI Risk Score
              │                     │
              └──────────┬──────────┘
                         │
                         ▼
                  Final Risk Score
                         │
                         ▼
                  Risk Classification
                         │
                         ▼
                Streamlit Dashboard


🛠️ Tech Stack
Python
Streamlit
GitHub REST API
Google Gemini API
Requests
python-dotenv
JSON

📁 Project Structure
pr-risk-detector/
│
├── analyzer.py
├── app.py
├── main.py
├── results.json
├── requirements.txt
├── README.md
├── .gitignore
└── .env

| File               | Purpose                                                         |
| ------------------ | --------------------------------------------------------------- |
| `analyzer.py`      | GitHub API integration, rule-based analysis and Gemini analysis |
| `app.py`           | Streamlit web application                                       |
| `main.py`          | Main project entry point / supporting logic                     |
| `results.json`     | Stores analyzed Pull Request results                            |
| `requirements.txt` | Python dependencies                                             |
| `.gitignore`       | Prevents sensitive/unnecessary files from being committed       |
| `.env`             | Stores API credentials locally                                  |
| `README.md`        | Project documentation                                           |

⚙️ Installation
1. Clone the repository
git clone https://github.com/VedantTawari/pr-risk-detector.git

Move into the project directory:

cd pr-risk-detector
2. Create a Virtual Environment
python -m venv .venv
3. Activate the Virtual Environment

For Windows PowerShell:

.venv\Scripts\Activate.ps1
4. Install Dependencies
pip install -r requirements.txt
🔑 Environment Variables

Create a .env file in the project root.

Add:

GITHUB_TOKEN=your_github_token
GEMINI_API_KEY=your_gemini_api_key

Replace the values with your own API credentials.

⚠️ Important

Never commit your .env file to GitHub.

The project uses .gitignore to prevent API keys and virtual-environment files from being tracked.

▶️ Running the Application

Start the Streamlit application:

streamlit run app.py

The application will open in your browser.

Default local address:

http://localhost:8501
🖥️ Dashboard

The Streamlit dashboard provides:

Risk Summary

The dashboard displays:

Total Pull Requests
High Risk Pull Requests
Medium Risk Pull Requests
Low Risk Pull Requests
Average Risk Score
Risk Overview

Visual charts show:

Distribution of Pull Requests by risk level
Risk scores of analyzed Pull Requests
Pull Request Search

Pull Requests can be searched using:

PR number
PR title
Risk Filtering

Pull Requests can be filtered by:

All
HIGH
MEDIUM
LOW
🔍 Analyze a Pull Request

Users can enter a Pull Request number and click:

Analyze PR

The application then:

Fetches the Pull Request from GitHub.
Retrieves Pull Request metadata.
Retrieves the Pull Request diff.
Calculates the rule-based score.
Sends the Pull Request to Gemini.
Receives the AI risk analysis.
Combines the AI and rule-based scores.
Determines the final risk level.
Displays risk factors and recommendations.
📋 Example Risk Factors

The system can identify risks such as:

Major dependency upgrade
Large code change
Security-related modification
Large lockfile modification
Unexpected dependency changes
Automated dependency update
Large Pull Request diff
🤖 AI Analysis

Google Gemini is used to understand the context of Pull Requests beyond simple numerical rules.

For example, a Pull Request may contain a relatively small number of changed files but introduce a major dependency upgrade.

The AI can identify the potential impact and provide a recommendation for additional review.

🔐 Security

This project uses environment variables for sensitive credentials.

Sensitive files such as:

.env
.venv/
__pycache__/
*.pyc

are excluded using .gitignore.

Never expose:
GitHub Personal Access Tokens
Gemini API Keys
Other private credentials

If a credential is accidentally exposed, revoke or rotate it immediately.

⚠️ Current Limitations
Gemini responses can vary between analyses.
The current system analyzes a limited number of Pull Requests at a time.
Results are stored locally in results.json.
There is no database yet.
Automatic GitHub webhook integration is not implemented yet.
The current rule engine uses predefined heuristics.
🔮 Future Improvements

Planned improvements include:

🔔 Automatic analysis when a Pull Request is opened
💬 Automatically post risk reports as GitHub PR comments
🪝 GitHub Webhook integration
🗄️ Database-backed result storage
📈 Historical risk tracking
🔐 User authentication
🛡️ Advanced security rules
🔎 Dependency vulnerability scanning
🧠 Improved AI risk analysis
☁️ Cloud deployment
📊 More advanced analytics
🚨 Automated alerts for HIGH-risk Pull Requests
🎯 Project Goal

The goal of PR Risk Detector is to help development teams quickly identify Pull Requests that may require additional review.

Instead of relying only on manual code review, the system combines:

GitHub Data
     +
Rule-Based Security Checks
     +
AI Analysis
     ↓
Risk Score
     ↓
Actionable Recommendation

This can help reviewers prioritize potentially high-risk Pull Requests.

👨‍💻 Author

Vedant Tawari

GitHub:

https://github.com/VedantTawari

Project Repository:

https://github.com/VedantTawari/pr-risk-detector

⭐ Future Vision

PR Risk Detector can evolve into an automated security layer for GitHub Pull Requests that analyzes changes in real time and assists developers and security teams before potentially risky code reaches production.

⭐ If you find this project useful, consider giving the repository a star!
