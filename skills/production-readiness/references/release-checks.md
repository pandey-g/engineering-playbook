# Release evidence prompts

Select relevant checks for the release and state why omitted checks do not apply.

- Access: cross-tenant IDs, nested/list/export queries, student privacy, revocation, worker/tool/checkpoint/history and stream authorization; tests include a legitimate allowed path.
- Data: constraints, migration/rollback or forward-fix strategy, retention/deletion including derived records and backups, backup restore and measured RPO/RTO against agreed objectives.
- Agents: grounded claims, insufficient-evidence response, injection, scoped capabilities, human approval, exact plan-version binding, idempotent resume, budgets and provider outage. Quality thresholds must exist before live-model evaluation.
- Operations: TLS, secrets handling, IAM, restricted network exposure, deploy/rollback evidence, actionable alerts and correlation across API/jobs/model calls without private content.
- Reliability: agreed pilot load, latency/error goals, timeout/cancellation, bounded retries, duplicate work, stale caches, disconnect and recovery, dependency outage.
- Cost: region-specific estimate, runtime hours, compute/disk/database/IPv4/NAT/LB/logs/egress/backups/model charges, alerts, teardown and realistic cap limitations.
- Experience: ordinary workflows, loading/empty/error states, accessibility, agent rendering fallback, misleading insights and human correction paths.
- Ownership: operator, incident path, support expectations, known limitations and actual acceptance by the appropriate person.

Record commands/demonstrations, observed results, dates and limitations. Unknown is a valid finding; it is not a pass.
