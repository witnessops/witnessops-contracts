import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]

SCHEMA_FIXTURE_PAIRS = [
    ("workflow-class.schema.json", "workflow-class.privileged-access-approval.json"),
    ("workflow-class.schema.json", "workflow-class.external-ad-exposure-proof-run.json"),
    ("evidence-manifest.schema.json", "evidence-manifest.sample.json"),
    ("receipt.schema.json", "receipt.sample.json"),
    ("verifier-result.schema.json", "verifier-result.sample.json"),
    ("failure-state.schema.json", "failure-state.sample.json"),
    ("package-index.schema.json", "package-index.sample.json"),
]

INVALID_FIXTURE_PAIRS = [
    ("workflow-class.schema.json", "workflow-class.missing-required-fields.json"),
    ("workflow-class.schema.json", "workflow-class.execution-boundary-missing-templates.json"),
    ("evidence-manifest.schema.json", "evidence-manifest.missing-artifact-hash.json"),
    ("receipt.schema.json", "receipt.missing-signature.json"),
    ("verifier-result.schema.json", "verifier-result.invalid-outcome.json"),
]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def validator_for(schema_name: str) -> Draft202012Validator:
    schema = load_json(ROOT / "schemas" / schema_name)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


@pytest.mark.parametrize(("schema_name", "fixture_name"), SCHEMA_FIXTURE_PAIRS)
def test_valid_fixtures_pass(schema_name, fixture_name):
    validator = validator_for(schema_name)
    instance = load_json(ROOT / "examples" / "valid" / fixture_name)
    errors = sorted(validator.iter_errors(instance), key=lambda error: error.path)
    assert errors == []


@pytest.mark.parametrize(("schema_name", "fixture_name"), INVALID_FIXTURE_PAIRS)
def test_invalid_fixtures_fail(schema_name, fixture_name):
    validator = validator_for(schema_name)
    instance = load_json(ROOT / "examples" / "invalid" / fixture_name)
    errors = sorted(validator.iter_errors(instance), key=lambda error: error.path)
    assert errors != []
