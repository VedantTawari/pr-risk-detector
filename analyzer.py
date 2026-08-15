import os
import json
import requests
from google import genai
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def get_pull_request(owner, repo, pr_number):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(response.json())
        return None

    data = response.json()

    diff_url = data["diff_url"]

    diff_response = requests.get(
        diff_url,
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.diff"
        }
    )

    diff = diff_response.text

    MAX_DIFF_LENGTH = 30000

    if len(diff) > MAX_DIFF_LENGTH:
        diff = diff[:MAX_DIFF_LENGTH] + "\n\n[DIFF TRUNCATED]"

    return {
    "title": data["title"],
    "body": data["body"],
    "state": data["state"],
    "author": data["user"]["login"],
    "changed_files": data["changed_files"],
    "additions": data["additions"],
    "deletions": data["deletions"],
    "diff": diff
    }

def get_open_prs(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    params = {
        "state": "open"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print("Error:", response.status_code)
        print(response.json())
        return []

    return response.json()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def calculate_rule_score(pr):
    score = 0
    factors = []

    changed_files = pr["changed_files"]
    additions = pr["additions"]
    deletions = pr["deletions"]
    diff = pr["diff"]

    if changed_files >= 10:
        score += 15
        factors.append("Large number of files changed")

    if additions + deletions >= 1000:
        score += 15
        factors.append("Large code change")

    if additions + deletions >= 5000:
        score += 10
        factors.append("Extremely large code change")

    if "security" in pr["title"].lower() or "security" in pr["body"].lower():
        score += 20
        factors.append("Security-related change")

    if "fix" in pr["title"].lower() and "bug" in pr["title"].lower():
        score += 10
        factors.append("Bug fix")

    if pr["author"].lower().startswith("dependabot"):
        score -= 10
        factors.append("Automated Dependabot update")

    if len(diff) >= 30000:
        score += 10
        factors.append("Large diff")

    score = max(0, min(score, 100))

    return score, factors


def analyze_pr(pr_data):
    prompt = f"""
You are a Pull Request Risk Analyzer.

Analyze this pull request:

{pr_data}

Return:
- risk_score: integer from 0 to 100
- risk_level: LOW, MEDIUM, or HIGH
- risk_factors: list of strings
- recommendation: string
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": {
                    "type": "OBJECT",
                    "properties": {
                        "risk_score": {
                            "type": "INTEGER"
                        },
                        "risk_level": {
                            "type": "STRING"
                        },
                        "risk_factors": {
                            "type": "ARRAY",
                            "items": {
                                "type": "STRING"
                            }
                        },
                        "recommendation": {
                            "type": "STRING"
                        }
                    },
                    "required": [
                        "risk_score",
                        "risk_level",
                        "risk_factors",
                        "recommendation"
                    ]
                }
            }
        )

        return response.text.strip()

    except Exception as e:
        error_message = str(e)

        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
            raise Exception(
                "Gemini API quota exceeded. Please use another Gemini API key "
                "or wait for the quota to reset."
            )

        raise Exception(
            f"Gemini API error: {error_message}"
        )



if __name__ ==  "__main__":
    results = []
    prs = get_open_prs("adagentpc-del", "divini-procure")

    prs = prs[:5]

    for pr in prs:
        print("Analyzing PR:", pr["number"])

        full_pr = get_pull_request(
            "adagentpc-del",
            "divini-procure",
            pr["number"]
        )

        rule_score, rule_factors = calculate_rule_score(full_pr)

        result = analyze_pr(full_pr)

        data = json.loads(result)

        data["rule_score"] = rule_score
        data["rule_factors"] = rule_factors

        final_score = int(
        0.6 * data["risk_score"] +
        0.4 * rule_score
        )

        if final_score >= 70:
            final_level = "HIGH"
        elif final_score >= 40:
            final_level = "MEDIUM"
        else:
            final_level = "LOW"

        data["final_score"] = final_score
        data["final_level"] = final_level

        results.append({
        "number": pr["number"],
        "title": pr["title"],
        "risk_score": data["risk_score"],
        "risk_level": data["risk_level"],
        "risk_factors": data["risk_factors"],
        "recommendation": data["recommendation"],
        "rule_score": data["rule_score"],
        "rule_factors": data["rule_factors"],
        "final_score": data["final_score"],
        "final_level": data["final_level"]
    })

    print("\n===== FINAL RESULTS =====")

    for result in results:
        print(f"\nPR #{result['number']} - {result['title']}")
        print("Risk Score:", result["risk_score"])
        print("Risk Level:", result["risk_level"])
        print("Rule Score:", result["rule_score"])
        print("Final Score:", result["final_score"])
        print("Final Level:", result["final_level"])

        print("Rule Factors:")
        for factor in result["rule_factors"]:
            print("-", factor)

        print("Risk Factors:")
        for factor in result["risk_factors"]:
            print("-", factor)

        print("Recommendation:")
        print(result["recommendation"])

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print("\nResults saved to results.json")
