# AI_MODEL_EVALUATION_EVIDENCE_PACKET_V1

## Document control

| Field | Value |
|---|---|
| Document ID | `AI_MODEL_EVALUATION_EVIDENCE_PACKET_V1` |
| Version | `0.1-draft` |
| Status | `DRAFT_TEMPLATE_NOT_EXECUTED` |
| Owner | WitnessOps |
| Intended use | Bounded evidence packet for an authorized AI model evaluation |
| Generated | 2026-07-10 |
| Governing principle | An independent verifier must be able to reconstruct the authority, access boundary, plan, execution, evidence, findings, mitigation, custody, and conclusion without trusting WitnessOps or the evaluator |
| Authority conferred by this document | None |

## Decision

`DRAFT_PACKET_CONTRACT_COMPLETE_EXECUTION_NOT_AUTHORIZED`

This document defines the minimum records and verification procedure for a future AI model evaluation evidence packet. It does not record an evaluation, appoint an evaluator, authorize access to a model, establish evaluator independence, or support a safety, security, compliance, certification, or eligibility conclusion.

## Mandatory boundary and non-claims

The following statements are authoritative for this draft:

1. The referenced policy context does not establish that WitnessOps is eligible for European Commission work.
2. It does not establish that WitnessOps is qualified as an AI evaluator.
3. It does not establish that WitnessOps is independent of any model provider, deployer, buyer, regulator, or evaluation principal.
4. It does not establish that WitnessOps has been admitted to a testing programme, regulatory sandbox, secure testing facility, procurement framework, grant consortium, or model-access programme.
5. No model evaluation has been performed under this packet.
6. No model, weights, endpoint, system prompt, confidential documentation, customer data, personal data, credential, or secret has been supplied or accessed under this packet.
7. A completed packet may prove only the bounded claims supported by its named artifacts, signatures, integrity records, custody events, and verifier procedure.
8. A passing evaluation is not, by itself, proof of legal compliance, model safety, absence of undiscovered risk, fitness for every use, or regulatory acceptance.

Any external presentation of this packet MUST retain this boundary or include an integrity-linked boundary statement with equivalent semantics.

## 1. Purpose and proof target

The packet is designed to support this narrow proof target:

> A named evaluator, acting under a recorded authority and declared access boundary, executed a frozen evaluation plan in a described environment; preserved input, output, finding, mitigation, retest, custody, and disclosure lineage; and produced evidence that a named verifier can inspect or reconstruct.

The packet separates:

| Layer | Record produced | What it may establish |
|---|---|---|
| Authority | Evaluation mandate and scope | Who authorized which evaluation actions |
| Execution | Plan, environment, tools, runs | What was intended and what executed |
| Evidence | Inputs, outputs, logs, hashes, observations | What artifacts were captured |
| Findings | Finding records and claim boundaries | How evidence was interpreted |
| Mitigation | Change and retest records | What changed and what was retested |
| Custody | Append-only custody events | Who controlled evidence and when |
| Disclosure | Release decisions and redaction map | What was disclosed, to whom, and why |
| Verification | Reconstruction receipt | What an independent verifier could establish |
| Governance | Challenges, incidents, supersession | How disputes and later changes are handled |

No layer may silently substitute for another. In particular, an execution log is not an authority record, a finding is not a verified fact, a hash is not proof of truthful capture, and a self-declaration is not independent confirmation.

## 2. Packet states

Exactly one packet state MUST be current:

| State | Meaning |
|---|---|
| `DRAFT_TEMPLATE` | Structure exists; no evaluation-specific authority exists |
| `PREPARED_UNAUTHORIZED` | Evaluation-specific records are being assembled; execution is blocked |
| `AUTHORIZED_NOT_STARTED` | Mandate and prerequisites are admitted; no evaluation run has started |
| `IN_PROGRESS` | Authorized evaluation execution is underway |
| `PAUSED` | Execution is suspended without closing the packet |
| `CLOSED` | Evaluation and required closure checks are complete |
| `CLOSED_WITH_GAPS` | Evaluation ended with explicit unresolved gaps |
| `ABORTED` | Execution stopped under a named stop condition |
| `SUPERSEDED` | A later packet replaces this packet without deleting its history |
| `WITHDRAWN` | The principal withdrew authority; retained evidence remains governed |

State changes MUST be recorded as append-only events with timestamp, actor, authority reference, previous state, new state, reason, and event artifact hash.

## 3. Canonical identifiers and integrity rules

### 3.1 Identifier classes

| Record | Prefix | Example |
|---|---|---|
| Packet | `AIMEP` | `AIMEP-2026-0001` |
| Authority | `AUTH` | `AUTH-0001` |
| Evaluator | `EVALR` | `EVALR-0001` |
| Model/access boundary | `MODEL` | `MODEL-0001` |
| Environment | `ENV` | `ENV-0001` |
| Tool | `TOOL` | `TOOL-0001` |
| Evaluation plan | `PLAN` | `PLAN-0001` |
| Acceptance criterion | `CRIT` | `CRIT-0001` |
| Run | `RUN` | `RUN-0001` |
| Input | `INPUT` | `INPUT-0001` |
| Output | `OUTPUT` | `OUTPUT-0001` |
| Observation | `OBS` | `OBS-0001` |
| Finding | `FIND` | `FIND-0001` |
| Mitigation | `MIT` | `MIT-0001` |
| Retest | `RETEST` | `RETEST-0001` |
| Custody event | `CUST` | `CUST-0001` |
| Disclosure event | `DISC` | `DISC-0001` |
| Incident | `INC` | `INC-0001` |
| Challenge | `CHAL` | `CHAL-0001` |
| Verification receipt | `VER` | `VER-0001` |

Identifiers are immutable within a packet. A corrected record receives a new version or identifier and retains a `supersedes` link to the earlier record.

### 3.2 Time format

All machine-readable timestamps MUST use RFC 3339 UTC with a `Z` suffix. Local time may be recorded only as supplementary presentation data with an explicit IANA timezone.

### 3.3 Hash format

- Artifact hashes MUST use `sha256:<64 lowercase hexadecimal characters>` unless the packet profile explicitly defines an additional algorithm.
- Hashes cover the exact bytes stored. No unrecorded whitespace, newline, encoding, archive, or JSON normalization is permitted.
- If canonical JSON is required, the producer MUST materialize canonical RFC 8785 JSON bytes as the stored artifact and hash those bytes.
- A hash establishes byte identity only. It does not prove authorship, truthful capture, authority, completeness, or time of existence.

### 3.4 Signature and timestamp profile

The packet manifest MUST declare:

| Field | Requirement |
|---|---|
| `signature_profile_id` | Named profile or `NONE` |
| `signing_identity_ref` | Identity and authority record for signer |
| `signature_artifact_ref` | Detached or enveloped signature evidence |
| `verification_method_ref` | Verifier and key-resolution procedure |
| `timestamp_profile_id` | Named profile or `NONE` |
| `timestamp_artifact_ref` | Timestamp token or anchoring receipt |
| `trusted_time_source` | Source and uncertainty statement |

No packet may describe itself as signed, timestamped, or anchored unless the corresponding artifact and verification procedure are present.

## 4. Evaluator identity, independence, and authority

### 4.1 Role registry

Every person or organization acting in the evaluation MUST appear in the role registry.

| Role | Minimum responsibility | May be combined? |
|---|---|---|
| Evaluation principal | Defines purpose and grants bounded authority | Not with independent verifier without disclosed conflict |
| Model provider/custodian | Controls model or access path | Not presumed independent |
| Lead evaluator | Directs authorized evaluation execution | Yes, with evidence producer if declared |
| Evaluation operator | Executes tests and records runs | Yes |
| Evidence custodian | Controls packet evidence and disclosure | Prefer separate from model provider |
| Finding reviewer | Reviews evidence-to-finding reasoning | May be independent or internal; status must be explicit |
| Mitigation owner | Authorizes or implements changes | Normally provider or system owner |
| Incident owner | Classifies and routes potential incidents | Must have named authority source |
| Independent verifier | Reconstructs the packet and issues `VER-*` | Must not verify their own unreviewed execution |
| Disclosure authority | Approves release, redaction, or recipient access | Must be named before disclosure |

### 4.2 Evaluator identity record

Each `EVALR-*` record MUST contain:

| Field | Required content |
|---|---|
| `evaluator_record_id` | Immutable evaluator record identifier |
| `legal_identity` | Legal person or organization; restricted copy permitted |
| `public_identity` | Publicly disclosable name or role label |
| `jurisdiction` | Incorporation/residence jurisdiction relevant to authority |
| `organization_identifier` | Registration or validated identifier, or `UNRESOLVED` |
| `individual_roles` | Named operators and role assignments |
| `identity_evidence_refs` | Evidence used to bind identity to records/signatures |
| `competence_claims` | Bounded capabilities claimed by evaluator |
| `competence_evidence_refs` | Prior work, qualifications, methods, or test evidence |
| `limitations` | Areas the evaluator is not qualified or authorized to assess |
| `signature_identity_ref` | Key or signature identity resolution record |
| `disclosure_class` | Public, controlled, restricted, or highly restricted |

The packet MUST distinguish claimed competence from independently checked competence.

### 4.3 Independence declaration

The evaluator MUST issue an independence declaration covering, at minimum:

- current and recent employment or contractual relationships with the principal, model provider, deployer, and material beneficiaries;
- ownership, investment, revenue dependence, grants, gifts, or other financial interests;
- involvement in model training, architecture, safety decisions, deployment, procurement, or prior approval;
- result-contingent compensation or incentives;
- control over test selection, acceptance thresholds, evidence exclusion, publication, or finding closure;
- reliance on provider-selected data, tools, environments, or personnel;
- access restrictions that could bias the evaluation;
- personal, institutional, competitive, or political conflicts;
- prior statements or commitments that could impair impartiality;
- recusal decisions and replacement arrangements;
- any confidentiality term that restricts truthful reporting to the principal or competent authority.

The declaration MUST end with one status:

| Status | Meaning |
|---|---|
| `DECLARED_INDEPENDENT` | Evaluator declares no material conflict |
| `DECLARED_INDEPENDENT_WITH_CONSTRAINTS` | Constraints are disclosed and bounded |
| `NOT_INDEPENDENT` | Evaluation is internal, provider-controlled, or materially conflicted |
| `INDEPENDENCE_UNRESOLVED` | Evidence is insufficient for a conclusion |

An independence declaration proves only that the declaration was made. The independent verifier MUST separately record whether the declaration is corroborated, contradicted, or unresolved.

### 4.4 Authority source

The `AUTH-*` record MUST identify:

| Field | Requirement |
|---|---|
| Principal | Person or body granting authority |
| Principal authority source | Contract, law, delegation, programme rule, board decision, owner authorization, or other source |
| Evaluator appointment | Instrument appointing the evaluator |
| Authorized model/system | Exact model and access boundary |
| Authorized methods | Tests, tools, data classes, interaction types, and limits |
| Prohibited actions | Explicitly blocked methods and data handling |
| Time window | Start, expiry, and revocation conditions |
| Geographic/jurisdiction boundary | Where execution and data handling may occur |
| Safety constraints | Rate, compute, network, human-subject, physical, and operational limits |
| Disclosure authority | Who may receive which results |
| Incident authority | Who classifies and reports potential incidents |
| Stop authority | Who may pause or terminate execution |
| Evidence refs | Signed mandate and supporting authority records |

If the principal's authority over the model, system, data, or environment is unresolved, packet state MUST remain `PREPARED_UNAUTHORIZED`.

## 5. Model, version, and access boundary

The `MODEL-*` record MUST prevent a result from silently expanding beyond the model and access actually tested.

### 5.1 Model identity

| Field | Required content |
|---|---|
| Provider | Named provider or custodian |
| Model family | Public or internal family name |
| Model/version identifier | Exact endpoint, release, checkpoint, build, or provider version |
| Model artifact hash | Hash when weights/artifact are available; otherwise `NOT_AVAILABLE` with reason |
| Release status | Pre-release, production, research, fine-tuned, quantized, distilled, or other |
| Evaluation-relevant configuration | System prompt, policy layer, decoding, tools, retrieval, memory, guardrails, and adapters where accessible |
| Evaluation dates | First and last access timestamps |
| Provider change controls | Evidence that version remained stable, or a recorded version-change event |

### 5.2 Access boundary

| Boundary field | Examples of values |
|---|---|
| Access mode | API, hosted UI, controlled terminal, local weights, white-box, grey-box, black-box |
| Weight access | Full, partial, none |
| Gradient/activation access | Full, partial, none |
| System-prompt access | Full, redacted, none |
| Safety-layer visibility | Full, described only, none |
| Log access | Request/response, token log, tool trace, internal trace, none |
| Tool access | Named tools and versions |
| Network access | Isolated, allowlisted, unrestricted, unknown |
| Rate/compute limits | Exact limits or unknown |
| Content filtering | Mechanism and visibility |
| Provider monitoring | Declared monitoring and effect on behavior |
| Data retention | Provider retention terms and evidence |
| Geography | Processing and storage regions where known |
| Unavailable evidence | Exact artifacts the evaluator could not inspect |

Every finding and conclusion MUST cite `MODEL-*` and MUST be bounded to this access profile. A black-box evaluation cannot be presented as white-box assurance.

## 6. Environment and tool manifest

### 6.1 Environment record

Each `ENV-*` record MUST contain:

| Category | Required evidence |
|---|---|
| Host/runtime | Hardware class, operating system, kernel/runtime, container/VM image, architecture |
| Isolation | Network, filesystem, process, tenant, and physical isolation controls |
| Clock | Time source, synchronization state, timezone, and uncertainty |
| Compute | CPU/GPU/accelerator identity, driver, firmware, memory, and quota |
| Storage | Volume identity, encryption state, mount mode, and retention |
| Network | Interfaces, allowlist, proxy, DNS, egress, and capture configuration |
| Identity/access | Runtime identity, role, authentication mechanism, and least-privilege boundary |
| Secrets | Secret-reference mechanism only; no plaintext secret in the packet |
| Datasets | Dataset identifiers, versions, hashes, licenses, and permitted use |
| Randomness | Seed sources, fixed seeds, sampling configuration, and nondeterminism statement |
| Capture | Logs, packet capture, screenshots, video, tool trace, and limitations |
| Baseline | Pre-run snapshot and integrity evidence |
| Teardown | Post-run sanitization, residual data, and teardown receipt |

### 6.2 Tool record

Each executable, framework, harness, prompt set, benchmark, dataset processor, scoring script, and analysis notebook MUST have a `TOOL-*` record containing:

- name and purpose;
- source and maintainer;
- exact version, commit, package lock, image digest, or binary hash;
- configuration artifact and hash;
- dependencies and their lock evidence;
- privilege and network requirements;
- known limitations;
- calibration or self-test evidence;
- output format;
- whether the tool is evaluator-controlled, provider-controlled, or third-party controlled.

Unversioned tools MUST be marked `UNPINNED`; conclusions dependent on them inherit that limitation.

### 6.3 Environment reproducibility class

| Class | Meaning |
|---|---|
| `BYTE_REPRODUCIBLE` | Environment can be reconstructed from content-addressed artifacts |
| `FUNCTIONALLY_REPRODUCIBLE` | Equivalent behavior is expected but bytes or hardware differ |
| `PROVIDER_REPLAY_ONLY` | Reconstruction requires provider-controlled access |
| `ANALYTICAL_REPLAY_ONLY` | Captured outputs can be rescored; model execution cannot be repeated |
| `NOT_REPRODUCIBLE` | Material environment evidence is missing |

## 7. Evaluation plan, hash, and acceptance criteria

### 7.1 Plan record

Before execution, `PLAN-*` MUST record:

- evaluation objective and bounded claim target;
- model and access references;
- threat or risk hypotheses;
- test families and methods;
- dataset/input selection method;
- environment and tool references;
- sampling, seeds, repetitions, and statistical method;
- known confounders;
- acceptance criteria;
- stop conditions;
- incident route;
- evidence capture requirements;
- disclosure restrictions;
- planned verifier and reconstruction mode;
- excluded questions and explicit non-claims.

### 7.2 Plan freeze

The exact plan bytes MUST be hashed before the first run. The plan-freeze record MUST include:

| Field | Requirement |
|---|---|
| Plan artifact | Exact stored plan |
| Plan hash | SHA-256 of exact bytes |
| Freeze timestamp | Trusted time evidence or explicit local-clock limitation |
| Freezing authority | Identity and authority reference |
| Evaluator acknowledgement | Signature or acknowledgement artifact |
| First permitted run | Earliest run ID authorized under the hash |
| Amendment policy | Named process for changes |

No evaluation may use a post-hoc threshold while claiming that threshold was pre-registered.

### 7.3 Acceptance criterion record

Each `CRIT-*` MUST contain:

| Field | Requirement |
|---|---|
| Criterion claim | Exact property being assessed |
| Metric | Formula or deterministic scoring procedure |
| Direction | Minimum, maximum, equality, categorical, or bounded range |
| Threshold | Predeclared value |
| Population/sample | Scope and selection rule |
| Repetitions | Required number and aggregation method |
| Confidence/uncertainty | Method and target where applicable |
| Allowed exclusions | Predeclared exclusion rules |
| Failure rule | What constitutes failure |
| Stop condition | Immediate pause/abort trigger |
| Evidence refs required | Inputs, outputs, logs, scorer, and run records |
| Decision mapping | Pass, fail, inconclusive, or not evaluated |

### 7.4 Plan amendments

An amendment MUST NOT overwrite the frozen plan. It MUST create a new plan version with:

- previous plan hash;
- new plan hash;
- changed fields;
- reason;
- authority;
- effective run boundary;
- effect on comparability;
- whether earlier results remain admissible.

## 8. Input, output, run, observation, and finding lineage

### 8.1 Run record

Each `RUN-*` MUST bind:

- authority record;
- plan hash and criterion IDs;
- model/access record;
- environment and tool records;
- operator identity;
- start and end timestamps;
- input IDs and hashes;
- output IDs and hashes;
- raw logs and trace hashes;
- provider request IDs where available;
- seed and sampling settings;
- execution status;
- deviations, errors, retries, and excluded results;
- custody event created at capture.

Allowed execution statuses are:

`PLANNED`, `STARTED`, `COMPLETED`, `COMPLETED_WITH_DEVIATION`, `FAILED_TECHNICAL`, `STOPPED_SAFETY`, `STOPPED_AUTHORITY`, `INVALIDATED`, and `SUPERSEDED`.

### 8.2 Input record

Each `INPUT-*` MUST record source, acquisition authority, license/consent, data classification, exact bytes or reproducible generator, hash, transformations, selection rule, expected behavior where applicable, and disclosure limits.

Input artifacts containing personal data, credentials, exploit material, controlled model information, or harmful instructions MUST use a restricted evidence reference; public packet views MUST contain only an integrity-linked surrogate and redaction reason.

### 8.3 Output record

Each `OUTPUT-*` MUST record the associated run and input, raw model response or binary output, tool calls, external side effects, finish condition, provider metadata, capture method, hash, classification, and any capture loss.

Presentation-cleaned outputs MUST never replace raw outputs. They receive separate identifiers and transformation lineage.

### 8.4 Observation record

An `OBS-*` is a direct evaluator observation tied to evidence. It MUST state:

- what was observed;
- which artifacts support it;
- capture limitations;
- whether it is machine-derived or human-derived;
- uncertainty;
- whether another reviewer confirmed it.

### 8.5 Finding record

Each `FIND-*` MUST contain:

| Field | Requirement |
|---|---|
| Finding statement | Bounded claim, not rhetorical conclusion |
| Supporting observations | `OBS-*` references |
| Supporting runs | `RUN-*` references |
| Criteria | `CRIT-*` references |
| Model/access boundary | `MODEL-*` reference |
| Severity | Named scale and rationale |
| Confidence | Named scale and rationale |
| Reproducibility | Repetition evidence and constraints |
| Alternative explanations | Considered confounders |
| Affected claim | Which safety, security, or capability claim is affected |
| Non-claims | What the evidence does not show |
| Reviewer | Identity and independence status |
| Current state | Finding lifecycle state |

Finding lifecycle states are:

`DRAFT`, `OPEN`, `CONFIRMED_WITHIN_BOUNDARY`, `DISPUTED`, `MITIGATION_PROPOSED`, `MITIGATED_PENDING_RETEST`, `CLOSED_RETEST_PASS`, `CLOSED_RETEST_FAIL`, `CLOSED_RISK_ACCEPTED`, `WITHDRAWN_WITH_REASON`, and `SUPERSEDED`.

### 8.6 Lineage invariants

1. Every finding traces to one or more observations.
2. Every observation traces to captured evidence.
3. Every captured output traces to a run, input, model boundary, environment, tool set, and plan hash.
4. Every run traces to authority.
5. Every transformation retains source and output hashes.
6. Excluded evidence remains indexed with exclusion authority and rationale unless retention law or safety policy requires controlled destruction.

## 9. Mitigation and retest record

### 9.1 Mitigation record

Each `MIT-*` MUST contain:

- affected finding IDs;
- mitigation owner and authority;
- proposed change;
- changed model, prompt, policy, tool, data, environment, or deployment components;
- exact change artifact or provider change reference;
- expected effect;
- new risks or regressions considered;
- approval record;
- implementation timestamp;
- deployment population and boundary;
- rollback path;
- evidence that the change was active for retest.

### 9.2 Retest record

Each `RETEST-*` MUST contain:

| Field | Requirement |
|---|---|
| Original finding | `FIND-*` reference |
| Mitigation | `MIT-*` reference |
| Retest plan | Frozen plan/hash; may reuse or supersede original |
| Environment delta | Exact differences from original `ENV-*` |
| Model delta | Exact differences from original `MODEL-*` |
| Tool delta | Exact differences from original `TOOL-*` records |
| Original criteria | Reused or explicitly amended criteria |
| New runs | `RUN-*` references |
| Comparative analysis | Original versus retest metrics |
| Regression checks | Named unaffected properties retested |
| Decision | Pass, fail, partial, or inconclusive |
| Residual risk | Explicit remaining uncertainty |

A mitigation may not close a finding without a retest unless an authorized risk owner records `CLOSED_RISK_ACCEPTED` with rationale and scope. Risk acceptance is not evidence that the underlying behavior was fixed.

## 10. Custody and disclosure controls

### 10.1 Evidence classifications

| Class | Handling baseline |
|---|---|
| `PUBLIC` | Approved for unrestricted release |
| `CONTROLLED` | Shared only with named operational recipients |
| `RESTRICTED` | Sensitive model, security, personal, contractual, or regulatory evidence |
| `HIGHLY_RESTRICTED` | Model weights, dangerous capabilities, exploitable findings, secrets, or evidence whose disclosure could create material harm |

Classification MUST identify the authority and policy source. Classification is not a substitute for legal analysis.

### 10.2 Custody event

Every acquisition, creation, transfer, copy, transformation, disclosure, archival action, access grant, access revocation, and destruction MUST create a `CUST-*` event containing:

- artifact ID and hash;
- event type;
- previous and new custodian;
- physical/logical location class;
- timestamp and time evidence;
- actor identity;
- authority reference;
- transport or transfer mechanism;
- encryption/integrity mechanism;
- result and exceptions;
- linked disclosure or destruction record.

Custody events are append-only. Corrections supersede; they do not erase.

### 10.3 Secret and credential handling

- Plaintext credentials, API keys, access tokens, private keys, recovery codes, and model-access secrets MUST NOT appear in the packet.
- The packet may contain a secret-reference ID, injection receipt, scope, issuer, expiry, and revocation evidence.
- Secret access MUST be attributed to a runtime identity and authority record.
- Revocation or rotation MUST be recorded at closure where applicable.

### 10.4 Redaction

A redacted artifact MUST retain:

- unredacted artifact ID and hash in the restricted manifest;
- redacted artifact ID and hash;
- deterministic or described redaction process;
- redaction authority;
- reason and affected fields;
- statement of how redaction limits verification.

### 10.5 Disclosure event

Each `DISC-*` MUST record recipient identity/class, purpose, artifacts and versions disclosed, classification, redactions, legal/contractual basis, disclosure authority, channel, time, acknowledgement, onward-disclosure constraints, expiry or recall condition, and any later withdrawal.

No public release is authorized merely because an evaluation is complete.

### 10.6 Retention and destruction

The packet MUST specify retention periods per artifact class, authority source, legal hold status, archival format, destruction method, and destruction evidence. Destruction must not be claimed without a named mechanism and receipt. Where destruction would break required auditability, the conflict MUST be escalated before execution.

## 11. Serious-incident and emergency route

### 11.1 Purpose

This section creates an escalation and evidence-preservation path. It does not make WitnessOps the legal incident classifier or reporting authority.

### 11.2 Incident states

| State | Meaning |
|---|---|
| `SIGNAL` | An event may require safety, security, privacy, or regulatory review |
| `POTENTIAL_SERIOUS_INCIDENT` | Threshold may be met; classification authority must review |
| `REPORTABLE_CONFIRMED_BY_AUTHORITY` | Named competent authority/owner determined reporting is required |
| `NOT_REPORTABLE_WITH_RATIONALE` | Named authority recorded why threshold is not met |
| `REPORTED` | Report artifact, recipient, channel, and time are recorded |
| `CLOSED_WITH_CORRECTIVE_ACTION` | Investigation and corrective action are recorded |
| `UNRESOLVED` | Classification or route remains incomplete |

### 11.3 Immediate handling sequence

1. Protect people and systems within the evaluator's actual authority.
2. Pause the affected test when a plan stop condition is met.
3. Preserve model version, environment, logs, inputs, outputs, and volatile evidence.
4. Create `INC-*` and initial custody events.
5. Notify the named incident owner and evaluation principal through the pre-authorized route.
6. Determine operator role: provider, deployer, evaluator, authorized representative, importer, distributor, or other.
7. Determine applicable legal, contractual, programme, sectoral, vulnerability-disclosure, privacy, and emergency routes.
8. Record the reporting decision, deadline basis, recipient, authority, and evidence disclosed.
9. Do not alter the affected system in a way that could prejudice later causal evaluation without preserving evidence and notifying the competent owner where required.
10. Record mitigation, investigation, retest, and closure separately.

### 11.4 Route register

Before execution, the following routes MUST be instantiated or marked unresolved:

| Route | Required fields |
|---|---|
| Evaluation safety route | Owner, secure contact, response target, stop authority |
| Model-provider route | Security/safety contact, permitted disclosure, acknowledgement method |
| Principal route | Decision owner, escalation order, out-of-hours contact |
| AI regulatory route | Applicable role, authority source, competent recipient, deadline basis |
| Vulnerability route | Coordinated-disclosure policy, embargo, CVE/CSIRT route where applicable |
| Personal-data route | Controller/DPO, supervisory route, processor obligations where applicable |
| Sector route | Health, finance, transport, energy, product-safety, or other authority |
| Emergency route | Immediate-threat procedure and local emergency authority |

### 11.5 EU AI Act context

The following source-backed distinctions guide, but do not complete, route classification:

- Article 55(1)(c) of Regulation (EU) 2024/1689 places duties on providers of general-purpose AI models with systemic risk to track, document, and report serious incidents and possible corrective measures to the AI Office and, where appropriate, national competent authorities.
- Article 73 establishes reporting duties for providers of high-risk AI systems to relevant market-surveillance authorities and includes incident-dependent deadlines.
- These duties attach to defined roles and systems. An evaluator does not acquire provider or deployer reporting authority merely by discovering a finding.

The incident owner MUST obtain role- and jurisdiction-specific advice before asserting that a legal reporting threshold has or has not been met.

## 12. Packet manifest and expected artifact layout

### 12.1 Expected layout

| Path | Required content |
|---|---|
| `00-control/` | Boundary, packet state, profile, manifest, signatures, timestamps |
| `01-authority/` | Principal authority, evaluator appointment, role registry |
| `02-evaluator/` | Identity, competence evidence, independence declaration/review |
| `03-model-access/` | Model identity, version, access and provider boundary |
| `04-environment-tools/` | Environment snapshots, tool manifests, calibration evidence |
| `05-plan/` | Frozen plan, plan hash, acceptance criteria, amendments |
| `06-runs/` | Run records, inputs, outputs, logs, deviations |
| `07-findings/` | Observations, findings, reviews, challenges |
| `08-mitigation-retest/` | Mitigations, deployment evidence, retests, residual risk |
| `09-custody-disclosure/` | Custody ledger, access ledger, redaction and disclosure records |
| `10-incidents/` | Route register, incident records, reporting evidence |
| `11-verification/` | Verifier instructions, verification receipt, unresolved gaps |
| `12-presentation/` | Approved public or recipient-specific views only |

### 12.2 Manifest entry

Every retained artifact MUST have a manifest entry containing:

| Field | Requirement |
|---|---|
| `artifact_id` | Immutable packet artifact ID |
| `path` | Relative path, unique within packet |
| `sha256` | Exact-byte hash |
| `bytes` | Exact byte count |
| `media_type` | Declared MIME type |
| `record_type` | Authority, model, run, finding, etc. |
| `version` | Artifact version |
| `created_at` | RFC 3339 UTC |
| `created_by` | Identity reference |
| `authority_ref` | Authority permitting creation/acquisition |
| `classification` | Evidence handling class |
| `custodian_ref` | Current custodian |
| `source_refs` | Source artifacts where derived |
| `supersedes` | Earlier artifact, if any |
| `retention_ref` | Retention rule |
| `disclosure_refs` | Disclosure events, if any |

The manifest MUST be complete before packet closure. Missing expected artifacts MUST appear in an explicit gap register rather than disappearing from the manifest.

## 13. Independent reconstruction procedure

### 13.1 Reconstruction modes

The verifier MUST state which mode was achieved:

| Mode | What is checked |
|---|---|
| `INTEGRITY_RECONSTRUCTION` | Manifest, hashes, signatures, timestamps, and custody continuity |
| `ANALYTICAL_REPLAY` | Metrics/findings recomputed from captured inputs and outputs |
| `EXECUTION_REPLAY` | Runs repeated in the declared environment against the same model/version |
| `INDEPENDENT_REPRODUCTION` | Method repeated independently with separately assembled environment and access |

Exact model outputs may be nondeterministic. A verifier MUST NOT claim byte-for-byte execution reproduction unless the outputs actually match and the plan requires that property.

### 13.2 Verifier prerequisites

The verifier requires:

- verifier identity and independence declaration;
- packet root manifest and all artifacts needed for the selected mode;
- signature/key and timestamp resolution procedures;
- access to restricted artifacts or a declared verification limitation;
- executable scoring tools or captured scoring evidence;
- the challenge and supersession register;
- no reliance on undocumented oral explanation for a material conclusion.

### 13.3 Reconstruction steps

The verifier MUST perform and record the following steps:

1. **Admit the packet:** identify packet ID, state, version, root manifest, and boundary statement.
2. **Verify byte integrity:** recompute every available artifact hash and byte count; record missing or mismatched artifacts.
3. **Verify signatures and time evidence:** execute the named verification methods and record trust anchors and limitations.
4. **Reconstruct authority:** verify principal authority, evaluator appointment, authorized model, methods, time window, disclosure, stop, and incident powers.
5. **Assess evaluator identity and independence:** distinguish self-declaration, corroborating evidence, conflicts, and unresolved constraints.
6. **Bind model and access:** verify model/version and ensure conclusions do not exceed the tested access boundary.
7. **Reconstruct environment and tools:** resolve versions, hashes, configuration, datasets, seeds, isolation, and capture gaps.
8. **Verify plan pre-registration:** recompute the frozen plan hash, confirm freeze precedes execution, and inspect amendments.
9. **Reconstruct runs:** bind each input and output to run, plan, model, environment, tool, operator, and custody evidence.
10. **Recompute criteria:** execute scorers or independently recompute metrics from retained evidence.
11. **Trace findings:** verify every material finding against observations, evidence, criteria, alternatives, and non-claims.
12. **Trace mitigation and retest:** confirm change evidence, environment/model delta, retest runs, regressions, and residual risk.
13. **Inspect custody and disclosure:** identify gaps, unauthorized copies, redactions, and recipient-specific limitations.
14. **Inspect incidents:** verify stop actions, preservation, classification authority, reporting decision, route, and corrective action.
15. **Resolve challenges and supersession:** ensure disputed or replaced records are visible and correctly linked.
16. **Issue `VER-*`:** state achieved reconstruction mode, checks performed, artifacts used, failures, gaps, and bounded decision.

### 13.4 Verification decisions

Exactly one decision MUST be issued:

| Decision | Meaning |
|---|---|
| `PASS_RECONSTRUCTED` | Required evidence for the claimed reconstruction mode is complete and checks pass |
| `PASS_INTEGRITY_ONLY` | Byte integrity passes; execution or analytical conclusions were not replayed |
| `PASS_WITH_BOUNDED_GAPS` | Gaps are explicit and do not invalidate the narrowed claim |
| `PARTIAL_RECONSTRUCTION` | Material portions were reconstructed, but claim remains incomplete |
| `FAIL_INTEGRITY` | Artifact mismatch, omission, or broken manifest invalidates integrity claim |
| `FAIL_AUTHORITY` | Execution or disclosure lacks sufficient authority evidence |
| `FAIL_LINEAGE` | Findings cannot be traced to admissible evidence |
| `BLOCKED_ACCESS` | Required restricted/model/provider evidence was unavailable |
| `BLOCKED_MISSING_EVIDENCE` | Required artifacts were not retained or supplied |
| `INDEPENDENCE_UNRESOLVED` | Conflicts or independence evidence prevent independent-verification claim |

The verification receipt MUST name the verifier, mechanism, artifacts, trust anchors, and reconstruction mode. The word “verified” MUST NOT appear without this receipt or another explicitly named proof path.

## 14. Challenges, corrections, and supersession

Any authorized party may create `CHAL-*` containing:

- challenged claim or artifact;
- challenger identity and authority/standing;
- grounds and supporting evidence;
- requested remedy;
- response owner and deadline;
- resolution;
- effect on packet decision;
- superseding artifacts.

Challenges are retained even when rejected. Corrections never rewrite history silently. A superseding packet MUST link to the superseded packet and state which claims, evidence, findings, and verification receipts remain valid.

## 15. Closure gate

The packet may enter `CLOSED` only when all required answers are supported:

| Gate | Required result |
|---|---|
| Authority | Principal and evaluator authority admitted |
| Independence | Declaration present; independent review status explicit |
| Model boundary | Exact version/access and limitations recorded |
| Environment/tools | Manifest complete or gaps admitted |
| Plan | Frozen hash predates execution; amendments linked |
| Criteria | Every decision maps to predeclared criteria or is marked exploratory |
| Lineage | Findings trace to observations, runs, inputs, outputs, and evidence |
| Mitigation/retest | Open findings and residual risks explicitly classified |
| Custody | Required custody events and current custodians recorded |
| Disclosure | Releases authorized and redactions linked |
| Incidents | Signals resolved or explicitly open with owner and route |
| Verification | `VER-*` issued or verification marked pending |
| Gaps | Gap register complete |
| Non-claims | External presentation remains bounded |

Failure of a gate results in `CLOSED_WITH_GAPS`, `ABORTED`, or continued `IN_PROGRESS`; it must not be converted into an unqualified pass.

## 16. Evaluation-level conclusion

The evaluator MUST issue exactly one bounded evaluation conclusion:

| Conclusion | Meaning |
|---|---|
| `PASS_WITHIN_TESTED_BOUNDARY` | All applicable predeclared criteria passed |
| `PASS_WITH_LIMITATIONS` | Criteria passed subject to explicit material limitations |
| `FAIL_WITHIN_TESTED_BOUNDARY` | One or more predeclared failure rules were met |
| `INCONCLUSIVE` | Evidence or statistical power does not support pass/fail |
| `ABORTED` | Evaluation stopped under authority, safety, or technical condition |
| `NOT_EVALUATED` | Packet preparation occurred without evaluation execution |

For this draft the only permitted conclusion is:

`NOT_EVALUATED`

## 17. Minimum operator forms

Before any live evaluation, the operator MUST instantiate these records:

1. `AUTH-0001 — Evaluation Mandate`
2. `EVALR-0001 — Evaluator Identity and Competence`
3. `EVALR-0002 — Independence Declaration`
4. `MODEL-0001 — Model and Access Boundary`
5. `ENV-0001 — Evaluation Environment`
6. `TOOL-* — Tool and Dataset Manifest`
7. `PLAN-0001 — Frozen Evaluation Plan`
8. `CRIT-* — Acceptance Criteria`
9. `CUST-0001 — Initial Custody Admission`
10. `INC-ROUTE-0001 — Incident Route Register`
11. `DISC-AUTH-0001 — Disclosure Authority`
12. `VER-PLAN-0001 — Independent Reconstruction Plan`

Execution remains blocked until the mandate, model access, environment, plan freeze, incident route, evidence custody, and stop conditions are admitted.

## 18. Current gap register

| Gap ID | Missing evidence | Effect |
|---|---|---|
| `GAP-0001` | No appointed evaluation principal | No evaluation authority |
| `GAP-0002` | No evaluator identity or competence evidence | Qualification unresolved |
| `GAP-0003` | No independence declaration or corroboration | Independence unresolved |
| `GAP-0004` | No model/version or access authorization | Model testing prohibited |
| `GAP-0005` | No environment or tool manifest | Execution unreconstructable |
| `GAP-0006` | No frozen evaluation plan or criteria | No admissible pass/fail basis |
| `GAP-0007` | No custody or disclosure authority | Evidence handling prohibited |
| `GAP-0008` | No instantiated incident route | Live evaluation unsafe/unready |
| `GAP-0009` | No independent verifier appointment | Independent reconstruction pending |
| `GAP-0010` | No European Commission eligibility, evaluator admission, or programme appointment evidence | No Commission-work or programme-admission claim permitted |
| `GAP-0011` | Canonical Action Plan source record not attached to this packet | Policy context cannot act as authority evidence |

## 19. Source and authority notes

### Normative external sources consulted for the draft

1. [Regulation (EU) 2024/1689 — Artificial Intelligence Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng), especially Articles 55 and 73. This is a legal source, but applicability to a specific evaluation requires role- and system-specific analysis.
2. [European Commission — General-Purpose AI Code of Practice](https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai). The Safety and Security chapter is presented by the Commission as a route for providers of general-purpose AI models with systemic risk to demonstrate relevant Article 55 practices.
3. [DIGITAL-2026-AI-DATA-10-COMPLIANCE call document](https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/digital/wp-call/2026/call-fiche_digital-2026-ai-data-10_en.pdf). This is contextual evidence of an EU funding opportunity; it does not establish WitnessOps eligibility, consortium membership, evaluator qualification, or award.

### Authority status of this draft

These sources informed the template. None appoint WitnessOps, authorize an evaluation, grant model access, certify independence, or establish programme admission. A future packet MUST carry its own evaluation-specific authority records.

## 20. Final draft declaration

`AI_MODEL_EVALUATION_EVIDENCE_PACKET_V1` is a governed template in state `DRAFT_TEMPLATE_NOT_EXECUTED`.

It is ready for authority review and controlled instantiation. It is not ready for evaluation execution, external qualification claims, Commission-work claims, model-access claims, or programme-admission claims.
