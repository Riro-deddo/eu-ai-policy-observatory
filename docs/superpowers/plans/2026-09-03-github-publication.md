# EU AI Policy Observatory GitHub Publication Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Validate, build and publish the English EU AI Policy Observatory repository and its read-only interface on GitHub Pages.

**Architecture:** GitHub Actions runs the same database and website gates used locally. A validation workflow checks every push and pull request. A separate least-privilege Pages workflow rebuilds canonical JSON into SQLite and static HTML, adds the downloadable database to the site artefact and deploys only after all tests pass.

**Tech Stack:** GitHub, GitHub Actions, GitHub Pages, GitHub CLI, Python 3.13 runner, Node.js 24 runner, pnpm 10, Astro static output.

**Action versions verified:** 2026-09-03 against the official release pages for `checkout`, `setup-python`, `setup-node`, `upload-artifact`, `configure-pages`, `upload-pages-artifact`, `deploy-pages` and `pnpm/action-setup`.

**Spec:** `docs/superpowers/specs/2026-09-03-eu-ai-policy-observatory-design.md`

**Dependencies:** Complete `docs/superpowers/plans/2026-09-03-database-foundation.md` and `docs/superpowers/plans/2026-09-03-static-research-atlas-ui.md` first.

## Global Constraints

- The repository and Pages interface are public and English-only.
- Canonical JSON remains the source of truth; generated files are never committed.
- Invalid or unpublished data cannot reach the Pages artefact.
- Actions use standard GitHub-hosted runners and least-privilege permissions.
- The repository contains no API keys, credentials, private research data or full research-proposal PDF.
- Version 0.1 contains no analytics, tracking, custom domain or server-side service.
- No reuse licence is added in Version 0.1.
- Each task ends with its own tests and commit.

---

## File Structure

```text
.github/workflows/validate.yml       Push and pull-request quality gate
.github/workflows/deploy-pages.yml   Tested Pages build and deployment
README.md                            Public project and database introduction
CONTRIBUTING.md                      Record-editing and review procedure
SECURITY.md                          Private vulnerability-reporting guidance
scripts/check_public_build.py        Secret, path and publication-boundary scan
scripts/__init__.py                  Importable scanner package marker
tests/test_public_build.py           Scanner tests
```

### Task 1: Add the Local and GitHub Validation Gate

**Files:**
- Create: `scripts/__init__.py`
- Create: `scripts/check_public_build.py`
- Create: `tests/test_public_build.py`
- Create: `.github/workflows/validate.yml`
- Modify: `web/astro.config.mjs`
- Modify: `web/playwright.config.ts`
- Modify: `web/package.json`

**Interfaces:**
- Consumes: canonical records, generated outputs and `web/dist/` from Plans 1 and 2.
- Produces: `check_public_build(site_root: Path, public_data_path: Path) -> list[str]`.
- Produces: command `python scripts/check_public_build.py --site web/dist --data generated/public-data.json`.
- Produces: required CI job named `validate`.

- [ ] **Step 1: Write failing public-build scanner tests**

Create `tests/test_public_build.py`:

```python
from pathlib import Path

from scripts.check_public_build import check_public_build


def test_scanner_rejects_local_paths_and_non_published_payloads(tmp_path: Path):
    site = tmp_path / "site"
    site.mkdir()
    (site / "index.html").write_text(r"C:\Users\Researcher\secret", encoding="utf-8")
    data = tmp_path / "public-data.json"
    data.write_text('{"documents":[{"publication_status":"draft"}]}', encoding="utf-8")
    errors = check_public_build(site, data)
    assert any("local filesystem path" in error for error in errors)
    assert any("non-published record" in error for error in errors)
```

- [ ] **Step 2: Run the scanner test and confirm failure**

Run `python -m pytest tests/test_public_build.py -q`.

Expected: collection fails because `scripts.check_public_build` does not exist.

- [ ] **Step 3: Implement the public-build scanner**

Scan UTF-8 text files under the site root for Windows user paths, `/Users/`, `/home/`, `localhost`, common token prefixes and private-key headers. Parse the public JSON recursively and report every dictionary whose `publication_status` is not `published`. Return sorted, human-readable errors and make the CLI exit 1 when errors exist.

Do not reject the words `draft` or `pending_review` in Methodology prose; inspect record payload values rather than performing an indiscriminate text search.

- [ ] **Step 4: Run the scanner tests**

Run `python -m pytest tests/test_public_build.py -q`.

Expected: all tests pass.

- [ ] **Step 5: Make Astro deployment coordinates environment-driven**

Set the Astro configuration to:

```javascript
const site = process.env.SITE_ORIGIN ?? 'https://eu-ai-policy-observatory.test';
const base = process.env.BASE_PATH ?? '/eu-ai-policy-observatory';

export default defineConfig({ output: 'static', site, base });
```

Set Playwright `baseURL` to `http://127.0.0.1:4321/eu-ai-policy-observatory/`. Add this script to `web/package.json`:

```json
"check:public": "python ../scripts/check_public_build.py --site dist --data ../generated/public-data.json"
```

- [ ] **Step 6: Create the validation workflow**

Create `.github/workflows/validate.yml` with:

```yaml
name: Validate

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    env:
      SITE_ORIGIN: https://${{ github.repository_owner }}.github.io
      BASE_PATH: /${{ github.event.repository.name }}
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v6
        with:
          python-version: '3.13'
          cache: pip
      - uses: pnpm/action-setup@v6
        with:
          version: 10
      - uses: actions/setup-node@v7
        with:
          node-version: '24'
          cache: pnpm
          cache-dependency-path: web/pnpm-lock.yaml
      - name: Install Python dependencies
        run: python -m pip install -e ".[test]"
      - name: Test and build database
        run: |
          python -m pytest -q
          observatory-build --project-root . --timestamp "1970-01-01T00:00:00Z"
      - name: Install web dependencies
        working-directory: web
        run: pnpm install --frozen-lockfile
      - name: Install Chromium
        working-directory: web
        run: pnpm exec playwright install --with-deps chromium
      - name: Test and build website
        working-directory: web
        run: |
          pnpm test
          pnpm build
          pnpm test:e2e
      - name: Check public output
        run: python scripts/check_public_build.py --site web/dist --data generated/public-data.json
      - name: Upload generated database build
        uses: actions/upload-artifact@v7
        with:
          name: database-build
          path: generated/
```

- [ ] **Step 7: Run the complete gate locally**

Run:

```powershell
python -m pytest -q
observatory-build --project-root . --timestamp 1970-01-01T00:00:00Z
Set-Location web
pnpm install --frozen-lockfile
pnpm test
pnpm build
pnpm test:e2e
Set-Location ..
python scripts/check_public_build.py --site web/dist --data generated/public-data.json
```

Expected: every command exits 0.

- [ ] **Step 8: Commit the validation gate**

```powershell
git add scripts tests/test_public_build.py web/astro.config.mjs web/playwright.config.ts web/package.json .github/workflows/validate.yml
git commit -m "ci: validate database and public site"
```

### Task 2: Add the GitHub Pages Deployment Workflow

**Files:**
- Create: `.github/workflows/deploy-pages.yml`
- Modify: `scripts/check_public_build.py`
- Modify: `tests/test_public_build.py`

**Interfaces:**
- Consumes: passing database, UI and public-build checks.
- Starts only after the `Validate` workflow succeeds for a push to `main`.
- Produces: a Pages artefact containing `web/dist/` plus `/downloads/eu-ai-policy-observatory.sqlite`.
- Produces: a deployed URL through the `github-pages` environment.

- [ ] **Step 1: Add a failing downloadable-database assertion**

Extend `test_public_build.py`:

```python
def test_scanner_requires_downloadable_database(tmp_path: Path):
    site = tmp_path / "site"
    site.mkdir()
    data = tmp_path / "public-data.json"
    data.write_text('{"documents":[]}', encoding="utf-8")
    errors = check_public_build(site, data, require_database=True)
    assert any("downloadable SQLite database" in error for error in errors)
```

- [ ] **Step 2: Run the focused test and confirm failure**

Run `python -m pytest tests/test_public_build.py::test_scanner_requires_downloadable_database -q`.

Expected: failure because `require_database` is not accepted.

- [ ] **Step 3: Implement the deployment-artefact check**

When `require_database=True`, require a non-empty file at `site_root/downloads/eu-ai-policy-observatory.sqlite`, open it read-only with `sqlite3`, and require `PRAGMA integrity_check` to return `ok`.

- [ ] **Step 4: Create the Pages workflow**

Create `.github/workflows/deploy-pages.yml`:

```yaml
name: Deploy GitHub Pages

on:
  workflow_run:
    workflows: [Validate]
    types: [completed]

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build:
    if: >-
      github.event.workflow_run.conclusion == 'success' &&
      github.event.workflow_run.event == 'push' &&
      github.event.workflow_run.head_branch == 'main'
    runs-on: ubuntu-latest
    env:
      SITE_ORIGIN: https://${{ github.repository_owner }}.github.io
      BASE_PATH: /${{ github.event.repository.name }}
    steps:
      - uses: actions/checkout@v7
        with:
          ref: ${{ github.event.workflow_run.head_sha }}
      - uses: actions/setup-python@v6
        with:
          python-version: '3.13'
          cache: pip
      - uses: pnpm/action-setup@v6
        with:
          version: 10
      - uses: actions/setup-node@v7
        with:
          node-version: '24'
          cache: pnpm
          cache-dependency-path: web/pnpm-lock.yaml
      - name: Install dependencies
        run: |
          python -m pip install -e ".[test]"
          pnpm --dir web install --frozen-lockfile
      - name: Set reproducible build timestamp
        run: echo "BUILD_TIMESTAMP=$(git show -s --format=%cI HEAD)" >> "$GITHUB_ENV"
      - name: Test and generate database
        run: |
          python -m pytest -q
          observatory-build --project-root . --timestamp "$BUILD_TIMESTAMP"
      - name: Test and build website
        run: |
          pnpm --dir web test
          pnpm --dir web build
      - name: Add downloadable database
        run: |
          mkdir -p web/dist/downloads
          cp generated/eu-ai-policy-observatory.sqlite web/dist/downloads/eu-ai-policy-observatory.sqlite
      - name: Check publication artefact
        run: python scripts/check_public_build.py --site web/dist --data generated/public-data.json --require-database
      - uses: actions/configure-pages@v6
      - uses: actions/upload-pages-artifact@v5
        with:
          path: web/dist

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy
        id: deployment
        uses: actions/deploy-pages@v5
```

Run browser tests in the validation workflow; do not duplicate the Chromium download in the Pages workflow. The Pages workflow still runs Python and front-end unit tests before publication.

- [ ] **Step 5: Test the deployment artefact locally**

Run:

```powershell
New-Item -ItemType Directory -Force web/dist/downloads
Copy-Item generated/eu-ai-policy-observatory.sqlite web/dist/downloads/eu-ai-policy-observatory.sqlite
python scripts/check_public_build.py --site web/dist --data generated/public-data.json --require-database
```

Expected: exit 0 and the database integrity check returns `ok` internally.

- [ ] **Step 6: Commit Pages deployment**

```powershell
git add .github/workflows/deploy-pages.yml scripts/check_public_build.py tests/test_public_build.py
git commit -m "ci: deploy verified atlas to GitHub Pages"
```

### Task 3: Document, Publish and Verify the Public Repository

**Files:**
- Create: `README.md`
- Create: `CONTRIBUTING.md`
- Create: `SECURITY.md`
- Modify: `docs/data-dictionary.md`

**Interfaces:**
- Consumes: complete local project and passing workflows.
- Produces: public repository `eu-ai-policy-observatory` under the currently authenticated GitHub account.
- Produces: public Pages site at the repository's GitHub Pages URL.

- [ ] **Step 1: Write the public README**

Use these exact sections:

```text
EU AI Policy Observatory
Purpose
Current scope
Explore the database
Data model
Verification and provenance
Local development
Repository status versus public corpus
Limitations
Author
```

State prominently that the database is the primary output, only `published` records form the reviewed public corpus, the Version 0.1 boundary is 2018–2024 and the project does not yet implement LLM experiments. Link to the downloadable SQLite database through the Pages base path after publication.

- [ ] **Step 2: Write contribution and security guidance**

`CONTRIBUTING.md` documents one-record-per-file JSON, stable IDs, British English, source requirements, vocabulary changes, publication states, validation commands and the rule that an analytical relationship needs rationale and evidence.

`SECURITY.md` asks reporters not to open public issues for exposed credentials or private research data and directs them to GitHub's private vulnerability reporting interface when enabled. Do not publish a personal email address.

- [ ] **Step 3: Run the final local verification**

Run:

```powershell
python -m pytest -q
observatory-build --project-root . --timestamp 1970-01-01T00:00:00Z
Set-Location web
pnpm test
pnpm build
pnpm test:e2e
Set-Location ..
python scripts/check_public_build.py --site web/dist --data generated/public-data.json
git diff --check
git status --short
```

Expected: all checks pass; only the three new documentation files and intentional data-dictionary edits are uncommitted.

- [ ] **Step 4: Commit publication documentation**

```powershell
git add README.md CONTRIBUTING.md SECURITY.md docs/data-dictionary.md
git commit -m "docs: prepare public research repository"
```

- [ ] **Step 5: Confirm GitHub authentication without changing remote state**

Run:

```powershell
gh auth status
gh api user --jq .login
```

Expected: an authenticated GitHub account and its exact username. If authentication is absent, stop and ask the project owner to authenticate; do not request or handle a personal access token in chat.

- [ ] **Step 6: Create the public repository and configure its remote**

After authentication succeeds, run:

```powershell
gh repo create eu-ai-policy-observatory --public --source . --remote origin --description "A verified research database and static atlas of EU artificial intelligence policy."
gh repo edit --add-topic eu-policy --add-topic artificial-intelligence --add-topic sts --add-topic research-database
```

Expected: the empty public repository exists and `origin` points to it. Do not push yet, so Pages can be configured before the first deployment workflow starts.

- [ ] **Step 7: Enable GitHub Pages with the Actions build type**

Run:

```powershell
gh api --method POST "repos/{owner}/{repo}/pages" -f build_type=workflow
```

If the endpoint reports that Pages already exists, query it instead of retrying creation:

```powershell
gh api "repos/{owner}/{repo}/pages"
```

- [ ] **Step 8: Push and watch the first deployment**

Run:

```powershell
git push -u origin main
$validateRunId = gh run list --workflow validate.yml --limit 1 --json databaseId --jq '.[0].databaseId'
gh run watch $validateRunId --exit-status
$deployRunId = gh run list --workflow deploy-pages.yml --limit 1 --json databaseId --jq '.[0].databaseId'
gh run watch $deployRunId --exit-status
```

Expected: validation completes successfully, then the Pages workflow for the same `main` commit completes successfully.

- [ ] **Step 9: Verify the public repository and Pages URL**

Run:

```powershell
gh repo view --web
gh api "repos/{owner}/{repo}/pages" --jq .html_url
```

Open the returned Pages URL and verify Home, Policy Map, Timeline, Corpus, Methodology, About, at least six document pages and the SQLite download. Check a 390-pixel mobile viewport and a desktop viewport. Confirm that every published source link resolves to an official EU domain or has a documented verification note.

- [ ] **Step 10: Record publication metadata**

Add the returned repository and Pages URLs to `README.md`, update the project status to Version 0.1, rerun the documentation link check and commit:

```powershell
git add README.md
git commit -m "docs: record public release URLs"
git push
```

## Plan 3 Completion Gate

The project is complete only when:

- Local tests and both GitHub workflows pass.
- The public repository exists under the authenticated owner's account.
- GitHub Pages serves all six approved top-level pages.
- At least six verified published documents have stable public pages.
- The downloadable SQLite database passes `PRAGMA integrity_check`.
- No private material, local path, credential or non-published record is present in the Pages artefact.
- The site is usable on desktop and a 390-pixel mobile viewport.
