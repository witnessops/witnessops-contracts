# Codex Security Threat Model — witnessops-contracts

Status: `repo_prep_seed_for_codex_security`

This document is a repository-specific seed for Codex Security review and GitHub PR review. It is not a vulnerability report, not a scan result, and not proof that any production workflow occurred.

## Scope

This repository is the canonical contract surface for WitnessOps proof runs.

It owns structural validity for:

- workflow classes
- proof runs
- evidence manifests
- receipts
- verifier results
- failure states
- valid examples
- invalid examples
- schema validation tests
- explanatory contract documentation

## Out of scope

This repository does not own:

- proof-engine execution
- offline verifier implementation
- source-system adapters
- signing-key custody
- customer evidence custody
- website copy
- live workflow execution
- production deployment
- private client evidence
- production proof claims

Do not infer that a passing Codex Security review verifies any out-of-scope system.

## Authority boundaries

- `main` in `witnessops/witnessops-contracts` is the code authority for schemas, examples, and schema tests.
- `schemas/` defines structural validity.
- `examples/valid/` and `examples/invalid/` prove expected validator behavior.
- `pytest -q` is the deterministic validation command observed for this repo.
- Codex Security may identify findings and suggest patches.
- Codex Security findings do not authorize merge, release, schema-semantic changes, fixture truth changes, signing authority, verifier behavior changes, proof-engine behavior changes, deploy, or customer-impacting changes.
- Human maintainer review remains required for any change that affects schema acceptance, negative fixture behavior, outcome semantics, failure-state semantics, receipt structure, evidence lineage, verifier-result shape, or downstream compatibility.

## Primary review surfaces

Treat the following as first-class review surfaces:

1. `schemas/`
   - required fields
   - `additionalProperties` boundaries
   - enum and const values
   - artifact hash and lineage requirements
   - receipt envelope and claim structure
   - verifier output shape
   - failure-state record shape
   - workflow execution boundaries

2. `examples/valid/`
   - positive fixtures that must validate
   - sample semantic boundaries
   - no real customer data or private evidence

3. `examples/invalid/`
   - negative fixtures that must fail
   - fixture names and failure intent
   - coverage for malformed or missing required fields

4. `tests/`
   - positive fixture validation
   - negative fixture rejection
   - exact schema/fixture pairing

5. `.github/workflows/validate-contracts.yml`
   - deterministic schema-test execution
   - no secrets or external system dependency

6. `docs/`
   - contract boundaries
   - outcome semantics
   - failure-state semantics
   - no production proof overclaims

## Untrusted inputs

Review all handling of:

- JSON schemas
- valid fixtures
- invalid fixtures
- receipt examples
- evidence manifests
- verifier result examples
- workflow class examples
- failure-state examples
- artifact path strings
- hash fields
- signer or key-reference fields
- proof-run identifiers
- any fixture value that resembles a real secret, credential, customer record, private key, token, production target, internal custody path, or private evidence path

## Security invariants

The following must remain true unless an explicit design change is reviewed and approved:

- Schema conformance is structural validity only; it is not proof that a workflow happened.
- Schema conformance does not prove source-system honesty, execution, approval, evidence custody, signer authority, or production workflow completion.
- Required fields must not be removed to make downstream code easier.
- `additionalProperties: false` boundaries must not be weakened without explicit compatibility rationale.
- Enums and const values must not be widened without clear downstream acceptance review.
- Invalid fixtures must remain invalid and must fail for the intended class of reason.
- Valid fixtures must not include real customer data, private evidence, credentials, signing keys, tokens, or production material.
- Receipt schema changes must preserve the distinction between declared claims, signed envelopes, evidence references, and verification output.
- Evidence manifest schema changes must preserve artifact hash, lineage, and portability requirements.
- Verifier-result schema changes must preserve bounded outcome semantics and failure visibility.
- Failure-state schema changes must preserve explicit blocked, partial, failed, or inconclusive language where applicable.

## High-priority finding classes

Treat the following as P1 for review purposes:

- schema accepts missing or malformed required proof material as valid
- schema permits undeclared fields that can smuggle authority, evidence, signer, or verifier claims
- invalid fixtures accidentally validate
- valid fixtures contain secrets, credentials, private keys, customer data, production evidence, tokens, or internal custody paths
- receipt schema weakens signature, claim, or evidence-reference requirements
- evidence manifest schema weakens artifact hash or lineage requirements
- verifier-result schema collapses pass/partial/fail/inconclusive/blocked semantics
- workflow-class schema allows execution boundaries to be omitted where downstream systems rely on them
- outcome or failure-state semantics allow unproven conditions to be presented as verified
- CI validation stops proving both valid fixtures pass and invalid fixtures fail

## Lower-priority but relevant finding classes

Review but do not automatically treat as P1 without demonstrated impact:

- cosmetic docs edits that preserve contract boundaries
- dependency advisories not reachable through schema validation
- missing web-app security headers, because this repo is not a web app
- broad performance concerns without a concrete schema-validation amplification path

## Review instructions for Codex

When reviewing this repository:

- prefer small, surgical findings over broad refactors
- name the affected schema, fixture, test, or doc
- include a concrete acceptance-bypass, overclaim, or schema-drift path where possible
- do not weaken schemas or negative fixtures to make downstream code pass
- do not add execution wrappers, proof-engine behavior, verifier behavior, signing behavior, website copy, or private evidence
- do not add production credentials, signing keys, customer evidence, or private proof bundles as fixtures
- preserve the distinction between contract validity, execution, evidence, signing, verification, and presentation
- preserve `pytest -q` as the baseline validation command unless a separate tooling lane changes it

## Suggested Codex Security scan configuration

Initial scan seed:

- repository: `witnessops/witnessops-contracts`
- branch: `main`
- history window: `180 days`
- environment family: `Python / JSON Schema`
- setup command: `pip install -r requirements-dev.txt`
- validation command for proposed patches: `pytest -q`
- agent secrets: none
- production credentials: prohibited
- customer data fixtures: prohibited
- private proof bundles: prohibited
- schema-semantic rewrites without maintainer authority: prohibited

## Closure condition for this prep artifact

This prep artifact is sufficient when:

- Codex Security scan context can be seeded from this file.
- `AGENTS.md` points reviewers to this file.
- A private-reporting `SECURITY.md` exists for the repo.
- No schema files, valid fixtures, invalid fixtures, schema tests, workflow behavior, verifier behavior, proof-engine behavior, production settings, secrets, customer evidence, or proof claims were changed by this prep pass.
