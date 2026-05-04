# CI Evidence Bundle v1

## Authority boundary

This contract defines the structure of CI evidence bundles and CI verifier results.

It does not execute workflows, verify artifacts, sign receipts, prove GitHub runner integrity, or assert source-system truth.

## Bundle layout

```text
ci-evidence/
  CI_EVIDENCE.json
  MANIFEST.sha256
  artifacts/
  logs/
```

## Required producer fields

- repo
- commit_sha
- workflow
- run_id
- run_attempt
- job

## Hash rule

All artifact and log records use:

```text
sha256:<64 lowercase hex chars>
```

## Status values

Producer bundle status:

- execution_complete
- execution_failed
- evidence_incomplete

Verifier result status:

- valid
- invalid
- incomplete
- unsupported

## Untracked-file policy

`mode: deny` requires:

```text
allowlist == []
untracked_files == []
```

`mode: allowlisted` allows declared allowlist entries. Actual allowlist membership enforcement belongs to the verifier implementation, not the schema.

## Verification boundary

A schema-valid bundle is not verified evidence.

Verification requires a verifier implementation to load the downloaded bundle, validate schemas, recompute hashes, check manifest entries, detect missing files, and enforce untracked-file policy.
