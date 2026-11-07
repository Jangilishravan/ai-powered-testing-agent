
import json
from ai_client import ask_ai


# ==========================================
# CONFIGURATION
# ==========================================

TEST_CASES_FILE = "generated_test_cases.json"
EXECUTION_FILE = "execution_results.json"
HISTORY_FILE = "execution_history.json"
SUGGESTIONS_FILE = "coverage_suggestions.json"
OUTPUT_FILE = "ai_recommendations.json"


# ==========================================
# LOAD JSON FILES
# ==========================================

def load_json(filename, default):

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        return default


# ==========================================
# NORMALIZE SCENARIO NAMES
# ==========================================

def normalize_scenario(scenario):

    return " ".join(str(scenario).lower().split())

# ==========================================
# TEST COVERAGE INTELLIGENCE
# ==========================================


def analyze_existing_coverage(test_cases):

    data_types = ["null", "numeric", "boolean", "array", "object"]

    coverage = {
        "wrong_password_with_valid_username": False,
        "null_credentials": False,
        "non_string_password": False,
        "malformed_json": False,
        "extra_fields": False,
        "username_data_types": {
            data_type: False for data_type in data_types
        },
        "password_data_types": {
            data_type: False for data_type in data_types
        }
    }

    def detect_data_type(value):

        if value is None:
            return "null"

        if isinstance(value, bool):
            return "boolean"

        if isinstance(value, (int, float)):
            return "numeric"

        if isinstance(value, list):
            return "array"

        if isinstance(value, dict):
            return "object"

        return None

    for test in test_cases:

        payload = test.get("Payload", {})

        if not isinstance(payload, dict):
            payload = {}

        username = payload.get("username")
        password = payload.get("password")

        if username == "sunny" and password == "wrong123":
            coverage["wrong_password_with_valid_username"] = True

        if "username" in payload and "password" in payload:
            if username is None or password is None:
                coverage["null_credentials"] = True

        username_type = detect_data_type(username)
        password_type = detect_data_type(password)

        if username_type in data_types:
            coverage["username_data_types"][username_type] = True

        if password_type in data_types:
            coverage["password_data_types"][password_type] = True

        if test.get("Request Mode") == "raw":
            coverage["malformed_json"] = True

        if any(key not in ["username", "password"] for key in payload):
            coverage["extra_fields"] = True

    coverage["non_string_password"] = all(
        coverage["password_data_types"].values()
    )

    coverage["unexpected_data_types"] = (
        all(coverage["username_data_types"].values())
        and all(coverage["password_data_types"].values())
    )

    return coverage

# ==========================================
# GENERATE AI RECOMMENDATIONS
# ==========================================
# ==========================================
# ==========================================
# SMART RECOMMENDATION COVERAGE CHECK
# ==========================================


def is_scenario_already_covered(scenario, coverage):

    scenario = normalize_scenario(scenario)

    # 1. Correct username + incorrect password
    wrong_password_keywords = [
        "wrong password",
        "incorrect password",
        "invalid password",
        "password mismatch"
    ]

    if (
        any(word in scenario for word in wrong_password_keywords)
        and any(word in scenario for word in ["correct username", "valid username"])
    ):
        return coverage.get("wrong_password_with_valid_username", False)

    # 2. General unexpected data types
    if "unexpected data type" in scenario or "unexpected datatypes" in scenario:
        return coverage.get("unexpected_data_types", False)

    # 3. Identify the data type being recommended
    data_type = None

    if "null" in scenario:
        data_type = "null"
    elif any(word in scenario for word in ["numeric", "number", "integer", "float"]):
        data_type = "numeric"
    elif "boolean" in scenario or "bool" in scenario:
        data_type = "boolean"
    elif "array" in scenario or "list" in scenario:
        data_type = "array"
    elif "object" in scenario or "dictionary" in scenario:
        data_type = "object"

    # 4. Field-specific data type coverage
    if data_type:

        if "username" in scenario and "password" not in scenario:
            return coverage["username_data_types"].get(data_type, False)

        if "password" in scenario and "username" not in scenario:
            return coverage["password_data_types"].get(data_type, False)

    # 5. General null credentials
    if "null" in scenario and any(
        word in scenario for word in ["credential", "username", "password"]
    ):
        return coverage.get("null_credentials", False)

    # 6. General non-string password
    if "password" in scenario and any(
        word in scenario for word in ["non-string", "non string", "data type", "datatype"]
    ):
        return coverage.get("non_string_password", False)

    # 7. Malformed JSON
    malformed_keywords = [
        "malformed json", "invalid json",
        "broken json", "incomplete json"
    ]

    if any(word in scenario for word in malformed_keywords):
        return coverage.get("malformed_json", False)

    # 8. Unexpected extra fields
    extra_field_keywords = [
        "extra field", "additional field",
        "unexpected field", "unknown field"
    ]

    if any(word in scenario for word in extra_field_keywords):
        return coverage.get("extra_fields", False)

    return False

def generate_recommendations():

    test_cases = load_json(TEST_CASES_FILE, [])
    execution_results = load_json(EXECUTION_FILE, [])
    history = load_json(HISTORY_FILE, [])
    existing_suggestions = load_json(SUGGESTIONS_FILE, [])
        # Analyze actual test coverage
    coverage_analysis = analyze_existing_coverage(test_cases)

    print("\n========== EXISTING COVERAGE ANALYSIS ==========")

    for scenario, covered in coverage_analysis.items():

        status = "COVERED" if covered else "MISSING"

        print(f"{scenario}: {status}")

    if not isinstance(test_cases, list):
        raise ValueError("Generated test cases must be a list.")

    if not isinstance(execution_results, list):
        raise ValueError("Execution results must be a list.")

    # Collect all existing scenario names
    existing_scenarios = {
        normalize_scenario(test.get("Scenario", ""))
        for test in test_cases
    }

    # Include previously suggested scenarios
    for suggestion in existing_suggestions:

        existing_scenarios.add(
            normalize_scenario(
                suggestion.get("Scenario", "")
            )
        )

    # Prepare compact execution information
    execution_summary = [
        {
            "Scenario": test.get("Scenario"),
            "Result": test.get("Result"),
            "Expected Status": test.get("Expected Status"),
            "Actual Status": test.get("Actual Status")
        }
        for test in execution_results
    ]

    # Prepare recent historical information
    historical_summary = [
        {
            "Run ID": run.get("Run ID"),
            "Total Tests": run.get("Total Tests"),
            "Passed": run.get("Passed"),
            "Failed": run.get("Failed"),
            "Pass Percentage": run.get("Pass Percentage")
        }
        for run in history[-5:]
    ]

    # Prepare AI prompt
    prompt = f"""
You are a senior software QA engineer.

Analyze this login API testing project and recommend
up to 5 additional, meaningful test scenarios.

EXISTING GENERATED TEST CASES:
{json.dumps(test_cases, indent=2)}

LATEST EXECUTION RESULTS:
{json.dumps(execution_summary, indent=2)}

RECENT EXECUTION HISTORY:
{json.dumps(historical_summary, indent=2)}

ALREADY SUGGESTED SCENARIOS:
{json.dumps(sorted(existing_scenarios), indent=2)}
ACTUAL SCENARIO COVERAGE:
{json.dumps(coverage_analysis, indent=2)}

Requirements:

1. Suggest only genuinely new test scenarios.
2. Do not repeat existing or previously suggested scenarios.
3. Consider edge cases, validation, security and robustness.
4. Prioritize scenarios based on testing importance.
5. Do not claim that suggested tests have been executed.
6. Do not invent application features or endpoints.
7. Return at most 5 recommendations.
8. Return ONLY valid JSON.

Required JSON format:

[
    {{
        "Scenario": "Example New Scenario",
        "Reason": "Explains why this test is important.",
        "Priority": "High"
    }}
]
"""

    print("\nRequesting AI test recommendations...")

    # One deliberate AI API call
    response = ask_ai(prompt).strip()

    # Remove Markdown code fences if present
    if response.startswith("```"):

        response = response.split("\n", 1)[1]
        response = response.rsplit("```", 1)[0].strip()

    recommendations = json.loads(response)

    if not isinstance(recommendations, list):
        raise ValueError("AI response must be a JSON list.")

    # Validate and remove duplicates
    filtered_recommendations = []
    seen_scenarios = set(existing_scenarios)

    for item in recommendations:

        if not isinstance(item, dict):
            continue

        scenario = str(item.get("Scenario", "")).strip()
        reason = str(item.get("Reason", "")).strip()
        priority = str(item.get("Priority", "")).strip().title()

        normalized = normalize_scenario(scenario)

        if not scenario or not reason:
            continue

        if normalized in seen_scenarios:
            print("Duplicate recommendation skipped:", scenario)
            continue

        if is_scenario_already_covered(scenario, coverage_analysis):
            print("Scenario already covered by existing tests:", scenario)
            continue

        if priority not in ["High", "Medium", "Low"]:
            priority = "Medium"

        filtered_recommendations.append({
            "Scenario": scenario,
            "Reason": reason,
            "Priority": priority
        })

        seen_scenarios.add(normalized)

        if len(filtered_recommendations) == 5:
            break

    return filtered_recommendations


# ==========================================
# MAIN EXECUTION
# ==========================================

if __name__ == "__main__":

    print("\n========== AI TEST RECOMMENDATION ENGINE ==========")

    try:

        recommendations = generate_recommendations()

        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            json.dump(recommendations, file, indent=4)

        if recommendations:

            for index, item in enumerate(recommendations, start=1):

                print(f"\nRecommendation {index}")
                print("Scenario:", item["Scenario"])
                print("Reason:", item["Reason"])
                print("Priority:", item["Priority"])

        else:

            print("\nNo additional recommendations found.")

        print("\nRecommendations saved successfully!")
        print("Output file:", OUTPUT_FILE)

    except json.JSONDecodeError as error:

        print("\nAI returned invalid JSON:", error)

    except Exception as error:

        print("\nRecommendation generation failed:", error)
