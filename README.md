Origin Audit Standard (OAS) is a deterministic audit proof framework
that separates Proof, Verification, and Trust.

Reference implementation of the Origin Audit Standard (OAS).

# Origin Audit Standard (OAS)

Origin Audit Standard (OAS) is a deterministic proof framework for generating,
anchoring, verifying, and signing audit evidence packages.

The system separates three layers:

Proof  
Verification  
Trust

Trust grows through signatures, not through protocol consensus.

---

# Core Components

Runner  
Generates audit reports and proof packages.

Verifier  
Recomputes deterministic proof and validates integrity.

Signature Layer  
Appends node trust endorsements without modifying the proof.

---

# Runtime Architecture

Actual system currently running:

docs/architecture-runtime.md

---

# Growth Architecture

Future trust-layer expansion path:

docs/architecture-growth.md

---

# Proof Structure

Example proof package:

manifest.json
artifacts/*
Anchor chain:

anchor.log
---

# Verification

Verification tool:

oas/verify/verify_oas.py
Verification checks:

- manifest self-hash
- artifact hashes
- anchor presence
- anchor chain integrity

---

# Trust Layer

Trust is appended through signatures.

Example:

signatures[]
Signatures do not modify proof hashes.

---

# Node Identity

Nodes publish identity through:

node.json
Example fields:

node_id
public_key
network metadata
---

# License

Open specification for deterministic audit proof systems.
