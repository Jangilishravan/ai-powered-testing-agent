
import json
import statistics
from datetime import datetime


HISTORY_FILE = "execution_history.json"
WEAK_FILE = "weak_area_analysis.json"
OUTPUT_FILE = "improvement_tracking.json"

MIN_OBSERVATIONS = 5


def load_json(filename, default):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return default


def track_improvements():

    history = load_json(HISTORY_FILE, [])
    weak_report = load_json(WEAK_FILE, {})

    weak_areas = weak_report.get("Weak Areas", [])

    tracking_results = []

    print("\n========== WEAK AREA IMPROVEMENT TRACKER ==========")

    for weak_test in weak_areas:

        test_id = weak_test.get("Test Case ID")
        scenario = weak_test.get("Scenario")

        observations = []

        for run in history:
            for test in run.get("Test Results", []):

                if test.get("Test Case ID") == test_id:
                    observations.append({
                        "Run ID": run.get("Run ID"),
                        "Execution Date": test.get("Execution Date"),
                        "Execution Time": test.get("Execution Time"),
                        "Result": test.get("Result")
                    })

        if not observations:
            continue

        latest = observations[-1]
        previous = observations[:-1]

        previous_times = [
            item["Execution Time"]
            for item in previous
            if isinstance(item.get("Execution Time"), (int, float))
        ]

        latest_time = latest["Execution Time"]

        if len(previous_times) < MIN_OBSERVATIONS:

            status = "INSUFFICIENT DATA"
            previous_median = None
            change_percentage = None

        else:

            previous_median = statistics.median(previous_times)

            if previous_median == 0:
                change_percentage = None
                status = "INCONCLUSIVE"

            else:
                change_percentage = round(
                    ((latest_time - previous_median) / previous_median) * 100,
                    2
                )

                status = "FASTER" if change_percentage < 0 else (
                    "SLOWER" if change_percentage > 0 else "UNCHANGED"
                )

        record = {
            "Test Case ID": test_id,
            "Scenario": scenario,
            "Previous Observations": len(previous_times),
            "Previous Median": previous_median,
            "Latest Execution Time": latest_time,
            "Change Percentage": change_percentage,
            "Performance Status": status,
            "Latest Result": latest["Result"],
            "Analysis Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        tracking_results.append(record)

        print(f"\n{test_id} - {scenario}")
        print(f"Previous Median: {previous_median}")
        print(f"Latest Time: {latest_time}")
        print(f"Status: {status}")

    output = {
        "Total Tests Tracked": len(tracking_results),
        "Minimum Required Observations": MIN_OBSERVATIONS,
        "Tracking Results": tracking_results
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=4)

    print("\nImprovement tracking completed!")
    print(f"Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    track_improvements()
