
import json
from collections import defaultdict


HISTORY_FILE = "execution_history.json"
OUTPUT_FILE = "historical_analysis.json"


def analyze_historical_tests():

    # Load execution history
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            history = json.load(file)

    except FileNotFoundError:
        print("Execution history file not found.")
        return

    except json.JSONDecodeError:
        print("Execution history contains invalid JSON.")
        return

    if not isinstance(history, list) or not history:
        print("No valid execution history available.")
        return

    # Group test executions by Test Case ID
    test_history = defaultdict(list)

    for run in history:

        run_id = run.get("Run ID", "Unknown")

        results = run.get("Test Results", [])

        if not isinstance(results, list):
            continue

        for test in results:

            if not isinstance(test, dict):
                continue

            test_id = test.get("Test Case ID")

            if not test_id:
                continue

            test_history[test_id].append({
                "Run ID": run_id,
                "Scenario": test.get("Scenario", "Unknown"),
                "Result": str(test.get("Result", "UNKNOWN")).upper(),
                "Execution Time": test.get("Execution Time", 0)
            })

    analyzed_tests = []

    flaky_tests = []
    repeated_failures = []

    # Analyze individual tests
    for test_id, observations in test_history.items():

        statuses = [
            item["Result"]
            for item in observations
        ]

        passed = statuses.count("PASSED")
        failed = statuses.count("FAILED")

        total_observations = len(observations)

        pass_rate = round(
            (passed / total_observations) * 100,
            2
        )

        # A flaky test has both passed and failed
        # in different recorded executions.
        is_flaky = passed > 0 and failed > 0

        # Repeated failures means at least two
        # recorded failures across different executions.
        is_repeated_failure = failed >= 2

        # Check the latest two observed executions
        consecutive_failures = (
            total_observations >= 2
            and statuses[-1] == "FAILED"
            and statuses[-2] == "FAILED"
        )

        report = {
            "Test Case ID": test_id,
            "Scenario": observations[-1]["Scenario"],
            "Runs Observed": total_observations,
            "Passed": passed,
            "Failed": failed,
            "Pass Rate": pass_rate,
            "Latest Result": statuses[-1],
            "Outcome History": statuses,
            "Flaky": is_flaky,
            "Repeated Failure": is_repeated_failure,
            "Consecutive Failures": consecutive_failures
        }

        analyzed_tests.append(report)

        if is_flaky:
            flaky_tests.append(report)

        if is_repeated_failure:
            repeated_failures.append(report)

    # Overall analysis
    total_tests = len(analyzed_tests)

    total_observations = sum(
        test["Runs Observed"]
        for test in analyzed_tests
    )

    analysis = {
        "Total Historical Runs": len(history),
        "Unique Test Cases": total_tests,
        "Total Test Observations": total_observations,
        "Flaky Test Count": len(flaky_tests),
        "Repeated Failure Count": len(repeated_failures),
        "Flaky Tests": flaky_tests,
        "Repeated Failures": repeated_failures,
        "Test Analysis": analyzed_tests
    }

    # Save analysis
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(analysis, file, indent=4)

    # Display results
    print("\n========== HISTORICAL TEST ANALYSIS ==========")

    print("Historical Runs:", len(history))
    print("Unique Test Cases:", total_tests)
    print("Total Test Observations:", total_observations)

    print("\n========== FLAKY TESTS ==========")

    if flaky_tests:

        for test in flaky_tests:
            print(
                test["Test Case ID"],
                "-",
                test["Scenario"],
                "| Outcomes:",
                test["Outcome History"]
            )

    else:
        print("No flaky tests detected.")

    print("\n========== REPEATED FAILURES ==========")

    if repeated_failures:

        for test in repeated_failures:
            print(
                test["Test Case ID"],
                "-",
                test["Scenario"],
                "| Failures:",
                test["Failed"]
            )

    else:
        print("No repeated failures detected.")

    print("\nAnalysis saved to:", OUTPUT_FILE)
    print("\nHistorical analysis completed!")


if __name__ == "__main__":
    analyze_historical_tests()
