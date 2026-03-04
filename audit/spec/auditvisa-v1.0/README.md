Architecture Map

AuditVisa Core Architecture v1.0

                         ┌──────────────────────────┐
                         │        Internet          │
                         │   Domains / Targets      │
                         └────────────┬─────────────┘
                                      │
                                      │ scan
                                      ▼
                         ┌──────────────────────────┐
                         │     Audit Worker         │
                         │  policy / checks / run   │
                         └────────────┬─────────────┘
                                      │
                                      │ evidence
                                      ▼
                         ┌──────────────────────────┐
                         │      Runner Agent        │
                         │ consume Stripe payload   │
                         │ build proof package      │
                         └────────────┬─────────────┘
                                      │
                                      │ package.json
                                      ▼
                         ┌──────────────────────────┐
                         │     AuditVisa Core       │
                         │                          │
                         │  JSON package structure  │
                         │  VisaID generation       │
                         │  Ed25519 issuer sign     │
                         │                          │
                         └────────────┬─────────────┘
                                      │
                                      │ delivery
                                      ▼
                         ┌──────────────────────────┐
                         │        Delivery          │
                         │                          │
                         │   JSON proof package     │
                         │   HTML report            │
                         │   ZIP bundle             │
                         │                          │
                         └────────────┬─────────────┘
                                      │
                                      │ public access
                                      ▼
                         ┌──────────────────────────┐
                         │        Consumers         │
                         │                          │
                         │   humans / machines      │
                         │   automated systems      │
                         └────────────┬─────────────┘
                                      │
                                      │ verify
                                      ▼
                         ┌──────────────────────────┐
                         │        Verifiers         │
                         │                          │
                         │  issuer signature check  │
                         │  optional recomputation  │
                         └────────────┬─────────────┘
                                      │
                                      │ divergence possible
                                      ▼
                     ┌──────────────────────────────────────┐
                     │        Bridge-of-Bridge Layer        │
                     │                                      │
                     │ cross-platform recomputation         │
                     │ compatibility adapters               │
                     │ third-party tooling                  │
                     │                                      │
                     │ (NOT required for issuance)          │
                     └──────────────────────────────────────┘


