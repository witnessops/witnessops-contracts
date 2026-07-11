import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = (
    ROOT / "schemas" / "ai-model-evaluation" / "evidence-packet.schema.json"
)
FIXTURE_ROOT = ROOT / "fixtures" / "ai-model-evaluation"
VALID_DRAFT_PATH = FIXTURE_ROOT / "valid" / "evidence-packet.draft.valid.json"
NEGATIVE_CASES_PATH = FIXTURE_ROOT / "invalid" / "negative-cases.json"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


SCHEMA = load_json(SCHEMA_PATH)
VALID_DRAFT = load_json(VALID_DRAFT_PATH)
NEGATIVE_CASES = load_json(NEGATIVE_CASES_PATH)["cases"]


def validator() -> Draft202012Validator:
    Draft202012Validator.check_schema(SCHEMA)
    return Draft202012Validator(SCHEMA, format_checker=FormatChecker())


def pointer_tokens(pointer: str) -> list[str]:
    if pointer == "":
        return []
    assert pointer.startswith("/")
    return [token.replace("~1", "/").replace("~0", "~") for token in pointer[1:].split("/")]


def apply_mutation(instance: dict, case: dict) -> None:
    tokens = pointer_tokens(case["path"])
    assert tokens, "The mutation corpus may not replace the document root."

    parent = instance
    for token in tokens[:-1]:
        parent = parent[int(token)] if isinstance(parent, list) else parent[token]

    final = tokens[-1]
    operation = case["operation"]
    if operation == "append":
        target = parent[int(final)] if isinstance(parent, list) else parent[final]
        assert isinstance(target, list)
        target.append(case["value"])
    elif operation in {"add", "replace"}:
        if isinstance(parent, list):
            parent[int(final)] = case["value"]
        else:
            if operation == "replace":
                assert final in parent
            parent[final] = case["value"]
    else:
        raise AssertionError(f"Unsupported mutation operation: {operation}")


def error_path(error) -> str:
    parts = [str(part).replace("~", "~0").replace("/", "~1") for part in error.absolute_path]
    return "" if not parts else "/" + "/".join(parts)


def test_schema_is_valid_draft_2020_12_schema():
    Draft202012Validator.check_schema(SCHEMA)


def test_draft_fixture_passes_with_format_checks_enabled():
    errors = sorted(validator().iter_errors(VALID_DRAFT), key=lambda error: list(error.path))
    assert errors == []


@pytest.mark.parametrize("case", NEGATIVE_CASES, ids=lambda case: case["case_id"])
def test_negative_mutation_is_rejected_at_declared_boundary(case):
    instance = copy.deepcopy(VALID_DRAFT)
    apply_mutation(instance, case)

    errors = list(validator().iter_errors(instance))
    assert errors, f"Negative case unexpectedly passed: {case['case_id']}"

    matching_path_errors = [
        error for error in errors if error_path(error) == case["expected_error_path"]
    ]
    assert matching_path_errors, (
        f"{case['case_id']} did not fail at {case['expected_error_path']}; "
        f"observed: {[(error_path(error), error.validator) for error in errors]}"
    )

    expected_validator = case.get("expected_validator")
    if expected_validator is not None:
        assert any(error.validator == expected_validator for error in matching_path_errors), (
            f"{case['case_id']} did not produce {expected_validator} at "
            f"{case['expected_error_path']}; observed: "
            f"{[error.validator for error in matching_path_errors]}"
        )


def test_draft_fixture_preserves_required_external_non_claims():
    claims = VALID_DRAFT["boundary"]["external_claims"]
    assert set(claims) == {
        "commission_work_eligibility",
        "evaluator_qualification",
        "testing_program_admission",
    }
    assert all(claim["status"] == "NOT_ESTABLISHED" for claim in claims.values())
    assert all(claim["evidence_refs"] == [] for claim in claims.values())
    assert VALID_DRAFT["boundary"]["packet_confers_authority"] is False
    assert VALID_DRAFT["boundary"]["schema_conformance_is_proof"] is False


def test_draft_fixture_contains_no_execution_or_verification_evidence():
    for collection in (
        "inputs",
        "outputs",
        "runs",
        "observations",
        "findings",
        "mitigations",
        "retests",
        "custody_events",
        "disclosure_events",
        "incidents",
        "manifest",
    ):
        assert VALID_DRAFT[collection] == []

    reconstruction = VALID_DRAFT["independent_reconstruction"]
    assert reconstruction["status"] == "NOT_PERFORMED"
    assert reconstruction["verification_receipt_ref"] is None
    assert VALID_DRAFT["evaluation_conclusion"] == "NOT_EVALUATED"
