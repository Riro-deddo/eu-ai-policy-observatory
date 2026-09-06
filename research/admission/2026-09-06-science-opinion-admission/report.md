# Scientific Opinion No. 15 local admission

Admitted two canonical records on 6 September 2026 following the user's approval: the original first edition and its corrected first edition. The original candidate was added as a dependency; the corrected candidate changed from pending to included, retaining the prior decision verbatim in its history.

The original's printed issue date is 27 March 2024, read in the preserved ALLEA copy and corroborated by KNAW. Its 15 April publication date comes from the independent Commission announcement. The corrected edition retains the March issue date and has a separate EU Publications Office website release on 21 June 2024. The corrected date is not represented as proof of the earliest publication anywhere.

ALLEA and KNAW are labelled institutional archive supplements, with their own truthful host identities. They are not official EU sources. Both full texts have 102 PDF pages and identical page-by-page extracted text, but different bytes. The three local PDF hashes were recomputed and match the recorded snapshots. Public snapshot records have null archived paths.

Authorship and adoption belong to the Group of Chief Scientific Advisors; DG RTD support and Publications Office publishing are separate roles. The opinion is independent, non-binding advice, not a Commission strategy. The original record omits an official-host role because the Commission source hosts its announcement, while the original PDF is preserved by academy hosts.

The single corrected-to-original revises relationship is analytical. It uses the official correction label plus researcher comparison against the preserved original. The comparison detected non-whitespace differences on 22 page pairs, including wording changes; no publisher errata schedule or typography-only correction is claimed. SAPEA's supporting report remains a separate work.

Preservation checks passed against the actual canonical files: 184 existing documents remain byte-for-byte identical, with unchanged IDs and slugs. All 26 legacy review hold IDs and the separate retained-route notices are preserved. Totals are now 186 documents, 160 explicitly verified and 26 legacy holds. The inventory has 226 candidates. Only the corrected candidate and the bounded Publications Office source-sweep row changed among existing audit rows; one original dependency candidate and one bounded dependency entrance were appended. The 4 September 2026 coverage cutoff is unchanged.

The baseline is the canonical data directory. The stale 117-document generated export was not used for admission or preservation comparisons. The controller independently rechecked all 184 baseline document hashes and exact equality between the exported IDs and published canonical IDs. No commit, push or deployment was performed.

## Integration verification

- Full Python suite: 424 passed, 1 Windows-specific permission test skipped. The 20 supplement boundary tests also passed independently.
- Existing Node suite: 65 passed after the source-label change.
- Validated pipeline: 186 documents; SQLite integrity `ok`, no foreign-key violations; two equal-timestamp builds produced byte-identical SQLite and JSON.
- Static build: 199 pages. Public-build scan passed with the downloadable SQLite required.
- Targeted browser regression: 2 passed, at 1280x900 and 390x844, using installed Chrome through existing Playwright because the Browser plugin was unavailable. The original shows one official release source and two separately labelled academy-preserved supplements. The corrected version retains three official sources. Navigation works in both directions.
- Independent review found no remaining material issues in the admission, source gate or source labels. The publication-kind primary-date bypass found during review was fixed with a failing-then-passing regression test.
- The repository script guard passed; a separate 644-file scan included untracked canonical additions, with no non-Latin-script letters. New copy was reviewed in English.

Fresh output is retained in the workspace sibling `science-opinion-admission-local-20260906`: `public-data.json`, `eu-ai-policy-observatory.sqlite`, and `site/`. The repository's old `generated/` files remain stale: use the retained fresh JSON through `EU_AI_POLICY_PUBLIC_DATA_PATH`, or rerun the pipeline in a writable release environment. The static build used a temporary copy of the same source because the local environment rejected repository cache/output writes; no ACLs or security controls were changed. The unrelated full browser and Vitest suites were not rerun. These local checks are not a deployment claim.

The approved bounded-source rule is documented in `docs/data-dictionary.md` and summarised in `README.md`. Its implementation touches `schema/record.schema.json`, `schema/controlled-vocabularies.json`, `src/observatory/supplementary_sources.py`, `src/observatory/validate.py`, `src/observatory/historical_readiness.py` and `tests/test_supplementary_sources.py`. The only display change is in `web/src/pages/corpus/[slug].astro`, with a regression in `web/tests/science-opinion.spec.ts`.

## Exact paths touched by this admission subtask

- `data/sources/gcsa-ai-science-2024-release.json`
- `data/sources/gcsa-ai-science-2024-original-allea-archive.json`
- `data/sources/gcsa-ai-science-2024-original-knaw-archive.json`
- `data/sources/gcsa-ai-science-2024-corrected-catalogue.json`
- `data/sources/gcsa-ai-science-2024-corrected-pdf.json`
- `data/institutions/group-of-chief-scientific-advisors.json`
- `data/institutions/directorate-general-for-research-and-innovation.json`
- `data/documents/chief-scientific-advisors-ai-science-opinion-2024-first-edition.json`
- `data/documents/chief-scientific-advisors-ai-science-opinion-2024.json`
- `data/relationships/gcsa-ai-science-2024-corrected-revises-original.json`
- `research/corpus-inventory.json`
- `research/source-sweep.json`
- `research/admission/2026-09-06-science-opinion-admission/before-state.json`
- `research/admission/2026-09-06-science-opinion-admission/result-manifest.json`
- `research/admission/2026-09-06-science-opinion-admission/report.md`
