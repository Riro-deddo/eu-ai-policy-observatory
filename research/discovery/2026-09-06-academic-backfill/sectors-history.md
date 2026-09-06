# v0.2 sector/history omission audit

## Scope and method

- Retrieval time: `2026-09-06T22:11:40.583Z` (UTC).
- Corpus inspected: `academic-readiness-20260906` at the supplied baseline `5ed89e1`; 187 published records. I read the current `data/documents` records and `research/corpus-inventory.json` before searching.
- Target: omitted, English, substantively AI-related official-EU documents in employment/labour, migration/asylum/border management, transport/mobility, and defence/security, with emphasis on pre-2018 precursors. Cut-off: 2026-09-04 inclusive.
- Existing tagged coverage observed: employment/labour 12 records, migration/asylum/border 5, transport/mobility 14, and defence/security 2. The candidate count is therefore not a proxy for the present sector balance.
- Duplicate check: exact and distinctive-title-fragment searches across both `data/documents` and `research/corpus-inventory.json`. None of the eight titles below matched. The existing `osha-ai-worker-management-2022` is the different EU-OSHA report *Artificial intelligence for worker management: implications for occupational safety and health* (DOI `10.2802/76354`), not candidate 2.
- Selection rule: retain only an official EU document whose title/description/body makes AI, autonomous AI-enabled systems, or algorithmic automation a substantive object and for which a positive target-sector passage can be identified. Exclude news items, events, general digital-sector material, records already present, inaccessible leads without enough official metadata, and results whose only connection is a search keyword.
- Stopping rule: stop at eight strong, distinct, evidence-ready omissions after at least one broad and one targeted official-domain query per sector, targeted pre-2018 queries, exact-title follow-ups, duplicate checks, and saturation into duplicates or weaker/non-document results. This is a bounded discovery audit, not an exhaustiveness claim about either the engines or EU holdings.

## Recommended bounded admission batch (three)

Admit candidates **1–3** as one defence/history backfill batch, in that order. They are distinct in document function (adopted parliamentary resolution; commissioned legal/human-rights study; EDA technical-policy white paper), have direct official English text/PDF URLs, and address the corpus's thinnest target sector. Their actionable locators are:

1. **2018 autonomous-weapons resolution:** CELEX `52018IP0341`; title/date header and operative points on a common EU position, meaningful human control and a prohibition on lethal autonomous weapon systems. Direct official PDF: [EUR-Lex PDF](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:52018IP0341).
2. **2013 drones/unmanned-robots study:** PDF cover/credits for `EXPO/B/DROI/2012/12` and Nils Melzer; executive summary and the sections addressing increasing autonomy, legal implications and autonomous-weapons policy. Direct official PDF: [Parliament PDF](https://www.europarl.europa.eu/RegData/etudes/etudes/join/2013/410220/EXPO-DROI_ET%282013%29410220_EN.pdf).
3. **2025 EDA trustworthiness white paper:** PDF cover (`European Defence Agency`, `Trustworthiness for AI in Defence`, `TAID WG`), p. 9 introduction and p. 11/section 2.1 AI-system definition, followed by the defence-specific legal, standards, V&V, human-factors, ethics and military-use-case sections. Direct official PDF: [EDA PDF](https://eda.europa.eu/docs/default-source/brochures/taid-white-paper-final-09052025.pdf).

**Raw-byte capture status:** the browsing layer retrieved/indexed the official texts but does not expose original bytes or hashes. A same-turn in-memory HTTPS retrieval of all three failed at TLS establishment; a `curl` fallback was denied by the execution sandbox before it ran. Therefore no file was persisted and **no SHA-256 is claimed**. The admission executor must capture each direct PDF above, verify `%PDF-`, record final URL/HTTP status/media type/byte length/SHA-256 and retain the bytes before constructing a source. This is the only remaining mechanical gate for the three-record batch; the identity, dates, roles, status, AI substance and duplicate checks are resolved below.

The other five candidates remain a follow-up queue rather than part of this bounded batch: candidate 4 needs a successful Publications Office/PDF capture after repeated 429 responses; candidates 5–7 are valid but lower priority because their sectors already have materially more coverage; candidate 8 additionally requires inspection of its PDF credit page to resolve expert-group versus DG RTD attribution. This avoids competing with the separate JRC-definitions work reported by the horizontal audit.

## Ranked candidates

### 1. European Parliament resolution of 12 September 2018 on autonomous weapon systems (2018/2752(RSP))

**Sector:** defence and security. **Confidence:** very high.

- Exact title and references: *European Parliament resolution of 12 September 2018 on autonomous weapon systems (2018/2752(RSP))*; `P8_TA(2018)0341`; CELEX `52018IP0341`; `2019/C 433/10`, OJ C 433, p. 86.
- Official URLs: [EUR-Lex text/metadata](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52018IP0341); [European Parliament procedure file](https://oeil.europarl.europa.eu/oeil/en/procedure-file?reference=2018%2F2752%28RSP%29).
- Document date proof: the act title and procedure record identify adoption/vote on **2018-09-12**. Use `document_date=2018-09-12`, kind `adoption`.
- Publication date proof: EUR-Lex identifies OJ C 433 of **2019-12-23**. Keep this separately as `publication_date=2019-12-23`; do not substitute it for the adoption date.
- Status/version: adopted European Parliament resolution; final parliamentary act, non-binding (not a draft and not legislation).
- Attribution: European Parliament is author/adopter. There is no external commissioned author.
- Positive sector evidence: the resolution calls for a common position and an international prohibition on lethal autonomous weapon systems lacking meaningful human control, and addresses human control of critical functions plus international humanitarian and human-rights law. This is directly defence-policy and autonomous-systems substantive.

### 2. Human Rights Implications of the Usage of Drones and Unmanned Robots in Warfare

**Sector:** defence and security; pre-2018 precursor. **Confidence:** very high.

- Exact title and references: *Human Rights Implications of the Usage of Drones and Unmanned Robots in Warfare*; `EXPO/B/DROI/2012/12`; PE `410.220`; May 2013.
- Official URLs: [European Parliament Think Tank record](https://www.europarl.europa.eu/thinktank/en/document/EXPO-DROI_ET%282013%29410220); [official PDF](https://www.europarl.europa.eu/RegData/etudes/etudes/join/2013/410220/EXPO-DROI_ET%282013%29410220_EN.pdf).
- Document date proof: the PDF identifies **May 2013**; the official Think Tank record supplies the exact release **2013-05-03**. If the schema requires a full canonical date, use `document_date=2013-05-03`, kind `publication`, and preserve `2013-05` as the internal issue month rather than pretending the PDF carries a day.
- Publication date proof: official Think Tank record, **2013-05-03**.
- Status/version: final commissioned study, non-binding; not an adopted Parliament position.
- Attribution: **Nils Melzer** is the external study author. The European Parliament Directorate-General for External Policies commissioned/published the work and must not be represented as the personal author.
- Positive sector evidence: the study examines drones and unmanned robots in warfare, increasing operational autonomy, the resulting legal/human-rights implications, and EU policy options concerning autonomous weapons. It is a clear historical precursor to later military-AI governance.

### 3. WHITEPAPER: Trustworthiness for Artificial Intelligence in Defence

**Sector:** defence and security. **Confidence:** high.

- Exact title/reference: official listing title *WHITEPAPER: Trustworthiness for Artificial Intelligence in Defence*; PDF cover short title *Trustworthiness for AI in Defence*; `TAID WG`.
- Official URLs: [EDA thematic-policy listing](https://eda.europa.eu/publications-and-data/thematic-policy-reports); [official PDF](https://eda.europa.eu/docs/default-source/brochures/taid-white-paper-final-09052025.pdf).
- Document date proof: the PDF is a final 2025 white paper but the indexed content does not establish a trustworthy day from within the document. Use the official publication date as an explicit fallback: `document_date=2025-05-12`, kind `publication`; do **not** infer 9 May solely from the filename `09052025`.
- Publication date proof: EDA's official thematic-policy list says **12 May 2025**.
- Status/version: final white paper/starting reference, advisory and expressly without Member-State commitment or obligation; not a draft, adoption, or binding rule.
- Attribution: European Defence Agency / its Trustworthiness for AI in Defence Working Group (`TAID WG`) is the corporate authoring body. Do not turn referenced Commission standardisation activity into Commission authorship.
- Positive sector evidence: the paper is expressly about engineered AI systems for defence, including defence-specific taxonomy, law, standards, testing/validation/verification, human factors, ethics, impact, military use cases, and recommendations to Member States, defence ministries, and industry.

### 4. Opportunities and challenges for the use of artificial intelligence in border control, migration and security. Volume 1, Main report

**Sector:** migration, asylum and border management. **Confidence:** high.

- Exact title and references: *Opportunities and challenges for the use of artificial intelligence in border control, migration and security. Volume 1, Main report*; ISBN `978-92-76-18447-8`; DOI `10.2837/923610`; catalogue `DR-02-20-303-EN-N`.
- Official URL: [Publications Office record](https://op.europa.eu/en/publication-detail/-/publication/c8823cd1-a152-11ea-9d2d-01aa75ed71a1/language-en).
- Document date proof: the report identifies **May 2020**, without a verified internal day. If a full date is mandatory, use `document_date=2020-05-28`, kind `publication`, and preserve May 2020 separately as issue month.
- Publication date proof: Publications Office release **2020-05-28**.
- Status/version: final Volume 1 main report, commissioned research and non-binding; not a draft policy or adopted act.
- Attribution: the report says **“Written by Deloitte”**. DG Migration and Home Affairs / European Commission is the commissioning, corporate-metadata, publishing/hosting institution; do not flatten commissioner and author into one role.
- Positive sector evidence: the report examines how AI may be used across border-control, migration and security processes, discusses bias, transparency, privacy and accountability, and develops a roadmap for DG HOME. The sector connection is explicit, not inferred from a stray keyword.

### 5. People, machines, robots and skills

**Sector:** employment and labour; pre-2018 precursor. **Confidence:** high.

- Exact title and references: *People, machines, robots and skills*; Cedefop briefing note; DOI `10.2801/057353`; ISBN `978-92-896-2316-2`; catalogue `TI-BB-17-003-EN-N`; ISSN `1831-2411`.
- Official URLs: [Publications Office record](https://op.europa.eu/en/publication-detail/-/publication/973495f4-ad64-11e7-837e-01aa75ed71a1/language-en); [Cedefop PDF](https://www.cedefop.europa.eu/files/9121_en.pdf).
- Document date proof: the PDF masthead states **July 2017**. Preserve `2017-07` as the issue date. If the schema requires a day, use the separately evidenced publication day as fallback rather than inventing a July day.
- Publication date proof: Publications Office release **2018-03-06**. Recommended full canonical fallback: `document_date=2018-03-06`, kind `publication`, with the July 2017 issue month retained in additional dates.
- Status/version: final briefing note, analytical/non-binding; not a draft or adopted act.
- Attribution: Cedefop is the institutional author/publisher; no external commissioner-author split is evidenced in the inspected official records.
- Positive sector evidence: the note directly analyses technological unemployment, automation-driven job substitution/creation/transformation, Cedefop skills-and-jobs survey evidence, and the skills implications of machines and robots.

### 6. Advanced robotics, artificial intelligence and the automation of tasks: definitions, uses, policies and strategies and Occupational Safety and Health

**Sector:** employment and labour. **Confidence:** high.

- Exact title and references: title as above; ISBN `978-92-9479-672-1`; DOI `10.2802/681779`; catalogue `TE-RO-22-005-EN-N`.
- Official URLs: [EU-OSHA publication page](https://osha.europa.eu/en/publications/advanced-robotics-artificial-intelligence-and-automation-tasks-definitions-uses-policies-and-strategies-and-occupational-safety-and-health); [official PDF](https://osha.europa.eu/sites/default/files/2022-04/Advanced%20robotics_AI_based%20systems.pdf).
- Document date proof: PDF copyright/year **2022**; no independently verified internal day. Recommended exact fallback: `document_date=2022-04-26`, kind `publication`.
- Publication date proof: publication page says **26/04/2022**. A separate EU-OSHA highlight dated 29 April is a news item and is not the report publication date.
- Status/version: final research report, non-binding; not a draft policy or adopted measure.
- Attribution: Patricia Helen Rosen, Eva Heinold, Elena Fries-Tersch, Phoebe Moore, and Sascha Wischniewski are the credited report authors. EU-OSHA commissioned/published the report; its project managers Ioannis Anyfantis, Annick Starren, and Emmanuelle Brun are not bibliographic authors.
- Positive sector evidence: the report addresses how AI and advanced robotics transform human labour, task automation, workplace use and sector distribution, and occupational-safety-and-health policy and strategy.

### 7. AI Watch: AI Uptake in Smart Mobility

**Sector:** transport and mobility. **Confidence:** very high.

- Exact title and references: *AI Watch: AI Uptake in Smart Mobility* (Publications Office display punctuation/case differs); JRC `126302`; EUR `30821 EN`; ISBN `978-92-76-41403-2`; DOI `10.2760/879190`; catalogue `KJ-NA-30821-EN-N`; ISSN `1831-9424`.
- Official URLs: [AI Watch publication page](https://ai-watch.ec.europa.eu/publications/ai-watch-ai-uptake-smart-mobility_en); [Publications Office record](https://op.europa.eu/en/publication-detail/-/publication/3b2bb4f5-1699-11ec-b4fe-01aa75ed71a1/language-en).
- Document date proof: report citation/copyright identifies **2021**; use exact official publication as fallback: `document_date=2021-09-15`, kind `publication`.
- Publication date proof: AI Watch and Publications Office give **2021-09-15**.
- Status/version: final JRC technical report, analytical/non-binding; not a draft or adopted measure.
- Attribution: S. De Nigris, J. Hradec, M. Craglia, and D. Nepelski are the personal authors; the Joint Research Centre is the institutional authoring/publishing service. Do not label the named authors as commissioners.
- Positive sector evidence: the report studies AI uptake in mobility, including traffic-flow management, road safety, mobility access, energy/pollution, data sharing and protection, standardisation, and algorithmic fairness/transparency.

### 8. Ethics of connected and automated vehicles: Recommendations on road safety, privacy, fairness, explainability and responsibility

**Sector:** transport and mobility. **Confidence:** medium-high (PDF credit-page check required before final attribution).

- Exact title and references: *Ethics of connected and automated vehicles: Recommendations on road safety, privacy, fairness, explainability and responsibility*; ISBN `978-92-76-17867-5`; DOI `10.2777/035239`; catalogue `KI-03-20-238-EN-N`.
- Official URL: [Publications Office record](https://op.europa.eu/en/publication-detail/-/publication/89624e2c-f98c-11ea-b44f-01aa75ed71a1/language-en/).
- Document date proof: report year **2020**; no verified internal day. Recommended exact fallback: `document_date=2020-09-17`, kind `publication`.
- Publication date proof: Publications Office release **2020-09-17**.
- Status/version: final recommendations report containing 20 recommendations; non-binding and not an adopted Commission measure.
- Attribution: the Commission established an **independent Expert Group on the Ethics of Connected and Automated Vehicles**, which produced the report. Publications Office exposes DG Research and Innovation as a corporate author/record institution. Before admission, check the PDF credit page and preserve the expert group as the substantive author and DG RTD/Commission as commissioner/publisher unless the credits explicitly say otherwise.
- Positive sector evidence: the report directly evaluates connected and automated vehicles and AI-related recommendations concerning road safety, privacy, fairness, explainability and responsibility, alongside accessibility and emissions considerations.

## Backfill order and cautions

The order above prioritises the largest undercoverage and historical value, then documentary specificity. Candidates 1–7 are ready for source capture subject to the normal retained-byte and evidence-locator workflow. Candidate 8 should remain one gate behind them until its PDF credit page resolves the expert-group/DG RTD attribution precisely. Date precision must follow the notes above: a month-only issue date is not evidence for an invented day, and an exact repository release can be used as a clearly labelled publication fallback. All eight are dated before the 2026-09-04 cut-off.

## Exact search and navigation log

Searches were restricted to official EU domains. Exact queries, in execution order:

1. `site:europa.eu artificial intelligence employment labour report EU-OSHA PDF`
2. `site:europa.eu artificial intelligence migration border report PDF EU`
3. `site:europa.eu artificial intelligence transport mobility report PDF European Commission`
4. `site:europa.eu artificial intelligence defence autonomous weapons report PDF European Parliament`
5. `site:osha.europa.eu/en/publications artificial intelligence worker management report 2022`
6. `site:osha.europa.eu/en/publications "advanced robotics and AI-based systems"`
7. `site:osha.europa.eu/en/publications "AI-based worker management"`
8. `site:op.europa.eu artificial intelligence labour market employment report European Commission 2021`
9. `site:op.europa.eu "Ethics of connected and automated vehicles"`
10. `site:op.europa.eu "AI Uptake in Smart Mobility"`
11. `site:publications.jrc.ec.europa.eu "Artificial Intelligence in Automated Driving"`
12. `site:publications.jrc.ec.europa.eu "Artificial Intelligence in Autonomous Vehicles"`
13. `site:europarl.europa.eu/doceo/document/TA-8-2018 autonomous weapon systems 12 September 2018`
14. `site:eur-lex.europa.eu autonomous weapon systems European Parliament resolution 12 September 2018`
15. `site:eda.europa.eu artificial intelligence defence report PDF ethics`
16. `site:op.europa.eu artificial intelligence defence military report European Defence Agency`
17. `site:op.europa.eu artificial intelligence employment 2017 European Union report`
18. `site:europarl.europa.eu/RegData/etudes 2013 drones unmanned robots warfare human rights`
19. `site:op.europa.eu autonomous vehicles artificial intelligence 2017 European Commission report`
20. `site:op.europa.eu artificial intelligence border migration 2017 EU report`
21. `"Opportunities and challenges for the use of artificial intelligence in border control" Deloitte commissioned by European Commission PDF`
22. `"DR-02-20-303-EN-N" PDF`
23. `"AI watch, AI uptake in smart mobility" "2021" "European Commission" PDF authors`
24. `"People, machines, robots and skills" Cedefop PDF 2017`
25. `site:ai-watch.ec.europa.eu/publications "Artificial Intelligence in Automated Driving"`
26. `site:ai-watch.ec.europa.eu/publications "Artificial Intelligence in Autonomous Vehicles"`
27. `site:op.europa.eu "Artificial intelligence in automated driving" JRC127189`
28. `site:op.europa.eu "Trustworthy autonomous vehicles" JRC128170`
29. `"Advanced robotics, artificial intelligence and the automation of tasks" authors commissioned EU-OSHA`
30. `"Advanced robotics_AI_based systems.pdf" EU-OSHA authors`
31. `"Advanced robotics, artificial intelligence and the automation of tasks" ISBN DOI`
32. `site:op.europa.eu "Advanced robotics, artificial intelligence and the automation of tasks"`
33. `"EXPO/B/DROI/2012/12" "requested by" "European Parliament" Nils Melzer`
34. `"Human rights implications of the usage of drones" "This study was requested by"`
35. `site:op.europa.eu "Human rights implications of the usage of drones and unmanned robots in warfare"`
36. `site:europarl.europa.eu/thinktank "Human Rights Implications" "03-05-2013"`
37. `site:eda.europa.eu "Trustworthiness for AI in Defence"`
38. `site:op.europa.eu "Trustworthiness for AI in Defence"`
39. `site:eda.europa.eu "Action Plan on Autonomous Systems"`
40. `site:eda.europa.eu/publications-and-data/publications "WHITEPAPER: Trustworthiness for Artificial Intelligence in Defence"`
41. `site:eda.europa.eu/publications-and-data/thematic-policy-reports "Trustworthiness for Artificial Intelligence in Defence"`
42. `site:eda.europa.eu/docs/default-source/brochures/taid-white-paper-final-09052025.pdf "12 May 2025"`

Navigation/result review included the official Publications Office records for the border/migration report, smart-mobility report, connected/automated-vehicle ethics report, Cedefop note, and related autonomous-driving leads; EU-OSHA publication/highlight pages and report PDF; AI Watch publication pages; EUR-Lex and Parliament procedure/Think Tank records; the Parliament-hosted 2013 study PDF; and EDA's thematic-policy list, autonomous-systems/APAS pages, and TAID PDF. Related results evaluated but not selected included the already-held EU-OSHA worker-management report, JRC autonomous-driving reports that would overconcentrate the capped list in transport, EDA's 2024 Action Plan on Autonomous Systems (broader autonomy and less directly AI-centred than TAID), news/event pages, post-cut-off pages, and general digital reports lacking a positive target-sector passage.

## Access limitations and failures

- The first local inventory lookup treated `research/corpus-inventory` as a directory and failed; it was corrected to the actual `research/corpus-inventory.json` file.
- The Publications Office border/migration record intermittently returned HTTP 429, and several Publications Office opens returned cache-miss/429 responses. Indexed official-result metadata and the official record URLs were retained; no third-party page was used as decisive evidence.
- The Parliament Think Tank page intermittently produced a decoding/robots error and an EP page displayed a JavaScript-disabled shell. The official Parliament PDF and indexed official metadata supplied the study evidence.
- The EU-OSHA PDF click timed out once (HTTP 400 in the browsing layer); the official publication page and indexed official PDF content still exposed title, date, references, credits and scope.
- Search engines expose incomplete and unstable indexes. The bounded query set and saturation rule above support discovery of these omissions only; they do not establish that no other eligible EU document exists.

## Dated correction addendum — 2026-09-06T22:16:12Z

This addendum preserves the original audit text above as an evidence trail and supersedes two claims with counterevidence from the parent's direct document inspection:

1. **2018 Parliament resolution OJ item:** the correct Official Journal item is **`2019/C 433/11`**, not `2019/C 433/10`. CELEX `52018IP0341`, the adoption date 2018-09-12, and OJ publication date 2019-12-23 are unchanged. Any admission record must use `/11`.
2. **2025 EDA TAID white paper:** direct PDF inspection resolves what the browsing-only audit left uncertain. Page 2 states publication **09/05/2025** (9 May 2025) and **version 1.0**; the separate EDA listing date remains 12 May 2025 and should be modelled as public release, not document date. Page 8 credits **16 personal authors** and contains version-history evidence for **1.1**. Therefore the earlier statement that EDA/TAID WG alone was the corporate authoring body is insufficient: the 16 named people must be preserved as bibliographic authors, with EDA/TAID WG represented in the appropriate institutional relationship. The page-2 version label and page-8 version-history entry must both be retained and reconciled against the captured artifact rather than inferred from its filename.
