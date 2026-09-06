# Retained Section Notices Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans. Steps use checkboxes.

**Goal:** Preserve three existing section routes while making their unresolved whole-work parent relationship explicit in canonical data, SQLite, public JSON and English document pages.
**Architecture:** One optional document-level retained_route_notice object; normalized supporting SQLite tables and a nullable public projection. The active validator enforces this narrowly reviewed exception, while the historical lineage validator still reports the three missing-parent holds. No eighth entity, guessed relationship, new admission or public deployment.
**Tech Stack:** Existing Python/pytest/JSON Schema/SQLite and Astro/TypeScript/Playwright; no dependencies added.
**Spec:** docs/superpowers/specs/2026-09-05-historical-scope-and-coverage-design.md sections 2, 5.2, 9-11; docs/superpowers/plans/2026-09-05-historical-corpus-delivery-roadmap.md Phase B. The user approved the specific three-route notice, short-title clarification, unchanged pending status and database/page round-trip in chat immediately before this plan.
**Base:** dac7c6099962eae415844441f3da12ecc55a8007.

## Global Constraints

- Keep the seven canonical entities: policy, document, event, concept, institution, relationship and source.
- Preserve all 117 published document IDs, slugs and URLs, 95 relationships and the 2026-09-04 publication cutoff. Principal count remains 35.
- Keep official facts distinct from researcher classifications; notice and reviewer are editorial, not EU status or authorship.
- Use only English project content. Keep the current UI design and all six pages.
- Do not add or publish a whole-guidelines parent record, a source, candidate, relationship or final successor.
- Preserve attachment and draft status on the three sections. The three historical_relationship holds must remain; a reviewed notice is not resolved lineage or Phase B completion.
- Only the three named documents may carry this notice in the first reviewed contract. Other records cannot use a notice to evade evidence gates.
- Preserve current source/snapshot metadata, all old review attribution and immutable B2/B3/B4 audit ledgers.
- Do not change the final-guidelines candidate's exclusion in this batch; its stronger-than-evidence reasoning is a separately recorded follow-up.
- Do not overwrite generated/public-data.json or generated/eu-ai-policy-observatory.sqlite. Generate fresh temporary artifacts for validation and preview; no GitHub push, merge, deployment or cleanup.
- EVERY git invocation uses git --git-dir=work/sdd-gitmeta --work-tree=.; retain the existing isolated checkout and branch.
- All edits use apply_patch. All pytest basetemp paths are fresh system Temp directories, never old repository scratch directories.
- Reviewer/updated timestamps are actual UTC review times, not the publication cutoff or copied prior researcher attribution.

## Exact scope and interface

The reviewed IDs and corresponding PDF source IDs are:

| Document ID | PDF source ID | Section |
| --- | --- | --- |
| draft-high-risk-classification-guidelines-2026 | commission-newsroom-128559-pdf | General principles |
| draft-high-risk-classification-guidelines-annex-i-2026 | commission-newsroom-128560-pdf | Article 6(1) and AI Act Annex I |
| draft-high-risk-classification-guidelines-annex-iii-2026 | commission-newsroom-128561-pdf | Article 6(2) and AI Act Annex III |

All three also cite high-risk-guidelines-draft-commission, already a linked official source. Its locator is the publication date, the paragraph immediately before Downloads explaining separate sections, and Downloads 1-3. Each PDF locator is pages 1-2 (cover and first body page), not a claim to have read all pages.

Canonical shape (optional property, non-null object when present):

```typescript
type RetainedRouteNotice = {
  status: 'parent_relationship_under_review';
  reason: string; // nonblank English editorial reason
  reviewed_by: string; // AI-assisted reviewer, not the original Yichen Hao metadata reviewer
  reviewed_at: string; // timezone-aware ISO timestamp
  evidence: Array<{ source_id: string; locator: string }>;
};
// Public DocumentRecord always includes:
retained_route_notice: RetainedRouteNotice | null;
```

Require every object key above, no unknown keys, nonblank reason/reviewer/locators, distinct source IDs and at least the two specified source references (the common landing page plus this section's PDF). Each evidence source must resolve uniquely to a published official HTTPS source, be declared in this document's source_ids, and use the existing official-source predicate. Validate timestamps and created_at <= notice.reviewed_at <= updated_at, without backdating other review fields.

The notice is valid only on the three published attachment/draft records and only while the historical relationship check still identifies their missing-parent condition. If a scoped unresolved published section loses its notice, active validation must fail. If a genuine parent is later admitted and valid lineage recorded, the notice must be explicitly removed; a stale notice is rejected. Do not impose this migration-specific mandatory-notice condition on arbitrary legacy version/attachment fixtures outside these three IDs. Reuse the existing lineage checker instead of inventing a parallel definition, and avoid circular module imports (local function imports are acceptable).

Keep historical_relationships.py unchanged unless a demonstrated integration need exists; the notice never suppresses its issues. The prospective historical schema should inherit the new active property naturally.

Reason template (substitute the exact section above):
"This record contains the {section} section of the draft Commission guidelines. The Observatory has not admitted a separate record for the whole guidelines; the parent relationship remains under review. This existing route is retained for access. The document remains a consultation draft."
For the Annex I/III sections append:
"The annex designation identifies the AI Act annex addressed; it does not make this file an annex to the General principles section."

Change only the General-principles short_title to:
"Draft high-risk classification guidelines — General principles".
Keep its official_title, IDs and slug unchanged. Other canonical changes are the three updated_at values and the new notice objects; no notes append is necessary because the notice has its own attribution.

## Task 1: Complete the reviewed notice vertical slice

**Files:**

- Modify schema/record.schema.json: optional document property and strict local definitions.
- Create src/observatory/retained_routes.py: narrowly scoped review validator using existing evidence and lineage semantics.
- Modify src/observatory/validate.py: invoke the new checks and preserve deterministic structured issues.
- Modify schema/database.sql and src/observatory/build_db.py: supporting tables document_retained_route_notices and document_retained_route_evidence with document/source foreign keys and stable evidence order. No change to seven-entity public top-level collections.
- Modify src/observatory/export_public.py: emit the complete nullable notice with ordered evidence only on exported published documents.
- Modify the three canonical document JSON files above: only declared fields.
- Create research/migrations/2026-09-05-retained-section-notices.json: full before objects, exact top-level after_changes, source/locator evidence, existing counts/holds and review scope. Do not include invented byte retrieval claims.
- Modify web/src/lib/types.ts: export RetainedRouteNotice type and required nullable document property; update existing TypeScript fixtures where needed.
- Modify web/src/pages/corpus/[slug].astro or create a small web/src/components/RetainedRouteNotice.astro component: render only non-null notices in a separate editorial section immediately after the heading; heading text is "Parent relationship under review". Include reason, reviewer/time and labelled source links/locators, resolved through document.sources. Keep it separate from Official metadata. Use existing layout; permit minimal wrapping CSS only if QA shows a need.
- Create tests/test_retained_routes.py for real validation/build/export/data migration behavior.
- Modify tests/test_official_pdf_evidence.py only to reverse the newly declared document corrections in memory before its original B3 assertions. Preserve the real current snapshots and source checks. Do not rewrite historical ledgers or replace the entire current object with a historical one.
- Add web/tests/retained-routes.spec.ts for actual rendered behavior. Update existing fixture constructors/tests only when the new public contract requires it.
- Modify data-dictionary.md and docs/historical-readiness.md to explain the notice, limited scope, unchanged lineage holds and editorial meaning. Qualify obsolete historical counts as their earlier review state, not current counts.

**Interfaces:**

```python
def validate_retained_route_notices(records, data_root: Path) -> list[ValidationIssue]:
    # Called by validate_records after basic shape/reference checks.
    # Must tolerate malformed inputs and return deterministic issues, not throw.
    ...
```

Use issue code retained_route_notice and field paths under retained_route_notice. Schema-shape errors can retain existing code schema. Group published sources by ID for uniqueness checks. A local import of validate_historical_relationships plus _is_official_source can avoid the existing validate/historical circular dependency; do not duplicate the host allowlist.

**Tests and implementation steps:**

- [ ] Add real failing validation and pipeline tests before implementation. First run should fail for unsupported/missing notice or absent export, not broken test setup. Use an existing real-data copy in tmp_path; leave original records unchanged.
- [ ] Cover malformed status, missing/blank reason/reviewer/locator, absent/unpublished/non-official/unlinked/duplicate evidence, wrong PDF, invalid/backdated/review-after-updated timestamps, unsupported ID/level/status, missing mandatory notice and stale notice after genuine evidenced parent linkage.
- [ ] Implement strict schema and active validator. Existing valid fixtures without notices remain valid; original non-object/malformed canonical handling continues to return issues.
- [ ] Implement normalized SQLite insertion and deterministic nullable JSON export. Add three reviewed objects and the one short-title correction with a full before/after migration ledger. Use a fresh actual review timestamp.
- [ ] Preserve historical assertions with a field-by-field in-memory reversal of this ledger, then apply the already existing B4 reversal. For a new field absent in before, assert the current after value and remove only that field in the local copy.
- [ ] Add the typed rendered notice and exact three-route browser regression. No notice appears on ordinary AI Act page. Source anchors point to the canonical official sources, not an invented parent. Browser test checks one H1, distinct editorial section, visible reviewer/time, retained draft status, no horizontal overflow and a usable Return to Corpus link.
- [ ] Run focused and full Python suites, TypeScript/web tests and Astro check/build against fresh generated artifacts. Do not deselect the existing Windows ACL skip.
- [ ] Self-review scope and test evidence; write the task report. The controller will run rendered desktop/mobile QA and independent review before any local commit.

Minimal real-pipeline assertion shape:

```python
outputs = run_pipeline(ROOT, REVIEW_TIME, output_root=tmp_path / "output")
public = json.loads(outputs.public_json.read_text(encoding="utf-8"))
by_id = {row["id"]: row for row in public["documents"]}
assert len(by_id) == 117
assert len(public["relationships"]) == 95
assert {key for key, row in by_id.items() if row["retained_route_notice"] is not None} == HELD_IDS
assert by_id["artificial-intelligence-act"]["retained_route_notice"] is None
assert {Path(i.record_path).stem for i in validate_historical_readiness(
    load_records(ROOT / "data"), ROOT / "schema", "2026-09-04"
) if i.code == "historical_relationship" and i.field == "record_level"} == HELD_IDS
```

Also query the real SQLite notice/evidence rows, verify all fields/order survive, assert the frozen 117 route set, repeat generation with the same timestamp for determinism, and compare every changed canonical object with its ledger before plus declared changes. Invalid notice input must block pipeline publication before replacing prior artifacts.

Browser behavior skeleton:

```typescript
await page.goto('corpus/draft-high-risk-classification-guidelines-2026/');
await expect(page.getByRole('heading', { level: 1 })).toContainText('General principles');
const notice = page.getByRole('region', { name: 'Parent relationship under review' });
await expect(notice).toBeVisible();
await expect(notice).toContainText('AI-assisted reviewer');
await expect(notice.getByRole('link')).toHaveCount(2);
await page.getByRole('link', { name: 'Return to the Corpus' }).click();
await expect(page).toHaveURL(/\/corpus\/$/);
```

Run both existing chromium-desktop and chromium-mobile projects, plus the ordinary AI Act page negative check. The Browser plugin/skill is absent; existing Playwright is the selected QA path. Do not install dependencies. The controller prepares a temporary web copy and fresh generated input if original protected artifacts or subprocess sandboxing block the regular build.

## Verification commands

```powershell
$env:PYTHONPATH = Join-Path (Get-Location).Path 'src'
& '.venv/Scripts/python.exe' -m pytest tests/test_retained_routes.py -q -p no:cacheprovider --basetemp 'C:/Users/ROG/AppData/Local/Temp/eu-ai-b5-focused-20260905' --tb=short
& '.venv/Scripts/python.exe' -m pytest tests -q -rs -p no:cacheprovider --basetemp 'C:/Users/ROG/AppData/Local/Temp/eu-ai-b5-full-20260905' --tb=short
```

Use a fresh suffix on reruns; do not delete old Temp paths. Node is the bundled dependency runtime; web scripts are npm-compatible and run existing node --test, vitest, astro check/build and Playwright. All QA reports/screenshots stay in system Temp, not committed source.

## Preflight and integration

| Pair/task | Producer/consumer agreement |
| --- | --- |
| Task 1 schema -> validator -> SQL -> JSON -> TypeScript -> Astro | Same five notice keys; nullable only in public output; ordered evidence source_id/locator pairs. |
| Task 1 data -> historic ledger tests | Only new notice, updated_at and one short_title; snapshots and older ledgers remain intact. |
| Task 1 notice -> historical readiness | Active notice validates editorial transparency; lineage remains unresolved with exactly three holds. |

The bounded user-approved slice is one independently testable delivery. It does not activate the rest of the historical contract, admit new records or publish a release. Independently review this complete diff, address supported findings, then preserve it as a local exact-allowlist commit.
