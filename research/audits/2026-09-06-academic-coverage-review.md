# Academic coverage review and bounded backfill

Baseline: main `5ed89e1ba71f476f9ca14814e97d8f5f8043cc16` (v0.1.0); publication cutoff remains **4 September 2026**. This revision is a documented improvement, not certification of exhaustive coverage or independent human peer review.

## Findings and actions

1. **Corrected legal status.** Horizon 2020 Decision 2013/743/EU was incorrectly recorded as unqualified `in_force`. Council Decision (EU) 2021/764 Article 15 expressly repeals it from 1 January 2021; Article 16 preserves existing actions until closure. The corrected record explains why these provisions take precedence over a conflicting original EUR-Lex status indicator. No other old programme was marked expired from its end year.
2. **Completed six OJ citations.** The exact assigned citations were already present in the evidence but absent from the dedicated metadata fields. Six targeted corrections preserve original IDs, dates, classifications and routes. The before/after ledger and historical fingerprint tests keep the correction auditable.
3. **Recovered a missing queue entry.** C(2025) 7719 final is distinct from the included July C(2025) 5045 annex. A new pending inventory entry restores its tracking without importing the July publication date or admitting it on historical staging evidence alone.
4. **Disclosed selection bias.** All 117 records created on 3-4 September had concept and policy assignments; 69 of 70 created on 5-6 September lacked both. These baseline counts demonstrate concentration by ingestion cohort, not the cause of missingness. The methodology now warns against treating a filtered annotated subset as representative of the full corpus. Empty annotations were not mechanically populated.
5. **Completed role documentation.** The dictionary now explains all eleven permitted institutional roles, role-specific source locators, personal authors and the difference between authorship, hosting and transmission.

## Five admitted documents

| Record | Date treatment | Attribution/status safeguard |
| --- | --- | --- |
| Joint AIB/MDCG medical-device AI guidance (2025) | Exact 19 June publication fallback; cover month June retained | Joint boards, explicitly not Commission-authored; non-binding |
| EIOPA AI governance consultation (2025) | Issue 10 February; linked-file publication 11 February; consultation opens 12 February | Consultation draft, not the August final opinion |
| Horizon Europe specific programme, Decision 2021/764 | Act 10 May; OJ 12 May 2021 | Council adopter, Commission proposer; explicit predecessor repeal/savings relationship |
| EP autonomous-weapons resolution (2018) | Adoption 12 September 2018; cited OJ manifestation 23 December 2019 | Non-binding resolution; OJ item 2019/C 433/11 |
| Trustworthiness for AI in Defence white paper (2025) | Catalogue release 12 May fallback; printed 9 May retained separately | Sixteen named authors; TAID WG authorship distinct from EDA publisher; version discrepancy disclosed |

The EDA primary PDF corrected the discovery summary: it does print a publication date, and its author table cannot be replaced with sole agency authorship. Its front matter says version 1.0 while its history lists 1.1; the captured published manifestation is identified without inventing another document. `TAID WG` is a working-group abbreviation, not an assigned document reference.

## Counts and preservation

- Published documents: **187 -> 192** (102 principal, 36 supporting, 30 version, 24 attachment).
- Expanded-evidence verified: **183 -> 188**; the four qualified published records are unchanged.
- Pending unpublished candidates: **12 -> 34**. The increase comprises 21 newly tracked discoveries and one restored GPAI queue entry. Some require access/date evidence; others await full review. Pending does not mean nonexistent or impossible to verify.
- Published relationships: **114 -> 115**, adding only the explicit Horizon successor relationship.
- All 187 old IDs/routes, historical ledgers and the released v0.1.0 snapshot are preserved. No schema, gate, cutoff, DOI, licence or LLM-experiment protocol changed.

## Method and limits

The independent [baseline audit](../discovery/2026-09-06-academic-backfill/baseline-audit.md) checks all 187 records structurally and names an eleven-record purposive substantive sample. It does not claim to reread all original texts. [Health/finance](../discovery/2026-09-06-academic-backfill/health-finance.md) and [sector/history](../discovery/2026-09-06-academic-backfill/sectors-history.md) reports retain exact query strings, selected navigation, access failures and stopping rules. The latter preserves and corrects two discovery-summary errors rather than silently erasing them. Those reports are archived copies of read-only investigation outputs; references to their original outer-workspace locations describe their origin, not additional public artefacts.

[Search log](../discovery/2026-09-06-academic-backfill/search-log.json), [candidate decisions](../discovery/2026-09-06-academic-backfill/candidate-evidence.json), [before-image and capture receipts](../migrations/2026-09-06-academic-backfill.json), and [correction outcome](../migrations/2026-09-06-academic-backfill-outcome.json) support inspection. Actual response bytes and SHA-256 values were captured locally. Two Parliament requests returned empty HTTP 202 responses and are explicitly failures; their empty-body fingerprints must not be mistaken for PDF snapshots. Successful source bytes are locally retained, not promised as permanently public archives.

This batch does not exhaust official agency libraries, every version/annex, pre-2018 material, non-English manifestations, or relevant institutional and sector sources. A 1982 ESPRIT pilot lead remains pending because generic information technology does not establish substantive AI relevance. New records remain uncoded at concept/policy level until an actual research coding protocol is applied. The source sweep therefore remains `gap_found`, not complete.

## Verification

Baseline Python suite: 475 passed, 1 skipped. Nine new export regression checks first failed on the missing records/citations and wrong status, then passed after targeted integration. Full-suite and website CI results are recorded in the delivery report/PR; this file does not pre-claim their success.

The post-integration full Python run passed 484 tests with one skip; the final targeted file, including two further defence/queue checks, passed all eleven tests. The generated SQLite database contains 192 documents, passes `integrity_check` and has no foreign-key violations. The [current census](2026-09-06-academic-coverage-census.json) records overlapping sector/role counts and 74 records without concept and policy annotations.

Independent read-only review checked all five new records against the identified primary passages, all ten response receipts against cached bytes, and all 227 prior inventory decisions for preservation. It found no remaining critical or important issue after removing the spurious TAID WG document reference. Eight candidate evidence paths were changed to the committed report location. This is a substantive targeted cross-check, not a human sign-off or another fresh full-text census.
