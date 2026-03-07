OAS Runtime Architecture

This diagram shows the actual running structure of the Origin Audit Standard system.

Reality
   │
   ▼
Runner (runner_oas_test.py)
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

Components

Runner
Generates audit reports.

Proof Package
Deterministic report package.
Files:
manifest.json
artifacts/*

Anchor Chain
Append-only hash chain.
/var/lib/origin-oas/anchors/anchor.log

Verification
Open deterministic verification algorithm.
verify_oas.py

Signature Layer
Optional trust endorsement.
signatures[]

Node Identity
Public node declaration.
node.json

