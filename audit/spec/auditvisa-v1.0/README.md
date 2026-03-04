Architecture Map

# AuditVisa Core Architecture v1.0

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



## Architecture Diagramflowchart TB

The following diagram shows the relationship between:

- Core issuance layer
- Bridge and Bridge-of-Bridge governance
- Agent pipeline
- Trust network expansion

```mermaid
flowchart TB

  subgraph EXT[Trust Network Expansion]
    MN[Multi-node Signatures (E1)]
    TP[Third-party Verification (E2)]
    TA[Chained Time Anchors (E3)]
  end

  subgraph BOB[Bridge-of-Bridge]
    CC[Cross-platform recomputation convergence]
    AD[Compatibility adapters / SDKs]
    TOOL[3rd-party tooling ecosystem]
  end

  subgraph BR[Bridge]
    RV[Reference Verifier (browser/cli)]
    API[Integration Interface / API endpoints]
    DOC[Spec + Freeze Notice]
  end

  subgraph CORE[AuditVisa Core]
    PK[Public Key Anchor: /.well-known/auditvisa.pub]
    IS[Issuer Signature: Ed25519]
    VID[VisaID: AV-YYYYMMDD-NODE-RUNHASH6]
    PKG[Proof Package JSON (spec v0.2)]
    DEL[Delivery: JSON / HTML / ZIP]
    GOV[Governance: Core / Bridge / Bridge-of-Bridge]
  end

  subgraph PIPE[Agent Pipeline]
    TM[systemd timer]
    ST[Stripe events]
    RUN[Runner agent]
    WK[Audit worker]
  end

  subgraph WORLD[External World]
    TGT[Targets: domains / endpoints]
    CUS[Consumers: humans + machines]
    VER[External verifiers]
    ECO[Node ecosystem / agent economy]
  end

  TM --> RUN
  ST --> RUN
  RUN --> WK
  TGT --> WK

  WK --> PKG
  VID --> PKG
  PK --> IS
  PKG --> IS
  IS --> DEL

  DEL --> CUS
  CUS --> VER

  VER --> RV
  RV --> DOC
  RV --> API

  VER -. divergence possible .-> CC
  CC --> AD
  AD --> TOOL

  EXT -. deferred .-> CORE
  MN -. attaches .-> PKG
  TP -. attaches .-> PKG
  TA -. attaches .-> PKG

  CUS --> ECO
  ECO -. future trust linking .-> EXT


