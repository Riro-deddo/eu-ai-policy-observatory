# Contributing

Contributions should preserve the Observatory’s database-first, evidence-led approach. Use British English throughout public data, documentation and interface copy.

## Canonical records

Each canonical record is one UTF-8 JSON object in one file under `data/`. Keep identifiers and document slugs stable, lowercase and hyphenated. Do not reuse an identifier for a different entity; stable identifiers support links, citations and reproducible builds.

`publication_status` is an editorial state, distinct from a document’s legal or policy status:

```text
draft → pending_review → verified → published
```

Only `published` records, with published dependencies, enter the public JSON, static atlas and SQLite artefact. A record may be committed while it remains unpublished, but it must carry its accurate editorial status and must not be presented as part of the reviewed public corpus.

## Sources and review

Use official, evidenced sources for official metadata, dates, identifiers, institutional roles and claims about official relationships. Record the source URL, publisher, actual retrieval time and verification information. A record reaches `verified` only after the required official source, stable identifier or documented verification basis has been reviewed; promotion to `published` is a deliberate approval for public inclusion.

Keep official metadata separate from researcher analysis. Corpus assessments, concepts and policy classifications are analytical and must not be written as though an EU institution supplied them. Every analytical relationship requires a clear English rationale, an official evidence source and an explicit analytical basis. Official relationships also require their supporting official evidence source.

Add a document snapshot only for bytes actually retrieved from an official source, except for the explicitly approved [Opinion 15 institutional-archive supplement](docs/data-dictionary.md#approved-opinion-15-preserved-original-supplement). Its SHA-256 must be calculated from those bytes. Follow the existing evidence-retention policy; do not introduce unrelated full-text copies, fabricate hashes or use snapshots to conflate distinct legal documents.

Every published document must have an `included` candidate decision linking to its canonical ID. An admission discovered to be missing from the inventory is reconciled explicitly at the actual reconciliation time, citing its existing admission evidence; do not invent an earlier discovery or review event. The repository-level admission test enforces this traceability requirement in CI.

Record human review or release approval only when it actually occurs, with its scope and real timestamp. Public reviewer credit must not overwrite the recorded evidence-review actor or be treated as a separately timestamped personal sign-off. Missing search logs and unknown annotation states must remain explicit; do not infer completed searches or negative concept/sector findings from missing values.

## Schema and vocabulary changes

Treat a new field, vocabulary value or changed constraint as a deliberate schema change. Update the relevant JSON Schema, controlled vocabularies, data dictionary and validation tests together, then validate all records. Do not introduce ad hoc values to a record merely to avoid a schema update.

## Local checks

From the repository root, install dependencies and run the database checks:

```powershell
python -m pip install -e ".[test]"
python -m pytest -q
observatory-build --project-root . --timestamp 1970-01-01T00:00:00Z
```

Install, test and build the web interface:

```powershell
pnpm --dir web install --frozen-lockfile
pnpm --dir web test
pnpm --dir web build
pnpm --dir web test:e2e
```

Then add the generated database to the local static artefact and scan it:

```powershell
New-Item -ItemType Directory -Force web/dist/downloads
Copy-Item generated/eu-ai-policy-observatory.sqlite web/dist/downloads/eu-ai-policy-observatory.sqlite
python scripts/check_public_build.py --site web/dist --data generated/public-data.json --require-database
```

Equivalent portable commands use `python`, `pnpm --dir web`, `mkdir -p` and `cp`. Browser tooling depends on Playwright’s installed browser runtime; not every restricted Windows sandbox can run it. CI runs the browser checks on its supported runner.

## What not to commit

Do not commit the research proposal PDF, credentials, tokens, private research material, generated outputs, copied SQLite databases or personal filesystem paths. Generated directories are ignored and must be rebuilt from canonical inputs. Before submitting a change, inspect `git diff --check` and the staged diff for accidental secrets, paths and non-public material.
