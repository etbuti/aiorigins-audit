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



flowchart TB
  %% =========================
  %% AuditVisa Core + Trust Network + Agent Economy
  %% =========================

  subgraph EXT[Trust Network Expansion (Deferred / Commercial Activation)]
    MN[Multi-node Signatures<br/>E1]:::ext
    TP[Third-party Verification<br/>E2]:::ext
    TA[Chained Time Anchors<br/>E3]:::ext
  end

  subgraph BOB[Bridge-of-Bridge (Frozen / Optional)]
    CC[Cross-platform recomputation convergence<br/>(out of Core scope)]:::bob
    AD[Compatibility adapters / SDKs]:::bob
    TOOL[3rd-party tooling ecosystem]:::bob
  end

  subgraph BR[Bridge (Open for integration)]
    RV[Reference Verifier (browser/cli)]:::bridge
    API[Integration Interface / API endpoints]:::bridge
    DOC[Spec + Freeze Notice]:::bridge
  end

  subgraph CORE[AuditVisa Core (Frozen / Operational)]
    PK[Public Key Anchor<br/>/.well-known/auditvisa.pub]:::core
    IS[Issuer Signature<br/>Ed25519]:::core
    VID[VisaID Generation<br/>AV-YYYYMMDD-NODE-RUNHASH6]:::core
    PKG[Proof Package JSON<br/>auditvisa-v0.2.md spec]:::core
    DEL[Delivery Artifacts<br/>JSON / HTML / ZIP]:::core
    GOV[Core / Bridge Governance<br/>freeze policy]:::core
  end

  subgraph PIPE[Agent Pipeline (Running)]
    ST[Stripe Checkout / Events]:::pipe
    RUN[Runner Agent<br/>consume payloads]:::pipe
    WK[Audit Worker<br/>policy checks]:::pipe
    TM[systemd timer]:::pipe
  end

  subgraph WORLD[External World]
    TGT[Targets<br/>domains/endpoints]:::world
    CUS[Customers / Consumers<br/>humans + machines]:::world
    VER[External Verifiers]:::world
    ECO[Agent Economy / Node Ecosystem]:::world
  end

  %% pipeline wiring
  TM --> RUN
  ST --> RUN
  RUN --> WK
  WK --> PKG
  PKG --> IS
  IS --> DEL
  PK --> IS
  VID --> PKG
  GOV --> CORE

  %% delivery to consumers
  DEL --> CUS
  CUS --> VER

  %% verifiers use bridge
  VER --> RV
  RV --> DOC
  RV --> API

  %% divergence detection leads to Bridge-of-Bridge
  VER -. divergence possible .-> CC
  CC --> AD
  AD --> TOOL

  %% expansion attaches to core (optional)
  EXT -. attaches later .-> CORE
  MN -.-> PKG
  TP -.-> PKG
  TA -.-> PKG

  %% targets
  WORLD --> TGT
  TGT --> WK

  %% economy/ecosystem
  CUS --> ECO
  ECO -. future trust linking .-> EXT

  classDef core fill:#111827,stroke:#6b7280,color:#e5e7eb;
  classDef bridge fill:#0b1220,stroke:#93c5fd,color:#e5e7eb;
  classDef bob fill:#1f2937,stroke:#f59e0b,color:#fde68a;
  classDef ext fill:#0f172a,stroke:#34d399,color:#d1fae5;
  classDef pipe fill:#0b0d12,stroke:#a7b0c0,color:#e9eefc;
  classDef world fill:#0b0d12,stroke:#374151,color:#e9eefc;

