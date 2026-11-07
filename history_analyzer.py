
import json


def analyze_history():

    try:
        with open("execution_history.json", "r") as file:
            history = json.load(file)

    except FileNotFoundError:
        print("Execution history file not found.")
        return

    if not history:
        print("No execution history available.")
        return

    print("\n========== EXECUTION HISTORY ANALYSIS ==========")

    print("Total Execution Runs:", len(history))

    for run in history:

        print("\nRun ID:", run["Run ID"])
        print("Execution Date:", run["Execution Date"])
        print("Total Tests:", run["Total Tests"])
        print("Passed:", run["Passed"])
        print("Failed:", run["Failed"])
        print("Pass Percentage:", run["Pass Percentage"], "%")
        print("Average Execution Time:",
              run["Average Execution Time"], "seconds")

    # Compare latest run with previous run
    if len(history) >= 2:

        previous = history[-2]
        latest = history[-1]

        print("\n========== RUN COMPARISON ==========")

        print(
            "Previous Pass Rate:",
            previous["Pass Percentage"], "%"
        )

        print(
            "Latest Pass Rate:",
            latest["Pass Percentage"], "%"
        )

        difference = (
            latest["Pass Percentage"]
            - previous["Pass Percentage"]
        )

        print("Pass Rate Change:", round(difference, 2), "%")

    else:
        print("\nOnly one run recorded.")
        print("Run the test executor again to compare results.")


if __name__ == "__main__":
    analyze_history()
