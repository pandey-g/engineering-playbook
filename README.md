# Engineering Playbook

Reusable engineering skills, BMAD workflows and spec-driven templates for learning-first development. This checkout uses the existing engineering-playbook GitHub remote. Product code and specifications will ultimately live in their own repository. Existing Pathshala planning work is preserved temporarily in [product-draft/](product-draft/README.md), as requested when moving all work here.

## Start here

1. Read [workflow](docs/workflow.md). Start a bounded concept using `skills/learn-before-build/SKILL.md`.
2. Use BMAD for guided discovery/design when helpful, and `skills/spec-driven-delivery/SKILL.md` to maintain the canonical feature specification. Read [BMAD integration](docs/bmad-integration.md) for installation evidence and version boundaries.
3. Produce a learning record, spec and appropriate design; receive the learner's real teach-back before implementation.
4. Implement one slice, demonstrate acceptance and failure behavior, then assess readiness proportionately.

## Skills

| Skill | Use |
|---|---|
| `learn-before-build` | Explain a concept, elicit teach-back and record readiness |
| `spec-driven-delivery` | Convert a bounded outcome into testable behavior and implementation evidence |
| `architecture-tradeoffs` | HLD/LLD and evidence-based technology adoption |
| `python-agent-workflows` | Durable, scoped Python/LangGraph agent workflows |
| `production-readiness` | Review operational and agent readiness against a defined release |
| `bmad-spec-workflow` | Combine BMAD conversations with one canonical specification set |

Six relative symlinks in `.agents/skills/` expose the first-party skills for repository-local discovery alongside the 29 generated BMAD skills. Read a selected `skills/<name>/SKILL.md` directly when explicit routing is needed. The consuming product's `AGENTS.md` can route to the checkout as the preserved product draft does. These files are not automatically installed as global Codex skills. Native installation can be done later with the supported skill installer after choosing installation scope; no global settings were changed here.

`templates/` provides feature specs, design/ADR, learning records, delivery evidence and lab plans. Copy only what a slice needs. Pin this repository's commit in the consuming project's workflow record when implementation starts. Updates are reviewed deliberately rather than silently changing every project.

Framework installation does not mean it has been exercised on a product or that any plan is accepted. See `frameworks.json` for actual installation state. No Spec Kit CLI is installed: spec-driven development here is the engineering method, with first-party templates. A second framework can be evaluated later if it provides a concrete benefit.

Migration: all Gurukul work was moved here on 2026-11-18. Original local Git histories and the initial destination README are retained in the ignored `.migration-backups/gurukul-2026-11-18/` directory. The existing GitHub checkout history and remote were preserved; nothing was pushed.
