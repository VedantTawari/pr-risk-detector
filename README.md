# PR Risk Detector

An AI-powered Pull Request Risk Analyzer that evaluates GitHub Pull Requests using rule-based scoring, Gemini AI, and Retrieval-Augmented Generation (RAG).

## Features

- Fetch Pull Requests directly from GitHub
- Analyze PR title, description, and code diff
- Rule-based risk scoring
- AI-based risk analysis using Gemini
- RAG-based retrieval of similar historical Pull Requests
- Gemini embeddings with ChromaDB
- Combined final risk score
- Risk levels: LOW, MEDIUM, HIGH
- Risk factors and recommendations
- Streamlit web interface
- Automatically stores newly analyzed PRs in the RAG knowledge base

## Architecture

GitHub API
↓
Pull Request Data
↓
Rule Engine ─────────┐
                     ↓
                Final Risk Score
                     ↑
Gemini AI ← RAG Context
    ↑                    ↑
    │                ChromaDB
    │                    ↑
Gemini Embeddings ← Historical PRs

## How It Works

### 1. Fetch Pull Request

The application uses the GitHub API to retrieve:

- Pull Request title
- Description
- Author
- Number of changed files
- Additions
- Deletions
- Code diff

### 2. Rule-Based Analysis

The system checks factors such as:

- Number of changed files
- Size of code changes
- Security-related changes
- Bug fixes
- Dependabot updates
- Large diffs

This produces a rule-based risk score.

### 3. RAG Retrieval

The PR title and description are converted into an embedding using Gemini's `gemini-embedding-001` model.

ChromaDB searches the historical PR knowledge base and retrieves the most similar Pull Requests.

### 4. AI Analysis

Gemini analyzes the current Pull Request using:

- PR information
- Code diff
- Similar historical Pull Requests

It generates:

- AI risk score
- Risk level
- Risk factors
- Recommendation

### 5. Final Risk Score

The final score combines AI analysis and rule-based analysis:

Final Score = 60% AI Score + 40% Rule Score

Risk levels:

- 0–39 → LOW
- 40–69 → MEDIUM
- 70–100 → HIGH

### 6. Knowledge Base Update

After a PR is analyzed, its result is converted into a document, embedded, and stored in ChromaDB.

This allows future Pull Requests to use previously analyzed PRs as historical context.

## Tech Stack

- Python
- Streamlit
- GitHub REST API
- Google Gemini API
- Gemini Embeddings
- ChromaDB
- Requests
- python-dotenv

## Project Structure

```text
pr-risk-detector/
│
├── app.py
├── analyzer.py
├── rag.py
├── results.json
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

1. Clone the repository
git clone <your-repository-url>
cd pr-risk-detector
2. Create virtual environment
python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables

Create a .env file:

GITHUB_TOKEN=your_github_token
GEMINI_API_KEY=your_gemini_api_key
5. Run the application
streamlit run app.py

The application will open in your browser.

RAG Pipeline
Historical PR
     ↓
Create Document
     ↓
Gemini Embedding
     ↓
ChromaDB
     ↓
Vector Search
     ↑
New PR → Query Embedding

The system retrieves the most semantically similar historical Pull Requests rather than simply matching keywords.

Future Improvements
GitHub webhook integration
Automatic PR monitoring
CI/CD integration
More advanced code-diff analysis
Risk trend visualization
Repository-level risk analytics
Automated GitHub comments
Multi-repository support