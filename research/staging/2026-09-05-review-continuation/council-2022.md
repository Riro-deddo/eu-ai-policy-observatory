# Council 2022 third-pass evidence audit

Reviewed by **Codex (AI-assisted evidence review)** at **2026-09-05T20:41:35Z**. Publication cutoff remains **2026-09-04**.

## Outcome

All nine Council 2022 records remain on hold. No canonical or source update is proposed.

The third pass used three new official routes rather than repeating the earlier register-detail and PDF checks:

1. The Council's own [open-data metadata guide](https://www.consilium.europa.eu/media/29364/understanding-open-data-datasets.pdf) explicitly enumerates the public-register fields. It distinguishes current **Publication status** from **Issue Date**, says publication status can vary over time, and defines the date field as the date the document was issued. It exposes no date when status changed or when the content first became public.
2. The Council [requests-for-public-access dataset](https://www.consilium.europa.eu/en/general-secretariat/corporate-policies/transparency/access-to-documents/) was searched by exact document number. It returned no request record for any of the nine documents, including searches for both `12206/22` and `12206/1/22`. Therefore it supplies no reply date that could date a release through an access request.
3. Exact EUR-Lex `CONSIL:` manifestation metadata was checked. Only `ST_15698_2022_INIT` exists there. Its metadata gives **Date of document 06/12/2022**, Council authorship, responsible body TREE.2 and form Note, but no publication-date field. The other eight exact identifiers return “The requested document does not exist.”

Bounded exact-number searches of Consilium and the relevant 2022 Presidency domains did not recover a dated page or official list directly publishing any held manifestation. Search-engine crawl dates, current availability, meeting dates and last-review timestamps were excluded as publication evidence.

## Record decisions

| Document | Decision | New evidence result | Exact remaining fact |
| --- | --- | --- | --- |
| ST 14336/22 | Hold | No access-request record; no EUR-Lex manifestation. Coreper agenda ST 14659/22 merely references it for meeting preparation. | Dated official public-release event for exact ST 14336/22; precise GSC versus Czech Presidency roles. |
| ST 13955/22 | Hold | No access-request record; no EUR-Lex manifestation; no dated exact official release. | Dated official publication for exact version; Presidency origin. |
| ST 10069/22 | Hold | No access-request record; no EUR-Lex manifestation; no dated French Presidency or Council release. | Dated publication of exact multilingual `/x/pdf` manifestation. |
| ST 13102/22 | Hold | No access-request record; no EUR-Lex manifestation; no dated Czech Presidency or Council release. | Dated official publication and Presidency origin. |
| ST 15698/22 | Hold | EUR-Lex has exact document metadata but only a document date. The dated TTE meeting page links the general approach to ST 14954/22, not ST 15698/22. | Dated official manifestation directly publishing ST 15698/22. |
| ST 11124/22 | Hold | No access-request record; no EUR-Lex manifestation; no dated exact official release. | Dated official publication and Presidency origin. |
| ST 12206/22 INIT | Hold | No access-request record; no EUR-Lex manifestation. The corrected 7 September date remains an issue date only. | Dated official publication and Presidency origin. |
| ST 12206/1/22 REV 1 | Hold | Neither access-request number form returns a record; no EUR-Lex manifestation. | Dated official publication of exact REV 1 and Presidency origin. |
| ST 12549/22 | Hold | No access-request record; no EUR-Lex manifestation; no dated exact official release. | Dated official publication and Presidency origin. |

## Audit boundary

No HTTP challenge or 403 response was bypassed. No issue, meeting, retrieval, crawl or website-modification date was promoted to `publication_date`. The detailed per-record URLs, locators and evidence results are in `council-2022.json`.
