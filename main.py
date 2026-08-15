from analyzer import get_pull_request, analyze_pr
import json

owner = "adagentpc-del"
repo = "divini-procure"
pr_number = 18

print(f"Analyzing PR #{pr_number}...")

pr = get_pull_request(owner, repo, pr_number)

result = analyze_pr(pr)

data = json.loads(result)

print("\n===== PR RISK ANALYSIS =====")
print("PR:", pr_number)
print("Risk Score:", data["risk_score"])
print("Risk Level:", data["risk_level"])

print("\nRisk Factors:")
for factor in data["risk_factors"]:
    print("-", factor)

print("\nRecommendation:")
print(data["recommendation"])