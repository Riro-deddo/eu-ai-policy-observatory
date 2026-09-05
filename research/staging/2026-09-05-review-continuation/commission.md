# Commission third-pass evidence review

Reviewed by Codex (AI-assisted evidence review) at 2026-09-05T20:45:17Z, with the fixed publication cutoff 2026-09-04.

## Outcome

This bounded third pass reviewed exactly ten Commission holds. Two records are evidence-ready and eight remain held.

The new resolving evidence is a distinct official AI Act Service Desk Resources manifestation. Its page-1 index shows separate 06/05/2026 Guidelines cards for the AI-system-definition and prohibited-practices texts, and each card links directly to a PDF. The linked PDFs are C(2025) 5053 final and C(2025) 5052 final. Their rendered covers show the exact Commission communication identities, and complete whitespace-normalized text matches the current official newsroom PDFs despite different PDF wrapper bytes. Under section 5.1 of the readiness contract, 6 May 2026 can therefore be used as the publication represented by those later official sources. It is not a claim that this was the first time either text appeared anywhere.

| Decision | Record | Finding |
| --- | --- | --- |
| Ready | `ai-system-definition-guidelines-2025` | Official Service Desk card dated 06/05/2026 directly serves the exact C(2025) 5053 final text. Keep issue date 29 July 2025; use 6 May 2026 as the cited manifestation's publication date. |
| Ready | `prohibited-ai-practices-guidelines-2025` | Official Service Desk card dated 06/05/2026 directly serves the exact C(2025) 5052 final text. Keep issue date 29 July 2025; use 6 May 2026 as the cited manifestation's publication date. |
| Hold | `ai-standardisation-request-c-2023-3215` | The exact Register detail gives Date 22/05/2023 and downloads, while the Register FAQ defines Date as most commonly Commission adoption. No separate publication date was found. |
| Hold | `standardisation-request-c-2025-3871` | The exact Register detail gives Date 23/06/2025 and downloads for C(2025)3871/M/613. The date is adoption/decision evidence, not separately labelled publication. |
| Hold | `gpai-provider-guidelines-2025` | The dated 27/08/2025 Service Desk PDF is the earlier C(2025) 5045 approval annex, not current C(2025) 7719. The Register confirms C(2025)7719 and 19/11/2025 but marks it not published. |
| Hold | `gpai-training-content-explanatory-notice-2025` | The Register confirms C(2025)8311 and 05/12/2025 but marks it not published. The 24 July library publication and later generic update do not date that later exact PDF. |
| Hold | `gpai-training-content-template-2025` | The 20/10/2025 Service Desk card links to a press release, then a mutable library page, rather than directly to DOCX 118578. The current DOCX was created/modified 28 July; these internal fields are not publication evidence. |
| Hold | `draft-high-risk-classification-guidelines-2026` | Exact cover remains an ANNEX to an unidentified draft communication; no parent artifact/reference exists. |
| Hold | `draft-high-risk-classification-guidelines-annex-i-2026` | Section III is a separately downloadable component, but remains an ANNEX with no parent identity. |
| Hold | `draft-high-risk-classification-guidelines-annex-iii-2026` | Section IV is a separately downloadable component, but remains an ANNEX with no parent identity. |

## Exact-version checks

- Definition Service Desk PDF: 13 pages, 343,210 bytes, SHA-256 `43202a8965f7f912987b3eef1d699fb6f201a7e984f41e91bc28674d48b4a501`. The current newsroom 112455 PDF is 333,765 bytes, SHA-256 `fe39f41d061184a913c32f1f92aaaa30a096858fa168c6053e22a19eef58910e`; normalized full text is identical.
- Prohibited-practices Service Desk PDF: 134 pages, 1,319,114 bytes, SHA-256 `8b7cb759a821b70e19b5188c72aaf44c5978088777e3035ff9633dda5e9d4244`. The current newsroom 112367 PDF is 1,204,912 bytes, SHA-256 `298bf8677884b333fae6d5f84aac947f45a59dff6027ca038ba08615092fd82f`; normalized full text is identical.
- GPAI Service Desk PDF: 36 pages, 570,508 bytes, SHA-256 `6809d563ec3df310f55002d3fcfbcea748877f2b2215a07e62a31a3c4bba5517`. Its cover is C(2025) 5045 final, 18 July 2025, and its normalized full text differs from current newsroom 118340, which is C(2025) 7719 final, 19 November 2025, 544,991 bytes, SHA-256 `13481bd90108505c477165c8aefb13dbe7a83847bad0e983e09115f78aeefe78`.

## High-risk lineage conclusion

The official library page is a real work-level representation: it says the Guidelines are divided into sections and provides three separately downloadable files. The Service Desk likewise exposes an online explorer and describes the PDFs as the complete draft. That evidence does not solve the retained attachment contract. Each exact PDF cover says ANNEX to a Commission communication, keeps `XXX` placeholders, and names no parent. The official consultation says final guidelines will be adopted later. Neither changing these files to principal records nor inventing a composite parent is justified by the reviewed evidence.

## Handoff boundaries

The JSON contains complete proposed patches and three proposed new source objects only for the two ready records. It proposes no relationship edits and no updates to existing sources. The eight holds have no patch. No canonical files, tests, schemas, ledgers, generated exports, or Git state were changed.
