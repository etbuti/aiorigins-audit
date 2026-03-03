AuditVisa Specification

⸻

Version 1.0 (Frozen)

Status: Active
Applies to: AuditVisa v0.2+ issuances
Authority: aiorigins.org

⸻

1. Purpose

AuditVisa defines a structured, machine-readable domain integrity snapshot.

Each issuance produces:
	•	A unique VisaID
	•	A JSON proof package
	•	A human-readable report
	•	Evidence references
	•	Immutable timestamps

This document freezes the identifier format, status enumeration, and JSON field structure.

⸻

2. VisaID Format (Frozen)
   AV-YYYYMMDD-NODE-RUNHASH
   Example:
   AV-20260303-AO-9C4B7E

   Components
Part                          Meaning
AV                            Product prefix (AuditVisa)
YYYYMMDD                      UTC issuance date
NODE                          Issuer node short code
RUNHASH                       Short hash derived from canonical package

RUNHASH Rule
	•	Derived from sha256(canonical_package_json)
	•	Encoded as uppercase hex
	•	First 6 characters used
	•	Deterministic and reproducible

VisaID must remain immutable once issued.

⸻

3. Status Enumeration (Frozen)

Package-level status
PASS
WARN
FAIL

Meaning:
Status        Definition
PASS          All critical checks passed
WARN          No critical failures, but warnings exist
FAIL          At least one high-severity failure

Check-level status
PASS
WARN
FAIL
SKIP

SKIP is reserved for controlled omission.

No other values are permitted.

⸻

4. Severity Levels
   info
low
medium
high
critical (reserved)

Severity classification must be explicit per check.

⸻

5. JSON Field Structure (Frozen)

Top-level required fields:
schema
kind
version
visa_id
status
summary
header
target
policy
checks
evidence
artifacts
signatures
timestamps

Field names are case-sensitive and immutable.

No renaming is permitted in future minor versions.

⸻

6. Timestamp Standard

All timestamps must:
	•	Use UTC
	•	Use ISO 8601 format
	•	End with Z
	•	Be immutable once issued

Example:
2026-03-03T06:12:16Z

⸻

7. Canonicalization Rule

The canonical JSON used for hashing:
	•	Must exclude transport formatting
	•	Must be deterministically ordered
	•	Must not change after issuance

Hash derivation must be reproducible by third parties.

⸻

8. Immutability Rule

Once a VisaID is issued:
	•	JSON package must not change
	•	Status must not change
	•	Evidence must not be edited
	•	Timestamps must not be altered

Corrections require a new VisaID issuance.

⸻

9. Policy Enforcement

If a target violates policy (protocol or host restriction):
	•	Status must be FAIL
	•	Evidence must document the block
	•	VisaID must still be issued

No silent rejection is permitted.

⸻

10. Human Override

AuditVisa operates as an automated issuance system.

Human intervention is permitted only for:
	•	Non-delivery cases
	•	Infrastructure failure
	•	System malfunction

Manual alteration of issued data is prohibited.

⸻

11. Forward Compatibility

Future extensions may add:
	•	Multi-node signatures
	•	Third-party verification blocks
	•	Chain-based time anchoring
	•	Cross-node attestations

Such extensions must not break:
	•	VisaID format
	•	Status enumeration
	•	Existing field names

⸻

12. Versioning Policy

Minor version updates:
	•	May add fields
	•	May add check types
	•	May extend signature blocks

Major version updates:
	•	May introduce structural redesign
	•	Must not retroactively alter issued packages

⸻

13. Authority

This specification is governed by:
https://aiorigins.org/

Specification freeze date:
2026-03-03 (UTC)

Evanbei
London
