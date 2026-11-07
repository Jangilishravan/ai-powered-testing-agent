
import json
from ai_client import ask_ai


def analyze_failure(test):

    prompt = f"""
You are an expert software test failure analyst.

Analyze the following failed API test.

Test Case ID: {test["Test Case ID"]}
Scenario: {test["Scenario"]}
Expected Status: {test["Expected Status"]}
Actual Status: {test["Actual Status"]}
API Response: {test.get("Response Message", "")}

Provide:
1. Failure reason.
2. Likely root cause.
3. Recommended fix.
4. One additional test to prevent this issue.

Important:
- Base your analysis on the supplied information.
- Do not invent server logs or code details.
- If information is insufficient, clearly say so.
- Keep the explanation beginner-friendly.
"""

    try:
        return ask_ai(prompt)

    except Exception as error:
        return (
            "AI analysis unavailable: "
            + str(error)
        )


# Read execution results
with open("execution_results.json", "r") as file:
    results = json.load(file)


print("\n========== AI FAILURE ANALYSIS ==========")

for test in results:

    if test["Result"] == "FAILED":

        print("\nTest Case ID:", test["Test Case ID"])
        print("Scenario:", test["Scenario"])
        print("Expected Status:", test["Expected Status"])
        print("Actual Status:", test["Actual Status"])
        print("API Response:", test.get("Response Message", ""))

        print("\nAI ANALYSIS:")

        analysis = analyze_failure(test)

        print(analysis)

    else:

        print(
            "\n",
            test["Test Case ID"],
            "-",
            test["Scenario"],
            ": PASSED"
        )

print("\n========== ANALYSIS COMPLETED ==========")


