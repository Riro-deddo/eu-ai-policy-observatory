import type { DocumentRecord } from './types';

export interface CorpusCriteria {
  query?: string;
  year?: string;
  institution?: string;
  documentType?: string;
  legalStatus?: string;
  policyStage?: string;
  concept?: string;
  corpusTier?: string;
}

function normalise(value: string): string {
  return value.trim().toLocaleLowerCase('en-GB');
}

function matchesValue(value: string, criterion: string | undefined): boolean {
  return criterion === undefined || normalise(value) === normalise(criterion);
}

function hasMatchingId(entries: Array<{ id: string }>, criterion: string | undefined): boolean {
  return criterion === undefined || entries.some((entry) => matchesValue(entry.id, criterion));
}

export function filterDocuments(
  documents: DocumentRecord[],
  criteria: CorpusCriteria,
): DocumentRecord[] {
  const query = criteria.query === undefined ? undefined : normalise(criteria.query);

  return documents
    .filter((document) => {
      const queryMatches = query === undefined || query === '' || [
        document.official_title,
        document.short_title,
        document.celex,
        document.eli,
      ].some((value) => value !== null && normalise(value).includes(query));
      const assessment = document.corpus_assessment;

      return queryMatches
        && (criteria.year === undefined || document.publication_date.startsWith(criteria.year))
        && hasMatchingId(document.institutions, criteria.institution)
        && matchesValue(document.document_type, criteria.documentType)
        && matchesValue(document.legal_status, criteria.legalStatus)
        && (criteria.policyStage === undefined
          || assessment?.policy_stage !== undefined
            && matchesValue(assessment.policy_stage, criteria.policyStage))
        && hasMatchingId(document.concepts, criteria.concept)
        && (criteria.corpusTier === undefined
          || assessment?.corpus_tier !== undefined
            && matchesValue(assessment.corpus_tier, criteria.corpusTier));
    })
    .sort((first, second) => (
      second.publication_date.localeCompare(first.publication_date, 'en-GB')
      || first.short_title.localeCompare(second.short_title, 'en-GB')
      || first.id.localeCompare(second.id, 'en-GB')
    ));
}
