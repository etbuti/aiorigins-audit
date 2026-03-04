# AuditVisa Spec v0.2 (Issuer-Centric Proof)

**Status:** Active (Core) · Extensions Deferred (Trust Network Layer)  
**Model:** Issuer-centric truth. Core rules do not adapt to divergent external recomputation.  
**Audience:** Humans + Machines (machine-first, not human-only).

---

## 1. Purpose

AuditVisa defines a machine-verifiable proof package issued by an issuer-side reference implementation.

The package is intended for:
- Automated integrity snapshots (domain / endpoint / policy checks)
- Evidence packaging (machine-readable)
- Issuer signature anchoring (Ed25519)

AuditVisa is **not** a universal compatibility toolkit. Cross-environment differences are out of scope for Core.

---

## 2. Scope and Boundary

### 2.1 Core Guarantees (Issuer Responsibility)
Core guarantees are provided by the issuer implementation:
- Deterministic package construction (issuer-defined canonicalization)
- Issuer signature (Ed25519)
- Public key anchor URL
- Delivery artifacts (JSON/HTML/ZIP)
- Evidence traceability within issuer boundary

### 2.2 Out of Scope (Core)
Not a Core obligation:
- Cross-platform recomputation convergence
- Third-party implementation variance (JSON libs, encoding, crypto backends)
- Protocol adapters for arbitrary environments

Such items may exist as **commercial/value-added Bridge layers**.

---

## 3. Roles

- **Issuer**: produces and signs AuditVisa packages.
- **Consumer**: receives package as proof.
- **Verifier**: checks issuer signature (minimum requirement), plus optional checks.

---

## 4. Package Identity

### 4.1 VisaID Format

`AV-YYYYMMDD-NODE-RUNHASH6`

- `YYYYMMDD`: UTC date of issuance (issuer-side)
- `NODE`: issuer node code (e.g., `AO`)
- `RUNHASH6`: 6 hex chars derived from an issuer-defined signing anchor (see §6)

Example: `AV-20260303-AO-B01AFE`

### 4.2 Status Enum

`PASS | WARN | FAIL`

- PASS: no failing checks
- WARN: warnings present, no fails
- FAIL: one or more fails present

---

## 5. JSON Package Structure

### 5.1 Top-level Fields

| Field | Type | Required | Notes |
|---|---|---:|---|
| `schema` | string (URL) | yes | schema identifier URL |
| `kind` | string | yes | must be `AuditVisa` |
| `version` | string | yes | must be `0.2` |
| `visa_id` | string | yes | §4.1 |
| `status` | enum | yes | §4.2 |
| `summary` | object | recommended | human-friendly counts |
| `header` | object | recommended | issuer metadata |
| `target` | object | yes | target input/normalized |
| `policy` | object | optional | policy / notes |
| `checks` | array | yes | list of check results |
| `evidence` | array | optional | evidence records |
| `artifacts` | array | optional | downloadable artifacts |
| `signatures` | object | yes | issuer signature block |
| `timestamps` | object | yes | issued timestamps |

### 5.2 `target`

| Field | Type | Required | Notes |
|---|---|---:|---|
| `input` | string | yes | user input |
| `normalized` | string | recommended | issuer-normalized canonical target |

### 5.3 `checks[]`

Each check item:
| Field | Type | Required | Notes |
|---|---|---:|---|
| `check_id` | string | yes | stable identifier |
| `status` | enum | yes | PASS/WARN/FAIL |
| `severity` | string | optional | `info|low|medium|high` (issuer-defined) |
| `path` | string | optional | path / component |
| `evidence_ids` | array | optional | references into evidence |

### 5.4 `evidence[]`

Each evidence item:
| Field | Type | Required | Notes |
|---|---|---:|---|
| `evidence_id` | string | yes | stable id |
| `type` | string | yes | issuer-defined |
| `ts` | string | yes | ISO8601 UTC |
| `data` | object | yes | machine-readable payload |

### 5.5 `artifacts[]`

| Field | Type | Required | Notes |
|---|---|---:|---|
| `name` | string | yes | filename or label |
| `type` | string | optional | `json|html|zip|bin|txt` |
| `url` | string | optional | public link (if any) |
| `sha256` | string | optional | hash if available |

### 5.6 `timestamps`

| Field | Type | Required | Notes |
|---|---|---:|---|
| `issued_at` | string | yes | ISO8601 UTC |

---

## 6. Signature Model (Issuer)

### 6.1 Algorithms

- `Ed25519` signature over an issuer-defined canonical byte sequence
- Public key provided via anchor URL

### 6.2 Signatures Block

Minimum required fields:

| Field | Type | Required | Notes |
|---|---|---:|---|
| `canonicalization` | string | recommended | e.g., `JCS` (issuer-defined) |
| `issuer` | object | yes | issuer signature |
| `package_self_hash` | object | optional | hash of final package (file integrity) |

`signatures.issuer`:
| Field | Type | Required | Notes |
|---|---|---:|---|
| `alg` | string | yes | `Ed25519` |
| `pub` | string (URL) | yes | public key anchor URL |
| `sig` | string (base64) | yes | signature bytes |

### 6.3 Verification Minimum Requirement

A verifier MUST:
1) Fetch issuer public key from `signatures.issuer.pub`
2) Verify Ed25519 signature against issuer-defined signing payload

Other checks are optional.

---

## 7. Delivery Model

Issuer may provide:
- JSON package (`.json`)
- Human-readable HTML (`.html`)
- ZIP bundle (`.zip`)

Public delivery endpoints and naming are issuer-defined.

---

## 8. Freeze Governance

AuditVisa uses a layered governance model:

- **Core**: issuer-defined rules; stable; changes are rare and controlled.
- **Bridge**: integration helpers and convenience tooling.
- **Bridge-of-Bridge**: compatibility layers, adapters, cross-environment convergence attempts.

Non-essential modules that cannot be completed under limited iterations are moved to **Bridge-of-Bridge** by policy.

---

## 9. Trust Network Extensions (Deferred)

These are not required for v0.2 Core issuance and may be implemented later as a separate track.

### E1. Multi-node Signatures (Deferred)
Support multiple node signatures:
- `signatures.multi_node_signatures[]`

### E2. Third-party Verification (Deferred)
Allow third-party attestations:
- `signatures.third_party_verifications[]`

### E3. Chained Time Anchors (Deferred)
External time anchoring / chained logs:
- `timestamps.anchors[]` (issuer-defined format)

---

## 10. Change Log

- v0.2: issuer signature + proof package structure; trust network extensions deferred.
