# Origin Audit Standard (OAS)

Origin Audit Standard (OAS) is a deterministic audit proof framework  
that separates **Proof**, **Verification**, and **Trust**.

The system allows audit evidence to be generated, anchored, verified,  
and optionally endorsed by independent nodes.

---

## Core Model

OAS separates three layers:

Proof  
Verification  
Trust  

Trust grows through **signatures**, not through **consensus complexity**.

---

## Architecture

Two diagrams describe the system.

Runtime architecture:

docs/architecture-runtime.md

Growth architecture:

docs/architecture-growth.md

---

## Proof Package

An OAS report produces a deterministic proof package.

Example structure:

manifest.json
artifacts/*
The proof hash is stored in the anchor chain.

---

## Anchor Chain

OAS uses an append-only hash chain.

Example:

seq timestamp hash prev_hash domain
File:

anchor.log
This ensures proof immutability.

---

# Verification

Anyone can independently verify a proof package.

Verifier:

oas/verify/verify_oas.py
Verification checks:

- manifest self-hash  
- artifact integrity  
- anchor presence  
- anchor chain continuity  

---

## Layer

Trust is appended through signatures.

Example:

signatures[]
Signatures **do not modify proof hashes**.

They extend the trust layer independently of proof generation.

---

## Node Identity

Nodes declare identity using:
node.json
Example fields:

node_id
public_key
network metadata
---

## Repository Structure

aiorigins-audit

docs/
architecture-runtime.md
architecture-growth.md

oas/
verify/
verify_oas.py

---

## Project Status

Reference implementation of **Origin Audit Standard v0.1**.

Current components implemented:

- proof generation
- anchor chain
- deterministic verifier
- signature layer

---

## License

Open specification for deterministic audit proof systems.
