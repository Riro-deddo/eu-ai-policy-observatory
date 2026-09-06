# EU AI Policy Observatory

The EU AI Policy Observatory is a verified research database of European Union artificial intelligence policy. The database serves as research infrastructure; the accompanying website is a read-only research atlas over generated public data. It makes a bounded, inspectable corpus easier to browse, cite and interrogate without replacing the official sources on which individual records rely.

## Version 0.2 research snapshot

For a fixed research citation and downloadable snapshot, use [dataset release v0.2.0](https://github.com/Riro-deddo/eu-ai-policy-observatory/releases/tag/v0.2.0), [citation metadata](CITATION.cff) and the [release boundaries and limitations](docs/releases/v0.2.0.md). Version0.1.0 remains unchanged. The website remains a changing view of the database.

- [Browse the public research atlas](https://riro-deddo.github.io/eu-ai-policy-observatory/)
- [View the GitHub repository](https://github.com/Riro-deddo/eu-ai-policy-observatory)
- [Download the published SQLite database](https://riro-deddo.github.io/eu-ai-policy-observatory/downloads/eu-ai-policy-observatory.sqlite)

## Purpose

Version 0.1 establishes the policy, document, event, concept, institution, relationship and provenance infrastructure for a research corpus. It distinguishes official metadata and evidence from researcher-authored classifications and analysis. The project is not an official European Union service and does not imply official endorsement.

## Current scope

The [6 September academic coverage review](research/audits/2026-09-06-academic-coverage-review.md) adds five evidence-backed documents, corrects the Horizon 2020 status and six OJ citations, and records further discoveries without claiming full coverage. The fixed v0.1.0 release remains unchanged.

The approved research boundary admits official European Communities and EU documents substantively concerning artificial intelligence, including formally published drafts and sector-specific materials as well as adopted instruments. Formal official publication, not adoption or entry into force, is the eligibility threshold. The four research lenses remain risk, trustworthiness, accountability and compliance.

An expanding corpus of official EU and European Communities AI-related documents. Verification dates and known coverage gaps are documented.

Implemented coverage is currently concentrated on the AI Act pathway and related implementation. The published records span 1982–2026, with a publication cutoff of 4 September 2026; historical backfill and the wider institutional and sectoral sweep remain incomplete. The cutoff records the last date admitted by the audit revision. It is distinct from the actual retrieval, verification and decision-review timestamps recorded when research actions occur.

Stage 1 establishes the schema and interface over the existing reviewed corpus, controlled classifications, source registry and candidate inventory. It is not the completed EU-wide source sweep. The canonical repository may contain records in editorial states such as `draft`, `pending_review` or `verified`; only records whose `publication_status` is `published` enter the generated public JSON, static site and SQLite output. Pending candidates are included in aggregate audit summaries but excluded from public document records, published record counts and downloads.

The implemented method constructs, verifies and publishes the corpus. It does not yet run LLM experiments; comparison of large-language-model interpretations will use a separately documented future protocol.

## Explore the database

The read-only atlas has six pages:

- **Home** introduces the project argument, four research lenses and the core policy pathway.
- **Policy Map** presents policy families and documented relationships, including a text alternative.
- **Timeline** places published documents and policy events within the generated coverage range.
- **Corpus** provides local search, sorting and filters for published documents, with stable document pages.
- **Methodology** explains inclusion, publication, provenance and the distinction between official evidence and research analysis.
- **About** summarises the project’s scope, limitations and authorship.

The build also produces the downloadable SQLite research artefact [`eu-ai-policy-observatory.sqlite`](https://riro-deddo.github.io/eu-ai-policy-observatory/downloads/eu-ai-policy-observatory.sqlite). The generated Pages artefact places the file at `downloads/eu-ai-policy-observatory.sqlite`.

## Data model

Canonical data are UTF-8 JSON records, with one record per file. JSON Schema, controlled vocabularies and cross-record checks validate policies, documents, events, concepts, institutions, relationships and sources before the deterministic build generates public JSON and SQLite outputs.

Documents retain official fields such as title, date, identifiers, institutional roles and source links. Version-aware records add `record_level`, `official_reference`, `procedure_references`, `oj_reference`, `document_date`, `version_label` and `version_status`. A composite identity check rejects two records that share a non-null official reference, language, normalised version label and the same sorted issuing-institution IDs; CELEX, ELI and slug uniqueness checks remain independent.

The `record_level` vocabulary distinguishes `principal`, `supporting`, `version` and `attachment` records. Expanded document, relationship, version and source vocabularies are specified in [`schema/controlled-vocabularies.json`](schema/controlled-vocabularies.json) and documented in the [data dictionary](docs/data-dictionary.md). Corpus assessments contain researcher-authored inclusion rationale, policy-stage classification and review information. Relationships are labelled as either official or analytical; analytical relationships have an explicit rationale and evidence source.

## Source sweep and inventory

[`research/source-sweep.json`](research/source-sweep.json) records each bounded official entrance, its source family, covered interval, discovery method, cutoff and one of five review states: `not_started`, `in_progress`, `reviewed`, `gap_found` or `recheck_due`. In legacy entries, an empty document-type or sector coverage array records no explicit restriction in that dimension; it does not establish that all document types or sectors were reviewed. [`research/corpus-inventory.json`](research/corpus-inventory.json) gives every discovered candidate a reasoned decision:

- `included` points to a canonical document record;
- `merged` identifies another manifestation represented by an existing canonical document;
- `excluded` records a verified failure of the research boundary; and
- `pending` retains unresolved official availability, identity or metadata for later verification without publishing it.

An optional private `decision_history` array preserves the prior `decision`, `decision_reason`, document links, `reviewed_at` and `reviewed_by` values when a candidate decision is reopened. This research metadata remains in the inventory and is never added to public data. An independently citable annex is represented as an `attachment` with an `annex_to` relationship. A second file format or duplicate manifestation is merged rather than counted as another document. Inventory and sweep files are validated offline before generated outputs are replaced. Public data expose aggregate status and decision counts only; pending candidate titles, URLs, reasons and decision history remain out of the public payload.

## Expansion sequence

The approved research scope is broader than the coverage currently implemented. Expansion is deliberately staged:

1. **Stage 1 — schema and interface:** establish controlled sector and provenance classifications, the auditable coverage contract, deterministic exports and the English browsing interface over the existing AI Act-centred corpus.
2. **Stage 2 — priority backfill:** extend implemented coverage to the highest-value historical, institutional and sector gaps identified by the audit without weakening the publication boundary.
3. **Stage 3 — wider source sweep:** execute and document bounded searches across registered official source families, add needed entrances, review each discovered candidate and publish only verified eligible records.

Stage completion is evidence-based. A registered source count is not proof that every eligible record has been found.

## Research use and annotation limits

The corpus currently represents English-language manifestations, not a completed search across all EU languages. This acquisition boundary is distinct from the English interface. Counts of records, principal works, versions and attachments are not interchangeable with counts of unique laws or independent analytical observations.

Unassigned concept or policy links are not evidence of substantive absence. The current records do not distinguish all reasons for an empty annotation list, and concept labels are browsing lenses rather than a completed passage-level coding study. Sector tags are positive, researcher-assigned classifications; a cross-sector tag does not automatically match every sector filter. The Policy Map contains recorded relationship endpoints only, not every document. See [Methodology](https://riro-deddo.github.io/eu-ai-policy-observatory/methodology/#annotation-coverage) for generated annotation-coverage counts and the separate published-record and unpublished-candidate review queues.

Public review credit identifies Yichen Hao as the project reviewer. The displayed evidence-review date comes from the recorded evidence assessment, whose actor is preserved in canonical and downloadable data; it is not a separately recorded human sign-off date. A personal review or release approval must be recorded with its actual scope and date before being claimed as such. Historical actors and timestamps are not replaced by display credit.

For an independently reproducible search, retain the actual query or navigation steps, language/date/type filters, result list, pagination or stopping rule, access limitations and candidate decisions. Some legacy search narratives do not retain this detail and must not be described as fully reproducible. Missing past search evidence must not be invented. Before using concepts or relationships as research variables, define a separate coding protocol and analytical sample.

## Verification and provenance

Published records retain official source links plus retrieval and verification information, so readers can trace displayed claims to their stated evidence. Verified or published documents require at least one existing source record; events require an existing source; and relationships require an evidence source. Official relationships must be supported by an official HTTPS source. Verification supports transparent, reviewable research records; it does not claim that the corpus is complete, exhaustive or legally authoritative.

The original first edition of Scientific Opinion No. 15 additionally uses two clearly identified academy-preserved PDFs under a [bounded supplementary-source approval](docs/data-dictionary.md#approved-opinion-15-preserved-original-supplement), with independent official release evidence. These archive hosts are not classified as EU official sources; the corrected edition remains a separate version record.

Official metadata, provenance links and evidenced official relationships are kept distinct from researcher analysis. Researcher-authored concepts, corpus assessments and analytical relationships are clearly identified as such. Where an official record changes, earlier retrieved snapshots may be retained only when they reflect actually retrieved bytes and a real SHA-256 hash.

### Policy Map

The Policy Map opens on principal documents in the AI Act legislative-process grouping. Choose another research-defined policy grouping, expand to all linked records, or search by title or year. Selecting a document opens its evidence-bearing relationships; **Focus connections** shows every recorded immediate relationship across group boundaries, and **Back to group** restores the selected group. The citation-friendly relationship list remains complete and readable when JavaScript is unavailable.

Group membership is an analytical classification, not a legal relationship. Expanded views mark directly linked records from outside the selected group as context. Dates guide the layout but do not form a proportional timeline, and the map neither infers shortcut edges nor claims that an isolated node has no relationships elsewhere in the corpus.

Graph geometry is generated at build time with pinned [ELK.js 0.12.0](https://github.com/kieler/elkjs), licensed under [EPL-2.0](https://www.eclipse.org/legal/epl-2.0/). ELK is not shipped to or executed in the browser; the client loads the precomputed, base-relative `policy-map/atlas.json` route.

## Local development

Use Python 3.11 or later, Node.js and pnpm. Install the Python test dependencies and web dependencies once per checkout.

PowerShell:

```powershell
python -m pip install -e ".[test]"
pnpm --dir web install --frozen-lockfile
python -m pytest -q
observatory-build --project-root . --timestamp 1970-01-01T00:00:00Z
pnpm --dir web test
pnpm --dir web build
New-Item -ItemType Directory -Force web/dist/downloads
Copy-Item generated/eu-ai-policy-observatory.sqlite web/dist/downloads/eu-ai-policy-observatory.sqlite
python scripts/check_public_build.py --site web/dist --data generated/public-data.json --require-database
python scripts/check_repository_english.py --root .
```

Portable shell:

```sh
python -m pip install -e '.[test]'
pnpm --dir web install --frozen-lockfile
python -m pytest -q
observatory-build --project-root . --timestamp 1970-01-01T00:00:00Z
pnpm --dir web test
pnpm --dir web build
mkdir -p web/dist/downloads
cp generated/eu-ai-policy-observatory.sqlite web/dist/downloads/eu-ai-policy-observatory.sqlite
python scripts/check_public_build.py --site web/dist --data generated/public-data.json --require-database
python scripts/check_repository_english.py --root .
```

Use the same fixed UTC timestamp when comparing deterministic builds. Generated release files are derived artefacts, while `web/dist/` and the copied downloadable database are disposable build outputs; change canonical JSON, research audit data, schema, source code or documentation instead of editing generated files. The automated repository guard rejects letters from non-Latin scripts in tracked text and path names, including escaped JSON strings. It allows Latin-script diacritics but cannot determine whether Latin-script prose is semantically English, so copy still requires human review.

The full Python suite validates the canonical records, the source sweep, inventory decisions, cross-record references, composite identities and output pipeline. `observatory-build` repeats validation before atomically replacing the generated public JSON and SQLite database. The public scanner then checks the static distribution and, with `--require-database`, the downloadable database and its published-only boundary.

Browser end-to-end tests are available with `pnpm --dir web test:e2e`. They require the Playwright browser runtime and may be unavailable in restricted local Windows sandboxes; the validation workflow runs them in CI.

## Repository status versus public corpus

The repository is an editorial workspace as well as a public research record. Canonical JSON can therefore include unpublished editorial states. The static atlas, `generated/public-data.json` and generated SQLite database include only `publication_status: published` records and their published dependencies. A scanner checks public build output for unpublished payloads, local paths and common credential markers before publication.

## Limitations

The Observatory is a selected corpus rather than a complete archive of EU AI policy. It provides neither legal advice nor a server-side API, accounts, comments, analytics or tracking. It does not reproduce full policy texts or implement LLM experiments. No licence is included in Version 0.1; public visibility does not itself grant reuse rights.

## Author

Created and maintained by Yichen Hao
