# Security scan orchestrator evidence contract v1

## Status and authority

This contract defines the structural shape of Security CLI scan-orchestrator
run state and normalized observed findings. It does not define execution order,
authorize a scan, grant cloud access, select a target, establish scanner
completion, validate a finding, approve remediation, merge code, or deploy.

Runtime authorization and execution behavior remain owned by
`witnessops/witnessops-security-cli`. This repository is the schema authority
for the resulting evidence records only.

## Schemas

- `schemas/security-scan/orchestrator-run.schema.json` validates `state.json`.
- `schemas/security-scan/normalized-findings.schema.json` validates
  `findings.normalized.json`.

The run record pins the runtime contract identity and digest together with the
exact contracts repository commit, paths, and schema digests. A consumer must
check those pins against the schema bytes it actually uses.

## Security properties

- Unknown top-level fields are rejected.
- Backend, ownership, status, severity, and confidence values are closed enums.
- A terminal run requires an end timestamp; an active run requires `null`.
- Native handoff claim tokens may only appear as the literal `[withheld]`.
- Finding provenance is mandatory and artifact paths are confined below one
  declared backend directory without parent traversal.
- Findings remain `observed`; structural conformance does not promote them to
  verified, accepted, fixed, or production-impacting.

## Cross-record semantics

JSON Schema validates individual files. The producer must additionally test
that effective backends are a subset of requested backends, every finding
backend is effective, every referenced artifact exists beneath the same run
directory, and the recorded schema digests match the vendored bytes.

Those checks validate internal consistency only. They do not prove source-system
honesty, operator authorization, cloud-account status, execution completeness,
finding truth, or independent review.
