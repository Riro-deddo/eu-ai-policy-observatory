# Four Evidence Admissions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement the single bounded batch with independent review. Steps use checkbox syntax for tracking.

**Goal:** Correct and complete evidence extensions for the four records approved after the 19-record audit, reducing the local pending count from 19 to 15 without changing route identities.

**Architecture:** Canonical JSON remains authoritative. Add exact official source citations and version-aware relationships, use the existing admission gate, and regenerate local database/public exports. Preserve the prior audit ledgers and all unrelated records; no schema or website redesign.

**Tech Stack:** Python, JSON Schema, SQLite, pytest, Astro static export.

**Spec:** `../evidence-review-19-20260906/report.md` and its authoritative `all-records.json` (paths relative to the repository root); `docs/historical-readiness.md` and `schema/historical-document-extension.schema.json` define the unchanged gate.

## Global Constraints

- User approved the four-record correction step, not deployment or the other fifteen holds.
- Work in the current directory using a byte snapshot, honoring the user's earlier explicit preference. Preserve the old dirty checkout and do not create commits, branches, PRs, pushes or deployments.
- Exactly 186 published document IDs/slugs remain; after successful admission exactly 171 are verified and 15 remain pending.
- Publication cutoff stays `2026-09-04`. No validators, source trust rules, schema, dependencies, web components or UI copy are to be changed.
- Repository prose and metadata remain English. Preserve `Reviewed by — Yichen Hao` display and pre-existing `reviewed_by`/`reviewed_at` fields; record this automated evidence correction separately in the new chronological ledger.
- Prior verified documents, the other fifteen pending documents, prior migration ledgers and existing source files remain byte-identical. Add new sources without rewriting retrieval history.
- Exact official manifestation publication is acceptable; do not claim first-ever publication or transfer a date to a different version/translation.
- Preserve source receipts and caveats inside the repository so verification does not depend on workstation-only paths.

## Task 1: Complete the four evidence-backed records as one batch

**Files:**
- Modify four `data/documents/` JSON files named below.
- Create dedicated sources under `data/sources/` using document-specific IDs; source entries consume exact URLs, hashes and times in the audit's `all-records.json`.
- Modify `data/relationships/ecb-technical-working-document-annex-to-opinion.json`; add the outgoing GPAI `annex_to` relationship; update evidence on these four documents' existing edges only where required.
- Modify only matching candidate entries in `research/corpus-inventory.json` when required for canonical alignment.
- Create `tests/test_four_evidence_admissions.py`; adjust current-status assertions in `tests/test_evidence_corrections.py`, `tests/test_expanded_evidence_review.py`, `tests/test_remaining_evidence_review.py`, and `tests/test_review_continuation.py` to recognize the new chronological ledger without altering earlier historical results.
- Create `research/migrations/2026-09-06-four-evidence-admissions.json` and `research/reviews/2026-09-06-four-evidence-admissions/` receipt archives/preservation proof.
- Update `docs/historical-readiness.md` and any README current-count sentence only to report the new checkpoint accurately.

**Interfaces:** Read existing `load_records`, `validate_historical_readiness`, `validate_historical_publication` and `run_pipeline`. Do not change them. The controller supplies `../evidence-four-corrections-20260906/before-state.json` and `before.zip` (a byte snapshot avoiding Windows long-path copies). Output the canonical changes and a full report to `.superpowers/sdd/2026-09-06-four-evidence-admissions/task-1-report.md`.

### Evidence-specific changes

1. `ai-act-regulatory-scrutiny-board-opinion-sec-2021-167`: retain compound package and issue `2021-03-22`; use OP exact Council-hosted ST 8115 ADD 5 publication `2021-04-23`, UUID `ee0d5478-a428-11eb-9585-01aa75ed71a1`. Explain competing SEC catalogue DATE_DOCUMENT `2021-04-21`; it does not override the actual cover/signature. Commission/RSB authorship is distinct from Council transmission. Complete all date, classification, roles, source and relationship citations.
2. `ecb-technical-working-document-con-2026-10`: retain issue `2026-03-13` and qualified catalogue publication `2026-03-13`, UUID `c249d527-34cb-11f1-be39-01aa75ed71a1`. Keep non-binding final companion identity and financial-services tag. Distinguish the catalogue assertion from first EUR-Lex availability and the opinion's 15 April OJ publication. Change the existing attachment edge basis to analytical with a precise rationale and official companion evidence; keep endpoints.
3. `ai-omnibus-council-adoption-statements-st-10752-add-1`: issue/publication `2026-06-22`, OP UUID `e69a1045-6fa1-11f1-ae88-01aa75ed71a1`. Full official title from the actual cover. Attribute Belgium and Commission statements separately; Council is publisher/General Secretariat sender, not sole substantive author. Preserve mixed EN/FR OP manifestation versus current English translation caveat; no claim the English translation first appeared on that date. Complete classification/role evidence consistent with partial EU institutional authorship.
4. `gpai-provider-guidelines-2025`: retain July ID/slug and issue `2025-07-18`; correct to `attachment`, `draft`, a content-approved draft-annex label and exact C(2025)5045 ANNEX title/reference. Publication `2025-08-27` cites the dated Service Desk resource card directly linking the original July PDF, not the current November C(2025)7719 file. Add official `annex_to` pointing to existing verified `gpai-provider-guidelines-approval-communication-2025`. Preserve old source history and non-binding status. Complete all extension fields.

### Steps and acceptance checks

- [x] Read the four ready rows and cited originals/receipts from the completed audit, the gate, and comparable already-verified canonical records. Read project instructions if present.
- [x] Write failing regression tests against the real pipeline's public payload before changing canonical data. Parameterize literal expected publication dates for all four and assert resolved official source URLs, complete admitted extension and preserved ID/slug. Add separate cases showing original GPAI draft/parent identity, ECB analytical companion relationship, and Belgium/Commission versus Council attribution.
- [x] Run the focused tests and capture expected pre-admission failures (not environment errors). Use a fresh short temporary directory to avoid Windows MAX_PATH failures:

```powershell
& '.\.venv\Scripts\python.exe' -m pytest tests/test_four_evidence_admissions.py -q --basetemp "$env:TEMP/euai4-red"
```

- [x] Apply the four minimal JSON correction packages with `apply_patch`, using precise locators and retained caveats rather than generic verification assertions. Supply complete candidate extensions, then call the existing readiness validator for these four IDs before persisting their verified status. Do not weaken any gate if a candidate fails.
- [x] Archive cited source bytes with deterministic gzip compression where useful; preserve their original retrieval timestamps and hashes. Add the new migration ledger with exact before/after counts, four upgraded IDs, fifteen held IDs, preservation proof and prior-ledger hashes. Never rewrite historical migration outcomes.
- [x] Adjust old test expectations only through the expressly recorded later admissions; retain assertions for historical counts/dispositions and reject silent unledgered upgrades. Run the focused new and affected historical-ledger tests, then run the full Python suite once. Record commands/results.
- [x] Measure byte-preservation of the other 182 documents, all 186 routes, all previous sources/migration ledgers and reviewed-by attribution envelopes. Check any corpus-inventory changes are limited to four candidate IDs and are factually required.
- [x] Update current-count documentation, write report with RED/GREEN evidence, changed paths and any concerns. Do not commit or deploy. The controller independently reviews and runs the final pipeline/build checks.

## Controller integration and finish

- [x] Read-only snapshot/diff review against the exact start state, not the old Git HEAD.
- [x] Independent task review: both spec compliance and evidence/data quality; resolve important findings before accepting admissions.
- [x] Run fresh pipeline to `generated/` and confirm SQLite/public JSON counts, record fields and source/relationship resolutions. Run the existing static website build/check if the available runtime permits, without modifying frontend source or dependencies; report an environment limitation instead of making an unsupported success claim.
- [x] Independent final scoped review of the complete local change, including immutable old ledgers and pending records.
- [x] Deliver measured outcome, actual test/build results and explicit not-pushed/not-deployed state. Keep evidence/snapshots for recovery; no cleanup of earlier work.
