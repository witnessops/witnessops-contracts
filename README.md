# witnessops-contracts

Canonical contract surface for WitnessOps proof runs.

This repository defines the schemas and validation contracts that decide whether a WitnessOps workflow class, proof run, evidence manifest, receipt, verifier result, and failure state are structurally valid.

## Authority boundary

This repo defines validity. It does not execute proof runs, normalize client evidence, sign receipts, or present marketing copy.
CI evidence contracts define workflow-run evidence structure only. They do not verify runner integrity, sign receipts, or prove semantic correctness of workflow outputs.

| Concern | Owned here? | Notes |
|---|---:|---|
| Workflow class schema | Yes | Defines structure for workflow definitions. |
| Proof run schema | Yes | Defines required run-level fields. |
| Evidence manifest schema | Yes | Defines artifact hash and lineage requirements. |
| Receipt schema | Yes | Defines signed receipt envelope and claim structure. |
| Verifier result schema | Yes | Defines verifier output shape. |
| Failure-state schema | Yes | Defines bounded failure-state records. |
| Engine execution | No | Belongs in `witnessops-proof-engine`. |
| Offline verification implementation | No | Belongs in `witnessops-verifier`. |
| Source-system adapters | No | Belongs in future `witnessops-adapters`. |

## Initial map

```text
witnessops-contracts/
  schemas/
    workflow-class.schema.json
    proof-run.schema.json
    evidence-manifest.schema.json
    receipt.schema.json
    verifier-result.schema.json
    ci-evidence-bundle.schema.json
    ci-verifier-result.schema.json
    failure-state.schema.json
  examples/
    valid/
    invalid/
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

## Outcome semantics

| Outcome | Meaning |
|---|---|
| `pass` | Required evidence exists and checks passed for the bounded run. |
| `partial` | Some evidence exists, but the proof path has material gaps. |
| `fail` | Required proof conditions were not met. |
| `inconclusive` | Evidence is insufficient to determine pass or fail. |

## First workflow target

```text
privileged_access_approval
```

The contract must support a proof run that can answer:

> Was one privileged access event approved, granted as approved, bounded by time, and removed or expired when it should have been?

## Release gates

```text
valid schema fixtures pass
invalid schema fixtures fail
valid receipt fixture validates
receipt missing signature fails
valid manifest fixture validates
manifest missing artifact hash fails
valid verifier result fixture validates
invalid verifier outcome fails
```

## Non-goals for v0

- No dashboard contract.
- No live client integration contract.
- No certification language.
- No broad IAM maturity scoring.
- No claim that a client environment is secure.

## Trust boundary

This repository is a schema authority only. A proof run is not verified merely because it conforms to these schemas. Verification requires a signed receipt, evidence manifest, artifact hashes, and an offline verifier path.
