# Backend MVP v0.1 integration assessment

Status: proposed integration boundary; no deployment or product-authority change

Source artifact: `WitnessOps-backend-mvp-v0.1.0.zip`

Source SHA-256:
`fe889c560ace7b560a8c08922fbb3d7fe1e8654f6b991b00a0140051c8a02543`

## Decision

Use the artifact as design input only. Do not import it as a service or create a
second WitnessOps backend.

WitnessOps already separates the relevant authorities:

| Concern | Current authority |
| --- | --- |
| Public buyer request and verification surfaces | `witnessops-web` |
| Governed review execution and engagement evidence | `witnessops-offsec` |
| Structural receipt/evidence/verifier contracts | `witnessops-contracts` |
| Evidence manifest construction and receipt signing | `witnessops-proof-engine` |
| Canonical internal offline package verification | `witnessops-verifier` |
| Workflow-class definitions | `witnessops-workflow-catalog` |
| Public signing-key lifecycle records | `witnessops-key-registry` |
| Public Exposure Review offer and price | Existing product authority; unchanged by this work |

The source artifact instead combines FastAPI, PostgreSQL, S3-compatible object
storage, OIDC/RBAC, tenant RLS, audit chains, signing, public verification, and
an agent endpoint in one new stack. Importing that stack would duplicate current
authority and deployment surfaces.

## Evidence basis

The current-state statements above are **FACTS** established from these
repository sources; the concept dispositions and integration boundary below are
**DECISIONS** proposed by this change.

| Fact | Repository evidence |
| --- | --- |
| Canonical receipt, evidence-manifest, and verifier-result shapes live in the contracts repository. | `witnessops-contracts/schemas/receipt.schema.json`, `schemas/evidence-manifest.schema.json`, `schemas/verifier-result.schema.json` |
| Receipt construction and signing are producer responsibilities, not independent verification. | `witnessops-proof-engine/proof_engine/sign_receipt.py`, `AGENTS.md`, `docs/verifier-compatibility.md` |
| The offline verifier owns independent package checks. | `witnessops-verifier/verifier/witnessops_verify.py`, `verifier/verify_signature.py`, `verifier/verify_manifest.py`, `verifier/verify_artifacts.py`, `verifier/verify_schema.py` |
| Workflow definitions and public-key trust inputs remain separate authorities. | `witnessops-workflow-catalog/indexes/workflow-index.json`, `witnessops-key-registry/manifests/key-registry.manifest.json` |
| Public Exposure Review offer, intake, and receipt-only web verification are existing web authority. | `witnessops-web/apps/witnessops-web/src/lib/buyer-services.ts`, `docs/commercial/10-public-exposure-review-offer.md`, `apps/witnessops-web/src/app/api/verify/route.ts`, `packages/proof/src/receipt/verify-receipt.ts` |
| Public Exposure Review execution scope and engagement evidence are governed outside the web and proof-engine repositories. | `witnessops-offsec/automation/contracts/external-exposure-assessment.v1.json`, repository `AGENTS.md` |
| The candidate is a complete competing runtime rather than a portable primitive. | Source artifact `src/witnessops/main.py`, `routes.py`, `services.py`, `models.py`, `storage.py`, `auth.py`, `docker-compose.yml` |

Production key-custody activation, a reconciled receipt lifecycle, and a
canonical Public Exposure Review package adapter remain **UNKNOWN/UNIMPLEMENTED**
in the inspected canonical path. This proposal does not infer them from public
copy or producer-side verification output.

## Current state and gaps

Current implementation already provides:

- a request path and primary Public Exposure Review buyer workflow;
- engagement-local scope and evidence controls;
- a canonical receipt schema with claims and evidence references;
- SHA-256 evidence manifests;
- deterministic producer-side receipt construction;
- Ed25519 receipt signing;
- an offline verifier for signature, manifest, artifact, schema, and optional
  key-registry checks;
- a public `/verify` page and `/api/verify` receipt-only boundary.

Material gaps relevant to this integration are:

1. The canonical proof-package receipt does not yet carry a profiled subject,
   event-specific scope, method version, timestamps, or explicit limitations.
2. The public web receipt console currently accepts other receipt lanes and must
   not be described as a proof-package verification path for this schema.
3. Production signing-key custody remains outside the proof engine.
4. Public Exposure Review evidence still needs a deliberately bounded adapter
   from the governed engagement output into the proof package; the proof engine
   must not become a scanner or source-system executor.
5. The existing catalogue's `external_ad_exposure_proof_run` includes AD/SMB
   and credential-oriented semantics and is not the Public Exposure Review
   contract; reusing it would widen the current unauthenticated outside-in
   offer.

## Concept disposition

| Candidate concept | Decision | Integration rationale |
| --- | --- | --- |
| Trust Receipt Engine | **ADAPT** | Keep the existing contracts → proof engine → offline verifier composition. Do not adopt the candidate service boundary. |
| Receipt schema | **ADAPT** | Add an explicit verification-context profile to the canonical envelope. Keep existing claims, manifest binding, result, and signature fields. Do not claim the conflicting local v1 or documented v2 identifiers. |
| Claim model | **ADAPT** | Keep `claims[]` in the signed receipt. Do not add generic organization/claim CRUD or a mutable claim database. |
| Evidence model | **ADAPT** | Keep evidence bytes outside the receipt and bind existing manifest artifact IDs and hashes. Do not import the candidate evidence vault. |
| Verification method | **ADOPT** | Freeze method ID, version, procedure, pass criteria, and fail criteria in the signed context. |
| Scope | **ADOPT** | Freeze included items, criteria, exclusions, and the observation window in the signed context. |
| Limitations | **ADOPT** | Require explicit limitations in the profile and bind their exact values through the signature. Do not silently append or rewrite them. |
| Timestamps | **ADAPT** | Use one `timestamps` object with performed, issued, and explicit nullable expiry fields; reject the candidate's duplicate timestamp aliases. |
| Signatures | **ADAPT** | Retain current Ed25519 signing and fail-closed verifier behavior. Defer an RFC 8785/JWS wire-format migration to a successor contract. |
| Verification endpoint | **DEFER** | Reuse the existing web surface only after a separate adapter preserves receipt-only versus bundle-complete semantics. Do not add a FastAPI endpoint. |
| Evidence hashing | **ADOPT** | Retain SHA-256 file hashes and the receipt-to-manifest hash binding. Salted public commitments are unnecessary until a disclosed low-entropy evidence case requires them. |
| Audit/event history | **DEFER** | Reconcile with the existing event ledger before defining a receipt lifecycle or another hash chain. |
| Tenant boundaries | **REJECT** | Do not add OIDC, tenant CRUD, RLS, or user roles to this primitive. They are a separate SaaS/product decision. |
| Storage model | **REJECT** | Do not add PostgreSQL, MinIO/S3, application encryption, or retention workers. Preserve existing evidence custody and deployment. |

## Recommended integration boundary

```text
existing Public Exposure Review request
  → governed scoped review in the existing execution authority
  → selected/redacted evidence package
  → witnessops-proof-engine result + signed profiled receipt
  → witnessops-verifier independent package result
  → existing public verification surface after a separate compatible adapter
```

The Public Exposure Review remains the primary workflow. This integration does
not create offers, change pricing, widen scope, or alter payment behavior.

## Implementation plan

### Repository: `witnessops-contracts`

- add the explicit verification-context profile and complete context shape;
- retain v0 fixture validity;
- add valid and negative profile fixtures;
- document authority and migration boundaries.

### Repository: `witnessops-proof-engine`

- allow `build_receipt` to accept one complete verification context;
- emit the profile only when all context fields and resolvable evidence
  references are supplied;
- preserve exact limitations without implicit additions;
- test deterministic generation, evidence-reference reconstructability, and
  signature coverage of the context.

### Repository: `witnessops-verifier`

- update the mechanically pinned packaged receipt schema after the contract
  change;
- prove a profiled package verifies deterministically;
- prove limitation or evidence tampering fails verification.

### Repository: `witnessops-web`

No code change in this phase. Its instructions keep `/verify` receipt-only and
forbid silently widening into proof-bundle verification. A later PR must define
the adapter result as incomplete/indeterminate when artifacts or trust sources
were not independently checked.

### Repository: `witnessops-offsec`

No code change in this phase. Execution and evidence capture remain governed by
its existing scope and engagement boundaries.

## Migration and compatibility risks

| Risk | Control |
| --- | --- |
| Existing v0 receipts stop validating | Conditional profile requirements; retain and test v0 fixtures unchanged. |
| Partial context is signed | Proof-engine accepts the profile only as one complete field set; canonical schema requires all five fields. |
| Limitations are weakened after issuance | Signature covers the complete unsigned envelope; tamper test must fail. |
| Evidence becomes non-reconstructable | Claims continue to reference manifest artifact IDs; manifest retains paths and SHA-256 hashes. |
| Web overstates receipt-only checks | Defer the web adapter and preserve explicit incomplete/indeterminate semantics. |
| New service or deployment drift | No API service, database, object store, tenant model, DNS, secret, or deployment change. |
| Receipt namespace collision creates another dialect | Use a separate profile identifier on the canonical envelope; do not claim the incompatible OffSec v1 or documented web v2. |
| Canonicalization migration breaks signatures | Keep the current wire format in this phase; address JWS/RFC 8785 only in a versioned successor. |

## Source artifact limits

The candidate contains useful test ideas, but its PostgreSQL RLS, runtime roles,
triggers, and object-store behavior are not exercised by its SQLite/in-memory
test harness. Its issuance path also does not validate generated output against
its published JSON Schema. Those gaps reinforce the decision to extract only
bounded contract concepts, not runtime code or infrastructure.
