# Pathshala draft working agreement

This directory preserves the Pathshala product drafts inside the engineering-playbook checkout. Reusable skills are in `../skills/`; this is not a separate Git repository. Keep product-specific rules scoped to this directory. Future application implementation belongs in a separate Pathshala repository.

The user is building for coaching institutes, wants a Python backend with agentic AI (LangGraph and appropriate LangChain integrations), Next.js plus A2UI, and an AWS learning budget of at most INR 2,000/month. No paid resources have been authorized by this documentation work.

Learning comes before implementation. Read `learning/README.md` and the active feature's learning record. Explain the mechanism, alternatives and failure modes; ask for a short teach-back; record the user's actual answer. Never manufacture understanding, approval, evaluation scores or completed checks. Continue independent analysis and specification work while waiting, but do not implement the dependent feature before the learner confirms readiness. A later explicit user instruction may change this preference.

Read `docs/product-brief.md` and the active spec before proposing changes. Drafts and proposed ADRs are not accepted decisions. Keep acceptance criteria traceable to evidence. Do not build the entire roadmap in one pass.

Reusable skills, when available at the local checkout, are routed explicitly:
- Understanding a concept: `../skills/learn-before-build/SKILL.md`
- Feature definition: `../skills/spec-driven-delivery/SKILL.md`
- HLD/LLD or technology selection: `../skills/architecture-tradeoffs/SKILL.md`
- Python agent workflows: `../skills/python-agent-workflows/SKILL.md`
- Release readiness: `../skills/production-readiness/SKILL.md`
- BMAD planning: `../skills/bmad-spec-workflow/SKILL.md`

If that checkout is absent, ask for its location before claiming the skills were applied. Record the exact skills commit used when implementation begins. Keep framework-generated files separate from product specifications; `specs/` owns feature behavior and `docs/decisions/` owns design decisions. BMAD cannot override the learning gate or tenant authorization rules.
