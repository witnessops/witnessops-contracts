# AGENTS.md

## Identity

This repo is the canonical contract surface for WitnessOps proof runs and bounded evidence packets. It defines structural validity for workflow classes, proof artifacts, evidence manifests, receipts, verifier results, failure states, CI evidence bundles, and evidence-packet profiles.

It is a schema authority only. It is not an execution engine, verifier implementation, signer, customer evidence store, deployment target, or marketing surface.

## Ownership

This repo owns:

- JSON schemas under `schemas/`
- valid and invalid examples under `examples/` and profile fixtures under `fixtures/`
- schema validation tests under `tests/`
- explanatory contract docs under `docs/`
- CI validation for contract fixtures

This repo does not own:

- proof-engine execution
- offline verifier implementation
- source-system adapters
- signing-key custody
- customer evidence custody
- website copy
- live workflow execution
- production deployment

## Non-Negotiable Rules

- Do not change schemas casually; schema edits are contract edits.
- Do not weaken `additionalProperties: false`, required fields, enums, const values, or negative fixtures to make downstream code pass.
- Do not remove invalid fixtures unless replacing them with an equal or stronger negative case.
- Do not describe schema conformance as proof that a workflow happened.
- Do not add execution wrappers, proof-engine generation, signing implementation, verifier implementation, website copy, or private client evidence.
- Do not commit secrets, credentials, private keys, customer records, production evidence, tokens, cloud credentials, or private proof bundles.
- Preserve failure-state language as bounded contract semantics, not as a production incident claim.
- Preserve the AI model evaluation packet's explicit non-claims: schema conformance cannot establish evaluation execution, evaluator qualification or independence, European Commission eligibility, testing-programme admission, evidence truth, or legal compliance.
- Do not promote an AI model evaluation packet past its lifecycle gates by weakening authority, model access, environment, plan-freeze, disclosure, incident-route, custody, or reconstruction requirements.

## Codex Security review

Use [`docs/CODEX_SECURITY_THREAT_MODEL.md`](./docs/CODEX_SECURITY_THREAT_MODEL.md) as the seed context for Codex Security review.

Codex Security may identify findings and propose patches, but it does not authorize merge, release, schema-semantic changes, fixture truth changes, signing authority, verifier behavior changes, proof-engine behavior changes, deploy, or customer-impacting changes.

For security-sensitive changes, preserve these boundaries:

- schemas define structural validity only
- examples prove validator behavior only
- invalid fixtures must fail for the intended reason
- machine-readable evidence-packet profiles must remain aligned with their governing prose boundary and declared lifecycle states
- schema conformance is not proof of source-system honesty, execution, approval, evidence custody, signer authority, or production workflow completion
- contract changes that affect downstream acceptance semantics need explicit maintainer review

## Validation

Install dev dependencies:

```bash
pip install -r requirements-dev.txt
```

Run the contract validation suite:

```bash
pytest -q
```

GitHub Actions runs the same schema test command through `.github/workflows/validate-contracts.yml`.
