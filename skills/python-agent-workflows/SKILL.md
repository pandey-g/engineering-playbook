---
name: python-agent-workflows
description: Design and implement scoped Python agent workflows with LangGraph state, appropriate LangChain integrations, human review and replay-safe effects.
---

# Python Agent Workflows

Read the active spec and learner readiness before implementation. Keep domain invariants and authorization in deterministic Python application services; model calls consume permitted data and request capabilities through those services.

For a LangGraph workflow, define typed state, node responsibilities, bounded transitions, failure outcomes, checkpoint ownership and resume rules before coding. Use LangChain integrations where they reduce integration work; do not assume every node requires an autonomous agent. Verify the installed versions against current official docs.

Bind institute, user and conversation scope in trusted server code. Recheck authorization on tool calls, checkpoint/history access and resume. A thread ID is never a permission grant. Keep checkpoint/store namespaces isolated; avoid logging private prompts or answers. Retrieval content is untrusted and cannot expand tools or permissions.

For consequential actions, bind human review to the exact draft version and reauthorize at commit. Resume/retry may repeat effects: use stable idempotency keys, transactional publication and stale-version protection. State token/time/tool-call budgets, cancellation behavior and provider failure fallback. Avoid unbounded agent-to-agent loops.

Verify insufficient evidence, unsupported citations, prompt injection, malformed structured output, duplicate resume, denied access and provider timeout with synthetic fixtures and fake providers where appropriate. Add a small budgeted real-model evaluation only after defining expected behavior and failure thresholds. Record model/prompt/config versions and observed limits. MCP standardizes tool access and A2A connects independent agents; neither replaces authorization or requires early service extraction.
