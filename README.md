# witnessops-contracts

Canonical contract surface for WitnessOps proof runs and bounded evidence packets.

This repository defines the schemas and validation contracts that decide whether WitnessOps workflow classes, proof artifacts, receipts, verifier results, failure states, CI evidence bundles, and bounded evidence packets are structurally valid.

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
| AI model evaluation evidence-packet contract | Yes | Defines the structural core, lifecycle gates, explicit non-claims, and fixture corpus for a bounded evaluation evidence packet. |
| Engine execution | No | Belongs in `witnessops-proof-engine`. |
| Offline verification implementation | No | Belongs in `witnessops-verifier`. |
| Source-system adapters | No | Belongs in future `witnessops-adapters`. |

## Initial map

```text
witnessops-contracts/
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
  fixtures/
    ai-model-evaluation/
      valid/
        evidence-packet.draft.valid.json
      invalid/
        negative-cases.json
  examples/
    valid/
    invalid/
  tests/
    test_ai_model_evaluation_evidence_packet.py
    test_schema_validation.py
  docs/
    evidence-packets/
      ai-model-evaluation-evidence-packet-v1.md
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
AI model evaluation draft fixture validates
draft execution, unsupported overclaims, unfrozen-plan promotion, unauthorized disclosure, malformed hashes, and receipt-free reconstruction fail
```

## Non-goals for v0

- No dashboard contract.
- No live client integration contract.
- No certification language.
- No broad IAM maturity scoring.
- No claim that a client environment is secure.

## Trust boundary

This repository is a schema authority only. A proof run or evidence packet is not verified merely because it conforms to these schemas. Conformance does not establish execution, authority, evaluator qualification or independence, Commission-work eligibility, programme admission, artifact integrity, custody continuity, or legal compliance. Those conclusions require the named evidence and an independent verifier path.
