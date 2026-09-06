# Admission ledger — plan: docs/superpowers/plans/2026-09-06-fifty-three-candidate-admissions.md

Baseline: 131 published canonical documents; 105 expanded reviews verified; 26 legacy expanded-review holds remain outside this task. Existing isolated repository and codex/remaining-evidence-review branch retained under prior explicit workspace preference.

Queue: 33 new main identities plus 20 outstanding prior candidates, exactly as audit.json. No follow-up leads or other inventory pending records added.

Allocation: historical9; rights15; sectoral21; commission8. Shared canonical integration belongs to root only.

Preflight: all groups consume the same approved evidence gate and publish no records independently. No conflicting write paths. Data curation uses existing validators; no schema/UI feature implementation is planned.

- [x] Baseline verification: 131 documents; 105 verified; 26 existing holds. Baseline Python suite: 404 passed, 1 skipped.
- [x] Historical evidence bundle: 8 admitted; JURI report pending after official endpoint retries.
- [x] Rights evidence bundle: 15 admitted, including the recovered Frontex report.
- [x] Sectoral evidence bundle: 20 admitted; NDSG version 2 pending predecessor verification.
- [x] Commission evidence bundle: 7 admitted; corrected scientific opinion pending original-edition verification. Work is split into commission-base.json and commission-experts.json.
- [x] Canonical integration and independent review: 50 documents, 97 sources, 21 institutions and 11 relationships added. One minor official-date discrepancy documented; no critical or important findings remain.
- [x] Deterministic export and final reconciliation: final/final-repeat pairs match; SQLite integrity and foreign keys pass; exactly 53 decisions reconcile to 50 admitted and 3 pending.
- [x] Node source/unit tests: 65 passed against the final expanded export.
- [x] Python testing: worker full suite 404 passed, 1 skipped. Root full suite 402 passed, 1 skipped, 2 failures caused only by denied access to protected generated/public-data.json. No production changes were made to work around permissions.
- [ ] Fresh Astro/Vitest/rendered-site checks: blocked by existing Windows directory permissions. Public-build scanner and browser end-to-end checks not run against a fresh build.

Final authoritative deliverables are in work/gap-admission-20260906/final, not the earlier output scratch directory. Existing protected generated artifacts remain unchanged. No GitHub push, merge or deployment occurred. The repository script guard and diff whitespace validation passed at delivery recheck; the script guard is not a substitute for manual English copy review. Exact reconciliation against the frozen audit passed for all 53 candidate identities.
