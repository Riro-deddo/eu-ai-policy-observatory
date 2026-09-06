# Local admission of three verified records

Reviewed: 2026-09-06T01:28:20Z. Reviewer: AI-assisted evidence review. Fixed corpus cutoff: 4 September 2026. User scope: local admission only.

The canonical corpus now contains three additional records: JURI's 2017 robotics report, NDSG workplan v1.4 (July 2025), and NDSG workplan v2.0 (February 2026). These are two resolved candidates from the former three-candidate remainder plus one newly identified version dependency. The scientific opinion remains pending and absent from canonical published documents. Local structural, reference, inventory and historical-publication gates passed for 184 documents. Independent generated-output checks passed: JSON and SQLite exactly match all 184 canonical document IDs, with 158 verified and 26 unchanged legacy holds. The complete Python suite passed 404 tests with one skip; Node source tests passed 65/65. Vitest was blocked before executing tests by a local directory-access error.

## Admission decisions

- `historical-juri-robotics-report-2017`: report/principal; `A8-0005/2017`, procedure `2015/2103(INL)`, `PE582.443v03-00`. Issue and publication 27 January 2017; publication explicitly means official parliamentary tabling for plenary. The 12 January committee adoption remains a separate date. The official procedure supports `procedural_step_for` the existing 16 February resolution. No resolution CELEX/OJ identifiers were copied; six embedded opinions remain report components.
- `hma-ema-ndsg-workplan-2025-2028-v1-4`: non-binding work programme/version. The cover supplies July 2025 at month precision; the exact 22 July catalogue update supplies a transparent hosted-revision publication fallback. March adoption and May first publication refer to the earlier original workplan lineage and do not date v1.4.
- `hma-ema-ndsg-workplan-2026-2028-v2`: non-binding work programme/version. Cover issue and NDSG adoption remain February 2026 at month precision; exact publication fallback is 9 March 2026. The 11 February minutes record endorsement in principle followed by written adoption, so no final-adoption day is invented. Official catalogue previous-version linkage and v2.0 Introduction p.4 evidence `revises` v1.4.
- Both NDSG records credit Joint HMA/EMA Network Data Steering Group as author, with EMA separately identified as publisher and official host. A necessary NDSG institutional identity is added; the existing BDSG identity is not renamed or repurposed. Health, public-administration and research tags have specific AI-workstream page evidence. v2.0's explicit adoption also supports a separate NDSG adopter role.

## Scientific-opinion follow-up and retained limitations

The [6 September verification memo](../../verification/2026-09-06-remaining-three/science-opinion.md) establishes the corrected official opinion's 102-page full text and distinct DOI `10.2777/46863`. The Commission announcement and mechanism pages corroborate original DOI `10.2777/08845` and the April 2024 initial release, but live links supply corrected content or errors. No original full text or authoritative correction schedule was recovered; substantive change extent remains unknown. This improved evidence does not resolve the version dependency. The live candidate's previous decision fields remain unchanged, and no substitute summary/SAPEA report or fabricated original is admitted.

JURI's unknown first server-upload timestamp is disclosed, with the publication field tied explicitly to official tabling. NDSG v1.0-v1.3 manifestations remain unrecovered and no complete history is asserted. PDF hashes describe the September retrieval snapshots rather than byte-identical historical availability. Sector and provenance tags are editorial classifications, separately evidenced from official metadata.

## Inventory, coverage and preservation

The two formerly pending records have their six prior decision fields appended to `decision_history` before inclusion. New v1.4 has its own candidate and a separate `ndsg-v1-4-dependency-follow-up-20260906` registry row marked `in_progress`. The old frozen 53-candidate scope is not expanded to absorb v1.4. Only bounded follow-up notes/timestamps change on the existing Parliament and EMA admission rows; all existing source statuses and cutoffs remain unchanged. Inventory decisions now total 225: 184 included, 13 pending, 10 excluded, 18 merged.

All 181 pre-existing document records, 26 legacy holds, prior admission bundles and verification memos are preserved. Before editing, full working bytes and SHA-256 values were captured in eleven `work/three-record-admission-20260906/before-*.zlib.base64` files. Each contains base64-encoded zlib-compressed JSON mapping original paths to hashes and base64 file bytes. This is the working-file baseline; the stale Git HEAD is not used. `make_diff.py` verifies those hashes and compares current bytes to produce `task-1-diff.txt`.

## Exact changed-file manifest

- `data/documents/historical-juri-robotics-report-2017.json`
- `data/documents/hma-ema-ndsg-workplan-2025-2028-v1-4.json`
- `data/documents/hma-ema-ndsg-workplan-2026-2028-v2.json`
- `data/institutions/hma-ema-network-data-steering-group.json`
- `data/sources/historical-juri-robotics-report-2017-official-pdf.json`
- `data/sources/ep-oeil-robotics-procedure-2015-2103.json`
- `data/sources/hma-ema-ndsg-workplan-2025-2028-v1-4-official-pdf.json`
- `data/sources/hma-ema-ndsg-workplan-2026-2028-v2-official-pdf.json`
- `data/sources/hma-ema-ndsg-workplan-2026-2028-v2-official-page.json`
- `data/relationships/juri-robotics-report-procedural-step-for-resolution-2017.json`
- `data/relationships/hma-ema-ndsg-v2-revises-v1-4.json`
- `research/corpus-inventory.json`
- `research/source-sweep.json`
- `research/admission/2026-09-06-three-record-admission/result.json`
- `research/admission/2026-09-06-three-record-admission/report.md`

Task-local helper/report artifacts are separate from canonical admission: `snapshot.py`, eleven compressed before-state files, `make_diff.py`, `task-1-diff.txt` and `task-1-report.md` under `work/three-record-admission-20260906`. Root owns its independent verification helper, QA logs and fresh generated outputs.

## Validation

Focused validation passed after correcting three candidate-provenance fields to the existing validator's canonical priority rule. The initial mismatch was a data error, not a code defect; no assertions, schemas or tests were changed. Existing structure/reference validation, inventory validation and historical-publication validation returned no issues.

Independent root verification passed: all 184 canonical IDs exactly equal exported JSON and SQLite document IDs; science is absent; 158 verified/26 legacy partition and all 181 old document bytes preserved. Old admission bundles/memos and unrelated candidates are unchanged; prior decision histories are preserved. SQLite integrity is `ok`, with zero foreign-key violations. Both output pairs generated at `2026-09-06T01:37:03Z` match checksums:

- SQLite: `2027b4394d9afa48f89f4f820d872d7753679ec304b249b44313ce1180d4b680`.
- JSON: `f4b91033943f2a9263544e929ad8cad247ed6d1489c622adc9250ddd87541723`.

Fresh output pair: `work/three-record-admission-20260906/output/eu-ai-policy-observatory.sqlite` and `public-data.json`; repeated pair under `output-repeat`. Node source tests passed 65/65 against the fresh JSON. The final full Python rerun passed 404 tests with one skip and no failures in 53.93 seconds (exit 0). Vitest was blocked before any assertions ran: esbuild reported `Cannot read directory ../../../../../..: Access is denied` and could not resolve/load `vitest.config.ts`. This is an environment-limited check, not a test pass. No frontend code changed in this admission. The full Python attempt exposed one JURI tag-order convention error, now corrected without changing tags or assertions; its targeted rerun passed 1/1, and the final corrected structural/reference/inventory/historical gate passed again. Other subprocess failures arose from tests overriding PYTHONPATH, which hides an existing dependency directory; root used a task-local `PYTHONUSERBASE` with a `.pth` reference to existing `../.euai-pydeps`; the final full rerun passed without installation or runtime-code changes. Root also explicitly confirmed that generated source notes include the final prior-review clarification and equal the current canonical record. Commands, earlier attempt results and the scope of the blocked check are recorded in `work/three-record-admission-20260906/task-1-report.md`.

No installation, runtime/schema/UI change, Git operation, commit, push, merge, remote message or deployment was performed.
