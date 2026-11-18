# BMAD integration

Checked against official documentation on 2026-11-17. The upstream main documentation describes v7 preview alpha and separately points stable users to v6.12. The selected stable package is `bmad-method@6.12.4`, confirmed via npm metadata. Do not use v7 command names or directory assumptions with the stable installation.

Primary references:
- [Install guidance and stable/preview boundary](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/docs/start/install-bmad.md)
- [Release history](https://github.com/bmad-code-org/BMAD-METHOD/releases)
- [Spec Kit](https://github.com/github/spec-kit): a separate toolkit, not a prerequisite for using specifications.

Actual installer version, target, tool integration and verification status are recorded in `../frameworks.json`. Installation artifacts are upstream framework material; they do not replace the first-party skills. Keep upstream notices. No autonomous build loop is enabled by this project.

## Applying BMAD

Read the installed version's help and manifest before invoking commands. Use its analyst/product capabilities to challenge the product brief, architect capabilities to evaluate boundaries and alternatives, and story/review capabilities for one bounded feature. These are workflow responsibilities, not assumed command spellings. Use the exact commands present in the installed integration.

Canonical outputs stay in the product checkout. Record consumer scope in the prompt, use its working agreement, and promote reviewed decisions into the consumer's brief, spec and ADR. Implementation waits for the learner's teach-back. Do not let a generated 'approved' field count as the user's approval. Do not run unattended implementation or party mode merely because the framework offers it.

For later product integration, install the same pinned stable release in the product checkout only after checking its existing agent files and output configuration. The foundation installation here validates the framework/tool availability; product bootstrap is a separate step and should avoid copying the entire skills repository into the product history.

## Installed commands and smoke check

The local catalog confirms `bmad-help`, `bmad-product-brief`, `bmad-prd`, `bmad-spec`, `bmad-architecture`, `bmad-create-epics-and-stories` and `bmad-build`, among other skills. These names come from this installation, not an assumed older tutorial. Start with the brief/spec discussion; do not invoke Build before the consumer learning gate.

Installed: core and BMM 6.12.4; Codex integration with 29 generated skill entrypoints. The six first-party skills are linked beside them using repository-relative symlinks. Smoke check passed with the existing uv runtime:

```sh
uv run --offline _bmad/scripts/resolve_config.py --project-root .
```

Run from this repository. Personal installer answers are ignored in Git; fresh users supply their own. This is configuration/runtime verification, not a completed BMAD product session. The prior consumer drafts are preserved in `../product-draft/`. Use their canonical files for any continued product discussion; do not mix them with reusable workflow documentation. Future product implementation belongs in its own repository.
