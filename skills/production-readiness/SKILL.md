---
name: production-readiness
description: Assess a specific release against operational, data, security and agent-quality evidence; use for release or pilot readiness reviews.
---

# Production Readiness

Read the release scope, service objectives, deployment budget and evidence. Review what the release actually needs; do not add a whole enterprise platform to a small pilot. Use `references/release-checks.md` for applicable prompts, then report demonstrated, missing and explicitly accepted limits.

A proposed architecture, generated checklist, installed framework or passing unit suite is not production certification. Require observable evidence for material risks. State blockers concretely and distinguish unresolved tests from confirmed defects. A low-cost single-instance lab has availability limits even if application code is robust. Do not approve paid infrastructure implicitly or invent a user's acceptance of operational risk.
