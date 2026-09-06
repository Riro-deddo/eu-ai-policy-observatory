# 53-candidate admission review — 6 September 2026

## Result

50 candidates have been verified and appended to the canonical database. Three remain pending; none was silently excluded or forced through the evidence gate.

| Measure | Before | After |
| --- | ---: | ---: |
| Canonical documents marked for publication (local) | 131 | 181 |
| Expanded evidence reviews verified | 105 | 155 |
| Existing legacy review holds | 26 | 26 |
| Inventory candidates | 171 | 224 |

New admissions by review group: historical lineage 8; Parliament, rights and borders 15; sectoral bodies 20; Commission, expert-group and research policy 7.

The batch adds 97 evidence-source records, 21 institutional records and 11 evidenced relationships. Medical, employment, migration/border, financial, aviation/transport, defence and other applicable sector tags are recorded with passage-level evidence. Production provenance is separate from sector classification.

## Three pending identities

| Candidate | Verified so far | Remaining requirement |
| --- | --- | --- |
| JURI robotics report A8-0005/2017 | Official procedure and report tabling on 27 January 2017 | Original English report endpoints still return empty responses or access challenges; full text and detailed attribution must be recovered. |
| Chief Scientific Advisors' AI-in-science opinion, corrected edition (2024) | Official corrected PDF, issue 27 March 2024, catalogue release 21 June 2024, credits and recommendations | Independently verify the original first edition (DOI 10.2777/08845) and establish its canonical version relationship. |
| HMA/EMA NDSG workplan 2026–2028, version 2 | Official text, AI relevance and publication on 9 March 2026 | Verify/admit the preceding 2025–2028 workplan and establish the evidenced revision relationship. |

The latter two holds are version-dependency gaps, not findings that the corrected opinion or workplan does not exist. Their predecessor identities are outside the frozen 53-candidate queue. The earlier 26 canonical review holds and 12 unrelated inventory pending candidates were not reclassified.

## Important evidence distinctions

- Publication, issue and adoption dates remain separate. For example, Frontex's report is dated 17 March 2021 and was published on 31 March; the EMA consultation draft issue is 13 July 2023, with separate committee-adoption dates.
- Officially published consultation drafts remain labelled as drafts. Sharing an official reference does not merge EMA's draft and final reflection papers.
- The AI HLEG and other expert bodies are distinguished from Commission hosting; external report authors and commissioning institutions are recorded separately.
- The Digital Europe Regulation note records an unresolved inconsistency within the official source: EUR-Lex metadata gives entry into force on 12 May 2021, while Article 34 says publication day, 11 May. No adjudication is presented as fact.
- Canonical classification arrays were normalized to existing vocabulary order. No schema, application behavior or existing document record was changed.
- The source registry retains bounded, in-progress coverage. This review does not establish a complete census of every EU AI publication.

## Verification and delivery

The canonical schema, cross-record references, historical publication gate and inventory validation pass. The final JSON and SQLite outputs were generated twice with the same timestamp and match byte-for-byte. SQLite integrity and foreign-key checks pass. All 50 admitted identities are exported; all three pending identities are absent.

The Node source/unit suite passes all 65 tests against the expanded export. The independent worker's full Python rerun passes 404 tests with one skip. Root's full rerun passes 402 tests with one skip; two additional tests stop at a PermissionError reading the protected legacy generated/public-data.json, before their assertions. This context-specific failure is not reported as a passing root suite.

Independent review of all nine changed test files found no critical or important issues. Tests now derive current totals from canonical inputs while preserving the original 131-record cohort, routes, review-state partitions and provenance hashes.

Astro build remains blocked by a Windows permission error creating web/.astro/collections, including after a specific write grant. Vitest's configuration bundling is separately blocked by an ancestor-directory access error. Therefore no fresh rendered-site, browser end-to-end or public-build-scanner success is claimed. No GitHub push, merge or deployment was attempted.

Deliverable pair:

- work/gap-admission-20260906/final/public-data.json
- work/gap-admission-20260906/final/eu-ai-policy-observatory.sqlite

Final SHA-256:

- JSON: 6402d4accdb2d5e4296d5fa3e75300f97e85346ac607b90fc141ed98bed358df
- SQLite: 67262ec435e48d532f7568eb6b5a31fecf5c6fa11a9e7be299a30d9d5886cf08

See result.json for all 53 identity-level decisions, and the six evidence bundles for source locators and access limitations. recovered.json supersedes only the earlier pending decisions for FP5 and Frontex. Original discovery handoffs remain unchanged as historical research notes.
