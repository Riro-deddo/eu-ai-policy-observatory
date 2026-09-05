# Relationship evidence migration — 2026-09-05

Codex completed a narrow editorial review at `2026-09-05T07:35:00Z`, against publication cutoff `2026-09-04` and base commit `f4085fdf6ada9da4954f815738ff2b8bffe81ec0`. The machine-readable ledger is [`2026-09-05-relationship-evidence-migration.json`](2026-09-05-relationship-evidence-migration.json).

The migration corrects three final GPAI chapter edges from `version_of` to `part_of`, adds four third-draft component edges, and represents three administrative forms conservatively as `supporting` records with `related_to` associations. Commission HTML positively establishes the forms' supporting or signing purposes; linked binary interiors were not inspected, so no stronger binary structure is claimed.

The General-principles high-risk-guidelines record is corrected from `version` to `attachment`. Its two former `version_of` edges now record analytical sibling association only. Those three records remain held until a whole-guidelines endpoint is represented. The serious-incident guidance and template also remain held because co-issuance of separate consultation documents does not establish same-work version lineage.

This resolves the relationship-readiness issue for 10 of the 15 reviewed targets and retains five explicit holds. It does not establish overall historical readiness, verify every record field or classification, or claim corpus completeness. No source snapshots were retained. The canonical relationship count is now 95 and the document count remains 117.

The protected `generated/public-data.json` and `generated/eu-ai-policy-observatory.sqlite` files remain the pre-migration pair pending a later controlled rebuild. Temporary pipeline output is used for verification only.
