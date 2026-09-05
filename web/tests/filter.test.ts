import { describe, expect, it } from 'vitest';

import {
  buildCorpusSearchParams,
  buildTimelineEntries,
  filterDocuments,
  filterTimeline,
  parseCorpusCriteria,
  vocabularyLabel,
} from '../src/lib/filter';
import type { DocumentRecord, PolicyEvent, PublicData } from '../src/lib/types';
import { publishedDocuments } from './fixtures/documents';

const act = publishedDocuments[0];
if (act === undefined) throw new Error('Expected an AI Act fixture.');

const versionedDocuments: DocumentRecord[] = [
  ...publishedDocuments,
  {
    ...act,
    id: 'ai-act-presidency-compromise-2022',
    slug: 'ai-act-presidency-compromise-2022',
    official_title: 'Presidency compromise text on the Artificial Intelligence Act',
    short_title: 'AI Act Presidency compromise',
    record_level: 'version',
    official_reference: 'ST 10069/22',
    document_date: '2022-06-15',
    version_label: 'First consolidated Presidency compromise',
    version_status: 'draft',
    publication_date: '2022-06-15',
  },
  {
    ...act,
    id: 'ai-act-presidency-compromise-annex-2022',
    slug: 'ai-act-presidency-compromise-annex-2022',
    official_title: 'Annex to a Presidency compromise text on the Artificial Intelligence Act',
    short_title: 'AI Act Presidency compromise annex',
    record_level: 'attachment',
    official_reference: 'ST 10069/22 ADD 1',
    document_date: '2022-06-15',
    version_label: 'Annex',
    version_status: 'draft',
    publication_date: '2022-06-15',
  },
  {
    ...act,
    id: 'ai-act-revised-compromise-2022',
    slug: 'ai-act-revised-compromise-2022',
    official_title: 'Revised Presidency compromise text on the Artificial Intelligence Act',
    short_title: 'Earlier AI Act Presidency compromise',
    record_level: 'version',
    official_reference: 'ST 10068/22',
    document_date: '2022-05-15',
    version_label: 'Earlier Presidency compromise',
    version_status: 'revised',
    publication_date: '2022-05-15',
  },
  {
    ...act,
    id: 'transparency-code-draft-2022',
    slug: 'transparency-code-draft-2022',
    official_title: 'Draft code on AI-generated content transparency',
    short_title: 'Transparency code draft',
    record_level: 'version',
    official_reference: 'Draft transparency code',
    document_date: '2022-04-15',
    version_label: 'Draft',
    version_status: 'draft',
    publication_date: '2022-04-15',
    policies: [{
      ...act.policies[0]!,
      id: 'ai-generated-content-transparency',
      name: 'AI-generated content transparency',
    }],
  },
];

describe('filterDocuments', () => {
  it('matches titles, CELEX and ELI case-insensitively', () => {
    expect(filterDocuments(publishedDocuments, { query: '32024r1689' }).map((document) => document.id))
      .toEqual(['artificial-intelligence-act-2024']);
    expect(filterDocuments(publishedDocuments, { query: 'ELI/REG/2024' }).map((document) => document.id))
      .toEqual(['artificial-intelligence-act-2024']);
  });

  it('matches the general official reference case-insensitively', () => {
    expect(filterDocuments(versionedDocuments, {
      view: 'all',
      query: 'st 10069/22 add 1',
    }).map((document) => document.id)).toEqual(['ai-act-presidency-compromise-annex-2022']);
  });

  it('defaults to principal records and exposes every record in the all view', () => {
    expect(filterDocuments(publishedDocuments, {}).map((document) => document.id)).toEqual([
      'artificial-intelligence-act-2024',
      'artificial-intelligence-for-europe-2018',
    ]);
    expect(filterDocuments(versionedDocuments, { view: 'all' }).map((document) => document.id)).toEqual([
      'artificial-intelligence-act-2024',
      'ai-act-presidency-compromise-2022',
      'ai-act-presidency-compromise-annex-2022',
      'ai-act-revised-compromise-2022',
      'transparency-code-draft-2022',
      'artificial-intelligence-for-europe-2018',
    ]);
  });

  it('combines record level, version status and policy filters with logical AND', () => {
    expect(filterDocuments(versionedDocuments, {
      view: 'all',
      recordLevel: 'version',
      versionStatus: 'draft',
      policy: 'artificial-intelligence-act-legislative-process',
    }).map((document) => document.id)).toEqual(['ai-act-presidency-compromise-2022']);
  });

  it('combines concept and institution filters with logical AND', () => {
    expect(filterDocuments(publishedDocuments, {
      concept: 'risk',
      institution: 'european-commission',
    }).map((document) => document.id)).toEqual(['artificial-intelligence-act-2024']);
  });

  it('matches sector and provenance tags with logical AND', () => {
    expect(filterDocuments(publishedDocuments, {
      sector: 'financial_services',
      provenance: 'eu_institution_authored',
    }).map((document) => document.id)).toEqual(['artificial-intelligence-act-2024']);
  });

  it('separates a historical collection from publication year and pending review', () => {
    const historical = {
      ...act,
      id: 'historical-test-resolution',
      historical_review_status: 'verified' as const,
      temporal_collection: 'historical_lineage' as const,
      relevance_class: 'direct_ai_substantive' as const,
      document_date: '2017-02-16',
      publication_date: '2018-07-18',
      record_level: 'principal' as const,
    };
    const pending = {
      ...act,
      id: 'legacy-test-record',
      historical_review_status: 'legacy_review_pending' as const,
      temporal_collection: null,
      relevance_class: null,
      record_level: 'principal' as const,
    };
    const rows = [historical, pending];

    expect(filterDocuments(rows, {
      collection: 'historical_lineage',
      relevance: 'direct_ai_substantive',
      year: '2018',
    }).map((row) => row.id)).toEqual(['historical-test-resolution']);
    expect(filterDocuments(rows, { collection: 'historical_lineage', year: '2017' })).toEqual([]);
    expect(filterDocuments(rows, { relevance: 'legacy_review_pending' }).map((row) => row.id))
      .toEqual(['legacy-test-record']);
    expect(filterDocuments(rows, {}).map((row) => row.id).sort())
      .toEqual(['historical-test-resolution', 'legacy-test-record']);
  });

  it('sorts by publication date descending and short title ascending', () => {
    const communication = publishedDocuments[1];
    if (communication === undefined) throw new Error('Expected a communication fixture.');
    const sameDate: DocumentRecord = {
      ...communication,
      id: 'same-date',
      short_title: 'A companion communication',
      publication_date: '2024-07-12',
    };

    expect(filterDocuments([...publishedDocuments, sameDate], {}).map((document) => document.id)).toEqual([
      'same-date',
      'artificial-intelligence-act-2024',
      'artificial-intelligence-for-europe-2018',
    ]);
  });

  it('does not mutate its input array', () => {
    const documents = [...publishedDocuments].reverse();
    const before = documents.map((document) => document.id);

    const result = filterDocuments(documents, {});

    expect(documents.map((document) => document.id)).toEqual(before);
    expect(result).not.toBe(documents);
  });

  it('applies scalar filters without matching documents lacking an assessment', () => {
    expect(filterDocuments(publishedDocuments, { year: '2024' }).map((document) => document.id))
      .toEqual(['artificial-intelligence-act-2024']);
    expect(filterDocuments(publishedDocuments, { documentType: 'regulation' }).map((document) => document.id))
      .toEqual(['artificial-intelligence-act-2024']);
    expect(filterDocuments(publishedDocuments, { legalStatus: 'in_force' }).map((document) => document.id))
      .toEqual(['artificial-intelligence-act-2024']);
    expect(filterDocuments(publishedDocuments, { policyStage: 'adoption' }).map((document) => document.id))
      .toEqual(['artificial-intelligence-act-2024']);
    expect(filterDocuments(publishedDocuments, { corpusTier: 'core' }).map((document) => document.id))
      .toEqual(['artificial-intelligence-act-2024']);
  });
});

describe('Corpus query serialisation', () => {
  it('uses explicit human labels for verified classes and pending review', () => {
    expect(vocabularyLabel('direct_ai_substantive')).toBe('Direct AI relevance');
    expect(vocabularyLabel('ai_related_precursor')).toBe('AI-related precursor');
    expect(vocabularyLabel('indirect_adm_legal_context')).toBe('Automated-decision legal context');
    expect(vocabularyLabel('legacy_review_pending')).toBe('Expanded evidence review pending');
  });

  it('parses collection and relevance criteria without treating pending as verified', () => {
    expect(parseCorpusCriteria(new URLSearchParams(
      'collection=historical_lineage&relevance=legacy_review_pending',
    ))).toEqual({
      collection: 'historical_lineage',
      relevance: 'legacy_review_pending',
    });
  });

  it('serialises collection and relevance criteria in stable order', () => {
    expect(buildCorpusSearchParams(new URLSearchParams('ref=phd'), {
      collection: 'historical_lineage',
      relevance: 'direct_ai_substantive',
    }).toString()).toBe(
      'ref=phd&collection=historical_lineage&relevance=direct_ai_substantive',
    );
  });
  it('serialises sector and provenance criteria in stable order', () => {
    expect(buildCorpusSearchParams(new URLSearchParams('ref=phd'), {
      sector: 'health',
      provenance: 'eu_agency_or_body_authored',
    }).toString()).toBe(
      'ref=phd&sector=health&provenance=eu_agency_or_body_authored',
    );
  });

  it('preserves unrelated query parameters and emits controlled criteria in stable order', () => {
    expect(buildCorpusSearchParams(
      new URLSearchParams('ref=phd&query=old&view=principal&preview=true'),
      {
        view: 'all',
        query: 'AI Act',
        recordLevel: 'version',
        versionStatus: 'draft',
        policy: 'artificial-intelligence-act-legislative-process',
      },
    ).toString()).toBe(
      'ref=phd&preview=true&view=all&query=AI+Act&recordLevel=version&versionStatus=draft&policy=artificial-intelligence-act-legislative-process',
    );
  });

  it('canonicalises the principal default by removing stale controlled criteria', () => {
    expect(buildCorpusSearchParams(
      new URLSearchParams('ref=phd&view=all&query=old&recordLevel=version'),
      { view: 'principal' },
    ).toString()).toBe('ref=phd');
  });
});

const publishedAt = '2026-09-03T00:00:00Z';

const timelineEvents: PolicyEvent[] = [
  {
    id: 'event-tie',
    publication_status: 'published',
    created_at: publishedAt,
    updated_at: publishedAt,
    event_type: 'proposal',
    event_date: '2018-04-25',
    title: 'A recorded proposal event',
    description: 'An event linked to the 2018 document.',
    policy_id: 'policy-pathway',
    document_id: 'artificial-intelligence-for-europe-2018',
    source_id: 'source-2018',
  },
  {
    id: 'final-act-publication',
    publication_status: 'published',
    created_at: publishedAt,
    updated_at: publishedAt,
    event_type: 'publication',
    event_date: '2024-07-12',
    title: 'Publication of the final Act',
    description: 'An event linked to the final Act.',
    policy_id: 'policy-pathway',
    document_id: 'artificial-intelligence-act-2024',
    source_id: 'source-2024',
  },
  {
    id: 'unlinked-publication',
    publication_status: 'published',
    created_at: publishedAt,
    updated_at: publishedAt,
    event_type: 'publication',
    event_date: '2023-01-01',
    title: 'An unlinked publication event',
    description: 'An event with no document record.',
    policy_id: 'policy-pathway',
    document_id: null,
    source_id: 'source-unlinked',
  },
];

const timelineData: PublicData = {
  coverage: {
    from_year: 2018,
    to_year: 2024,
    last_verified_date: '2026-09-03',
    published_documents: publishedDocuments.length,
    principal_documents: 2,
    supporting_files_and_versions: 0,
    coverage_cutoff: '2026-09-04',
    coverage_statement: 'A deterministic test audit for the public corpus.',
    source_families: {
      total: 2,
      by_status: {
        not_started: 0,
        in_progress: 0,
        reviewed: 2,
        gap_found: 0,
        recheck_due: 0,
      },
    },
    inventory: {
      included: 2,
      merged: 0,
      excluded: 0,
      pending: 0,
    },
    unresolved_candidates: 0,
    historical_review: {
      verified: 1,
      legacy_review_pending: 1,
    },
    source_scopes: [],
  },
  generated_at: publishedAt,
  policies: [],
  documents: [
    ...publishedDocuments,
    {
      ...act,
      id: 'ai-act-presidency-compromise-2022',
      slug: 'ai-act-presidency-compromise-2022',
      short_title: 'AI Act Presidency compromise',
      record_level: 'version',
      document_date: '2022-06-15',
      publication_date: '2022-06-15',
    },
  ],
  events: timelineEvents,
  concepts: [],
  institutions: [],
  relationships: [],
  sources: [],
};

describe('timeline filtering', () => {
  it('builds every published document and event in ascending ISO-date then ID order', () => {
    expect(buildTimelineEntries(timelineData).map((entry) => entry.id)).toEqual([
      'artificial-intelligence-for-europe-2018',
      'event-tie',
      'ai-act-presidency-compromise-2022',
      'unlinked-publication',
      'artificial-intelligence-act-2024',
      'final-act-publication',
    ]);
  });

  it('inherits linked document metadata and keeps unlinked events empty', () => {
    const entries = buildTimelineEntries(timelineData);

    expect(entries.find((entry) => entry.id === 'final-act-publication')).toMatchObject({
      kind: 'event',
      href: 'corpus/artificial-intelligence-act/',
      institutionIds: ['european-commission'],
      documentType: 'regulation',
      policyStage: 'adoption',
      eventType: 'publication',
    });
    expect(entries.find((entry) => entry.id === 'unlinked-publication')).toMatchObject({
      kind: 'event',
      href: 'policies/policy-pathway/',
      institutionIds: [],
      documentType: null,
      policyStage: null,
      eventType: 'publication',
      dateKind: null,
    });
    expect(entries.find((entry) => entry.id === 'artificial-intelligence-act-2024')).toMatchObject({
      kind: 'document',
      dateKind: 'official_act_date',
    });
  });

  it('applies timeline criteria with logical AND and normalised values', () => {
    const entries = buildTimelineEntries(timelineData);

    expect(filterTimeline(entries, {
      institution: ' EUROPEAN-COMMISSION ',
      documentType: 'REGULATION',
      policyStage: 'adoption',
      eventType: 'PUBLICATION',
    }).map((entry) => entry.id)).toEqual(['final-act-publication']);
  });

  it('does not treat nullable assessments or unlinked events as matching a policy stage', () => {
    const entries = buildTimelineEntries(timelineData);

    expect(filterTimeline(entries, { policyStage: 'adoption' }).map((entry) => entry.id)).toEqual([
      'artificial-intelligence-act-2024',
      'final-act-publication',
    ]);
  });

  it('defaults to principal timeline records while retaining unlinked events', () => {
    const entries = buildTimelineEntries(timelineData);

    expect(filterTimeline(entries, {}).map((entry) => entry.id)).toEqual([
      'artificial-intelligence-for-europe-2018',
      'event-tie',
      'unlinked-publication',
      'artificial-intelligence-act-2024',
      'final-act-publication',
    ]);
    expect(filterTimeline(entries, { view: 'all' }).map((entry) => entry.id)).toContain(
      'ai-act-presidency-compromise-2022',
    );
    expect(entries.find((entry) => entry.id === 'unlinked-publication')?.recordLevel).toBeNull();
  });

  it('returns new arrays without mutating source documents, events or entries', () => {
    const documents = [...timelineData.documents].reverse();
    const events = [...timelineData.events].reverse();
    const beforeDocuments = documents.map((document) => document.id);
    const beforeEvents = events.map((event) => event.id);
    const entries = buildTimelineEntries({ ...timelineData, documents, events });
    const beforeEntries = entries.map((entry) => entry.id);

    const filtered = filterTimeline(entries, { eventType: 'publication' });

    expect(documents.map((document) => document.id)).toEqual(beforeDocuments);
    expect(events.map((event) => event.id)).toEqual(beforeEvents);
    expect(entries.map((entry) => entry.id)).toEqual(beforeEntries);
    expect(entries).not.toBe(documents);
    expect(filtered).not.toBe(entries);
  });
});
