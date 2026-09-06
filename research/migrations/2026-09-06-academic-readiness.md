# Academic readiness: bounded corrections and disclosures

Baseline: `44a35d4238a46ea999bcfc498779f8661a5a16ef`.
Correction timestamp: `2026-09-06T21:03:47Z`.

## Inventory reconciliation

The published record `draft-high-risk-classification-guidelines-consultation-work-2026`
was missing from the included candidate inventory. Its admission was already
recorded in `2026-09-06-six-record-evidence-update.json` at
`2026-09-06T17:05:16Z`. The new inventory entry reconciles that omission; it is
not a new admission. Its discovery and review timestamps describe the
reconciliation, not an invented original search or admission date.

Included candidates increase from 186 to 187. Published documents remain 187:
183 expanded-review verified and four retained pending. The separate unpublished
candidate queue remains 12. A repository-level regression test now requires
every published document to have an included candidate entry.

## ESPRIT I bibliographic correction

For `council-decision-84-130-eec-esprit`, `oj_reference` changes from null to
`OJ L 67, 9.3.1984, pp. 54–59`, as recorded in the
[official EUR-Lex record](https://eur-lex.europa.eu/eli/dec/1984/130/oj/eng).
Only this field and `updated_at` change in the canonical document. The latter
changes from `2026-09-05T11:54:18Z` to the correction timestamp above. Evidence
review dates, actors and conclusions are unchanged.

The historical fingerprint helper reconstructs precisely these two earlier
field values before checking the existing historical hash. It first checks the
new values and still protects every other byte. Historical ledgers and their
hashes are not rewritten.

## Research interpretation and attribution

Public documentation now distinguishes missing annotation from evidence of
absence, graph coverage from corpus coverage, English manifestations from a
multilingual search, and the published-record review queue from the candidate
queue. Counts are derived from the published data rather than hardcoded.

The public `Reviewed by` credit remains Yichen Hao. `Evidence review date`
names the existing evidence-action timestamp and is explicitly not a separate
human sign-off date. The methodology explains the distinction between project
review credit and the preserved evidence-review actor. No human sign-off or
search log has been fabricated.

The data dictionary documents existing qualified-null publication dates and
existing legal statuses. Contribution guidance describes the already approved,
bounded institutional-archive exception and requires actual review provenance.

No schema, classification assignment, source capture, review conclusion,
historical admission boundary or licence changes in this correction. Generated
JSON and SQLite artefacts are rebuilt from the corrected canonical inputs.
