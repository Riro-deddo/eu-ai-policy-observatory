# Historical requirement recheck

Review date: 5 September 2026. Publication cutoff: 4 September 2026, unchanged.
Reviewer: AI-assisted reviewer, AI-assisted source and contract review. No human admission decision is inferred.

## Requirement and outcome

The task is to investigate EU AI-related documents before 2018, audit omissions against the approved design, and extend the collection where official evidence justifies it. CI repair and unrelated UI work are not the research deliverable.

The [approved historical scope](../../docs/superpowers/specs/2026-09-05-historical-scope-and-coverage-design.md) already makes 2018 an analytical boundary, not a lower eligibility limit. It includes relevant European Communities predecessors. No replacement design or new entity model is needed.

Fresh inspection of canonical `data/documents/*.json`, rather than the older generated export, found:

| Measure | Observed state |
| --- | --- |
| Published canonical documents | 117 |
| Earliest canonical document date | 2018-04-25 |
| Canonical documents dated before 2018 | 0 |
| Documents with active temporal/relevance/date-kind fields | 0 |
| Historical candidates in the existing admission ledger | 17 |
| Historical evidence-ready recommendations in that ledger | 14 |
| Historical evidence holds in that ledger | 3 |
| Historical canonical imports | 0 |

The existing [admission ledger](../admission/2026-09-05-document-admission-review.json) and [review report](2026-09-05-document-admission-review.md) are preserved unchanged. Evidence readiness, editorial admission, canonical import and public deployment are separate states. This recheck does not claim the original requirement is fully delivered.

## Official-source checks and new evidence

### Reconfirmed historical anchors

- **ESPRIT I, Council Decision 84/130/EEC:** act dated 28 February 1984; OJ publication 9 March 1984. Annex section 3 funds knowledge processing, expert systems, inference and learning. It qualifies as a documented precursor, not an early AI Act version. The act also cites Decision 82/878/EEC, a backward-search lead. [Official text](https://eur-lex.europa.eu/eli/dec/1984/130/oj/eng).
- **Civil Law Rules on Robotics, 2017 Parliament resolution:** adopted 16 February 2017; OJ manifestation dated 18 July 2018. Recitals B-C expressly discuss AI; paragraphs 24-35 address autonomous transport and care/medical robotics. The later OJ date does not create a second contemporary document. [Official text](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52017IP0051).

### EESC 2017 opinion: original access hold can now be reconsidered

The English [official PDF](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:52016IE5369) was opened. Page 1 confirms plenary adoption on 31 May 2017, publication on 31 August 2017, reference 2017/C 288/01 and rapporteur Catelijne Muller. Sections 1.4-1.11 support direct AI relevance and cross-sector/employment classification; section 3.1 supports health, section 3.39 defence, and sections 4.1-4.4 research. These are editorial tag recommendations. EESC remains the authoring/adopting EU body, distinct from its rapporteur and publisher.

The prior English-primary-text access obstacle is resolved for passage review. Recommend an evidence supplement and renewed admission review; do not silently change the original 14-ready/3-held ledger. PDF text was reviewed; screenshot retrieval was unreliable, and no complete visual review or retained byte-level snapshot is claimed.

### FP7 Cooperation: previously uncounted lead gains primary-text support

Council Decision **2006/971/EC**, CELEX **32006D0971**, is dated 19 December 2006; its English OJ citation is L 400, 30 December 2006, pp. 86-242. Annex I, Theme 3 ICT, contains substantive cognitive/learning-system and cooperative-robotics provisions. Proposed classification: `historical_lineage` / `ai_related_precursor`; proposed sectors: `research_and_innovation`, `industry_and_manufacturing`. Preserve the period-correct issuer. [Official record](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32006D0971).

Important access limitation: despite the English URL/header, the parent review received a French primary-text body. Its relevant provisions were read, but the English PDF could not be opened. This strengthens the discovery evidence without completing English-manifestation admission review. It is not included in the existing 17-candidate ledger and is not imported.

### Earlier and adjacent leads remain pending

An official EUR-Lex indexed search exposed references **COM(1977) 283**, **COM(1979) 650**, **COM(1980) 314**, **COM(1982) 287**, **COM(1982) 486**, **COM(1983) 107** and **COM(1983) 258**. Their primary texts were not substantively verified in this recheck. Decision **82/878/EEC** and **91/394/EEC** also remain access-limited. These are search leads, not accepted additions, proof of an earliest-ever AI document, or a complete historical count.

Reproducible lead method: EUR-Lex preparatory documents; English title-and-text phrase `artificial intelligence`; document-date order, oldest end of results. Also search exact references and follow ESPRIT I's cited instruments. The indexed result counts differed between cached search pages, so no total or pagination-completion claim is made. Reopen and record a live bounded search before certifying coverage. Reference-level retrieval URLs include [COM(1982) 287](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:51982DC0287) and [COM(1977) 283](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:51977DC0283); both retrieval attempts failed in this pass.

Parallel follow-up also identified unresolved [EDPS Opinion 4/2015](https://www.edps.europa.eu/data-protection/our-work/publications/opinions/towards-new-digital-ethics-data-dignity-and_en) and [Opinion 7/2015](https://www.edps.europa.eu/data-protection/our-work/publications/opinions/meeting-challenges-big-data_en) evidence. Original PDFs remained access-limited. An opinion discussing automated decisions must not automatically enter `indirect_adm_legal_context`: the approved category specifically requires an instrument materially governing automated individual decisions/profiling. Its relevance needs review, not an invented enum or an automatic inclusion. Opinion 8/2016 remains an unresolved relevance/access lead. The [WP251 official page](https://ec.europa.eu/newsroom/article29/items/612053/en) exposes a revised edition; the original October 2017 manifestation has not been independently verified, so no historical duplicate is created.

## Design-to-data gaps, in delivery order

| Gap | Current evidence | Required outcome |
| --- | --- | --- |
| Historical eligibility is approved but inactive | `schema/corpus-inventory.schema.json:53` still has minimum year 2018; `schema/record.schema.json` lacks the temporal/relevance/date-kind fields. `docs/historical-readiness.md` explicitly calls the new contract inactive. | Historical dates and evidence-backed classifications must survive canonical validation, SQLite and export. |
| Ready candidates remain outside the database | Existing historical ledger: 14 ready, 3 held, no canonical links/imports. | Review and admit the evidence-ready batch under the active historical contract; preserve all existing IDs/routes. |
| Attribution and historical types remain prospective | Active institution roles omit commissioner and official host; types/statuses omit conclusions, directive, expired and repealed. | Preserve historical institutional names and distinguish authors, rapporteurs, commissioners, adopters, publishers and hosts. |
| Tags exist, but reviewed historical evidence is not connected | Active schema already has sector and provenance vocabularies. Candidate recommendations remain outside canonical data. | Apply passage-supported tags per document; do not invent generic defaults or describe official hosting as authorship. |
| Source-period coverage is not historical | The 30 registered source-sweep rows all begin on 2018-01-01. Current coverage output aggregates family states, not the approved multidimensional matrix. | Register pre-2018 intervals and missing repositories; show searched, unsearched, inaccessible and unresolved scopes separately. |
| Expanded collection must not silently redefine the PhD sample | Existing route baseline preserves URLs, not an RP analytical subset. Mutable `corpus_tier` is not a versioned sample definition. | Preserve an explicitly reviewed RP-core ID selection separately from the growing database. |

The seven entities, six English pages, sector/origin vocabularies, stable URLs and separation of official facts from research judgments remain appropriate. The immediate issue is implementing the already-approved historical semantics and completing controlled data admissions, not rebuilding the atlas.

## Completion boundary and next deliverable

Next delivery should report actual historical records added, remaining named evidence holds, source-period gaps and corresponding necessary schema changes. Tests verify those changes before release; test repair alone must not be described as completion of historical research.

This pass added only this English audit note. It did not change canonical data, the admission ledger, generated database/export, active schema, UI, GitHub branches or the live site. Existing research drafts were preserved. No all-EU completeness claim or new publication cutoff is justified.
