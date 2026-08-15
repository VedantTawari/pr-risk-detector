import streamlit as st
import json
from analyzer import (
    get_pull_request,
    get_open_prs,
    analyze_pr,
    calculate_rule_score
)

st.set_page_config(
    page_title="PR Risk Detector",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ PR Risk Detector")
st.caption("AI-powered Pull Request security and risk analysis")


try:
    with open("results.json", "r", encoding="utf-8") as f:
        results = json.load(f)
except FileNotFoundError:
    results = []


st.subheader("Dashboard")


total_prs = len(results)

high_count = sum(
    1 for r in results
    if r["final_level"] == "HIGH"
)

medium_count = sum(
    1 for r in results
    if r["final_level"] == "MEDIUM"
)

low_count = sum(
    1 for r in results
    if r["final_level"] == "LOW"
)

avg_score = round(
    sum(r["final_score"] for r in results) / total_prs
) if total_prs else 0

highest_risk_pr = max(
    results,
    key=lambda r: r["final_score"]
) if results else None

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric("Total PRs", total_prs)

with col2:
    st.metric("🔴 High Risk", high_count)

with col3:
    st.metric("🟠 Medium Risk", medium_count)

with col4:
    st.metric("🟢 Low Risk", low_count)

with col5:
    st.metric("Average Score", avg_score)

with col6:
    if highest_risk_pr:
        st.metric(
            "Highest Risk",
            f"PR #{highest_risk_pr['number']}",
            f"{highest_risk_pr['final_score']}/100"
        )
    else:
        st.metric("Highest Risk", "N/A")


st.divider()


st.subheader("Risk Overview")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:

    risk_data = {
        "HIGH": high_count,
        "MEDIUM": medium_count,
        "LOW": low_count
    }

    st.bar_chart(risk_data)


with chart_col2:

    score_data = {
        f"{r['owner']}/{r['repo']} — PR #{r['number']}": r["final_score"]
        for r in results
    }

    if score_data:
        st.bar_chart(score_data)
    else:
        st.info("No PR analysis available yet.")


st.divider()


st.subheader("Analyze a Pull Request")

col1, col2 = st.columns(2)

with col1:
    owner = st.text_input(
        "GitHub Owner",
        value="adagentpc-del"
    )

with col2:
    repo = st.text_input(
        "Repository",
        value="divini-procure"
    )

st.subheader("Select a Pull Request")

try:
    open_prs = get_open_prs(
        owner.strip(),
        repo.strip()
    )
except Exception:
    open_prs = []

if not open_prs:
    st.info("No open Pull Requests found for this repository.")
    st.stop()

pr_options = {
    f"PR #{pr['number']} — {pr['title']}": pr["number"]
    for pr in open_prs
}

selected_pr = st.selectbox(
    "Choose a Pull Request",
    list(pr_options.keys())
)

pr_number = pr_options[selected_pr]


if st.button("🔍 Analyze PR"):

    with st.spinner("Fetching and analyzing Pull Request..."):

        try:


            pr = get_pull_request(
                owner.strip(),
                repo.strip(),
                int(pr_number)
            )

            if pr is None:
                st.error("❌ Pull Request not found")
                st.info(
                    "Please check the GitHub Owner, Repository name, "
                    "and Pull Request number."
                )
                st.stop()


            result = analyze_pr(pr)

            if not result:
                st.error("AI analysis failed. Please try again.")
                st.stop()

            try:
                data = json.loads(result)
            except json.JSONDecodeError:
                st.error("AI returned an invalid response. Please try again.")
                st.stop()


            rule_score, rule_factors = calculate_rule_score(pr)


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


            new_result = {
                "owner": owner.strip(),
                "repo": repo.strip(),
                "number": int(pr_number),
                "title": pr["title"],
                "author": pr["author"],
                "state": pr["state"],
                "changed_files": pr["changed_files"],
                "additions": pr["additions"],
                "deletions": pr["deletions"],
                "risk_score": data["risk_score"],
                "risk_level": data["risk_level"],
                "risk_factors": data["risk_factors"],
                "recommendation": data["recommendation"],
                "rule_score": rule_score,
                "rule_factors": rule_factors,
                "final_score": final_score,
                "final_level": final_level
            }


            existing_index = None

            for i, r in enumerate(results):
                if (
                    r["owner"] == owner.strip()
                    and r["repo"] == repo.strip()
                    and r["number"] == int(pr_number)
                ):
                    existing_index = i
                    break

            if existing_index is not None:
                results[existing_index] = new_result
            else:
                results.append(new_result)


            try:
                with open("results.json", "r", encoding="utf-8") as f:
                    existing_results = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                existing_results = []

            existing_results = [
                r for r in existing_results
                if not (
                    r.get("owner") == new_result["owner"]
                    and r.get("repo") == new_result["repo"]
                    and r["number"] == new_result["number"]
                )
            ]

            existing_results.append(new_result)

            with open("results.json", "w", encoding="utf-8") as f:
                json.dump(existing_results, f, indent=4)

            st.success("Analysis Complete!")
            st.rerun()


            st.success("Analysis Complete!")


            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "AI Risk Score",
                    data["risk_score"]
                )

            with col2:
                st.metric(
                    "Rule Score",
                    rule_score
                )

            with col3:
                st.metric(
                    "Final Risk Score",
                    final_score
                )


            if final_level == "HIGH":
                st.error(f"🔴 Final Risk Level: {final_level}")

            elif final_level == "MEDIUM":
                st.warning(f"🟠 Final Risk Level: {final_level}")

            else:
                st.success(f"🟢 Final Risk Level: {final_level}")


            st.subheader("🔍 Risk Factors")

            for factor in data["risk_factors"]:
                st.write("•", factor)


            st.subheader("📋 Rule Factors")

            for factor in rule_factors:
                st.write("•", factor)


            st.subheader("💡 Recommendation")

            st.info(data["recommendation"])


        except json.JSONDecodeError:

            st.error(
                "Gemini returned an invalid response. Please try again."
            )

        except Exception as e:

            st.error(
                f"Analysis failed: {e}"
            )


st.divider()


st.subheader("Pull Requests")


search = st.text_input(
    "🔎 Search Pull Requests",
    placeholder="Search by PR number or title..."
)


filter_option = st.selectbox(
    "Filter by Risk Level",
    ["All", "HIGH", "MEDIUM", "LOW"]
)


filtered_results = results


if search:

    search = search.lower().strip()

    filtered_results = [
        r for r in filtered_results
        if search in str(r["number"]).lower()
        or search in r["title"].lower()
    ]


if filter_option != "All":

    filtered_results = [
        r for r in filtered_results
        if r["final_level"] == filter_option
    ]


st.write(
    f"Showing **{len(filtered_results)}** of **{len(results)}** PRs"
)


if not filtered_results:

    st.info("No PRs match your search/filter.")


for result in filtered_results:

    level = result["final_level"]

    if level == "HIGH":
        icon = "🔴"
    elif level == "MEDIUM":
        icon = "🟠"
    else:
        icon = "🟢"


    with st.expander(
        f"{icon} PR #{result['number']} — "
        f"{result['title']} — "
        f"Score: {result['final_score']}"
    ):
        pr_url = (
            f"https://github.com/{result['owner']}/"
            f"{result['repo']}/pull/{result['number']}"
        )

        st.link_button(
            "🔗 View on GitHub",
            pr_url
        )
        st.subheader("📄 Pull Request Details")

        detail_col1, detail_col2, detail_col3, detail_col4 = st.columns(4)

        with detail_col1:
            st.write("**Author**")
            st.write(result.get("author", "Unknown"))

        with detail_col2:
            st.write("**State**")
            st.write(result.get("state", "Unknown"))

        with detail_col3:
            st.write("**Files Changed**")
            st.write(result.get("changed_files", 0))

        with detail_col4:
            st.write("**Changes**")
            st.write(
                f"+{result.get('additions', 0)} / "
                f"-{result.get('deletions', 0)}"
            )

        st.write(
            f"🔗 [View PR #{result['number']} on GitHub]("
            f"https://github.com/{result['owner']}/{result['repo']}/pull/{result['number']}"
            f")"
        )

        st.divider()
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Final Score",
                result["final_score"]
            )

        with col2:
            st.metric(
                "AI Risk Score",
                result["risk_score"]
            )

        with col3:
            st.metric(
                "Rule Score",
                result["rule_score"]
            )

        with col4:
            st.metric(
                "Risk Level",
                f"{icon} {level}"
            )


        st.progress(
            result["final_score"] / 100,
            text=f"Risk Score: {result['final_score']}/100"
        )


        st.divider()


        st.subheader("🔍 Risk Factors")

        for factor in result["risk_factors"]:
            st.write("•", factor)


        st.subheader("📋 Rule Factors")

        for factor in result["rule_factors"]:
            st.write("•", factor)


        st.subheader("💡 Recommendation")

        st.info(result["recommendation"])