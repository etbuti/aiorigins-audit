# OAS Architecture Overview

This repository contains the reference implementation of the **Origin Audit Standard (OAS)**.

---

## System Overview

Reality
│
▼
Runner
│
▼
Proof Package
(manifest.json + artifacts)
│
▼
Anchor Chain
(anchor.log)
│
▼
Verification
(verify_oas.py)
│
▼
Signature Layer
(oas-sign)
│
▼
Node Identity
(node.json)

This diagram shows the **runtime flow of an OAS proof**.

---

## Runtime Architecture

Actual system currently running.

See:

docs/architecture-runtime.md

---

## Growth Architecture

Future natural expansion path of the trust layer.

See:

docs/architecture-growth.md

---

## Core Principle

The system separates three layers:

Proof  
Verification  
Trust  

Trust grows through **signatures**, not through **consensus complexity**.

