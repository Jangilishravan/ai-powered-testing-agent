
import json
import os
from ai_client import ask_ai


FILE_NAME = "generated_test_cases.json"
COVERAGE_FILE = "coverage_suggestions.json"
AI_RECOMMENDATIONS_FILE = "ai_recommendations.json"
GROUPS_FILE = "coverage_groups.json"


def normalize_scenario(scenario):
    return " ".join(str(scenario).lower().split())


def generate_test_cases(requirement):

    prompt = f"""
You are an expert API testing engineer.

Our login API endpoint is:
POST http://127.0.0.1:5000/login

API validation rules:
- Valid username: sunny
- Valid password: sunny123
- Successful login returns HTTP 200.
- Invalid credentials return HTTP 401.
- Missing fields, empty fields, invalid formats,
  and unexpected data types return HTTP 400.
- Username must contain only alphanumeric characters.
- Username must contain between 3 and 20 characters.
- Password must contain between 6 and 30 characters.

Boundary test requirements:
- Username minimum: 3 characters.
- Username maximum: 20 characters.
- Password minimum: 6 characters.
- Password maximum: 30 characters.
- Use a valid-length password when testing username boundaries.
- Use a valid-length username when testing password boundaries.
- Below minimum and above maximum: expected status 400.
- At minimum and at maximum: expected status 401,
  because the credentials are deliberately incorrect
  but their lengths are valid.

IMPORTANT:

- Generate ONLY the scenarios requested below.

- For "Valid Username with Incorrect Password":
  use username "sunny" and password "wrong123".
  Expected status: 401.

- For "Null Credential Values":
  use JSON null values, not the string "null".
  Generate one test with both username and password set to null.
  Expected status: 400.

- For "Non-String Password":
  generate exactly three separate test cases
  with these exact Scenario names:

  1. Non-String Password - Numeric
     Password payload value: 123456

  2. Non-String Password - Array
     Password payload value: ["password123"]

  3. Non-String Password - Object
     Password payload value: {{"value": "password123"}}

  In all three cases:
  - Username must be "sunny".
  - Expected status code must be 400.
  - Keep the password value in its original JSON data type.
  - Do not convert these values into strings.

- If Missing Scenarios is provided, generate ONLY those scenarios.
- Never regenerate scenarios that are already covered.
- Do not automatically generate all eight boundary tests.
- Generate exactly one test case per requested scenario,
  except Non-String Password, which requires three cases.
- Do not generate duplicate scenarios.

Generate relevant test cases for this requirement:

{requirement}

Each test case MUST contain:
- Scenario
- Expected Result
- Expected Status Code
- Payload

Supported scenarios include:
- Valid Login
- Invalid Login
- Missing Password
- Empty Username
- Empty Password
- Both Fields Empty
- Missing Username
- Whitespace-Only Inputs
- Invalid Input Format
- SQL Injection Attempt
- Unexpected Data Types
- Username With Leading or Trailing Whitespace
- Username Below Minimum Length
- Username At Minimum Length
- Username At Maximum Length
- Username Above Maximum Length
- Password Below Minimum Length
- Password At Minimum Length
- Password At Maximum Length
- Password Above Maximum Length
- Valid Username with Incorrect Password
- Null Credential Values
- Non-String Password

Rules:
1. Generate only relevant scenarios.
2. Do not generate duplicate scenarios.
3. Generate realistic request payloads.
4. Payload must be a JSON object.
5. Do not include Test Case IDs; Python will assign them.
6. Do not claim that tests have been executed.
7. Return ONLY a valid JSON array.

Example:

[
    {{
        "Scenario": "Empty Password",
        "Expected Result": "Validation error",
        "Expected Status Code": 400,
        "Payload": {{
            "username": "sunny",
            "password": ""
        }}
    }}
]
"""

    response = ask_ai(prompt).strip()

    if response.startswith("```"):
        response = response.split("\n", 1)[1]
        response = response.rsplit("```", 1)[0].strip()

    test_cases = json.loads(response)

    if not isinstance(test_cases, list):
        raise ValueError("AI must return a JSON list.")

    validated_cases = []

    allowed_status_codes = {200, 400, 401}

    for case in test_cases:

        if not isinstance(case, dict):
            continue

        scenario = case.get("Scenario")
        payload = case.get("Payload")
        expected_status = case.get("Expected Status Code")
        expected_result = case.get("Expected Result")

        if not isinstance(scenario, str) or not scenario.strip():
            continue

        if not isinstance(payload, dict):
            continue

        if not set(payload.keys()).issubset({"username", "password"}):
            continue

        if not all(
            key in payload for key in ["username", "password"]
        ):
            continue

        if expected_status not in allowed_status_codes:
            continue

        if not isinstance(expected_result, str):
            continue

        normalized = normalize_scenario(scenario)

        # Validate the three non-string password scenarios.
        if normalized.startswith("non-string password -"):

            if payload.get("username") != "sunny":
                continue

            if expected_status != 400:
                continue

            password = payload.get("password")

            if normalized == "non-string password - numeric":
                if not isinstance(password, (int, float)) or isinstance(password, bool):
                    continue

            elif normalized == "non-string password - array":
                if not isinstance(password, list):
                    continue

            elif normalized == "non-string password - object":
                if not isinstance(password, dict):
                    continue

            else:
                continue

        # Validate the null credentials scenario.
        if normalized == "null credential values":

            if payload.get("username") is not None:
                continue

            if payload.get("password") is not None:
                continue

            if expected_status != 400:
                continue

        # Validate the incorrect password scenario.
        if normalized == "valid username with incorrect password":

            if payload.get("username") != "sunny":
                continue

            if payload.get("password") == "sunny123":
                continue

            if expected_status != 401:
                continue

        validated_cases.append({
            "Scenario": scenario,
            "Expected Result": expected_result,
            "Expected Status Code": expected_status,
            "Payload": payload
        })

    return validated_cases


def save_test_cases(new_cases):

    if os.path.exists(FILE_NAME):

        with open(FILE_NAME, "r", encoding="utf-8") as file:
            existing_cases = json.load(file)

    else:
        existing_cases = []

    if isinstance(existing_cases, dict):
        existing_cases = [existing_cases]

    # Find the highest existing test case ID.
    existing_ids = [
        int(str(case.get("Test Case ID", ""))[2:])
        for case in existing_cases
        if isinstance(case, dict)
        and str(case.get("Test Case ID", "")).startswith("TC")
        and str(case.get("Test Case ID", ""))[2:].isdigit()
    ]

    next_id = max(existing_ids, default=0) + 1

    for new_case in new_cases:

        new_scenario = normalize_scenario(new_case["Scenario"])

        # Avoid duplicate scenarios in the existing file.
        matching_case = next(
            (
                case for case in existing_cases
                if isinstance(case, dict)
                and normalize_scenario(case.get("Scenario", "")) == new_scenario
            ),
            None
        )

        if matching_case:

            new_case["Test Case ID"] = matching_case["Test Case ID"]

            existing_cases = [
                case for case in existing_cases
                if not (
                    isinstance(case, dict)
                    and normalize_scenario(case.get("Scenario", "")) == new_scenario
                )
            ]

        else:

            new_case["Test Case ID"] = f"TC{next_id:03d}"
            next_id += 1

        existing_cases.append(new_case)

    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(existing_cases, file, indent=4)

    return existing_cases


if __name__ == "__main__":

    try:

        # Step 1: Load recommendations from both sources.

        with open(COVERAGE_FILE, "r", encoding="utf-8") as file:
            coverage_suggestions = json.load(file)

        with open(AI_RECOMMENDATIONS_FILE, "r", encoding="utf-8") as file:
            ai_recommendations = json.load(file)

        suggestions = coverage_suggestions + ai_recommendations

        # Remove duplicate recommendation names.

        unique_suggestions = []
        seen_suggestions = set()

        for suggestion in suggestions:

            scenario = normalize_scenario(
                suggestion.get("Scenario", "")
            )

            if scenario and scenario not in seen_suggestions:
                unique_suggestions.append(suggestion)
                seen_suggestions.add(scenario)

        suggestions = unique_suggestions

        print("\nTotal recommendations loaded:", len(suggestions))

        # Step 2: Load existing test cases.

        if os.path.exists(FILE_NAME):

            with open(FILE_NAME, "r", encoding="utf-8") as file:
                existing_cases = json.load(file)

        else:
            existing_cases = []

        if isinstance(existing_cases, dict):
            existing_cases = [existing_cases]

        # Step 3: Identify existing scenarios.

        existing_scenarios = {
            normalize_scenario(case.get("Scenario", ""))
            for case in existing_cases
            if isinstance(case, dict)
            and case.get("Scenario")
        }

        # Step 4: Load grouped coverage configuration.

        with open(GROUPS_FILE, "r", encoding="utf-8") as file:
            coverage_groups = json.load(file)

        normalized_groups = {
            normalize_scenario(group_name): {
                normalize_scenario(item)
                for item in required_scenarios
            }
            for group_name, required_scenarios in coverage_groups.items()
        }

        new_suggestions = []

        for suggestion in suggestions:

            scenario = suggestion.get("Scenario", "").strip()

            if not scenario:
                continue

            normalized = normalize_scenario(scenario)

            # Check grouped coverage suggestions.

            if normalized in normalized_groups:

                required_scenarios = normalized_groups[normalized]

                missing_scenarios = (
                    required_scenarios - existing_scenarios
                )

                if not missing_scenarios:

                    print("AI suggestion fully covered:", scenario)

                else:

                    print("AI suggestion partially covered:", scenario)

                    print("Missing scenarios:", sorted(missing_scenarios))

                    new_suggestions.append({
                        **suggestion,
                        "Missing Scenarios": sorted(missing_scenarios)
                    })

            # Check ordinary coverage suggestions.

            elif normalized in existing_scenarios:

                print("AI suggestion already covered:", scenario)

            else:

                print("New AI suggestion found:", scenario)

                new_suggestions.append(suggestion)

        # Step 5: Check whether AI generation is necessary.

        if not new_suggestions:

            print(
                "\nAll AI coverage suggestions "
                "are already covered."
            )

            print("No additional AI API call required.")

        else:

            print("\nNew coverage suggestions found:")

            print(json.dumps(new_suggestions, indent=4))

            # Step 6: Prepare AI requirement.

            requirement = (
                "Generate test cases only for the missing coverage "
                "scenarios provided below. Follow all API validation "
                "rules. If a suggestion contains Missing Scenarios, "
                "generate only those individual scenarios. "
                "Do not regenerate already covered scenarios.\n\n"
                + json.dumps(new_suggestions, indent=4)
            )

            # Step 7: Generate test cases.

            results = generate_test_cases(requirement)

            # Step 8: Keep only requested and genuinely new scenarios.

            requested_scenarios = set()

            for suggestion in new_suggestions:

                if suggestion.get("Missing Scenarios"):

                    requested_scenarios.update(
                        normalize_scenario(item)
                        for item in suggestion["Missing Scenarios"]
                    )

                else:

                    scenario = normalize_scenario(
                        suggestion["Scenario"]
                    )

                    requested_scenarios.add(scenario)

                    if scenario == "non-string password":

                        requested_scenarios.update({
                            "non-string password - numeric",
                            "non-string password - array",
                            "non-string password - object"
                        })

            filtered_results = [
                case for case in results
                if normalize_scenario(case["Scenario"]) in requested_scenarios
                and normalize_scenario(case["Scenario"]) not in existing_scenarios
            ]

            if filtered_results:

                # Step 9: Save generated test cases.

                saved_cases = save_test_cases(filtered_results)

                print(
                    "\n========== AI GENERATED COVERAGE TESTS =========="
                )

                print(json.dumps(filtered_results, indent=4))

                print("\nNew test cases saved successfully!")

                print(
                    "New cases generated:",
                    len(filtered_results)
                )

                print(
                    "Total test cases stored:",
                    len(saved_cases)
                )

            else:

                print(
                    "\nAI did not generate any new valid "
                    "coverage test cases."
                )

    except FileNotFoundError as error:

        print("\nRequired file not found:", error)

    except json.JSONDecodeError:

        print(
            "\nInvalid JSON found in a project file "
            "or AI response."
        )

    except Exception as error:

        print("\nError generating test cases:", error)

