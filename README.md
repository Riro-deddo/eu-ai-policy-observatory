# EU AI Policy Observatory

The EU AI Policy Observatory is a verified research database of European Union artificial intelligence policy. The database is the primary output; the accompanying website is a read-only research atlas over generated public data. It makes a bounded, inspectable corpus easier to browse, cite and interrogate without replacing the official sources on which individual records rely.

## Version 0.1 release

- [Browse the public research atlas](https://riro-deddo.github.io/eu-ai-policy-observatory/)
- [View the GitHub repository](https://github.com/Riro-deddo/eu-ai-policy-observatory)
- [Download the published SQLite database](https://riro-deddo.github.io/eu-ai-policy-observatory/downloads/eu-ai-policy-observatory.sqlite)

## Purpose

Version 0.1 establishes the policy, document, event, concept, institution, relationship and provenance infrastructure for a research corpus. It distinguishes official metadata and evidence from researcher-authored classifications and analysis. The project is not an official European Union service and does not imply official endorsement.

## Current scope

The current corpus is bounded to the EU AI Act policy process and directly relevant implementation; it is not an archive of all EU digital law. Its generated coverage range, principal-document total, supporting/version/attachment total and latest source-verification date are published on the Home page from `data.coverage`. The four research lenses remain risk, trustworthiness, accountability and compliance.

The corpus is deliberately bounded rather than comprehensive. The canonical repository may contain records in editorial states such as `draft`, `pending_review` or `verified`. Only records whose `publication_status` is `published` enter the generated public JSON, static site and SQLite output. Pending-review records are excluded from public totals. Those generated outputs, rather than repository visibility alone, define the reviewed public corpus.

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

[`research/source-sweep.json`](research/source-sweep.json) records each bounded official entrance, its scope, check time and `pending`, `in_progress` or `complete` scan status. [`research/corpus-inventory.json`](research/corpus-inventory.json) gives every discovered candidate a reasoned decision:

- `included` points to a canonical document record;
- `merged` identifies another manifestation represented by an existing canonical document;
- `excluded` records why a candidate is outside the corpus or lacks the required evidence; and
- `pending` retains an unresolved candidate for later verification without publishing it.

An independently citable annex is represented as an `attachment` with an `annex_to` relationship. A second file format or duplicate manifestation is merged rather than counted as another document. Inventory and sweep files are validated offline before generated outputs are replaced.

## Verification and provenance

Published records retain official source links plus retrieval and verification information, so readers can trace displayed claims to their stated evidence. Verified or published documents require at least one existing source record; events require an existing source; and relationships require an evidence source. Official relationships must be supported by an official HTTPS source. Verification supports transparent, reviewable research records; it does not claim that the corpus is complete, exhaustive or legally authoritative.

Official metadata, provenance links and evidenced official relationships are kept distinct from researcher analysis. Researcher-authored concepts, corpus assessments and analytical relationships are clearly identified as such. Where an official record changes, earlier retrieved snapshots may be retained only when they reflect actually retrieved bytes and a real SHA-256 hash.

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
```

Use the same fixed UTC timestamp when comparing deterministic builds. `generated/`, `web/dist/` and the copied downloadable database are ignored build outputs, not editing surfaces; change canonical JSON, schema, source code or documentation instead.

The full Python suite validates the canonical records, the source sweep, inventory decisions, cross-record references, composite identities and output pipeline. `observatory-build` repeats validation before atomically replacing the generated public JSON and SQLite database. The public scanner then checks the static distribution and, with `--require-database`, the downloadable database and its published-only boundary.

Browser end-to-end tests are available with `pnpm --dir web test:e2e`. They require the Playwright browser runtime and may be unavailable in restricted local Windows sandboxes; the validation workflow runs them in CI.

## Repository status versus public corpus

The repository is an editorial workspace as well as a public research record. Canonical JSON can therefore include unpublished editorial states. The static atlas, `generated/public-data.json` and generated SQLite database include only `publication_status: published` records and their published dependencies. A scanner checks public build output for unpublished payloads, local paths and common credential markers before publication.

## Limitations

The Observatory is a selected corpus rather than a complete archive of EU AI policy. It provides neither legal advice nor a server-side API, accounts, comments, analytics or tracking. It does not reproduce full policy texts or implement LLM experiments. No licence is included in Version 0.1; public visibility does not itself grant reuse rights.

## Author

Created and maintained by Yichen Hao
