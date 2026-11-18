---
name: spec-driven-delivery
description: Define and deliver a bounded feature from explicit behavior, invariants and traceable acceptance evidence; use for spec-driven product changes.
---

# Spec Driven Delivery

Read the consumer brief, working agreement and current feature spec. Clarify the user outcome, scope and trust boundaries. Use `../../templates/feature-spec.md` when starting a feature. Mark assumptions and unresolved decisions instead of inventing product requirements.

Write observable acceptance criteria before implementation, with concrete success and relevant failure/denial cases. Link concepts requiring learning to their actual records. For substantial design choices, use `../../templates/design-adr.md`; avoid a separate design document for a trivial edit.

Keep a single canonical behavior specification even when BMAD or another framework supplies drafts. Preserve accepted intent and update criteria before implementing a behavior change. In learning-first consumers, respect the actual learner gate; a generated 'ready' status cannot satisfy it.

Implement one vertical slice and map substantive criteria to meaningful demonstrations/tests. Record observed results and unverified limits using `../../templates/delivery-evidence.md` where useful. Do not claim tests were run or that production readiness follows from passing tests. Keep framework scaffolding and unrelated roadmap features out of the change.
