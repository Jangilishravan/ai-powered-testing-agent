
import json


def analyze_trends():

    with open("execution_history.json", "r") as file:
        history = json.load(file)

    if not history:
        print("No execution history available.")
        return

    print("\n========== EXECUTION TREND ANALYSIS ==========")

    for index, run in enumerate(history, start=1):

        print(f"\nRun {index}: {run['Run ID']}")
        print("Pass Rate:", run["Pass Percentage"], "%")
        print("Average Execution Time:",
              run["Average Execution Time"], "seconds")

    if len(history) >= 2:

        first_run = history[0]
        latest_run = history[-1]

        pass_change = (
            latest_run["Pass Percentage"]
            - first_run["Pass Percentage"]
        )

        time_change = (
            latest_run["Average Execution Time"]
            - first_run["Average Execution Time"]
        )

        print("\n========== OVERALL TREND ==========")

        print("Pass Rate Change:", round(pass_change, 2), "%")
        print("Execution Time Change:", round(time_change, 4), "seconds")

        if pass_change > 0:
            print("Quality Trend: Improving")
        elif pass_change < 0:
            print("Quality Trend: Declining")
        else:
            print("Quality Trend: Stable")

        if time_change < 0:
            print("Performance Trend: Faster")
        elif time_change > 0:
            print("Performance Trend: Slower")
        else:
            print("Performance Trend: Unchanged")


if __name__ == "__main__":
    analyze_trends()
