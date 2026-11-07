
import json
import statistics


HISTORY_FILE = "execution_history.json"
OUTPUT_FILE = "performance_analysis.json"

MIN_OBSERVATIONS = 5
MAD_THRESHOLD = 3.5

# Used when MAD is zero: flag only clearly larger execution times.
ZERO_MAD_MULTIPLIER = 2.5
ZERO_MAD_MIN_DIFFERENCE = 0.02


def load_history():

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            history = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        print("Unable to load execution history.")
        return None

    if not isinstance(history, list):
        print("Execution history must be a list.")
        return None

    return history


def analyze_performance():

    history = load_history()

    if not history:
        print("No execution history available.")
        return

    test_times = {}

    # Collect timing along with its original run information.
    for run in history:

        run_id = run.get("Run ID", "Unknown")
        run_date = run.get("Execution Date", "Unknown")

        for test in run.get("Test Results", []):

            test_id = test.get("Test Case ID")
            execution_time = test.get("Execution Time")

            if (
                not test_id
                or isinstance(execution_time, bool)
                or not isinstance(execution_time, (int, float))
                or execution_time < 0
            ):
                continue

            test_times.setdefault(test_id, []).append({
                "Run ID": run_id,
                "Execution Date": run_date,
                "Execution Time": execution_time
            })

    performance_results = []
    insufficient_data = []

    for test_id, observations in test_times.items():

        if len(observations) < MIN_OBSERVATIONS:
            insufficient_data.append(test_id)
            continue

        times = [
            item["Execution Time"]
            for item in observations
        ]

        median_time = statistics.median(times)

        deviations = [
            abs(value - median_time)
            for value in times
        ]

        mad = statistics.median(deviations)

        spike_details = []

        for item in observations:

            value = item["Execution Time"]

            if mad == 0:

                # Avoid flagging every value above the median.
                threshold = max(
                    median_time * ZERO_MAD_MULTIPLIER,
                    median_time + ZERO_MAD_MIN_DIFFERENCE
                )

                is_spike = value > threshold

            else:

                score = (
                    0.6745 * (value - median_time) / mad
                )

                is_spike = score > MAD_THRESHOLD

            if is_spike:

                spike_details.append({
                    "Run ID": item["Run ID"],
                    "Execution Date": item["Execution Date"],
                    "Execution Time": round(value, 4)
                })

        average_time = statistics.mean(times)

        result = {
            "Test Case ID": test_id,
            "Observations": len(times),
            "Average Execution Time": round(average_time, 4),
            "Median Execution Time": round(median_time, 4),
            "Maximum Execution Time": round(max(times), 4),
            "Unusual Slow Execution Count": len(spike_details),
            "Slow Executions": spike_details,
            "Potential Performance Concern": len(spike_details) > 0
        }

        performance_results.append(result)

    performance_results.sort(
        key=lambda item: item["Unusual Slow Execution Count"],
        reverse=True
    )

    analysis = {
        "Minimum Required Observations": MIN_OBSERVATIONS,
        "MAD Threshold": MAD_THRESHOLD,
        "Zero MAD Multiplier": ZERO_MAD_MULTIPLIER,
        "Tests Analyzed": len(performance_results),
        "Tests With Insufficient Data": len(insufficient_data),
        "Insufficient Data Test IDs": insufficient_data,
        "Potential Performance Concerns": sum(
            1 for item in performance_results
            if item["Potential Performance Concern"]
        ),
        "Performance Results": performance_results
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(analysis, file, indent=4)

    print("\n========== PERFORMANCE ANALYSIS ==========")

    print("Tests Analyzed:", len(performance_results))
    print("Tests With Insufficient Data:", len(insufficient_data))
    print(
        "Potential Performance Concerns:",
        analysis["Potential Performance Concerns"]
    )

    print("\n========== TEST PERFORMANCE DETAILS ==========")

    for item in performance_results:

        print("\nTest:", item["Test Case ID"])
        print("Observations:", item["Observations"])
        print("Median Time:", item["Median Execution Time"], "seconds")
        print("Average Time:", item["Average Execution Time"], "seconds")
        print(
            "Unusual Slow Executions:",
            item["Unusual Slow Execution Count"]
        )

        for spike in item["Slow Executions"]:
            print(
                "  Run:", spike["Run ID"],
                "| Time:", spike["Execution Time"],
                "seconds"
            )

        if item["Potential Performance Concern"]:
            print("Status: Potential performance concern")
        else:
            print("Status: No unusual spikes detected")

    print("\nAnalysis saved to:", OUTPUT_FILE)
    print("Performance analysis completed!")


if __name__ == "__main__":
    analyze_performance()

