# Coverage Integrity — Phase A Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make existing coverage reporting and unresolved-candidate decisions truthful without changing canonical corpus records or public document URLs.

**Architecture:** Retain the existing aggregate coverage interface and atomic Python-to-SQLite/JSON pipeline. Replace the blanket completion claim, add an optional private candidate-decision history, reopen the explicitly identified unresolved candidates, and present all existing source states in the current English atlas. Full historical schema migration, source-matrix generation and new document imports belong to later plans.

**Tech Stack:** Python >=3.11, jsonschema >=4.23,<5, pytest >=8,<9; Astro 5.17.1, TypeScript 5.9.3, Node 24 and pnpm 10 in CI, Playwright 1.55.0. No new runtime dependency.

**Spec:** [Historical Scope and Evidence-Based Coverage Design](../specs/2026-09-05-historical-scope-and-coverage-design.md), primarily sections 7, 8.2 and 10 package 1. See the [delivery roadmap](./2026-09-05-historical-corpus-delivery-roadmap.md) for requirements assigned to B and C.

## Global Constraints

- “Keep one canonical dataset, one generated SQLite database and one public JSON export.”
- “Keep the six English pages: Home, Policy Map, Timeline, Corpus, Methodology and About.”
- “Preserve existing document IDs, slugs and URLs.”
- “Do not add LLM experiments, interpretation coding, a backend, accounts, a second-language public site or a new hosting service.”
- “The current dataset's cutoff remains 4 September 2026 until a separate audit supports a change.”
- “Do not rerun the old automatic classification migration over reviewed records.”
- “Keep pending candidate content out of the public corpus but report aggregate pending counts and coverage limitations.”
- “A cutoff date alone must never generate a comprehensive or completed-audit claim.”
- All additions, copy, comments, commits and research notes are English. Use actual review timestamps and honest reviewer attribution; do not attribute automated review to Yichen Hao as if he personally inspected every source.
- No change to `data/`, canonical record schema/vocabularies, SQL tables, public document identities or the four research concepts in Phase A. Candidate history is private research metadata, not a canonical entity or public field.

## Execution environment and baseline

All paths below are repository-relative. Inspect applicable AGENTS instructions and use the worktree skill at execution time. The inspected local checkout has alternate Git metadata at `work/sdd-gitmeta`; its original `.git` is stale. In this checkout use `git --git-dir=work/sdd-gitmeta --work-tree=.` for every Git operation, including task commits. In a normal isolated worktree use its real Git metadata instead. Do not change system ACLs or construct another metadata directory to evade a denied write; request the precise permission if needed.

The planning baseline is local commit `627b997`; specification-approval and planning commits may follow, but Phase A expects the same canonical data. Capture actual before-values at execution: 117 published documents, 33 principal, 84 other records, 157 candidates, 117 included, 18 merged, 22 excluded and 0 pending, with 30 source entrances in 13 registered families. Stop and reconcile the plan if these changed independently; do not overwrite new research.

The generated JSON and SQLite files are tracked even though generation patterns also appear in `.gitignore`. Update tracked generated files only via the pipeline, not manual edits. Use a fixed build timestamp for deterministic comparisons; it is not a source verification timestamp.

Known host limitation: prior local Astro/esbuild runs encountered ancestor-directory EACCES. Record the actual environment result if it recurs. Do not label a skipped web build successful or change directory permissions indiscriminately. An authorised isolated environment or CI may perform web validation; no push/merge is authorised by this plan alone.

## File responsibility map

| File | Responsibility / ownership |
| --- | --- |
| `src/observatory/coverage.py` | Existing aggregate interface and safe default statement; Task 1 |
| `src/observatory/candidate_history.py` (new) | Pure, non-writing reopen operation preserving prior decision facts; Task 2 |
| `schema/corpus-inventory.schema.json` | Optional private history snapshots; Task 2 |
| `research/corpus-inventory.json`, `research/source-sweep.json` | Reviewed corrections to the named decisions and affected source states; Task 3 |
| `research/audits/2026-09-05-coverage-reopening.md` (new) | Evidence ledger for this decision review; Task 3; state actual execution date inside |
| `web/src/pages/methodology.astro`, `index.astro`, `about.astro` | Accurate current-versus-planned scope and aggregate state presentation; Task 4 |
| `README.md`, `docs/data-dictionary.md` | Matching contributor-facing semantics; Task 4 |
| `scripts/check_public_build.py` | Regression guard against the withdrawn public claim; Task 5 |
| `generated/public-data.json`, `generated/eu-ai-policy-observatory.sqlite` | Pipeline-produced tracked artefacts; Tasks 1, 3 and final verification |
| `tests/test_coverage.py`, `test_pipeline.py`, `test_export_public.py`, `test_public_build.py`, `test_research_inventory.py`, new `test_candidate_history.py` | Python regression and publication/privacy checks |
| `web/tests/corpus.source.test.mjs`, `web/tests/site.spec.ts` | Updated source and rendered coverage assertions |

Do not refactor the large general validator or add a coverage-matrix subsystem in this phase. The existing schema-validation call already validates the new optional history structure.

## Task 1: Replace the unconditional completion claim

**Files:** Modify `src/observatory/coverage.py`, `tests/test_coverage.py`, `tests/test_pipeline.py`, `tests/test_export_public.py`; regenerate the two tracked generated outputs.

**Interfaces:** Keep `build_public_coverage_summary(research_root: Path) -> dict[str, object]` and every returned key. Add `PUBLIC_COVERAGE_STATEMENT: str`; downstream tasks may import this constant. Do not add a completed-audit boolean without the later evidence model.

- [ ] **Step 1: Add failing tests covering every state, including apparently closed inputs.** Add `pytest` to `tests/test_coverage.py` imports and this test. Existing `_source` and `_candidate` helpers in that file supply its records.

```python
@pytest.mark.parametrize("status", [
    "not_started", "in_progress", "reviewed", "gap_found", "recheck_due",
])
@pytest.mark.parametrize("decision", ["excluded", "pending"])
def test_cutoff_never_implies_completeness(tmp_path, status, decision):
    sweep = {
        "coverage_cutoff": "2026-09-04",
        "sources": [_source("bounded-search", "One family", status)],
    }
    inventory = {"candidates": [_candidate("private-candidate", decision)]}
    (tmp_path / "source-sweep.json").write_text(json.dumps(sweep), encoding="utf-8")
    (tmp_path / "corpus-inventory.json").write_text(json.dumps(inventory), encoding="utf-8")
    result = build_public_coverage_summary(tmp_path)
    assert result["coverage_statement"] == (
        "An expanding corpus of official EU and European Communities AI-related "
        "documents. Verification dates and known coverage gaps are documented."
    )
    assert result["coverage_cutoff"] == "2026-09-04"
    assert result["unresolved_candidates"] == int(decision == "pending")
    assert "private-candidate" not in json.dumps(result)
```

- [ ] **Step 2: Run the red check.** `python -m pytest tests/test_coverage.py -q` must fail on the old comprehensive statement, not an import/environment error.
- [ ] **Step 3: Make the minimal implementation.** Define the following constant and replace only the `coverage_statement` return value with the constant. Keep all current counting and family-priority logic. Remove `human_cutoff`; retain validation of the cutoff with `date.fromisoformat(cutoff_text)` or the upstream validated contract, without synthesising any review date.

```python
PUBLIC_COVERAGE_STATEMENT = (
    "An expanding corpus of official EU and European Communities AI-related "
    "documents. Verification dates and known coverage gaps are documented."
)
# In build_public_coverage_summary's existing return mapping:
# "coverage_statement": PUBLIC_COVERAGE_STATEMENT,
```

Update the existing exact expected sentence in `tests/test_coverage.py`, `tests/test_pipeline.py` and the `AUDIT_SUMMARY` fixture in `tests/test_export_public.py`. Keep their structural/counter assertions; do not delete them to make a wording change pass.

- [ ] **Step 4: Verify and generate.** Run `python -m pytest tests/test_coverage.py tests/test_pipeline.py tests/test_export_public.py -q`, then `observatory-build --project-root . --timestamp 1970-01-01T00:00:00Z`. Expected: targeted tests pass; generated coverage has the new sentence and the old cutoff; canonical arrays and counts are unchanged. Some contributor-copy tests remain scheduled for Task 4; do not claim full-suite success yet.
- [ ] **Step 5: Review and commit the named files.** Use `git diff --check`, inspect generated JSON, then `git add` only the four named source/test files and `git add -u -- generated`. Commit message: `fix: stop inferring corpus completeness from a cutoff`.

## Task 2: Preserve old decisions when reopening candidates

**Files:** Create `src/observatory/candidate_history.py` and `tests/test_candidate_history.py`; modify `schema/corpus-inventory.schema.json` and `tests/test_research_inventory.py`.

**Interfaces:** Produce `reopen_candidate(candidate: Mapping[str, object], *, reason: str, reviewed_at: str, reviewed_by: str) -> dict[str, object]`. It returns a copy, supports only `excluded -> pending`, and never writes files. History snapshots use exactly `decision`, `decision_reason`, `document_id`, `merged_into_document_id`, `reviewed_at`, `reviewed_by`. New current-review fields contain actual review values.

- [ ] **Step 1: Add the failing pure-function test.** This fixture is intentionally minimal for the function; schema tests below use the existing full inventory fixture.

```python
from copy import deepcopy
import pytest
from observatory.candidate_history import reopen_candidate

def test_reopen_preserves_prior_decision_without_mutation():
    candidate = {
        "id": "audit-example", "decision": "excluded",
        "decision_reason": "The English file was not verified.",
        "document_id": None, "merged_into_document_id": None,
        "reviewed_at": "2026-09-04T00:00:00Z", "reviewed_by": "Prior reviewer",
    }
    original = deepcopy(candidate)
    result = reopen_candidate(
        candidate, reason="Official publication identity needs further verification.",
        reviewed_at="2026-09-05T12:00:00Z", reviewed_by="Test reviewer",
    )
    assert candidate == original
    assert result["decision"] == "pending"
    assert result["id"] == candidate["id"]
    assert result["decision_history"] == [{
        key: original[key] for key in (
            "decision", "decision_reason", "document_id",
            "merged_into_document_id", "reviewed_at", "reviewed_by",
        )
    }]
    with pytest.raises(ValueError):
        reopen_candidate(result, reason="Again", reviewed_at="2026-09-05T13:00:00Z",
                         reviewed_by="Test reviewer")
```

- [ ] **Step 2: Run the red check.** `python -m pytest tests/test_candidate_history.py -q` should fail because the module does not exist.
- [ ] **Step 3: Add the pure implementation.** This is the whole new module; it makes no classification or inclusion decision on its own.

```python
from collections.abc import Mapping
from copy import deepcopy
from datetime import datetime

SNAPSHOT_FIELDS = (
    "decision", "decision_reason", "document_id",
    "merged_into_document_id", "reviewed_at", "reviewed_by",
)

def reopen_candidate(candidate: Mapping[str, object], *, reason: str,
                     reviewed_at: str, reviewed_by: str) -> dict[str, object]:
    if candidate.get("decision") != "excluded":
        raise ValueError("Only excluded candidates can be reopened by this operation.")
    if not reason.strip() or not reviewed_by.strip():
        raise ValueError("A reason and an accurately named reviewer are required.")
    current_time = datetime.fromisoformat(reviewed_at.replace("Z", "+00:00"))
    if current_time.tzinfo is None:
        raise ValueError("A timezone-aware review timestamp is required.")
    previous_time = candidate.get("reviewed_at")
    if isinstance(previous_time, str):
        previous = datetime.fromisoformat(previous_time.replace("Z", "+00:00"))
        if previous.tzinfo is None or current_time < previous:
            raise ValueError("Review history cannot be backdated.")
    result = deepcopy(dict(candidate))
    history = result.get("decision_history", [])
    if not isinstance(history, list):
        raise ValueError("decision_history must be an array.")
    history.append({key: deepcopy(candidate[key]) for key in SNAPSHOT_FIELDS})
    result.update(decision="pending", decision_reason=reason,
                  document_id=None, merged_into_document_id=None,
                  reviewed_at=reviewed_at, reviewed_by=reviewed_by,
                  decision_history=history)
    return result
```

Add optional `decision_history` to `$defs.candidate.properties` without adding it to legacy required fields. Define its items as follows; existing nullable ID/timestamp/string references are retained. Do not recursively embed the whole candidate.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "decision": {"enum": ["included", "merged", "excluded", "pending"]},
      "decision_reason": {"type": "string", "minLength": 1},
      "document_id": {"$ref": "#/$defs/nullable_id"},
      "merged_into_document_id": {"$ref": "#/$defs/nullable_id"},
      "reviewed_at": {"$ref": "#/$defs/nullable_timestamp"},
      "reviewed_by": {"$ref": "#/$defs/nullable_string"}
    },
    "required": ["decision", "decision_reason", "document_id", "merged_into_document_id", "reviewed_at", "reviewed_by"],
    "additionalProperties": false
  }
}
```

- [ ] **Step 4: Add schema and error-path tests, then run green.** In `tests/test_research_inventory.py`, reuse `_valid_inventory`, `_write_research_files` and `SCHEMA_ROOT`:

```python
def test_decision_history_is_private_validated_audit_metadata(tmp_path):
    inventory = _valid_inventory()
    candidate = inventory["candidates"][0]
    snapshot = {key: candidate[key] for key in (
        "decision", "decision_reason", "document_id",
        "merged_into_document_id", "reviewed_at", "reviewed_by",
    )}
    candidate["decision_history"] = [snapshot]
    root = _write_research_files(tmp_path, inventory=inventory)
    assert validate_research_inventory(root, SCHEMA_ROOT, Path("tests/fixtures/valid/data")) == []
    candidate["decision_history"][0]["reviewed_at"] = "not-a-date"
    (root / "corpus-inventory.json").write_text(json.dumps(inventory), encoding="utf-8")
    issues = validate_research_inventory(root, SCHEMA_ROOT, Path("tests/fixtures/valid/data"))
    assert any("decision_history" in issue.field for issue in issues)
```

Add these error cases to `tests/test_candidate_history.py`; each must raise `ValueError` and leave the input unchanged:

```python
@pytest.mark.parametrize("candidate_patch,argument_patch", [
    ({}, {"reason": " "}),
    ({}, {"reviewed_by": " "}),
    ({}, {"reviewed_at": "2026-09-05T12:00:00"}),
    ({}, {"reviewed_at": "2026-09-03T12:00:00Z"}),
    ({"decision": "included"}, {}),
    ({"decision_history": {}}, {}),
])
def test_invalid_reopening_does_not_mutate_input(candidate_patch, argument_patch):
    candidate = {
        "id": "audit-example", "decision": "excluded",
        "decision_reason": "Prior decision", "document_id": None,
        "merged_into_document_id": None,
        "reviewed_at": "2026-09-04T00:00:00Z", "reviewed_by": "Prior reviewer",
    }
    candidate.update(candidate_patch)
    original = deepcopy(candidate)
    arguments = {
        "reason": "Requires review", "reviewed_at": "2026-09-05T12:00:00Z",
        "reviewed_by": "Test reviewer",
    }
    arguments.update(argument_patch)
    with pytest.raises(ValueError):
        reopen_candidate(candidate, **arguments)
    assert candidate == original
```

Run `python -m pytest tests/test_candidate_history.py tests/test_research_inventory.py -q`. Expected: pass, including legacy no-history inventory validation.

- [ ] **Step 5: Commit only this contract.** Commit message: `feat: retain private history when reopening corpus candidates`. No actual candidate decision is changed by this task.

## Task 3: Reopen the named unresolved review set

**Files:** Modify `research/corpus-inventory.json`, affected entries only in `research/source-sweep.json`, `tests/test_research_inventory.py`, `tests/test_pipeline.py`; create `research/audits/2026-09-05-coverage-reopening.md`; regenerate tracked generated outputs.

**Interfaces:** Consume `reopen_candidate` from Task 2. Keep candidate IDs and `source_ids` stable; a pending candidate has both canonical target fields null. No canonical record is created, removed or reclassified.

The review set is:

```python
REOPEN_IDS = {
    "ai-board-harmonised-standards-report-2026",
    "ai-board-article-40-standardisation-report-2026",
    "ai-board-international-standardisation-report-2026",
    "ep-ai-act-committee-amendments-pe-732802",
    "ep-ai-act-committee-amendments-pe-732836",
    "ep-ai-act-committee-amendments-pe-732837",
    "ep-ai-act-committee-amendments-pe-732838",
    "ep-ai-act-committee-amendments-pe-732839",
    "ep-ai-act-committee-amendments-pe-732840",
    "ep-ai-act-committee-amendments-pe-732841",
    "ep-ai-act-committee-amendments-pe-732843",
    "ep-ai-act-committee-amendments-pe-732844",
}
```

- [ ] **Step 1: Add an explicit regression for the inspected baseline.** Put `REOPEN_IDS` above the test in `tests/test_research_inventory.py`.

```python
def test_known_unresolved_exclusions_are_reopened_with_history():
    inventory = json.loads(Path("research/corpus-inventory.json").read_text(encoding="utf-8"))
    candidates = {row["id"]: row for row in inventory["candidates"]}
    for identifier in REOPEN_IDS:
        row = candidates[identifier]
        assert row["decision"] == "pending"
        assert row["document_id"] is None and row["merged_into_document_id"] is None
        assert row["decision_history"][-1]["decision"] == "excluded"
        assert row["decision_history"][-1]["decision_reason"] != row["decision_reason"]
    sweep = json.loads(Path("research/source-sweep.json").read_text(encoding="utf-8"))
    affected = {sid for identifier in REOPEN_IDS for sid in candidates[identifier]["source_ids"]}
    assert all(row["scan_status"] == "recheck_due"
               for row in sweep["sources"] if row["id"] in affected)
```

- [ ] **Step 2: Run red, then verify the decisions still match the audited reasons.** Run `python -m pytest tests/test_research_inventory.py -k known_unresolved -q`; expected failure on excluded status. Read each existing reason. The three reports were not fully verifiable; the nine amendments were excluded under the narrower rule. If any candidate has independently acquired a new evidenced decision, stop and reconcile this bounded test/review set rather than overwrite it.
- [ ] **Step 3: Record the scope review and reopen, not admit.** Use the pure function to preview JSON for these twelve records, then apply the reviewed changes with `apply_patch`. No unattended bulk writer. Use distinct English reasons:

> Official listing identified this report, but its independently citable English version and required metadata still need record-level verification. Reopened under the approved unresolved-evidence rule; not approved for publication.

> The prior discovery-only exclusion predates the broadened inclusion rule. The independently citable amendment file, version identity and metadata require review. Reopened for that review; not approved for publication.

Use the actual execution timestamp and `Codex (scope-review reopening)` when this action is automated. Preserve the prior recorded reviewer and timestamp only inside the history snapshot. A later individual source verification may resolve the candidate in Phase C; reopening does not assert it will be included.

For the union of their existing discovery source IDs, set `scan_status` to `recheck_due`, record the actual status-review timestamp and reviewer, and explain the unresolved document/changed-boundary reason in `verification_note`. Preserve prior query intervals and cutoff; `covered_through` is the previously recorded bounded search interval, not a new completed review. The note must say that the earlier result needs rechecking. Do not mark unrelated source entrances unreviewed without evidence.

Write the private audit ledger with actual execution date, the twelve IDs, old/new decision rationale, affected source IDs, relevant official entry URLs already stored in those records, and the explicit limitation that this is a scope/status review rather than verification of each English file. Do not claim fresh retrieval if only the stored evidence was reviewed.

- [ ] **Step 4: Repair obsolete test assumptions without weakening integrity.** Rename `test_2025_to_2026_source_sweep_is_closed_and_candidate_decisions_are_auditable` to describe auditable states. Retain its required-candidate presence check; replace the assertions forcing every source reviewed and every candidate decided with vocabulary/reason/link integrity and the explicit reopened-set test above.

At the unchanged baseline, counts become 117 included, 18 merged, 10 excluded and 12 pending. In `tests/test_pipeline.py`, import `Counter` and `build_public_coverage_summary`, and replace the old exact inventory/family mappings in the repository-build test with:

```python
inventory = json.loads(Path("research/corpus-inventory.json").read_text(encoding="utf-8"))
decisions = Counter(row["decision"] for row in inventory["candidates"])
assert payload["coverage"]["inventory"] == {
    key: decisions[key] for key in ("included", "merged", "excluded", "pending")
}
assert sum(decisions.values()) == 157
assert decisions["pending"] == 12
summary = build_public_coverage_summary(Path("research"))
assert payload["coverage"]["source_families"] == summary["source_families"]
```

Retain the independent reopened-ID regression in `tests/test_research_inventory.py`. Do not hardcode all 13 families as reviewed. Also repair `test_pending_inventory_candidate_is_absent_from_public_output`: its isolated project copies the repository inventory, which now already contains pending candidates. Capture `initial_pending = sum(row["decision"] == "pending" for row in inventory["candidates"])` before appending its synthetic candidate, then assert the exported pending count equals `initial_pending + 1`, retaining every synthetic-candidate privacy assertion.

Add this export-privacy check after the existing pipeline payload is loaded:

```python
inventory = json.loads(Path("research/corpus-inventory.json").read_text(encoding="utf-8"))
public_text = json.dumps(payload)
assert "decision_history" not in public_text
public_ids = {record["id"] for record in payload["documents"]}
for candidate in inventory["candidates"]:
    if candidate["decision"] == "pending":
        assert candidate["id"] not in public_ids
        assert candidate["official_title"] not in public_text
        assert candidate["decision_reason"] not in public_text
```

The privacy check does not ban a shared official landing-page URL that is independently justified by an already published record. Run `python -m pytest tests/test_research_inventory.py tests/test_pipeline.py tests/test_coverage.py -q`, then regenerate with the fixed pipeline timestamp. Expected: pass, 117 public documents still present, pending count 12 and cutoff unchanged.

- [ ] **Step 5: Review and commit this audit correction.** `git diff -- data schema/record.schema.json schema/controlled-vocabularies.json schema/database.sql` must be empty. Inspect every changed candidate/source and the generated JSON before committing the named files. Commit message: `fix: reopen unresolved corpus decisions without losing audit history`.

## Task 4: Present honest coverage states and current scope

**Files:** Modify `web/src/pages/methodology.astro`, `index.astro`, `about.astro`, `web/tests/site.spec.ts`, `web/tests/corpus.source.test.mjs`, `README.md`, `docs/data-dictionary.md`, `tests/test_public_build.py`.

**Interfaces:** Continue using `PublicData.coverage: CorpusCoverage` from `web/src/lib/types.ts`. No new TypeScript fields or runtime requests. Existing IDs `methodology-coverage`, `data-coverage-statement` and `data-unresolved-candidates` stay intact.

- [ ] **Step 1: Add a rendered regression for all five states and the cutoff.** In `web/tests/site.spec.ts`, add:

```typescript
test('methodology distinguishes incomplete registered searches from corpus completeness', async ({ page }) => {
  await page.goto('methodology/');
  const section = page.locator('#methodology-coverage');
  await expect(section).toContainText('An expanding corpus');
  await expect(section).not.toContainText('Comprehensive within');
  for (const label of [
    'Publication cutoff', 'Registered source families', 'Reviewed registered families',
    'Not started', 'In progress', 'Known gaps', 'Recheck due',
    'Included candidates', 'Merged candidates', 'Excluded candidates', 'Unresolved candidates',
  ]) {
    const row = section.locator('dt').filter({ hasText: label });
    await expect(row).toHaveCount(1);
    await expect(row.locator('xpath=following-sibling::dd[1]')).toBeVisible();
  }
  await expect(section).toContainText('Unregistered sources and unreviewed periods are not covered by these counts.');
});
```

- [ ] **Step 2: Run the red browser check.** `pnpm --dir web exec playwright test tests/site.spec.ts -g "methodology distinguishes" --project=chromium-desktop`. Expected: missing status rows before implementation. Use the frontend-testing-debugging skill during execution; follow its Browser-plugin-first requirement for interactive inspection. If local build access is blocked, record the environment failure and obtain an authorised test environment; do not call that a red behavioural result.
- [ ] **Step 3: Update the existing definition list, not the page layout.** Use these rows in the existing coverage section:

```astro
<dl>
  <dt>Publication cutoff</dt><dd>{data.coverage.coverage_cutoff}</dd>
  <dt>Registered source families</dt><dd>{data.coverage.source_families.total}</dd>
  <dt>Reviewed registered families</dt><dd>{data.coverage.source_families.by_status.reviewed}</dd>
  <dt>Not started</dt><dd>{data.coverage.source_families.by_status.not_started}</dd>
  <dt>In progress</dt><dd>{data.coverage.source_families.by_status.in_progress}</dd>
  <dt>Known gaps</dt><dd>{data.coverage.source_families.by_status.gap_found}</dd>
  <dt>Recheck due</dt><dd>{data.coverage.source_families.by_status.recheck_due}</dd>
  <dt>Included candidates</dt><dd>{data.coverage.inventory.included}</dd>
  <dt>Merged candidates</dt><dd>{data.coverage.inventory.merged}</dd>
  <dt>Excluded candidates</dt><dd>{data.coverage.inventory.excluded}</dd>
  <dt>Unresolved candidates</dt><dd>{data.coverage.unresolved_candidates}</dd>
</dl>
<p>These are aggregate states of registered, bounded searches, not a complete source matrix. Unregistered sources and unreviewed periods are not covered by these counts.</p>
```

Replace the Current corpus method paragraph with this data-bound wording. Do not advertise historical filters that Phase B has not built:

```astro
<p>
  The current published records are concentrated on the AI Act pathway and related implementation.
  Their document dates span {data.coverage.from_year}–{data.coverage.to_year},
  with a publication cutoff of {data.coverage.coverage_cutoff}.
  The approved research boundary also admits earlier European Communities and EU material,
  but historical backfill and the wider institutional and sectoral sweep remain incomplete.
  Formally published drafts can qualify; all additions still require record-level official-source verification.
</p>
```

Change Inventory decisions so `excluded` means a verified boundary failure and `pending` includes unresolved official availability, identity and metadata. Explain that pending candidates are counted in audit summaries but excluded from public document records, record counts and downloads. This resolves the current sentence incorrectly saying they do not enter any public totals.

Use this Home lede and a matching About scope sentence while retaining generated counts and project authorship:

> The database is the primary research output; this atlas presents its published records. The current collection is concentrated on the AI Act pathway and related implementation, within an expanding research scope that also admits earlier European Communities and EU AI-related documents.

Update README's Current scope and Expansion sequence to separate approved scope from implemented coverage. Replace its blanket comprehensive sentence with `PUBLIC_COVERAGE_STATEMENT`'s exact text; remove the assertion that empty sector/type arrays prove unrestricted review. In README and the data dictionary, explain that an empty legacy scope array does not establish all-sector coverage, document the private optional `decision_history`, and distinguish actual review timestamps from the publication cutoff. Keep existing field/vocabulary documentation and historical design documents intact.

- [ ] **Step 4: Update narrow source tests and run green.** Replace obsolete exact-copy regexes in `web/tests/corpus.source.test.mjs` with assertions for the new labels and data bindings. Replace the exact old comprehensive README assertion in `tests/test_public_build.py` with the new statement and an assertion that pending counts are documented. Retain tests for tags, statuses, English, slugs and publication boundaries.

Run `python -m pytest tests/test_public_build.py -q`, `pnpm --dir web test` and the two-project `pnpm --dir web exec playwright test tests/site.spec.ts -g methodology`. Expected: pass; cutoff and counters match generated data at both widths, with no new navigation routes or filters claimed.

- [ ] **Step 5: Commit after copy and responsive review.** Commit message: `fix: distinguish current corpus coverage from approved research scope`.

## Task 5: Reject stale claims and verify the bounded release

**Files:** Modify `scripts/check_public_build.py` and `tests/test_public_build.py`; regenerate tracked outputs. Existing CI and Pages workflows already run the public scanner; no workflow mutation is required.

**Interfaces:** Preserve `check_public_build(site_root: Path, public_data_path: Path, require_database: bool = False) -> list[str]`. Add detection for the withdrawn fixed comprehensive phrase in both site text and public JSON. This is a regression guard for the known phrase, not a general natural-language truth detector.

- [ ] **Step 1: Add a failing scanner regression.** Use the existing `write_public_data` helper:

```python
@pytest.mark.parametrize("location", ["html", "json"])
@pytest.mark.parametrize("phrase", [
    "Comprehensive within the documented inclusion boundary",
    "COMPREHENSIVE  within   the documented inclusion boundary",
])
def test_public_scanner_rejects_withdrawn_completeness_claim(tmp_path, location, phrase):
    site = tmp_path / "site"
    site.mkdir()
    (site / "index.html").write_text(phrase if location == "html" else "An expanding corpus", encoding="utf-8")
    data_path = tmp_path / "public.json"
    write_public_data(data_path, {"coverage": {"coverage_statement": phrase if location == "json" else "An expanding corpus"}})
    errors = check_public_build(site, data_path)
    assert any("unsupported corpus-completeness claim" in error for error in errors)

def test_public_scanner_accepts_expanding_corpus_statement(tmp_path):
    site = tmp_path / "site"
    site.mkdir()
    (site / "index.html").write_text("An expanding corpus", encoding="utf-8")
    data_path = tmp_path / "public.json"
    write_public_data(data_path, {"coverage": {"coverage_statement": "An expanding corpus"}})
    assert check_public_build(site, data_path) == []
```

- [ ] **Step 2: Run red.** `python -m pytest tests/test_public_build.py -k withdrawn_completeness -q` must fail because the scanner currently accepts the phrase.
- [ ] **Step 3: Extend the existing text scanner.** Add the pattern and yield branch below. In `_scan_public_data`, return both `_publication_errors(payload, "$")` and `_text_errors(public_data_path, text)`, preserving existing parse/read error behaviour.

```python
_UNSUPPORTED_COVERAGE = re.compile(
    r"\bComprehensive\s+within\s+the\s+documented\s+inclusion\s+boundary\b",
    re.IGNORECASE,
)
# Add to _text_errors(path, text):
if _UNSUPPORTED_COVERAGE.search(text):
    yield f"unsupported corpus-completeness claim found in public output: {path}"
# End of _scan_public_data, after successful JSON decoding:
return [*_publication_errors(payload, "$"), *_text_errors(public_data_path, text)]
```

Do not scan archived specification text as if it were public website content. The regression covers mixed case and repeated whitespace alongside the safe expanding-statement case.

- [ ] **Step 4: Run the complete verification sequence.** First use `superpowers:verification-before-completion`. Run each command separately and retain its actual result:

```text
observatory-build --project-root . --timestamp 1970-01-01T00:00:00Z
python -m pytest -q
pnpm --dir web test
pnpm --dir web build
pnpm --dir web test:e2e
python scripts/check_public_build.py --site web/dist --data generated/public-data.json
python scripts/check_repository_english.py --root .
```

In the alternate-metadata checkout, the English guard's internal `git ls-files` must use the real metadata. Set `GIT_DIR` and `GIT_WORK_TREE` only in the environment of that one guard subprocess, not globally for pytest (its tests create independent Git repositories). Use `Path("work/sdd-gitmeta").resolve()` and `Path.cwd()` as those two values. Restore any temporary shell environment afterwards; in a normal worktree no override is necessary.

For the deploy-equivalent artefact, copy the generated database to `web/dist/downloads/eu-ai-policy-observatory.sqlite` as the existing deployment workflow does, then run the public scanner with `--require-database`. This is an artefact-generation operation, not permission to alter canonical JSON or deploy. Regenerate twice with the same fixed timestamp and compare SHA-256 hashes of both generated outputs; expected equality. Inspect the JSON for the preserved cutoff, reopened pending count and absence of history/private candidate content.

Check `git diff -- data schema/record.schema.json schema/controlled-vocabularies.json schema/database.sql` is empty and compare current published document IDs/slugs with the pre-task baseline. Check all existing routes via the established browser suite and inspect Methodology at desktop/mobile widths. A blocked build or unperformed browser check is reported as such, not counted as passing.

- [ ] **Step 5: Commit and hand off, without automatic publication.** Commit the scanner/test/generated changes with message `test: guard against unsupported public completeness claims`. Confirm the final commit contains no canonical-record edits. Summarise tests, the twelve reopenings and the still-unimplemented historical/matrix work. Offer the user the verified preview and proposed publication target; do not merge to `main` merely because CI could deploy it.

## Self-review and completion boundary

Tasks 1 and 5 address specification section 8.2's unsafe blanket claim without inventing a completed-audit evidence model. Tasks 2–3 implement the existing-candidate part of section 7 with preserved history. Task 4 supplies accurate aggregate disclosure and current-versus-approved scope copy from section 9. Full matrix generation, broad source registration, historical fields/filters, provenance migration, relationship repair and new records remain assigned to B/C in the roadmap; this plan does not claim to complete those requirements.

The shared names are `PUBLIC_COVERAGE_STATEMENT`, `build_public_coverage_summary` and `reopen_candidate`; candidate history has one six-field snapshot contract. No task may rename that contract without updating its consumers and tests. All task steps remain unchecked until actually executed.

Phase A is complete only when its scoped implementation and checks have actually passed, with limitations disclosed. At plan-writing time none of these implementation tasks has been executed.
