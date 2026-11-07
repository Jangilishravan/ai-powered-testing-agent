
import json
from datetime import datetime


# File names
TEST_CASES_FILE = "generated_test_cases.json"
EXECUTION_FILE = "execution_results.json"
HISTORY_FILE = "execution_history.json"
SUGGESTIONS_FILE = "coverage_suggestions.json"
GROUPS_FILE = "coverage_groups.json"
REPORT_FILE = "gap_analysis_report.json"


def load_json(filename, default):

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        return default


def save_json(filename, data):

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def analyze_coverage():

    # 1. Load project data
    test_cases = load_json(TEST_CASES_FILE, [])
    execution_results = load_json(EXECUTION_FILE, [])
    execution_history = load_json(HISTORY_FILE, [])
    suggestions = load_json(SUGGESTIONS_FILE, [])
    coverage_groups = load_json(GROUPS_FILE, {})

    if not isinstance(test_cases, list):
        raise ValueError("Generated test cases must be a JSON list.")

    if not isinstance(execution_results, list):
        raise ValueError("Execution results must be a JSON list.")

    if not isinstance(suggestions, list):
        raise ValueError("Coverage suggestions must be a JSON list.")

    # 2. Build generated test case lookup
    generated_tests = {
        test.get("Test Case ID"): test
        for test in test_cases
        if test.get("Test Case ID")
    }

    # 3. Build execution lookup using test case IDs
    executed_tests = {
        test.get("Test Case ID"): test
        for test in execution_results
        if test.get("Test Case ID")
    }

    generated_ids = set(generated_tests.keys())
    executed_ids = set(executed_tests.keys())

    # 4. Identify tests not executed
    unexecuted_tests = []

    for test_id in sorted(
        generated_ids - executed_ids
    ):

        test = generated_tests[test_id]

        unexecuted_tests.append({
            "Test Case ID": test_id,
            "Scenario": test.get("Scenario", "Unknown"),
            "Status": "NOT EXECUTED"
        })

    # 5. Identify failed tests
    failed_tests = []

    for test_id, result in executed_tests.items():

        if test_id not in generated_ids:
            continue

        if result.get("Result", "").upper() == "FAILED":

            failed_tests.append({
                "Test Case ID": test_id,
                "Scenario": result.get("Scenario", "Unknown"),
                "Expected Status": result.get("Expected Status"),
                "Actual Status": result.get("Actual Status"),
                "Response Message": result.get(
                    "Response Message", ""
                ),
                "Result": "FAILED"
            })

    # 6. Identify missing test-design scenarios
    existing_scenarios = {
        test.get("Scenario", "").strip()
        for test in test_cases
    }

    missing_tests = []

    for suggestion in suggestions:

        scenario = suggestion.get("Scenario", "").strip()

        if not scenario:
            continue

        # Check whether this suggestion represents a group
        if scenario in coverage_groups:

            required_scenarios = set(
                coverage_groups[scenario]
            )

            missing_scenarios = (
                required_scenarios - existing_scenarios
            )

            for missing in sorted(missing_scenarios):

                missing_tests.append({
                    "Scenario": missing,
                    "Parent Category": scenario,
                    "Reason": suggestion.get("Reason", ""),
                    "Priority": suggestion.get(
                        "Priority", "Medium"
                    )
                })

        elif scenario not in existing_scenarios:

            missing_tests.append({
                "Scenario": scenario,
                "Parent Category": None,
                "Reason": suggestion.get("Reason", ""),
                "Priority": suggestion.get(
                    "Priority", "Medium"
                )
            })

    # 7. Calculate execution statistics
    total_generated = len(generated_ids)

    total_executed = len(
        generated_ids.intersection(executed_ids)
    )

    total_unexecuted = len(unexecuted_tests)
    total_failed = len(failed_tests)

    total_passed = sum(
        1
        for test_id in generated_ids.intersection(executed_ids)
        if executed_tests[test_id].get("Result", "").upper()
        == "PASSED"
    )

    execution_coverage = (
        total_executed / total_generated * 100
        if total_generated else 0
    )

    pass_percentage = (
        total_passed / total_executed * 100
        if total_executed else 0
    )

    # 8. Historical execution summary
    historical_runs = []

    for run in execution_history:

        historical_runs.append({
            "Run ID": run.get("Run ID"),
            "Execution Date": run.get("Execution Date"),
            "Total Tests": run.get("Total Tests", 0),
            "Passed": run.get("Passed", 0),
            "Failed": run.get("Failed", 0),
            "Pass Percentage": run.get(
                "Pass Percentage", 0
            )
        })

    # 9. Build final gap analysis report
    report = {

        "Analysis Date": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "Summary": {
            "Total Generated Tests": total_generated,
            "Total Executed Tests": total_executed,
            "Total Passed Tests": total_passed,
            "Total Failed Tests": total_failed,
            "Total Unexecuted Tests": total_unexecuted,
            "Total Missing Scenarios": len(missing_tests),
            "Execution Coverage Percentage": round(
                execution_coverage, 2
            ),
            "Pass Percentage": round(
                pass_percentage, 2
            )
        },

        "Missing Tests": missing_tests,

        "Unexecuted Tests": unexecuted_tests,

        "Failed Tests": failed_tests,

        "Historical Execution Summary": historical_runs
    }

    # 10. Save report
    save_json(REPORT_FILE, report)

    return report


if __name__ == "__main__":

    print("\n========== AI TEST GAP DETECTION ==========")

    try:

        report = analyze_coverage()

        summary = report["Summary"]

        print("\n========== COVERAGE SUMMARY ==========")

        for key, value in summary.items():
            print(f"{key}: {value}")

        print("\n========== MISSING TEST SCENARIOS ==========")

        if report["Missing Tests"]:

            for test in report["Missing Tests"]:
                print(
                    f"\nScenario: {test['Scenario']}"
                    f"\nPriority: {test['Priority']}"
                    f"\nReason: {test['Reason']}"
                )

        else:
            print("No missing scenarios detected.")

        print("\n========== UNEXECUTED TESTS ==========")

        if report["Unexecuted Tests"]:

            for test in report["Unexecuted Tests"]:
                print(
                    test["Test Case ID"],
                    "-",
                    test["Scenario"]
                )

        else:
            print("All generated tests have been executed.")

        print("\n========== FAILED TESTS ==========")

        if report["Failed Tests"]:

            for test in report["Failed Tests"]:
                print(
                    test["Test Case ID"],
                    "-",
                    test["Scenario"],
                    "-",
                    test["Response Message"]
                )

        else:
            print("No failed tests detected.")

        print(
            f"\nGap analysis report saved successfully: "
            f"{REPORT_FILE}"
        )

    except Exception as error:

        print("\nCoverage analysis failed:", error)
