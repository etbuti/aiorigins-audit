# OAS Runtime Architecture

This diagram shows the **actual running structure** of the Origin Audit Standard (OAS) system.

---

## System Overview

```mermaid
flowchart TB

Reality["Reality / Observed State"]

Runner["Runner
runner_oas_test.py"]

Proof["Proof Package
manifest.json
artifacts"]

Anchor["Anchor Chain
anchor.log"]

Verify["Verification
verify_oas.py"]

Sign["Signature Layer
oas-sign"]

Node["Node Identity
node.json"]

Reality --> Runner
Runner --> Proof
Proof --> Anchor
Proof --> Verify
Anchor --> Verify
Verify --> Sign
Sign --> Node

Components

Runner

Generates audit reports from observed system state.

⸻

Proof Package

A deterministic report package.

Files:
manifest.json
artifacts/*

Anchor Chain

Append-only hash chain used to lock proof hashes.

Example location:
/var/lib/origin-oas/anchors/anchor.log

Verification

Open deterministic verification algorithm.

Reference implementation:
verify_oas.py

Signature Layer

Optional trust endorsement layer.

Signatures extend trust without modifying the proof hash.

Example:
signatures[]

Node Identity

Public node declaration.

Example file:
node.json
