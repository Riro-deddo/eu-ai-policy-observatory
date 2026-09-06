# Council 2022 pending-record second pass

Reviewed 11 retained Council AI Act records dated 2022 against their exact PDFs, live Council public-register results and bounded searches for dated official publication manifestations. Reviewer: AI-assisted evidence review, 5 September 2026 at 19:47:08 UTC. Publication cutoff remains 4 September 2026.

## Outcome

- 2 upgrades: `ai-act-council-general-approach-st-14954-2022` and `ai-act-council-general-approach-german-statement-14954-add-1`.
- 9 holds: exact text, issue date, originator, AI relevance and stored lineage were rechecked, but no official source labels a publication date for each exact manifestation.
- 1 held-document factual repair: ST 12206/22 INIT is dated 7 September 2022; 16 September belongs to REV 1.
- 1 held-source repair: ST 10069/22 is the official multilingual `/x/pdf`, not the broken `/en/pdf`.

## Why the two records can upgrade

The official Council release headed **6 December 2022 10:20** states that the Council adopted its common position and directly links both **General approach** (ST 14954/22 INIT) and **General approach - Statement by Germany** (ST 14954/22 ADD 1). This is a dated official publication of those exact manifestations under historical-scope specification section 5.1. The proposed patches therefore keep the PDFs' 25 November issue dates and separately set `publication_date` to 6 December; they do not claim this was the globally first availability.

The roles are not conflated. ST 14954/22 is a Coreper I-to-Council note whose body says the Czech Presidency prepared the final text and Coreper agreed to submit it without changes; the Council later adopted it. ADD 1 is authored by the **Government of the Federal Republic of Germany**; the Council is recorded only as publisher. The existing `version_of` edge from ST 14954/22 to ST 14336/22 is supported by the cover's `No. prev. doc.: 14336/22`. The ADD 1 `annex_to` edge is supported by its cover and attachment sentence.

## Specific remaining holds

| Document | Exact official metadata/content result | Remaining blocker |
| --- | --- | --- |
| ST 14336/22 | Public; 11 Nov 2022; GSC originator to Coreper; Czech Presidency final compromise; expressly compares ST 13955/22 | No labelled publication date or exact dated release; generic Council author loses GSC/Presidency distinction |
| ST 13955/22 | Public; 3 Nov 2022; Presidency to delegations; final Czech Presidency compromise; previous ST 13102/22 | No labelled publication date or exact dated release |
| ST 10069/22 | Public multilingual 136-page `/x/pdf`; 15 Jun 2022; Presidency; first consolidated compromise; prior ST 9029/22 and Cion doc 8115/21 | URL is repaired, but no labelled publication date or exact dated release |
| ST 13102/22 | Public; 19 Oct 2022; Presidency; fourth compromise; previous ST 12549/22 | No labelled publication date or exact dated release |
| ST 15698/22 | Public; 6 Dec 2022; GSC outcome note; Council adoption independently proven | The dated release links ST 14954/22 and ADD 1, not ST 15698/22; adoption is not publication of this exact outcome document |
| ST 11124/22 | Public; 15 Jul 2022; Presidency; second compromise; previous ST 10069/22 | No labelled publication date or exact dated release |
| ST 12206/22 INIT | Public; **7 Sep 2022**; Presidency; third-compromise part one; changes from ST 11124/22 | Canonical issue date must be corrected; no labelled publication date or exact dated release |
| ST 12206/1/22 REV 1 | Public; 16 Sep 2022; Presidency; explicit REV 1; changes from ST 11124/22 | No labelled publication date or exact dated release |
| ST 12549/22 | Public; 23 Sep 2022; Presidency; final part of third compromise; previous ST 12206/1/22 REV 1 | No labelled publication date or exact dated release |

The live register was also checked for hidden publication labels (`First made public`, `Publication date`, and equivalent field names); none is present in the returned page. Its date alongside each result is the document date. Public status alone does not establish when the exact manifestation became public.

Complete machine-readable patches, evidence locators, the new dated-release source, and the two bounded partial corrections are in `council-2022.json`. No canonical, schema, test, Git or deployment files were changed.
