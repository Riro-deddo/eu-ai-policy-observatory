# Fresh recheck of four qualified published records

Review receipts: 6 September 2026 UTC (7 September in Europe/London). Historical inclusion cutoff remains **4 September 2026**. This is a bounded evidence recheck, separate from the 34-candidate review.

## Outcome

All four records remain **retain_qualified_pending**. No qualifying new evidence justifies a canonical change. Their existing published routes, qualifications, date fields and historical review timestamps are preserved. No schema exception, publication operation, external correspondence or human sign-off is introduced.

| Record | Existing qualification | Fresh result |
| --- | --- | --- |
| standardisation-request-c-2025-3871 | publication_date_pending | Exact eNorm metadata adds first-ingest evidence, not a public-release day. |
| gpai-training-content-explanatory-notice-2025 | parent_evidence_pending | Original July ANNEX remains available; distinct MAIN public release remains unproved. |
| gpai-training-content-template-2025 | parent_evidence_pending | Original internal template is available; the same MAIN ancestor gap persists. |
| ai-act-council-third-compromise-part-one-st-12206-2022-init | official_version_conflict | Later Council cross-reference preserves the distinction but does not recover or correct INIT. |

## 1. Standardisation request C(2025)3871 / M/613

Fresh Commission register metadata and the official final PDF are byte-identical to the retained captures. Adoption is 23 June 2025; the register labels 27 June 2025 13:50:51 as transmission. Neither is relabelled publication.

A materially different official route was checked: the Commission's eNorm application and its public corporate-search service. The exact [613_en metadata](https://webgate.ec.europa.eu/es/search-api/rest/document/613_en?apiKey=ENORM_PROD), retrieved at 23:11:41 UTC, explicitly identifies C(2025)3871 and M/613. It records adoptionDate on 23 June 2025, esDA_FirstIngestDate on 27 June 2025 at 15:21:27.320 +0200, and esDA_IngestDate on 15 June 2026. These labels describe adoption and technical ingestion; they do not establish that this exact manifestation was publicly released on the first-ingest day. No publication field resolving the hold was recovered.

The route was established from the publicly served application configuration and document service. An initial path on the SPA host returned its HTML shell, not a document. This failed metadata attempt is logged, not treated as an empty authoritative record. Current accessRestriction:false also does not establish historical release timing.

Reopen only for an official dated public manifestation or explicit publication record identifying this exact decision.

## 2-3. July GPAI explanatory notice and training-content template

The fresh [Commission C(2025)5235 register response](https://ec.europa.eu/transparency/documents-register/api/search/C(2025)5235?lang=en) remains byte-identical: separate MAIN and ANNEX entries have null ersId values. Its 24 July transmission timestamp is not evidence of the MAIN's public release.

The [Commission library](https://digital-strategy.ec.europa.eu/en/library/explanatory-notice-and-template-public-summary-training-content-general-purpose-ai-models) still labels publication 24 July 2025 and links the original ANNEX PDF and template files. The original ANNEX PDF's fresh hash matches the preserved copy. The template is present at PDF pages 9-14; it is not missing, and an editable-file requirement is not added.

These positive findings confirm the original ANNEX and its internal template, but not publication of the distinct approval MAIN. Later December C(2025)8311 and OJ work-level July publication do not remove that exact-version ancestor gap. Both records retain their existing parent-evidence qualification under the unchanged admission rule.

Reopen both when the official C(2025)5235 MAIN manifestation and qualifying public-release evidence are recovered. A proposed parent-rule change would require separate explicit review, not an exception here.

## 4. Council ST12206/22 INIT

Fresh official INIT and REV 1 PDFs match their respective retained hashes. The INIT download still carries the 16 September 2022 third-compromise cover, conflicting with the previously evidenced 7 September second-compromise register identity. The public-register HTML request returned HTTP 403; this is recorded as an access limitation, not proof of absence.

The additional official [ST12549/22 INIT](https://data.consilium.europa.eu/doc/document/ST-12549-2022-INIT/en/pdf), dated 23 September 2022, was retrieved independently. Its cover identifies 12206/1/22 REV 1 as predecessor. Page 3, paragraph 7 separately identifies document 12206/22 as the second compromise. This is useful corroboration that the identities should remain distinguished. It does not provide the original 7 September bytes or an explicit Council correction.

Reopen only on recovery of that original INIT manifestation or an explicit official correction reconciling the conflict. No REV 1 substitution or inferred publication-date correction is made.

## Audit package and limits

- [decision-ledger.json](retained-records.json): exactly four dispositions, confirmed facts, new evidence, unresolved issue and reopening trigger.
- [query-log.json](retained-query-log.json): actual search terms, direct paths, timestamped request index and access limitations.
- [captures/receipts.json](retained-source-checks.json): metadata-only receipts; full responses and excerpts remain local-only and are not included in the release archive.
- Search result captures are retained only in the local audit package. Repeated large-output attempts that were truncated were not represented as complete body captures.
- The four original PDF files remain in the sibling release-closure-cache directory and were not overwritten. New Council ST12549/22 was read in memory; only its receipt and first-three-page text were retained.

This package makes no claim that every possible official route has been exhausted. A no-change result closes this bounded task, not the underlying evidence questions. Parent integration, repository-wide validation and snapshot publication are outside this subtask.
