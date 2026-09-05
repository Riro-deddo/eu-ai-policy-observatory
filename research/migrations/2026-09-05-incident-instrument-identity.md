# Incident Instrument Identity Review

Review by Codex at 2026-09-05T08:35:01Z; publication cutoff 2026-09-04.
Base commit: 01e6108328952a078c41a8608464093ddd0cf932.

## Applied scope

Two existing records are classified as principal documents, on positive evidence of distinct titles and substantive/operational purposes. Neither is a version of the other. Principal is an editorial record level, not a claim of final adoption; both remain draft, non-binding consultation materials.

| Existing record | Official PDF | Identity evidence |
| --- | --- | --- |
| draft-guidance-serious-ai-incidents-2025 | [119624](https://ec.europa.eu/newsroom/dae/redirection/document/119624) | Article 73 guidance with its own title, background, objectives, definitions and analysis. |
| draft-serious-ai-incident-report-template-2025 | [119623](https://ec.europa.eu/newsroom/dae/redirection/document/119623) | Separately titled reporting instrument with five sections and version 1.0.0. |

Titles are transcribed from page 1 with line breaks joined; short titles remain readable and unchanged. Canonical changes are restricted to official_title, record_level, updated_at and an attributed researcher-note append. Earlier review attribution is preserved; this is not a re-verification of every metadata field. The appended notes are chronological: statements in the earlier B3 review describe that earlier review's unchanged record level.

The two corresponding included inventory candidates receive matching titles/levels, and the template version label becomes 1.0.0. Their original admission decisions, reasons, discovery/review timestamps and attribution are unchanged. The JSON ledger retains complete before objects and the precise changes.

## Counts and remaining work

- Documents: 117 unchanged; relationships: 95 unchanged.
- Principal documents: 33 to 35; version records: 26 to 24.
- Relationship holds: five to three. No relationship edge was invented or removed.

The remaining holds are the three high-risk classification guideline sections (general principles, Annex I and Annex III). The general-principles PDF must not be mistaken for the whole guidelines. Their existing attachment records, sibling associations and routes are preserved.

A new public whole-work endpoint is a Phase C admission, not merely a Phase B relationship repair. A later Phase B retained-route contract should expose explicit reviewed, unresolved-parent notices; researcher notes alone do not implement that contract. This batch implements neither new admission nor the notice mechanism, and does not claim Phase B readiness. Covering-Communication identity, a combined PDF, exact Explorer-version equivalence, final-successor identity and formal annex_to justification remain unestablished.

## Evidence boundaries

The two local source PDF covers were visually reinspected and SHA-256 values recomputed against the B3 ledger. No new download or committed source archive is claimed. The consultation-page reopen returned HTTP 429; its previously observed descriptions and dates are not presented as a fresh successful fetch. Earlier B2 and B3 evidence ledgers remain immutable historical receipts.

## Verification and integration

Baseline: 316 passed, 1 skipped. Four new regressions failed before the correction for the expected old classifications/counts and absent ledger.

Targeted verification: 17 passed in 2.26 seconds. Full suite: 320 passed, 1 skipped in 13.90 seconds. The sole skip is the existing Windows chmod/ACL negative test; no tests were deselected. Independent read-only review ran the 17 focused tests in 2.30 seconds and found one important evidence-locator error, now corrected. Page 1 has section 1 BACKGROUND AND OBJECTIVES and section 2 DEFINITIONS. The added exact-locator assertion failed before correction. No critical issue was found; the reviewer considered this bounded batch ready for local commit after correction and receipt recording, not publication.

A semantic comparison against the base commit confirms only the declared two canonical and two candidate metadata corrections. All other inventory content, source records, relationships and historical ledgers remain unchanged. Both source-PDF hashes and the protected generated-pair hashes match their recorded values. The changed batch contains no CJK text; git diff --check passed.

Historical-contract preflight still reports 1,666 migration issues: 1,192 schema, 353 classification, 1 date, 117 collection and 3 relationship issues. These are not presented as resolved by this narrow batch; regression success does not mean the future historical contract is ready.

Post-correction full verification: 320 passed, 1 existing Windows ACL skip in 14.12 seconds. All six scoped plan steps are complete for the local batch; broader historical-contract migration remains open.

Local branch only. The protected generated JSON/SQLite pair is not regenerated. No GitHub push or deployment.
