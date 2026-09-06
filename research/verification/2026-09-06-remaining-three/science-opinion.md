# Deep verification: Scientific Opinion No. 15 on AI in science

Candidate: `chief-scientific-advisors-ai-science-opinion-2024`.

Research date: 6 September 2026. Retrieval window: approximately 01:08-01:17 UTC. Audit timestamp: 2026-09-06T01:16:58Z. Research-only evidence memo; no admission, canonical record, relationship, website or publication changes.

## Verdict

**Pending original-edition verification.** The corrected opinion is fully identifiable and substantively relevant. Fresh inspection of the official 102-page PDF verifies its issue date, correction label, institutional roles and recommendations. The earlier version dependency has not been resolved: the original Publications Office entry linked by the Commission now returns 404, its download route produces an HTML error page, its RDF export is empty, and the original DOI redirects to a generic DOI help page. No eligible original full text was retrieved in this pass, so no complete comparison of original and corrected text or validated original-version relationship is claimed.

This is an independent expert opinion adopted by the Group of Chief Scientific Advisors (GCSA), not an adopted Commission strategy or binding EU policy. The Commission's own announcement expressly describes the advice as non-binding.

## Sources successfully inspected

1. Corrected edition catalogue: https://op.europa.eu/en/publication-detail/-/publication/d6d8ed54-32a8-11ef-a61b-01aa75ed71a1/language-en
   - Official HTML opened through web browsing and directly through Python standard-library HTTPS retrieval.
   - Publication details and release field inspected; the catalogue exposes the PDF download-handler in its HTML.
2. Corrected edition full text: https://op.europa.eu/o/opportal-service/download-handler?identifier=d6d8ed54-32a8-11ef-a61b-01aa75ed71a1&format=pdf&language=en&productionSystem=cellar&part=
   - HTTP 200, `application/pdf`, **14,846,309 bytes**, **102 PDF pages**.
   - SHA-256 of bytes inspected: `df125f19a4673b57f19b93fe6edcd00101b6009160a131838fc1dc14774a5d2d`.
   - Parsed in memory with bundled `pypdf`. Cover, imprint, title page, contents, group membership, acknowledgments, executive summary, scope, recommendations and methodology read. All pages were text-extracted and searched for correction notices. This is successful full-text retrieval plus inspection of relevant sections; it does not claim a visual audit of all 102 pages or an archival snapshot.
3. Equivalent corrected full-text item, identified in official RDF: https://publications.europa.eu/resource/cellar/d6d8ed54-32a8-11ef-a61b-01aa75ed71a1.0001.01/DOC_1
   - HTTP 200, `application/pdf;charset=UTF-8`, **14,846,309 bytes**; PDF header reports 102 pages.
4. Commission announcement, dated 15 April 2024: https://research-and-innovation.ec.europa.eu/news/all-research-and-innovation-news/commission-receives-scientific-advice-artificial-intelligence-uptake-research-and-innovation-2024-04-15_en
   - Heading/date, opening release statement, handover, recommendations, background and More Information links inspected.
   - Identifies the opinion as GCSA Scientific Opinion No. 15 and supplies the now-broken original OP catalogue link below.
5. Corrected official RDF export, obtained through the catalogue's Metadata RDF action:
   https://op.europa.eu/en/publication-detail?p_p_id=publicationDetailsActions_PublicationDetailsActionsPortlet_INSTANCE_P7Lc96wTRLvv&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&_publicationDetailsActions_PublicationDetailsActionsPortlet_INSTANCE_P7Lc96wTRLvv_requestAction=rdf&cellarId=d6d8ed54-32a8-11ef-a61b-01aa75ed71a1&nonInferred=true
   - HTTP 200; 22,059-character RDF response parsed and inspected.
   - `genpub:2024.3180`; `expression_edition` confirms the corrected first-edition label; PDF manifestation is `PUB_KI0924456ENN`.
6. Official edition-list action, found in the catalogue HTML:
   https://op.europa.eu/en/publication-detail?p_p_id=publicationDetails_PublicationDetailsPortlet&p_p_lifecycle=1&p_p_state=exclusive&p_p_mode=view&_publicationDetails_PublicationDetailsPortlet_jakarta.portlet.action=loadPublicationEditionsAction&_publicationDetails_PublicationDetailsPortlet_language=en&_publicationDetails_PublicationDetailsPortlet_cellarId=d6d8ed54-32a8-11ef-a61b-01aa75ed71a1
   - HTTP 200; the returned edition list contains only the corrected UUID and date 2024-06-21. It does not independently identify an original-version parent.

## Exact corrected-edition identity and dates

| Field | Verified value | Precise locator |
| --- | --- | --- |
| Title | Successful and timely uptake of Artificial Intelligence in science in the EU | PDF pp. 1-3 |
| Series | Scientific Opinion No. 15 | PDF pp. 1, 3 |
| Edition label | “First edition - corrected version.” | PDF p. 2; RDF `expression_edition` |
| Manuscript completion | March 2024 | PDF p. 2 |
| Document issue date | 27 March 2024, Brussels | PDF p. 3 |
| Corrected manifestation website release | 21 June 2024 | OP catalogue, Released on EU publications website |
| PDF DOI | 10.2777/46863 | PDF p. 2; OP PDF metadata |
| PDF ISBN | 978-92-68-17917-8 | Same |
| PDF catalogue number | KI-09-24-456-EN-N | Same |
| Print DOI | 10.2777/065364 | PDF p. 2; OP Paper metadata |
| Print ISBN | 978-92-68-17916-1 | Same |
| Print catalogue number | KI-09-24-456-EN-C | Same |
| Publisher | Publications Office of the European Union, Luxembourg, 2024 | PDF p. 2 |

The March date is the date printed on the opinion. The June date is the release of the corrected catalogue manifestation. Neither should replace the other. PDF p. 7 (printed p. 5) says the group adopted the opinion but does not itself specify an adoption day; the printed 27 March issue date should not be silently relabelled as a separately proven formal adoption event.

The 15 April 2024 Commission news article says the SAM released the recommendations that day and records their handover to Commissioners. This supports an earlier public-release/handover event for Opinion No. 15. It does not make 15 April the publication date of the corrected June manifestation.

The corrected RDF includes technical creation/modification timestamps (including an English-expression modification on 29 August 2024) and a `work_date_document` of 21 June 2024. Those catalogue/ingestion dates do not establish a further substantive revision or change the opinion's printed issue date.

## Authorship, institutional roles and policy status

- **GCSA: substantive group author and adopter.** The title page attributes the opinion to the group. Acknowledgments, PDF p. 7 / printed p. 5, state that it was adopted by GCSA and endorsed by all seven advisors. Nicole Grobert and Alberto Melloni were co-leads, with Maarja Kruusmaa preparing the opinion. Methodology, PDF p. 49 / printed p. 47, confirms they developed it on behalf of the group.
- **European Commission / DG Research and Innovation: requester and support body, also corporate catalogue attribution.** The acknowledgments name the request from Margrethe Vestager and Iliana Ivanova and thank the Commission support team in Unit RTD.02. The imprint identifies DG RTD and Unit 02. Preserve these roles separately from the group's authored/adopted opinion.
- **Publications Office: publisher and official host.** Imprint, catalogue and downloaded item agree.
- **SAPEA: supporting evidence, not this document's author or original version.** PDF p. 3 explicitly identifies support by Evidence Review Report No. 13. The methodology describes how the recommendations build on that report and other evidence. The ERR is a separate work, not a prior edition of Scientific Opinion No. 15.

PDF p. 2 disclaims representation of the Commission's official position. The Commission announcement's opening paragraph characterises the recommendations as independent and non-binding, potentially informing a future strategy. These directly support `non_binding`, an advisory/agenda-setting policy stage and expert-group authorship. A Commission logo or DG catalogue credit does not turn the opinion into Commission-adopted policy.

Group membership (PDF p. 6 / printed p. 4): Nicole Grobert (chair), Naomi Ellemers, Maarja Kruusmaa, Eric F. Lambin, Alberto Melloni, Nebojša Nakićenović (deputy chair), Eva Zažímalová. This is a membership list; do not automatically replace the group author with an unsupported personal-author list.

## Substantive AI scope and locators

The document clearly qualifies as directly and substantively about AI. The strongest primary sector is research and innovation.

| Evidence | Locator in corrected PDF | Classification implication |
| --- | --- | --- |
| Mandate to advise on responsible AI uptake in science, impacts on research productivity, scientific process, skills and Commission action | Section 1.2, PDF pp. 14-15 / printed pp. 12-13 | Direct AI substance; research and innovation |
| Funding and governance, a publicly funded distributed AI research institute (EDIRAS), an AI in science council (EASC), and monitoring | Section 2, recommendation 1 and 1.1-1.3, PDF pp. 35-38 / printed pp. 33-36 | AI research policy and infrastructure |
| Green AI; societal priorities including personalised health, materials, climate and cultural/historical research; science-specific AI tools | Recommendations 1.4-1.6, PDF pp. 38-40 / printed pp. 36-38 | Supports environmental and health subject notes if appropriate to the approved vocabulary; these are research applications within the overarching research policy |
| Data quality and representativeness, access, partnerships, transparent models and evaluation of AI limits | Recommendation 2 and 2.1-2.4, PDF pp. 41-44 / printed pp. 39-42 | Substantive governance of AI research resources and outputs |
| Coordination of research infrastructures, EuroHPC and EDIRAS; support for European SMEs providing research services | Recommendation 3, PDF pp. 44-45 / printed pp. 42-43 | Infrastructure and innovation |
| AI literacy, researcher training and talent, human rights and research assessment | Recommendation 4 and 4.1-4.5, PDF pp. 46-48 / printed pp. 44-46 | Human/community focus and research governance |

These are recommendations of the advisors. Their appearance in this report does not prove that the EU subsequently implemented them. The preamble, PDF p. 35 / printed p. 33, limits the evidence and policy knowledge underpinning recommendations to March 2024.

## Original edition and attempted recovery

The Commission's April announcement links this exact original catalogue URL:

https://op.europa.eu/en/publication-detail/-/publication/2a6e3d4f-fae0-11ee-a251-01aa75ed71a1/language-en/format-PDF/source-315352732

Both that URL (web tool) and the shortened `/language-en` form (direct HTTPS) return 404. Ordinary in-app browser navigation independently displayed the Publications Office message “The document was not found” after normalising the URL to `/language-en`. This identifies an official historical destination, but does not recover its original content or complete metadata.

Other safe public retrieval checks:

- https://data.europa.eu/doi/10.2777/08845 -> HTTP 200 after redirect to https://op.europa.eu/en/web/general-publications/doi; generic DOI information, not the original opinion.
- https://data.europa.eu/doi/10.2777/473374 -> the same generic page; no original print manifestation recovered.
- https://op.europa.eu/o/opportal-service/download-handler?identifier=2a6e3d4f-fae0-11ee-a251-01aa75ed71a1&format=pdf&language=en&productionSystem=cellar&part= -> HTTP 200 HTML error page, not PDF.
- https://publications.europa.eu/resource/cellar/2a6e3d4f-fae0-11ee-a251-01aa75ed71a1.0001.01/DOC_1 -> 404.
- https://publications.europa.eu/resource/cellar/2a6e3d4f-fae0-11ee-a251-01aa75ed71a1.0001.01/DOC_2 -> 404.
- https://op.europa.eu/resource/cellar/2a6e3d4f-fae0-11ee-a251-01aa75ed71a1 -> 404.
- https://publications.europa.eu/resource/genpub/PUB_KI0523478ENN -> 404.
- https://publications.europa.eu/resource/doi/10.2777/08845 -> 404.
- The RDF export action above, with original UUID `2a6e3d4f-fae0-11ee-a251-01aa75ed71a1`, returns HTTP 200 `application/rdf+xml` with zero bytes.
- The previously used flexpaper endpoint, https://op.europa.eu/flexpaper/view?doc=2a6e3d4f-fae0-11ee-a251-01aa75ed71a1.en.PDF.pdf&user=&format=pdf&page=[*,0], returned a one-byte NUL body labelled PDF. The same viewer path for the corrected UUID also returned a one-byte body during this pass, while its actual download-handler succeeded. A nominal HTTP 200 / PDF header alone must not count as full-text verification.

Targeted official-domain searches used title, DOI, ISBN, catalogue number, original UUID and correction terms. No additional official original PDF or published correction table was found. These are bounded searches and retrieval tests, not an exhaustive EU catalogue census. No login, access control or security challenge was bypassed.

The Commission links the Scientific Advice Mechanism site. Its https://scientificadvice.eu/scientific-outputs/ai-in-science-scientific-opinion/ page still labels the item 15 April 2024 and DOI 10.2777/08845. Crucially, ordinary live browser inspection established that its Download PDF version link actually targets the **corrected** DOI https://data.europa.eu/doi/10.2777/46863. Its advice page https://scientificadvice.eu/advice/artificial-intelligence-in-science/, after opening the Recommendations by the Advisors tab, displays original DOI 10.2777/08845 and ISBN 978-92-68-10084-4 but also links the corrected DOI from both Scientific opinion links. Displayed old bibliographic metadata and the live download destination disagree. These mechanism-site metadata corroborate the original identification; they do not supply successfully retrieved original EU-hosted full text. Academy mirrors surfaced in search, but are not promoted to eligible official EU source evidence under this pass's source restriction.

The Publications Office's EU Web Archive page, https://op.europa.eu/en/web/euwebarchive, was inspected in the ordinary browser as one further official recovery route. It describes an open archive preserving EU websites and links the official Publications Office collection at https://archive-it.org/collections/12090?fc=websiteGroup%3APublications+Office+of+the+EU. Following that public link reached a Session Verification page and did not expose a searchable archive or capture. No archive challenge was solved or circumvented and no archived original copy was recovered. The existence of that archive is not proof that this particular PDF was captured.

Original identifiers carried forward as unresolved verification leads: PDF DOI `10.2777/08845`, ISBN `978-92-68-10084-4`, catalogue number `KI-05-23-478-EN-N`; print DOI `10.2777/473374`, ISBN `978-92-68-14344-5`, catalogue number `KI-05-23-478-EN-C`. Only the first DOI/ISBN have current mechanism-site metadata corroboration in this pass; the others were search/discovery leads, not newly verified original EU-hosted imprint fields.

## Correction extent and other distinct publications

Full corrected-PDF text search for `corrected`, `corrigendum`, `erratum`, `revision` and the original DOI found correction wording only on PDF pp. 1-2. There is no located correction schedule or original-DOI cross-reference in that extracted text. The corrected label is verified, but **which substantive passages changed remains unverified**. Do not claim editorial-only correction, unchanged recommendations, or a complete original-versus-corrected diff.

The corrected RDF's `work_related_to_work` points to `genpub:2024.0720`, resolved and inspected at https://publications.europa.eu/resource/genpub/2024.0720 and https://op.europa.eu/en/publication-detail/-/publication/9e451cf1-65b5-11ef-a8ba-01aa75ed71a1/language-en. This is **Summary of the scientific opinion on successful and timely uptake of artificial intelligence in science in the EU**, catalogue `KI-02-24-137-EN-N`, released 28 August 2024. It is a summary, not the missing original report and not evidence for a `revises` relationship. Likewise SAPEA Evidence Review Report No. 13 is distinct supporting research. Print/PDF manifestations of the corrected opinion should not be counted as separate documents.

## Exact remaining deficiencies and next permissible step

1. Obtain original Opinion No. 15 full text from an eligible official EU source and verify the original imprint/identifiers and edition label against it.
2. Establish the original-versus-corrected connection using original content plus explicit corrected-edition evidence; inspect differences or an authoritative correction notice. Do not infer that all changes are cosmetic.
3. Prepare an independently supported original parent and validated version relationship before any later admission of the corrected version, following the existing admission rule. No such canonical changes were made here.

The current official evidence supports a strong corrected-edition record draft and a 15 April initial-release event, but does not remove the original-version hold. Further progress needs an eligible original copy or an authoritative source clarifying the correction/version lineage; contacting the publisher is an external message and has not been attempted.
