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
failure-state schema
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

## Planned structure

```text
schemas/
  workflow-class.schema.json
  proof-run.schema.json
  evidence-manifest.schema.json
  receipt.schema.json
  verifier-result.schema.json
  failure-state.schema.json

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
  test_schema_validation.py
  test_negative_fixtures.py

docs/
  contract-boundaries.md
  outcome-semantics.md
  failure-state-semantics.md

.github/workflows/
  validate-contracts.yml
```

## First gate

```text
CI proves valid fixtures pass and invalid fixtures fail.
```
