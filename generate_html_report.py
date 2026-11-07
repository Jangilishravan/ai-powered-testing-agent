
import json
import html
from datetime import datetime
from ai_client import ask_ai


# ==========================================
# 1. LOAD LATEST EXECUTION RESULTS
# ==========================================

with open("execution_results.json", "r") as file:
    results = json.load(file)


# ==========================================
# 2. LOAD EXECUTION HISTORY
# ==========================================

try:
    with open("execution_history.json", "r") as file:
        history = json.load(file)

except FileNotFoundError:
    history = []

# ==========================================
# 2A. LOAD TEST GAP ANALYSIS REPORT
# ==========================================

try:
    with open("gap_analysis_report.json", "r") as file:
        gap_report = json.load(file)

except FileNotFoundError:
    gap_report = {
        "Summary": {},
        "Missing Tests": [],
        "Unexecuted Tests": [],
        "Failed Tests": [],
        "Historical Execution Summary": []
    }


gap_summary = gap_report.get("Summary", {})

missing_tests = gap_report.get("Missing Tests", [])

unexecuted_tests = gap_report.get("Unexecuted Tests", [])

gap_failed_tests = gap_report.get("Failed Tests", [])


# ==========================================
# 2B. LOAD WEAK AREA ANALYSIS
# ==========================================

try:
    with open("weak_area_analysis.json", "r", encoding="utf-8") as file:
        weak_report = json.load(file)

except FileNotFoundError:
    weak_report = {
        "Total Tests Analyzed": 0,
        "Total Weak Tests": 0,
        "High Priority": 0,
        "Medium Priority": 0,
        "Low Priority": 0,
        "Flaky Tests": 0,
        "Repeated Failures": 0,
        "Performance Concerns": 0,
        "Weak Areas": []
    }

weak_areas = weak_report.get("Weak Areas", [])

weak_total = weak_report.get("Total Weak Tests", 0)
weak_high = weak_report.get("High Priority", 0)
weak_medium = weak_report.get("Medium Priority", 0)
weak_low = weak_report.get("Low Priority", 0)
weak_flaky = weak_report.get("Flaky Tests", 0)
weak_repeated = weak_report.get("Repeated Failures", 0)
weak_performance = weak_report.get("Performance Concerns", 0)


# ==========================================
# 2C. LOAD PERFORMANCE ANALYSIS
# ==========================================

try:
    with open("performance_analysis.json", "r", encoding="utf-8") as file:
        performance_report = json.load(file)

except FileNotFoundError:
    performance_report = {
        "Tests Analyzed": 0,
        "Tests With Insufficient Data": 0,
        "Insufficient Data Test IDs": [],
        "Potential Performance Concerns": 0,
        "Performance Results": []
    }

performance_results = performance_report.get("Performance Results", [])

performance_tests_analyzed = performance_report.get("Tests Analyzed", 0)

performance_insufficient = performance_report.get(
    "Tests With Insufficient Data", 0
)

performance_concerns = performance_report.get(
    "Potential Performance Concerns", 0
)

insufficient_data_ids = performance_report.get(
    "Insufficient Data Test IDs", []
)

# ==========================================
# 2D. LOAD HISTORICAL TREND DATA
# ==========================================

try:
    with open("execution_history.json", "r", encoding="utf-8") as file:
        execution_history = json.load(file)

except FileNotFoundError:
    execution_history = []

historical_runs = execution_history

trend_run_count = len(historical_runs)

if trend_run_count >= 2:

    first_run = historical_runs[0]
    latest_run = historical_runs[-1]

    pass_rate_change = (
        latest_run["Pass Percentage"]
        - first_run["Pass Percentage"]
    )

    execution_time_change = (
        latest_run["Average Execution Time"]
        - first_run["Average Execution Time"]
    )

else:
    pass_rate_change = 0
    execution_time_change = 0

# Determine overall quality trend

if pass_rate_change > 0:
    quality_trend = "Improving"
elif pass_rate_change < 0:
    quality_trend = "Declining"
else:
    quality_trend = "Stable"


# Determine overall performance trend

if execution_time_change < 0:
    performance_trend = "Faster"
elif execution_time_change > 0:
    performance_trend = "Slower"
else:
    performance_trend = "Unchanged"

# ==========================================
# 2D. LOAD IMPROVEMENT TRACKING
# ==========================================

try:
    with open("improvement_tracking.json", "r", encoding="utf-8") as file:
        improvement_report = json.load(file)

except FileNotFoundError:
    improvement_report = {
        "Total Tests Tracked": 0,
        "Minimum Required Observations": 5,
        "Tracking Results": []
    }

improvement_results = improvement_report.get("Tracking Results", [])

improvement_total = improvement_report.get("Total Tests Tracked", 0)

improved_tests = sum(
    1 for test in improvement_results
    if test.get("Performance Status") == "FASTER"
)

slower_tests = sum(
    1 for test in improvement_results
    if test.get("Performance Status") == "SLOWER"
)

insufficient_tests = sum(
    1 for test in improvement_results
    if test.get("Performance Status") == "INSUFFICIENT DATA"
)


# ==========================================
# 3. CALCULATE TEST STATISTICS
# ==========================================

total = len(results)

passed = sum(
    1 for test in results
    if test["Result"] == "PASSED"
)

failed = sum(
    1 for test in results
    if test["Result"] == "FAILED"
)

pass_percentage = (passed / total * 100) if total else 0

execution_times = [
    float(test["Execution Time"])
    for test in results
]

average_time = (
    sum(execution_times) / len(execution_times)
    if execution_times else 0
)

fastest_time = min(execution_times) if execution_times else 0
slowest_time = max(execution_times) if execution_times else 0


# ==========================================
# 4. FASTEST AND SLOWEST TESTS
# ==========================================

fastest_test = None
slowest_test = None

if results:

    fastest_test = min(
        results,
        key=lambda test: float(test["Execution Time"])
    )

    slowest_test = max(
        results,
        key=lambda test: float(test["Execution Time"])
    )


fastest_name = (
    html.escape(str(fastest_test["Scenario"]))
    if fastest_test else "N/A"
)

slowest_name = (
    html.escape(str(slowest_test["Scenario"]))
    if slowest_test else "N/A"
)


# ==========================================
# 5. GENERATE TEST TABLE
# ==========================================

table_rows = ""

for test in results:

    status = test["Result"]
    status_class = "passed" if status == "PASSED" else "failed"

    table_rows += f"""
    <tr>
        <td>{html.escape(str(test['Test Case ID']))}</td>
        <td>{html.escape(str(test['Scenario']))}</td>
        <td>{html.escape(str(test['Expected Status']))}</td>
        <td>{html.escape(str(test['Actual Status']))}</td>
        <td>{float(test['Execution Time']):.4f} sec</td>
        <td class="{status_class}">{html.escape(status)}</td>
    </tr>
    """


# ==========================================
# 6. PREPARE AI FAILURE ANALYSIS
# ==========================================

failure_details = []

for test in results:

    if test["Result"] == "FAILED":

        failure_details.append({
            "Test Case ID": test["Test Case ID"],
            "Scenario": test["Scenario"],
            "Expected Status": test["Expected Status"],
            "Actual Status": test["Actual Status"],
            "Response Message": test.get("Response Message", "")
        })


# ==========================================
# 7. GENERATE AI INSIGHTS
# ==========================================

prompt = f"""
You are an expert software testing analyst.

Analyze these execution results.

Total tests: {total}
Passed: {passed}
Failed: {failed}
Pass percentage: {pass_percentage:.2f}%
Average execution time: {average_time:.4f} seconds

Failed test details:
{json.dumps(failure_details, indent=2)}

Provide:
1. Overall execution summary.
2. Important observations.
3. Recommendations to improve testing.
4. Additional test scenarios worth considering.

If all tests passed, mention that no failures were observed.
Do not invent failures or root causes.
Clearly distinguish observations from suggestions.
Keep the report concise and beginner-friendly.
"""


import os

if os.getenv("RUN_AI_INSIGHTS", "false").lower() == "true":

    try:
        print("\nGenerating AI report insights...")

        ai_insights = ask_ai(prompt)

    except Exception as error:
        ai_insights = "AI insights could not be generated: " + str(error)

else:

    ai_insights = (
        "AI insights were skipped to conserve API credits. "
        "All execution statistics, performance analysis, "
        "coverage results and historical analytics are available above."
    )

    print("\nAI insights skipped. No API call was made.")

ai_insights_html = html.escape(ai_insights)



# ==========================================
# 8. PREPARE HISTORICAL CHART DATA
# ==========================================

run_labels = []

for run in history:

    execution_date = run.get("Execution Date", "")

    try:
        label = datetime.strptime(
            execution_date,
            "%Y-%m-%d %H:%M:%S"
        ).strftime("%m-%d %H:%M")

    except (ValueError, TypeError):

        try:
            label = datetime.strptime(
                run.get("Run ID", ""),
                "%Y%m%d_%H%M%S"
            ).strftime("%m-%d %H:%M")

        except (ValueError, TypeError):
            label = run.get("Run ID", "Unknown")

    run_labels.append(label)

historical_pass_rates = [
    float(run.get("Pass Percentage", 0))
    for run in history
]

historical_execution_times = [
    float(run.get("Average Execution Time", 0))
    for run in history
]

# Safely prepare JavaScript data
chart_labels = json.dumps(run_labels).replace("</", "<\\/")
chart_pass_rates = json.dumps(historical_pass_rates)
chart_execution_times = json.dumps(
    historical_execution_times
)


# ==========================================
# 9. CREATE HTML DASHBOARD
# ==========================================

html_content = f"""
<!DOCTYPE html>
<html>

<head>

    <title>AI Testing Agent Dashboard</title>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>

        body {{
            font-family: Arial, sans-serif;
            margin: 30px;
            background: #f4f6f9;
            color: #263238;
        }}

        h1 {{
            text-align: center;
        }}

        .summary {{
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 20px;
            margin: 25px;
        }}

        .card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            min-width: 130px;
            box-shadow: 0 2px 6px #ddd;
        }}

        .card h2 {{
            font-size: 28px;
        }}

        .passed {{
            color: green;
            font-weight: bold;
        }}

        .failed {{
            color: red;
            font-weight: bold;
        }}

        .statistics, .insights, .chart-card {{
            background: white;
            padding: 20px;
            margin-top: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 6px #ddd;
        }}

        .charts {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 20px;
            margin-top: 25px;
        }}

        .chart-container {{
            position: relative;
            height: 300px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
        }}

        th, td {{
            padding: 12px;
            border: 1px solid #ddd;
            text-align: center;
        }}

        th {{
            background: #263238;
            color: white;
        }}

        .insights {{
            line-height: 1.7;
        }}

        .insights-content {{
            white-space: pre-wrap;
        }}

        .footer {{
            text-align: center;
            margin-top: 30px;
            color: gray;
        }}

        @media (max-width: 750px) {{
            .charts {{
                grid-template-columns: 1fr;
            }}

            body {{
                margin: 12px;
            }}
        }}

    </style>

</head>

<body>

    <h1>AI Testing Agent - Analytics Dashboard</h1>

    <div class="summary">

        <div class="card">
            <h2>{total}</h2>
            <p>Total Tests</p>
        </div>

        <div class="card">
            <h2 class="passed">{passed}</h2>
            <p>Passed</p>
        </div>

        <div class="card">
            <h2 class="failed">{failed}</h2>
            <p>Failed</p>
        </div>

        <div class="card">
            <h2>{pass_percentage:.2f}%</h2>
            <p>Pass Percentage</p>
        </div>

    </div>

<!-- RELIABILITY SCORECARD -->

<h2>Reliability Scorecard</h2>

<div class="summary">

    <div class="card">
        <h2>{pass_percentage:.2f}%</h2>
        <p>Test Pass Rate</p>
    </div>

    <div class="card">
        <h2>{gap_summary.get("Execution Coverage Percentage", 0):.2f}%</h2>
        <p>Execution Coverage</p>
    </div>

    <div class="card">
        <h2>{len(gap_failed_tests)}</h2>
        <p>Failed Tests</p>
    </div>

    <div class="card">
        <h2>{len(unexecuted_tests)}</h2>
        <p>Unexecuted Tests</p>
    </div>

</div>

<div class="statistics">

    <h3>Reliability Assessment</h3>

    <p>
        Tests Passed: {passed} out of {total}
    </p>

    <p>
        Execution Coverage:
        {gap_summary.get("Execution Coverage Percentage", 0):.2f}%
    </p>

    <p>
        Missing Scenarios: {len(missing_tests)}
    </p>

    <p>
        Failed Tests: {len(gap_failed_tests)}
    </p>

</div>

<!-- TEST GAP ANALYSIS -->

<h2>Test Gap Analysis</h2>

<div class="summary">

    <div class="card">
        <h2>{gap_summary.get("Total Generated Tests", 0)}</h2>
        <p>Generated Tests</p>
    </div>

    <div class="card">
        <h2>{gap_summary.get("Total Executed Tests", 0)}</h2>
        <p>Executed Tests</p>
    </div>

    <div class="card">
        <h2>{gap_summary.get("Total Unexecuted Tests", 0)}</h2>
        <p>Unexecuted Tests</p>
    </div>

    <div class="card">
        <h2>{gap_summary.get("Total Missing Scenarios", 0)}</h2>
        <p>Missing Scenarios</p>
    </div>

    <div class="card">
        <h2>{gap_summary.get("Execution Coverage Percentage", 0):.2f}%</h2>
        <p>Execution Coverage</p>
    </div>

</div>


<div class="statistics">

    <h3>Gap Detection Results</h3>

    <p>Missing Test Scenarios: {len(missing_tests)}</p>

    <p>Unexecuted Tests: {len(unexecuted_tests)}</p>

    <p>Failed Tests: {len(gap_failed_tests)}</p>

</div>


<div class="statistics">

    <h3>Missing Test Scenarios</h3>

    {''.join(
        f"<p><strong>{html.escape(str(test.get('Scenario', '')))}</strong> - "
        f"Priority: {html.escape(str(test.get('Priority', 'Medium')))}<br>"
        f"{html.escape(str(test.get('Reason', '')))}</p>"
        for test in missing_tests
    ) or "<p>No missing test scenarios detected.</p>"}

</div>


<div class="statistics">

    <h3>Unexecuted Tests</h3>

    {''.join(
        f"<p>{html.escape(str(test.get('Test Case ID', '')))} - "
        f"{html.escape(str(test.get('Scenario', '')))}</p>"
        for test in unexecuted_tests
    ) or "<p>All generated tests have been executed.</p>"}

</div>


<div class="statistics">

    <h3>Failed Tests - Gap Analysis</h3>

    {''.join(
        f"<p>{html.escape(str(test.get('Test Case ID', '')))} - "
        f"{html.escape(str(test.get('Scenario', '')))} - "
        f"{html.escape(str(test.get('Response Message', '')))}</p>"
        for test in gap_failed_tests
    ) or "<p>No failed tests detected.</p>"}

</div>


<!-- WEAK AREA ANALYSIS -->

<h2>Weak Area Analysis</h2>

<div class="summary">

    <div class="card">
        <h2>{weak_total}</h2>
        <p>Total Weak Tests</p>
    </div>

    <div class="card">
        <h2>{weak_high}</h2>
        <p>High Priority</p>
    </div>

    <div class="card">
        <h2>{weak_medium}</h2>
        <p>Medium Priority</p>
    </div>

    <div class="card">
        <h2>{weak_low}</h2>
        <p>Low Priority</p>
    </div>

</div>

<div class="statistics">

    <h3>Detected Weak Areas</h3>

    {''.join(
        f"<p><strong>{html.escape(str(test.get('Test Case ID', '')))} - "
        f"{html.escape(str(test.get('Scenario', '')))}</strong><br>"
        f"Priority: {html.escape(str(test.get('Priority', '')))}<br>"
        f"Issues: {html.escape(', '.join(test.get('Issues Detected', [])))}</p>"
        for test in weak_areas
    ) or "<p>No weak areas detected.</p>"}

</div>

<div class="statistics">

    <h3>Reliability and Performance Summary</h3>

    <p>Flaky Tests: {weak_flaky}</p>

    <p>Repeated Failures: {weak_repeated}</p>

    <p>Performance Concerns: {weak_performance}</p>

</div>


<!-- DETAILED PERFORMANCE ANALYSIS -->

<h2>Detailed Performance Analysis</h2>

<div class="summary">

    <div class="card">
        <h2>{performance_tests_analyzed}</h2>
        <p>Tests Analyzed</p>
    </div>

    <div class="card">
        <h2>{performance_concerns}</h2>
        <p>Potential Performance Concerns</p>
    </div>

    <div class="card">
        <h2>{performance_insufficient}</h2>
        <p>Insufficient Historical Data</p>
    </div>

</div>

<div class="statistics">

    <h3>Performance Results</h3>

    <table>
        <tr>
            <th>Test ID</th>
            <th>Observations</th>
            <th>Average (sec)</th>
            <th>Median (sec)</th>
            <th>Maximum (sec)</th>
            <th>Slow Executions</th>
            <th>Status</th>
        </tr>

        {''.join(
            f"<tr>"
            f"<td>{html.escape(str(test.get('Test Case ID', '')))}</td>"
            f"<td>{test.get('Observations', 0)}</td>"
            f"<td>{test.get('Average Execution Time', 0):.4f}</td>"
            f"<td>{test.get('Median Execution Time', 0):.4f}</td>"
            f"<td>{test.get('Maximum Execution Time', 0):.4f}</td>"
            f"<td>{test.get('Unusual Slow Execution Count', 0)}</td>"
            f"<td>{'Potential Concern' if test.get('Potential Performance Concern') else 'Normal'}</td>"
            f"</tr>"
            for test in performance_results
        ) or "<tr><td colspan='7'>No performance data available.</td></tr>"}

    </table>

</div>

<div class="statistics">

    <h3>Insufficient Historical Data</h3>

    <p>These tests need more execution history before reliable performance analysis:</p>

    <p>{html.escape(', '.join(insufficient_data_ids)) or 'None'}</p>

</div>

<div class="statistics">

    <h3>Unusual Slow Executions</h3>

    {''.join(
        f"<p><strong>{html.escape(str(test.get('Test Case ID', '')))}</strong><br>"
        f"Slow Execution Count: {test.get('Unusual Slow Execution Count', 0)}<br>"
        + ''.join(
            f"Date: {html.escape(str(slow.get('Execution Date', '')))} | "
            f"Time: {slow.get('Execution Time', 0):.4f} seconds<br>"
            for slow in test.get('Slow Executions', [])
        )
        + "</p>"
        for test in performance_results
        if test.get("Slow Executions")
    ) or "<p>No unusual slow executions detected.</p>"}

</div>


<!-- IMPROVEMENT TRACKING -->

<h2>Improvement Tracking</h2>

<div class="summary">

    <div class="card">
        <h2>{improvement_total}</h2>
        <p>Total Tests Tracked</p>
    </div>

    <div class="card">
        <h2>{improved_tests}</h2>
        <p>Faster Tests</p>
    </div>

    <div class="card">
        <h2>{slower_tests}</h2>
        <p>Slower Tests</p>
    </div>

    <div class="card">
        <h2>{insufficient_tests}</h2>
        <p>Insufficient Data</p>
    </div>

</div>

<div class="statistics">

    <h3>Test Performance Comparison</h3>

    {''.join(
        f"<p><strong>{html.escape(str(test.get('Test Case ID', '')))} - "
        f"{html.escape(str(test.get('Scenario', '')))}</strong><br>"
        f"Previous Median: {float(test.get('Previous Median', 0)):.4f} seconds<br>"
        f"Latest Execution: {float(test.get('Latest Execution Time', 0)):.4f} seconds<br>"
        f"Change: {float(test.get('Change Percentage', 0)):+.2f}%<br>"
        f"Performance Status: {html.escape(str(test.get('Performance Status', 'UNKNOWN')))}<br>"
        f"Latest Test Result: {html.escape(str(test.get('Latest Result', 'UNKNOWN')))}</p>"
        for test in improvement_results
    ) or "<p>No improvement tracking data available.</p>"}

</div>
<div class="statistics">

    <h3>Execution Statistics</h3>

        <p>Average Execution Time: {average_time:.4f} seconds</p>

        <p>Fastest Test: {fastest_name}
        ({fastest_time:.4f} seconds)</p>

        <p>Slowest Test: {slowest_name}
        ({slowest_time:.4f} seconds)</p>

        <p>Total Historical Runs: {len(history)}</p>

    </div>

<!-- HISTORICAL TREND SUMMARY -->

<h2>Historical Trend Analysis</h2>

<div class="summary">

    <div class="card">
        <h2>{trend_run_count}</h2>
        <p>Historical Runs Analyzed</p>
    </div>

    <div class="card">
        <h2>{pass_rate_change:+.2f}%</h2>
        <p>Pass Rate Change</p>
    </div>

    <div class="card">
        <h2>{execution_time_change:+.4f}s</h2>
        <p>Execution Time Change</p>
    </div>

</div>

<div class="statistics">

    <h3>Overall Quality Trend: {quality_trend}</h3>

    <h3>Overall Performance Trend: {performance_trend}</h3>

    <p>Comparison between the earliest and latest recorded execution runs.</p>

</div>

    <!-- VISUAL ANALYTICS -->

    <h2>Visual Analytics</h2>

    <div class="charts">

        <div class="chart-card">

            <h3>Pass vs Fail Distribution</h3>

            <div class="chart-container">
                <canvas id="resultChart"></canvas>
            </div>

        </div>


        <div class="chart-card">

            <h3>Historical Pass Percentage</h3>

            <div class="chart-container">
                <canvas id="passTrendChart"></canvas>
            </div>

        </div>


        <div class="chart-card">

            <h3>Execution Time Trend</h3>

            <div class="chart-container">
                <canvas id="timeTrendChart"></canvas>
            </div>

        </div>

    </div>


    <h2>Test Execution Details</h2>

    <table>

        <tr>
            <th>Test ID</th>
            <th>Scenario</th>
            <th>Expected</th>
            <th>Actual</th>
            <th>Execution Time</th>
            <th>Result</th>
        </tr>

        {table_rows}

    </table>


    <div class="insights">

        <h2>AI-Generated Test Insights</h2>

        <div class="insights-content">{ai_insights_html}</div>

    </div>


    <div class="footer">

        <p>Report generated:
        {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

        <p>Powered by OpenAI, Python and Chart.js</p>

    </div>


    <!-- CHART CONFIGURATION -->

    <script>

        const runLabels = {chart_labels};
        const passRates = {chart_pass_rates};
        const executionTimes = {chart_execution_times};


        // Pass vs Fail Doughnut Chart

        new Chart(document.getElementById("resultChart"), {{

            type: "doughnut",

            data: {{

                labels: ["Passed", "Failed"],

                datasets: [{{

                    data: [{passed}, {failed}],

                    backgroundColor: ["#22c55e", "#ef4444"]

                }}]

            }},

            options: {{

                responsive: true,
                maintainAspectRatio: false

            }}

        }});


        // Historical Pass Percentage Chart

        new Chart(document.getElementById("passTrendChart"), {{

            type: "line",

            data: {{

                labels: runLabels,

                datasets: [{{

                    label: "Pass Percentage (%)",

                    data: passRates,

                    borderColor: "#2563eb",
                    backgroundColor: "rgba(37,99,235,0.15)",
                    fill: true,
                    tension: 0.3

                }}]

            }},

            options: {{

                responsive: true,
                maintainAspectRatio: false,

               scales: {{

    x: {{
        ticks: {{
            callback: function(value, index) {{
                return index % 2 === 0
                    ? this.getLabelForValue(value)
                    : "";
            }}
        }}
    }},

    y: {{
        beginAtZero: true,
        max: 100
    }}

}}
            }}

        }});


        // Execution Time Trend Chart

        new Chart(document.getElementById("timeTrendChart"), {{

            type: "line",

            data: {{

                labels: runLabels,

                datasets: [{{

                    label: "Average Execution Time (seconds)",

                    data: executionTimes,

                    borderColor: "#f59e0b",
                    backgroundColor: "rgba(245,158,11,0.15)",
                    fill: true,
                    tension: 0.3

                }}]

            }},

           options: {{

    responsive: true,
    maintainAspectRatio: false,

    scales: {{

        x: {{
            ticks: {{
                callback: function(value, index) {{
                    return index % 2 === 0
                        ? this.getLabelForValue(value)
                        : "";
                }}
            }}
        }}

    }}

}}

        }});

    </script>

</body>

</html>
"""


# ==========================================
# 10. SAVE REPORT
# ==========================================

with open("execution_report.html", "w", encoding="utf-8") as file:
    file.write(html_content)


print("\n========== REPORT SUMMARY ==========")

print("Total Tests:", total)
print("Passed:", passed)
print("Failed:", failed)

print(f"Pass Percentage: {pass_percentage:.2f}%")
print(f"Average Execution Time: {average_time:.4f} seconds")

print("Historical Runs:", len(history))

print("\nAI insights section prepared successfully!")
print("\nHTML report generated successfully!")
print("Report saved as execution_report.html")
