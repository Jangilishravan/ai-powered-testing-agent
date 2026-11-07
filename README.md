# AI-Powered Software Testing Agent

An AI-assisted software testing automation project that generates API test scenarios, executes test cases, analyzes test coverage and performance, tracks historical results, and produces an interactive HTML testing dashboard.

## Project Overview

The AI Testing Agent is designed to reduce manual testing effort by automating test generation, execution, analysis, and reporting.

It combines traditional automation testing techniques with AI-assisted test recommendations and historical test analytics.

## Key Features

- **UI Automation:** Automates login scenarios using Playwright and pytest.
- **API Testing:** Tests REST API endpoints using Python Requests.
- **Test Case Generation:** Generates API test scenarios using AI.
- **Batch Test Execution:** Executes generated test cases against a local Flask API.
- **Test Coverage Analysis:** Identifies missing, unexecuted, and failed test scenarios.
- **Historical Analysis:** Tracks test execution results across multiple runs.
- **Performance Analysis:** Detects unusual execution-time variations.
- **Weak Area Detection:** Identifies test cases that may need further investigation.
- **Improvement Tracking:** Compares recent execution times against previous results.
- **HTML Dashboard:** Generates a detailed report with execution statistics, charts, and analysis.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Playwright | Browser automation |
| Pytest | Test execution framework |
| Requests | API testing |
| Flask | Local authentication API |
| OpenAI API | AI-assisted test generation and analysis |
| JSON | Test data and execution results |
| HTML, CSS, JavaScript | Test dashboard and reports |
| Chart.js | Dashboard visualizations |
| Git | Version control |

## Project Structure

```text
ai-testing-agent/
│
├── api_tests/
│   ├── auth_server.py
│   ├── test_api.py
│   └── test_auth.py
│
├── pages/
│   ├── __init__.py
│   └── login_page.py
│
├── test_data/
│   └── login_data.json
│
├── screenshots/
├── logs/
│
├── ai_client.py
├── ai_test_generator.py
├── ai_gap_recommender.py
├── execute_generated_tests.py
├── generated_test_cases.json
├── execution_results.json
│
├── coverage_analyzer.py
├── historical_test_analyzer.py
├── performance_analyzer.py
├── weak_area_detector.py
├── improvement_tracker.py
│
├── generate_html_report.py
├── execution_history.json
├── gap_analysis_report.json
├── performance_analysis.json
├── weak_area_analysis.json
├── improvement_tracking.json
│
├── main.py
├── .env
├── .gitignore
└── README.md
```

## Setup and Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ai-testing-agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install pytest pytest-html requests flask playwright openai python-dotenv
```

Install the Playwright browser:

```bash
playwright install
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=your_supported_model_name
```

Never commit your actual API key to GitHub.

## Running the Project

### Start the local Flask API

Open the first terminal:

```bash
python -m api_tests.auth_server
```

The local API runs at:

```text
http://127.0.0.1:5000
```

Keep this terminal running while executing the API tests.

### Run API tests

Open a second terminal:

```bash
pytest api_tests/test_api.py -v
```

### Run authentication tests

```bash
pytest api_tests/test_auth.py -v
```

### Execute AI-generated test cases

```bash
python execute_generated_tests.py
```

This executes the generated test scenarios and records the results.

**Note:** This workflow may use OpenAI API credits depending on the configured AI features.

### Run coverage analysis

```bash
python coverage_analyzer.py
```

### Run historical analysis

```bash
python historical_test_analyzer.py
```

### Run performance analysis

```bash
python performance_analyzer.py
```

### Run weak-area detection

```bash
python weak_area_detector.py
```

### Run improvement tracking

```bash
python improvement_tracker.py
```

### Generate the HTML dashboard

```bash
python generate_html_report.py
```

Open the generated report:

```powershell
Start-Process execution_report.html
```

AI-generated report insights are optional and disabled by default to conserve API credits.

## Current Project Results

The current verified execution contains:

| Metric | Result |
|---|---:|
| Generated Test Cases | 32 |
| Executed Test Cases | 32 |
| Passed Test Cases | 32 |
| Failed Test Cases | 0 |
| Execution Coverage | 100% |
| Pass Percentage | 100% |
| Historical Runs | 17 |
| Detected Weak Areas | 5 |

These are results from a recorded development run and may change as new tests are added.

## Future Enhancements

- Integration with CI/CD pipelines.
- Support for additional API endpoints.
- More advanced AI-based test recommendations.
- Automated test scheduling.
- Enhanced dashboard filtering and export options.

## Author

**Jangili Shravan Kumar**

