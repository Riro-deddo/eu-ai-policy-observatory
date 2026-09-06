# Incident Instrument Identity Review Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans for this bounded data-only unit and request independent review.

**Goal:** Represent the two separately issued serious-incident instruments as principal records with cover-faithful titles, without inventing version lineage.
**Architecture:** Correct existing canonical JSON and reconcile the same two included inventory candidates. Preserve earlier evidence ledgers as historical receipts; make their regression assertions aware of the subsequent review rather than rewriting their evidence.
**Tech Stack:** Existing Python, pytest, JSON and SQLite; no dependencies or production-code changes.
**Spec:** docs/superpowers/specs/2026-09-05-historical-scope-and-coverage-design.md, especially identity, provenance and stable-route requirements; data-dictionary.md document-level/status definitions.
**Base:** 01e6108328952a078c41a8608464093ddd0cf932.

## Boundaries and evidence

- Keep 117 documents, 95 relationships, all IDs/slugs/routes, dates, publication states, draft status, source/snapshot metadata, tags and RP-related memberships.
- Keep all-English output and cutoff 2026-09-04. Do not regenerate the protected generated JSON/SQLite pair or publish.
- The two inspected PDFs are distinct standalone instruments, not versions of each other. Guidance has a substantive guidance title and its own analysis; the reporting template has its own title, five operational sections and version label 1.0.0.
- Change both record_level values from version to principal on positive identity/purpose evidence, not on missing-parent logic. Other formally distinct drafts/versions are unaffected.
- The guidance official_title becomes DRAFT GUIDANCE ARTICLE 73 AI ACT- INCIDENT REPORTING (HIGH-RISK AI SYSTEMS). The template official_title becomes Incident Report for Serious Incidents under the AI Act (High-risk AI systems). Retain short titles and draft status.
- Review scope is title/record-level only, not every official field or classification. Credit the correction to AI-assisted reviewer in notes/ledger while preserving prior researcher and candidate decision-review attribution.
- Update the two linked inventory candidate titles/levels and the template version label to 1.0.0; preserve their original decision, decision reason, discovered_at, reviewed_at/by, source links and all other candidates. Record before/after metadata in the new audit ledger.
- Preserve the three high-risk sections as attachments and their unresolved parent holds. A new public whole-work admission belongs to Phase C. Phase B's later retained-route contract needs a separately designed, visible reviewed notice; no such feature is implemented here.
- Retain local worktree/branch and unrelated files. Only use git --git-dir=work/sdd-gitmeta --work-tree=.; no push, merge, cleanup, new worktree or fallback classifier.

## Task 1: Apply the two evidenced identity corrections

**Files:**

- Modify data/documents/draft-guidance-serious-ai-incidents-2025.json and draft-serious-ai-incident-report-template-2025.json: only official_title, record_level, updated_at and corpus_assessment.researcher_notes.
- Modify research/corpus-inventory.json: only the two matching candidates' official_title/record_level, plus the template version_label.
- Create research/migrations/2026-09-05-incident-instrument-identity.json and .md.
- Create tests/test_incident_instrument_identity.py.
- Modify tests/test_official_pdf_evidence.py and tests/test_relationship_evidence_migration.py only to distinguish immutable historical batch evidence from current post-review classifications.

**Interfaces and concrete checks:**

- Current principal count rises from 33 to 35; version count falls from 26 to 24. Total documents/relationships remain 117/95.
- Expected current relationship holds are exactly draft-high-risk-classification-guidelines-2026, draft-high-risk-classification-guidelines-annex-i-2026 and draft-high-risk-classification-guidelines-annex-iii-2026.
- Existing template snapshots, version_label 1.0.0, version_status draft and publication/date values survive SQLite/public JSON generation.
- The new ledger holds full before objects for the two documents, exact dotted after_changes, candidate before/after objects, source IDs/hash/page locators and the distinction between applied editorial judgments and preserved evidence.

- [x] Add failing tests that run the real pipeline and assert the two exact titles/levels, frozen routes, 35 principal documents, unchanged draft dates and snapshots, three remaining holds, and matching included-candidate metadata.
- [x] Run tests in a fresh system-Temp directory and confirm failure because the two levels/titles and candidate metadata still reflect the old classification.
- [x] Apply the data corrections and new ledger/report. Do not edit B2/B3 historical ledger files.
- [x] Adapt B3 ledger comparisons by reversing this new ledger's declared title/level/note/timestamp changes in memory, preserving checks on real unchanged source/snapshot data. Test the historical five-hold state in memory by restoring the two prior version levels; current-state tests must assert the exact three remaining holds. Update B2 current-state hold assertion without changing its historical five-hold target list.
- [x] Run complete tests without deselection. Compare all canonical objects and the inventory against base, permitting only declared changes. Verify protected generated hashes, source hashes and English content.
- [x] Obtain independent review, address supported findings and save an exact-allowlist local commit after final tests pass.

## Verification

```powershell
$env:PYTHONPATH = Join-Path (Get-Location).Path 'src'
& '.venv/Scripts/python.exe' -m pytest tests/test_incident_instrument_identity.py -q -p no:cacheprovider --basetemp 'C:/Users/ROG/AppData/Local/Temp/eu-ai-b4-red-20260905' --tb=short
& '.venv/Scripts/python.exe' -m pytest tests -q -rs -p no:cacheprovider --basetemp 'C:/Users/ROG/AppData/Local/Temp/eu-ai-b4-full-20260905' --tb=short
```

Use fresh suffixes for reruns; do not delete earlier temporary directories. This single reviewed identity batch does not implement retained-route notices, finish Phase B or admit new documents.
