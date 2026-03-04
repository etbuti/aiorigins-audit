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
  MN[Multi node signatures E1]
  TP[Third party verification E2]
  TA[Chained time anchors E3]
end

subgraph BOB[Bridge of Bridge]
  CC[Cross platform recomputation]
  AD[Compatibility adapters]
  TOOL[Third party tooling]
end

subgraph BR[Bridge]
  RV[Reference verifier]
  API[Integration interface]
  DOC[Spec and freeze notice]
end

subgraph CORE[AuditVisa Core]
  PK[Public key anchor well known auditvisa pub]
  IS[Issuer signature Ed25519]
  VID[VisaID AV YYYYMMDD NODE RUNHASH6]
  PKG[Proof package JSON spec v0 2]
  DEL[Delivery JSON HTML ZIP]
  GOV[Governance Core Bridge Bridge of Bridge]
end

subgraph PIPE[Agent pipeline]
  TM[Systemd timer]
  ST[Stripe events]
  RUN[Runner agent]
  WK[Audit worker]
end

subgraph WORLD[External world]
  TGT[Targets domains endpoints]
  CUS[Consumers humans machines]
  VER[External verifiers]
  ECO[Node ecosystem]
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


