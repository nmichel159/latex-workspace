# Submission

From finished manuscript to submitted, preprinted and revised paper. Venue-specific rules (template, limits,
anonymity, fees): [../venues/README.md](../venues/README.md). Paper structure: [paper-structure.md](paper-structure.md).
Template moves: [template-porting.md](template-porting.md). Tick list: [checklist.md](checklist.md).
Thesis and UPJŠ rules on AI: [thesis.md](thesis.md).

Every row and rule that describes an outside policy was read on the cited page on 2026-10-08. Policies change
several times a year: re-open the URL before each submission and update the row.

## 1. Generative-AI policies

### 1.1 Policy table (checked 2026-10-08)

| Body | AI as author | Disclosure: when, where, form | Grammar / copy-editing | AI-generated figures | Reviewers | Policy |
|---|---|---|---|---|---|---|
| **Elsevier** (DAM, TCS, IPL) | no | at submission; separate section at the end of the manuscript, before the references, headed *Declaration of generative AI and AI-assisted technologies in the manuscript preparation process*; name tool, purpose, human oversight; template sentence provided; AI used in the research goes to Methods | basic grammar, spelling, punctuation checks and non-generative reference managers exempt; substantive rewording of sentence structure must be declared | explanatory images (flow charts, schematics) allowed with caption disclosure; data visualisations only if reproducible from data, described in Methods; no AI in primary research images; no general-purpose genAI in graphical abstracts | must not upload a manuscript or any part of it; private tools only, supportive role; disclose in the report | [policy](https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals) ("Policy updated June 2026") |
| **Springer Nature** (Algorithmica, JOCO, MPC; LNCS: see [card](../venues/lncs.md)) | no (listed as not permitted) | AI declaration in the manuscript; for every permitted use "clearly describe use and confirm author accountability"; visuals: disclosure in caption or legend; central page: section not named; Algorithmica's guidelines (JOCO and MPC cards: same text): LLM use documented in the Methods section or a suitable alternative part | central page: no exemption, language editing, readability, formatting, translation are low-risk uses that still require a description; Algorithmica's guidelines: AI-assisted copy editing (readability, grammar, style, no generated content) need not be declared | AI visuals not derived from verifiable data not permitted; charts from data, diagrams from author content, figures from verified code allowed | no upload to public or unsecured tools; no AI-generated reports or recommendations; declare supporting use | [manuscript preparation](https://www.springernature.com/gp/policies/editorial-policies/ai-manuscript-preparation), [peer review](https://www.springernature.com/gp/policies/editorial-policies/using-ai-in-peer-review), [Algorithmica guidelines](https://link.springer.com/journal/453/submission-guidelines) |
| **IEEE** (TEVC) | page silent | Acknowledgments section; name the AI system, the sections that use AI-generated content (text, figures, images, code), and the level of use | editing and grammar enhancement "generally outside the intent"; disclosure not required but recommended; keep the reference list out of AI editing | covered by the general disclosure rule; no separate rule | no processing of manuscript content through a public AI platform (confidentiality) | [submission and peer-review policies](https://journals.ieeeauthorcenter.ieee.org/become-an-ieee-journal-author/publishing-ethics/guidelines-and-policies/submission-and-peer-review-policies/) |
| **ACM** (TELO; GECCO proceedings) | no (authors must be identifiable humans) | AI used to conduct the research (design, data, code, experiments, analysis, AI-dependent charts) described in detail in the methods section; AI used to assist with writing: no disclosure required since the 2026-05-14 update | writing assistance needs no disclosure | AI-dependent charts and figures: methods section | may use genAI only to improve readability of their own report, after removing anything identifying or confidential | [authorship](https://www.acm.org/publications/policies/new-acm-policy-on-authorship), [peer review](https://www.acm.org/publications/policies/peer-review) |
| **SIAM** | no (authors must be human) | "Acknowledgements" or "Declarations" section, plus the sentence *The authors assume responsibility for all content.*; diligence expected for literature summaries, proofs, code, synthetic data, figures, citations | grammar checking generally need not be disclosed | figures should come from verifiable, reproducible processes | must not share papers with genAI tools in any form | [Version 2.0, effective May 2026](https://epubs.siam.org/artificial-intelligence) |
| **Wiley** (JGT, Networks) | no | Acknowledgments for drafting, editing, translation, formatting; Methods for design, analysis, code, literature review; figure captions for visuals; give tool name and version, date or year, role, affected sections, author's role; prompts may be requested | simple grammar and spelling, word choice, formatting, citation formatting typically exempt; translation and reorganising arguments must be disclosed | AI-edited photographs and evidential images not permitted; AI visualisations and illustrations disclosed in caption | no upload in full or in part; may polish own review; disclose drafting help | [AI guidelines](https://www.wiley.com/en-us/publish/article/ai-guidelines/) |
| **Taylor & Francis** | no | any genAI use; full tool name with version, how and why it was used; section not named for articles | language improvement is a supported use; no exemption from disclosure stated | allowed for data visualisations, conceptual illustrations, flow diagrams; not for research results | no upload; no AI-generated review reports; language polishing allowed | [AI policy](https://taylorandfrancis.com/our-policies/ai-policy/) |
| **AMS** | no | adopts the COPE text: Materials and Methods "(or similar section)"; how the tool was used and which tool | none stated | disclosure covers images and graphical elements | editors and referees must not upload papers under review to an LLM in any form | [Use of AI](https://www.ams.org/publications/journals/policies/UseofArtificialIntelligence) |
| **INFORMS** (IJOC) | TODO(verify) | TODO(verify): the IJOC policy is in its author guidelines; pubsonline.informs.org was behind a bot check on 2026-10-08 | TODO(verify) | TODO(verify) | IJOC (2023): no upload of manuscripts, reports or letters to genAI, not even for language polishing | [INFORMS Connect post, 2023-08-27](https://connect.informs.org/discussion/generative-artificial-intelligence-ai-policy-for-reviewers-associate-editors-department-editors-editors-for-informs-journals) |
| **arXiv** | no (also in author metadata) | report significant use of text-to-text genAI following the field's methodology norms; authors fully responsible for errors, plagiarism, wrong references | not addressed | not addressed | n/a | [moderation policy](https://info.arxiv.org/help/moderation/index.html), [metadata](https://info.arxiv.org/help/prep.html) |
| **NeurIPS 2026** | no ("agents and LLMs cannot be authors") | LLM use that is an important, original or non-standard part of the method: experimental setup section (or equivalent); paper checklist mandatory | spell and grammar checkers, editing aids, basic code assistance need not be documented | no separate rule; authors responsible for figures | no LLM use except a sanctioned LLM on papers where it is enabled; no sharing with unsanctioned LLMs | [Main Track Handbook](https://neurips.cc/Conferences/2026/MainTrackHandbook) |
| **ICML 2026** (2027 call not online on 2026-10-08) | no | encouraged, not required: explain notable uses in the methodology; prompt injection forbidden (desk rejection) | not required | no separate rule | separate policy: icml.cc/Conferences/2026/LLM-Policy, TODO(verify) content | [Call for Papers](https://icml.cc/Conferences/2026/CallForPapers) |
| **ICLR 2027** | page silent | mandatory AI disclosure section in the paper (outside the page limit) and in the submission form; required for synthetic data, formulating mathematical claims, implementing methods, data cleaning, interpreting results | editing for readability: disclosure recommended, not required | creating figures: disclosure recommended | limited use allowed; must submit own original assessment and all LLM interactions | [authors](https://iclr.cc/Conferences/2027/AIPolicyForAuthors), [reviewers](https://iclr.cc/Conferences/2027/AIPolicyForReviewers) |
| **AAAI** | no; AI systems may not be cited as a source either | any AI use allowed only if its role is documented in the manuscript | no exemption stated | not addressed separately | no prompting LLMs with submissions; tools may improve wording, not generate content | [publication policies](https://aaai.org/aaai-publications/aaai-publication-policies-guidelines/) |
| **GECCO** (ACM SIGEVO) | no | any genAI assistance disclosed in the Acknowledgments; AI detection may be used | not exempt (stricter than ACM's own 2026 rule) | not addressed | no upload or sharing; may improve readability of the report | [GECCO 2026 instructions](https://gecco-2026.sigevo.org/Paper-Submission-Instructions), [GECCO 2027 call](https://gecco-2027.sigevo.org/Call-for-Papers) |
| **COPE** (position, last reviewed 2023-02-13) | no | Materials and Methods (or similar section): how and which tool | none stated | disclosure covers images and graphical elements | n/a | [Authorship and AI tools](https://publicationethics.org/guidance/cope-position/authorship-and-ai-tools), doi:10.24318/cCVRZBms |

### 1.2 Common denominator

Follow these and no venue above is violated. Where a venue is stricter, the venue wins.

1. Never list an AI tool as author and never cite it as the source of a claim.
2. Disclose every generative-AI use beyond spelling and grammar checking, even where the venue does not require it
   (ACM, NeurIPS). Disclosure costs one paragraph; a missing one can mean rejection (SIAM, ICLR, GECCO).
3. State: tool and version, provider, purpose, affected parts, how the output was checked, and that the author takes
   full responsibility.
4. Separate writing assistance (declaration or acknowledgments) from AI used in the research (methods or experimental
   setup, with model, version, date, prompts and parameters; see [experiments-reporting.md](experiments-reporting.md)).
   For the owner's LLM-driven optimisation work the second kind is the method itself and is never "just assistance".
5. No AI-generated pictures of data. Figures come from code (TikZ, pgfplots, plotting scripts kept in the project).
6. Check every reference and every AI-touched definition, proof and algorithm statement yourself; SIAM states that
   authors, not referees, bear this responsibility.
7. Keep a log of prompts and outputs for AI-assisted parts in `projects/<p>/submission/` (Wiley may request
   prompts); that folder is left out of the package ([latex-conventions.md](latex-conventions.md) §1.1).
8. Keep the same statement in the arXiv version (arXiv asks for disclosure of significant use).
9. As a reviewer: never paste a manuscript or a report into a public AI tool. Every body above forbids it.

### 1.3 Disclosure statement (template)

Default wording for "an AI assistant helped with language editing and LaTeX typesetting; the author reviewed all
content and takes full responsibility". Single author; for several authors use *the authors ... take*.

```latex
\section*{Declaration of generative AI use}
During the preparation of this work the author used [TOOL, VERSION] ([PROVIDER]) to improve the language of the
manuscript and to assist with LaTeX typesetting. The tool did not generate research ideas, results, proofs or
references. The author reviewed and edited all output and takes full responsibility for the content of the
publication.
```

Adapt per venue:

| Venue | Change |
|---|---|
| Elsevier | heading *Declaration of generative AI and AI-assisted technologies in the manuscript preparation process*; a new section before the reference list; where the guide also wants the acknowledgements directly before the reference list (DAM), the declaration goes before the acknowledgements |
| Springer Nature journals | keep the wording; Algorithmica: in the Methods section or a suitable alternative part ([guidelines](https://link.springer.com/journal/453/submission-guidelines), card checked 2026-10-08; the JOCO and MPC cards report the same text); other Springer journals: TODO(verify) |
| IEEE | move the paragraph into Acknowledgments; add which sections were edited ("Sections 1-5") and that use was limited to language and typesetting |
| ACM journals | optional for writing help; keep it in Acknowledgments if the venue asks (GECCO does) |
| SIAM | Acknowledgements or Declarations; end with *The authors assume responsibility for all content.* (SIAM's exact sentence) |
| Wiley | Acknowledgments; add the year of use and the affected sections |
| Taylor & Francis | name the full tool with version and say why it was used |
| AMS, COPE-based journals | a paper without a Methods section: a short unnumbered section *Use of AI tools* before the references (the "similar section"), TODO(verify) with the journal |
| ICLR | put the text into the mandatory AI disclosure section; list any required-category use |
| NeurIPS, ICML | not required for language help; keep one sentence after the acknowledgments (camera-ready) or in the checklist |
| Double-anonymous review | keep the statement, drop names of people and institutions from it |

File convention (House rule):

- Manuscript: the statement is text only in `sections/91-ai-declaration.tex`; the wrapper gives the venue's heading
  (`\section*{...}`) and the `\input` line, after the last section and before the acknowledgments, so the
  acknowledgments stay directly before the references (Elsevier, DAM card). A venue that wants the statement inside
  the acknowledgments or the back matter (table above) gets it there instead.
- Draft: until the owner inserts it, the statement stays in `projects/<p>/submission/ai-declaration.tex`, which is
  never packaged. The owner decides whether and when it moves into `sections/`.
- Packager: an AI tool name is allowed only in the text (not the comments) of a file named `*ai-declaration*.tex`
  (the thesis: `*ai-statement*.tex`) that the main file reads, in the printed declaration of the staged PDF, or by
  `submission/package-allow.txt`; anywhere else it fails as `[trace]`, and so does a placeholder of the template
  (`[TOOL, VERSION]`, `[PROVIDER]`, `[MODEL AND VERSION]`, `[NAME OF TOOL / SERVICE]`, `[REASON]`). Every run prints `AI declaration: ...`
  before the verdict, with a reminder when the manuscript has no such section
  ([latex-conventions.md](latex-conventions.md) §1.1, point 4).

## 2. arXiv

Source: arXiv help pages, all checked 2026-10-08.

### 2.1 Before the first submission

| Rule | Detail | Source |
|---|---|---|
| Endorsement | needed before the first paper in a category. Since 2026-01-21 an institutional e-mail is not enough: automatic endorsement needs an institutional e-mail **and** prior authorship of a paper already on arXiv in that domain; otherwise ask an established author for personal endorsement (six-character code). The owner has no arXiv paper yet: plan for personal endorsement in cs or math | [endorsement](https://info.arxiv.org/help/endorsement.html), [blog 2026-01-21](https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/) |
| Rate limit | since 2026-10-01: at most 2 new submissions per submitter per calendar month and 3 active at a time; rejected ones count; co-authors not counted; replacements not addressed | [blog 2026-10-01](https://blog.arxiv.org/2026/10/01/updated-rate-limit-policy/) |
| Content type in cs | review articles and position papers in cs are accepted only after peer review at a journal or conference (journal reference and DOI required); research articles unaffected | [blog 2025-10-31](https://blog.arxiv.org/2025/10/31/attention-authors-updated-practice-for-review-articles-and-position-papers-in-arxiv-cs-category/) |
| Generative AI | AI cannot be an author; report significant use; authors carry full responsibility | [moderation](https://info.arxiv.org/help/moderation/index.html) |

### 2.2 Format and processing

The bundle for arXiv is the packager's zip made without `-Flat` (§3.2 step 3): sub-folders kept, `.bbl` included.

| Topic | Rule | Source |
|---|---|---|
| Source vs PDF | TeX/LaTeX source is the preferred format; arXiv does not accept PDF, PS or DVI created from TeX source | [submit](https://info.arxiv.org/help/submit/index.html) |
| TeX Live | TeX Live 2025 (default) and 2023 selectable; all past trees kept so old papers rebuild | [texlive](https://info.arxiv.org/help/faq/texlive.html) |
| Engines | processors: plain TeX, LaTeX (DVI mode), LaTeX (PDF mode), PDFLaTeX; `00README.json` also lists `xelatex`, while the mistakes page still calls XeTeX and LuaTeX unsupported. House rule: submit pdfLaTeX only | [submit_tex](https://info.arxiv.org/help/submit_tex.html), [00README](https://info.arxiv.org/help/00README.html), [mistakes](https://info.arxiv.org/help/faq/mistakes.html) |
| Bibliography | an uploaded `.bbl` is used as is; its name must match the main `.tex`. Without `.bbl` arXiv runs BibTeX, or the backend configured for biblatex (biber, bibtex, bibtex8); a missing `.bib` blocks submission | [submit_tex](https://info.arxiv.org/help/submit_tex.html) |
| biblatex versions | TL2025: biblatex 3.20, Biber 2.20, `.bbl` format 3.3 (only 3.3 accepted); TL2023: biblatex 3.19, Biber 2.19, format 3.2 (3.2 and 3.3 accepted). Local MiKTeX (2026-10-08): biblatex 3.21, biber 2.21, format 3.3, so a local `.bbl` passes the format check. A biblatex `.bbl` must come from the same backend the document requests | [submit_tex](https://info.arxiv.org/help/submit_tex.html); local `biblatex.sty` |
| Archives and folders | `.zip` or `.tar.gz`; sub-directories allowed; the main file may sit in a sub-directory but compilation always runs from the root, so `\input` paths are root-relative. Files read with `\include` must be in the top directory (sub-directories are not writable during processing); use `\input` for `sections/*.tex` | [submit_tex](https://info.arxiv.org/help/submit_tex.html), [mistakes](https://info.arxiv.org/help/faq/mistakes.html) |
| File names | only `a-z A-Z 0-9 _ + - . , =`; case-sensitive; no spaces; relative paths only | [submit](https://info.arxiv.org/help/submit/index.html), [mistakes](https://info.arxiv.org/help/faq/mistakes.html) |
| Figures | PDFLaTeX: PDF, PNG, JPEG; DVI mode: PS/EPS only; no conversion on arXiv, so ship the `*-eps-converted-to.pdf` files or convert yourself; one format family per paper; `psfig` unsupported | [submit_tex](https://info.arxiv.org/help/submit_tex.html) |
| Size | no number stated; images above 34 megapixels trigger a warning (since 2026-02); photos as JPEG, diagrams as PDF/PNG; figures may not be omitted | [sizes](https://info.arxiv.org/help/sizes.html) |
| Packages | only what TeX Live contains; ship any other `.sty`/`.cls`/`.bst` (journal classes!) | [submit_tex](https://info.arxiv.org/help/submit_tex.html) |
| hyperref | load without a driver option such as `[pdftex]` | [submit_tex](https://info.arxiv.org/help/submit_tex.html) |
| Date | do not use `\today` in `\date`: the date changes when arXiv rebuilds the PDF | [submit_tex](https://info.arxiv.org/help/submit_tex.html) |
| JavaScript | a PDF with embedded JavaScript is rejected | [submit_tex](https://info.arxiv.org/help/submit_tex.html) |

### 2.3 00README

Since submission system 1.5 arXiv writes `00README.json` itself; write one only to fix the top-level file, ignore
files, pin TeX Live or turn off the stamp. Example (keys from the
[00README page](https://info.arxiv.org/help/00README.html)):

```json
{
  "spec_version": 1,
  "process": { "compiler": "pdflatex" },
  "texlive_version": 2025,
  "sources": [
    { "filename": "main.tex", "usage": "toplevel" },
    { "filename": "response-to-reviewers.tex", "usage": "ignore" }
  ]
}
```

### 2.4 Typical failures

From the [mistakes page](https://info.arxiv.org/help/faq/mistakes.html) and [submit_tex](https://info.arxiv.org/help/submit_tex.html):

| Symptom | Fix |
|---|---|
| file not found | relative paths; exact case; no spaces or special characters |
| missing `.sty`/`.cls` | ship the journal class and any non-TeX-Live package |
| `.bbl` version error | ship a `.bbl` built by BibTeX, or by biber/biblatex with format 3.3 |
| figure missing or wrong type | PDF/PNG/JPEG only with pdfLaTeX; no on-the-fly EPS conversion |
| `\include` write error | `\include` files in the top directory, or use `\input` |
| `Command \Bbbk already defined` | `newtxmath` vs `amssymb`: load order, or `\let\Bbbk\relax` before the second |
| `minted` fails | `--shell-escape` is off and hidden directories are deleted at announcement; use `listings` |
| "line too long" from `\cite` in captions | `\protect\cite` |
| bad bookmarks | `hyperref` option `bookmarks=false` |
| interactive prompt | processing is automatic; a document that stops for input fails |

### 2.5 Metadata

| Field | Rule ([prep](https://info.arxiv.org/help/prep.html)) |
|---|---|
| Title | no all-caps, no Unicode; TeX accents allowed |
| Authors | `First Last`, full list, no titles or degrees, affiliation in parentheses (city and country at most); TeX accents allowed: `Norbert Miche\v{l} (Pavol Jozef \v{S}af\'arik University in Ko\v{s}ice)` |
| Abstract | at most 1,920 characters; no word "Abstract"; no Unicode; no font or spacing commands |
| Comments | pages, figures, "submitted to"/"to appear in"; on replacement say what changed; no copyright statements |
| MSC-class (math) | e.g. `05C85 (Primary) 68Q25, 05C40 (Secondary)` - codes TODO(verify) against MSC2020 |
| ACM-class (cs) | ACM CCS codes separated by `; ` |
| Journal-ref, DOI | only after publication, with full data (journal, volume, year, pages); DOI without `doi:` prefix; no new version needed ([jref](https://info.arxiv.org/help/jref.html)) |

### 2.6 Licences

Offered ([license](https://info.arxiv.org/help/license/index.html)): arXiv perpetual non-exclusive licence 1.0,
CC BY 4.0, CC BY-SA 4.0, CC BY-NC-SA 4.0, CC BY-NC-ND 4.0, CC0. Metadata is always CC0.

| Choice | Consequence |
|---|---|
| arXiv non-exclusive 1.0 | arXiv may distribute; others may not reuse; author keeps copyright; compatible with every publisher below |
| CC BY 4.0 | maximal reuse; many publishers accept CC BY preprints (arXiv's words), but check the target journal first |
| CC BY-NC-ND 4.0 | the licence Elsevier requires when an accepted manuscript replaces the arXiv preprint |
| CC0 | gives up copyright; conflicts with many publishers |

The licence of a version is irrevocable; a later version may carry a different licence. House default: arXiv
non-exclusive licence for v1 unless a funder requires CC BY.

### 2.7 Versions

- Replace at most once a week; all earlier versions stay public ([replace](https://info.arxiv.org/help/replace.html)).
- Every content or comment change creates a new version; journal reference, DOI and report number do not.
- After acceptance: replace with the accepted manuscript only where the publisher allows it (section 6), then add
  the DOI and journal reference once published.

### 2.8 Categories

From the [taxonomy](https://arxiv.org/category_taxonomy). Candidates for the owner's topics:

| Category | Covers | Typical use |
|---|---|---|
| `cs.DM` Discrete Mathematics | combinatorics, graph theory, applications of probability | Min Cut-Path (primary candidate) |
| `math.CO` Combinatorics | discrete mathematics, graph theory, enumeration, combinatorial optimization | Min Cut-Path, lattice polytopes |
| `cs.DS` Data Structures and Algorithms | algorithm design and analysis | polynomial cases, algorithms |
| `cs.CC` Computational Complexity | models, classes, bounds | NP-completeness results |
| `math.PR` Probability | random structures, limit theorems | random-graph results (cross-list) |
| `math.OC` Optimization and Control | operations research, linear programming | optimisation methods |
| `cs.NE` Neural and Evolutionary Computing | neural networks, genetic algorithms | LLM-driven evolutionary search |
| `cs.AI` Artificial Intelligence | general AI except areas with their own category | LLM-based optimisation |
| `cs.LG` Machine Learning | all of ML, also as primary for ML applications | LLM-based optimisation |

Moderators may reclassify or change cross-lists ([moderation](https://info.arxiv.org/help/moderation/index.html)).

## 3. Submission package

Venue limits, anonymity, files and statements: the card in [../venues/](../venues/README.md). Pages opened
2026-10-08: **E** = Elsevier [LaTeX instructions](https://www.elsevier.com/researcher/author/policies-and-guidelines/latex-instructions),
**S** = Springer Nature [LaTeX author support](https://www.springernature.com/gp/authors/campaigns/latex-author-support).

### 3.1 What is uploaded

| Item | Journal | Conference | arXiv (§2) |
|---|---|---|---|
| PDF | built locally; most Elsevier journals accept a PDF at initial submission (E), DAM asks for editable `.tex`; Algorithmica, JOCO: PDF plus all sources every time; IJOC: PDF, sources optional (cards) | the only review file; class, options and page or line limit of the call | refused when made from TeX |
| Sources | `.tex`, `.cls`, `.bst`, own `.sty`, figures, `.bbl`, `.bib` in **one flat folder** (packager switch `-Flat`, §3.2 step 3): Editorial Manager cannot process sub-folders, compiles the sources itself and returns only an error log when the build fails (E). Springer: single directory; no custom fonts; diacritics as TeX code; TeX Live 2018 (Editorial Manager), 2017 (eJP), 2021 (Article Processing Platform, https://submission.nature.com/, which Algorithmica uses); `.bbl` or `.bib` with `.bst`, most reliable the `.bbl` pasted into the main file: stated for Editorial Manager and eJP only, no bibliography rule for the Article Processing Platform; "Snapp" needs pdfLaTeX and a `.zip`, but the page does not say which system Snapp is (S) | not at submission; camera-ready as the proceedings publisher asks (LIPIcs: `.bib` required, a `.bbl` alone is not enough: card) | sub-folders allowed; `.bbl` used as is |
| Supplement | separate files, each cited in the text; code and data where the card demands release (IJOC, MPC) | appendix or one archive as the call says, anonymized like the paper | - |
| Statements, extras | per card, in the manuscript or the form: competing interests, funding, data and code availability, author contributions ([CRediT](https://credit.niso.org/): 14 fixed roles), AI use (§1). Elsevier highlights (separate file, 3-5 bullets of at most 85 characters): required by IPL, encouraged by DAM and TCS (cards) | per call: AI statement (ICLR), paper checklist (NeurIPS) | AI statement kept (§1.2); `00README.json` (§2.3) |
| Form: title, abstract, keywords, codes, authors | House rule: one file `projects/<p>/submission/metadata.txt`, pasted into every form, so form, PDF and arXiv agree. Abstract as plain text: no commands, citations or macros; formulas as text (`cp(u,v) = c(u,v) + d(u,v) - 1`). No title words among the keywords ([paper-structure.md](paper-structure.md) §3). MSC 2020 and ACM CCS from the official lists, never from memory ([template-porting.md](template-porting.md) §2). Name, affiliation, ORCID: §6.3 | same | TeX accents, no Unicode (§2.5) |
| Form: reviewers | Elsevier: suggested = name, institution, e-mail; opposed = name, institution, reason; not every journal offers it; the editor decides ([support page](https://www.elsevier.support/publishing/answer/how-can-i-suggest-or-oppose-reviewers-for-my-submission), updated 2025-11-20). House rule: suggest only authors of work the paper cites who share no paper, institution or supervision with the author (never the supervisors in [../author.md](../author.md)); e-mail copied from the person's institutional page, else leave the field empty; oppose only with a stated conflict | - | - |

### 3.2 Procedure (House rule)

`<p>` = project; commands run from the workspace root in PowerShell. Uploading is the owner's step. The source
package is made and proved by the packager, never by hand (invariant, switches and findings:
[latex-conventions.md](latex-conventions.md) §1.1); the steps below add what the script does not do.

1. Re-open the URLs of the venue card and update it ([../venues/README.md](../venues/README.md), rule 1). The owner
   confirms "Content changes to review" in the project README.
2. Source: draft switch off, todonotes `disable` ([latex-guide.md](latex-guide.md) §13); statements of §3.1 present;
   PDF title and author set (§4 there), author empty for double-anonymous review. Then the machine checks, the whole
   [checklist.md](checklist.md) and the clean-build table of [latex-conventions.md](latex-conventions.md) §2.
3. Package:

   ```powershell
   .\scripts\package-project.ps1 -Project <p> -Template <venue> [-MaxPages <n>] [-Flat]
   ```

   `-Template`: the folder of the venue's template under `templates/`. `-MaxPages`: the limit on the card. `-Flat`:
   the system builds from one directory (Elsevier, Springer: §3.1); not for arXiv, which keeps sub-folders (§2.2).
   Continue only on `Verdict: PASS`; a finding is fixed in `projects/<p>/` and the script is run again. Read the
   `[comment]` and `[unused]` lists and the allowed `[trace]` notes even on PASS, and check the line
   `AI declaration:` against the venue's policy (§1.3). The zip carries no workspace or tool trace and the venue
   template is a recorded download (`[trace]`, `[template-origin]`). Result: `outputs/<p>/package/<p>-<yyyyMMdd>.zip` (`-flat.zip`),
   `.bbl` inside, the PDF beside it. Not done by the script: the content of `main.bbl` in place of the
   `\bibliography` line (S calls it the most reliable form for Editorial Manager and eJP and states no rule for the
   Article Processing Platform; the zip carries the `.bbl`); one `.tex` file, which the sn-jnl sample asks for and
   Algorithmica's guide does not (open: [template-porting.md](template-porting.md) §6.3).
4. Double-anonymous venue: §3.3, on the packager's PDF and zip. A hit is fixed in the project; then step 3 again.
5. Upload set: the zip and the PDF from `outputs/<p>/package/`, plus the files the script does not make: cover
   letter (§4), highlights and supplement (§3.1), response letter and marked PDF in a revision (§5). Nothing is
   zipped or re-zipped by hand: `Compress-Archive` of Windows PowerShell 5.1 names entries with a backslash
   (`sections\01-a.tex`, tested 2026-10-08), which matters for arXiv bundles, and a build log holds paths with the
   Windows user name.
6. Freeze: `archives/submissions/<p>/<YYYY-MM-DD>-<venue>-<stage>/` (stage `v1`, `r1`, `final`, `arxiv-v1`) with
   `upload/` (every uploaded file: the packager's zip and PDF copied from `outputs/<p>/package/`, cover letter and
   `metadata.txt` included) and `source/` (copy of `projects/<p>/`, the old side of the next diff, §5.3). Never edit
   it. Add a row to `archives/README.md`; record venue, date and manuscript number in the project README (§6.2).
7. After the owner's upload: compare the PDF the system built with `upload/` (pages, `??`, figures) before approving.

### 3.3 Anonymization sweep (double-anonymous venues)

| Place | Requirement |
|---|---|
| title block | the class's anonymous option (card); no name, affiliation, e-mail, ORCID, `\thanks`, grant number |
| acknowledgments, funding | removed; the AI statement stays, without names (§1.3) |
| text | no first-person reference to own work; own papers and the thesis in the third person (*Micheľ [5] shows*); the arXiv version neither cited nor linked (§6.1). The second command below may hit only such citations and their reference entries |
| code and data | supplementary archive or an anonymizing mirror, never the author's account ([../author.md](../author.md)); no `.git` folder |
| files | no surname in PDF, archive or figure names; `pdfinfo img/<figure>.pdf` shows no Author |

Run in Git Bash from the workspace root on what the packager wrote (§3.2 step 3): `F` = the PDF beside the zip,
`Z` = the zip. A hit is fixed in `projects/<p>/`, then the packager runs again.

```bash
pdfinfo "$F" | grep -i author               # empty value: clear pdfauthor in \hypersetup
pdftotext -enc UTF-8 "$F" - | grep -n -i -E "miche|upj|af.{1,2}rik|ko.{1,2}ice|loebl|semani|our (earlier|previous)|in our"
unzip -o -q "$Z" -d tmp/sweep-<p> && grep -r -i -l -E "miche|norom|upjs" tmp/sweep-<p>   # also the supplement; norom = Windows user name in paths
```

## 4. Cover letter

**TF** = Taylor & Francis
[cover letter guide](https://authorservices.taylorandfrancis.com/publishing-your-research/making-your-submission/writing-a-journal-article-cover-letter/),
opened 2026-10-08 like every page linked in this section.

| Submission | Letter |
|---|---|
| journal, first submission | when the card requires it or the system has the field (some systems take it in a text box, not as a file: TF). IJOC requires it and prescribes its content ([card](../venues/informs-joc.md)); DAM, TCS, IPL: TODO(verify), the guide for authors returned HTTP 403 on 2026-10-08 |
| journal, revision | three lines: manuscript number, "revised version", pointer to the response letter (§5) |
| conference, arXiv | none: no conference card lists one; arXiv has the Comments field (§2.5) |

The editor reads it to judge scope, assign a handling editor and see the declarations; IJOC shows it to editors
only (card). Assume that everywhere: nothing the reviewers need goes into it.

Parts in order; at most one page (TF), House rule: at most 200 words. Draft:
`projects/<p>/submission/cover-letter.txt`, so it stays out of the package (§3.2).

1. Salutation: the editor by name from the journal page, else *Dear Editor*; title, article type from the card,
   journal (TF).
2. Result: problem and main result in two or three sentences with the class, bound or number
   ([academic-style.md](academic-style.md) §3.3); never the abstract pasted (TF).
3. Fit: one sentence naming a scope item of the journal or one or two of its papers on the topic (required by IJOC).
4. Declarations: not published and not under consideration elsewhere (TF; TEVC: field *Comments to
   Editor-in-Chief*); related versions (table below); competing interests (TF); funding or unpublished work the
   paper relies on where the card puts them in the letter (IJOC, JOCO).
5. Requests, only real ones: special issue, agreed exception to a limit (IJOC), opposed reviewer when the form
   has no field. Then name, affiliation, university e-mail (§6.3).

Never: praise words or a novelty claim without a logged search ([academic-style.md](academic-style.md) §3.6, §6);
impact factor, career or deadline arguments; earlier rejections unless the form asks; jargon (TF); an AI statement
that replaces the one in the manuscript (§1). A single author writes *I* in the letter; *we* stays in the paper.

| Related version | Add to the declarations |
|---|---|
| master's thesis | the thesis with its reference number; what the paper adds or corrects. Elsevier does not count an academic thesis, an abstract or an electronic preprint as prior publication; society-owned titles may differ ([post of 2016-01-27](https://www.elsevier.com/connect/clarification-of-our-policy-on-prior-publication)). Springer Nature: TODO(verify), not on the pages opened. House rule: declare it everywhere; article 1 shares paragraphs with the thesis ([academic-style.md](academic-style.md) §9), and undeclared overlap reads as duplicate publication |
| conference abstract (CSGT 2026) | title, event, URL, "abstract without proofs"; its type is `TODO(verify)` in [../author.md](../author.md) |
| proceedings paper | cite it in the paper and in the letter; list what is new; attach what the card's *Prior publication* field asks (IJOC: original paper, one-page summary, highlighted version; DMTCS: title footnote; TELO: at least 30 percent new material) |
| preprint | arXiv identifier (§6.1) |
| rejected elsewhere | House rule: revise by the old reports first; submit only after the decision or a withdrawal (Springer Nature: one journal at a time, [editorial policies](https://www.springernature.com/gp/policies/editorial-policies)); do not name the earlier venue unless the form asks. Same journal again: old manuscript number, a response to the old reports (§5), permission where the card demands it (IJOC) |

```text
Dear Professor [Surname],                                  (or: Dear Editor,)

I submit the manuscript "[Title]" for publication in [Journal] as a [article type].
[Problem in one sentence.] [Main result with the class, bound or number.] [Fit: scope item or a paper of the journal.]

The manuscript has not been published and is not under consideration elsewhere. [It is based on my master's
thesis [n] (Charles University, 2025) / extends the abstract presented at [event] [n]; new in the manuscript:
[...].] [A preprint is available as arXiv:[id].] I have no competing interests to declare. [Funding: [...].]

Sincerely,
Norbert Micheľ, Institute of Computer Science, Faculty of Science,
Pavol Jozef Šafárik University in Košice, Slovakia; [university e-mail]; ORCID [id]
```

## 5. Response to reviewers

**N1-N10** = the rules of Noble, "Ten simple rules for writing a response to reviewers", PLoS Comput. Biol.
13(10): e1005730, 2017, [doi:10.1371/journal.pcbi.1005730](https://doi.org/10.1371/journal.pcbi.1005730);
**LD** = [latexdiff man page](https://manpages.debian.org/testing/latexdiff/latexdiff.1.en.html), version 1.3.2. Both opened 2026-10-08.

### 5.1 Rules and structure

1. Readers: the editor, and a reviewer who reads only the replies to their own comments; each reply stands alone (N4).
2. Order: header (manuscript number, title, round, date); thanks in one sentence; the three to six main changes
   with locations; the letter's conventions; then the comments of the editor and of each reviewer in the order of
   the decision letter, numbered E.1, R1.1, R1.2, ... (N1, N6).
3. Quote every comment in full and unedited; answer every one (N1, N5). Split a multi-point comment into numbered
   parts without dropping words.
4. Per comment: quotation, reply, change. The reply opens with the answer: *Done.*, *We agree: ...*, *We kept X,
   because ...* (N7). The change gives its place in the revised manuscript (section, statement, page) and quotes
   new text up to a paragraph (N4, N9); `lineno` is not installed here, so no line numbers.
5. Do what is asked whenever possible (N8). A misreading is the text's fault: rewrite the passage (N3). Polite and
   factual; thanks once, at the top; a reply written in irritation is rewritten the next day (N2, N10).
6. Every promise is a change in the source; unrequested changes get their own list at the end. A change to a
   statement or a proof goes to the owner first and into "Content changes to review" (CLAUDE.md rule 4).
7. Reviews are confidential correspondence ([Springer Nature](https://www.springernature.com/gp/policies/editorial-policies)):
   never paste them into a public AI tool; AI-drafted replies are checked like manuscript text (§1.2).

### 5.2 Hard cases

| Case | Do |
|---|---|
| the reviewer is wrong | say which passage misled, rewrite it, then give the argument, counterexample or reference; never *the reviewer misunderstood* |
| disagreement on substance | the reason once, with evidence (proof, citation, experiment); offer the smallest change that removes the concern (remark, stated limitation); the editor decides (N8) |
| two reviewers conflict | follow one; say so in both replies with a cross-reference (*see R2.3*) |
| extra experiment or analysis | run it when feasible and report the result in the reply, also when it stays out of the paper, with the reason (N8); when infeasible, state the cost (runs, time, tokens) and name the gap as a limitation ([experiments-reporting.md](experiments-reporting.md) §8) |
| requested citation | add it only when relevant, after reading it, through the canonical `.bib` ([../bibliography/README.md](../bibliography/README.md)); decline an irrelevant one with one sentence of reason |
| error in a proof | fix it; state the corrected statement in full; list every result that depends on it |
| suspected bias or conflict of interest | separate letter to the editor, never the response (N2) |

### 5.3 Marked changes

State here on 2026-10-08: `where.exe latexdiff` finds only the MiKTeX stub;
`kpsewhich --miktex-disable-installer -format=texmfscripts latexdiff.pl` finds nothing; `ulem.sty` (needed by
latexdiff's default type `UNDERLINE`: LD), `soul.sty`, `changes.sty` and `changebar.sty` are absent. Do not run the
stub ([latex-guide.md](latex-guide.md) §15). Installed packages suffice for this (tested on a scratch copy of
article 1 with the build script's latexmk call):

```latex
% main.tex, before \begin{document}; needs xcolor (tcolorbox loads it)
\ifdefined\MarkChanges \newcommand{\rev}[1]{{\color{blue}#1}} \else \newcommand{\rev}[1]{#1} \fi
% main-marked.tex, the whole file
\def\MarkChanges{}\input{main}
```

- Wrap new and changed text in `\rev{...}`, inside an environment, not around it (paragraphs and displays inside
  are fine); list deleted text in the response letter; remove the wrappers after acceptance.
- Marked PDF: `.\scripts\build-project.ps1 -Project <p> -MainFile main-marked.tex`; clean PDF: the usual build,
  run last, because the packager compares its PDF with it. `main-marked.tex` and `response-to-reviewers.tex` stay in
  the project and are left out of the package ([latex-conventions.md](latex-conventions.md) §1.1).
- Change list for the letter (compares two folders, touches no repository):
  `git diff --no-index --word-diff archives/submissions/<p>/<previous>/source/sections projects/<p>/sections`.
- After the owner agrees to install `latexdiff` and `ulem` (CLAUDE.md rule 6), in Git Bash:
  `latexdiff --flatten old/main.tex new/main.tex > diff.tex` (LD); its output on the `problem` box and on
  `algorithmic`: TODO(verify) at first use.

### 5.4 Journal revision and conference rebuttal

| | Journal revision | Conference rebuttal |
|---|---|---|
| Form | response letter (PDF), marked PDF, clean PDF and sources; item names per card (IJOC: letter marked "Supplemental File for Review"; Algorithmica: all sources again; JGT, Networks: figures as separate files) | NeurIPS 2026: text box per review, 10,000 characters, Markdown, no files, no links, no revision of paper or supplement ([handbook](https://neurips.cc/Conferences/2026/MainTrackHandbook)). ICLR 2027: revised PDF (10 pages) until the discussion ends; comments word-limited, their number is not ([author guide](https://iclr.cc/Conferences/2027/AuthorGuidelines)). STACS 2027: three-day window ([card](../venues/lipics.md)) |
| Scope | every comment | by weight on the decision: factual errors in the reviews, direct questions, the two or three deciding concerns |
| New results | in the manuscript | as numbers in the text; NeurIPS allows them, the original submission stays the basis of the decision (handbook) |
| Limits | none; every change is made, not promised | promise only what fits the camera-ready limit; no names, no identifying links (handbook); House rule: draft in `projects/<p>/submission/rebuttal-<reviewer>.txt` and count before pasting: `(Get-Content -Raw <file>).Length` |

### 5.5 Deadlines and versions (House rule)

- On the day of the decision: save the reviews unedited as `projects/<p>/submission/reviews-r1.txt` and write the
  revision deadline into the project README; ask for an extension before the deadline, not after it.
- Revise in `projects/<p>/`, one sentence per line ([latex-guide.md](latex-guide.md) §15); the submitted state stays
  frozen (§3.2 step 6). Order: manuscript, rebuild, letter, so every cited location exists in the revised PDF.
- Each round repeats §3.2 steps 2-6 (step 3 writes the round's own zip; the `\rev{}` wrappers stay in the source
  until acceptance) and freezes its own folder (`...-r1`) with reviews, letter, clean and marked PDF. arXiv: replace
  after the revision is submitted, with a comment on what changed (§2.5, §2.7); never upload the response letter
  (§2.3).

### 5.6 Letter skeleton

`projects/<p>/response-to-reviewers.tex`; packages from [latex-guide.md](latex-guide.md) only; compiled here on
2026-10-08. Build: `.\scripts\build-project.ps1 -Project <p> -MainFile response-to-reviewers.tex`. With this file in
the project, check the manuscript text alone: `.\scripts\check-text.ps1 -Path projects\<p>\sections`.

```latex
\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc} \usepackage{lmodern,microtype,xcolor}
\usepackage[margin=2.5cm]{geometry} \usepackage[hidelinks]{hyperref}
\newcounter{com}
\newcommand{\party}[2]{\section*{#1}\setcounter{com}{0}\renewcommand{\thecom}{#2.\arabic{com}}}
\newenvironment{comment}{\refstepcounter{com}\medskip\noindent\textbf{\thecom.}\ \itshape}{\par}
\newenvironment{reply}{\smallskip\noindent\textbf{Reply.}\ }{\par}
\newenvironment{change}{\begin{quote}\color{blue}}{\end{quote}}
\begin{document}
\noindent\textbf{Response to reviewers}\\ Manuscript NUMBER, \emph{TITLE}, revision 1, YYYY-MM-DD
\section*{Summary of changes}
We thank the editor and the reviewers. Comments are in italics, replies upright, new manuscript text in blue.
Locations refer to the revised manuscript. Main changes: (1) CHANGE, Section~3; (2) CHANGE, Theorem~4.2.
\party{Reviewer 1}{R1}   % the editor first: \party{Editor}{E}
\begin{comment}\label{c:bound} COMMENT, VERBATIM. \end{comment}   % \ref{c:bound} prints R1.1
\begin{reply} ANSWER. Changed: Section~3, proof of Lemma~3.2, page~7. \end{reply}
\begin{change} NEW MANUSCRIPT TEXT. \end{change}
\end{document}
```

## 6. Preprints, copyright and self-archiving

### 6.1 Publisher rules (checked 2026-10-08)

| Publisher | Preprint (submitted version) | Accepted manuscript (AM) | Published version | Source |
|---|---|---|---|---|
| Elsevier | anywhere, any time; may be updated on arXiv with the AM; link the DOI | personal non-commercial page at once; arXiv at once if the licence is changed to CC BY-NC-ND; institutional repository after the journal's embargo; AM under CC BY-NC-ND | no public posting (also not ResearchGate); link only; theses allowed | [sharing](https://www.elsevier.com/about/policies-and-standards/sharing) |
| Springer Nature (journals) | TODO(verify): the self-archiving page refers to the editorial-policy section "Preprints" | personal website on acceptance (Springer imprint); repositories after 12 months for Springer subscription/hybrid journals; no CC licence on the AM; link the published version | gold OA only | [journal policies](https://www.springernature.com/gp/open-science/policies/journal-policies) |
| IEEE | arXiv, TechRxiv, personal or employer site; not prior publication | personal site, institutional repository, arXiv, TechRxiv; funder repositories after 24 months unless the mandate is shorter; IEEE copyright notice on the first page | not posted (non-OA); approved proofs not posted | [post-publication policies](https://journals.ieeeauthorcenter.ieee.org/become-an-ieee-journal-author/publishing-ethics/guidelines-and-policies/post-publication-policies/) |
| ACM | all pre-publication versions on homepage, institutional or funder repository, non-commercial repositories such as arXiv; add the DOI later; not ResearchGate, Academia.edu, Mendeley | same | all ACM articles open access since 2026-01-01 (CC BY or CC BY-NC-ND); own work reusable in the dissertation with citation and DOI | [author rights](https://authors.acm.org/author-resources/author-rights), [authorship policy](https://www.acm.org/publications/policies/new-acm-policy-on-authorship) |
| SIAM | TODO(verify): no statement on the authors page | institutional or subject repository at final publication, CC BY allowed (Plan S / UKRI green route) | optional OA for an APC of $3,750 | [journal authors](https://epubs.siam.org/journal-authors) |
| Wiley | any time: personal site, institutional repository, not-for-profit preprint servers; first-page notice after publication | 12-month embargo (STM journals) from publication; prescribed first-page notice with full citation and DOI | not self-archived | [self-archiving](https://authors.wiley.com/author-resources/Journal-Authors/licensing/self-archiving.html) |
| Taylor & Francis | any time, incl. arXiv; not duplicate publication | personal website after publication; open repository deposit after 12 months (STM) | 50 free e-prints | [sharing versions](https://authorservices.taylorandfrancis.com/research-impact/sharing-versions-of-journal-articles/) |
| AMS, INFORMS | TODO(verify) | TODO(verify) | TODO(verify) | - |

Conferences: NeurIPS 2026, ICML 2026 and ICLR 2027 allow arXiv preprints during review; the preprint must not
announce the submission ("under review at ...") and the submitted version must not point to it. Details on the
cards. ACM states that an arXiv posting is not a prior publication venue.

Society journals and double-anonymous journals may deviate (Elsevier and Wiley say so); read the journal's guide.

### 6.2 House rules

1. Post v1 on arXiv when the manuscript is submitted, unless the venue is double-anonymous and forbids it; licence
   per 2.6.
2. Record in the project `README.md` (Change history): arXiv id, licence, venue, submission date.
3. Never upload the publisher's PDF anywhere.
4. After acceptance: AM to arXiv only where the table allows it; after publication add DOI and journal reference.
5. Thesis reuse: check the publisher row before putting a published article into the dissertation
   ([thesis.md](thesis.md)).

### 6.3 Identity

| Item | Value |
|---|---|
| Name in print | Norbert Micheľ (LaTeX `Norbert Miche\v{l}`, BibTeX `Miche{\v{l}}, Norbert`, arXiv metadata `Norbert Miche\v{l}`) |
| Affiliation | Institute of Computer Science, Faculty of Science, Pavol Jozef Šafárik University in Košice, Košice, Slovakia ([../author.md](../author.md)) |
| ORCID | none yet ([../author.md](../author.md)); ACM requires one before publication, SIAM uses it for login; template fields: see the venue cards. Register at orcid.org before the first submission and add it to `author.md` |
| E-mail | the university address from [../author.md](../author.md) |

Use the same spelling, with the caron, on every submission system, on arXiv and in ORCID.
