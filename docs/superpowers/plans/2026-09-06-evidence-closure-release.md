# Evidence Closure and Citable Release Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Review four retained records, adjudicate twelve existing candidates, then freeze a traceable scholarly dataset release.

**Architecture:** Preserve canonical records and append dated evidence/decision records. Only positively established facts may change. Freeze a specific Git commit and its exported data with citation metadata and checksums.

**Tech Stack:** Canonical JSON, Python validation and SQLite export, Astro, GitHub Actions and Releases.

**Spec:** User-approved sequence in this conversation: retained-record evidence closure, candidate decisions, citable version. Existing admission rules and `CONTRIBUTING.md` remain binding.

## Global Constraints

- English repository and public interface; preserve historical actors, timestamps, routes and decisions.
- Do not invent publication dates, human sign-offs, negative coding or institutional evidence.
- Do not change schema or admission standards to force completion.
- Unresolved evidence may remain qualified and pending after a documented bounded review.
- No external correspondence, licence selection or DOI registration is implied by freezing a GitHub release.

## Task 1: Four retained records

- [x] Read the exact qualifications and existing source history for the standardisation request, the two July GPAI records and Council ST 12206/22 INIT.
- [x] Recheck official registers, linked original documents and specific missing evidence; record access failures distinctly from negative evidence.
- [x] Save an English dated decision ledger under `research/reviews/2026-09-06-release-closure/`, with one disposition and a concrete reopening condition for each record.
- [x] Upgrade only if every required field and relationship is evidenced; otherwise retain existing qualifications without altering prior reviews.
- [x] Run repository integrity and relevant evidence-preservation tests before moving to Task 2.

## Task 2: Twelve existing candidates

- [x] Inspect the three AI Board report links and nine PE amendment identifiers against official sources.
- [x] For each candidate, determine identity, English manifestation, document/publication dates, scope and duplication. A listing alone does not establish a distinct document or adoption date.
- [x] Append the previous decision to `decision_history` before any changed decision; record current reasoning and actual review time.
- [x] Add fully supported canonical records and dependencies only for admissible candidates; otherwise record a specific exclusion, merger or evidence hold.
- [x] Run inventory validation, publication-boundary checks and the full Python suite; regenerate exports.

## Task 3: Frozen citable release

- [x] Add `CITATION.cff` and release documentation describing author, title, version, repository, data cutoff, review date, counts and known limits, without an invented DOI or licence.
- [ ] Verify citation syntax, data consistency, historical preservation, English text, website build and browser tests.
- [ ] Obtain read-only code/data review, resolve defects, then merge the checked branch and confirm Pages deployment.
- [ ] Create an unused version tag and GitHub Release at the exact checked commit. Attach the generated JSON/SQLite and SHA-256 manifest with the declared build timestamp.
- [ ] Download or independently hash the uploaded artefacts; report the release link, decisions and remaining evidence gaps.
