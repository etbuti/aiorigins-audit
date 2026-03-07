# OAS Architecture Overview

This repository contains the reference implementation of the **Origin Audit Standard (OAS)**.

---

## System Overview

```mermaid
flowchart TB

Reality["Reality / Observed State"]

Runner["Runner
generate proof"]

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
```

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