# JURI robotics report: primary-source verification

Candidate: `historical-juri-robotics-report-2017`.

Decision after independent gate review: **evidence-ready for canonical admission**. Identity, authorship, full-text relevance, procedural lineage and an exact official publication event are verified. The directly evidenced 27 January 2017 event is official tabling for plenary, which can populate `publication_date=2017-01-27` with that explicit meaning under the existing specification. A separately identified first website-upload timestamp is not required. Full canonical construction and validation remain unperformed; no canonical record, publication status, relationship, Git state or website was changed.

Verification window: 2026-09-06T01:08:20Z to 2026-09-06T01:13:12Z (Europe/London: 02:08-02:13 BST). PDF download was observed locally at 02:10:27 BST; hash and completeness were subsequently checked.

## Primary sources and access evidence

1. [Official English report HTML](https://www.europarl.europa.eu/doceo/document/A-8-2017-0005_EN.html). Ordinary web fetch returned a JavaScript/robot-verification page. Opening the same URL normally in the in-app browser succeeded immediately without a CAPTCHA interaction. The complete rendered report body was accessible: 156,039 characters, with motion, annex, explanatory statement, all six opinions and final JURI vote. This is direct report text, not an indexed search snippet.
2. [Official English report PDF](https://www.europarl.europa.eu/doceo/document/A-8-2017-0005_EN.pdf). Downloaded through the report page's displayed PDF link using normal browser download. Retained at `C:/Users/ROG/Downloads/A-8-2017-0005_EN.pdf`: 587,245 bytes; 64 pages; SHA-256 `b28361a4a6dfdda93c0bb24facb7ca9f9fe20dc227a4640596b1cd8647e26d95`. All 64 pages have nonempty extracted text and the footer identifier `PE582.443v03-00`. Cover, page 10 and final vote page 64 were rendered with Poppler and visually inspected. Relevant full pages and section headings were inspected in PDF text and rendered HTML. The file has not been altered. A research-folder copy was attempted but shell writes were denied; the downloaded copy remains the verified local source.
3. [OEIL procedure 2015/2103(INL)](https://oeil.europarl.europa.eu/oeil/en/procedure-file?reference=2015%2F2103%28INL%29), direct English HTML success. Key players, key events and documentation gateway independently verify responsibility, tabling and the distinct procedural stages.
4. [OEIL full procedure PDF](https://oeil.secure.europarl.europa.eu/oeil/en/procedure-file/pdf?reference=2015%2F2103%28INL%29), direct English text extraction success, five pages. This is a procedure dossier containing summaries, not the original report. Web screenshot requests failed with cache-miss errors; direct HTML corroborates the metadata independently. Page 1 lists responsible/opinion committees and rapporteurs; pages 2-3 list draft, report, adopted resolution and dates.
5. [OEIL report summary](https://oeil.europarl.europa.eu/oeil/en/document-summary?id=1473044), direct English HTML success. Heading associates the summary with the 27 January 2017 tabling event. The opening paragraph attributes the adopted report to JURI and Mady Delvaux; topic headings corroborate AI relevance. This was used as corroboration, not as a full-report substitute.
6. [Mady Delvaux: reports as rapporteur, eighth term](https://www.europarl.europa.eu/meps/en/124776/MADY_DELVAUX/all-activities/reports/8), direct English HTML success. The robotics entry supplies the full report title, 27-01-2017, `A8-0005/2017`, `PE582.443v03-00`, JURI and Delvaux. Its download links resolve to the same Doceo PDF/DOCX manifestations.
7. [Adopted resolution on EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A52017IP0051), direct English full-text success. The heading gives the separate resolution's date and identity; the preamble explicitly cites `A8-0005/2017`; paragraph 44 provides a useful text-level difference from the report.

Unsuccessful official alternatives tested before browser recovery: Doceo HTML/PDF and DOCX via official links returned challenges; RegData `https://www.europarl.europa.eu/RegData/seance_pleniere/textes_deposes/rapports/2017/0005/P8_A(2017)0005_EN.pdf` and DOCX did not open; legacy `sides/getDoc.do` report URLs failed; `https://redmapl3.europarl.europa.eu/RedmapFront/media/reds_iPlRp/A-8-2017-0005/A-8-2017-0005_en.html` failed. No challenges were solved and no access controls were bypassed. Later normal browser retrieval makes these endpoint failures a method limitation rather than an outstanding full-text blocker.

## Identity and dates

| Field | Verified value | Evidence and interpretation |
|---|---|---|
| Official title | REPORT with recommendations to the Commission on Civil Law Rules on Robotics | PDF cover and HTML heading |
| Document identity | A8-0005/2017 | PDF cover, official MEP listing and OEIL report row |
| Procedure | 2015/2103(INL) | PDF cover and OEIL; legislative initiative/request for a legislative proposal |
| Committee dossier | JURI/8/03463 | OEIL technical information |
| Version identifier | PE582.443v03-00 | PDF cover and every page footer; MEP listing |
| Internal production identifier | RR\\1115573EN.docx | PDF footer; do not treat as a second document |
| Main institution | European Parliament, Committee on Legal Affairs | PDF cover and OEIL committee-responsibility field |
| Rapporteur | Mady Delvaux | PDF cover; MEP listing; OEIL |
| Document issue date | 2017-01-27 | Explicit PDF cover date and official English report heading |
| Committee adoption | 2017-01-12 | PDF p. 64 final vote table explicitly labels Date adopted; result 17 for, 2 against, 2 abstentions; OEIL independently records committee vote |
| Public procedural tabling | 2017-01-27 | OEIL key events and documentation gateway explicitly label the committee report tabled for plenary |
| Plenary adoption of resulting resolution | 2017-02-16 | OEIL and separate EUR-Lex resolution heading; this is not the report's issue/adoption date |

Publication-date treatment: use `document_date=2017-01-27`, `document_date_kind=document_issue`, and `publication_date=2017-01-27`, with publication evidence explicitly meaning official parliamentary tabling/publication for plenary. The [OEIL key-events/documentation-gateway rows](https://oeil.europarl.europa.eu/oeil/en/procedure-file?reference=2015%2F2103%28INL%29) independently associate `A8-0005/2017` with `27/01/2017`; the gateway labels it `Committee report tabled for plenary, single reading`. The rapporteur's official report listing also corroborates the exact date and version. This is a transparent bibliographic interpretation of official publication, not a verified server-upload timestamp. Keep committee adoption `2017-01-12` as a separate `institutional_adoption` date. Do not introduce `public_plenary_tabling` as an additional-date kind: it is not in the current vocabulary.

The date interpretation was independently checked against historical-scope design section 5.1 (official publication represented by the cited source, rather than first website upload) and existing canonical reports `ep-joint-committee-report-a9-0188-2023` and `ep-ai-omnibus-report-a10-0073-2026`, both of which use OEIL tabling dates for publication and preserve committee adoption separately. No schema change or relaxation of official-source requirements is needed. Do not infer publication from the cover, search-engine date labels, HTTP information or PDF metadata alone.

The PDF's embedded CreationDate and ModDate are `D:20170216103747+01'00'`. These are file-generation timestamps, not evidence that the report was first issued/adopted/published on 16 February. Its PDF Author property reads `PEDERSEN Jeanette Borno`; that is production metadata and does not displace the institutional/rapporteur credits visibly printed in the report. The inspected manifestation remains explicitly labelled the 27 January report and retains report-specific text distinct from the adopted resolution.

## Authorship and embedded contributions

European Parliament is the institutional author/publisher; JURI is the responsible authoring and adopting committee; Delvaux is rapporteur. The Commission is the requested future proposer/addressee, not co-author of this report. The cover names TRAN and LIBE as associated committees under then Rule 54. The six separately headed opinion sections remain embedded components for this candidate; no separate opinion records are proposed here.

| Embedded opinion | Named rapporteur | Section heading date | Explicit adoption table | PDF locators |
|---|---|---|---|---|
| TRAN | Georg Mayer | 2016-11-16 | 2016-11-10 | pp. 30, 34 |
| LIBE | Michał Boni | 2016-11-23 | 2016-11-17 | pp. 35, 40 |
| EMPL | Ádám Kósa | 2016-11-09 | 2016-11-08 | pp. 41, 46 |
| ENVI | Cristian-Silviu Buşoi | 2016-10-14 | 2016-10-13 | pp. 47, 54 |
| ITRE | Kaja Kallas | 2016-11-15 | 2016-10-13 | pp. 55, 58 |
| IMCO | Dita Charanzová | 2016-10-12 | 2016-10-11 | pp. 59, 63 |

These differences demonstrate why heading, gateway and adoption dates must not be collapsed. OEIL lists EMPL's committee-opinion document on 23 November, whereas the embedded opinion heading is 9 November and its adoption table is 8 November; that is not a reason to change the main report date. If opinions are later proposed as independent records, their separate manifestation identities and gateway dates need their own review.

## Direct AI substance and classifications

The primary full report supports `direct_ai_substantive` and `historical_lineage`. It contains concrete AI governance proposals, rather than only generic automation history. These are editorial classifications; the institution did not assign the catalogue's taxonomy labels.

| Proposed classification | Precise primary locator | Evidence rationale |
|---|---|---|
| direct_ai_substantive; general_cross_sector | Motion recital B, p. 3; paras. 12 and 16-17, p. 10; explanatory statement pp. 27-29 | Explicit AI legal/ethical implications, explanation of AI-assisted decisions and proposed European robotics/AI agency |
| justice | Motion paras. 49-59, pp. 16-18; especially para. 51, p. 16; annex civil-law liability, pp. 20-21 | Requests Union legislative and complementary measures for legal questions involving robotics and AI, liability and compensation |
| industry_and_manufacturing | ITRE opinion suggestion 1, p. 55, and suggestion 2, pp. 55-56; IMCO recital E, p. 59 | AI/robotics industrial policy, integration into value chains, commercialisation and manufacturing competitiveness |
| transport_and_mobility | Motion paras. 24-30, pp. 12-13; TRAN opinion pp. 30-34 | Dedicated autonomous-transport regulation, infrastructure, safety and liability proposals |
| employment_and_labour | Motion paras. 41-46, pp. 15-16; EMPL suggestions 2 and 11, pp. 41-43 | AI-related employment monitoring, social security and workplace protection |
| research_and_innovation | Motion paras. 6-9, pp. 8-9; annex charter pp. 21-26 | AI/robotics research funding, innovation, interoperability and research ethics |
| health | Motion paras. 31-40, pp. 13-15; ENVI recital E and suggestions, pp. 47-53 | Dedicated care/medical robotics and AI-containing cyber-physical-system safeguards |
| consumer_protection | Motion paras. 17, 22 and 49, pp. 10, 12, 16; IMCO suggestions 2, 5, 8-9, pp. 60-61 | Product safety, consumer remedies and standards for robotics/AI |
| eu_institution_authored; officially_published | PDF cover, contents p. 2, official Parliament hosting and OEIL tabling row | Parliament/JURI report officially issued and publicly tabled; no claim of an OJ publication for the report |

The original five sector suggestions are supported. Research, health and consumer protection also have substantive dedicated passages; adding them would be a later editorial classification change, not an automatic mutation in this verification pass.

## Version and procedural lineage

OEIL distinguishes the committee draft `PE582.443` dated 31 May 2016, the tabled report `A8-0005/2017` dated 27 January 2017 and adopted text `T8-0051/2017` dated 16 February 2017. The current report's full version number is independently matched by its cover and Delvaux's listing. The draft's direct Doceo endpoint challenged, so a line-by-line draft-to-report comparison was not performed; its identity and procedural precedence are verified from OEIL, not misrepresented as draft full-text verification.

The report is a distinct committee-report record, related as the report preceding/supporting the already catalogued `civil-law-rules-on-robotics-resolution-2017`. It is neither the adopted resolution nor merely a second URL for it. Besides having an explanatory statement and six opinions absent from the resolution, its motion paragraph 44 (PDF p. 15) includes a proposed debate about general basic income. The adopted resolution's paragraph 44 ends after the social-security-scenarios request and omits that passage. This direct content comparison confirms that the downloaded report is not a mislabelled copy of the adopted resolution.

The separate resolution is `P8_TA(2017)0051`, CELEX `52017IP0051`, OJ C 252 of 18 July 2018, pp. 239-257. Those CELEX/OJ/publication facts belong to the resolution and must not be copied onto the report. Its preamble explicitly cites `A8-0005/2017`.

## Remaining limitations and handling

No original-report identity, English access, authoring attribution, AI-relevance or report-to-resolution relationship deficiency remains. The public-tabling publication meaning has been checked against the existing specification and canonical precedents; an unknown first website-upload timestamp is a retained source limitation, not an additional admission blocker. No substantive adoption is inferred from 27 January. No draft content equivalence, prior-version byte history, first-upload time or independent opinion identity is asserted. Canonical record preparation and validation remain to be done. This verification itself did not admit or publish the report.
