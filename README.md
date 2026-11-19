# Engineering Playbook

Reusable engineering skills and templates for coding agents. Install selected workflows as real files in your application repository, commit them alongside your code, and update them explicitly when you choose.

No submodule, symlink, global agent configuration or permanent external checkout is required in the consuming repository. Your application's technology choices and project instructions remain its own.

## Set up your existing `xyz` repository

Prerequisites: Python 3.9+ and Git. macOS, Linux and Windows can use the Python script; substitute your Python command if needed. No Python packages are required. You need access to this repository to clone it or fetch updates.

Clone the playbook once, outside `xyz`, or use your existing checkout:

```sh
git clone https://github.com/pandey-g/engineering-playbook.git
cd engineering-playbook
```

Install the three starting workflows into your already-cloned application repository. Replace `/path/to/xyz` with its root directory:

```sh
python3 scripts/sync-playbook.py \
  --target /path/to/xyz \
  --skills learn-before-build spec-driven-delivery architecture-tradeoffs
```

This initial command copies from the local playbook working tree. It records the full source commit and file hashes; if the source has uncommitted changes, it reports that and records `source_dirty: true`. Commit and publish playbook changes before expecting them to be available through remote updates.

The installer creates:

```text
xyz/
├── AGENTS.md
├── .agents/
│   ├── skills/
│   │   ├── learn-before-build/SKILL.md
│   │   ├── spec-driven-delivery/SKILL.md
│   │   └── architecture-tradeoffs/SKILL.md
│   ├── templates/                 # Only templates needed by selected skills
│   └── playbook-lock.json         # Source, commit, selection and file hashes
├── scripts/
│   └── sync-playbook.py           # Standalone updater
└── your application files
```

Skills' nested resources are copied too. Their relative references continue to work: for example, `../../templates/feature-spec.md` from `.agents/skills/spec-driven-delivery/` resolves to `.agents/templates/feature-spec.md`.

The installer appends a marked playbook section to an existing `AGENTS.md`, preserving its existing content. If the file is absent, it creates it. It does **not** copy this repository's maintainer instructions or product drafts into your application.

Keep project-specific instructions outside the managed markers. Add your actual install, run and test commands, technology choices, and working agreement there. For learning-first development, include:

```markdown
Learning comes before implementation in this project. Explain the concepts
needed for a bounded change, ask for my teach-back, and wait for my explicit
readiness before implementing dependent behavior. Continue independent
research and specification work while waiting.
```

Review and commit the installation from `xyz`:

```sh
cd /path/to/xyz
git status --short
git diff
git add AGENTS.md .agents/playbook-lock.json .agents/skills .agents/templates scripts/sync-playbook.py
git diff --cached
git commit -m "Add project engineering workflows"
```

Inspect untracked files before staging; `git diff` alone does not show their contents. If your project already has unrelated files under `.agents/skills/` or `.agents/templates/`, stage only the installed files listed by the installer. Check that your ignore rules permit these files to be committed. Push through your usual process. A normal clone of `xyz` then includes the installed workflows; teammates do not need the playbook checkout.

## Use the workflows with your agent

Open **`xyz`**, rather than the playbook repository, in Codex or VS Code with the Codex extension. Start a new agent session after setting up instructions. Codex reads applicable `AGENTS.md` files and discovers skill metadata under `.agents/skills/`; it loads a selected skill's full instructions when needed. See the official [AGENTS.md guidance](https://learn.chatgpt.com/docs/agent-configuration/agents-md) and [skills documentation](https://learn.chatgpt.com/docs/build-skills).

Verify the setup with:

> Read this repository's AGENTS.md. List the installed playbook skills and the paths you read, explain the project's learning agreement, and report missing resources. Do not change files.

Then give a concrete task:

> Use learn-before-build and spec-driven-delivery to help me add login. Inspect the existing authentication code, define one bounded behavior, and explain the concepts I need before implementation.

For architecture decisions:

> Use architecture-tradeoffs to compare the options for background jobs in this project. Start with our requirements and the simplest workable option.

For other coding agents or other VS Code extensions, discovery depends on the tool. Do not assume every extension reads `AGENTS.md` or `.agents/skills/` automatically. Use the tool's supported project-instruction mechanism to point to `AGENTS.md`, or begin with:

> Read AGENTS.md and the relevant SKILL.md under .agents/skills/ before working. Follow the project agreement and read the skill's supporting resources when needed.

The agent must have local file access. A plain chat interface needs the relevant files supplied as context. Files are instructions, not enforcement; verify the agent's reported sources and work.

## Check and apply updates

From `xyz`, check the configured source's default branch without changing project files:

```sh
python3 scripts/sync-playbook.py --check
```

Exit codes: `0` means current, `1` means updates are available, and `2` means an error or local conflict. Checks fetch into a temporary directory and do not modify the consumer. Checking requires Git access to the configured source; ordinary skill use works offline.

Apply updates when ready:

```sh
python3 scripts/sync-playbook.py --update
git diff
```

Review and commit the changed files, including the lock file, through your normal workflow. The updater also updates its own copied script; fetched Python is not executed during the current update. Only use a source you trust, and review script changes before the next run.

Use a particular tag or full commit instead of the default branch when desired:

```sh
python3 scripts/sync-playbook.py --check --ref <tag-or-full-commit>
python3 scripts/sync-playbook.py --update --ref <tag-or-full-commit>
```

`--ref` applies to that invocation. The lock records the installed commit; a later update without `--ref` checks the default branch again.

For an unpublished or offline source, fetch from a local playbook Git checkout:

```sh
python3 scripts/sync-playbook.py --update --source /path/to/engineering-playbook
```

Updates use **committed** source content, even for a local checkout. A successful update stores the chosen source for subsequent runs. A local source path is specific to your machine; restore the shared Git URL before committing the lock for teammates:

```sh
python3 scripts/sync-playbook.py --update \
  --source https://github.com/pandey-g/engineering-playbook.git
```

The initial local installation configures that shared GitHub URL by default. To install committed content from another source initially, pass `--source` with `--target`.

### Change the selected skills

Pass the **complete desired selection**, not just the additions:

```sh
python3 scripts/sync-playbook.py --update \
  --skills learn-before-build spec-driven-delivery architecture-tradeoffs production-readiness
```

You can preview this with `--check` instead. Updates remove unchanged managed files no longer needed by the selection, preserve unrelated files, and update the routes in `AGENTS.md`. Empty directories can remain.

### Resolve a local conflict

The updater stops before writing any files if a managed file was locally edited or deleted, a new destination already contains an unmanaged file, or the managed `AGENTS.md` section changed. Symlinked managed paths are rejected. It never silently replaces local customizations.

Keep project-specific rules outside the `AGENTS.md` markers and keep your own skills under distinct names. If a managed file needs customization, save the change elsewhere or contribute it to the playbook. Once your installation is committed, you can restore an individual managed file from Git after saving any desired edits, then retry the update. There is no force-overwrite option.

Keep `.agents/playbook-lock.json` with the managed files. Deleting it does not uninstall the playbook; existing files will be treated as unmanaged collisions. For reverting an update, restore its managed file changes and lock together using Git.

Text checksums tolerate Git's LF/CRLF line-ending conversion across machines. Other text changes remain conflicts; binary resources are compared without newline conversion.

## Available skills

| Skill | Use | Copy installer |
|---|---|---|
| `learn-before-build` | Explain a bounded concept, elicit teach-back and record readiness | Supported |
| `spec-driven-delivery` | Define observable behavior and trace acceptance to evidence | Supported |
| `architecture-tradeoffs` | Evaluate HLD/LLD, simpler alternatives and technology choices | Supported |
| `python-agent-workflows` | Scoped Python/LangGraph workflows and replay-safe effects | Supported |
| `production-readiness` | Assess operational, data, security and agent evidence | Supported |
| `bmad-spec-workflow` | Combine installed BMAD workflows with canonical specs | Separate BMAD setup |

Omitting `--skills` during initial installation selects the first three. The install includes only selected first-party skills, their declared templates, the instructions section, updater and lock. It excludes `_bmad/`, generated BMAD skills and `product-draft/`.

## Workflow and optional BMAD

Read [the delivery workflow](docs/workflow.md) for the learning-first progression. Product briefs, feature specs, decisions, learning records and evidence belong in the consuming repository. Templates prompt substantive decisions; generated plans do not establish approval or production readiness.

BMAD is optional. The existing installation in this checkout is recorded in [frameworks.json](frameworks.json); it does not install BMAD into `xyz`. Generated BMAD skills need framework files and project-specific configuration, so the copy installer rejects them and `bmad-spec-workflow`. Follow [BMAD integration](docs/bmad-integration.md) for a separate version-aware setup that preserves the consumer's instructions and learning gate. No Spec Kit CLI or unattended loop is installed by the copy tool.

Existing Pathshala planning drafts are temporarily retained under [product-draft/](product-draft/README.md). They are not part of the reusable installation.

## Maintaining the installer

`playbook.json` declares installable skills and required templates. A skill's whole folder is copied, including references and scripts; add any shared templates to its manifest entry. Preserve relative resource paths when adding dependencies. `templates/consumer-agents.md` defines only the managed instructions section; `scripts/sync-playbook.py` handles initial installation and subsequent updates.

Run the integration tests with disposable local Git repositories:

```sh
python3 -m unittest discover -s tests -v
```

The tests cover installation, resources, updates, read-only checks, commit selection, conflict handling, instruction preservation, skill selection changes and recovery from a write failure. They do not require network access or change global settings.
