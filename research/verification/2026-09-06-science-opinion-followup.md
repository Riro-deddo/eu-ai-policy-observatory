# Scientific Opinion No. 15: original-edition recovery and gate reassessment

Candidate: `chief-scientific-advisors-ai-science-opinion-2024`.

Research date: 6 September 2026. PDF retrieval timestamp: `2026-09-06T02:11:26.654360+00:00`. Research-only follow-up to [the earlier memo](2026-09-06-remaining-three/science-opinion.md). No canonical data, inventory decisions, schema, website, GitHub publication or deployment was changed. The earlier memo remains an historical account of that retrieval pass.

## Outcome

**Original full text recovered and compared; admission remains pending on version-specific official evidence.** The original opinion is no longer unavailable for inspection. Two academy-hosted copies supply its complete text and imprint. They corroborate the earlier identification, while the existing EU source rules prevent treating either academy host as an official EU source.

This is not a finding that the document is fictitious or irrelevant. Nor does the approved specification impose a universal requirement to recover every original PDF from an EU server. The unresolved question is narrower: whether eligible official evidence supports the original's exact metadata and its relationship to the corrected edition, or whether a documented supplementary-source policy should be approved. An official correction statement could also resolve this without recovery of EU-hosted original bytes.

## Retrieved evidence

| Copy | Inspected source | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Original, ALLEA | [Original PDF](https://allea.org/wp-content/uploads/2024/04/successful-and-timely-uptake-of-artificial-intelligence-KI0523478ENN.pdf) | 14,379,324 | `fc260a451bed2cee18f438c8ec92badc6f7d48c8c3a563b1d97785fb7e235327` |
| Original, KNAW | [Original PDF](https://storage.knaw.nl/2024-04/Successful-and-timely-uptake-of-artificial-intelligence.pdf) | 2,898,243 | `21833b9e7be4a0cf5ffb23b9d0eb2f55c342271fb4c994f6c4c8d7facf9d7705` |
| Corrected, Publications Office | [Official PDF](https://publications.europa.eu/resource/cellar/d6d8ed54-32a8-11ef-a61b-01aa75ed71a1.0001.01/DOC_1) | 14,846,309 | `df125f19a4673b57f19b93fe6edcd00101b6009160a131838fc1dc14774a5d2d` |

All three direct retrievals returned HTTP 200, a PDF content type and genuine PDF bytes. Each file contains 102 PDF pages. The two academy copies are not byte-identical, but their complete page-by-page extracted text is exactly equal. That result does not establish identical annotations, graphics, links or accessibility tags.

Original imprint, PDF p. 2: first edition; PDF DOI `10.2777/08845`, ISBN `978-92-68-10084-4`, catalogue `KI-05-23-478-EN-N`. Original p. 3 identifies Opinion No. 15 and the issue date 27 March 2024. These fields were inspected in academy-hosted files, not newly recovered from an original EU catalogue.

The [Commission announcement](https://research-and-innovation.ec.europa.eu/news/all-research-and-innovation-news/commission-receives-scientific-advice-artificial-intelligence-uptake-research-and-innovation-2024-04-15_en) explicitly records release on 15 April 2024, identifies the opinion and describes non-binding independent advice. The current [official corrected catalogue](https://op.europa.eu/en/publication-detail/-/publication/d6d8ed54-32a8-11ef-a61b-01aa75ed71a1/language-en) records release on 21 June 2024 and DOI `10.2777/46863`. The release dates refer to different publication manifestations and must not be conflated.

## Comparison result and its limits

Every page was text-extracted with the same `pypdf` runtime. Corresponding pages were compared after removing whitespace. There are 22 changed page pairs: 1, 2, 4, 5, 8, 9, 10, 13, 14, 27, 32, 34, 38, 40, 41, 44, 45, 47, 48, 69, 75 and 81. These are changed pages, not 22 substantive corrections. They include covers, imprint, contents, punctuation and pagination effects.

Three clear wording changes were independently verified by viewing complete rendered pages in both editions:

- PDF p. 13 / printed p. 11: the opening description adds a qualification about less uncertain predictions.
- PDF p. 27 / printed p. 25: the ERC passage removes the reference to human third parties as a source of researchers' input.
- PDF p. 34 / printed p. 32: the science-for-policy box adds false information to the potential consequences discussed alongside inequities.

The correction therefore cannot be described as typography-only. This is researcher-produced comparison evidence, not an official correction schedule, a complete semantic assessment, or proof of the publisher's reason for each edit. No publisher correction schedule was located in this bounded search. The SAPEA evidence review report's contributor-name correction concerns a different work and must not be substituted for the opinion's correction history.

Working evidence is retained in `work/science-opinion-followup-20260906/`: three PDFs, `compare_opinions.py`, `comparison-manifest.json`, and `academy-original-comparison.md`. The main reviewer independently recomputed the hashes, reproduced all 22 changed page numbers and equality of academy text, and visually inspected pages 2, 13, 27 and 34 in both editions. Poppler reported missing optional display fonts, but the inspected imprint and relevant passages rendered legibly. No complete 102-page visual audit is claimed.

## Additional official route checked

The Commission's [expert-group register, E03378](https://ec.europa.eu/transparency/expert-groups-register/screen/expert-groups/consult?groupID=3378&lang=en) was inspected in an ordinary browser. Additional Information supplied institutional, selection and procedural material, but no original opinion attachment. The Meetings tab displayed no results. The linked SAM meeting list did not expose a retrieved original or correction notice in this pass. These are bounded observations, not proof that no other official copy exists. No challenge was bypassed and no external correspondence was sent.

## Admission-rule interpretation

The approved historical specification, section 5.1, requires the stated issue date when available and official evidence for dates. Section 5.2 requires an evidenced version relationship. The data dictionary requires official metadata to come from an inspectable official English source. The implementation currently accepts official source URLs only over HTTPS on `europa.eu` or its subdomains; analytical version relationships also need official evidence and published endpoints.

Consequently:

1. Do not place ALLEA or KNAW in the canonical source list as if they were EU hosts. Retain their identity and comparison evidence transparently in research notes.
2. Do not replace the known 27 March issue date with 15 April just to use a publication-date fallback. The latter is a separately verified release date, not a substitute issue date.
3. Optional identifiers may be omitted if genuinely unverified, but omission alone does not resolve the date or version-evidence question.
4. A corrected PDF's facts must not silently be attributed to the original edition. Applicability to that specific version needs explicit justification.
5. Passing software validation would not, by itself, establish that the cited source supports a fact.

The previous memo's demand for an EU-hosted original PDF was one possible resolution path, not the only path established by the approved specification. A follow-up admission decision should use either sufficient version-specific official documentation or an explicitly approved, narrowly defined supplementary-source policy for preserved institutional copies with independent official publication evidence. No such exception is implemented or assumed here.
