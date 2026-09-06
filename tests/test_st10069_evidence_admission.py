"""Evidence and preservation contracts for the one-record admission."""
import json
import tempfile
from pathlib import Path

import pytest
from observatory.pipeline import run_pipeline

ROOT = Path(__file__).resolve().parents[1]
TARGET = 'ai-act-council-first-consolidated-compromise-st-10069-2022'
HOLDS = {'ai-act-council-third-compromise-part-one-st-12206-2022-init', 'gpai-training-content-explanatory-notice-2025', 'gpai-training-content-template-2025', 'standardisation-request-c-2025-3871'}

@pytest.fixture(scope='module')
def payload():
    with tempfile.TemporaryDirectory(prefix='euai-st-') as out:
        result = run_pipeline(ROOT, '2026-09-06T21:00:00Z', output_root=Path(out))
        return json.loads(result.public_json.read_text(encoding='utf-8'))

def test_st10069_and_later_backfill_preserve_the_four_qualified_holds(payload):
    assert len(payload['documents']) == 192
    assert payload['coverage']['historical_review'] == {'verified':188,'legacy_review_pending':4}
    assert {d['id'] for d in payload['documents'] if d['historical_review_status']!='verified'} == HOLDS
    assert len(payload['relationships']) == 115

def test_st10069_preserves_issue_and_records_documented_access(payload):
    d = next(d for d in payload['documents'] if d['id']==TARGET)
    assert d['document_date'] == '2022-06-15'
    assert d['publication_date'] == '2022-06-20'
    assert d['document_date_kind'] == 'document_issue'
    assert d['legal_status'] == 'non_binding'
    assert d['record_level'] == 'version'
    assert d['date_evidence']['publication_date']['source_id'] == 'council-access-request-22-1313'
    assert 'not first-ever' in d['date_evidence']['publication_date']['meaning']
    sources = {s['id']:s for s in d['sources']}
    assert sources['council-st-10069-2022']['url'].endswith('/ST-10069-2022-INIT/x/pdf')
    assert sources['council-access-request-22-1313']['url'].endswith('?RequestNumber=22%2F1313')
    assert 'council-access-request-22-1307' in sources
    assert 'council-access-dataset-semantics' in sources
    assert d['bibliographic_authors'][0]['name'] == 'Presidency of the Council of the European Union'
    assert 'without implying Council adoption' in d['institutions'][0]['evidence_locator']
    assert d['corpus_assessment']['reviewed_by'] == 'Yichen Hao'
    assert d['corpus_assessment']['reviewed_at'] == '2026-09-04T00:00:00Z'

@pytest.mark.parametrize('identifier',sorted(HOLDS))
def test_holds_are_not_partially_extended(identifier):
    d = json.loads((ROOT/'data/documents'/f'{identifier}.json').read_text(encoding='utf-8'))
    assert 'historical_review_status' not in d
    assert 'date_evidence' not in d
    if identifier.startswith('gpai-'):
        assert 'gpai-training-summary-july-original-annex' in d['source_ids']
        assert 'parent' in d['corpus_assessment']['researcher_notes'].lower()
        assert 'public' in d['corpus_assessment']['researcher_notes'].lower()
