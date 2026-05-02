import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def get_validator():
    schema = load_json(ROOT / "schemas" / "evidence-manifest.schema.json")
    return Draft202012Validator(schema)


def test_valid_host_triage_manifest_passes():
    validator = get_validator()
    data = load_json(ROOT / "examples" / "valid" / "evidence-manifest.host-triage.json")
    errors = list(validator.iter_errors(data))
    assert errors == []


def test_prohibited_artifact_fails():
    validator = get_validator()
    data = load_json(ROOT / "examples" / "invalid" / "evidence-manifest.host-triage-prohibited.json")
    errors = list(validator.iter_errors(data))
    assert errors != []
