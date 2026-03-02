OAS v0.1 Verification Tools

This directory provides two ways to verify an OAS sample report.

1) Browser verification (no upload)
- Open: /oas/verify/
- Upload: manifest.json
- The page recomputes the canonical self-hash (SHA-256) locally in your browser
  and compares it with manifest.anchor.current_hash.

2) Offline verification (CLI)
- Script: verify_oas.py
- Usage:
  python3 verify_oas.py --manifest manifest.json

Optional (if an anchor log is provided with the package):
  python3 verify_oas.py --manifest manifest.json --anchor-log anchor.log

Notes
- The public sample is a format demonstration (provenance-style snapshot).
- It is NOT a security rating and does not claim vulnerability findings.
