# Security Policy

We take security issues in this repository seriously. This document describes what is in scope, how to report a suspected vulnerability, and what to expect from us in return.

## Scope

This repository contains the canonical contract surface for WitnessOps proof runs:

- JSON schemas under `schemas/`
- valid and invalid examples under `examples/`
- schema validation tests under `tests/`
- explanatory contract documentation under `docs/`
- CI validation for contract fixtures

This repository does **not** contain proof-engine execution, offline verifier implementation, source-system adapters, signing-key custody, customer evidence custody, website copy, live workflow execution, deployment authority, production proof claims, or private client evidence.

Reports against systems outside this repository are out of scope here and should be directed to the appropriate project or vendor.

## Supported surface

Only the current `main` branch of this repository is supported and receives security fixes. Older branches, tags, and historical releases are not patched.

## Reporting a vulnerability

Please report suspected vulnerabilities privately through one of the following channels:

- **Preferred:** GitHub Private Vulnerability Reporting —
  <https://github.com/witnessops/witnessops-contracts/security/advisories/new>
- **Alternative:** email <security@witnessops.com>

When reporting, please include:

- a description of the issue and its potential impact
- steps to reproduce, or a proof of concept
- the affected schema, fixture, test, or document if known
- any relevant commit SHA or environment details

> **Do not use public GitHub issues, discussions, or pull requests to report suspected vulnerabilities.** Public reports can put users at risk before a fix is available.

## Acknowledgment window

We will acknowledge receipt of your report within **5 business days**. That acknowledgment confirms the report reached us; a full triage and impact assessment will follow.

## Disclosure handling

We prefer coordinated disclosure:

- We will work with you to validate the issue, assess impact, and prepare a fix.
- We ask for a reasonable embargo period while a fix is being prepared and rolled out. The exact length depends on severity and complexity, and we will agree it with you.
- Once a fix is available, we will publish an advisory describing the issue and its resolution.
- Reporters will be credited in the advisory unless they ask to remain anonymous.

## Examples of in-scope issues

The following are examples of issues that may be security-relevant in this repository:

- schema accepts missing or malformed required proof material as valid
- schema permits undeclared fields that can smuggle authority, evidence, signer, or verifier claims
- invalid fixtures accidentally validate
- valid fixtures contain secrets, credentials, private keys, customer data, production evidence, tokens, or internal custody paths
- receipt schema weakens signature, claim, or evidence-reference requirements
- evidence manifest schema weakens artifact hash or lineage requirements
- verifier-result schema collapses pass, partial, fail, inconclusive, or blocked semantics
- workflow-class schema allows execution boundaries to be omitted where downstream systems rely on them
- outcome or failure-state semantics allow unproven conditions to be presented as verified
- CI validation stops proving both valid fixtures pass and invalid fixtures fail

## Generally out of scope

The following are generally not considered reportable vulnerabilities for this repository unless a concrete security impact is demonstrated:

- missing generic web-app security headers, because this repo is not a web app
- social-engineering attacks targeting maintainers or operators
- denial-of-service via volumetric traffic flooding
- third-party dependency advisories already tracked by an automated advisory feed
- claims that a production workflow occurred without a concrete proof bundle, evidence manifest, artifact hashes, receipt, signer or key reference, and verifier result

If you believe one of the above has a concrete, demonstrable security impact in this repository, please still report it through the private channels above and explain the impact.
