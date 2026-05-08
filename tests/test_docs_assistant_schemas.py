import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures" / "docs-assistant"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def validator_for(schema_name: str) -> Draft202012Validator:
    schema_path = ROOT / "schemas" / "docs-assistant" / schema_name
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


DOCS_ASSISTANT_VALID_FIXTURES = [
    ("answer.schema.json", "valid/answer.valid.json"),
    ("source-manifest.schema.json", "valid/source-manifest.valid.json"),
    ("eval-result.schema.json", "valid/eval-result.valid.json"),
]


DOCS_ASSISTANT_INVALID_FIXTURES = [
    ("answer.schema.json", "invalid/answer.invalid-status.json"),
    ("answer.schema.json", "invalid/answer.missing-citation-source.json"),
    ("source-manifest.schema.json", "invalid/source-manifest.invalid-hash.json"),
    ("eval-result.schema.json", "invalid/eval-result.invalid-status.json"),
]


@pytest.mark.parametrize(("schema_name", "fixture_name"), DOCS_ASSISTANT_VALID_FIXTURES)
def test_docs_assistant_valid_fixtures_pass(schema_name, fixture_name):
    validator = validator_for(schema_name)
    instance = load_json(FIXTURES / fixture_name)
    assert sorted(validator.iter_errors(instance), key=lambda error: error.path) == []


@pytest.mark.parametrize(("schema_name", "fixture_name"), DOCS_ASSISTANT_INVALID_FIXTURES)
def test_docs_assistant_invalid_fixtures_fail(schema_name, fixture_name):
    validator = validator_for(schema_name)
    instance = load_json(FIXTURES / fixture_name)
    assert sorted(validator.iter_errors(instance), key=lambda error: error.path) != []
