# 001 — Institute and workspace isolation

Status: draft. Learning gate: pending. Implementation: not started.

## Problem and outcome

An institute member needs a personal workspace. A teacher needs scoped educational records for currently assigned students. Neither path may expose other institutes or private student conversations.

## Scope and terms

Institute = tenant; user = authenticated person; membership = role within an institute; assignment = explicit active teacher/student/cohort/subject relationship with scope and validity. Student and teacher AI execute delegated user capabilities, never broader authority. Institute administrator can manage memberships; educational content access is a separate permission, not implied by administrator status.

The active institute is validated against current membership on every request. All protected objects, joins, search results, exports, background jobs, agent state and stream subscriptions retain tenant context. Student sharing scope defaults to educational evidence and approved shared summaries only; exact field policy remains a clarification before implementation.

## Acceptance criteria

- AC-01: Given memberships in institutes A and B, when a student in A requests a protected B record by guessed ID, then return a consistent denial/not-found response without record metadata.
- AC-02: Given an active scoped assignment in A, when its teacher requests the permitted progress fields for that student and subject, then only those fields are returned.
- AC-03: Given an assignment was revoked, when the teacher, an existing agent run or a stream next attempts protected access, then no new protected data is returned. Queued work reauthorizes before loading and before publishing.
- AC-04: Given a teacher requests a student's private conversation, then deny even if assigned; a deliberately shared summary is independently permissioned.
- AC-05: Given an authenticated student, then their own workspace is accessible but another student's workspace is denied. A teacher in institute A cannot reuse their A role in institute B.
- AC-06: Given a client/model supplies another institute ID, learner ID or thread ID, then trusted authorization prevents impersonation and cross-tenant checkpoint/history access.
- AC-07: Given a write connects records from different institutes, then database constraints reject the relationship, including worker/tool writes.
- AC-08: Given an access denial or assignment change, then an audit event records actor, institute, action, resource reference, result, time and correlation ID without private content or credentials.
- AC-09: Given paginated/list/search/export endpoints, then unauthorized records and their counts, snippets and references are excluded.

## Invariants

No protected lookup by bare object ID without authorized scope. Role is interpreted within a verified membership. Permission is evaluated in application code and database policy if adopted; prompts are never the enforcement layer. UI hiding is not authorization. Revocation must cover cache, jobs, history and open streams. Revocation cannot erase data legitimately delivered earlier.

## Evidence plan

Two synthetic institutes, a multi-institute user, two teachers and several students. Map each AC to integration/security evidence. Exercise direct API access, nested joins, forged IDs, assignment revocation during a job, cache access after revocation and checkpoint history. Include constrained database writes. Verify the normal teacher/student journeys alongside negative cases. No real student data needed.

## Open decisions before implementation

Student ages; identity/session design; initial role and field-access matrix; how scope changes invalidate open streams and caches; whether learners can approve additional sharing; cohort versus direct assignments; database RLS policy and pool behavior. Agree on deployment/service targets separately before a hosted pilot.

## Out of scope

AI generation, payments, autonomous plan publication, guardian portal, video, social features and cross-institute sharing. This slice is a foundation, not the whole product.
