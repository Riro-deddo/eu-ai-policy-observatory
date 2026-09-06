# V0.2 bounded health and finance omission search

Researcher: delegated AI-assisted read-only review. Search/retrieval window: 2026-09-06 22:08:02–22:10:33 UTC (clock observations bracketing the principal search batches; not fabricated per-document timestamps). Cutoff: official publication no later than 2026-09-04. English documents only. Report written after this retrieval window. No canonical data, publication, or external account was changed.

## Scope and baseline

The inspected checkout is `academic-readiness-20260906`, HEAD `5ed89e1`. There are 187 canonical document JSON files. The inspected `research/corpus-inventory.json` has 187 included, 12 pending, 18 merged and 10 excluded entries. I read its health/financial-services and relevant institutional entries, then searched canonical documents and inventory for the candidate titles/references. Each ranked work below is absent from that baseline; absence is not a claim about every other worktree.

This is a bounded purposive gap search, **not an exhaustive institutional bibliography**. It prioritises substantive guidance, consultations, institutional research and discrete AI reports. Official-site search results were discovery material. Successful full-text retrieval is distinguished below from search-index evidence and failed direct requests. None of the retrieval dates or generic page-update dates is offered as a document date.

## Ranked candidates

### 1. Joint AIB/MDCG medical-device AI FAQ — high confidence

- Exact PDF title: **Interplay between the Medical Devices Regulation (MDR) & In vitro Diagnostic Medical Devices Regulation (IVDR) and the Artificial Intelligence Act (AIA)**. References: **AIB 2025-1; MDCG 2025-6**. The Commission catalogue adds “FAQ” to its display title.
- [Official 27-page PDF](https://health.ec.europa.eu/document/download/b78a17d7-e3cd-4943-851d-e02a2f22bbb4_en). Successfully opened; cover and substantive text retrieved.
- [Commission publication announcement](https://health.ec.europa.eu/latest-updates/mdcg-2025-6-faq-interplay-between-medical-devices-regulation-vitro-diagnostic-medical-devices-2025-06-19_en). Successfully opened. Its publication-date field and linked English-file stamp both give **19 June 2025**.
- Issue/date proof: PDF p.1 gives **June 2025**, not an exact day. Version/status proof: p.1 says both AIB and MDCG endorsed the document; it also explicitly disclaims Commission-document status and legal binding effect. Record as endorsed non-binding joint-board guidance, not a Commission-authored act, and do not convert June to 1 June.
- Source authority: Artificial Intelligence Board and Medical Device Coordination Group, jointly; DG SANTE is official host/publisher of the catalogue announcement. The catalogue’s author field refers to that announcement and does not override the PDF’s explicit attribution.
- AI/sector evidence: PDF pp.2–3 introduction concerns complementary MDR/IVDR/AI Act application; p.5 questions 1–2 assess AI medical software and high-risk qualification; pp.7–11 cover lifecycle, risk management and data governance; contents p.4 identify human oversight, conformity assessment and post-market monitoring. Strong `health`; `industry_and_manufacturing` is supportable for manufacturer obligations, but should not be added merely because manufacturers are addressed.
- Duplication check: no MDCG/AIB reference or matching title in inventory/canonical files. Distinct from the admitted 2026 horizontal high-risk draft guidance and from EMA medicine-lifecycle reflection papers.

### 2. EMA/HMA LLM principles — high identity/content confidence; publication corroboration partly indexed

- Exact title: **Guiding principles on the use of large language models in regulatory science and for medicines regulatory activities**. No document-number reference found in the inspected cover.
- [Official 10-page PDF](https://www.ema.europa.eu/en/documents/other/guiding-principles-use-large-language-models-regulatory-science-medicines-regulatory-activities_en.pdf). Successfully opened. PDF p.1 prints **29 August 2024**: exact document issue date, not adoption/publication date.
- [EMA release announcement](https://www.ema.europa.eu/en/news/harnessing-ai-medicines-regulation-use-large-language-models-llms); direct open later returned 429. [EMA data-regulation catalogue](https://www.ema.europa.eu/en/about-us/how-we-work/data-regulation-big-data-other-sources) search-index result lists that exact announcement with **05/09/2024**. The official AI-topic page independently says the first version was published in September 2024. Therefore 5 September is a supported release candidate, but preserve the indexed-vs-successful-open limitation before final admission.
- Source authority: PDF credits European Medicines Agency and displays EMA/HMA identities; announcement explicitly names joint EMA/HMA publication. Do not treat the wider EMRN as a named bibliographic author without additional evidence.
- Version/status: publicly issued guiding principles, described by EMA as a living document. No numbered version or formal adoption date established. The retrieved PDF still carries the August 2024 cover.
- AI/sector evidence: PDF p.2 scope targets safe and responsible LLM use by regulatory authorities; pp.6–9 operational user principles; p.10 agency-level recommendations. Strong `health` and `public_administration`; `research_and_innovation` can be grounded in regulatory-science scope. This is an independent implementation deliverable, not the multiannual AI workplan already included.

### 3. EMA/FDA good AI practice in drug development — high work/date confidence; EMA manifestation retrieval incomplete

- Exact title: **Guiding principles of good AI practice in drug development**. No numerical official reference established.
- [EMA official PDF](https://www.ema.europa.eu/en/documents/other/guiding-principles-good-ai-practice-drug-development_en.pdf) was discovered in official search but repeated direct requests returned 429. [FDA co-author’s official two-page PDF](https://www.fda.gov/media/189581/download) was successfully opened in full; it uses title-case and US spelling.
- Issue proof: FDA PDF p.1 gives **January 2026**. Do not manufacture an exact issue day.
- Publication proof: [FDA’s official release bulletin](https://content.govdelivery.com/accounts/USFDA/bulletins/4045c84), successfully opened, has **14 January 2026**, 10:01 AM EST, and states that FDA and EMA are releasing the joint principles that day. [EMA AI-topic page](https://www.ema.europa.eu/en/about-us/how-we-work/data-regulation-big-data-other-sources/artificial-intelligence), indexed official result, has a document-specific “First published: 14/01/2026” entry.
- Source authority: jointly developed EMA/FDA principles; FDA is an official co-author source, not an unrelated mirror. Record EMA/FDA joint provenance rather than FDA-only or Commission authorship. Do not assert byte-equivalence of the two agency manifestations: it was not tested and spelling differs.
- Version/status: published common principles, non-binding; not a consultation draft and not a formally adopted EU legislative act.
- AI/sector evidence: FDA PDF p.1 scope covers evidence generation across the medicine lifecycle, including clinical and manufacturing phases; principles on risk, human values and standards appear p.1; p.2 covers data provenance, validation, monitoring, drift and explanations. Strong `health`, `research_and_innovation`, and `industry_and_manufacturing` if tagging the explicitly scoped manufacturing phase.
- Duplicate check: no matching title/reference in baseline. Distinct from the 2024 reflection paper. For strict EU-endpoint full-text admission, recover the EMA PDF; for work-level corroboration the official co-author PDF plus EMA catalogue is substantial evidence.

### 4. Draft GMP Annex 22 — high confidence, explicitly a draft

- Exact title: **Annex 22: Artificial Intelligence**. Reference: EudraLex Volume 4, proposed new Annex 22.
- [Official six-page draft PDF](https://health.ec.europa.eu/document/download/5f38a92d-bb8e-4264-8898-ea076e926db6_en?filename=mp_vol4_chap4_annex22_consultation_guideline_en.pdf), successfully opened from the consultation’s “Draft guidelines: New annex 22” link.
- [Commission consultation](https://health.ec.europa.eu/consultations/stakeholders-consultation-eudralex-volume-4-good-manufacturing-practice-guidelines-chapter-4-annex_en), successfully opened, gives opening **7 July 2025**, deadline **7 October 2025**, now closed. Opening is an exact consultation/release fallback, not a printed PDF issue or adoption date. No printed issue day was found in the six-page draft. The separate privacy statement’s **1 July 2025** stamp must not be reused for Annex 22.
- Provenance proof: consultation explanation credits drafting to **EMA GMDP-Inspectors Working Group in cooperation with PIC/S**; Commission DG SANTE hosts the consultation. Preserve those distinct roles.
- Version/status: consultation draft, not adopted GMP requirements. No later final version was verified in this bounded search.
- AI/sector evidence: PDF p.2, scope, specifically regulates trained AI/ML models in medicinal-product/active-substance manufacturing; p.2 excludes dynamic/probabilistic/GenAI models from critical GMP applications in this draft; pp.3–6 address metrics, test independence, feature attribution, confidence, change control, monitoring and human review. Strong `health` and `industry_and_manufacturing`.
- Duplicate check: no Annex 22 entry in baseline. Distinct from generic Annex 11 and the admitted EMA reflection paper; do not admit all three consultation attachments merely because they share the page.

### 5. EIOPA consultation predecessor to the final 2025 opinion — high confidence, three separate dates

- Exact PDF title: **Consultation Paper On Opinion on Artificial Intelligence Governance and Risk Management**. Reference **EIOPA-BoS-25-007**. A legacy internal header reads EIOPA (2023)0071709; do not substitute its year for the actual issue date.
- [Official 22-page consultation PDF](https://www.eiopa.europa.eu/document/download/8953a482-e587-429c-b416-1e24765ab250_en?filename=EIOPA-BoS-25-007-AI+Opinion.pdf), successfully opened from [official consultation page](https://www.eiopa.europa.eu/consultations/consultation-paper-and-impact-assessment-eiopas-opinion-ai-governance-and-risk-management_en).
- Date proof: PDF p.1 gives **10 February 2025** (issue). Official consultation’s linked English-file stamp is **11 February 2025** (file publication metadata). Consultation opening is **12 February 2025**, independently confirmed by the successfully opened [EIOPA launch announcement](https://www.eiopa.europa.eu/eiopa-seeking-feedback-its-opinion-artificial-intelligence-governance-and-risk-management-2025-02-12_en). Do not flatten these into one date or call 12 February adoption.
- Source/status: EIOPA agency-authored consultation draft, non-binding. PDF p.2 says feedback will be considered and the opinion revised.
- AI/sector evidence: PDF pp.3–5 paragraphs 1.1–1.3 and 2.1–2.8 establish insurance-authority addressees and interpretation of insurance law for AI; subsequent framework specifies governance and risk management. Strong `financial_services`. Health insurance is mentioned in high-risk context, but `health` should not be added automatically when this draft’s scope excludes high-risk systems.
- Duplicate/version check: distinct from included `eiopa-opinion-ai-governance-risk-management-2025` / EIOPA-BoS-25-360, issued 6 August 2025. This is the missing consultation predecessor. The consultation also has separate impact-assessment and feedback files; they were not promoted as additional candidates in this ten-work sample.

### 6. EIOPA 2019 motor/health-insurance thematic review — high content confidence; publication proof indexed

- Exact title: **Big Data Analytics in motor and health insurance: A thematic review**. PDF identifiers: **ISBN 978-92-9473-142-5; DOI 10.2854/54208; EI-02-19-220-EN-N**.
- [Official 68-page PDF](https://register.eiopa.europa.eu/Publications/EIOPA_BigDataAnalytics_ThematicReview_April2019.pdf), successfully opened. Printed page numbering differs from PDF indices: PDF p.8 is printed p.6.
- Date proof: imprint PDF p.2 establishes publication year **2019** but no exact issue day. **April2019 in the filename is not independent issue-date proof.** [EIOPA release announcement](https://www.eiopa.europa.eu/eiopa-reviews-use-big-data-analytics-motor-and-health-insurance-2019-05-08_en), indexed official text, states publication “today” under **8 May 2019**. A contemporaneous [official press-release PDF](https://register.eiopa.europa.eu/Publications/Press%20Releases/2019-05-08%20BigDataAnalyticsThematicReviewMotorHealthInsurancePressRelease.pdf) has the same date in indexed text. Direct requests returned 429/403 respectively. The later [catalogue page](https://www.eiopa.europa.eu/publications/big-data-analytics-motor-and-health-insurance_en?prefLang=el) displays 19 June 2019; this is later catalogue metadata, not evidence overriding the contemporaneous release.
- Source/status: final published EIOPA empirical thematic report; Publications Office imprint. It is not a binding insurance regulation.
- AI/sector evidence: executive summary printed pp.6–7 discusses AI/ML adoption and fairness/explainability; section 2.2.1 printed pp.14–16 focuses on AI/ML; chapter 5 printed pp.42–44 considers governance. Strong `financial_services`; health-insurance data and pricing justify a possible `health` cross-tag, to be judged against corpus sector semantics. Printed p.6 explains sample scope: 222 insurers/intermediaries, 28 jurisdictions; distinguish empirical findings from general EU-wide census claims.
- Duplicate check: absent; distinct from 2021 EIOPA expert governance report and included 2024 digitalisation report. Do not merge merely because those later reports cite this review.

### 7. EBA Chair’s AI Act mapping letter and annex — high identity/content confidence; publication-date discrepancy needs preserving

- Exact subject/title: **Outcome of EBA’s AI Act mapping exercise**. Reference **EBA/2025/D/5384**.
- [Official nine-page signed letter including annex](https://www.eba.europa.eu/sites/default/files/2025-11/2019d1b5-59f8-4149-ad3b-23cfcd4388a1/EBA%2520Chair%2520letter%2520to%2520Mr%2520Berrigan%2520and%2520Mr%2520Viola%2520on%2520outcome%2520of%2520EBA%25E2%2580%2599s%2520AI%2520Act%2520mapping%2520exercise.pdf), successfully opened. Preserve the working double-encoded official URL.
- Issue proof: PDF p.1 prints **21 November 2025**, reference, and subject. Signature p.2: José Manuel Campa, EBA Chairperson. Recipients are DG FISMA and DG CNECT; they are not co-authors.
- Publication proof/discrepancy: indexed [EBA correspondence archive](https://www.eba.europa.eu/about-us/organisation-and-governance/accountability/correspondence/archive) lists this letter and related factsheet under **21/11/2025**; indexed EBA general result lists show a **20 November 2025** document stamp. Direct archive requests returned 403/non-retryable safety error, so do not assert that the discrepancy is resolved. Prefer printed 21 November as document issue, retain publication date as unresolved unless the archive evidence meets the parent review’s threshold. Both dates are before cutoff.
- Source/status: issued EBA Chair correspondence with substantive annex, non-binding institutional input to Commission guidelines, not an Article 16 EBA guideline or legislative act.
- AI/sector evidence: p.1 specifies AI creditworthiness/credit scoring; p.2 explains mapping purpose; pp.3–9 annex maps AI Act requirements to CRR/CRD, DORA, consumer-credit, mortgage-credit and payment-services rules. Strong `financial_services` and potentially `consumer_protection` from explanation/credit-decision obligations.
- Duplicate check: no matching subject/reference in inventory. Distinct from ECB AI Act opinions and EBA IRB machine-learning consultation/report. Treat the nine-page letter-plus-annex as one work. A separately listed AI Act implications factsheet summarises this exercise; it is not this letter, and is not promoted as an eleventh ranked candidate.

### 8. ECB Financial Stability Review AI special feature — high confidence

- Exact title: **The rise of artificial intelligence: benefits and risks for financial stability**. Published as special feature B of Financial Stability Review, May 2024; no separate document-number reference established.
- [Official complete HTML article](https://www.ecb.europa.eu/press/financial-stability-publications/fsr/special/html/ecb.fsrart202405_02~58c3ce5246.en.html), successfully opened. Named authors: **Georg Leitner, Jaspal Singh, Anton van der Kraaij, Balázs Zsámboki**; ECB publishes the institutional analysis. Preserve named authors; do not turn it into a Governing Council opinion.
- Date proof: article header says it was published as part of the May 2024 FSR. [16 May 2024 ECB release announcement](https://www.ecb.europa.eu/press/pr/date/2024/html/ecb.pr240516~b140d28dd6.en.html), successfully opened, says that Review was published that day. [Governing Council publication decision record](https://www.ecb.europa.eu/press/govcdec/otherdec/2024/html/ecb.gc240510~463d58280d.en.html), successfully opened, records publication authorisation **8 May 2024**, explicitly identifies the AI special feature, and scheduled release **16 May 2024**. The 10 May webpage date is neither article issue nor publication. Use publication **2024-05-16**; issue is month-only unless stronger article-specific proof is recovered. Publication authorisation is not substantive adoption of the article’s findings.
- AI/sector evidence: introduction and sections on financial institutions/systemic implications explicitly analyse generative AI, operational/cyber risks, provider concentration, herding and regulatory implications. Strong `financial_services`; AI is the whole article’s subject.
- Duplicate check: absent; distinct from ECB legislative opinions. Work-level relation should be `part_of` the May 2024 FSR if the parent volume is represented, not a revision of existing ECB opinions. A complete HTML manifestation is independently citable.

### 9. EMA 2024 AI Observatory report — genuine omission, hold for full-text recovery

- Exact title: **2024 AI Observatory report**. Reference **EMA/76534/2025**.
- [Official PDF](https://www.ema.europa.eu/en/documents/report/2024-ai-observatory-report_en.pdf), found through official search. Indexed PDF cover shows **8 May 2025**, EMA reference and agency credit. Direct PDF attempts returned 429; full-text direct retrieval was **not** successful in this run.
- [Official EMA AI catalogue](https://www.ema.europa.eu/en/about-us/how-we-work/data-regulation-big-data-other-sources/artificial-intelligence) search-index entry supplies document-specific first publication **10/07/2025**. Distinguish activity year 2024, issue **2025-05-08**, release **2025-07-10**.
- Source/status: EMA credited on indexed cover; EMRN experience compiled in HMA/EMA workplan context. Joint publication versus joint authorship requires full-text/catalogue confirmation. Public annual report; no adoption asserted.
- AI/sector evidence: indexed opening explains AI Act context, medicines-lifecycle horizon scanning, and regulatory AI use. Strong provisional `health`, `public_administration`, `research_and_innovation`.
- Duplicate check: only **2025 AI Observatory report** / EMA/67888/2026 is included. Annual reports are distinct works, not necessarily revision versions. Related compilation (EMA/154528/2025) and horizon-scanning report (EMA/571739/2024) are separately listed attachments, not counted here; determine work/part identities before admitting them.
- Admission recommendation: pending full primary PDF recovery; indexed metadata must not be presented as completed full-text verification.

### 10. EBA September 2025 AI adoption factsheet — genuine omission, hold for full-text recovery

- Exact title: **Rising application of AI in EU banking and payments sector**. No numerical reference established. Official PDF search title identifies the Digital Finance Factsheet Series.
- [Official PDF](https://www.eba.europa.eu/sites/default/files/2025-09/146b3558-d026-47bf-a872-f05e93ed30d2/Rising%20application%20of%20AI%20in%20EU%20banking%20and%20payments%20sector.pdf), indexed official text gives **25/09/2025** on the first-page text. Direct requests returned 403. No full PDF retrieval claimed.
- [Official filtered EBA result list](https://www.eba.europa.eu/search?f%5B0%5D=date%3A2025-09&f%5B1%5D=document_type%3A5606&f%5B2%5D=type%3ADocuments&p_p_auth=paERy6SJ&p_p_id=101&p_p_lifecy=) returned an indexed one-result list, document type Factsheet, dated **25 September 2025**. The official digital-finance result also locates it in the Factsheets section. Do not promote it to a substantial standalone report solely because the generated listing description calls it a report.
- Source/status: EBA institutional factsheet, publicly issued; not legislation or a consultation draft.
- AI/sector evidence: indexed document opening and observed-use-cases section address AI banking adoption, client profiling and transaction/credit-history grouping; catalogue identifies credit scoring, fraud detection, customer support and GPAI. Strong provisional `financial_services`.
- Duplicate check: absent; distinct from 2020 EBA big-data report and 2023 IRB follow-up. Admission recommendation: pending full official text, exact pagination and any further version identifiers.

## Search and navigation log

The following are the exact queries sent, grouped in execution order. Search used the web search tool, normally 2–4 queries per batch. Queries with literal `site:` strings were initially unfiltered; later explicit domain filters narrowed official-only retrieval. Off-domain hits (commercial commentary, Reddit, arXiv) were not used as evidence. This is a selected-result navigation log, not a preserved complete SERP export or a reproducible search-engine census.

1. `site.ema.europa.eu artificial intelligence reflection paper workplan guidance 2025 2026`; `site.eba.europa.eu artificial intelligence report 2025 2026`; `site.eiopa.europa.eu artificial intelligence report opinion 2025`; `site.esma.europa.eu artificial intelligence statement report 2025 2026`.
2. `site.health.ec.europa.eu "MDCG 2025-6"`; `site.ema.europa.eu "artificial intelligence" "guiding principles"`; `site.ema.europa.eu "large language models" principles`; `site.eba.europa.eu "Rising application of AI"`.
3. `site.eba.europa.eu "AI Act" "mapping" 2025 report`; `site.eiopa.europa.eu "big data analytics" "2019" report`; `site.health.ec.europa.eu "Annex 22" "2025" artificial intelligence`; `site.eba.europa.eu "automated" "2016" advice report`.
4. `"site:eba.europa.eu" "AI Act" "mapping" "report"`; `"site:bankingsupervision.europa.eu" "artificial intelligence" report 2024`; `site.eiopa.europa.eu "Big Data Analytics" "8 May 2019"`. The first two overquoted site expressions produced little useful material; they are retained as search defects, not silently corrected in retrospect.
5. `site.eba.europa.eu "AI Act" "mapping" report 2025` (domain filter eba.europa.eu); `site.ecb.europa.eu artificial intelligence financial stability 2024` (ecb.europa.eu).
6. `site.ema.europa.eu "Harnessing AI" "September" "2024"`; `site.ema.europa.eu "Guiding principles of good AI" "14/01/2026"`; `site.fda.gov "Guiding Principles of Good AI Practice" January 2026`; `site.eba.europa.eu "Rising application" "25" "September"`.
7. `"Harnessing AI in medicines regulation" "2024"` (ema.europa.eu); `"2024 AI Observatory report"` (ema.europa.eu); `"AI Act implications for the EU banking" "21 November"` (eba.europa.eu); `"automation in financial advice" "2016"` (eba.europa.eu, esma.europa.eu, eiopa.europa.eu).
8. `"Financial Stability Review" "May 2024" "16 May" ECB` (ecb.europa.eu); `"AI Act implications for the EU banking sector" filetype:pdf` (eba.europa.eu); `"Rising application of AI" filetype:pdf` (eba.europa.eu).

Selected results and follow-through:

| Route | Results inspected/selected | Navigation and outcome |
|---|---|---|
| EMA broad search | Existing reflection paper, existing workplans; LLM principles; good-AI principles; 2024/2025 observatories | Official PDF and topic catalogue routes. LLM full text succeeded; later EMA pages/PDFs frequently returned 429. FDA official co-author route recovered good-AI text and release proof. |
| MDCG search | Commission announcement, endorsed-guidance index, direct MDCG2025-6 PDF | Announcement and PDF successfully opened. Cover resolved joint AIB/MDCG authorship caveat. |
| GMP search | Chapter4/Annex11/Annex22 consultation | Opened consultation; clicked only new Annex22 draft; six-page full text successful. |
| EIOPA2025 search | Existing final opinion; missing draft consultation | Opened launch → consultation → English consultation PDF. Exact file-publication stamp11Feb and opening12Feb retained separately. |
| EIOPA2019 search | Thematic report, contemporaneous release, later catalogue | Full report successful; release direct requests failed but official indexed announcement/press-release text confirmed May8 release; June19 catalogue conflict recorded. |
| EBA search | Adoption factsheet, AIAct mapping factsheet, Chair letter, programming/risk reports | Chair letter full PDF successful; factsheet PDFs403; correspondence archive403. Non-www digital-finance page once opened an older cached snapshot (through January2025), unsuitable for proving current2025 entries. Indexed current lists retained explicitly as indexed evidence. |
| ESMA search | AI securities2023, retail statement2024, investment-fund article2025, adoption2026 | These were all already included. No new ESMA record promoted; no complete library pagination performed. |
| ECB search | May2024 AI special feature; FSR press release; Governing Council publication authorisation | All three successfully opened; sequence separates authorisation8May, announcement-page10May, actualrelease16May. |
| Pre2018 probe | Joint ESAs automation-in-advice discussion paper, consultation opened4Dec2015; 2016 response/event pages | Not promoted: algorithmic automation/decision trees do not by themselves establish substantive AI under the corpus definition, and complete text/date review was not completed. Do not use the EBA page’s4Mar2016 response deadline as original issue. |

## Stopping rule and practical limitations

Stopped after establishing ten distinct, non-duplicate candidate works and tracing the strongest official date/provenance sources within these routes. Full institutional archives, language variants, all publication pagination, all versions, and all pre-2018 references were **not** exhausted. The existence of additional unassessed annexes or topic-page links is not a coverage claim. No search-result counts are reported for broad queries because the tool did not supply reliable universe totals.

Best immediate admission targets from successfully retrieved texts are 1, 4, 5 and 8; 2, 3, 6 and 7 have strong substantive texts but the indicated publication/manifestation caveats should be resolved or explicitly carried in evidence fields. Items9–10 should remain pending until full official text is recovered. This report is not a substitute for the parent agent’s canonical schema validation, full source preservation, independent review, or publication decision.
