# Remaining evidence review: continuation

## Outcome

All 30 records retained after the second pass received a further bounded official-source review. Four now pass the expanded evidence contract; 26 remain explicit evidence holds. The local corpus is **131 documents: 105 verified and 26 pending**. This does not claim completion of metadata verification or exhaustive EU AI document coverage. The cutoff remains **4 September 2026**.

The machine-readable audit is `2026-09-05-review-continuation.json`. Four handoffs under `research/staging/2026-09-05-review-continuation/` account for every starting record. The earlier 77/37 and 7/30 review decisions remain unchanged historical records.

## Four evidence-backed admissions

| Record | Document date | Primary cited official publication | Review result |
| --- | --- | --- | --- |
| Parliament amendments P9_TA(2023)0236 | 14 June 2023, institutional adoption | 23 January 2024, OJ | Adopted institutional position; not the final AI Act |
| Transparency guidelines, C(2026)5054 annex | 20 July 2026, issue | 20 July 2026, Commission library | Content-approved draft annex; non-binding; formal adoption deferred |
| AI-system-definition guidelines, C(2025)5053 | 29 July 2025, issue | 6 May 2026, Service Desk resource | Final Commission guidance, non-binding |
| Prohibited-practices guidelines, C(2025)5052 | 29 July 2025, issue | 6 May 2026, Service Desk resource | Final Commission guidance, non-binding |

The [Parliament text](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52023AP0236) independently identifies adoption and OJ publication. The [Commission library](https://digital-strategy.ec.europa.eu/en/library/guidelines-transparency-obligations-providers-and-deployers-ai-systems) and exact files [131214](https://ec.europa.eu/newsroom/dae/redirection/document/131214) and [131215](https://ec.europa.eu/newsroom/dae/redirection/document/131215) identify the approval communication and draft annex. The stable final-prefixed URL is retained for compatibility; it is not proof of formal adoption.

The [Service Desk Resources index](https://ai-act-service-desk.ec.europa.eu/en/resources?page=1) separately dates the two direct-download guideline cards. Their card-specific HTML datetime values are `2026-05-06T16:20:21+02:00` and `2026-05-06T16:22:32+02:00`. The exact PDF covers and complete normalized texts match the current Commission newsroom versions despite differing PDF wrapper bytes. These are later cited official manifestations, not first-ever-publication claims. The original February library dates cannot date the later July texts. Exact hashes and observed retrieval times are recorded in the source handoff.

## Authorized compatibility corrections

The user explicitly authorized both corrections:

- `institutional_position` may use `institutional_adoption` only with `legal_status: adopted`, plus the existing independent official date evidence. A proposed position is still rejected.
- A version may link to an attachment manifestation only when the attachment has its own valid outgoing officially evidenced `annex_to`/`part_of` parent. Missing, unpublished, unofficial and wrong-direction parents remain invalid, including selected-document-only validation.

Neither correction permits unknown dates, invented parent records or source-free classification. All 101 previously verified document files remain unchanged, including the earlier transparency consultation draft.

## Remaining evidence holds

There are **23 exact-publication-evidence holds** and **3 missing-attachment-parent holds**. The files exist; the unresolved facts are narrower than document existence. Current public availability, cover issue dates, adoption dates, repository ingestion dates and generic webpage updates do not independently establish the publication day of an exact manifestation. Three draft high-risk section PDFs name an unidentified parent communication using placeholders; no parent was invented.

| Stable record ID | Remaining evidence needed |
| --- | --- |
| `ai-act-consolidated-2026-07-27` | The exact official publication day remains unestablished. Repository ingestion/creation and consolidation applicability dates have different meanings and cannot be substituted. |
| `ai-act-council-adoption-note-st-9645-2024-rev-1` | No newly located official source supplies a dated publication manifestation or historical public-release timestamp for exact ST 9645/1/24 REV 1. Current Public status, the 15 May issue date, the 17 May A-item package and the 21 May adoption event cannot substitute for publication_date. |
| `ai-act-council-adoption-statements-st-9645-add-1-rev-2` | No newly located official source supplies a dated publication manifestation or historical public-release timestamp for exact ST 9645/24 ADD 1 REV 2. The exact A-item citation and later adoption record corroborate identity and context only. |
| `ai-act-council-coreper-general-approach-st-14336-2022` | A dated official publication or access-status event that directly makes the exact ST 14336/22 manifestation available to the public, plus role wording that distinguishes the GSC sender from Czech Presidency drafting responsibility. |
| `ai-act-council-final-compromise-st-13955-2022` | A dated official source establishing public release of exact ST 13955/22; the eventual role patch must identify Presidency origin rather than an undifferentiated Council author. |
| `ai-act-council-first-consolidated-compromise-st-10069-2022` | A dated official page, list or access decision directly publishing the exact multilingual ST 10069/22 INIT manifestation. |
| `ai-act-council-fourth-compromise-st-13102-2022` | A dated official publication manifestation for exact ST 13102/22 and role evidence recorded as Presidency origin. |
| `ai-act-council-general-approach-st-15698-2022` | A dated official manifestation that directly publishes exact ST 15698/22, or an official metadata field identifying when that exact EUR-Lex/Consilium manifestation became public. Adoption on 6 December and current hosting remain insufficient. |
| `ai-act-council-second-compromise-st-11124-2022` | A dated Council or Presidency publication directly linking exact ST 11124/22, with Presidency origin preserved in the role model. |
| `ai-act-council-third-compromise-part-one-st-12206-2022-init` | A dated official source directly publishing ST 12206/22 INIT; Presidency must remain the exact originator when the historical extension is completed. |
| `ai-act-council-third-compromise-part-one-st-12206-2022-rev-1` | A dated official source that directly publishes the exact ST 12206/1/22 REV 1 manifestation, with Presidency origin retained. |
| `ai-act-council-third-compromise-part-two-st-12549-2022` | A dated official publication manifestation for exact ST 12549/22, with Presidency origin expressed precisely. |
| `ai-act-regulatory-scrutiny-board-opinion-sec-2021-167` | No exact dated official publication manifestation of the SEC package was recovered. The retained 23 April 2021 date is only evidenced as the Council cover-note date in the previous pass. |
| `ai-omnibus-council-adoption-note-st-10752-2026` | No newly located official source supplies a dated publication manifestation or historical public-release timestamp for exact ST 10752/26 INIT. The 29 June adoption package and press release are adoption evidence for the legislative act, not publication evidence for this Council note. |
| `ai-omnibus-council-adoption-statement-st-10752-add-2` | No newly located official source supplies a dated publication manifestation or historical public-release timestamp for exact ST 10752/26 ADD 2. The vote record and 29 June press release establish adoption context only. |
| `ai-omnibus-council-adoption-statements-st-10752-add-1` | No newly located official source supplies a dated publication manifestation or historical public-release timestamp for exact ST 10752/26 ADD 1. The official mirror's Date of document and the A-item-list date are not publication dates. |
| `ai-omnibus-council-information-note-st-10599-2026` | No newly located official source supplies a dated publication manifestation or historical public-release timestamp for exact ST 10599/26 INIT. The 17 June cover date, 16 June Parliament adoption and 29 June Council adoption are distinct events and cannot establish publication_date for this information note. |
| `ai-standardisation-request-c-2023-3215` | No official source reviewed in this third pass supplied a separately evidenced publication date for exact C(2023)3215 / M/593. |
| `draft-high-risk-classification-guidelines-2026` | The retained attachment record still lacks an evidenced parent document identity. Neither the Register search nor the official library, consultation, press release, or Service Desk surfaced a separately issued parent by the cutoff. |
| `draft-high-risk-classification-guidelines-annex-i-2026` | The exact attachment still lacks an evidenced parent document identity. |
| `draft-high-risk-classification-guidelines-annex-iii-2026` | The exact attachment still lacks an evidenced parent document identity. |
| `ecb-technical-working-document-con-2026-10` | The exact attachment publication day remains unestablished. The March document date, April repository creation timestamp and parent opinion's OJ publication are not interchangeable. |
| `gpai-provider-guidelines-2025` | No dated official publication manifestation of the exact current C(2025)7719 text was recovered; the Register itself marks that record not published. |
| `gpai-training-content-explanatory-notice-2025` | No dated official publication manifestation for exact C(2025)8311 was recovered. |
| `gpai-training-content-template-2025` | The current DOCX's exact-version publication date remains unresolved after following the Service Desk card through the press release and current library download. |
| `standardisation-request-c-2025-3871` | No official source reviewed in this third pass supplied a separately evidenced publication date for exact C(2025)3871 / M/613. |

Additional Council register metadata, dated meeting packages, exact-number access-request searches, EUR-Lex mirrors, Cellar object notices, Commission Register entries and alternative Service Desk manifestations were checked. Per-record URLs, methods, positive identity findings and access limitations remain in the handoffs. A zero-result access-request search is not proof that no release ever occurred. No access challenge or HTTP rate limit was bypassed.

Closing these holds now requires new official evidence, such as source-publisher confirmation of exact release dates and parent identities. No inquiry was sent and no wider schema change was made.

## Verification and preservation

- Focused chronology/admission regressions: **21 passed**.
- Full Python suite: **404 passed, 1 skipped** for Windows-incompatible POSIX permission semantics.
- Node tests: **65 passed**, including atlas endpoint integrity and non-overlapping geometry.
- Vitest: **26 passed** using the supported runner configuration loader; the default bundler encountered an ancestor-directory permission error. No permanent configuration change was made.
- Fresh canonical pipeline: 131 documents, 96 relationships, 160 sources. Output was written only to a disposable validation directory.
- Historical preflight: 131 checked, 105 ready; expected exit 1 for 26 pending records. The 398 field-level issues are not 398 missing documents.
- Astro: 0 errors, 0 warnings, 3 existing hints; **144 static pages built**. Public-output scan and English/whitespace checks passed.
- Independent admission and final-ledger reviews found no critical or important issues. All 13 canonical changes match their ledger hashes. All 131 ID/slug routes, the prior 101 verified document files, the 26 remaining held files, the protected generated pair and the two previous review ledgers are preserved.

Public **Reviewed by — Yichen Hao** remains unchanged. Backend evidence attribution remains factual AI-assisted review attribution. Browser interaction tests were not run; their count assertions were updated but no E2E success is claimed. No commit, push, PR, merge or deployment was requested or performed. This report describes local work, not a changed live site.
