# External evidence source provenance v0.1

Status: proposed explanatory contract guidance  
Scope: provenance and interpretation of external/third-party evidence sources  
Schema effect: none; this document does not change an existing JSON Schema, enum, fixture, verifier, or receipt contract

## Purpose

WitnessOps may ingest records produced by external systems: scanners, cloud providers, CI systems, decision engines, payment systems, source-control systems, human reviewers, or other observers.

Those records can be useful evidence. They must not silently become stronger claims than the producing mechanism supports.

This document extends the semantic boundary in `RESULT-SEMANTICS.md`:

`provider result != WitnessOps verification of the underlying substantive claim`

## Core invariants

The following are not interchangeable:

```text
provider output
    != adapter coverage
    != source-system truth
    != authority truth
    != execution truth
    != WitnessOps verification
```

Additional invariants:

- A signature's presence does not establish receipt integrity. A successfully executed signature or other integrity check can establish only the integrity properties covered by that named mechanism and its selected trust inputs; it does not establish the truth of the issuer's underlying assertion.
- A provider-reported factor such as `authority_check=pass` remains provider-reported unless a separate authority check was actually performed with retained evidence and a bounded result. Calling that check independent additionally requires explaining the verifier's independence from the relevant provider, authority source, and assertion. Merely naming a mechanism, source, and scope establishes neither execution nor independence.
- An adapter can expose only part of a provider's full input contract. A decision produced through a limited adapter must retain that coverage boundary.
- A provider decision does not establish downstream execution. Execution evidence remains a separate domain.
- Missing, unsupported, unavailable, not-checked, and not-applicable inputs must remain distinguishable.

## Minimum provenance envelope

When an external result is material to a claim, retain enough information to reconstruct what was actually evaluated.

The following fields are the minimum conceptual envelope. This is **not** a machine schema and does not define new required JSON keys yet.

```text
provider
provider_version

adapter
adapter_version

input_contract
input_contract_version
input_scope

authority_source
authority_verification_status

verification_mechanism
verification_scope

receipt_ref
trace_ref
transaction_ref

execution_boundary

establishes
does_not_establish
limitations
```

Fields that do not apply may be omitted or represented according to the governing schema. Absence must not be overloaded to mean unknown, not checked, or not applicable.

## Field semantics

### provider / provider_version

Identifies the system that produced the record and, when known, the relevant version.

This identifies provenance only. It does not establish provider correctness or independence.

### adapter / adapter_version

Identifies the concrete integration surface used to obtain the record.

This matters because different adapters for the same provider may expose different fields, authority inputs, scopes, or execution capabilities.

If the adapter version is unknown, preserve that unknown rather than implying the provider's complete current contract was exercised.

### input_contract / input_contract_version

Names the request or evidence contract presented to the provider.

Examples include an Action Card profile, API revision, scanner profile, event schema, or report format.

### input_scope

Describes the material inputs actually available to the provider for the recorded decision or observation.

If an applicable provider input could not be supplied through the adapter, record the resulting limitation.

### authority_source / authority_verification_status

Describes where authority information came from and whether that authority was independently resolved, provider-resolved, developer-supplied, operator-supplied, unavailable, or otherwise bounded by a named mechanism.

Do not infer authority truth from a generic provider `pass` value. Preserve whether a check actually ran, its result and supporting evidence, and whether independence is established or remains unknown. Provider-controlled or developer/operator-supplied information does not become independent evidence because those fields are populated.

### verification_mechanism / verification_scope

Names the method used to verify the record or claim and its bounded coverage.

This must align with `RESULT-SEMANTICS.md`: verification is valid only under the declared mechanism and mode and does not automatically establish the substantive claim. Retain the executed check's result and evidence; naming a method is not evidence that it ran or passed.

### receipt_ref / trace_ref / transaction_ref

Preserves provider-issued correlation references when available.

A reference establishes linkage to a provider record only to the extent supported by the named retrieval/integrity mechanism.

### execution_boundary

States whether the provider only advised, gated, observed, or also performed execution.

Do not infer execution from policy/decision outputs.

### establishes

A concise bounded statement of what the retained record supports.

Example, when the exchange and integration context have actually been retained:

`The recorded exchange contains provider decision X for input contract Y through adapter Z at the recorded time.`

### does_not_establish

A concise statement of materially adjacent claims the record does not prove.

Example:

`This receipt does not independently establish the truth of the delegated-authority claim.`

### limitations

Records missing coverage, adapter restrictions, unavailable checks, unresolved identity/authority material, stale context, or other interpretation limits.

## Interpretation rules

1. Preserve provider-native decision/factor values as provider observations. A stronger verification claim requires an actually executed check, its evidence and result, and its named mechanism and scope; independence must be established separately.
2. Do not map provider `pass`, `allow`, `approved`, `valid`, or similar labels directly into WitnessOps verification semantics.
3. If an adapter cannot submit an applicable input supported by the provider's fuller contract, record the adapter limitation and do not claim that the fuller provider evaluation occurred.
4. Keep authority, policy, execution, evidence, and verification semantics separate.
5. Preserve retrieval/integrity evidence for provider refs when those refs materially support later reconstruction.
6. Prefer explicit limitation text over a stronger but ambiguous status.
7. A Proofpack or seal may expose gaps; a gap is not a reason to invent or upgrade certainty.

## Generic example

This fictional example combines a provider response with retained local integration context. All names and references below are illustrative, not live evidence or new required schema fields:

```text
provider: example-decision-system
provider_version: unknown
adapter: example-limited-adapter
adapter_version: 0.1
input_contract: example-action-card
input_contract_version: 0.1
input_scope: action summary and evidence/rule references; no delegated-authority packet
request_capture_ref: synthetic://exchange-123/request
response_capture_ref: synthetic://exchange-123/response
adapter_contract_ref: synthetic://example-limited-adapter/0.1

decision: human_review
authority_factor: pass
receipt_ref: provider-receipt-123
authority_verification_status: provider-reported; not independently checked
verification_mechanism: receipt integrity not checked
execution_boundary: decision response only; downstream execution not observed
```

For this example, the retained adapter contract records that the integration cannot submit the provider's fuller delegated-authority packet. The exchange and local context support the interpretation below; the provider's three result fields alone would not.

Safe interpretation:

```text
establishes:
  The retained exchange records a human_review response obtained through
  example-limited-adapter 0.1 for the limited example-action-card 0.1 input.

does_not_establish:
  Receipt integrity or provider/source-system honesty was verified.
  The underlying delegated authority was independently verified.
  The provider evaluated authority fields the adapter could not submit.
  The downstream action executed.
```

Unsafe interpretation:

`WitnessOps verified the agent was authorized.`

## Relationship to existing semantics

This guidance complements:

- evidence epistemic basis and source type;
- the evidence/truth boundary;
- verification result semantics;
- policy decision versus execution result separation.

It does not replace them.

A future schema may represent this provenance as an external-evidence-source object, observation-source metadata, or profile-specific extension. That choice is intentionally deferred.

## Adoption sequence

1. Keep this document as explanatory contract guidance.
2. Identify the smallest existing schema/profile that needs machine-readable external-source provenance.
3. Propose a separate schema revision.
4. Add valid and invalid fixtures demonstrating:
   - limited adapter coverage;
   - unverified/provider-supplied authority;
   - independent authority verification;
   - execution boundary separation;
   - explicit limitations.
5. Add tests proving invalid fixtures fail for the intended reason.
6. Only after the contract settles, update downstream Proofpack/report/UI surfaces.

## Non-goals

This document does not:

- define a universal trust score;
- declare any external provider trustworthy or untrustworthy;
- create a provider dependency;
- define execution behavior;
- authorize production changes;
- make a schema-valid external record substantively true;
- authorize a Proof Seal to imply more than the named verification mechanism supports.
