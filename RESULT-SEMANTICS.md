# WitnessOps result semantics

Status: normative semantic baseline for new contract work

Scope: semantic meaning of policy, execution, workflow, check, verification, evidence, and lifecycle fields across WitnessOps contract work.

This document is explanatory contract guidance. It does not change an existing JSON Schema, receipt, manifest, verifier result, fixture, or stored artifact. Existing schemas remain valid at their current revisions. A schema change requires a separate contract edit and review.

## 1. Non-interchangeability invariant

The following domains are independent:

    policy decision
        != execution result
        != workflow outcome
        != check disposition
        != verification result
        != evidence epistemic state
        != artifact lifecycle

A value in one domain must not be inferred from a value in another domain.

In particular:

- allow is not executed.
- deny is not failed.
- pass is not valid.
- valid is not true.
- observed is not verified.
- active is not approved.
- blocked is not failed.

## 2. Policy decision

The shared policy vocabulary for new contract work is:

    allow | deny | require_human

Meanings:

| Value | Meaning |
|---|---|
| allow | The governing policy permits the proposed action within the declared scope. |
| deny | The governing policy does not permit the proposed action. |
| require_human | Autonomous continuation is not authorized; a human must decide, investigate, perform, review, or otherwise satisfy the stated policy condition. |

A policy decision is an authorization result. It is not an execution result.

A policy deny may lead to an execution result of denied, but the values are not aliases. The execution record describes what the executor did; the policy record describes what the policy allowed.

Terms such as block, quarantine, allow_read_only, needs_review, and escalate may remain as policy effects or workflow states where their additional domain meaning is needed. They are not automatic synonyms for the three shared policy decisions.

## 3. Execution result

The execution vocabulary is:

    executed | denied | paused | failed

Meanings:

| Value | Meaning |
|---|---|
| executed | The executor reports that the bounded execution reached its declared terminal execution condition. This does not establish the substantive claim. |
| denied | The execution did not proceed because an authorization or execution gate refused it. |
| paused | Execution is intentionally incomplete and awaits a continuation condition. |
| failed | Execution was attempted but did not reach its declared terminal execution condition. |

Execution result is about the execution attempt. It does not report policy intent, workflow quality, verification, evidence epistemic basis, or artifact lifecycle.

## 4. Workflow outcome

Workflow outcomes describe whether a declared procedure met its own criteria:

    pass | partial | fail | inconclusive | blocked

Meanings:

| Value | Meaning |
|---|---|
| pass | The workflow criteria declared for the bounded procedure were met. |
| partial | Some criteria or evidence were met, but material gaps remain. |
| fail | A required workflow criterion was not met. |
| inconclusive | Available evidence cannot determine pass or fail. |
| blocked | The workflow could not proceed because an authority, scope, dependency, or gate condition was not satisfied. |

The current receipt and verifier schemas use pass, partial, fail, and inconclusive for result.outcome. The workflow-class schema also permits blocked. This document does not alter those schemas.

A workflow pass is not a policy allow, execution success, verification valid, or assertion of substantive truth.

## 5. Check disposition

A check disposition describes one check, not the overall artifact:

    passed | failed | not_checked | not_applicable

Meanings:

| Value | Meaning |
|---|---|
| passed | The applicable check was performed and passed. |
| failed | The applicable check was performed and failed. |
| not_checked | The check applies, but it was not performed. |
| not_applicable | The check does not apply to this object, mechanism, or declared verification mode. |

The current verifier-result schema uses skipped. Until a successor schema is approved, skipped is a legacy representation that must be interpreted as not_checked when the check applies but was not performed.

Skipped must never be mapped to not_applicable merely because the required input was omitted or the verifier chose a limited mode.

## 6. Verification result

Verification results describe a named verification mechanism and mode:

    valid | invalid | incomplete | unsupported | indeterminate

Meanings:

| Value | Meaning |
|---|---|
| valid | All checks required by the declared verification mode passed. |
| invalid | At least one required check was performed and failed. |
| incomplete | A required input or check was unavailable or not performed, so the declared verification scope is incomplete. |
| unsupported | The verifier does not support the declared schema, mechanism, algorithm, or profile. |
| indeterminate | The mechanism ran, but available evidence or trust material cannot determine a valid or invalid result. |

The current verifier-result schema accepts valid, invalid, incomplete, and unsupported. It does not yet accept indeterminate. Adding or removing a machine value requires a later schema revision; this document does not change that schema.

A limited or receipt-only verification mode must preserve its coverage boundary. It must not be reported as valid for checks that were applicable but not performed. An adapter must not silently convert limited-pass, incomplete, or indeterminate into valid.

Verification valid means valid under the declared mechanism and mode. It does not mean that the underlying substantive claim is true.

## 7. Evidence epistemic state

An assertion has two separate properties:

    assertion:
      basis: observed | inferred | assumed | unknown
      source_type: first_party | third_party | operator | system

Basis:

| Value | Meaning |
|---|---|
| observed | Directly captured or directly witnessed evidence supports the assertion. |
| inferred | The assertion is derived from one or more observations or records. |
| assumed | The assertion is accepted as a premise for the bounded procedure but is not established by the retained evidence. |
| unknown | The available material does not establish which basis applies or does not support a conclusion. |

Source type:

| Value | Meaning |
|---|---|
| first_party | The source is the system, owner, or authority directly responsible for the subject. |
| third_party | The source is external to the subject and is not the executing operator. |
| operator | The source is the accountable human operator or reviewer. |
| system | The source is an automated WitnessOps or adjacent system record. |

source_type describes who or what supplied the assertion. It does not establish truth. basis describes how the assertion is known. claim is the assertion subject or content, not an epistemic state.

## 8. Artifact lifecycle

There is no universal lifecycle enum for every WitnessOps object. Where a durable artifact needs a lifecycle, these meanings are available:

    draft | active | deprecated | superseded | retired

Meanings:

| Value | Meaning |
|---|---|
| draft | Work in progress and not yet approved for the stated use. |
| active | Current and available for its declared use. |
| deprecated | Retained for compatibility or history, but new use is discouraged. |
| superseded | Replaced by a named successor. The predecessor remains historical evidence unless separately retired. |
| retired | No longer supported or usable for the stated purpose. |

Profile-specific states such as sample, approved, test, rotated, and revoked remain type-specific. They must not be treated as aliases for execution, verification, or epistemic state.

## 9. Absence and applicability

These meanings are distinct:

| Representation | Meaning |
|---|---|
| absent | The field was not supplied. |
| null | The schema explicitly permits a known no-value. |
| unknown | The value cannot currently be determined. |
| not_checked | An applicable check was not performed. |
| not_applicable | The check or field has no meaning for the object or declared mode. |

Existing schemas may use null or skipped for historical reasons. New contract work must not rely on those values to carry multiple meanings.

## 10. Evidence and truth boundary

The following sequence is intentionally separate:

    operation reported
            ↓
    evidence captured
            ↓
    receipt produced
            ↓
    receipt integrity checked
            ↓
    verification mechanism executed
            ↓
    substantive claim assessed

Interpretation:

1. Operation reported means an actor or system records that an operation occurred.
2. Evidence captured means one or more evidence records were collected and referenced.
3. Receipt produced means a receipt artifact was emitted.
4. Receipt integrity checked means the declared digest, signature, continuity, or structure check passed.
5. Verification mechanism executed means a named verifier ran against a declared scope and mode.
6. Substantive claim assessed means the retained evidence and mechanism support a conclusion about the claim itself.

No earlier stage automatically proves a later stage. In particular:

- A receipt is not evidence that its issuer was truthful merely because its signature is valid.
- A valid receipt is not automatically a valid substantive claim.
- A schema-valid object is not proof that its represented operation happened.
- A producer-local check is not independent verification.
- An observed assertion is not automatically true.

## 11. Legacy mapping rules

These mappings are semantic safeguards, not migration instructions:

| Legacy or overloaded value | Interpretation for new work |
|---|---|
| skip or skipped | not_checked when the check applies but was not performed; never not_applicable |
| not_applicable | Use only when the check genuinely does not apply |
| ok, success, succeeded | No global alias. Interpret only in the owning execution or workflow field |
| pass | Workflow outcome or check result only; never a policy decision or verification verdict |
| valid | Verification result only, with mechanism and mode |
| block | Policy effect or workflow state unless the owning contract explicitly defines it otherwise |
| denied | Execution result, not a synonym for policy deny |
| needs_review, require_approval, require_human | Use require_human for the shared policy decision only when autonomous continuation is not authorized; retain more specific workflow or review meanings elsewhere |
| claim | Assertion subject/content; not an evidence state |

New machine values should use lowercase spellings. Existing fixtures, receipts, and schemas remain unchanged until a separately approved successor contract exists.

## 12. Contract boundary

This document intentionally does not:

- edit receipt.schema.json;
- edit verifier-result.schema.json;
- edit workflow-class.schema.json;
- add a common artifact envelope;
- add recipe identity or recipe version;
- define canonicalization or hashing bytes;
- migrate existing receipts, manifests, fixtures, or evidence;
- propagate fields to other repositories.

Those are separate decisions after result semantics and receipt authority are resolved.
