# NDSG workplan: deep verification

Review date: 6 September 2026. Publication cutoff retained: 4 September 2026.

Candidate: `hma-ema-ndsg-workplan-2026-2028-v2`.

## Finding

The evidence blocker is resolved. The 2026-2028 workplan and the officially linked previous 2025-2028 manifestation can be represented as two independently citable versions with an evidenced revision relationship. Canonical admission and deployment have not been performed in this verification task.

An important correction is required in the predecessor description: the file currently supplied by EMA is **version 1.4, July 2025**, not an unchanged copy of the workplan first published in May 2025. The current candidate is **version 2.0, February 2026**. Do not date the v1.4 manifestation to May or assume that all intermediate versions have been recovered.

## Official sources inspected

- [EMA NDSG catalogue](https://www.ema.europa.eu/en/about-us/how-we-work/data-regulation-big-data-other-sources/network-data-steering-group-ndsg): Workplan section, previous-version panel and document-specific dates.
- [2025-2028 workplan, hosted v1.4 PDF](https://www.ema.europa.eu/en/documents/other/network-data-steering-group-workplan-2025-2028_en.pdf): all 37 pages extracted; cover, introduction and AI workstream on PDF pages 17-22 examined; cover and introduction visually inspected.
- [2026-2028 workplan, v2.0 PDF](https://www.ema.europa.eu/en/documents/other/network-data-steering-group-workplan-2026-2028-data-artificial-intelligence-medicines-regulation_en.pdf): all 36 pages extracted; cover, introduction and AI workstream on PDF pages 17-21 examined; introduction visually inspected.
- [31 March 2025 meeting minutes](https://www.ema.europa.eu/en/documents/minutes/minutes-hma-ema-joint-network-data-steering-group-meeting-31-march-2025_en.pdf): four pages, especially page 4, item 3.
- [17 July 2025 meeting minutes](https://www.ema.europa.eu/en/documents/minutes/minutes-hma-ema-joint-network-data-steering-group-meeting-17-july-2025_en.pdf): five pages inspected. These concern change management and do not independently establish the day of adoption of v1.4.
- [11 February 2026 meeting minutes](https://www.ema.europa.eu/en/documents/minutes/minutes-hma-ema-joint-network-data-steering-group-meeting-11-february-2026_en.pdf): four pages, especially pages 2-3, item 2.

Several web extraction requests returned HTTP 429. Ordinary direct requests subsequently returned HTTP 200 for all five PDFs. Actual retrieved PDFs, complete page-text extraction, retrieval timestamps and hashes are retained locally under `work/remaining-three-20260906/`. No access challenge was bypassed. The snapshots represent the bytes retrieved in September 2026, not proof of byte-identical historical availability.

## Identity, dates and status

| Fact | Evidence and interpretation |
| --- | --- |
| Authorship | Both covers name Joint HMA/EMA Network Data Steering Group. EMA is the official hosting/publishing agency. Joint network authorship must not be reduced to the name embedded in PDF software metadata. |
| First 2025 workplan adoption | The minutes of the 31 March 2025 meeting, page 4, explicitly record adoption of the 2025-2028 workplan. HMA/EMA Management Board endorsement is described as a subsequent written process; its completion is not inferred from the planned procedure. |
| First 2025 workplan publication | The catalogue's first-publication date is 7 May 2025. This is a lineage-level fact, not the publication date of July's v1.4 manifestation. |
| v1.4 issue | Cover: July 2025, month precision only. The catalogue assigns the linked document entry last update 22 July 2025. |
| v2.0 issue/adoption | Cover: February 2026; introduction, page 4: adoption by NDSG in February 2026. Preserve month precision. |
| February meeting distinction | The 11 February 2026 minutes record endorsement in principle followed by circulation for written adoption. They do **not** establish 11 February as the final adoption date. |
| v2.0 publication | The catalogue gives 9 March 2026 for this document and its page update history records publication of the revised workplan that day. |
| Legal character | An officially published institutional work programme, not an EU regulation or binding legislative act. Future deliverables are plans, not completed events. |

Recommended future canonical date representation:

- v1.4: `document_date_kind: publication`, with `document_date` and `publication_date` of `2025-07-22`. Evidence must explicitly label this as the document-specific hosted-revision publication/update fallback; preserve the cover issue month `2025-07` separately. Do not describe July 22 as a known issue or adoption day. Do not put May 7 into an unqualified first-publication field on v1.4.
- v2.0: the same publication fallback using `2026-03-09`, with cover issue and NDSG adoption retained as `2026-02` at month precision.
- PDF creation/modification metadata is corroborative at most. In particular, the v1.4 file contains a 2023 creation timestamp inherited from its production history; it cannot establish the date of this workplan.

## Substantive AI relevance and proposed classifications

The AI sections are extensive, not incidental keyword mentions. The 2025 edition has four AI dimensions: guidance/policy/product support, tools and technologies, collaboration/change management, and experimentation. The 2026 edition reorganises these into three dimensions and adds concrete work on AI guidance, risk-management practices, a prompting community, deployed analytical tools and training. Both discuss human and veterinary medicines.

Proposed editorial relevance: `direct_ai_substantive`. Strongly evidenced sector tags are `health`, `public_administration`, and `research_and_innovation`. Additional broad sectors should not be inferred merely because the plan mentions training, legislation or tools. Evidence supports joint HMA/EMA NDSG production and official EMA publication; the precise existing institutional/provenance vocabulary must be retained during any later admission.

The 2026 PDF's page 4 explicitly identifies it as the first annual revision of the earlier workplan. The EMA catalogue links the v1.4 PDF as the previous version. Together these support `v2.0 revises v1.4`; they do not claim a complete history of v1.0-v1.3.

## Gate review

Independent review of the active specification and validator confirms that a version may have an incoming or outgoing `revises`/`version_of` edge. Thus an evidenced v2.0-to-v1.4 relationship can satisfy both records. There is no recursive requirement to recover an original v1.0 or create a principal record solely to satisfy validation.

Relevant locations: `src/observatory/historical_relationships.py:151-169`; `tests/test_historical_readiness.py:368`; historical-scope specification sections 5.1-5.2; `schema/historical-document-extension.schema.json:95-107` for month-precision additional dates. This conclusion does not waive independent official evidence or the requirement that both relationship endpoints be published canonical documents when admitted.

Before admission, register and prepare the newly verified v1.4 predecessor as its own candidate, prepare both canonical records and their source/relationship records, and run the existing validations. No schema amendment is needed. Unrecovered earlier manifestations remain a disclosed coverage limitation, not fabricated links.

## Retained PDF evidence

All five successful retrievals below occurred on 6 September 2026 at approximately 01:12:53 UTC; exact timestamps are in their local extraction manifests.

| Snapshot | Pages | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| `ndsg-2025-v1-4.pdf` | 37 | 829312 | `c4218dcd0f9a55c1e4d04d92be2866e7f36aa3ea451a1d85691d3fcaa44ff52c` |
| `ndsg-2026-v2-0.pdf` | 36 | 640017 | `9a71bb191807f899f1a63867c4a30aec366b35d15bf1189413ea4f2ff793b101` |
| `ndsg-minutes-2025-03-31.pdf` | 4 | 189121 | `b2379899c2f38683e3ec36b4377755ad74e9137a7e019ed79d6af0e4d4dbfc2e` |
| `ndsg-minutes-2025-07-17.pdf` | 5 | 208048 | `0d2e0e7aa390d127315401a3b43d239f458f8e0519427108c6a1e0c3bfe570b1` |
| `ndsg-minutes-2026-02-11.pdf` | 4 | 219522 | `b93794965d452debb12c91a8c082766e2845c28edc1ad1c6cd331c1aa4443a6a` |

No canonical data, old admission decisions, public exports, source-sweep cutoff, GitHub files or live-site contents were changed by this verification.
