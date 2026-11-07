
import json
import requests
import time
from datetime import datetime

# Load original AI-generated test cases
with open("generated_test_cases.json", "r") as file:
    test_cases = json.load(file)

# Additional executable scenarios from AI coverage analysis




# Add all predefined scenarios before AI suggestions

existing_scenarios = {
    case["Scenario"] for case in test_cases
}

# Load AI coverage suggestions

try:
    with open("coverage_suggestions.json", "r") as file:
        suggestions = json.load(file)

    existing_scenarios = {
        case.get("Scenario")
        for case in test_cases
    }

    # Load coverage groups from JSON configuration

    try:
        with open("coverage_groups.json", "r") as file:
            coverage_groups = json.load(file)

    except FileNotFoundError:
        print("Coverage groups configuration not found.")
        coverage_groups = {}

    for suggestion in suggestions:

        scenario = suggestion.get("Scenario")

        if not scenario:
            continue

        # Check grouped coverage
        if scenario in coverage_groups:

            required_scenarios = coverage_groups[scenario]

            missing_scenarios = (
        set(required_scenarios) - existing_scenarios
    )

            if not missing_scenarios:

                print(
                    "AI suggestion fully covered:",
                    scenario
                )

            else:

                print(
                    "AI suggestion partially covered:",
                    scenario
                )

                print(
                    "Missing boundary tests:",
                    sorted(missing_scenarios)
                )

        # Check ordinary scenario coverage
        elif scenario in existing_scenarios:

            print(
                "AI suggestion already covered:",
                scenario
            )

        else:

            print(
                "New AI suggestion requires a test payload:",
                scenario
            )

except FileNotFoundError:

    print("Coverage suggestions file not found.")





passed = 0
failed = 0
execution_results = []

print("\n========== AI BATCH TEST EXECUTION ==========")

for test_case in test_cases:

    scenario = test_case["Scenario"]
    expected_status = test_case["Expected Status Code"]

    # Read request configuration
    payload = test_case.get("Payload", {})
    request_mode = test_case.get("Request Mode", "json")

    start_time = time.time()
    response_message = ""

    try:

        # Support raw request data (malformed JSON)
        if request_mode == "raw":

            raw_body = test_case.get("Raw Body")

            if not isinstance(raw_body, str):
                print("\nInvalid raw request body:", scenario)
                continue

            response = requests.post(
                "http://127.0.0.1:5000/login",
                data=raw_body,
                headers={
                    "Content-Type": "application/json"
                },
                timeout=5
            )

        # Support normal JSON requests
        elif request_mode == "json":

            if not isinstance(payload, dict):
                print("\nInvalid JSON payload:", scenario)
                continue

            # Additional JSON fields are allowed
            response = requests.post(
                "http://127.0.0.1:5000/login",
                json=payload,
                timeout=5
            )

        else:

            print("\nUnsupported request mode:", request_mode)
            continue


        actual_status = response.status_code
        execution_time = round(time.time() - start_time, 4)

        try:
            response_data = response.json()

            if isinstance(response_data, dict):
                response_message = (
                    response_data.get("message")
                    or response_data.get("error")
                    or response_data.get("detail")
                    or json.dumps(response_data)
                )
            else:
                response_message = str(response_data)

        except ValueError:
            response_message = response.text or "No response body returned."

        if actual_status == expected_status:
            status = "PASSED"
            passed += 1
        else:
            status = "FAILED"
            failed += 1

    except requests.RequestException as error:
        actual_status = None
        execution_time = round(time.time() - start_time, 4)
        response_message = str(error)
        status = "FAILED"
        failed += 1

        print("Execution Error:", error)

    print(f"\nScenario: {scenario}")
    print("Expected:", expected_status)
    print("Actual:", actual_status)
    print("Response Message:", response_message)
    print("Execution Time:", execution_time, "seconds")
    print("Result:", status)

    execution_results.append({
        "Test Case ID": test_case["Test Case ID"],
        "Scenario": scenario,
        "Expected Status": expected_status,
        "Actual Status": actual_status,
        "Response Message": response_message,
        "Execution Time": execution_time,
        "Result": status,
        "Execution Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# Save execution results
with open("execution_results.json", "w") as file:
    json.dump(execution_results, file, indent=4)

# Add all predefined coverage scenarios

# Save execution history

total_tests = len(execution_results)

pass_percentage = (
    (passed / total_tests) * 100
    if total_tests > 0 else 0
)

average_execution_time = (
    sum(test["Execution Time"] for test in execution_results) / total_tests
    if total_tests > 0 else 0
)

run_summary = {
    "Run ID": datetime.now().strftime("%Y%m%d_%H%M%S"),
    "Execution Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "Total Tests": total_tests,
    "Passed": passed,
    "Failed": failed,
    "Pass Percentage": round(pass_percentage, 2),
    "Average Execution Time": round(average_execution_time, 4),
    "Test Results": execution_results
}

try:
    with open("execution_history.json", "r") as file:
        history = json.load(file)

except FileNotFoundError:
    history = []

history.append(run_summary)

with open("execution_history.json", "w") as file:
    json.dump(history, file, indent=4)

print("\nExecution history saved successfully!")
print("Total recorded runs:", len(history))

print("\n========== FINAL TEST SUMMARY ==========")
print("Total Executed:", len(execution_results))
print("Passed:", passed)
print("Failed:", failed)

print("\nResults saved to execution_results.json")

# Generate HTML report automatically
import generate_html_report

# Run AI failure analysis automatically
import failure_analyzer




