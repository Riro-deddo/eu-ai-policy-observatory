# Official PDF Evidence Batch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for this bounded inline unit with independent review.

**Goal:** Attach real, individually identified source-file evidence to five existing records while retaining unresolved relationship decisions.
**Architecture:** Data-only changes under the active seven-entity contract; an English evidence ledger records observation limits and before/after values. Existing snapshot storage in SQLite is used; no export/UI extension or new public document is introduced.
**Tech Stack:** Canonical JSON, Python, pytest, SQLite; installed pypdf and Poppler for read-only PDF inspection.
**Spec:** docs/superpowers/specs/2026-09-05-historical-scope-and-coverage-design.md; historical-corpus-delivery-roadmap.md Phase B.
**Base:** bed7486b937a67960226c5ab8e88a8f65cee6d6b

## Global Constraints

- Preserve all 117 public document IDs, slugs, dates, record levels, publication states, legal statuses, sector/provenance tags and the 95 relationship records.
- Keep the English-only project, seven entities, six pages and publication cutoff 2026-09-04.
- Keep the prospective historical contract inactive and the protected generated JSON/SQLite pair unchanged.
- Preserve prior review attribution. Credit this field-limited evidence review to Codex, not Yichen Hao.
- No new public document, invented parent, final version, formal number, combined PDF or whole-corpus verification.
- A real retrieved file can have snapshot metadata with archived_path null. This means no deliberately committed binary archive, even though a local ignored review copy exists.
- Use existing isolated checkout and git --git-dir=work/sdd-gitmeta --work-tree=.; no push, merge, deployment, dependency installation or cleanup.
- New-agent creation hit the thread limit. Execute inline and request review from the existing read-only reviewer.

## Task 1: Record five real official representations

**Files:**

- Create tests/test_official_pdf_evidence.py.
- Modify data/documents/draft-guidance-serious-ai-incidents-2025.json and draft-serious-ai-incident-report-template-2025.json.
- Modify data/documents/draft-high-risk-classification-guidelines-2026.json, draft-high-risk-classification-guidelines-annex-i-2026.json and draft-high-risk-classification-guidelines-annex-iii-2026.json.
- Create data/sources/commission-newsroom-119624-pdf.json, commission-newsroom-119623-pdf.json, commission-newsroom-128559-pdf.json, commission-newsroom-128560-pdf.json and commission-newsroom-128561-pdf.json.
- Modify data/sources/high-risk-incident-consultation-commission.json and high-risk-guidelines-draft-commission.json to append a narrowly dated follow-up, preserving earlier retrieval history.
- Create research/migrations/2026-09-05-official-pdf-evidence.json and its .md report.
- Update only the obsolete exact updated_at assertion for General principles in tests/test_relationship_evidence_migration.py; retain historical B2 ledger and all identity, status, relationship and hold assertions.

**Interfaces:**

- Consumes the existing snapshots[] object fields id, source_id, retrieved_at, format, content_hash and archived_path.
- Produces five direct official_pdf source records, five document snapshots in canonical JSON and document_snapshots in temporary SQLite; the current public JSON intentionally omits snapshots and is not extended.
- Five local originals exist at work/source-review-2026-09-05-b3/document-{newsroom_id}.bin. PDF parser/magic establish format because HTTP Content-Type was the invalid value "/".
- retrieved_at uses observed UTC local file-write completion as an operational retrieval-time proxy, not a precisely recorded HTTP completion timestamp. Stored fractional seconds do not imply network timing accuracy; publisher dates and the cutoff remain unchanged.
- Only the incident template's version_label changes from Consultation draft to 1.0.0, transcribed from PDF page 1. version_status stays draft. The visible form date on page 7 and PDF creation dates are not publication dates.
- All five relationship holds remain. Record a whole-guidelines identity lead in the research ledger only; no endpoint is admitted.
- Preserve the inventory candidate's original Consultation draft discovery label and document its divergence from the corrected canonical version label; inventory reconciliation is outside this batch. Preserve the incident principal-level recommendation as an explicitly deferred editorial decision.
- Retain normalized HTTP receipts from the original downloader stdout. Do not claim those headers can be reconstructed from PDFs. Narrow the legacy source note's unproved universal no-final-successor statement to the actual draft/download evidence.

- [x] Write the offline integration test before data changes. It must run the real pipeline in pytest tmp_path, then assert the five hand-checked (document ID, newsroom source URL, SHA-256, page count evidence) mappings, exact SQLite snapshot provenance, template label 1.0.0 with draft status, all 117 frozen routes, 95 relationships and unchanged five preflight holds. Check ledger before/after fields against current records, and keep local byte verification separate from CI.
- [x] Run the new test with PYTHONPATH=src and a fresh system-Temp --basetemp; confirm failure because snapshots are absent, not an import error.
- [x] Add the five sources/snapshots, timestamped narrow notes, template version label and evidence ledger. Do not change production code. The ledger includes SHA-256, byte/page counts, observed response content type/status, exact scope of pages inspected, visual checks, no committed archive, held decisions and the bounded broken-link successor search.
- [x] Change the B2 general-principles timestamp assertion from equality to a parsed >= comparison against its historical review time; ensure all B2 historical ledger values remain unchanged.
- [x] Run targeted and complete tests without deselection using a fresh system Temp. Recompute all five local file hashes, and verify the protected generated pair is unchanged.
- [x] Request independent review of the exact diff; fix supported findings, rerun checks and record limitations. Stage an exact allowlist and make a local commit only if narrow Git metadata permissions permit.

## Verification commands

From the isolated repository in PowerShell:

```powershell
$env:PYTHONPATH = Join-Path (Get-Location).Path 'src'
& '.venv/Scripts/python.exe' -m pytest tests/test_official_pdf_evidence.py tests/test_relationship_evidence_migration.py -q -p no:cacheprovider --basetemp 'C:/Users/ROG/AppData/Local/Temp/eu-ai-b3-targeted-20260905' --tb=short
& '.venv/Scripts/python.exe' -m pytest tests -q -rs -p no:cacheprovider --basetemp 'C:/Users/ROG/AppData/Local/Temp/eu-ai-b3-full-20260905' --tb=short
```

Use a new suffix for reruns instead of deleting prior temporary directories. Runtime generation targets only pytest's temporary directory.

## Plan self-review

This is a Phase B evidence unit, not the complete Phase B delivery or Phase C backfill. Temporal fields, RP selection, new public admissions and UI work remain outside this plan. The active contract already supports all proposed fields and official_pdf sources; no new API, dependency or schema is needed.
