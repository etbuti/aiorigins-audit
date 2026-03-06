AI Origins Protocol Specification v1.0

Sections:

Node Specification
/spec/node/v1

Network Specification
/spec/network/v1

Admission Specification
/spec/admission/v1

⸻

AI Origins Protocol

Version 1.0

Status: Draft v1.0
Network: AI Origins
Canonical Root: https://aiorigins.org/

⸻

1. Overview

AI Origins is a protocol‑led node network designed around three principles:
	1.	Identity first
	2.	Protocol compatibility over hardware standardisation
	3.	Separation between onboarding and trust layers

The network allows independently operated infrastructure to join through a shared specification rather than through a centralised hardware deployment model.

Nodes that comply with identity rules, transport compatibility, and admission verification may participate in the network.

⸻

2. Design Principles

2.1 Specification Network

AI Origins is not a hardware network.

It is a specification network.

Operators may deploy infrastructure using:
	•	VPS
	•	dedicated servers
	•	local mini computers
	•	colocated machines
	•	portable nodes

Hardware choice does not affect compatibility.

Protocol compliance does.

⸻

2.2 Identity‑based Participation

Nodes are defined through a machine‑readable identity document.

Example identity:

{
 "schema":"https://aiorigins.org/spec/node/v1",
 "node_id":"fixed-qingdao-01",
 "node_role":"fixed",
 "region":"CN-QD",
 "transport":{
   "type":"wireguard",
   "wg_address":"10.66.66.10/32",
   "endpoint":"qingdao.example.net:51820",
   "public_key":"BASE64_PUBLIC_KEY"
 }
}

Identity documents allow automated verification and discovery.

⸻

3. Network Roles

AI Origins defines several node roles.

3.1 Core Nodes

Core nodes act as:
	•	identity anchor
	•	protocol authority
	•	root discovery node

Example:

core-london

Core nodes are not publicly self‑registered.

⸻

3.2 Fixed Nodes

Fixed nodes are stable infrastructure nodes.

Characteristics:
	•	persistent connectivity
	•	stable geographic location
	•	production workloads

Example:

fixed-helsinki
fixed-qingdao


⸻

3.3 Mobile Nodes

Mobile nodes provide portable presence.

Use cases:
	•	travel nodes
	•	presence proofs
	•	lightweight services

Example:

mobile-evan


⸻

3.4 Reserve Nodes

Reserve nodes exist for:
	•	replacement
	•	redundancy
	•	infrastructure expansion

⸻

3.5 Edge and Service Nodes

Edge nodes provide public entry points.

Service nodes may run:
	•	APIs
	•	gateways
	•	compute services

⸻

4. Transport Layer

AI Origins uses a private mesh network.

Transport protocol:

WireGuard

Private network range:

10.66.66.0/24

Address allocation:

10.66.66.1      core
10.66.66.10‑19  fixed nodes
10.66.66.20‑29  mobile nodes
10.66.66.30‑39  reserve nodes
10.66.66.40‑49  edge/service nodes


⸻

5. Minimal Network Topology

Initial distributed topology:

            core-london
               │
      ┌────────┼────────┐
      │                 │
fixed-helsinki     fixed-qingdao

This topology marks the transition from a tunnel pair into a distributed node network.

⸻

6. Admission Model

Nodes must pass verification before activation.

Admission states:

PASS
WARN
FAIL

Meaning:

PASS → protocol compliant
WARN → acceptable with minor issues
FAIL → incompatible with rules

⸻

7. Join Flow

Typical onboarding process:

Read rules
→ prepare node.json
→ deploy infrastructure
→ run join‑check
→ PASS / WARN / FAIL
→ admission review
→ node activated


⸻

8. Discovery System

AI Origins exposes several machine‑readable entry points.

Root discovery:

/.well-known/ai-origins.json

Node identity:

/node.json

Portal description:

/portal.json

Agent entry:

/agent.json


⸻

9. Trust Layer

Trust verification is separated from onboarding.

Audit layer location:

/audit/

Principle:

preserve stable audit paths and extend protocol layers alongside them.

⸻

10. Portal Structure

The AI Origins portal provides human‑readable documentation.

/
/join/
/spec/
/rules/
/verify/
/nodes/
/audit/


⸻

11. Philosophy

AI Origins follows a simple operational rule:

hardware is optional; protocol compliance is essential.

The network grows through specification compatibility rather than centralised infrastructure deployment.

⸻

12. Status

AI Origins Protocol v1.0 represents the first stable definition of:
	•	node identity model
	•	mesh transport structure
	•	admission verification model
	•	machine discovery entrypoints

Future versions may extend the protocol while preserving compatibility with v1.

⸻

AI Origins Protocol v1.0
Protocol‑led node infrastructure
