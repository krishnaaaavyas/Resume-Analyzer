import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from utils.analyzer import extract_skill_evidence


TEST_CASES = {
    "high_confidence": {
        "text": "Developed a React dashboard.",
        "skill": "react",
        "expected_confidence": "high",
        "expected_evidence": "Developed a React dashboard.",
    },
    "medium_confidence": {
        "text": "Worked with Python.",
        "skill": "python",
        "expected_confidence": "medium",
        "expected_evidence": "Worked with Python.",
    },
    "low_confidence": {
        "text": "Currently learning Docker.",
        "skill": "docker",
        "expected_confidence": "low",
        "expected_evidence": "Currently learning Docker.",
    },
    "rejected_skill": {
        "text": "No experience with AWS.",
        "skill": "aws",
        "expected_confidence": "rejected",
        "expected_evidence": "No experience with AWS.",
    },
    "strongest_evidence_wins": {
        "text": (
            "Currently learning React. "
            "Developed a React dashboard."
        ),
        "skill": "react",
        "expected_confidence": "high",
        "expected_evidence": "Developed a React dashboard.",
    },
}


def run_tests() -> None:
    passed = 0
    failed = 0

    for test_name, test_data in TEST_CASES.items():
        evidence = extract_skill_evidence(test_data["text"])
        skill = test_data["skill"]

        if skill not in evidence:
            print(f"\nFAIL: {test_name}")
            print(f"  Skill '{skill}' was not detected.")
            failed += 1
            continue

        actual = evidence[skill]

        confidence_correct = (
            actual["confidence"]
            == test_data["expected_confidence"]
        )

        evidence_correct = (
            actual["evidence_text"]
            == test_data["expected_evidence"]
        )

        if confidence_correct and evidence_correct:
            print(f"PASS: {test_name}")
            passed += 1
        else:
            print(f"\nFAIL: {test_name}")

            if not confidence_correct:
                print(
                    "  Confidence:"
                    f"\n    Expected: {test_data['expected_confidence']}"
                    f"\n    Actual:   {actual['confidence']}"
                )

            if not evidence_correct:
                print(
                    "  Evidence:"
                    f"\n    Expected: {test_data['expected_evidence']}"
                    f"\n    Actual:   {actual['evidence_text']}"
                )

            failed += 1

    total = passed + failed
    pass_rate = (passed / total * 100) if total else 0

    print("\n---------------------------")
    print(f"Total tests: {total}")
    print(f"Passed:      {passed}")
    print(f"Failed:      {failed}")
    print(f"Pass rate:   {pass_rate:.2f}%")
    print("---------------------------")


if __name__ == "__main__":
    run_tests()