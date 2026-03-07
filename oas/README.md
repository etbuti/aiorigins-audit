## OAS System Architecture

```mermaid
flowchart LR

A[Target Domain]

A --> B[OAS Runner]

B --> C[Proof Package]

C --> D[manifest.json]
C --> E[Artifacts Evidence]

B --> F[Anchor Chain]

F --> G[anchor.log]
G --> H[hash chain]

D --> I[Verification Layer]

I --> J[CLI Verification]
I --> K[Web Verification]

G --> L[Public Anchor Sample]

L --> J
L --> K

J --> M[Independent Reproducible Proof]
K --> M
