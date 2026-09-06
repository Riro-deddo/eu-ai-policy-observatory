# Fresh recheck of twelve legacy pending candidates

Reviewed by AI-assisted evidence review at 2026-09-06T22:54:39Z. Scope cutoff remains 4 September 2026. This is the first-stage recheck of exactly twelve pre-existing candidates; it does not review the four retained published holds, certify a wider search, change canonical files, or approve publication.

## Result

Nine Parliament amendment compilations now have sufficient version-specific publication evidence for inclusion. Three AI Board reports remain pending. No merger or exclusion is recommended. The prior full-text PDFs were preserved without modification.

The materially new evidence is the Parliament Open Data API's English **Manifestation** metadata and its linked downloadable distribution, distinct from the catalogue's **Work** date. Every fresh English distribution PDF is byte-identical to the retained PDF, and every work identifies version 0100. This resolves the previously unexplained relationship between the 10 June catalogue date and the 13 June English cover. It does not turn the catalogue date into publication.

## Parliament: exact dates and identity

All nine retained covers state **13 June 2022** and **v01-00**. Use `document_date=2022-06-13` and `document_date_kind=document_issue`. Use the date component of the exact English PDF manifestation's `issued` timestamp for `publication_date`.

| PE reference | Amendments | English PDF formal issuance | Bytes |
| --- | --- | --- | ---: |
| PE732.802v01-00 | 310 - 538 - | 2022-06-20T16:46:31+02:00 | 626876 |
| PE732.836v01-00 | 539 - 773 - | 2022-06-21T11:56:20+02:00 | 634476 |
| PE732.837v01-00 | 774 - 1189 - | 2022-06-21T13:16:23+02:00 | 568230 |
| PE732.838v01-00 | 1190 - 1580 - | 2022-06-21T13:16:25+02:00 | 560499 |
| PE732.839v01-00 | 1581 - 2005 - | 2022-06-21T13:16:24+02:00 | 570221 |
| PE732.840v01-00 | 2006 - 2355 - | 2022-06-21T13:16:22+02:00 | 584324 |
| PE732.841v01-00 | 2356 - 2726 - | 2022-06-21T13:16:23+02:00 | 574114 |
| PE732.843v01-00 | 2727 - 3019 - | 2022-06-21T13:16:25+02:00 | 479860 |
| PE732.844v01-00 | 3020 - 3312 - | 2022-06-20T16:36:22+02:00 | 430763 |

For every record, the API also provides Work `document_date=2022-06-10`, `epNumberVersion=0100`, publisher `org/EU_PARLIAMENT`, and `foresees_change_of=eli/dl/doc/CJ40-PR-731563`. The date distinction is encoded in the official [API context](https://data.europarl.europa.eu/api/v2/context.jsonld): `document_date` maps to `eli:date_document`; `issued` maps to `dcterms:issued`, typed `xsd:dateTime`. The vocabulary defines the latter as the resource's formal issuance date ([DCMI](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/terms/issued/)). The evidence is therefore specific to the English PDF manifestation. It is not an HTTP Last-Modified substitution; HTTP dates are retained only as ancillary receipts.

The fresh distribution URLs redirect to Parliament's `redmapl3.europarl.europa.eu` host. Each body starts with a PDF signature, has the API-stated length, and matches the previously retained SHA-256. Exact hashes, API/distribution URLs, retrieval times, and capture paths are in [decision-ledger.json](decision-ledger.json) and [query-log.json](query-log.json). The complete decoded official API responses are retained under `captures/`; their original UTF-8 body byte lengths and hashes were verified by reconstructing the recorded content.

The ten June value remains explicitly labelled in each draft's researcher notes and source verification note as the Work/catalogue date. No existing additional-date enum means catalogue/work date, so no ad hoc enum was invented and no ten June publication date was added.

Each document is a supporting `report` with `legal_status=proposed` and `version_status=draft`. It is a distinct proposed amendment compilation, not an adopted institutional position or enacted amendment. Individual sponsors are credited in the PDF. Cover rapporteurs describe the underlying draft report, not authorship of all amendments. The draft notes explain that sponsor rosters and concepts have not been exhaustively indexed. Relevance and horizontal-sector classifications cite inspected substantive amendment passages, not only title keywords.

Each draft has an official `procedural_step_for` relationship to existing `ep-ai-act-draft-report-pe-731563`, backed by the cover and API `foresees_change_of`. No revision, legal amendment, or adoption is inferred.

## AI Board: three holds remain

The three candidates remain pending independently:

- `ai-board-harmonised-standards-report-2026` — AIB2025-doc2 / SG Standards2025-1; retained `board-D1.pdf`.
- `ai-board-article-40-standardisation-report-2026` — AIB2025-doc3 / SG Standards2025-2; retained `board-D2.pdf`.
- `ai-board-international-standardisation-report-2026` — AIB2025-doc4 / SG Standards2025-3; retained `board-D3.pdf`.

The new [20 March Commission news article](https://digital-strategy.ec.europa.eu/en/news/seventh-ai-board-meeting) identifies the seventh meeting and reports endorsement of three subgroup reports with publication still forthcoming. This corroborates the register's seventh-meeting description and makes it especially inappropriate to treat 20 March as an evidenced release date. It still does not enumerate the three exact reference/version identities.

The [June meeting news](https://digital-strategy.ec.europa.eu/en/news/ai-board-convenes-its-eight-meeting), published 12 June and updated 17 June, likewise refers generally to endorsed subgroup documents with future publication. It does not identify these precise versions. Fresh `expertGroups/3966` metadata supplies group-level publication and update dates, not report-level release dates; fresh `meetings/67904` contains the existing download identities but no per-document issue/publication timestamp. Exploratory document metadata routes returned 404 and are logged as unsuccessful routes, not absence findings.

The retained reports still give only March 2026 on the covers. June PDF creation/modification metadata and Ares registration are separate technical/registration facts, not public-release evidence. The mismatch between the minutes' ordinal and the register is not enough by itself to reject the documents; the remaining decisive hold is missing exact version-specific issue/adoption and public-release evidence.

Reopen each Board candidate when an official record binds its exact report reference/version to an exact issue/adoption date and public-release date. No calendar day was imputed to March.

## Integration package and verification

Archive boundary: this is the original investigator's proposal report. Paths such as `captures/`, `drafts/data/` and the ledger's `retained_pdf` are relative to the investigator's local audit package, not this repository directory. Complete multilingual API response bodies and full PDFs remain local-only; they are not included in the public research snapshot. Published source records and this ledger retain official URLs, exact retrieval times, hashes and field-level locators. The nine accepted records were subsequently integrated; this report's original draft-status statements describe its preparation stage, not their current status.

`drafts/data/` contains 37 schema-compatible draft records: nine documents, eighteen individual PDF/API sources, one shared official API-context source, and nine procedural relationships. All remain `publication_status=draft`; root integration and deliberate publication are still required. Snapshot hashes represent actually retrieved official PDF bytes, with `archived_path=null`; retained earlier local PDFs are preserved outside the repository.

Verification: all 37 drafts pass the current canonical-record schema; all nine documents pass the historical-evidence extension. Nine English PDF manifestations match retained bytes and API lengths/version/date identities. Fifteen captured non-PDF response bodies reproduce their stored original lengths and SHA-256 hashes. All twelve decisions are present; nine recommend inclusion and three remain pending. See [verification.json](verification.json).

Access limitations were recorded rather than silently treated as zero results: initial web-tool access to Parliament API/register routes failed, some Commission news opens returned 429, the register homepage presented JavaScript anti-bot content, and exploratory aliases returned 404. Ordinary Python urllib subsequently retrieved the exact Parliament metadata, distribution PDFs and Board news/register records. No institutional contact was messaged. No canonical or Git changes were made by this subtask.
