# Official PDF Evidence Batch — 2026-09-05

**Status: bounded canonical-evidence batch completed locally; not published.**

This bounded batch adds source-file provenance to five existing records, not five new documents. The corpus still contains 117 published documents and 95 relationships, with the same document IDs, slugs, publication dates and record levels. All five relationship-readiness holds remain explicit. No Phase B completion or corpus-completeness claim is made.

The machine-readable [evidence ledger](2026-09-05-official-pdf-evidence.json) includes every changed field's before/after value, five direct official sources, checksums, download receipts and inspection limits. The [implementation plan](../../docs/superpowers/plans/2026-09-05-official-pdf-evidence.md) defines this batch.

## Evidence added

| Existing record | Official file | Pages | Text review |
| --- | --- | ---: | --- |
| High-risk serious-incident guidance | [119624](https://ec.europa.eu/newsroom/dae/redirection/document/119624) | 13 | PDF pages 1–3 and 13 |
| High-risk serious-incident reporting template | [119623](https://ec.europa.eu/newsroom/dae/redirection/document/119623) | 7 | All seven pages |
| High-risk classification: General principles | [128559](https://ec.europa.eu/newsroom/dae/redirection/document/128559) | 6 | PDF pages 1–2 |
| High-risk classification: Annex I | [128560](https://ec.europa.eu/newsroom/dae/redirection/document/128560) | 13 | PDF pages 1–2 |
| High-risk classification: Annex III | [128561](https://ec.europa.eu/newsroom/dae/redirection/document/128561) | 148 | PDF pages 1–2 |

One selected page per file was also visually checked; exact pages are recorded in the ledger. Download success is not a claim that every page was substantively reviewed. The incident template's official version label is now **1.0.0**, as printed on its cover; its existing draft status remains unchanged.

Five canonical `snapshots` entries carry direct source IDs, hashes, format and retrieval-time proxies. Existing SQLite generation stores those values. The current public JSON exporter exposes the linked sources and corrected version label but does not export snapshot objects; no new UI/export feature is claimed.

## Provenance limits

- Original responses remain in the ignored local review directory `work/source-review-2026-09-05-b3/`, not a committed archive. All `archived_path` values are null. Other repository users will not receive those local bytes automatically.
- Retrieval timestamps are observed NTFS local file-write-completion times immediately after downloading. They are operational proxies, not precise HTTP completion measurements. Verification time is separately recorded as `2026-09-05T08:20:53Z`.
- The download tool emitted status, final URL and the malformed Content-Type value `/`. Normalized receipts are preserved from its stdout in the ledger. PDF signature, Poppler and pypdf establish actual file format; headers cannot be recovered from PDF bytes.
- Hashes were independently recomputed on resumption and matched all five original download observations.
- PDF creation metadata, cover placeholders and the template's page-7 form date do not replace publication dates. The release cutoff remains 4 September 2026.

## Unresolved work

The three guideline files are sections of one draft work. The Commission library describes separately downloadable sections, and the official Service Desk links a full draft Explorer. Direct Explorer access returned a JavaScript shell; a parallel reviewer found indexed text, but the controller did not independently retain the complete online text. No combined PDF, formal covering-communication identity or new public parent record is claimed.

Independent editorial review found positive grounds for treating each incident document as a principal instrument. Reclassification is deliberately deferred; it is not an unresolved claim that the two files exist. Keeping the current version-level records means their readiness holds still apply. Neither file is represented as a version of the other.

The template's linked discovery candidate still retains its original label `Consultation draft` in `research/corpus-inventory.json`. That discovery-stage record is not current canonical version-label authority and is not exported as public document metadata. Reconciliation is explicitly deferred to an inventory review rather than silently rewriting discovery history.

A bounded final-successor search encountered a broken Commission implementation-overview link. It established no new final document identity, not universal absence of such a document.

## Verification and handoff

The resumed unchanged baseline passed with **308 passed, 1 skipped**. The skip is the existing Windows chmod/ACL negative test. New tests initially failed on the missing five snapshots, SQLite evidence and audit ledger; all 13 targeted tests then passed after the first data implementation.

The complete suite passed with **316 passed, 1 existing Windows ACL skip**, without deselection. Independent review found no blocking issues and separately passed all 13 targeted tests. Its later shell-start failure prevented independent reopening of the added verification-receipt fields; the controller supplied those fields explicitly, and no canonical data changed during that handoff.

All 12 canonical objects match the audit ledger. Reversing only the recorded changes recovers the exact base objects, while all five new sources are absent from that base. All 117 public IDs/slugs and 95 relationships remain intact. The inactive historical preflight still reports 1,668 issues, including the same five relationship holds; this is not overall historical readiness.

The protected generated JSON/SQLite pair retains its pre-batch hashes and remains unchanged pending a later controlled rebuild. The work stays on the local historical-corpus branch; use Git history for this report's commit. No push, merge or GitHub Pages deployment occurred. The next separate batch must review the whole-guidelines endpoint and the incident documents' editorial classifications.
