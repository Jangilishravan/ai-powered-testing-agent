
import json


HISTORICAL_FILE = "historical_analysis.json"
PERFORMANCE_FILE = "performance_analysis.json"
OUTPUT_FILE = "weak_area_analysis.json"


def load_json(filename):

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None

    except json.JSONDecodeError:
        print(f"Invalid JSON in: {filename}")
        return None


def detect_weak_areas():

    historical = load_json(HISTORICAL_FILE)
    performance = load_json(PERFORMANCE_FILE)

    if historical is None or performance is None:
        return

    historical_tests = historical.get("Test Analysis", [])
    performance_tests = performance.get("Performance Results", [])

    performance_lookup = {
        item["Test Case ID"]: item
        for item in performance_tests
    }

    weak_areas = []

    for test in historical_tests:

        test_id = test.get("Test Case ID")

        if not test_id:
            continue

        issues = []

        flaky = test.get("Flaky", False)
        repeated_failure = test.get("Repeated Failure", False)
        consecutive_failures = test.get("Consecutive Failures", False)

        performance_data = performance_lookup.get(test_id, {})

        performance_concern = performance_data.get(
            "Potential Performance Concern", False
        )

        # Reliability checks
        if consecutive_failures:
            issues.append("Consecutive failures")

        if repeated_failure:
            issues.append("Repeated failures")

        if flaky:
            issues.append("Flaky test behavior")

        # Performance check
        if performance_concern:
            issues.append("Unusual execution time spikes")

        if not issues:
            continue

        # Assign priority based on issue severity
        if consecutive_failures or repeated_failure:
            priority = "HIGH"

        elif flaky:
            priority = "MEDIUM"

        else:
            priority = "LOW"

        weak_areas.append({
            "Test Case ID": test_id,
            "Scenario": test.get("Scenario", "Unknown"),
            "Priority": priority,
            "Issues Detected": issues,
            "Pass Rate": test.get("Pass Rate", 0),
            "Runs Observed": test.get("Runs Observed", 0),
            "Latest Result": test.get("Latest Result", "Unknown"),
            "Median Execution Time": performance_data.get(
                "Median Execution Time"
            ),
            "Unusual Slow Execution Count": performance_data.get(
                "Unusual Slow Execution Count", 0
            ),
            "Slow Executions": performance_data.get(
                "Slow Executions", []
            )
        })

    priority_order = {
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3
    }

    weak_areas.sort(
        key=lambda item: (
            priority_order[item["Priority"]],
            -len(item["Issues Detected"])
        )
    )

    summary = {
        "Total Historical Runs": historical.get(
            "Total Historical Runs", 0
        ),
        "Total Tests Analyzed": len(historical_tests),
        "Total Weak Tests": len(weak_areas),
        "High Priority": sum(
            1 for item in weak_areas
            if item["Priority"] == "HIGH"
        ),
        "Medium Priority": sum(
            1 for item in weak_areas
            if item["Priority"] == "MEDIUM"
        ),
        "Low Priority": sum(
            1 for item in weak_areas
            if item["Priority"] == "LOW"
        ),
        "Flaky Tests": historical.get("Flaky Test Count", 0),
        "Repeated Failures": historical.get(
            "Repeated Failure Count", 0
        ),
        "Performance Concerns": performance.get(
            "Potential Performance Concerns", 0
        ),
        "Weak Areas": weak_areas
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4)

    print("\n========== WEAK AREA DETECTION ==========")

    print("Historical Runs:", summary["Total Historical Runs"])
    print("Tests Analyzed:", summary["Total Tests Analyzed"])
    print("Total Weak Tests:", summary["Total Weak Tests"])

    print("\n========== PRIORITY SUMMARY ==========")

    print("High Priority:", summary["High Priority"])
    print("Medium Priority:", summary["Medium Priority"])
    print("Low Priority:", summary["Low Priority"])

    print("\n========== DETECTED WEAK AREAS ==========")

    if not weak_areas:
        print("No weak areas detected.")

    for item in weak_areas:

        print("\nTest ID:", item["Test Case ID"])
        print("Scenario:", item["Scenario"])
        print("Priority:", item["Priority"])
        print("Issues:", ", ".join(item["Issues Detected"]))

        if item["Median Execution Time"] is not None:
            print(
                "Median Execution Time:",
                item["Median Execution Time"],
                "seconds"
            )

        print(
            "Unusual Slow Executions:",
            item["Unusual Slow Execution Count"]
        )

    print("\nAnalysis saved to:", OUTPUT_FILE)
    print("Weak area detection completed!")


if __name__ == "__main__":
    detect_weak_areas()
