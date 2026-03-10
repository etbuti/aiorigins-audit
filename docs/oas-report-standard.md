# OAS Report Standard v1

Origin Audit Standard (OAS) defines a deterministic audit proof framework.

This document specifies the structure of an **OAS Report Package** and the rules
required for deterministic verification.

The goal is to allow any independent verifier to reproduce the proof hash
and confirm the integrity of the report without relying on the issuing node.

---

# 1. OAS Report Package

An OAS report is a deterministic package containing:

manifest.json
artifacts/*
Example structure:

AIR-2026-03-02T13:04:25Z/
manifest.json
artifacts/
evidence_min.json
The package is immutable once generated.

---

# 2. Manifest Structure

The manifest file describes the proof package.

File:

manifest.json
Example:

```json
{
  "report_id": "AIR-2026-03-02T13:04:25Z",
  "version": "0.1",
  "generated_at": "2026-03-02T13:04:26Z",

  "target": {
    "domain": "iana.org"
  },

  "engine": {
    "runner": "oas-test-runner",
    "issuer_mode": "origin-only"
  },

  "artifacts": [
    {
      "path": "artifacts/evidence_min.json",
      "sha256": "ae3483934f2d94b1a2c4a88e0da07e6b8ff45cc6049afcf65366ae007a15191a",
      "bytes": 443,
      "mime": "application/json"
    }
  ],

  "anchor": {
    "anchor_sequence": 43,
    "previous_hash": "1789d82b251e445a401bcbba0c5905640e7f5787cf501cc70722c7d47d965315",
    "current_hash": "695799e28c1ad58bcd7b440c3c0f01108e628cff1ea201b1b895d88f81e794b1"
  },

  "oas": {
    "standard": "Origin Audit Standard",
    "version": "0.1",
    "profile": "sample-minimal"
  },

  "signatures": []
}

⸻

3. Deterministic Proof Hash

The proof hash is stored in:
manifest.anchor.current_hash

The hash is calculated using:
SHA256(canonical_json(manifest_without_current_hash_and_signatures))

Rules:
		1.	anchor.current_hash must be removed before hashing
	2.	signatures must be normalized to an empty list
	3.	JSON must be serialized in canonical form

Canonical JSON rules:
sort_keys=true
separators=(",",":")
UTF-8 encoding

The computed hash must equal:
manifest.anchor.current_hash

⸻

4. Artifact Integrity

Each artifact listed in the manifest must match:
sha256
bytes

Verification steps:
	1.	locate artifact path
	2.	compute SHA256
	3.	compare with manifest entry

Example artifact entry:
{
  "path": "artifacts/evidence_min.json",
  "sha256": "...",
  "bytes": 443,
  "mime": "application/json"
}

Artifacts are immutable once included in a proof package.

⸻

5. Anchor Chain Integration

Each report must be anchored in the append-only chain.

Example:
seq timestamp current_hash previous_hash domain

File:
/var/lib/origin-oas/anchors/anchor.log

Example entry:
43 2026-03-02T13:04:26Z
695799e28c1ad58bcd7b440c3c0f01108e628cff1ea201b1b895d88f81e794b1
1789d82b251e445a401bcbba0c5905640e7f5787cf501cc70722c7d47d965315
iana.org

Verification rules:
anchor_sequence must exist
previous_hash must match previous entry
chain must be continuous

⸻

6. Verification

Any independent node can verify a report package.

Reference implementation:
oas/verify/verify_oas.py

Verification checks:
manifest self-hash
artifact integrity
anchor presence
anchor chain continuity

Verification must produce deterministic results.

⸻

7. Signature Layer

Signatures extend trust without modifying the proof.

Example:
"signatures": [
  {
    "node_id": "aiorigins.org",
    "key_id": "oas-ed25519-2026",
    "algorithm": "ed25519",
    "signed_at": "2026-03-07T15:56:00Z",
    "signature": "..."
  }
]

Rules:
signatures are append-only
signatures must not modify proof hash
multiple nodes may sign the same report

Signatures represent trust endorsement, not proof generation.

⸻

8. Node Identity

Signing nodes declare identity using:
node.json

Example fields:
node_id
public_key
network metadata

Node identity is independent from proof generation.

⸻

9. Deterministic Verification Principle

OAS verification must satisfy:
deterministic proof
independent verification
append-only trust

Verification results must not depend on:
network timing
node state
consensus participation

Any verifier with the report package and anchor chain
must reproduce the same verification result.

⸻

10. Version

This document describes:
Origin Audit Standard
Report Standard v1

Reference implementation:
aiorigins-audit

⸻

License

Open specification for deterministic audit proof systems.
