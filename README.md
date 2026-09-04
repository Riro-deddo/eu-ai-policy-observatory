# EU AI Policy Observatory

The EU AI Policy Observatory is a verified research database of European Union artificial intelligence policy. The database is the primary output; the accompanying website is a read-only research atlas over generated public data. It makes a bounded, inspectable corpus easier to browse, cite and interrogate without replacing the official sources on which individual records rely.

## Purpose

Version 0.1 establishes the policy, document, event, concept, institution, relationship and provenance infrastructure for a research corpus. It distinguishes official metadata and evidence from researcher-authored classifications and analysis. The project is not an official European Union service and does not imply official endorsement.

## Current scope

Version 0.1 covers the 2018–2024 EU AI policy pathway. Its current seed corpus contains seven reviewed, published documents and uses four research lenses: risk, trustworthiness, accountability and compliance. It does not yet implement LLM experiments; planned comparisons of large-language-model interpretations are future research.

The corpus is deliberately bounded rather than comprehensive. The canonical repository may contain records in editorial states such as `draft`, `pending_review` or `verified`. Only records whose `publication_status` is `published` enter the generated public JSON, static site and SQLite output. Those generated outputs, rather than repository visibility alone, define the reviewed public corpus.

## Explore the database

The read-only atlas has six pages:

- **Home** introduces the project argument, four research lenses and the core policy pathway.
- **Policy Map** presents policy families and documented relationships, including a text alternative.
- **Timeline** places published documents and policy events from 2018 to 2024 in context.
- **Corpus** provides local search, sorting and filters for published documents, with stable document pages.
- **Methodology** explains inclusion, publication, provenance and the distinction between official evidence and research analysis.
- **About** summarises the project’s scope, limitations and authorship.

The build also produces a downloadable SQLite research artefact, `eu-ai-policy-observatory.sqlite`. Its exact GitHub Pages release and download URL are pending the first deployment; the external publication step will record that URL here. The generated Pages artefact places the file at `downloads/eu-ai-policy-observatory.sqlite`.

## Data model

Canonical data are UTF-8 JSON records, with one record per file. JSON Schema, controlled vocabularies and cross-record checks validate policies, documents, events, concepts, institutions, relationships and sources before the deterministic build generates public JSON and SQLite outputs.

Documents retain official fields such as title, date, identifiers, institutional roles and source links. Their separate corpus assessment contains researcher-authored inclusion rationale, policy-stage classification and review information. Relationships are labelled as either official or analytical; analytical relationships have an explicit rationale and evidence source. See the [data dictionary](docs/data-dictionary.md) for the field-level contract.

## Verification and provenance

Published records retain official source links plus retrieval and verification information, so readers can trace displayed claims to their stated evidence. Verification supports transparent, reviewable research records; it does not claim that the corpus is complete, exhaustive or legally authoritative.

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

Browser end-to-end tests are available with `pnpm --dir web test:e2e`. They require the Playwright browser runtime and may be unavailable in restricted local Windows sandboxes; the validation workflow runs them in CI.

## Repository status versus public corpus

The repository is an editorial workspace as well as a public research record. Canonical JSON can therefore include unpublished editorial states. The static atlas, `generated/public-data.json` and generated SQLite database include only `publication_status: published` records and their published dependencies. A scanner checks public build output for unpublished payloads, local paths and common credential markers before publication.

## Limitations

Version 0.1 is a small, selected corpus rather than a complete archive of EU AI policy. It provides neither legal advice nor a server-side API, accounts, comments, analytics or tracking. It does not reproduce full policy texts or implement LLM experiments. No licence is included in Version 0.1; public visibility does not itself grant reuse rights.

## Author

Created and maintained by Yichen Hao
