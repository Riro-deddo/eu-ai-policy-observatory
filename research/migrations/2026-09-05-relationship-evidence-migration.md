# Relationship evidence migration — 2026-09-05

AI-assisted reviewer completed a narrow editorial review at `2026-09-05T07:35:00Z`, against publication cutoff `2026-09-04` and base commit `f4085fdf6ada9da4954f815738ff2b8bffe81ec0`. The machine-readable ledger is [`2026-09-05-relationship-evidence-migration.json`](2026-09-05-relationship-evidence-migration.json).

The migration corrects three final GPAI chapter edges from `version_of` to `part_of`, adds four third-draft component edges, and represents three administrative forms conservatively as `supporting` records with `related_to` associations. Commission HTML positively establishes the forms' supporting or signing purposes; linked binary interiors were not inspected, so no stronger binary structure is claimed.

The General-principles high-risk-guidelines record is corrected from `version` to `attachment`. Its two former `version_of` edges now record analytical sibling association only. Those three records remain held until a whole-guidelines endpoint is represented. The serious-incident guidance and template also remain held because co-issuance of separate consultation documents does not establish same-work version lineage.

This resolves the relationship-readiness issue for 10 of the 15 reviewed targets and retains five explicit holds. It does not establish overall historical readiness, verify every record field or classification, or claim corpus completeness. No source snapshots were retained. The canonical relationship count is now 95 and the document count remains 117.

The protected `generated/public-data.json` and `generated/eu-ai-policy-observatory.sqlite` files remain the pre-migration pair pending a later controlled rebuild. Temporary pipeline output is used for verification only.

## Verification receipt

Implementation commits: `bfe49d1` and `7856bdd`. Independent task and integration reviews found no blocking issues; the final scoped re-review confirmed both small evidence/test refinements were addressed.

The final controller Python run completed with **308 passed and 1 skipped** in 15.01 seconds. The skip is an existing Windows chmod/ACL negative test, not a skipped migration check. All tests ran without deselection. No frontend/browser release verification or deployment is claimed.

All thirteen modified canonical objects were compared with the base commit and the ledger: reversing only the recorded changes recovered the original objects exactly. Temporary SQLite and JSON exports preserved the frozen 117-document ID/slug baseline. The protected generated-pair hashes remained unchanged.

## Decisions and risks

- Retained the existing safety-chapter relationship ID instead of the mistaken longer filename in the initial plan. An incorrect mapping could have modified the wrong edge; exact endpoint regression checks verify the intended document.
- Updated the obsolete chapter-as-version test expectation and moved a legacy identity test from a blocked repository-local temporary directory to pytest's temporary directory. The risk was weakening the identity invariant; all original migration and ordered-ID/slug assertions were retained and passed.

## Remaining work

The three high-risk-guidelines sections need a represented whole-guidelines endpoint. The two serious-incident drafts need further editorial-level and genuine lineage review. The wider 117-record historical evidence migration and later new-document admissions are not complete. This batch does not establish a complete EU AI corpus, and nothing was pushed to GitHub or published.
