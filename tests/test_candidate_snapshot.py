"""Evidence-specific export regressions for the 34-candidate adjudication."""
import hashlib
import json
import os
import tempfile
from pathlib import Path

import pytest
from observatory.pipeline import run_pipeline

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / 'research/reviews/2026-09-06-candidate-snapshot'


@pytest.fixture(scope='module')
def exported():
    with tempfile.TemporaryDirectory(prefix='candidate-snapshot-', dir=os.environ.get('TEMP')) as out:
        result = run_pipeline(ROOT, '2026-09-06T22:52:47Z', output_root=Path(out))
        return json.loads(result.public_json.read_text(encoding='utf-8'))


def test_historical_pilot_is_exported_with_precursor_scope(exported):
    rows = {d['id']: d for d in exported['documents']}
    identifier = 'council-decision-82-878-eec-esprit-pilot'
    assert identifier in rows
    row = rows[identifier]
    assert (row['document_date'], row['publication_date']) == ('1982-12-21', '1982-12-29')
    assert row['relevance_class'] == 'ai_related_precursor'
    assert row['temporal_collection'] == 'historical_lineage'
    assert row['legal_status'] == 'expired'
    assert ('council-of-the-european-communities', 'adopter') in {(r['id'], r['role']) for r in row['institutions']}


@pytest.mark.parametrize('identifier,date', [
    ('jrc-ai-watch-defining-ai-2020', '2020-02-27'),
    ('jrc-ai-watch-defining-ai-2-2021', '2021-10-29'),
    ('jrc-ai-watch-public-services-2020', '2020-07-02'),
    ('jrc-ai-watch-public-sector-workshop-2020', '2020-06-08'),
])
def test_jrc_releases_use_repository_availability_not_workshop_or_file_dates(exported, identifier, date):
    rows = {d['id']: d for d in exported['documents']}
    assert identifier in rows
    assert rows[identifier]['document_date'] == rows[identifier]['publication_date'] == date
    assert rows[identifier]['document_date_kind'] == 'publication'
    assert rows[identifier]['bibliographic_authors']
    assert rows[identifier]['legal_status'] == 'non_binding'


@pytest.mark.parametrize('number,date', [('732802','2022-06-20'), ('732836','2022-06-21'),
    ('732837','2022-06-21'), ('732838','2022-06-21'), ('732839','2022-06-21'),
    ('732840','2022-06-21'), ('732841','2022-06-21'), ('732843','2022-06-21'), ('732844','2022-06-20')])
def test_amendment_pdf_issue_and_exact_manifestation_release_remain_distinct(exported, number, date):
    rows = {d['id']: d for d in exported['documents']}
    identifier = 'ep-ai-act-committee-amendments-pe-' + number
    assert identifier in rows
    row = rows[identifier]
    assert row['document_date'] == '2022-06-13'
    assert row['document_date_kind'] == 'document_issue'
    assert row['publication_date'] == date
    assert row['legal_status'] == 'proposed'


def test_original_192_documents_remain_unmodified():
    baseline = json.loads((REVIEW / 'baseline.json').read_text(encoding='utf-8'))
    for old in baseline['document_hashes']:
        path = ROOT / 'data/documents' / (old['id'] + '.json')
        assert path.exists(), old['id']
        assert hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest() == old['lf_sha256'], old['id']


def test_every_pending_candidate_has_a_decision_and_prior_decision_history():
    baseline = json.loads((REVIEW / 'baseline.json').read_text(encoding='utf-8'))
    path = REVIEW / 'candidate-decisions.json'
    assert path.exists(), 'All 34 adjudication outcomes must be recorded'
    decisions = json.loads(path.read_text(encoding='utf-8'))['decisions']
    assert len(decisions) == len({d['id'] for d in decisions}) == 34
    assert {d['id'] for d in decisions} == {d['id'] for d in baseline['pending_before']}
    assert sum(d['decision'] == 'included' for d in decisions) == 26
    assert all(d['reopen_when'] for d in decisions if d['decision'] == 'pending')
    current = {c['id']: c for c in json.loads((ROOT / 'research/corpus-inventory.json').read_text(encoding='utf-8'))['candidates']}
    for old in baseline['pending_before']:
        old_decision = {k: v for k, v in old.items() if k != 'id'}
        assert old_decision in current[old['id']].get('decision_history', [])


def test_unresolved_candidates_are_not_exported(exported):
    inventory = json.loads((ROOT / 'research/corpus-inventory.json').read_text(encoding='utf-8'))['candidates']
    pending = {c['id'] for c in inventory if c['decision'] == 'pending'}
    assert pending.isdisjoint({d['id'] for d in exported['documents']})
    assert exported['coverage']['unresolved_candidates'] == len(pending)

@pytest.mark.parametrize('identifier,issue,publication', [
    ('eba-rising-ai-banking-payments-factsheet-2025', '2025-09-25', '2025-09-25'),
    ('eiopa-big-data-motor-health-insurance-2019', '2019-05-08', '2019-05-08'),
    ('ema-2024-ai-observatory-report-2025', '2025-05-08', '2025-07-10'),
    ('ema-fda-good-ai-practice-drug-development-2026', '2026-01-14', '2026-01-14'),
    ('hma-ema-llm-guiding-principles-2024', '2024-08-29', '2024-09-05'),
    ('advanced-robotics-ai-task-automation-osh-2022', '2022-04-26', '2022-04-26'),
    ('ai-border-control-migration-security-main-report-2020', '2020-05-28', '2020-05-28'),
    ('ai-watch-ai-uptake-smart-mobility-2021', '2021-09-15', '2021-09-15'),
    ('ethics-connected-automated-vehicles-2020', '2020-09-17', '2020-09-17'),
    ('people-machines-robots-skills-2017', '2017-07-31', '2017-07-31'),
])
def test_sector_and_health_releases_are_evidenced(exported, identifier, issue, publication):
    rows = {d['id']: d for d in exported['documents']}
    assert identifier in rows
    assert rows[identifier]['document_date'] == issue
    assert rows[identifier]['publication_date'] == publication
    assert rows[identifier]['legal_status'] == 'non_binding'


def test_jrc_earlier_official_release_is_separately_preserved(exported):
    row = next(d for d in exported['documents'] if d['id'] == 'jrc-ai-watch-defining-ai-2020')
    assert any(d['kind'] == 'first_official_publication' and d['value'] == '2020-02-21'
               for d in row['additional_dates'])


def test_annex22_does_not_evade_unresolved_parent_gate(exported):
    assert 'draft-gmp-annex-22-artificial-intelligence-2025' not in {d['id'] for d in exported['documents']}


def test_four_retained_holds_preserve_specific_reopening_conditions(exported):
    ledger = json.loads((REVIEW / 'retained-records.json').read_text(encoding='utf-8'))
    assert len(ledger['decisions']) == 4
    current = {d['id']: d for d in exported['documents']}
    for row in ledger['decisions']:
        assert row['disposition'] == 'retain_qualified_pending'
        assert row['unresolved'] and row['reopen_when']
        assert current[row['document_id']]['historical_review_status'] == 'legacy_review_pending'
