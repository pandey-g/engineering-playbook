# One delivery workflow

## Source of truth

Consumer `docs/product-brief.md`: audience, problem, outcomes and scope.
Consumer `specs/<feature>/spec.md`: externally visible behavior, invariants and acceptance criteria.
Consumer `docs/decisions/`: accepted/proposed architecture decisions with status.
Consumer `specs/<feature>/design.md`: slice-level contracts, data and execution flow when needed.
Consumer `learning/`: the learner's answers, remaining gaps and readiness decisions.
Consumer `specs/<feature>/evidence.md`: implementation changes and observed validation.

BMAD produces structured conversations and candidate artifacts. Link or promote their conclusions into the appropriate canonical document; do not maintain a second independently edited feature contract. Preserve unresolved questions explicitly.

## Progression

Discovery → bounded behavior draft → concept explanation and comparison → learner teach-back → refine design and acceptance criteria → implement one slice → demonstrate normal and failure paths → record evidence → assess next step.

Teach-back is required before dependent implementation because this consumer explicitly wants understanding first. It is not a requirement to seek approval for routine file edits. Continue research, specifications and unrelated authorized work while waiting. The learner can explicitly change the gate.

A change starts with a concrete user outcome. Identify the concepts actually needed; avoid teaching an entire platform to change one endpoint. Explain data flow, alternatives and the failure mode the design addresses. Record the learner's words and gaps; do not substitute model-written answers. When ready, draft minimal tasks with AC references. Use meaningful behavioral/integration tests for data and security boundaries. Simple reversible documentation changes need link/frontmatter checks, not a test suite.

At the end, state what works, what was verified, what remains uncertain and whether the next feature's learning gate is pending. A checklist, passing unit tests or a framework review alone cannot establish production readiness.
