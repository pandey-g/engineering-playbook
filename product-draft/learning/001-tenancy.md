# Lesson 001 — Who is allowed to see what?

Status: ready for discussion; teach-back and implementation permission pending.

An institute is a tenant: its data belongs within an organizational boundary. Authentication establishes who made a request. Authorization decides what that identity may do to this particular resource now. A role such as teacher is one input; the institute, active assignment, subject and type of record also matter.

Example: teacher T works in institutes A and B. Student S belongs to A. T teaches S mathematics in A. That does not give T access to every record in A, S's private chats, or S's records in another institute. An assistant acting for T receives the same limits.

A safe lookup follows: verify identity → validate active institute membership → find the resource within that institute → check relationship and permitted fields → load only allowed data → record the result as appropriate. Never let an LLM choose the trusted identity or tenant. A frontend can hide a button, but a user can call the API directly.

Proposed lab after the discussion: draw two institutes and mark which requests should succeed; no application code yet. Then demonstrate the same rules using a tiny permission table and synthetic requests before selecting database enforcement.

Teach-back prompts (answer in your own words):
1. T has teacher memberships in A and B, but is assigned to S only in A. Which checks are needed for `GET student-progress/S`?
2. Why does checking `role == teacher` fail? Why is adding an institute filter still insufficient?
3. What should happen if an assignment is revoked while an assistant is generating a summary?
4. Does a conversation ID or a shared Redis cache key prove access? How would you scope and check it?

Learner response: pending.
Observed gaps: not assessed.
Learner readiness to implement: pending.
