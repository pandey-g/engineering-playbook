# ADR 0001 — Learning-first foundation

Status: proposed; user constraints below are confirmed, technical choices await learning/design review.

Confirmed: coaching institutes; Python and agentic AI including LangChain/LangGraph; Next.js/A2UI; AWS learning ceiling INR 2,000/month; independent skills repository; understand before implementing.

Proposed: Python/FastAPI modular monolith, PostgreSQL source of truth, scoped LangGraph workflows, local-first labs and incremental cloud exercises. Use BMAD for guided product/design conversations and specifications as the behavioral contract. Avoid two competing PRDs/spec trees. Pin actual framework versions and record installation evidence.

Alternatives: microservices from day one adds delivery/security/operations overhead; all-in Next.js conflicts with the chosen Python learning direction; a fully managed high-availability AWS deployment needs a cost estimate and may exceed the budget.

Consequences: distributed tools are learned later in isolated labs; early iterations optimize reliable learning evidence and tenant boundaries. Live production availability is not promised at the current budget.

Revisit on pilot requirements, measured scale, a new operating budget or explicit user preference. Acceptance and rationale will be recorded after review; this file does not claim user approval of the proposed stack.
