import json
import sys
from pathlib import Path

# Allows the test file to import modules from the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from utils.analyzer import analyze_skill_gap


def load_test_cases() -> dict:
    test_file = Path(__file__).parent / "test_cases.json"

    with open(test_file, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize_skills(skills: list[str]) -> list[str]:
    return sorted(skill.lower() for skill in skills)


def run_tests() -> None:
    test_cases = load_test_cases()

    passed = 0
    failed = 0

    for test_name, test_data in test_cases.items():
        result = analyze_skill_gap(
            test_data["resume_text"],
            test_data["job_description"]
        )

        actual_resume_skills = normalize_skills(
            result["resume_skills"]
        )
        actual_job_skills = normalize_skills(
            result["job_skills"]
        )
        actual_matched_skills = normalize_skills(
            result["matched_skills"]
        )
        actual_missing_skills = normalize_skills(
            result["missing_skills"]
        )

        expected_resume_skills = normalize_skills(
            test_data["expected_resume_skills"]
        )
        expected_job_skills = normalize_skills(
            test_data["expected_job_skills"]
        )
        expected_matched_skills = normalize_skills(
            test_data["expected_matched_skills"]
        )
        expected_missing_skills = normalize_skills(
            test_data["expected_missing_skills"]
        )

        checks = {
            "resume_skills": (
                expected_resume_skills,
                actual_resume_skills
            ),
            "job_skills": (
                expected_job_skills,
                actual_job_skills
            ),
            "matched_skills": (
                expected_matched_skills,
                actual_matched_skills
            ),
            "missing_skills": (
                expected_missing_skills,
                actual_missing_skills
            )
        }

        test_passed = all(
            expected == actual
            for expected, actual in checks.values()
        )

        if test_passed:
            print(f"PASS: {test_name}")
            passed += 1
        else:
            print(f"\nFAIL: {test_name}")
            print(f"Purpose: {test_data.get('purpose', 'Not provided')}")

            for field, (expected, actual) in checks.items():
                if expected != actual:
                    print(f"  {field}")
                    print(f"    Expected: {expected}")
                    print(f"    Actual:   {actual}")

            failed += 1

    total = passed + failed
    pass_percentage = (passed / total * 100) if total else 0

    print("\n---------------------------")
    print(f"Total tests: {total}")
    print(f"Passed:      {passed}")
    print(f"Failed:      {failed}")
    print(f"Pass rate:   {pass_percentage:.2f}%")
    print("---------------------------")


if __name__ == "__main__":
    run_tests()