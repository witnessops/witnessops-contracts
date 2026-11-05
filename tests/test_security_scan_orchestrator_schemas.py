import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = ROOT / "schemas" / "security-scan"
FIXTURE_ROOT = ROOT / "fixtures" / "security-scan"

VALID_FIXTURES = [
    ("orchestrator-run.schema.json", "orchestrator-run.blocked.valid.json"),
    ("orchestrator-run.schema.json", "orchestrator-run.pass-with-findings.valid.json"),
    ("normalized-findings.schema.json", "normalized-findings.valid.json"),
]

INVALID_FIXTURES = [
    ("orchestrator-run.schema.json", "orchestrator-run.missing-schema-pin.json"),
    ("orchestrator-run.schema.json", "orchestrator-run.running-with-ended-at.json"),
    ("normalized-findings.schema.json", "normalized-findings.missing-provenance.json"),
    ("normalized-findings.schema.json", "normalized-findings.path-traversal.json"),
]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validator_for(schema_name: str) -> Draft202012Validator:
    schema = load_json(SCHEMA_ROOT / schema_name)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


@pytest.mark.parametrize(("schema_name", "fixture_name"), VALID_FIXTURES)
def test_valid_security_scan_fixtures_pass(schema_name, fixture_name):
    validator = validator_for(schema_name)
    instance = load_json(FIXTURE_ROOT / "valid" / fixture_name)
    assert list(validator.iter_errors(instance)) == []


@pytest.mark.parametrize(("schema_name", "fixture_name"), INVALID_FIXTURES)
def test_invalid_security_scan_fixtures_fail(schema_name, fixture_name):
    validator = validator_for(schema_name)
    instance = load_json(FIXTURE_ROOT / "invalid" / fixture_name)
    assert list(validator.iter_errors(instance)) != []
