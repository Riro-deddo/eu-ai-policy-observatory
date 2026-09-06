# Evidence corrections implementation plan

> **For agentic workers:** Use superpowers:subagent-driven-development to implement this plan. Steps use checkbox syntax for progress tracking.

**Goal:** Apply the approved, evidence-backed corrections from the 26-record audit locally, without changing the evidence contract or publishing remotely.

**Architecture:** Canonical JSON remains the source of truth. Existing pipeline and historical-publication compatibility rules consume complete evidence extensions. This is a data correction, not a schema migration.

**Spec:** User-approved scope and `../../../../evidence-review-26-20260906/report.md`, with the four underlying audit ledgers and preserved official-source evidence.

**Technology:** Python, JSON Schema, pytest; existing static data export.

## Global constraints

- Work in the existing directory with user approval. Preserve every unrelated pre-existing change. Use the byte snapshot at `../evidence-corrections-20260906/before` as the change baseline; local Git HEAD predates the current content.
- Keep all 186 document IDs and slugs; do not delete records, alter prior verified document files, change schema/validators, or modify web UI.
- No commit, push, merge, deployment, broad staging, or destructive cleanup in this task.
- Keep all project prose English. Preserve the public attribution `Reviewed by — Yichen Hao`; do not rewrite audit history or claim new personal review by the user.
- A verified flag requires the complete existing evidence extension and passing checks, not merely a discovered date. Publication means the exact officially dated manifestation, not necessarily first-ever release.
- Unresolved dates, GPAI version identities, ECB chronology, and three draft-section parent relationships remain pending. Do not infer a parent, replace an original with a later version, or promote a procedural note into adopted law.
- Previously authored audit ledgers remain immutable. Add a new dated ledger that records evidence, decisions, file hashes, upgraded IDs and retained holds.

## Task 1: Apply the bounded evidence-correction batch

### Files and inputs

Read this brief first; it contains the task requirements. Repository is `eu-ai-policy-observatory-isolated`. Read `docs/historical-readiness.md`, `schema/historical-document-extension.schema.json`, the applicable record/vocabulary definitions, and verified Council examples before editing. Read the audit's `council-2022.json`, `council-later.json`, `eurlex-root.json`, `commission.json`, and `op-spotchecks.json`. Same-day downloaded evidence is in that audit folder. Preparation reports `council-implementation-prep.md` and `test-implementation-prep.md` may assist but are claims, not new authority.

Admit the following seven records if all extension fields are supported under the existing contract:

| Document ID | Exact OP publication date | OP publication UUID |
| --- | --- | --- |
| ai-act-council-general-approach-st-15698-2022 | 2022-12-06 | fd86e2b0-758c-11ed-9887-01aa75ed71a1 |
| ai-act-council-adoption-note-st-9645-2024-rev-1 | 2024-05-15 | e80c49bd-12d8-11ef-a251-01aa75ed71a1 |
| ai-act-council-adoption-statements-st-9645-add-1-rev-2 | 2024-05-15 | b1da3f85-143f-11ef-a251-01aa75ed71a1 |
| ai-omnibus-council-adoption-note-st-10752-2026 | 2026-06-22 | 10220a8a-6fa1-11f1-ae88-01aa75ed71a1 |
| ai-omnibus-council-adoption-statement-st-10752-add-2 | 2026-06-24 | f76aad95-7089-11f1-9800-01aa75ed71a1 |
| ai-omnibus-council-information-note-st-10599-2026 | 2026-06-17 | 37937497-6b1d-11f1-ae88-01aa75ed71a1 |
| ai-act-consolidated-2026-07-27 | 2026-07-27 | b1730fb2-8f1c-11f1-9262-01aa75ed71a1 |

OP URLs have form `https://op.europa.eu/en/publication-detail/-/publication/<UUID>/language-en`. Declare seven exact OP sources using source IDs derived from the record ID plus `-op-publication`; use preserved real retrieval timestamps, not fabricated current retrievals. Record local evidence hashes in the new audit ledger.

For these records correct full official titles using the official cover/catalogue, preserving short titles and routes. Cite each date, classification and institution role precisely. Use named bibliographic authors France/Austria and Greece for their substantive statements; Council/GSC hosting and transmission are separate roles. Do not invent member-state institution entities. A statement may use only `officially_published` provenance when no EU substantive author is evidenced.

For ST 10599 distinguish the Council wrapper of 17 June from the enclosed Parliament resolution of 16 June. For ST 10752 correct any relationship rationale claiming completed adoption: the note recommends adoption conditionally. Preserve its procedure connection.

For the consolidation preserve 27 July consolidation date and underlying-law `in_force` status, but explicitly explain the documentary text has no independent legal effect. Preserve Parliament/Council roles only as evidenced adopters of the underlying act, not joint producers of a new consolidation. Remove unsupported `joint_institutional` provenance; do not invent consolidation authorship. Record publisher/official-host role if evidenced with the existing Publications Office institution.

Additional authorized corrections, without status upgrades: correct clearly omitted ordinal/subject wording in the other 2022 Council titles where the audit supplies the full exact heading; identify the FR cover/EN annex in ST 10069 in an English scope note (do not redesign language schema); distinguish Belgium/Commission statement authors in ST 10752 ADD 1; clarify that the SEC(2021)167 package includes the positive second opinion/annex and the earlier negative opinion. Do not change the contested ST 12206 INIT date, derive publication dates from covers, split compound packages, or resolve GPAI identities. If exact field text is not available, retain the field and report the limitation rather than guessing.

Allowed production edits: the seven target document files, clearly evidenced pending-record corrections just listed, their necessary source records and existing relationship rationales. No schema/src/web-production edits. Two web-test files (`web/tests/site.spec.ts` and `web/tests/review-credit.spec.ts`) may be adjusted only to remove the stale assumption that ST 15698 always remains pending and that the current pending count is always 26. Use current public data for selected fixtures; keep independent assertions of correct review labels and attribution. These test-only changes do not authorize a UI redesign or a new frontend feature. Add `research/migrations/2026-09-06-evidence-corrections.json` and a concise English report under `research/reviews/2026-09-06-evidence-corrections/`. Update the current-summary passages of `docs/historical-readiness.md` without rewriting historical pass results.

### Steps

- [ ] Read the exact evidence and write pipeline-output regressions first in `tests/test_evidence_corrections.py`. Exercise the real `run_pipeline` consumer: verified extensions and exact date-source linkage, named statement authors, consolidation semantics, pending preservation and stable route set. Failures before data edits must be recorded. Avoid source-text-only tests or tautological expected values.
- [ ] Patch the seven complete extensions and necessary sources using `apply_patch`; keep each source's factual retrieval history. Apply only the additional unambiguous corrections above. If an unexpected blocker prevents one admission, report it instead of changing rules.
- [ ] Add the chronological ledger with all 26 dispositions, before/after counts, route identities, changed-file reasons and prior verified preservation evidence. Preserve old ledgers byte-for-byte.
- [ ] Update old tests only where they mistake immutable historical review counts/holds for an eternal current state. Keep checks of original ledger arithmetic, source evidence, record preservation and all new reviewed status transitions. Do not blanket accept pending-or-verified; require a later explicit admission ledger for upgrades. Leave unrelated baseline failures unchanged and report them separately.
- [ ] Run focused RED/GREEN tests. Run the full pytest suite once after changes and compare failures against the captured pre-edit baseline. Use a fresh, narrowly named temporary directory.
- [ ] Run current pipeline to a temporary output directory, plus standalone historical readiness with cutoff `2026-09-04`. Expected maximum result is 167 ready and 19 retained pending, with all 186 routes intact. Nonzero all-record readiness is expected for retained holds; production pipeline must still pass.
- [ ] Self-review the snapshot delta; write report (including exact commands/results and any incomplete admissions), return without committing or publishing.

## Task 2: Independently review and verify the complete local delta

- [ ] Controller creates a unified diff against the task snapshot, not stale Git HEAD. Confirm only allowed canonical files changed and all prior verified document bytes and 186 routes are preserved.
- [ ] Dispatch a task-scoped review of Task 1 for evidence truth, metadata attribution, exact-version identity, source dates, test strength and scope compliance.
- [ ] Resolve actionable findings through the implementer; provide focused test results and a scoped fix diff for re-review.
- [ ] Run fresh final pipeline/readiness checks; report actual counts and remaining holds. Complete a whole-delta review with the unchanged data contract as the authority.
- [ ] Keep snapshot and review artifacts locally because no commit records this work. Report local completion, baseline test limitations if any, and that nothing has been deployed.
