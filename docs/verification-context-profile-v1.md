# Verification context profile v1

Status: proposed additive receipt profile

`witnessops.verification_context.v1` extends the existing canonical receipt
envelope with the minimum context needed to understand one bounded verification
result. It does not introduce a second claim store, evidence store, receipt
namespace, or verification service.

The existing fields remain authoritative for their current concerns:

- `receipt_version` identifies the envelope contract;
- `workflow_class` and `proof_run_id` identify the bounded run;
- `claims[]` records assessed claims and their evidence references;
- `manifest_hash` binds the separate evidence manifest;
- `signature` binds the complete unsigned receipt envelope.

A profiled receipt declares:

```json
{
  "receipt_version": "witnessops.receipt.v0",
  "receipt_profile": "witnessops.verification_context.v1",
  "verification_context": {
    "subject": {},
    "scope": {},
    "verification_method": {},
    "timestamps": {},
    "limitations": []
  }
}
```

The profile requires all five context fields:

| Field | Purpose |
| --- | --- |
| `subject` | Identifies what the bounded result is about. |
| `scope` | Records included items, criteria, exclusions, and the observation window. |
| `verification_method` | Freezes the named method version, procedure, and pass/fail criteria used for the run. |
| `timestamps` | Separates performance, issuance, and an explicit nullable expiry time. |
| `limitations` | Preserves explicit non-claims and boundaries in the signed envelope. |

## Compatibility behavior

- Existing `witnessops.receipt.v0` receipts remain valid and byte-unchanged.
- A receipt declaring the profile must contain one complete
  `verification_context` object.
- A receipt containing `verification_context` must declare the profile.
- Producers must not emit a partial context.
- Producers and verifiers enforce
  `started_at <= ended_at <= performed_at <= issued_at` and, when expiry is
  present, `issued_at < expires_at`; JSON Schema alone cannot compare values.
- Consumers pinned to the earlier schema should reject the unknown profile until
  they deliberately update; they must not silently ignore it.
- Profiled receipts require a 64-byte Ed25519 signature encoded as lowercase
  hexadecimal. Legacy placeholder fixtures remain valid only without the
  profile.
- Verifiers check the signature over the complete envelope, including
  limitations. Changing a limitation after issuance invalidates the signature.

The separate profile identifier is deliberate. An incompatible local OffSec
bridge already uses `witnessops.receipt.v1`, while public documentation describes
another v2 shape. This change does not claim either version identifier or add a
fifth receipt dialect. Reconciliation and deprecation of those non-canonical
surfaces require a separate compatibility decision.

## Evidence boundary

The profile does not copy raw evidence or evidence metadata into another store.
The existing evidence manifest remains the portable evidence inventory. A claim
continues to reference manifest artifact IDs through `evidence_refs`, and the
receipt continues to bind the manifest through `manifest_hash`.

For a profiled receipt, producers must supply actual manifest artifact IDs for
each claim. A profiled receipt must not use unresolved logical labels as evidence
references.

This preserves reconstructability without embedding private evidence in a
public receipt. A matching hash establishes byte identity for supplied bytes;
it does not establish provenance truth, completeness, or authorization.

## Product boundary

The profile is a verification primitive, not a product catalogue. It does not
create an offer, price, tenant model, dashboard, or customer account. For the
Public Exposure Review, product-specific wording and execution authority remain
in their existing repositories. The receipt records only the bounded subject,
scope, method, timestamps, limitations, result, and evidence references for one
completed review.

## Deliberately deferred

- a successor canonicalization or JWS wire format;
- production signing-key custody;
- public web acceptance of proof-package receipts;
- lifecycle, revocation, or transparency-log contracts;
- tenant identity or database row-level security;
- a new evidence vault or object-storage deployment.

Those concerns require separate compatibility and authority decisions. Schema
conformance alone does not prove execution, evidence truth, signer authority,
or independent verification.
