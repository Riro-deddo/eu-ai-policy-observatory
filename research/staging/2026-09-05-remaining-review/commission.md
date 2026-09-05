# Commission remaining-record second pass

Reviewed by `Codex (AI-assisted evidence review)` at `2026-09-05T19:57:42Z`, against the fixed publication cutoff `2026-09-04`.

This is a research handoff only. It proposes one evidence-ready correction and retains ten explicit holds. It does not change canonical data, schemas, tests, prior ledgers, generated exports or Git state.

## Outcome

| Decision | Count | Records |
|---|---:|---|
| Upgrade | 1 | `final-transparency-guidelines-2026` |
| Hold | 10 | Two standardisation requests; AI-system-definition, GPAI-provider, training-notice, training-template and prohibited-practices records; three high-risk draft components |

The upgrade is not a claim that the Article 50 guidelines were formally adopted. Fresh review of the exact official pair establishes a narrower, internally consistent identity: newsroom document 131215 is the content-approved draft annex to C(2026) 5054, and newsroom document 131214 expressly says formal adoption will occur later. The official library page's `Publication 20 July 2026` field sits beside both exact downloads and can date that official release. The proposal therefore corrects the existing route from principal/final to attachment/draft, adds exact PDF sources, and adds an `annex_to` edge to the already represented approval communication.

## Exact-version findings

| Record or group | Fresh exact-file evidence | Disposition |
|---|---|---|
| Article 50 transparency guidelines | 131215: 51-page PDF, SHA-256 `30861fc5de31205846f023068069c92fabc7271ebeac6af7bef68b97f0a33f66`; cover says C(2026) 5054 and annex. 131214: 2-page PDF, SHA-256 `ea1a6d960a52d8532a068b8338622d1868616ce6b5bf2540dfef7a2378eb7c8c`; approval text says formal adoption later. | Upgrade with identity correction; no adopter role or formal-adoption claim. |
| AI-system-definition guidelines | 112455: 13-page PDF, SHA-256 `fe39f41d061184a913c32f1f92aaaa30a096858fa168c6053e22a19eef58910e`; current file is C(2025) 5053 dated 29 July 2025, while page publication is 6 February. | Hold: no version-specific publication date for the current later file. |
| Prohibited-practices guidelines | 112367: 134-page PDF, SHA-256 `298bf8677884b333fae6d5f84aac947f45a59dff6027ca038ba08615092fd82f`; current file is C(2025) 5052 dated 29 July 2025, while page publication is 4 February. | Hold: no version-specific publication date for the current later file. |
| GPAI-provider guidelines | 118340: 36-page PDF, SHA-256 `13481bd90108505c477165c8aefb13dbe7a83847bad0e983e09115f78aeefe78`; current file is C(2025) 7719 dated 19 November 2025, while page publication is 18 July. | Hold: no version-specific publication date for the current later file. |
| Training-content explanatory notice | 118480: 15-page PDF, SHA-256 `be6cdf10131c3fd9eb9265e592b23609fd7df2d2c9692517017f739188d408be`; current file is C(2025) 8311 dated 5 December 2025, while page publication is 24 July. | Hold: no version-specific publication date for the current later file. |
| Training-content template | 118578: 70,622-byte DOCX, SHA-256 `ec803008a5263a485146b24497a3445e2ea32f8b73f818e67652ad70de40f09b`; body is the Article 53(1)(d) template, but internal creation/modified time is 28 July 2025, after the 24 July release. | Hold: current bytes are not safely identified as the 24 July exact version. |
| High-risk draft sections | 128559: 6 pages, SHA-256 `b127bbdc50b1741bb2d97e8aff5839cccd1a4484445be4e8cca246c12541fc42`; 128560: 13 pages, SHA-256 `10f1302c9090d2bcfdb8eacd2b36ff7a09860fc7909f7c1c4b42cc3b9bed3b50`; 128561: 148 pages, SHA-256 `b1df0ffb30310e126c7e060e03c9b5aab97c0a2ab61a2f3e3e00ede3655e2792`. All three covers say `ANNEX` to an unidentified Commission communication and retain placeholder reference text. | Hold all three: exact components and 19 May release are verified, but retained attachment routes lack an evidenced parent identity. |
| Standardisation requests C(2023) 3215 and C(2025) 3871 | Exact Register routes and act/decision dates were rechecked. The Register FAQ says its `Date` most commonly denotes Commission adoption. The client-rendered detail response did not yield a separately labelled publication date. | Hold both: issue/adoption is not relabelled as publication. |

## Three-part high-risk parent issue

The official Commission library and press pages describe a single draft guideline work divided into three separately downloadable sections, and the AI Act Service Desk also links the three PDFs. That proves the grouping and release, but none of those sources supplies a separately issued parent communication or formal parent reference. All exact covers instead contain `Brussels, XXX`, `[…](2026) XXX draft`, and `ANNEX to the COMMUNICATION FROM THE COMMISSION`.

Under the existing attachment-lineage contract, the three records therefore remain held. If the project later wishes to treat a landing-page representation of a multi-file work as a conceptual parent despite no separately issued parent artifact, that is a scope/model decision for the root reviewer—not a fact to infer during evidence review.

## Source-handling notes

- The official binaries were freshly retrieved and inspected during this pass. Their checksums document the reviewed bytes; no local snapshot is proposed as an archival source.
- Existing source retrieval timestamps are preserved. Only the two freshly retrieved Article 50 PDFs receive new `retrieved_at` values in the proposed source objects.
- A landing-page `Last update` date is never used to date a changed binary.
- Commission hosting is not treated as proof of authorship or commissioning; roles are asserted only where the exact artifact identifies them.

The machine-readable handoff contains every checked URL, locator, correction, hold reason, the complete proposed document patch, two exact source objects, the source update, and the proposed relationship.
