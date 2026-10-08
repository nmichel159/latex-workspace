# Dissertation and the dissertation-exam written work

UPJŠ rules for the owner's PhD (Informatics, Faculty of Science (PF) UPJŠ) and how to build the dissertation from
papers. Structure of a single paper: [paper-structure.md](paper-structure.md). LaTeX craft:
[latex-guide.md](latex-guide.md); house rules: [latex-conventions.md](latex-conventions.md). AI-use statements,
licenses, preprints: [submission.md](submission.md). The template `templates/thesis-modular/` implements section 7.

Labels: **rule** = stated in an official document (short name in the last column, full reference in section 10);
**rec.** = recommendation of this knowledge base; **TODO(verify)** = not confirmed on an official page; open
questions are collected in section 9. All sources checked 2026-10-08.

## 1. Which rules apply

| Short name | Document (Slovak title, English gloss) | Use for |
|---|---|---|
| Smernica | Smernica č. 1/2011 o základných náležitostiach záverečných prác… (Directive 1/2011 on the basic requirements of final theses), with Dodatok (Amendment) 1-4; Dod. 4 (2016) rewrote Čl. 2 and Čl. 5 | form of the dissertation: parts, title page, abstracts, formatting, submission, originality check, license |
| SP DS | Študijný poriadok doktorandského štúdia UPJŠ (Doctoral Study Regulations), 2023, effective 2023-09-01 | dissertation exam, written work, defense, language, thesis by publication, autoreferát, credits |
| RR 1/2025 | Rozhodnutie rektora č. 1/2025 (Rector's decision on the use of AI) | generative AI |
| RR 21/2021 | Rozhodnutie rektora č. 21/2021 (Rector's decision on assessing plagiarism) | plagiarism, self-plagiarism |
| RR 25/2024 | Rozhodnutie rektora č. 25/2024 (Rector's decision on plagiarism-detection software); text not found, TODO(verify) | the "UPJŠ anti-plagiarism system"; the UPJŠ ethics page names Turnitin |
| RR 27/2025 | Rector's Decision No. 27/2025 on the Doctoral School at UPJŠ, effective 2026-01-01 | doctoral-school courses, duties |
| Usmernenie | Usmernenie k záverečným prácam (PF guidance on final theses, intranet docid 9135) | AiS2/EZP upload; names the LaTeX template rnthesis |
| Act 300/2025 | Zákon č. 300/2025 Z. z. (Higher Education Act), effective 2026-09-01; repeals act 131/2002, on which all UPJŠ documents above rest | AI statement, register of theses, transition |
| Decree 205/2026 | Vyhláška č. 205/2026 Z. z. (ministry decree implementing act 300/2025), effective 2026-09-01 | electronic format of theses |
| Study register | study plan Id and course sheets ÚINF/PDS/22 (dissertation exam), ÚINF/ODZP/15 (defense) | credits, program duties |

Not binding for this owner, used only as evidence of practice: guidance of the PF Institute of Geography
(UGE 2026), instructions of the Faculty of Medicine (LF) for the written work. Not applicable: Metodický pokyn
rektora č. 1/2022 (it governs DrSc. defenses, not the PhD).

Transition: act 300/2025 § 145 obliges universities to align internal rules by **2027-06-30** (ods. 1) and to
adjust running doctoral programs by the start of **AY 2027/2028** (ods. 7). On 2026-10-08 the UPJŠ doctoral
portal (edited 2026-09-22) still listed SP DS 2023, and the library page still listed the Smernica; no newer
regulation was found. Re-check both pages before each milestone in section 6.

## 2. Formal requirements of the dissertation

Rows in document order (Dod. 4 Čl. 5 ods. 2, 10). "Lang." = language in an English dissertation.

| Part (Slovak name) | Req.? | Content | Lang. | Source |
|---|---|---|---|---|
| Cover (*obal*) | rule | university; faculty; registration number if assigned (*evidenčné číslo*); title, subtitle; type *Dizertačná práca*; year of submission; author with degrees. Layout: model Príloha 1, section 7 C | model in SK; EN labels TODO(verify) | Dod. 4 Čl. 5 ods. 3; Smernica Príloha 1 |
| Title page (*titulný list*) | rule | in this order: university; faculty; title, subtitle; type; study program; name of the field of study; training department (*školiace pracovisko*); supervisor (*školiteľ*) with degrees; consultant if any; place and year of submission; author with degrees. Layout: model Príloha 2A | as cover | Dod. 4 Čl. 5 ods. 4; Príloha 2A |
| Acknowledgments (*poďakovanie*) | optional | supervisor, others, grants | EN | Dod. 4 Čl. 5 ods. 5 |
| Assignment (*zadanie záverečnej práce*) | rule | the AiS2 assignment; in the electronic version without signatures | as issued | Dod. 4 Čl. 5 ods. 2 d; Dod. 2 Čl. 8 ods. 3 b |
| AI-use statement | rule: the student must truthfully state that AI was used in preparing the thesis (act 300/2025 § 93 ods. 3 d) and every use of AI must be marked by citation (RR 1/2025 Čl. 5 ods. 5). Neither text prescribes a statement page or its content; a page is not in the Dod. 4 list; act § 8 ods. 2 leaves the AI rules to the university's internal regulations and § 101 accepts AI output when its origin is marked (checked 2026-10-08). rec.: own page after the assignment (the PF Institute of Geography requires a separate statement for Bc./Mgr. theses) | tools, versions, purposes; what remained the author's own work | EN | act 300/2025 § 93; RR 1/2025 Čl. 5; UGE 2026 sec. 6 |
| Abstract in Slovak (*abstrakt v štátnom jazyku*) | rule | one paragraph: aims, content, results, significance; 3-5 keywords; usually 100-500 words; own page | SK | Dod. 4 Čl. 5 ods. 7; SP DS Čl. 19 ods. 2 |
| Abstract in English | rule | same content; own page | EN | Dod. 4 Čl. 5 ods. 2 f, 7 |
| Table of contents (*obsah*) | rule | numbered and unnumbered parts | EN | Dod. 4 Čl. 5 ods. 8 |
| Lists of figures and tables | optional | when they help | EN | Dod. 4 Čl. 5 ods. 9 |
| List of abbreviations and symbols (*zoznam skratiek a značiek*) | listed without "optional" in ods. 2, called optional in ods. 9; rec.: include | symbol, meaning, page of definition | EN | Dod. 4 Čl. 5 ods. 2 i, 9 |
| Glossary (*slovník*) | optional | | EN | Dod. 4 Čl. 5 ods. 2 j |
| Introduction (*úvod*) | rule | state of knowledge, significance, aims, why the topic; **unnumbered**; usually 1-2 pages | EN | Dod. 4 Čl. 5 ods. 11 |
| Core (*jadro*) | rule | numbered chapters, **each first-level chapter on a new page**; usual parts: state of the art (usually ≥ 30 %), aims, methods, results, discussion (results + discussion usually 30-40 %) | EN | Dod. 4 Čl. 5 ods. 12-17; SP DS Čl. 19 ods. 4 |
| Conclusion (*záver*) | rule | results against the aims; **unnumbered**; SP DS: stress the contribution to practice | EN | Dod. 4 Čl. 5 ods. 18; SP DS Čl. 19 ods. 4 |
| Slovak summary (*resumé*) | rule for a non-Slovak thesis. Extent conflicts: "usually 10 % of the thesis" (Čl. 5 ods. 19, restated by Dod. 4 in 2016) vs. "at most one standard page" (Čl. 7 ods. 1, unchanged since 2011). rec.: about 10 % (the later wording; also used by UGE 2026); confirm (section 9) | rec.: aims, methods, results, conclusions | SK | Dod. 4 Čl. 5 ods. 10 d, 19; Smernica Čl. 7 ods. 1 |
| References (*zoznam použitej literatúry*) | rule | every entry cited, every citation listed | EN | Dod. 4 Čl. 5 ods. 20 |
| Appendices (*prílohy*) | optional | each on a new page, lettered A, B, …, listed in the table of contents | EN | Dod. 4 Čl. 5 ods. 21 |
| Back matter (*záverečná časť*) | optional | index, CV, other material | EN | Dod. 4 Čl. 5 ods. 22 |

Other rules on the document:

| Topic | Rule | Source |
|---|---|---|
| Extent | guideline 144 000-270 000 characters including spaces (80-150 standard pages); the character count decides | Smernica Čl. 7 ods. 7; SP DS Čl. 19 ods. 6 |
| Standards | layout per STN 01 6910, division numbering per STN ISO 2145, references per (STN) ISO 690; the standards' texts were not opened | Smernica Čl. 7 ods. 2 |
| Font and page | **recommended**: Times New Roman 12 pt, uniform; line spacing 1.5; margins left 3.5 cm, right 2 cm, top and bottom 2.5 cm; A4 portrait | Smernica Čl. 7 ods. 3 |
| Page numbers | Arabic, continuous, in the footer, centered or right, same font and size as the text; the title page counts but shows no number; every later page is numbered; in one-sided print the number counts sheets | Smernica Čl. 7 ods. 8 |
| Citations | one technique throughout, per the conventions of the field (Čl. 6 ods. 2). Čl. 6 ods. 3 (unchanged text) says the annex of examples serves running notes and numeric references per ISO 690, but since Dod. 3 (2014) that annex is Príloha 6A, whose examples are the author-date (Harvard) system (checked 2026-10-08); the library links ISO 690:2021 guidance | Smernica Čl. 6; Dod. 3 Príloha 6A; library page |
| Language and voice | Slovak by default, first person plural, past tense (Slovak convention; English: [academic-style.md](academic-style.md)); another language with consent of the dean and the chair of the field committee (*odborová komisia*), then the Slovak abstract is part of the thesis (SP DS Čl. 19 ods. 2, which names only the abstract). The older Smernica Čl. 7 ods. 1 gives a different consenter (*vedúci školiaceho pracoviska*, head of the training workplace) and asks for a Slovak summary of at most one standard page (see the *resumé* row); rec.: get the SP DS consent (checked 2026-10-08) | Smernica Čl. 7 ods. 1; SP DS Čl. 19 ods. 2 |
| Submission deadline | at the latest 3 months before 31 August of the last year of study, unless a faculty rule says otherwise | Dod. 2 Čl. 8 ods. 1; SP DS Čl. 18 ods. 3 |
| Electronic version | uploaded to AiS2 (module EZP) as a PDF from which text can be extracted, identical to the print except the unsigned assignment; decree 205/2026 § 17: PDF convertible to plain text. PDF/A is required by neither | Dod. 2 Čl. 8 ods. 2-3; decree 205/2026 § 17 |
| Print | 4 hard-bound copies (not comb-bound) to the dean within 3 working days after the upload, with 2 signed license agreements; TODO(verify) after act 300/2025. The PF Usmernenie (B.1) already says final theses are submitted only electronically, but its deadlines list only Bc. and Mgr. theses, so it is not read as overriding Dod. 2 for dissertations | Smernica Čl. 7 ods. 6; Dod. 2 Čl. 8 ods. 7; Usmernenie B.1 |
| Originality | before the request to defend: CRZP (national Central Register of Final Theses, checked by the ANTIPLAG system) and the UPJŠ anti-plagiarism system; both protocols are attached; the supervisor's assessment comments on them | SP DS Čl. 18 ods. 4, 6; Dod. 2 Čl. 8 ods. 4, 10; act 300/2025 § 137 ods. 2 |
| How ANTIPLAG reads the PDF | compares plain text extracted from the PDF (no formulas, no images); flags text whose extraction differs from what is visible; documents matching over 80 % (usually another version by the same author) are listed but left out of the global percentage | ANTIPLAG guide v3.0 |
| License and publication | license agreement generated by EZP (non-exclusive, free, 70 years). Act 300/2025: the register publishes the thesis within 30 days after the defense; the author may defer up to 12 months (+12 with the university's support) | Dod. 4 Príloha 4B; act 300/2025 § 137 ods. 6, 10 |
| Already published parts | declare by a sworn statement (journal, publisher, ISSN, issue; or publisher, year, print run, ISBN or DOI); public-access rules then do not apply to the published part | act 300/2025 § 137 ods. 11-13; Smernica Čl. 11 |
| Confidential data | separate non-public documentation, not in the thesis | act 300/2025 § 82 ods. 3; Dod. 2 Čl. 8 ods. 9 |

## 3. Written work for the dissertation exam

Slovak name: *písomná práca k dizertačnej skúške*. It is the project of the dissertation, not a survey.

**Official** (SP DS Čl. 17; course sheet ÚINF/PDS/22; PF application form):

| Item | Rule |
|---|---|
| Content | "tézy (projekt) dizertačnej práce" (theses, i.e. project, of the dissertation) containing: a) aims of the dissertation; b) theoretical foundations of the planned solution; c) current state of knowledge; d) analysis; e) methodological approach; f) state of progress on the date of application |
| Character | a scientific work: command of theory and terminology, overview of the state of the area, original scientific aims; formal details per the Smernica and SP DS; language Slovak or English |
| Submission | application in AiS2; written work in 2 copies + electronic version to the chair of the field committee; attach the protocol of the UPJŠ anti-plagiarism system. The PF form names the written work by title, says it includes a short written exposition (theses) of the project, has three lines for exam subjects and a field for the proposed opponent |
| Deadline | within **24 months** of the start of study (4-year full-time program); requires the completed study part and **90 credits**; missing it means dismissal |
| Review | one opponent (doctoral degree, outside the department, no joint publication) reviews within 3 weeks, grade pass/fail; the student sees the review ≥ 3 working days before the exam |
| Exam | (a) defense of and discussion on the written work, (b) theory in the set exam subjects; pass/fail; 20 credits; one retake after 3-12 months |
| Integrity | own research; no academic fraud; RR 21/2021 applies |
| Extent, binding | no extent or binding found in SP DS Čl. 17, in the course sheet or in the PF form (the form only asks for the number of pages; checked 2026-10-08). LF (not binding): at least 30 pages of text, 2 comb-bound copies. rec.: 30-50 pages |

**Recommended structure** (rec.; maps the official items a-f):

| Chapter | Item | Content |
|---|---|---|
| Theses of the project (1-2 pages, before chapter 1) | PF form; SP DS "tézy" | numbered statements: aims, research questions, expected contributions |
| 1 Introduction | a | problem, motivation in two paragraphs, aims as 3-5 numbered research questions |
| 2 Preliminaries | b | definitions and notation reused later in the dissertation |
| 3 State of the art | c, d | taxonomy of LLM-based algorithm design and of the graph problems used; analysis: which gaps the aims address ([../research/llm-optimization.md](../research/llm-optimization.md)) |
| 4 Results so far | f | own results with full statements; each published or submitted item with a full reference and the owner's share |
| 5 Methodology and planned research | e | per aim: method, benchmark, baselines, success criterion, risk ([experiments-reporting.md](experiments-reporting.md)) |
| 6 Publication plan | rec. | table: working title, target venue ([../venues/README.md](../venues/README.md)), status, planned date |
| 7 Timeline | rec. | semester plan up to the defense |
| References | | |

Write chapters 2-4 so that they become dissertation chapters with edits (rec.).

## 4. Dissertation built from papers

**Rules.** SP DS Čl. 19 ods. 3 allows a dissertation that is the author's published work or a set of the author's
published scientific papers, completed by a detailed commentary on the state of the art, the aims, the author's
own contribution and the conclusions. Čl. 19 ods. 5: in collective work state the own share and place it among the
co-authors' results. RR 21/2021 Čl. 2 ods. 3 g defines self-plagiarism; Čl. 2 ods. 5 exempts, among others,
republication in a collection of the author's papers when the place of first publication is marked.

**Choose the form (rec.):**

| Form | Use when | Cost |
|---|---|---|
| Merged narrative (default) | the papers share notation and build one argument (LLM-designed algorithms for one problem family) | rewriting; one notation; no repeated introductions |
| Chapter per paper + commentary (SP DS Čl. 19 ods. 3) | the papers are on distinct topics (e.g. Min Cut-Path and LLM optimization) | repetition across chapters; the commentary must be detailed, not a preface |

**Reuse checklist (rec. unless marked):**

1. Each reused paper: a footnote on the chapter title with the full reference (*This chapter is based on
   [Mic26], published in …*); mark text taken verbatim. Rule: RR 21/2021 Čl. 2 ods. 5.
2. A section *Publications and author's contribution* in the introduction: per paper the reference, status and the
   owner's share (ideas, proofs, code, experiments, writing). Rule: SP DS Čl. 19 ods. 3, 5.
3. Before submission, check each publisher's license for reuse in a thesis and record the clause in the project
   README; license types: [submission.md](submission.md). TODO(verify) per publisher.
4. Results of the master's thesis (Charles University, 2025) are prior work: cite the thesis, do not present them
   as new results (RR 21/2021 Čl. 2 ods. 3 g).
5. Expect CRZP matches with the owner's own papers and arXiv versions; explain them in the supervisor's
   assessment (Dod. 2 Čl. 8 ods. 10). Whether journals and arXiv are in the ANTIPLAG corpus is not stated
   (TODO(verify)); a near-identical earlier version (> 80 % match) is listed but not counted (ANTIPLAG guide, not re-checked 2026-10-08). RR 21/2021 Čl. 2 ods. 5 d, b, g (checked 2026-10-08) says preprints later published as articles, conference paper plus full version, and a translation of one's own work marked as such are not self-plagiarism.
6. Declare published parts for the register (act 300/2025 § 137 ods. 13).
7. One notation and terminology across chapters ([math-writing.md](math-writing.md) section 1); one `macros.tex`.

**Thesis-level parts (rec.):**

| Part | Content |
|---|---|
| Introduction (unnumbered, rule) | the research question of the whole thesis; aims; one paragraph per chapter stating its result; list of publications with the owner's share |
| Notation and preliminaries (chapter 1) | all shared definitions; the list of symbols points here |
| Result chapters | one per paper or per aim; each opens with what it proves or measures and closes with its limitations |
| Discussion | how the chapters answer the aims; comparison with others' results (Dod. 4 Čl. 5 ods. 17) |
| Conclusion (unnumbered, rule) | results against the aims; contribution to practice (SP DS Čl. 19 ods. 4); concrete open problems |
| Appendices | omitted proofs, prompts, hyperparameters, full tables ([experiments-reporting.md](experiments-reporting.md)) |

## 5. Language: English dissertation

| Step | Rule / rec. |
|---|---|
| Permission | rule: consent of the dean and of the chair of the field committee (SP DS Čl. 19 ods. 2). The study-register course sheets ÚINF/ODZP/15 (defense) and ÚINF/PDS/22 (written work) list the language as "slovenský alebo anglický" (API of studijne-programy.upjs.sk, AY 2026/2027, checked 2026-10-08); the sheets do not mention the consent, which SP DS still requires. The program also runs as IdAj (English); the PF topic list 2025/2026 shows the supervisor's topics in Id (language EN; SK) and IdAj (EN). TODO(verify) the owner's variant in AiS2 and whether consent is then implied |
| Slovak parts | rule: abstract in Slovak; Slovak *resumé* (extent: section 2). The autoreferát is in Slovak (section 8) |
| Hyphenation | rec.: `\usepackage[slovak,english]{babel}` (last option = main language); Slovak parts in `otherlanguage{slovak}`; Slovak patterns `hyph-sk.tex` are installed |
| Encoding | rec.: `\usepackage[T1]{fontenc}` so that *ľ, ť, ď, ň* hyphenate and extract as text |
| Spelling, style | American English; [academic-style.md](academic-style.md) |
| AI statement | rule: state AI use truthfully (act 300/2025 § 93 ods. 3 d) and mark every use by citation (RR 1/2025 Čl. 5 ods. 5); the supervisor may set the permitted extent (Čl. 5 ods. 2); be able to explain every AI-assisted part (Čl. 5 ods. 3). rec.: statement page with tools, versions, purposes; LLMs studied as research objects are reported in the method chapters, not in this statement. RR 1/2025 Čl. 7 ods. 4 additionally obliges researchers to state how AI was used in research, including the algorithms and approaches, for reproducibility; whether it binds a doctoral student's research is TODO(verify) (the decision's student rules are Čl. 5) |

## 6. Milestones (full-time, 4-year program)

Dates assume study started 2025-09-01 and ends 2029-08-31; TODO(verify) the start date in AiS2.

| Milestone | Rule | Date if start 2025-09-01 | Source |
|---|---|---|---|
| Individual study plan | within 30 days of enrollment and at every change | autumn 2025 | SP DS Čl. 15 ods. 1 |
| Institute seminar | present results every semester | each semester | study plan Id |
| Doctoral School | courses and workshops for all doctoral students, compulsory elective or elective by activity; duties include interim progress reports. Act 300/2025 § 64 ods. 2 makes the doctoral-school part a completion condition; TODO(verify) whether it binds students enrolled before the AY 2027/2028 adjustment | from 2026-01-01 | RR 27/2025 Art. 3, 5; act 300/2025 § 64, § 145 ods. 7 |
| Annual evaluation | supervisor via AiS2, 10-12 months after each enrollment | yearly, June-August | SP DS Čl. 16 ods. 5 |
| Progress | ≥ 40 credits for year 1 → 2; ≥ 90 credits in four consecutive semesters | 2026-08, 2027-08 | SP DS Čl. 14 ods. 10 |
| Exam application + written work | ≤ 24 months from start; ≥ 90 credits; study part complete | by **2027-08-31** | SP DS Čl. 17 ods. 1-2 |
| UPJŠ rules aligned with act 300/2025 | universities' deadline | 2027-06-30 | act 300/2025 § 145 ods. 1 |
| Request to defend + dissertation | ≥ 210 credits without the defense; the field committee's publication minimum (TODO(verify) for Informatics; the program description mentions at least one conference paper in the first two years as usual practice); ≥ 3 months before the planned end | by **2029-05-31** | SP DS Čl. 18 ods. 2-3; Dod. 2 Čl. 8 ods. 1 |
| Defense | by 31 August of the last standard year; PF schedules defenses in August (2027: 2027-08-09 to 2027-08-27) | by 2029-08-31 | SP DS Čl. 22 ods. 4; PF schedule 2026/2027 |
| Total | 240 credits including defense (30) and exam (20) | | SP DS Čl. 14 ods. 13 |

Publication credits in study plan Id (scientific part, min. 120 credits): journal Q1 first or corresponding author 40,
co-author 30; Q2 30/20; Q3 25/15; Q4 20/10; talk at an international conference abroad 10. Quartile by SJR or JCR;
proceedings in LNCS, LNAI or IEEE series count by the quartile or indexing of the series (SP DS Príloha 1, whose table for medical and science programs is headed "recommended distribution" and lists "first author"; the study register adds "or corresponding"; both checked 2026-10-08).

## 7. Template requirements (`templates/thesis-modular/`)

**Must** = rule; **should** = recommendation or unresolved rule. Packages: use only installed ones. Installed:
geometry, setspace, newtx, babel (slovak, english), fontenc, glyphtounicode, cmap, titlesec, fancyhdr, appendix,
makeidx, pdfx, biblatex, natbib. Not installed: pdfpages, tocbibind, tocloft, bookmark, nomencl, glossaries,
acronym, imakeidx, emptypage, lastpage, biblatex-iso690, memoir, KOMA-Script (`kpsewhich`, 2026-10-08).

**A. Page and type**

1. Should default to A4 portrait, 12 pt, margins left 35 mm, right 20 mm, top and bottom 25 mm (`geometry`),
   Times-like font (`newtxtext`, `newtxmath`), line spacing 1.5 via `\onehalfspacing` (`setspace`; stretch 1.241 at
   12 pt per the installed `setspace.sty`). All are recommendations (Smernica Čl. 7 ods. 3): expose them as options.
   `\usepackage[T1]{fontenc}` must be loaded before `newtxtext`: without it `pdftotext` returns Slovak letters as a
   letter plus a separate accent (tested 2026-10-08 in the template).
2. Should default to one-sided; offer `twoside` with mirrored margins (inner 35 mm, outer 20 mm). Both are allowed
   (Smernica Čl. 7 ods. 8).
3. Should keep one font family and size for the text and page numbers throughout (Smernica Čl. 7 ods. 3, 8).

**B. Order of parts (must; Dod. 4 Čl. 5 ods. 2, 10)**

4. cover → title page → acknowledgments (switch) → assignment → AI-use statement (switch, default on; should) →
   Slovak abstract + keywords → English abstract + keywords → table of contents → list of figures, list of tables
   (switches) → list of abbreviations and symbols (default on) → glossary (switch) → Introduction → chapters 1…n →
   Conclusion → Resumé (Slovak) → References → appendices A, B, … → back matter (switch: index, CV).
5. Each front-matter part on its own page (must for the abstracts, should for the rest).

**C. Cover and title page (content must; layout follows the models)**

6. Cover (Príloha 1), top to bottom: university and faculty in capitals, bold, centered; registration number
   (optional) small, left; title and subtitle in capitals, bold, centered; thesis type centered; at the bottom left in
   bold: year of submission, then author with degrees. Default: no page number, not counted (TODO(verify),
   section 9).
7. Title page (Príloha 2A): same head; title and subtitle in capitals, bold, centered; type bold, centered; a
   left-aligned two-column block *Študijný program:* / *Študijný odbor:* / *Školiace pracovisko:* / *Školiteľ:* /
   *Konzultant:* (line omitted if no consultant); at the bottom left in bold: place and year of submission, then
   author with degrees. Counts as page 1, number not printed.
8. Field macros with these defaults: university *Univerzita Pavla Jozefa Šafárika v Košiciach*; faculty
   *Prírodovedecká fakulta*; type *Dizertačná práca*; program *Informatika*; field *informatika* (name only, no
   code: Dod. 4 Čl. 5 ods. 4 f); training department *Ústav informatiky*; supervisor *prof. RNDr. Gabriel
   Semanišin, PhD.* ([../author.md](../author.md)); place *Košice*; registration number empty.
9. Labels in Slovak as in the models (default); an `english` option may translate them (rnthesis does) but its
   acceptance is TODO(verify). Should print the title exactly as in the AiS2 assignment.

**D. Page numbering (must; Smernica Čl. 7 ods. 8)**

10. Arabic numerals only, continuous from the title page (page 1, number hidden) to the last page, including the
    assignment, lists, appendices and back matter; no roman front matter.
11. Footer, centered (option: right), same font and size as the text; no other running headers required.
12. `hyperref` page labels must match the printed numbers.

**E. Divisions**

13. Chapters numbered 1, 2, …; sections decimal (1.1, 1.1.1) per STN ISO 2145 (standard not opened: dot and depth
    details TODO(verify)); should limit numbering and the table of contents to three levels.
14. Every numbered first-level chapter starts on a new page (must).
15. Introduction, Conclusion, Resumé and References unnumbered but listed in the table of contents (must for
    Introduction and Conclusion; should for the others). `tocbibind` is not installed: add entries with
    `\addcontentsline`.
16. Appendices lettered A, B, …, each on a new page, listed in the table of contents (must; `appendix` installed).

**F. Abstracts, lists, glossary**

17. Each abstract on its own page: heading *Abstrakt* / *Abstract*, one paragraph, then *Kľúčové slová:* /
    *Keywords:* with 3-5 entries (must); the Slovak page inside `otherlanguage{slovak}`. Should warn when a keyword
    list has fewer than 3 or more than 5 entries or an abstract falls outside 100-500 words.
18. List of abbreviations and symbols: a `longtable` or `description` list (symbol, meaning, `\pageref` to its
    definition); no `nomencl`/`glossaries`/`acronym` (not installed). Same for the glossary.

**G. Bibliography (must: one technique throughout; every entry cited)**

19. Numeric citations (Smernica Čl. 6 ods. 2 lets the field's convention decide and requires one technique
    throughout; the annex of examples, Príloha 6A since Dod. 3, shows the author-date system, so numeric is a choice
    of the field, not a copy of the annex): the workspace default BibTeX + `natbib`
    `numbers,sort&compress` ([latex-conventions.md](latex-conventions.md)); no `\nocite{*}`. Whether the chosen
    `.bst` satisfies ISO 690 in detail: TODO(verify) with the supervisor; `biblatex-iso690` is not installed and is
    installed only with the owner's consent.

**H. Language and PDF**

20. `\usepackage[T1]{fontenc}`, `\usepackage[slovak,english]{babel}` (main English; option to switch to Slovak);
    Slovak-language parts (cover and title page labels, Slovak abstract, Resumé) inside `otherlanguage{slovak}`.
21. Text must extract correctly (Dod. 2 Čl. 8 ods. 3 a; ANTIPLAG compares extracted text): `\input{glyphtounicode}`
    and `\pdfgentounicode=1` (or `cmap`); test with `pdftotext -enc UTF-8` that Slovak diacritics, ligatures and
    words survive. No password, no scanned pages.
22. PDF/A not required; the template does not provide it: `pdfx` compiles but gives duplicate-destination warnings
    on floats, and the result cannot be validated here (no veraPDF). PDF metadata: title, author, keywords (should).
23. Assignment: `pdfpages` is not installed; insert page 1 of `assignment.pdf` with
    `\includegraphics[page=1,width=\textwidth]{assignment.pdf}` (`graphicx` key `page`, defined in the installed
    `graphicx.sty`/`pdftex.def`) on a page that keeps its number, or a placeholder
    page until the PDF exists. The submitted electronic version carries the assignment without signatures.

**I. Structure, extras, variants**

24. Should keep chapters in `chapters/NN-name.tex` and shared notation in one macro file
    ([latex-conventions.md](latex-conventions.md)).
25. Should provide `\chapterbasedon{<bibkey>}` (title footnote naming the source paper) and a *Publications and
    author's contribution* section (section 4).
26. Should provide a character count: `pdftotext -enc UTF-8 main.pdf - | wc -m`, target 144 000-270 000.
27. Should provide a variant for the written work for the dissertation exam: same front matter, type *Písomná práca
    k dizertačnej skúške*, assignment page switched off, chapters of section 3. Whether it needs a Slovak resumé:
    TODO(verify).
28. Should provide a separate A5 autoreferát document (section 8).
29. Print: hard binding (must, Smernica Čl. 7 ods. 6); 4 copies (Dod. 2 Čl. 8 ods. 7; TODO(verify) after act
    300/2025). The PDF equals the print except the unsigned assignment.

## 8. Autoreferát (author's summary)

Rule (SP DS Čl. 18 ods. 4 i, 5): submitted with the request to defend; summary of aims, main results and their
contribution; **at most 20 pages A5**; **in Slovak**; parts: introduction, brief overview of the problem, theses of
the dissertation, methods, results, contribution to science and practice, *resumé* in English (or another foreign
language); then references and the list of all the owner's publications ordered per the UPJŠ directive on
publication records. Pages 1-2 follow a UPJŠ model: TODO(verify) (not found; the SP DS footnote points to the
Smernica, which has none).

## 9. Open questions for the PF doctoral office

Ask once, record the answers in this file with date and name of the office.

1. Which Slovak *resumé* extent applies to an English dissertation (10 % or one standard page)?
2. Are English labels accepted on the cover and title page? Does the cover count as a page?
3. Is a declaration of originality or an AI-use statement page expected inside the dissertation?
4. Printed copies and binding of the dissertation after act 300/2025 (still 4 hard-bound)?
5. The field committee's publication minimum for the defense in Informatics (SP DS Čl. 18 ods. 2 c).
6. Expected extent and binding of the written work for the dissertation exam; Slovak resumé needed?
7. The UPJŠ model for pages 1-2 of the autoreferát.
8. Does the doctoral-school requirement (act 300/2025 § 64) apply to students enrolled in 2025?
9. Are new UPJŠ rules under act 300/2025 published (Smernica, SP DS)?
10. Owner's data in AiS2: start date, variant Id or IdAj, consent to English.

## 10. Sources

| Short name | Document | URL |
|---|---|---|
| Smernica | Smernica č. 1/2011, č. j. 4405/2011, 2011-11-03 | <https://www.upjs.sk/app/uploads/sites/16/2023/01/smernica-1-2011.pdf> |
| Dod. 1 | Dodatok č. 1, č. j. 1944/2012, 2012-05-15 | <https://www.upjs.sk/app/uploads/sites/16/2023/01/dod1-smernica-1-2011.pdf> |
| Dod. 2 | Dodatok č. 2, č. j. 4687/2012, 2012-12-17 | <https://www.upjs.sk/app/uploads/sites/16/2023/01/Dodatok2-2012-SmernicaZP.pdf> |
| Dod. 4 | Dodatok č. 4, č. j. 756/2016, 2016-03-01 (Dod. 3 replaces only annexes) | <https://www.upjs.sk/app/uploads/sites/16/2023/01/Smernica-1-2011_dod-4_2016.pdf> |
| library page | University Library, final theses (Smernica, Dod. 1-4, ISO 690 guidance; edited 2024-02-19) | <https://www.upjs.sk/pracoviska/univerzitna-kniznica/zaverecne-prace/> |
| SP DS | Študijný poriadok doktorandského štúdia UPJŠ, REK000524/2023-UPA/800, 2023-02-24; English version docid 9702 | <https://intranet.upjs.sk/ext/share_to_public/op/Public.php?documentid=1449> |
| doctoral portal | UPJŠ doctoral portal (edited 2026-09-22) | <https://www.upjs.sk/informacie/vyskum/vedeckovyskumna-cinnost/doktorandsky-portal/> |
| PF PhD page | forms: exam application (docid 9184), request to defend (docid 9185) | <https://www.upjs.sk/prirodovedecka-fakulta/studium/doktorandske/organizacia-studia-phd/> |
| Usmernenie | PF guidance on final theses (docid 9135) | <https://intranet.upjs.sk/op/op.Public.php?documentid=9135> |
| RR 1/2025 | Rozhodnutie rektora č. 1/2025 (AI), REK00002/2025-UPA/09, 2025-01-07 | <https://www.upjs.sk/app/uploads/sites/11/2025/09/RR-c.-1_2025_AI.pdf> |
| RR 21/2021 | Rozhodnutie rektora č. 21/2021 (plagiarism), REK00420/2021-UPA/4174, 2021-09-27; copy on a UPJŠ staff page (official copy TODO(verify)) | <https://web.science.upjs.sk/novotny/BcSeminar/Plagiatorstvo_Rozhodnutie_rektora21_2021.pdf> |
| RR 25/2024 | listed in the UPJŠ overview of 2024 regulation changes: REK000273/2024-UPA/6610, 2024-12-15 | <https://www.upjs.sk/app/uploads/2025/06/Priloha-1_Prehlad-zmien-vn.-predpisov-UPJS-za-rok-2024.pdf> |
| ethics page | UPJŠ "Ethics of scientific work" (Turnitin; edited 2024-04-25) | <https://upjs.sk/en/?p=60242> |
| RR 27/2025 | Rector's Decision No. 27/2025 (Doctoral School), REK007315/2025-UPA/2783, 2025-12-18, English version | <https://intranet.upjs.sk/ext/share_to_public/op/Public.php?documentid=11177> |
| ANTIPLAG guide | "Ako čítať a interpretovať Protokol o kontrole originality", for CRZP/ANTIPLAG v3.0, 2022-08-23; copy hosted by the Armed Forces Academy (official location TODO(verify)) | <https://aos.sk/data/component_file/100/233/f1671.pdf> |
| study plan Id | Study register, Informatika PhD, AY 2026/2027; course sheets ÚINF/PDS/22, ÚINF/ODZP/15 | <https://studijne-programy.upjs.sk/program/Id?phd=> |
| PF topics | PF dissertation topics 2025/2026, Institute of Computer Science | <https://haik.upjs.sk/data/topic/2025-2026/PF_UPJS/D/SK/UINF.html> |
| PF schedule | Harmonogram akademického roka 2026/2027 | <https://intranet.upjs.sk/op/op.Public.php?documentid=11034> |
| UGE 2026 | Pokyny na tvorbu záverečných prác na Ústave geografie PF UPJŠ, 2026-01-28 (Bc./Mgr.; not binding here) | <https://uge-share.science.upjs.sk/webshared/uge_web_files/studium/Pokyny_ZP_UGE_2026.pdf> |
| LF | Pokyny k odovzdaniu písomnej práce k dizertačnej skúške, Faculty of Medicine (not binding here) | <https://www.upjs.sk/app/uploads/sites/9/2025/05/POKYNY-K-ODOVZDANIU-PISOMNEJ-PRACE-K-DIZERTACNEJ-SKUSKE.pdf> |
| Act 300/2025 | Zákon č. 300/2025 Z. z. (vysokoškolský zákon), promulgated 2025-11-14, Art. I effective 2026-09-01, time version effective 2026-09-01 (with amendment 121/2026 Z. z.; opened 2026-10-08) | <https://www.slov-lex.sk/ezbierky/pravne-predpisy/SK/ZZ/2025/300/20260901.html> |
| Decree 205/2026 | Vyhláška č. 205/2026 Z. z. of the Ministry of Education, Research, Development and Youth, dated 2026-07-21, promulgated 2026-08-11, effective 2026-09-01 (opened 2026-10-08) | <https://static.slov-lex.sk/static/SK/ZZ/2026/205/vyhlasene_znenie.html> |
| rnthesis | community LaTeX class named by the Usmernenie; LPPL 1.3c; last change 2020-08-16; bachelor/master samples, no cover, no dissertation support | <https://github.com/novotnyr/rnthesis> |
