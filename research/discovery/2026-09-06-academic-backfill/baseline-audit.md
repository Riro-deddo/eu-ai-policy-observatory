# Independent bounded academic audit

Baseline: `5ed89e1ba71f476f9ca14814e97d8f5f8043cc16` in `academic-readiness-20260906`.
Audit date: 6 September 2026; report completion recorded at 22:13:32 UTC.
This report is outside the repository. No repository files, Git state, canonical records or generated outputs were changed by this audit.

## Scope and sampling

The structural audit loaded all 187 canonical documents, 297 sources, 115 relationships, 44 institutions, 25 events, seven policies, four concepts, 227 inventory decisions and 54 source-sweep entries. Read-only calls to `validate_records`, `validate_research_inventory` and `validate_historical_publication` each returned zero issues. No pipeline was run. This establishes conformity to the present rules, not substantive truth of every recorded claim.

Independent counts reproduce 97 principal, 36 supporting, 30 version and 24 attachment documents; 183 expanded-review verified and four qualified legacy records; 187 included, 18 merged, 10 excluded and 12 pending candidates. Every published document has an included inventory decision. There are 114 published verified relationships and one unpublished pending relationship. All document dates fall between 1984-02-28 and 2026-07-27. One publication date is null under the existing explicit qualification. No assessment timestamp exceeds its document's update timestamp.

Substantive review was purposive, exploratory and bounded, not random or a preregistered error-rate study. Selection followed structural anomalies and interpretation risks: all six CELEX sector-3 records missing OJ references; the anomalous old `in_force` FP5 record; the two newest 2026 adopted regulations; one mixed institutional/external authorship study; and the documented July/November GPAI version split. Exact selected canonical IDs:

- `council-decision-88-279-eec-esprit-ii`
- `council-decision-88-417-eec-delta`
- `council-decision-89-415-eec-doses`
- `council-decision-94-802-ec-esprit`
- `horizon-2020-specific-programme-decision-2013-743-eu`
- `sixth-framework-programme-decision-1513-2002-ec`
- `historical-fp5-ist-specific-programme`
- `ai-omnibus-regulation-2026-1744`
- `ai-act-proceedings-implementing-regulation-2026-1755`
- `ep-ethical-cyber-physical-systems-2016`
- `gpai-provider-guidelines-2025`

Primary-source comparison covered bibliographic identity/date panels for the six OJ omissions, relevant Horizon repeal provisions, 2026 regulation identity/publication and selected operative text, and the Parliament study's cover/credits. It did not reread all pages of all eleven documents. FP5 received an exploratory primary-source search; no repeal was established, so programme completion was not treated as legal expiry. The current GPAI download could not be fetched by the browsing tool; the backlog finding below is based on the repository's own explicit preserved evidence, not a new independent finding about its publication date. Direct EUR-Lex access sometimes returned a robot check/cache failure; indexed primary EUR-Lex pages supplied the identified metadata where noted.

The existing README, methodology, data dictionary and `docs/releases/v0.1.0.md` were checked first. They already disclose non-exhaustiveness, English manifestations, missing annotations, work/version dependence, lack of completed coding, legacy search-log gaps, four qualified published records, twelve pending candidates and the difference between display credit and human sign-off. Those are not presented below as newly discovered defects. The following six findings are ranked by research consequence.

## 1. High: Horizon 2020 has an unqualified in-force status despite an express repeal

Evidence: `data/documents/horizon-2020-specific-programme-decision-2013-743-eu.json:27` records `in_force`; line 54 claims its current status is resolved. There is no `legal_status_evidence` qualification. This is consequential for any analysis of active instruments.

[Council Decision (EU) 2021/764](https://eur-lex.europa.eu/legal-content/en/TXT/?uri=CELEX:32021D0764), Article 15, expressly repeals Decision 2013/743/EU with effect from 1 January 2021. Article 16(1) preserves its application to existing actions until their closure. The [official consolidated predecessor PDF](https://eur-lex.europa.eu/eli/dec/2013/743/2021-01-01/eng/pdf) also identifies the repeal. The old [original EUR-Lex identity panel](https://eur-lex.europa.eu/legal-content/EN/TXT/?qid=1757323841187&uri=CELEX:32013D0743) nevertheless displays an in-force indicator. This is a real source conflict that the current unqualified field conceals; it is not a conclusion inferred from the programme's end year.

Minimum safe remediation: record `repealed`, add the repealing act as an official evidence source and cite Articles 15-16 together; explain transitional continued application and the conflicting legacy EUR-Lex indicator. Preserve the prior value in a new dated correction ledger and leave historical assessments untouched. Do not imply that repeal terminated every existing grant action. A review checklist should compare operative repeal/savings provisions when a status panel conflicts; globally changing all old programmes to expired would be unsound. Structural context: 131 of the 183 verified records lack a dedicated legal-status citation, but that absence alone does not establish 131 wrong statuses.

## 2. Medium: A known distinct GPAI final document has disappeared from the active candidate queue

Evidence: `research/corpus-inventory.json:705` explicitly recognises C(2025) 7719 as a different document while the sole corresponding included candidate is now the July C(2025) 5045 ANNEX. `data/documents/gpai-provider-guidelines-2025.json:55` explains that same separation. `research/staging/2026-09-05-review-continuation/commission.json:349` preserves an unresolved exact-publication finding for C(2025) 7719. There is no separate active candidate for that reference in the inventory. A search of the complete inventory found only the July candidate's explanatory mention and an unrelated ISSN containing 7719.

The existing disclosure that the corpus is incomplete is correct, but it does not repair this concrete workflow loss: an already discovered distinct work can no longer be tracked through the twelve pending inventory decisions. Preserved historical staging evidence remains available, so this is not lost evidence or a reason to rewrite earlier decisions.

Minimum safe remediation: add a new pending candidate for the distinct November communication at the actual reconciliation time, citing its earlier discovery/hold evidence and retaining its exact publication-date gap. Do not merge it into the July annex, copy the July release date, or admit it solely to reduce pending counts. This finding does not claim that the current final text is unpublished; it identifies absent active decision tracking.

## 3. Medium: The annotation subset is strongly associated with ingestion cohort

Evidence: all 187 records were compared by `created_at`, `concept_ids` and `policy_ids`. The 69 documents without concept assignments are exactly the same 69 without policy assignments. All 117 documents created on 3-4 September have both kinds of assignment. Of the 70 created on 5-6 September, 69 have neither; the only exception is `draft-high-risk-classification-guidelines-consultation-work-2026`. Examples are `data/documents/building-a-european-data-economy.json:47` and `data/documents/ep-ethical-cyber-physical-systems-2016.json:60`. `web/src/pages/methodology.astro:94` discloses aggregate missingness but not this cohort concentration.

Thus a concept/policy-filtered sample is also largely a selection of the earlier ingestion cohort. The newer historical and sector backfill is disproportionately excluded. This is an observed association, not a claim about the unrecorded causal reasons for missingness. Generic warnings against interpreting empty lists as absence do not tell a researcher how concentrated the selection is.

Minimum safe remediation: add this measured cohort pattern to the research-use disclosure, explicitly tie filter denominators to annotated records, and require stratified missingness assessment before constructing a longitudinal or sector sample. A small generated breakdown by collection or ingestion cohort would make it inspectable. Preserve empty values until an actual annotation protocol is applied; do not mass-populate concepts or policy memberships from titles.

## 4. Medium: Six assigned OJ citations are missing from their canonical citation fields

Each affected JSON has `oj_reference: null` at line 22, despite its own `classification_evidence` recording the exact assigned citation. The dictionary defines null as the alternative when no OJ reference is assigned. The omissions propagate into generated citation metadata and make this subset less complete than the underlying evidence.

| Canonical ID | Verified OJ citation | Primary source |
| --- | --- | --- |
| `council-decision-88-279-eec-esprit-ii` | OJ L 118, 6.5.1988, pp. 32-41 | [EUR-Lex 31988D0279](https://eur-lex.europa.eu/eli/dec/1988/279/oj/eng) |
| `council-decision-88-417-eec-delta` | OJ L 206, 30.7.1988, pp. 20-28 | [EUR-Lex 31988D0417](https://eur-lex.europa.eu/legal-content/EN/TXT/?qid=1782585447264&uri=CELEX:31988D0417) |
| `council-decision-89-415-eec-doses` | OJ L 200, 13.7.1989, pp. 46-49 | [EUR-Lex 31989D0415](https://eur-lex.europa.eu/legal-content/EN/TXT/?qid=1781991592358&uri=CELEX:31989D0415) |
| `council-decision-94-802-ec-esprit` | OJ L 334, 22.12.1994, pp. 24-46 | [EUR-Lex 31994D0802](https://eur-lex.europa.eu/legal-content/AUTO/?qid=1669824862680&rid=4&uri=CELEX:31994D0802) |
| `horizon-2020-specific-programme-decision-2013-743-eu` | OJ L 347, 20.12.2013, pp. 965-1041 | [EUR-Lex 32013D0743](https://eur-lex.europa.eu/legal-content/EN/TXT/?qid=1757323841187&uri=CELEX:32013D0743) |
| `sixth-framework-programme-decision-1513-2002-ec` | OJ L 232, 29.8.2002, pp. 1-33 | [EUR-Lex 32002D1513](https://eur-lex.europa.eu/eli/dec/2002/1513/oj/eng) |

Minimum safe remediation: fill only the OJ field and actual update timestamp, append a correction ledger, and rebuild derivatives. Preserve historical hashes through the existing explicit reconstruction approach rather than rewriting historical evidence. No legal or substantive classification change follows merely from filling these citations.

## 5. Medium: A directly relevant, precisely identifiable Horizon successor is absent

Full canonical and inventory searches found no CELEX `32021D0764` or reference `2021/764`. This is a concrete missing item within the declared publication boundary, not a claim that the corpus promised completeness. It is particularly useful because it supplies both the predecessor's repeal evidence and a substantive AI research-programme continuation.

Admission preparation from the [official act](https://eur-lex.europa.eu/legal-content/en/TXT/?uri=CELEX:32021D0764):

- Reference: Council Decision (EU) 2021/764; CELEX `32021D0764`.
- Act date: 10 May 2021, from the heading and signature; publication: 12 May 2021, from the OJ masthead. These are different dates. Article 17 separates entry into force on publication from application from 1 January 2021.
- Adopter: Council of the European Union, shown in the enactment and signature; proposer: European Commission, shown in the preamble.
- Exact substantive locator: Annex I, Pillar II, cluster 4 (Digital, Industry and Space), section 4.2.5, Artificial Intelligence and Robotics. The section specifies AI research, ethics, safety, discrimination risks and human oversight, alongside robotics. Section 1.2.5 separately supports health-sector AI applications.
- Suggested conservative research classification: contemporary EU AI policy; direct substantive AI relevance. Research/innovation and industry are supported by section 4.2.5; health can be supported separately by section 1.2.5. These remain researcher classifications, not an EU-assigned ontology.
- Evidence of predecessor relation: Articles 15-16, as in finding 1. Preserve the difference between repeal and transitional continued application.

Minimum safe remediation: record a new candidate with the actual discovery timestamp, verify and retain the exact official English manifestation and complete the normal gate. The facts above are preparation, not a completed admission, PDF snapshot, exhaustive reading or human approval.

Two additional primary-source leads appeared incidentally in the exact-identifier searches: Council Decision (CFSP) 2022/2269, Article 1, on responsible AI for peace/security, and Regulation (EU) 2026/150, Article 1, on AI gigafactories. Neither identifier was found in canonical or inventory data. They should be carried forward as leads, not claimed as reviewed admissions in this bounded correction. Sources: [2022/2269](https://eur-lex.europa.eu/legal-content/en/TXT/?uri=CELEX:32022D2269), [2026/150](https://eur-lex.europa.eu/legal-content/en/TXT/?uri=CELEX:32026R0150).

## 6. Lower: The dictionary omits institution roles used by 82 published documents

Evidence: `docs/data-dictionary.md:141` lists only author, proposer, adopter, publisher and contributor. `schema/controlled-vocabularies.json:7` and `schema/historical-document-extension.schema.json:111` also permit commissioner, official_host, responsible_body, requester, supervisor and cover_note_sender. A census found 82 documents using at least one omitted role. These distinctions matter when readers measure institutional authorship, commissioning or transmission: a cover-note sender is not necessarily the author of the attached policy text.

Minimum safe remediation: document the actual role vocabulary and evidence fields, with concise distinctions between authorship, commissioning, hosting and transmission. Update the dictionary from the current schema; do not simplify the records into author roles. Existing source locators already support many of these distinctions.

## Interpretation

This baseline is structurally coherent and unusually explicit about several limits. No general allegation of fabricated evidence follows from the findings. Its strongest immediate correction is the Horizon legal-status conflict. Citation completion, active tracking of the distinct GPAI hold, and the measured cohort disclosure are bounded improvements. They do not convert this database into an exhaustive corpus or a completed coding study. The v0.1.0 release should remain immutable; subsequent corrections belong in a new version with preserved history.
