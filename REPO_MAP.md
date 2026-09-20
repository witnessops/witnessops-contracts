# Repo Map: witnessops-contracts

## Responsibility

Schema and contract authority for WitnessOps proof artifacts.

## Owns

```text
workflow class schema
proof run schema
evidence manifest schema
receipt schema
verifier result schema
ci evidence bundle schema
ci verifier result schema
failure-state schema
AI model evaluation evidence-packet schema and fixtures
valid and invalid schema fixtures
schema validation CI
```

## Does not own

```text
proof execution
receipt signing implementation
offline verifier implementation
source-system adapters
private client evidence
website copy
```

## Current contract structure

This is a selective orientation map, not an exhaustive file inventory.
Ownership and structural-validity boundaries remain defined in [AGENTS.md](./AGENTS.md).
A listed path is not evidence of execution or independent verification;
inspect the Git tree at the chosen revision for complete tracked-file coverage.

```text
schemas/
  ai-model-evaluation/
    evidence-packet.schema.json
  docs-assistant/
    answer.schema.json
    eval-result.schema.json
    source-manifest.schema.json
  workflow-class.schema.json
  evidence-manifest.schema.json
  receipt.schema.json
  verifier-result.schema.json
  ci-evidence-bundle.schema.json
  ci-verifier-result.schema.json
  failure-state.schema.json
  orchestration-result.schema.json
  package-index.schema.json

fixtures/
  ai-model-evaluation/
    valid/
      evidence-packet.draft.valid.json
    invalid/
      negative-cases.json
  docs-assistant/
    valid/
    invalid/

examples/
  valid/
    workflow-class.privileged-access-approval.json
    evidence-manifest.sample.json
    receipt.sample.json
    verifier-result.sample.json
    failure-state.sample.json
  invalid/
    workflow-class.missing-required-fields.json
    evidence-manifest.missing-artifact-hash.json
    receipt.missing-signature.json
    verifier-result.invalid-outcome.json

tests/
  test_ai_model_evaluation_evidence_packet.py
  test_docs_assistant_schemas.py
  test_host_triage_manifest.py
  test_schema_validation.py

docs/
  CODEX_SECURITY_THREAT_MODEL.md
  ci-evidence-bundle.md
  evidence-packets/
    ai-model-evaluation-evidence-packet-v1.md

.github/workflows/
  validate-contracts.yml
```

## First gate

```text
CI proves valid fixtures pass, negative fixtures fail for their declared boundary, and draft AI model evaluation packets cannot cross execution, authority, disclosure, overclaim, or verification gates without the required records.
```
