# Remaining Evidence Review Plan

> **For agentic workers:** Use the existing evidence-readiness contract, parallel source research, and independent integration review. This is a bounded data-review task, not a new product feature.

**Goal:** Recheck all 37 retained evidence holds against official sources and integrate only substantiated corrections.

**Architecture:** Preserve canonical identities and prior audit history. Four disjoint research partitions stage evidence; the controller checks their findings before any canonical update. Unresolved evidence stays pending with a specific reason.

**Tech Stack:** Canonical JSON, Python evidence validators, SQLite export, official institutional registers and PDF/HTML publications.

**Spec:** `docs/superpowers/specs/2026-09-05-historical-scope-and-coverage-design.md` and `docs/historical-readiness.md`.

**Base:** `5bbd3d7258f53ba04fc3c942d12a9857ded1b3de`.

## Constraints

- Keep 131 published IDs/slugs, the seven-entity model, English-only output, and the 4 September 2026 publication cutoff.
- Do not overwrite old evidence ledgers or infer a publication date from an issue date, retrieval time, or later website update.
- Keep the public `Reviewed by` display as Yichen Hao; retain factual AI-assisted attribution in new backend review evidence.
- Do not alter schema or publication standards merely to make a held record pass. Document any genuine contract incompatibility separately.
- Leave protected generated files and unrelated working files untouched; generate verification output in a disposable directory.
- No push, merge or deployment is part of this evidence-review request without further release direction.

## Tasks

- [x] Freeze the 37-document pending set from the deployed baseline and match it to the previous explicit holds.
- [x] Recheck 11 Commission records, 11 Council 2022 records, 11 Council 2024/2026 records, and four EUR-Lex/Parliament records against fresh official evidence.
- [x] Save English, record-specific findings under `research/staging/2026-09-05-remaining-review/`, including checked URLs, observed locators, timestamps, proposed corrections, and remaining limitations.
- [x] Independently review every proposed upgrade for exact identity, date semantics, issuing roles, classification evidence, and required version/attachment relationships.
- [x] If evidence-ready changes exist, add a focused regression before applying them; preserve prior review facts in a new audit ledger and update only the corresponding canonical records/sources.
- [x] Run the historical preflight and relevant full Python regression tests; report structural results separately from substantive source-review results.
- [x] Prepare the handoff with exact reviewed/upgraded/held counts and explicit modeling holds; do not claim EU-wide completeness.

## Result

Seven upgrades, 30 explicit holds, and two precise pending-record/source repairs. The full suite passed 390 tests with one Windows-inapplicable POSIX permission test skipped; Astro built 144 pages. A Commission draft-annex candidate was withdrawn after the real pipeline exposed a predecessor-lineage dependency. No admission rule was weakened, no previously verified record was changed, and no release operation was performed. See `research/migrations/2026-09-05-remaining-evidence-review.md` and its JSON ledger.

## Validation

Run the read-only preflight with `PYTHONPATH=src` and:

```text
.venv/Scripts/python.exe -m observatory.historical_readiness --project-root . --publication-cutoff 2026-09-04
```

Verify that each starting ID has exactly one final review decision, no prior verified document or route disappears, all source references resolve, and only evidence-backed upgrades reduce the pending count. The standalone preflight may remain nonzero for explicitly retained holds; this is not a reason to relax evidence standards.

## Self-review

This plan covers the remaining queue only. New document admission, general source-universe expansion, UI redesign, attribution changes, and release operations are excluded. Source research can proceed independently; canonical integration remains single-writer.
