"""Unknown dates remain unknown across validation, SQLite and public export."""
import json
import shutil
import sqlite3
from pathlib import Path

import pytest
from observatory.build_db import build_database
from observatory.export_public import export_public
from observatory.io import load_records
from observatory.validate import validate_records

QUALIFICATION = {
    'kind': 'publication_date_pending',
    'confirmed': 'Official text and adoption date confirmed.',
    'unresolved': 'No qualifying public-release date has been established.',
}


def fixture_data(tmp_path, **updates):
    target = tmp_path / 'data'
    shutil.copytree(Path('tests/fixtures/valid/data'), target)
    path = target / 'documents/example-document.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    data.update(publication_date=None, review_qualification=QUALIFICATION)
    data.update(updates)
    path.write_text(json.dumps(data), encoding='utf-8')
    return target


def issues_for(root):
    return validate_records(root, Path('schema/record.schema.json'), Path('schema/controlled-vocabularies.json'))


def test_pending_unknown_date_validates_and_roundtrips(tmp_path):
    root = fixture_data(tmp_path)
    assert issues_for(root) == []
    database = tmp_path / 'out.sqlite'
    build_database(load_records(root), Path('schema/database.sql'), database)
    with sqlite3.connect(database) as db:
        value, qualification = db.execute('SELECT publication_date, review_qualification FROM documents').fetchone()
        assert value is None
        assert json.loads(qualification) == QUALIFICATION
    output = tmp_path / 'public.json'
    export_public(database, output, '2026-09-06T21:00:00Z', {})
    document = json.loads(output.read_text())['documents'][0]
    assert document['publication_date'] is None
    assert document['review_qualification'] == QUALIFICATION
    assert document['historical_review_status'] == 'legacy_review_pending'


@pytest.mark.parametrize('updates', [
    {'historical_review_status': 'verified'},
    {'review_qualification': None},
    {'publication_date': '2026-09-03'},
    {'review_qualification': {**QUALIFICATION, 'unresolved': ' '}},
])
def test_inconsistent_or_unexplained_gap_is_rejected(tmp_path, updates):
    assert issues_for(fixture_data(tmp_path, **updates))


def test_sql_rejects_verified_unknown_date(tmp_path):
    records = load_records(fixture_data(tmp_path, historical_review_status='verified'))
    with pytest.raises(sqlite3.IntegrityError):
        build_database(records, Path('schema/database.sql'), tmp_path / 'invalid.sqlite')


def test_canonical_qualifications_do_not_promote_pending_records():
    docs = [json.loads(p.read_text(encoding='utf-8')) for p in Path('data/documents').glob('*.json')]
    pending = [d for d in docs if d.get('historical_review_status') != 'verified']
    assert len(pending) == 4
    assert sorted(d['review_qualification']['kind'] for d in pending) == [
        'official_version_conflict', 'parent_evidence_pending', 'parent_evidence_pending', 'publication_date_pending']
    standard = next(d for d in pending if d['id'] == 'standardisation-request-c-2025-3871')
    assert standard['publication_date'] is None
    assert standard['document_date'] == '2025-06-23'
    assert standard['legal_status'] == 'adopted'
