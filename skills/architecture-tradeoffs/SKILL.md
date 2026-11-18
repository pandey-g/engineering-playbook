---
name: architecture-tradeoffs
description: Evaluate HLD, LLD and technology choices against product constraints, simpler alternatives, measured needs and operational cost.
---

# Architecture Tradeoffs

Read the confirmed audience, budget, desired learning goals and current design. Separate a technology learning objective from a production dependency; both are valid but have different adoption criteria.

At HLD level, identify actors, domain boundaries, sources of truth, trust boundaries, deployment shape and load assumptions. At LLD level, follow the active slice through API/event contracts, data invariants, transactions, authorization, idempotency and failure/recovery. Use `../../templates/design-adr.md` for material choices.

Compare a simpler alternative. State the benefit, operational burden, recurring cost assumptions and trigger for revisiting the choice. Do not turn every domain module into a service or every user agent into a pod. Existing architecture and user preferences constrain the comparison.

For a requested distributed tool without a current production need, propose a bounded synthetic-data lab using `../../templates/lab.md` and preserve its place in the learning roadmap. Promotion requires evidence rather than a technology checklist. Verify current official documentation before version-sensitive commands or cost recommendations. A budget alert is not a hard spend cap.
