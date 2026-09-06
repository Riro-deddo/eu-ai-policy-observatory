# Six-record Evidence Update and Publication Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development for the bounded data batch with independent review. Track steps with checkboxes.

**Goal:** Publish the evidence-backed updates for the three high-risk guideline sections and the three records with newly recovered publication evidence, without converting unresolved evidence into verified status.

**Architecture:** Keep canonical JSON, existing evidence gates and the static publishing pipeline. Admit one real whole-guidelines consultation work and its three existing sections; update only public research notes and qualifying official source references for the other three retained records. Ship a snapshot-scoped delta against current remote main, not the old dirty local HEAD.

**Tech Stack:** Python, JSON Schema, SQLite, pytest, Astro, GitHub Pages.

**Spec:** `../evidence-review-15-20260906/high-risk.json`, `../evidence-review-12-20260906/report.md`, `../evidence-review-12-20260906/training.json`, `../evidence-review-12-20260906/standards.json`; existing `docs/historical-readiness.md`, `schema/historical-document-extension.schema.json`, and `docs/data-dictionary.md` remain binding. Audit paths are relative to the repository root.

## Global Constraints

- User requested combined update and publication of the six existing records. A clarification offers the conservative combined scope or publication of only the guideline group; honour any reply before release.
- Work in the current directory, as previously approved, using an immutable byte snapshot. Preserve all pre-existing dirty changes. Do not use old Git HEAD as the content baseline, reset, clean, delete files or force-push.
- Publication cutoff remains `2026-09-04`. No schema, validator, source-trust exception, dependencies or frontend component changes.
- Exactly six existing document IDs are in scope. Only the three high-risk section records may newly pass the complete evidence gate. The other three remain legacy-review-pending; adding a partial historical extension is prohibited.
- The only new document is `draft-high-risk-classification-guidelines-consultation-work-2026`, a real whole consultation work, not a numbered Commission communication, new entity type or fourth independent PDF.
- On successful guideline admission the total becomes 187: 175 verified, 12 pending. All 186 original ID/slug routes and all 171 previously verified document bytes remain unchanged.
- Repository prose stays English. Preserve all existing corpus-assessment `reviewed_by` and `reviewed_at` values and the `Reviewed by — Yichen Hao` display. Record this automated correction in a new chronological audit ledger, not as a new personal-review attestation.
- Old source and migration files remain immutable. Add dedicated source entries with their actual retained receipt times; do not claim fresh retrieval. No BNetzA/Archive-It canonical source exception is approved by this publication request.
- The training notice/template have July work-level publication evidence, not a newly verified parent or exact editable-file version. C(2023)3215 has May 2023 publication evidence, not an established day. Do not silently replace dates, infer first-ever publication, substitute December C(2025)8311, or reclassify an unresolved attachment without its required dependency.
- No unrelated records or historical migration outcomes may change. Full tests, production pipeline, static build/public integrity, independent review and GitHub deployment checks gate release.

## Task 1: Apply the bounded canonical data and evidence update

**Files:**
- Modify `data/documents/draft-high-risk-classification-guidelines-2026.json`, `data/documents/draft-high-risk-classification-guidelines-annex-i-2026.json`, and `data/documents/draft-high-risk-classification-guidelines-annex-iii-2026.json`.
- Create `data/documents/draft-high-risk-classification-guidelines-consultation-work-2026.json`.
- Create the three `data/relationships/<existing-section-id>-part-of-consultation-work.json` files.
- Add dedicated official sources only if the existing library/PDF sources do not cover an independently required whole-work assertion. The existing `high-risk-guidelines-draft-commission` and `commission-newsroom-128559-pdf`, `commission-newsroom-128560-pdf`, `commission-newsroom-128561-pdf` sources are available; preserve them.
- If combined scope is retained, modify only `source_ids`, `corpus_assessment.researcher_notes` and `updated_at` in `data/documents/gpai-training-content-explanatory-notice-2025.json`, `data/documents/gpai-training-content-template-2025.json`, and `data/documents/ai-standardisation-request-c-2023-3215.json`. Existing uncompleted official-metadata fields stay explicitly legacy/unverified; explain the known caveats prominently in those notes. Do not add any extension-triggering field.
- For that combined scope, create `data/sources/gpai-training-summary-july-publication-oj-2026.json` and `data/sources/ai-standardisation-request-c-2023-3215-jrc-publication-month.json` using the source URLs, times and hashes in the twelve-record audit.
- Create `tests/test_six_record_evidence_update.py` and adjust only assertions explicitly describing the current corpus in prior admission/retained-route tests. Preserve tests of immutable historical outcomes; use the new ledger to distinguish chronological upgrades.
- Create `research/migrations/2026-09-06-six-record-evidence-update.json` and `research/reviews/2026-09-06-six-record-evidence-update/` for retained official receipt bytes, locators, caveats and preservation results.
- Update `docs/historical-readiness.md` and any README current-count statements only for the measured checkpoint. Do not revise old checkpoints.

**Interfaces:** Use `load_records`, `validate_historical_readiness`, `validate_historical_publication`, and `run_pipeline` unchanged. The controller supplies `../evidence-six-updates-20260906/before.zip` and `before-state.json`. The task report is `.superpowers/sdd/2026-09-06-six-record-evidence-update/task-1-report.md`. Do not commit or modify Git; the controller handles the authorized remote delta after review.

### Exact data requirements

The new whole work has title `Draft Commission Guidelines on the classification of high-risk AI systems`, short title `Draft high-risk classification guidelines — Complete consultation work`, record level `principal`, document type `guidelines`, version status `draft`, version label `Consultation draft — Complete work`, legal status `non_binding`, official reference/CELEX/ELI/OJ null, and both document and publication date `2026-05-19` with `document_date_kind: publication`. The official library explicitly publishes the combined work through separate section downloads; that is the date and parent-structure evidence. Do not copy the diagnostic-only cloned section record. The complete work's evidence and provenance are independently populated.

All four guideline records carry the complete historical extension: `historical_review_status: verified` only after an in-memory candidate readiness pass; `temporal_collection: contemporary_eu_ai_policy`; `relevance_class: direct_ai_substantive`; separate `date_evidence` entries; complete classification evidence for every tag; an empty bibliographic-author list after cover review; an empty additional-date list; and official evidence for the European Commission author role. No placeholder cover date/reference is inferred.

Preserve each existing section's exact title, reference-null state, dates, attachment level and non-binding draft status. Each gets an official `part_of` link to the new whole work, supported by `high-risk-guidelines-draft-commission` with an explicit rationale distinguishing a real consultation work from the prospective numbered communication. Remove or null the retained-route notice only after all four candidates and three edges pass existing validation. Existing sibling association edges stay unchanged.

Retain `general_cross_sector` and add only body-supported sector tags: Annex I adds `health`, `transport_and_mobility`, `industry_and_manufacturing` using PDF page 4 / printed page 3, paragraph 23. Annex III adds the ten sector tags and exact locators in the prior fifteen-record audit. The whole work may use the evidenced union of these tags with explicit PDF-section locators; do not infer sectors from the title alone. Keep general principles cross-sector.

For the combined scope, append dated English evidence updates while preserving prior notes:

- Training notice: OJ C/2026/4006 PDF page 2 independently corroborates Commission publication of the notice/template work on 24 July 2025. The recital does not print C(2025)5235 or prove the distinct main approval communication's publication. Register/preserved original identify the July ANNEX; the current linked PDF is December C(2025)8311. Existing final/record-level metadata remains under correction review, not newly verified. The approval-parent, source eligibility and exact formal identity corrections are unresolved.
- Training template: same July work-level publication evidence; the original template is an internal annex, and today's editable DOCX is not independently proved to be the historical July version. Preserve work/version/format distinction, unresolved parent/source requirements and pending status. Do not make the OJ's attributed `in force` wording an independent legal-status assertion.
- C(2023)3215: JRC134461 PDF page 8 / printed page 5 says published May 2023, with exact reference at PDF page 16 / printed page 13. The existing 22 May value is an adoption date and is not verified as publication; no day may be substituted. Article 4 of C(2025)3871 supplies the previously evidenced repeal finding, but exact operative timing and complete admission remain held. No month-precision item or legal-status-evidence field is inserted as a partial extension.

The two new official sources link respectively to `https://eur-lex.europa.eu/eli/C/2026/4006/oj/eng/pdf` and `https://publications.jrc.ec.europa.eu/repository/bitstream/JRC134461/JRC134461_01.pdf`. Use publication-versus-retrieval caveats in their verification notes and retain exact receipt times from the audit, not the current clock.

### Steps and acceptance checks

- [ ] Read the cited audit rows, exact official evidence, existing gate and compatible verified document examples. Inspect relevant PDF pages using the PDF skill where necessary.
- [ ] Write focused regressions before data edits. The real `run_pipeline` payload must contain the new principal work, three original section slugs, complete extensions, three official part-of edges and no retained-route notice. Assert draft/non-binding/no-invented-reference, sector evidence, and unchanged original review-credit values. Assert the other three records remain pending while their official source links and caveats are present for combined scope.
- [ ] Capture expected RED failures caused by absent data, not filesystem/environment failures. Run from the repository root with a fresh short `%TEMP%` base path to avoid Windows MAX_PATH.
- [ ] Apply exact JSON changes using `apply_patch`. Build candidate extensions and validate all four guideline IDs in memory before storing verified status. Stop on missing substantive evidence; do not weaken rules.
- [ ] Preserve cited official source bytes with deterministic gzip (`mtime=0`) where useful. Add a chronological ledger recording 186/171/15 before, 187/175/12 after, three upgraded existing IDs, one new verified whole work, and three evidence-only held updates. Preserve actual retrieval times and receipt hashes.
- [ ] Run focused new/affected tests, then the full Python suite with a short temporary directory. Record RED/GREEN commands, results and any diagnostics. Do not fix unrelated failures without reporting them.
- [ ] Compare against the controller's snapshot: exactly six existing document changes at most, one new document, all other 180 existing documents unchanged, all 171 previously verified documents unchanged, all old sources and migration ledgers unchanged, all 186 routes preserved.
- [ ] Update measured count documentation, self-review the complete diff and write the task report. No Git writes or release actions.

## Controller integration and finish

- [ ] Generate a snapshot-based diff package and conduct independent spec/evidence-quality review of Task 1; fix important findings through the original implementer.
- [ ] Run fresh database/public export, frontend unit/source checks, Astro build, public-build validation and proportionate browser smoke checks. Build outputs are generated artifacts, not new source records.
- [ ] Read current remote main and verify every pre-existing changed path still matches the starting snapshot or resolve any mismatch explicitly. Upload only reviewed delta paths to a new `codex/` branch; never push the dirty checkout wholesale.
- [ ] Create the English PR, await required checks, merge only the reviewed passing head, and verify the corresponding Pages deployment plus live representative records/counts.
- [ ] Report six-record update scope, actual verified/pending counts, PR/live links and any remaining limits. Keep all prior work and audit snapshots; no cleanup or deletion.
