# Product brief — draft, 2026-11-17

## Interpretation of the sketch

Pathshala gives each teacher a Guru assistant and each student a Kshatra assistant. The student assistant tracks evidence, helps curate a personalized plan, and supplies permitted summaries to the teacher assistant. The teacher assistant helps the teacher inspect learning progress and adjust instruction. Personal workspaces have progress, insights, plans, classes and chat. The sketch also includes groups, integrations, a common board, visualizations and a friend/mitr concept; these are deferred from the initial scope.

The user selected coaching institutes as the first audience, a Python backend with LangChain/LangGraph, and a maximum INR 2,000 monthly AWS budget with mostly local labs. Next.js and A2UI remain the chosen frontend direction. Exact student ages, institute workflow, subject and deployment region remain unresolved.

## Assessment

The useful product is a feedback loop between a teacher and a learner. An agent chat is an interface; the product advantage would come from trusted learning evidence, good interventions and measurable improvement. This is a promising hypothesis, not a validated business. Interview an institute owner, teachers and learners before expanding scope. Existing substitutes include LMS dashboards, spreadsheets, messaging groups and general AI tutors; ask where they fail instead of assuming demand.

Proposed first scenario: one institute, one cohort, one subject, one teacher, a small consented pilot. Multiple institutes must still be represented in authorization tests from the beginning. Classes mean cohort membership, scheduled sessions and learning activities initially; building video conferencing is out of scope.

Student journey: see assigned goals → submit an attempt or self-report → receive a grounded explanation → inspect a proposed study plan → follow the teacher-approved plan. Teacher journey: inspect evidence from assigned students → review an insight with evidence references → approve/edit a plan → observe whether the intervention helped.

## What must be true

- Evidence has provenance: assessment result, rubric, attempt, timestamp, author and confidence/limitations. Completion and chat frequency do not establish mastery.
- Insight separates measured facts from model inference and abstains when evidence is insufficient.
- Plans are versioned drafts until the appropriate human approves them. No autonomous grade changes or consequential assessment decisions.
- A student can have several teachers or change cohorts. Authorization is a scoped relationship, not a rigid tree.
- A teacher may see agreed educational records for actively assigned students; private conversations are private by default. Shared summaries are distinct, permissioned records.
- AI roles do not mean a model process, pod or database per person. Start with two workflow configurations and isolated per-user state in shared services.

## Initial scope

Institute membership, teacher/student assignments, cohorts/classes, learning goals, assessment evidence, basic progress views, student plan drafts, teacher review and narrowly scoped assistant chat. The first implementation slice covers only workspace isolation; the next adds evidence and a deterministic progress view before using an LLM.

Defer social network, autonomous agent negotiation, custom video, marketplaces, cross-institute sharing, arbitrary integrations and autonomous curriculum changes.

## Questions for discovery

Which exam/subject and student age range? Who buys, who administers and who approves learning plans? Where do assessment data and rubrics come from? Which conversations may a teacher see? Is the INR 2,000 ceiling for AWS only, or AWS plus LLM/API costs? What current task wastes teacher time, and how much? Is mobile/low-bandwidth access essential?

If minors are included, resolve guardian involvement, retention, access and applicable data obligations before a live pilot. This draft makes no jurisdiction-specific legal conclusions.

## Proposed pilot evidence

Compare teacher planning time and intervention usefulness against the existing workflow. Measure learner plan completion separately from assessment performance; use baseline and follow-up assessments with a stable rubric. Track plan correction/rejection rate and cost per supported learner. Define numeric success thresholds with the pilot institute; do not manufacture them now.

Tenant leaks, unsupported evidence claims and unauthorized actions are release-blocking defects. A polished dashboard cannot compensate for them.
