# Historical Scope and Evidence-Based Coverage Design

**Date:** 5 September 2026

**Status:** Scope direction approved; written specification awaiting final review

**Project:** EU AI Policy Observatory

**Implementation status:** Not implemented by this document

## 1. Decision and purpose

Maintain one English-language database and one static research atlas, with explicitly distinguishable historical and contemporary collections. The year 2018 remains an important analytical boundary, but no longer excludes earlier eligible documents from the database.

The user approved this direction on 5 September 2026 following the historical-scope and design audit. This specification records that direction and the detailed rules for review before implementation planning. It does not approve individual candidate records, certify a completed sweep, advance any verification cutoff or authorise a deployment.

The amendment changes the temporal eligibility rule and coverage-claim requirements of the 4 September comprehensive-corpus design. Its other inclusion rules, English-only requirement, seven-entity structure, provenance requirements and stable public routes remain in place unless explicitly refined below.

## 2. Invariants and non-goals

- Keep the seven canonical entities: `policy`, `document`, `event`, `concept`, `institution`, `relationship` and `source`.
- Preserve existing document IDs, slugs and URLs. Correct a record through a documented revision, not deletion and recreation under a new identity.
- Keep one canonical dataset, one generated SQLite database and one public JSON export. Collection labels are fields, not separate databases or an eighth entity.
- Keep the six English pages: Home, Policy Map, Timeline, Corpus, Methodology and About. No unrelated visual redesign is included.
- Keep official facts distinct from researcher classifications, including temporal/relevance groupings, sector tags, corpus tiers and policy membership.
- Preserve the RP-oriented core as an explicitly identified, reproducible subset. Database expansion does not automatically enlarge the PhD's analytical sample or research questions.
- Do not add LLM experiments, interpretation coding, a backend, accounts, a second-language public site or a new hosting service.
- Do not describe European research programmes from the 1980s as early versions of the AI Act.

## 3. Temporal collections

Every published document receives exactly one `temporal_collection` classification, derived from its verified `document_date` under section 5.

| Value | English label | Assignment |
| --- | --- | --- |
| `historical_lineage` | Historical lineage | Document date before 1 January 2018 |
| `contemporary_eu_ai_policy` | Contemporary EU AI policy | Document date on or after 1 January 2018 and no later than the applicable verified cutoff |

Both collections use the same evidence, identity and publication gates. A historical label does not excuse weaker verification.

The initially examined historical anchors span 1984–2017. This is a starting set for backfill, not a claim of complete coverage across those years and not a permanent lower boundary. A verified, substantively relevant earlier document is eligible under the same rules. Its source and newly examined period must be registered; discovering it does not establish coverage of the intervening years.

The current dataset's cutoff remains 4 September 2026 until a separate audit supports a change. Writing this specification on 5 September does not advance it. A single recent record verification must not advance the cutoff of older, unaudited source searches.

## 4. Relevance boundary

Temporal collection and substantive relevance are separate dimensions. Every published document receives exactly one primary `relevance_class`:

| Value | Inclusion test |
| --- | --- |
| `direct_ai_substantive` | AI is an explicit substantive policy subject, regulatory object or material sectoral issue. A dedicated policy passage can qualify even if the title is broader. |
| `ai_related_precursor` | Substantial provisions address expert systems, cognitive or learning systems, intelligent robotics or autonomous systems with a documented connection to the AI policy history being collected. Generic computing, digitisation or automation alone does not qualify. |
| `indirect_adm_legal_context` | An official legal instrument materially governs automated individual decisions or profiling and has a documented relationship to an included AI policy question or document, without itself satisfying either direct category. |

Use the first applicable category in the table. Secondary topics belong in sector/concept tags and the inclusion rationale, not contradictory primary classifications.

Every classification requires a cited passage or official section/page locator, an explanatory inclusion rationale, named reviewer and review date. A keyword hit or familiar title alone is insufficient. These judgments remain editorial, not official EU metadata.

Indirect automated-decision legal context is a visibly separate subset. Its records remain searchable, but their counts must not inflate the count of direct AI documents. GDPR does not qualify every data-protection document by association. The same restraint applies to general digital-market, industrial and research legislation.

Formal official publication remains the eligibility threshold, not final legal adoption. A verifiable official draft or proposal can qualify with explicit status; a planned or unissued draft cannot. An already published act with a future application date is a real document, but its future milestone must not be presented as an event that has already occurred.

## 5. Dates, publication and identity

### 5.1 Date meanings

Retain separate `document_date` and `publication_date` fields. Add an explicit `document_date_kind` with one of these meanings:

- `official_act_date`: the date identified in the official legal act's heading or document metadata; supporting evidence explains whether this is a signature or adoption date;
- `institutional_adoption`: the evidenced adoption date of a resolution, opinion or conclusions;
- `document_issue`: the issue date on a communication, report, study, draft or other independently citable version;
- `publication`: an evidenced official publication date used when no more specific document/issue date is available; or
- `consolidation`: the officially identified date of a consolidated version.

Apply the kind appropriate to the document type, not whichever date produces the desired collection assignment. For a study or report, use its stated issue date when available; otherwise use the official publication date and identify that fallback. Every kind and date must have evidence from the cited official record or text. If a required exact date cannot be established, keep the candidate pending; never substitute 1 January for an unknown day.

`publication_date` identifies the official publication represented by the primary cited source for that version. Preserve a separately evidenced first official publication or OJ publication date as an additional explicitly labelled date when these differ; do not overwrite either fact. Retrieval and last-verification timestamps are separate from all publication dates.

The primary cited official publication must exist on or before the cutoff for an item to enter that release. The verification itself may take place later: retain its actual timestamp rather than backdating it to the publication cutoff. A document's adoption/issue date alone does not prove public availability. A later website modification date or current retrieval timestamp does not change the document's collection.

Application, entry into force, withdrawal and comparable regulatory milestones remain `event` records with their own evidence. Completion of a funded programme does not, by itself, establish repeal of its legal basis.

### 5.2 Later manifestations and versions

A resolution adopted in 2017 and reproduced in the OJ in 2018 remains one historical document when both publications represent the same version. Record the distinct dates and source manifestations; do not manufacture a contemporary duplicate. A substantively revised, independently citable version issued after 2018 is a separate contemporary document with an evidenced version relationship to its predecessor.

An annex must be independently citable or contain materially distinct research content to justify its own document record. Public versions and attachments require an appropriate, evidenced parent/version relationship. Where identity or the necessary relationship cannot be established, the unresolved candidate remains pending rather than acquiring a guessed link.

## 6. Institutional scope and provenance

Include relevant predecessor European Communities institutions as well as the EU institutions, bodies, agencies and recognised expert groups already within scope. Preserve the official issuing name applicable to the document's period. Historical institution records or time-qualified names may link to successor institutions only when that relationship is evidenced; use modern discovery metadata without silently rewriting the original issuer.

The EU-named provenance vocabulary remains stable for compatibility, but its definitions explicitly encompass eligible Community predecessors. The exact historical institution name remains visible alongside the tag, so the tag cannot imply that the present-day EU institution issued the older act.

Preserve these as distinct facts:

- author or authors;
- adopter or proposer where applicable;
- commissioning institution, including a canonical `commissioner` role;
- official publisher; and
- official host of the cited manifestation.

An institution's adoption, contribution, hosting or publication does not alone establish authorship. Externally authored commissioned studies need named bibliographic author credits and the commissioning institution; individual external authors must not be misrepresented as EU institutions. These credits can be document fields without introducing a new top-level entity.

The AI Office's institutional involvement does not, by itself, justify `eu_commissioned_external`. Neither `general_cross_sector` nor an origin tag may be assigned as a substitute for an uncompleted classification review. Preserve evidence-backed existing tags when migrating records.

Historical backfill must be representable without distorting document types or validity. Add `directive` and `conclusions` to the document-type vocabulary, and evidenced `repealed` and `expired` distinctions to legal status. Use `expired` only where the instrument's validity ended; a programme's completion alone is not enough. Existing types/statuses remain valid, subject to their documented semantics.

## 7. Discovery and candidate decisions

Register the broader source universe before claiming coverage: EUR-Lex/Cellar, Publications Office catalogues, Parliament registers and studies, Council and European Council repositories, Commission departments and expert groups, CURIA, and relevant agency/body publication catalogues. This includes sectoral bodies such as FRA, ENISA and EMA when their publications satisfy the boundary. A source missing from the registry is a coverage gap, not an implicit zero-result search.

For each search retain its institution/source, period, language, document-type and sector scope, exact query or reproducible navigation method, search date, result/pagination evidence where available, reviewer, candidate decisions and access limitations. Distinguish an observed zero-result search from an unstarted or inaccessible search.

The registry continues to use `not_started`, `in_progress`, `reviewed`, `gap_found` and `recheck_due`. A `reviewed` search says the recorded bounded method was completed; it does not certify every document ever issued by that institution.

Candidate decisions retain these meanings:

- `included`: eligibility, identity, metadata and evidence are verified, with a linked document record;
- `merged`: the same version is already represented, with an explicit merge target;
- `excluded`: evidence establishes a reasoned boundary failure, not merely an inability to retrieve or verify the item; and
- `pending`: identity, official availability, required metadata, relevance or another publication requirement remains unresolved.

Keep pending candidate content out of the public corpus but report aggregate pending counts and coverage limitations. Inaccessibility must not be converted into exclusion merely to produce zero pending items. Reconsider old exclusions under the revised boundary, retaining the old decision/reason in the review history rather than erasing it.

## 8. Coverage and public claims

### 8.1 Coverage matrix

Generate coverage by source family, institution/body, audited date interval, document type and sector, with the temporal collection and relevance subset visible. For sources spanning many sectors, use documented applicability rather than treating an empty sector scope as coverage of every sector.

Expose unstarted, partial, gapped and recheck-due work. An explicitly documented not-applicable matrix cell is different from a zero-result reviewed cell and from a missing cell; it does not change the source-status vocabulary. Include discovered/included/merged/excluded/pending counts with unambiguous denominators. Multi-tag sector totals must not be summed as if they were unique-document totals.

Publish an incomplete matrix with honest statuses. Do not wait for completeness before making gaps visible. An initial historical backfill and a contemporary source sweep have separate coverage evidence and cannot inherit each other's completed status.

### 8.2 Claims and release gate

The default project description is:

> An expanding corpus of official EU and European Communities AI-related documents. Verification dates and known coverage gaps are documented.

The blanket sentence beginning “Comprehensive within the documented inclusion boundary” is no longer required and must not be generated from a cutoff date alone. Document counts, all-reviewed registered-family counts and passing software tests are not evidence of EU-wide completeness.

A bounded audit may be described as completed only when its named source universe, period and method are published, every required search is reviewed through that cutoff, there are no unresolved candidates or known gaps within that bounded scope, and identity/version, procedure-chain and reverse-citation checks have passed. This is a statement about the named audit, not about all EU documents.

Other sources may remain incomplete. Their status must be disclosed alongside the completed bounded audit, and the overall collection remains described as expanding. A newly found omission or unresolved source failure changes the relevant status to `gap_found` or `recheck_due` and removes the completed-audit claim until reverified. Do not suppress the known gap by changing an inventory decision without evidence.

Every public coverage view shows the relevant cutoff, audited interval, scope and pending count. The latest record verification date must be labelled as such, not presented as the completion date of the whole corpus.

## 9. Atlas behaviour and research subsets

Add collection and relevance filters to the existing Corpus controls. The default remains Principal documents across both temporal collections; the active relevance scope and number of contextual records must be clear. Visitors can include all versions/attachments and combine the new filters with existing sector, provenance, institution and date filters. Counts describe the active filters, not a claimed total EU universe.

Document pages display the temporal/relevance assignments and their evidence/rationale under Research classifications. Keep `record_level` and editorial `version_status` outside Official metadata. Official legal status, source dates and named institutional roles remain separately labelled.

Timeline permits both historical and contemporary records, identifies which date it plots, and preserves the document/event distinction. Policy Map derives links only from recorded relationships; historical proximity or membership in one collection never creates an official legal relationship. Preserve its legend, keyboard access and non-JavaScript relationship list.

Methodology reports the revised boundary, predecessor institutions, relevance tests, publication/date rules and coverage matrix. Home and About distinguish the current collection from its coverage ambition. Keep existing URLs and English labels stable wherever the new classification does not require a new label.

Retain the research core as a versioned list of document IDs or equivalent reproducible selection. The wider corpus must not silently redefine this subset when historical or sectoral documents are added. No research coding or LLM comparison protocol is implemented by this amendment.

## 10. Work packages after written approval

This is a design sequence, not permission to execute all packages in this documentation turn.

1. Correct coverage wording and its eligibility logic; expose existing known gaps and review pending/excluded decisions.
2. Implement temporal/relevance/date and provenance semantics across schema, validators, SQLite, export, documentation and UI. Preserve reviewed data and routes; repair evidence-backed version/attachment links. Stage any record failing the new requirements for review rather than inventing values or silently dropping a live URL.
3. Register missing institutional and historical source scopes and generate an honest coverage matrix.
4. Review and import the strongest historical anchors and missing contemporary agency/sector documents through the same publication gate.
5. Continue bounded source/year searches, deduplication and reverse-citation checks, updating coverage only on evidence.

Do not rerun the old automatic classification migration over reviewed records. Plan a reviewed, testable migration with before/after diffs and an explicit path for unresolved records. Preservation of URLs is an acceptance requirement; any necessary withdrawal of a public record requires an explicit review decision and a transparent retained record notice rather than silent deletion.

Snapshots, when collected, must represent actual retrieved bytes with timestamp, format and checksum. A metadata record or source URL must never be described as a retained full-text copy. Retrieval failure remains visible in the inventory.

## 11. Acceptance criteria for later implementation

- A pre-2018 eligible document can be published without changing the seven-entity model.
- A verified pre-1984 candidate is not rejected solely because it predates the initial anchor.
- A 2017 adopted document with a 2018 OJ manifestation remains historical and is not duplicated; a distinct later revision gets its own date and relationship.
- Retrieval and application dates cannot silently replace document/publication dates or move a document between collections.
- Explicitly published drafts remain eligible, while unissued/future documents and unresolved candidates do not enter public exports.
- Historical institutional names, external author credits, commissioner, publisher and host survive generation and display distinctly.
- Unknown classifications fail the publication gate rather than receiving cross-sector or authored-origin defaults.
- Every published version/attachment has its required evidenced relationship, and all published relationships meet the official-evidence rule regardless of official/analytical basis.
- Any pending candidate, relevant known gap or unreviewed required source prevents a completed-audit claim for that scope, while its incomplete matrix remains public.
- Contextual and multi-tag counts have explicit denominators; an unregistered source or unaudited period is never counted as reviewed.
- The RP-oriented core, existing IDs/URLs, principal/all controls and all-English output are preserved.
- Relevant Python and web tests, deterministic generation, production scanning, desktop/mobile keyboard and accessibility checks, and deployment checks pass before a later release is declared ready.

Documentation approval and software/data implementation are separate completion states. This file alone satisfies none of the implementation acceptance tests.

## 12. Evidence anchors and limits

- [Council Decision 84/130/EEC, ESPRIT](https://eur-lex.europa.eu/eli/dec/1984/130/oj/eng): Annex section 3 contains substantive expert-system, knowledge-representation and learning provisions. It is the earliest substantial programme instrument examined in this bounded audit, not a proven first European AI document.
- [Council Decision 88/279/EEC, Esprit](https://eur-lex.europa.eu/eli/dec/1988/279/oj/eng/pdf): Annex II, basic research, expressly includes artificial intelligence and cognitive science.
- [European Council conclusions, 19 October 2017, EUCO 14/17](https://www.consilium.europa.eu/media/21620/19-euco-final-conclusions-en.pdf): paragraph 11 requests a European AI approach by early 2018.
- [2017 Robotics resolution, later OJ publication](https://op.europa.eu/en/publication-detail/-/publication/13fd56d0-8a65-11e8-ac6a-01aa75ed71a1/language-en): an identity/date example, not a reason to count two policy documents.

The audit found historical candidates and contemporary omissions, not a complete inventory. Further screening of earlier cited instruments, work programmes, agency catalogues and procedural versions remains necessary. Candidate publication requires individual evidence review even when the title appears in an audit report.
