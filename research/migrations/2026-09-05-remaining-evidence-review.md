# Remaining evidence review — 5 September 2026

## Result

All 37 documents retained as pending after the previous expanded review were rechecked. Seven Council documents now pass the complete evidence contract. Thirty remain explicit holds. Two precise repairs were applied to held records without promoting them to verified.

The local canonical corpus now has **131 documents: 101 verified and 30 pending**. All 131 IDs/slugs and the full contents of the 94 previously verified documents are preserved. This is a bounded review, not a claim of exhaustive EU AI document coverage. The publication cutoff remains **4 September 2026**.

The machine-readable audit is `2026-09-05-remaining-evidence-review.json`. Four source-review handoffs under `research/staging/2026-09-05-remaining-review/` account for every starting record. A handoff recommendation is not an integration decision: the audit records controller overrides explicitly.

## Seven completed upgrades

| Exact document version | Document date and meaning | Evidenced publication |
| --- | --- | --- |
| ST 14954/22 INIT — Council general approach | 25 November 2022, issue | 6 December 2022 |
| ST 14954/22 ADD 1 — German statement | 25 November 2022, issue | 6 December 2022 |
| ST 5662/24 INIT — provisional agreement | 26 January 2024, issue | 2 February 2024 |
| PE-CONS 24/24 INIT | 14 May 2024, issue | 21 May 2024 |
| PE-CONS 24/1/24 REV 1 | 13 June 2024, official act/signature | 12 July 2024 |
| PE-CONS 30/26 INIT | 18 June 2026, issue | 29 June 2026 |
| PE-CONS 30/1/26 REV 1 | 8 July 2026, official act/signature | 24 July 2026 |

The [6 December 2022 Council release](https://www.consilium.europa.eu/en/press/press-releases/2022/12/06/artificial-intelligence-act-council-calls-for-promoting-safe-ai-that-respects-fundamental-rights/) directly links both ST 14954 files. The [provisional-agreement release](https://www.consilium.europa.eu/en/press/press-releases/2023/12/09/artificial-intelligence-act-council-and-parliament-strike-a-deal-on-the-first-worldwide-rules-for-ai/) explicitly dates the addition of ST 5662 to 2 February 2024. Dated [2024](https://www.consilium.europa.eu/en/press/press-releases/2024/05/21/artificial-intelligence-ai-act-council-gives-final-green-light-to-the-first-worldwide-rules-on-ai/) and [2026](https://www.consilium.europa.eu/en/press/press-releases/2026/06/29/artificial-intelligence-council-gives-final-green-light-to-simplify-and-streamline-rules/) adoption releases directly link the exact PE-CONS INIT versions. EUR-Lex identifies the exact [PE/24/2024/REV/1](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689) and [PE/30/2026/REV/1](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32026R1744) versions alongside their OJ dates.

These are dates of the primary cited official publication manifestations under specification section 5.1, not claims of globally first availability. Issue dates, Council adoption events and OJ dates remain distinct. Germany is credited as the statement's author, with the Council separately identified as publisher.

## Two partial repairs

- ST 10069/22 INIT: replace the failed English-only URL with the Council register's exact multilingual FR/EN PDF at `/ST-10069-2022-INIT/x/pdf`. The source note now accurately describes this artifact. Publication-date evidence is still missing.
- ST 12206/22 INIT: correct the document issue date from 16 September to **7 September 2022**. The register assigns 16 September to REV 1. The retained publication date is explicitly unsubstantiated; this correction does not approve it.

## Thirty remaining holds

| Main blocker | Records |
| --- | ---: |
| Exact-version official publication date or manifestation not established | 25 |
| Three high-risk-guideline sections lack an evidenced attachment parent | 3 |
| Parliament adopted amendments conflict with the current date-type compatibility rule | 1 |
| Transparency-annex identity conflicts with a predecessor's current lineage rule | 1 |

For the June 2023 Parliament amendments, the official adoption and OJ dates are evidenced. The current validator excludes `institutional_position` from the primary `institutional_adoption` date kind. No document type or date was changed merely to obtain a pass; a narrow rule correction remains a separate user decision.

For the 20 July 2026 transparency guidelines, exact files 131214 and 131215 establish a content-approved **draft annex**, not a formally adopted final principal document. Trial integration of that accurate identity caused the previously verified May consultation draft to fail the current non-attachment-peer lineage rule. The candidate was withdrawn from canonical integration, and its full evidence retained. The old canonical identity and its existing relationship therefore remain unresolved, not re-endorsed by this review.

## Verification and release boundary

- Focused second-pass and previous-audit regressions: **15 passed**.
- Full Python suite: **390 passed, 1 skipped**. The skipped test relies on POSIX unreadability semantics that do not apply reliably to Windows ACLs; the Windows access-denial test remains active.
- Real canonical pipeline: success, producing a fresh SQLite database and public JSON in a disposable output directory.
- Historical preflight: 131 checked, 101 ready. Expected nonzero status remains for the 30 explicit holds: 458 field-level issues are not 458 missing documents.
- Astro check: 0 errors, 0 warnings, 3 existing hints. Static build: **144 pages**.
- Public-output safety scan and Git whitespace check: passed.
- Two independent bounded integration reviews found no critical or important outstanding findings. The minor ST 10069 source-note wording adjustment is recorded in the audit.

Public `Reviewed by — Yichen Hao` presentation is unchanged. New backend evidence records retain factual AI-assisted review attribution. The previous ledger and protected generated output pair were not overwritten. No schema, validator, existing relationship, deployment setting, Git remote or published site was changed. Browser interaction tests and remote deployment were not run for this local data-only review.
