# Qualified Evidence Review Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement this approved plan inline. Steps use checkbox syntax for tracking.

**Goal:** Represent the four retained records' actual evidence gaps without false dates or full-verification upgrades.

**Architecture:** Allow a null publication date only with an explicit pending-review qualification. Add a small optional `review_qualification` object carried from canonical JSON through SQLite and public JSON to existing record/list views. Keep the historical readiness contract unchanged: full verification still requires exact dates and evidence.

**Tech Stack:** Python, JSON Schema, SQLite, Astro, TypeScript, pytest, Vitest, Playwright.

**Spec:** User-approved chat design: unknown publication date stays null; retain confirmed adoption; preserve old value and reason in audit history; explain two GPAI parent gaps and one Council version conflict; do not upgrade counts; English only.

## Global Constraints

- Preserve current-directory changes and all prior evidence, ledgers, routes and review credits.
- No inferred publication date, new historical admission, dependency upgrade or relaxed full-verification rule.
- Null dates are excluded from publication-year filters and sorted after known publication dates, never silently replaced by adoption dates.
- Deploy only after tests and remote-base comparison; never push the dirty checkout wholesale.

### Task 1: Data and export contract

- [ ] Snapshot existing project files outside the repository.
- [ ] Add `tests/test_review_qualification.py`: build a real fixture with `publication_date=None` and qualification; assert SQL null, JSON null and retained gap. Reject verified-plus-null, null-without-qualification, and a publication-date-gap with a non-null value.
- [ ] Run `python -m pytest tests/test_review_qualification.py -q`; record expected schema/SQL failure before production changes.
- [ ] Modify `schema/record.schema.json`, `schema/database.sql`, `src/observatory/build_db.py`, `src/observatory/export_public.py`: optional qualification `{kind, confirmed, unresolved}` with three exact kinds `parent_evidence_pending`, `publication_date_pending`, `official_version_conflict`; nullable publication date restricted to pending qualified records.
- [ ] Set only C3871 publication date to null; add four qualifications; retain existing notes, reviewer and historical status. Preserve old date/reason in an English migration ledger.
- [ ] Run focused tests and full pytest. Ensure 187 records / 183 fully verified / 4 pending.

### Task 2: Existing frontend consumers

- [ ] Add Vitest null-date sorting/filtering tests using a real document fixture with null publication date, and Playwright assertions for qualified badges and unknown date output.
- [ ] Run failing tests before edits.
- [ ] Add optional qualification type and nullable date type. Use `document.publication_date?.startsWith(year) ?? false` for filters and empty sort key for null; do not substitute document date.
- [ ] Update Corpus, record and policy pages to display the missing date and qualification, replacing the generic banner when qualified. Full-verification counters/filter keys remain unchanged.
- [ ] Explain null dates and retained evidence gaps in the existing methodology page.
- [ ] Run frontend tests, Astro check/build and browser interaction checks for Corpus filtering and relevant detail pages, desktop/mobile.

### Task 3: Preservation and publication

- [ ] Compare snapshot to working files; reject any unrelated document changes or dropped files.
- [ ] Generate fresh database/public JSON; run integrity/foreign-key and public-build checks.
- [ ] Compare scoped changed paths against current GitHub main before constructing a narrow release branch/PR; include previously local ST10069 admission only after an explicit release-scope check.
- [ ] Review patch, pass CI, merge and verify Pages deployment. If environment or remote divergence blocks safe release, retain local work and report the exact unfinished step.
