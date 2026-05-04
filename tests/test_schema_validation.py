import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SYNTHETIC_WORKFLOW = "privileged_access_approval_synthetic_public_proof_run"
SYNTHETIC_PROOF_RUN_ID = "pr_20260426_synthetic_access_approval_public_001"
SYNTHETIC_EXPECTED_MANIFEST_HASH = "sha256:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
SYNTHETIC_REQUIRED_ARTIFACTS = {
    "access_request",
    "approval_record",
    "execution_log",
    "output_snapshot",
    "boundary_and_failures",
}
SYNTHETIC_ALLOWED_CLAIMS = {
    "synthetic_scope_declared",
    "approval_preceded_execution",
    "prohibited_actions_absent",
}

SCHEMA_FIXTURE_PAIRS = [
    ("workflow-class.schema.json", "workflow-class.privileged-access-approval.json"),
    ("workflow-class.schema.json", "workflow-class.external-ad-exposure-proof-run.json"),
    ("workflow-class.schema.json", "workflow-class.synthetic-access-approval-public-proof-run.json"),
    ("evidence-manifest.schema.json", "evidence-manifest.sample.json"),
    ("evidence-manifest.schema.json", "evidence-manifest.synthetic-access-approval-public-proof-run.json"),
    ("receipt.schema.json", "receipt.sample.json"),
    ("receipt.schema.json", "receipt.synthetic-access-approval-public-proof-run.json"),
    ("verifier-result.schema.json", "verifier-result.sample.json"),
    ("verifier-result.schema.json", "verifier-result.synthetic-access-approval-public-proof-run.json"),
    ("failure-state.schema.json", "failure-state.sample.json"),
    ("package-index.schema.json", "package-index.sample.json"),
    ("ci-evidence-bundle.schema.json", "ci-evidence-bundle.valid.json"),
    ("ci-verifier-result.schema.json", "ci-verifier-result.valid.json"),
]

INVALID_FIXTURE_PAIRS = [
    ("workflow-class.schema.json", "workflow-class.missing-required-fields.json"),
    ("workflow-class.schema.json", "workflow-class.execution-boundary-missing-templates.json"),
    ("evidence-manifest.schema.json", "evidence-manifest.missing-artifact-hash.json"),
    ("receipt.schema.json", "receipt.missing-signature.json"),
    ("verifier-result.schema.json", "verifier-result.invalid-outcome.json"),
    ("ci-evidence-bundle.schema.json", "ci-evidence-bundle.missing-hash.json"),
    ("ci-evidence-bundle.schema.json", "ci-evidence-bundle.bad-sha.json"),
    ("ci-evidence-bundle.schema.json", "ci-evidence-bundle.untracked-file-policy-invalid.json"),
    ("ci-verifier-result.schema.json", "ci-verifier-result.invalid-status.json"),
]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def validator_for(schema_name: str) -> Draft202012Validator:
    schema = load_json(ROOT / "schemas" / schema_name)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def valid_fixture(fixture_name: str):
    return load_json(ROOT / "examples" / "valid" / fixture_name)


def invalid_fixture(fixture_name: str):
    return load_json(ROOT / "examples" / "invalid" / fixture_name)


def synthetic_manifest_artifact_ids(manifest: dict) -> set[str]:
    return {artifact["artifact_id"] for artifact in manifest["artifacts"]}


def validate_synthetic_contract_semantics(manifest: dict, receipt: dict, verifier_result: dict):
    assert manifest["workflow_class"] == SYNTHETIC_WORKFLOW
    assert receipt["workflow_class"] == SYNTHETIC_WORKFLOW
    assert verifier_result["workflow_class"] == SYNTHETIC_WORKFLOW
    assert manifest["proof_run_id"] == SYNTHETIC_PROOF_RUN_ID
    assert receipt["proof_run_id"] == SYNTHETIC_PROOF_RUN_ID
    assert verifier_result["proof_run_id"] == SYNTHETIC_PROOF_RUN_ID

    artifact_ids = synthetic_manifest_artifact_ids(manifest)
    assert SYNTHETIC_REQUIRED_ARTIFACTS.issubset(artifact_ids)

    assert receipt["manifest_hash"] == SYNTHETIC_EXPECTED_MANIFEST_HASH
    assert receipt["result"]["outcome"] == "pass"
    assert receipt["result"]["failure_states"] == []

    for claim in receipt["claims"]:
        assert claim["claim"] in SYNTHETIC_ALLOWED_CLAIMS
        assert set(claim["evidence_refs"]).issubset(artifact_ids)

    assert verifier_result["status"] == "valid"
    assert verifier_result["outcome"] == "pass"
    assert verifier_result["failure_states"] == []


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


def test_synthetic_access_approval_contract_semantics_pass():
    validate_synthetic_contract_semantics(
        valid_fixture("evidence-manifest.synthetic-access-approval-public-proof-run.json"),
        valid_fixture("receipt.synthetic-access-approval-public-proof-run.json"),
        valid_fixture("verifier-result.synthetic-access-approval-public-proof-run.json"),
    )


def test_synthetic_access_approval_missing_approval_fails_semantic_contract():
    manifest = invalid_fixture("synthetic-access-approval.missing-approval-record.json")
    artifact_ids = synthetic_manifest_artifact_ids(manifest)
    assert "approval_record" not in artifact_ids
    assert not SYNTHETIC_REQUIRED_ARTIFACTS.issubset(artifact_ids)


def test_synthetic_access_approval_prohibited_action_fails_semantic_contract():
    receipt = invalid_fixture("synthetic-access-approval.prohibited-action-observed.json")
    claims = {claim["claim"] for claim in receipt["claims"]}
    assert "write_action_observed" in claims
    assert not claims.issubset(SYNTHETIC_ALLOWED_CLAIMS)


def test_synthetic_access_approval_manifest_hash_mismatch_fails_semantic_contract():
    receipt = invalid_fixture("synthetic-access-approval.manifest-hash-mismatch.json")
    assert receipt["manifest_hash"] != SYNTHETIC_EXPECTED_MANIFEST_HASH


def test_ci_evidence_bundle_valid_fixture_declares_deny_untracked_policy():
    bundle = valid_fixture("ci-evidence-bundle.valid.json")
    assert bundle["untracked_file_policy"]["mode"] == "deny"
    assert bundle["untracked_file_policy"]["allowlist"] == []
    assert bundle["untracked_files"] == []
