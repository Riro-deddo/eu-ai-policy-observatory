# Council later documents: third-pass evidence review

Reviewed by: AI-assisted evidence review

Reviewed at: 2026-09-05T20:34:24Z

Publication cutoff: 2026-09-04

## Verdict

All six records remain on hold: **0 ready, 6 hold**. If accepted, the corpus remains **101 verified / 30 pending**.

The third pass found additional official identity, attribution and legislative-context evidence, but no dated official publication manifestation for any exact held version. The decisive new source is the Council's own public-register metadata guide: it defines `Publication status` as a mutable status at consultation time and `Issue Date` as the date a document is issued. Therefore a current `Public` result plus the masthead date does not establish when the exact manifestation was published.

## Record findings

| Document | Decision | Exact issue/role evidence | New publication-date search result |
|---|---|---|---|
| `ai-act-council-adoption-note-st-9645-2024-rev-1` | Hold | ST 9645/1/24 REV 1 is dated 15 May 2024; Council/GSC cover note. ST 10036 cites the exact REV 1 in the 17 May A-item package; ST 10172 records adoption on 21 May. | None. The later package and minutes establish scheduling/adoption, not publication of REV 1. |
| `ai-act-council-adoption-statements-st-9645-add-1-rev-2` | Hold | Exact ADD 1 REV 2 dated 15 May 2024. France and Austria authored the statements; Council is the wrapper. ST 10036 cites the exact addendum. | None. EUR-Lex identity was found, but the direct metadata page required JavaScript verification and supplied no usable publication date. |
| `ai-omnibus-council-adoption-note-st-10752-2026` | Hold | Exact INIT dated 22 June 2026; GSC cover-note sender. Its recommendation is conditional, while 29 June sources establish subsequent Council adoption. | None. The EUR-Lex `Date of document` is 22 June, not a publication field; the dated press release publishes/links PE-CONS 30, not this ST note. |
| `ai-omnibus-council-adoption-statements-st-10752-add-1` | Hold | Exact ADD 1 dated 22 June 2026. Belgium and the Commission authored the statements; Council is the wrapper. | None. The A-item list cites `10752/26 + ADD 1` but does not state when ADD 1 became public. |
| `ai-omnibus-council-adoption-statement-st-10752-add-2` | Hold | Exact ADD 2 dated 24 June 2026. Greece authored the statement; Council is the wrapper. | None. The public vote record and 29 June press release establish adoption context only. |
| `ai-omnibus-council-information-note-st-10599-2026` | Hold | Exact INIT dated 17 June 2026; GSC cover-note sender. The annex is Parliament text P10_TA(2026)0198, adopted 16 June, rather than Council-authored text. | None. The annex's adoption date and the later Council adoption are not publication of ST 10599/26. |

## Official sources and locators

- [Council public-register metadata guide](https://www.consilium.europa.eu/media/29364/understanding-open-data-datasets.pdf), PDF pages 14-15 and 18: `Publication status` is a separate, time-varying field; `Issue Date` is the document's issue date.
- [ST 10036/24](https://data.consilium.europa.eu/doc/document/ST-10036-2024-INIT/en/pdf): A-item package issued 17 May 2024, citing `9645/1/24 REV 1 + ADD 1 REV 2`.
- [ST 10172/24](https://data.consilium.europa.eu/doc/document/ST-10172-2024-INIT/en/pdf): draft minutes issued 28 May 2024, recording Council adoption on 21 May and citing the exact 9645 versions.
- [ST 10932/26 REV 1](https://data.consilium.europa.eu/doc/document/ST-10932-2026-REV-1/en/pdf): 29 June A-item list citing `10752/26 + ADD 1` and PE-CONS 30/26.
- [ST 11301/26](https://data.consilium.europa.eu/doc/document/ST-11301-2026-INIT/en/pdf): public vote record dated 29 June 2026.
- [Council press release, 29 June 2026](https://www.consilium.europa.eu/en/press/press-releases/2026/06/29/artificial-intelligence-council-gives-final-green-light-to-simplify-and-streamline-rules/): establishes final Council approval and links the legislative text, not the held ST manifestations.
- Exact EUR-Lex mirrors were queried for `ST_9645_2024_REV_1`, `ST_9645_2024_ADD_1_REV_2`, `ST_10752_2026_INIT`, `ST_10752_2026_ADD_1`, `ST_10752_2026_ADD_2`, and `ST_10599_2026_INIT`. Readable results repeated `Date of document`; none supplied an independently labelled publication date.

## Search coverage and limitations

Exact-number searches covered the Council public register, Council-hosted PDFs, dated A-item lists/minutes/vote records, the Council press release and EUR-Lex Council-document mirrors. Exact-number public-access request searches returned no dated request record for these manifestations.

No access control was bypassed. Some EUR-Lex direct opens returned JavaScript verification, cache-miss or safe-URL errors. Search-result crawl/age labels were deliberately excluded because snippets are not official full-text or metadata evidence. The dynamically updated Council latest-documents feed was also excluded as publication-date evidence because its item dates repeat document issue dates and do not provide a historical release timestamp.

No canonical patch or source update is proposed for any of the six records.
