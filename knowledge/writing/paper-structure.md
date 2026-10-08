# Paper structure

What goes into which part, in what order, and what does not belong there. Sentence style:
[academic-style.md](academic-style.md). Page limits, mandatory parts and the template come from the target venue; its
card is in [../venues/](../venues/README.md).

## 1. Before the first sentence

Write these four answers into `projects/<project>/README.md` (section "Intent") before any text exists.

| Question | Form of the answer |
|---|---|
| **Main claim** | one sentence the reader should remember (*Min Cut-Path is NP-complete, but $\cp = c + d - 1$ in graphs of diameter two.*) |
| **Contributions** | 2–4 checkable statements, each with its place in the text (theorem, table) |
| **Closest work** | which published result is closest and how exactly we differ |
| **Reader and venue** | who the text is for, where it goes, the length limit |

Writing order: (1) statements of the theorems, tables and figures, (2) the core: proofs and experiments,
(3) introduction, (4) conclusion, (5) abstract, (6) title. An introduction written first is always rewritten once the
core is done.

## 2. Types of text

| Type | Skeleton | What the reviewer checks |
|---|---|---|
| **Theory journal article** (graph theory, complexity, algorithms) | Introduction (problem, results, related work) → Preliminaries → one section per result → Concluding remarks with open problems | correctness and completeness of proofs, novelty over the literature, clean statements |
| **TCS conference paper** ([LIPIcs](../venues/lipics.md), [LNCS](../venues/lncs.md)) | the same within the page limit; *Our results* and *Technical overview* in the introduction; full proofs in an appendix or in a full version on arXiv, as the venue card allows | strength of the result, a clear overview of the technique in the main text |
| **Experimental paper** (LLMs in algorithm design, heuristics, ML) | Introduction with contributions → Related work → Method → Experimental setup → Results → Limitations → Conclusion; appendix with prompts, settings and further tables | fair comparison, reproducibility, conclusions proportionate to the data |
| **Computational study** (algorithm engineering, OR) | Introduction → Problem and prior algorithms → Algorithm → Computational study → Conclusion | test instances, baselines, time and quality, code availability |
| **Extended abstract** (conference without full-paper proceedings) | 1–4 pages: problem, definition, statements of results, one proof idea, references | a clear statement of the result |
| **Survey** | question and scope → method of selecting works → taxonomy → comparison → open problems | coverage, classification, own perspective |
| **Dissertation** | [thesis.md](thesis.md) | |

Mixed paper (theory plus experiment, typical for the dissertation topic): write the theoretical part by the first row,
the experimental part by the third; the introduction lists the two kinds of contribution separately.

## 3. Title

- Says **what** is studied and **what** was found; at most 12 words; no formulas, no non-standard abbreviations.
- Does not start with *On*, *A Study of*, *Towards*, *Some Remarks on*; contains no *novel*, no *efficient* without a
  measure, no *new approach*.
- A colon only when the second part carries the result: *Min Cut-Path: NP-Completeness and Polynomial Cases* (shape
  example; the author chooses the title).
- Keywords and classification (MSC 2020, ACM CCS) as the venue requires; keywords do not repeat words of the title.

## 4. Abstract

One paragraph, 100–200 words (the venue limit wins). No citations, no section references, no undefined symbols, no
motivation sentences that could open any paper.

| Sentence | Content |
|---|---|
| 1 | the object or problem; if new, its definition in one sentence |
| 2 | the main result, exactly (class, bound, complexity, number) |
| 3–4 | further results in order of importance |
| 5 (optional) | the method, if it is a contribution in itself |
| 6 (optional) | a consequence or an open question |

Example for article 1 (a proposal of the shape; it does not change the article source):

> A cut-path between two vertices $u$ and $v$ of a graph is a set of edges that contains both a $u$–$v$ path and a $u$–$v$ cut. We study Min Cut-Path, the problem of finding a cut-path with the fewest edges; its size is denoted $\mathrm{cp}(u,v)$. We prove that the decision version is NP-complete by a reduction from 3-SAT through an intermediate problem, Separating Shortest Path. In contrast, $\mathrm{cp}(u,v) = c(u,v) + d(u,v) - 1$ in graphs of diameter two and in graphs in which a minimum cut between any two vertices has at most two edges, where $c$ is the minimum cut size and $d$ the distance; in both classes the union of any minimum cut and any shortest path is optimal. As a consequence, Min Cut-Path is solvable in polynomial time on almost all dense Erdős–Rényi graphs, and for $p \ge \alpha \log n / n$ with $\alpha > 1$ the same union is asymptotically optimal with high probability.

## 5. Introduction

The introduction answers five questions, in this order. Each gets its own paragraph or subsection; nothing else is in
the introduction.

| # | Question | Length | Note |
|---|---|---|---|
| 1 | **What is the problem?** | 1 paragraph | an exact, if informal, definition; a small example or figure; no scene-setting |
| 2 | **Why does it matter, and what is known?** | 1–2 paragraphs | specific motivation and the closest known results with citations; what remains open |
| 3 | **What do we prove or show?** | list or subsection *Our results* | each contribution is a checkable statement with a reference to a theorem, table or section |
| 4 | **How?** | 1–3 paragraphs, optionally *Technical overview* | the main idea of the hardest proof or of the method; what differs from earlier work |
| 5 | **How does the paper relate to other work?** | paragraph or section *Related work* | including the author's own earlier texts (master's thesis, conference abstract) and a statement of what is new compared with them |

A paragraph on the paper's organization (*The paper is organized as follows*) is optional: at most four sentences, each
saying what a section **proves**, not that it exists. If the contributions in item 3 already point to sections, omit it.

**Contribution list.** An item starts with a verb the text backs (*We prove*, *We give an $O(m)$ algorithm*, *We
evaluate on 50 instances*). *We study*, *we discuss*, *we provide insights* do not belong there. In a theory paper the
main theorems may be stated in full in the introduction (*Theorem 1.1*) and restated with the same number in the core
(`thm-restate`, [latex-guide.md](latex-guide.md) §6) or referenced.

**Relation to the master's thesis.** If the paper takes results from the thesis, the introduction says so in one
sentence and cites the thesis; new results are marked as new. Take statements from the thesis only after checking them
against the list of errors in `knowledge/research/min-cut-path.md`, section 5a.

## 6. Related work

- Organize **by idea or question**, not paper by paper and not chronologically.
- Each group of works ends with a sentence on the difference: what they do, what we do.
- Which source to cite (original result, textbook for standard notions, published version over a preprint):
  [../bibliography/README.md](../bibliography/README.md) §6 and §8.
- A claim "not studied before" rests on a logged search: keywords, databases and date in
  [../literature/searches.md](../literature/searches.md); how old the search may be:
  [../literature/README.md](../literature/README.md), "Rules".
- Describe other work exactly and neutrally; criticism targets the result, not the authors.
- Placement: in a theory paper inside the introduction; in an experimental paper as Section 2 or before the conclusion,
  following the venue's habit.

## 7. Preliminaries

- Only notions and notation that are actually used; standard material by reference to one textbook.
- Conventions first (*All graphs are finite, simple, and undirected*).
- Define a new notion where the reader first needs it; Preliminaries hold only what at least two sections use.
- State the problem in a box (`problem`): *Input / Question* for the decision version, *Input / Output* for the
  optimization version ([latex-conventions.md](latex-conventions.md) §5).
- With more than about 15 symbols, a table of notation (in an article in the appendix, in a dissertation at the front).

## 8. Core

One section per result. A section opens with the result or one sentence about it, never with an announcement.

Headings: a noun phrase that names the content (*NP-completeness*, not *Main results*); capitalization follows the
venue's sample file, default title case as in the templates; no heading without at least two sibling headings at its
level; no text about the heading directly under it.

| Kind of result | Outline of the section |
|---|---|
| Structural theorem | idea (1 paragraph) → auxiliary lemmas right before their use → theorem → proof → remark on tightness or a counterexample |
| Hardness (NP-completeness) | source problem of the reduction → construction with a figure → size and time of the construction → both directions of the equivalence → membership in NP |
| Algorithm | idea → pseudocode → correctness → complexity → (example run) |
| Probabilistic result | model and parameters → inequalities used, with citations → theorem with the exact meaning of "with high probability" → proof |
| Experiment | [experiments-reporting.md](experiments-reporting.md) |

Details of the write-up: [math-writing.md](math-writing.md).

Not in the main text: routine computations, further cases analogous to the one shown, full tables, prompts; they go to
an appendix with a reference.

## 9. Discussion and limitations

In an experimental paper, a separate *Limitations* part: on which instances and under what budget the results hold,
what was not tested, what may stem from data leakage or from the choice of model
([experiments-reporting.md](experiments-reporting.md) §8). In a theory paper the limitations are part of the theorem
statements (hypotheses) and of the conclusion (what remains open).

## 10. Conclusion

- One to three paragraphs. Not the abstract in the past tense; does not repeat the contribution list.
- Says what is now known, what is not, and why; if the results connect, that belongs here.
- **Open problems are specific**, in a theory paper numbered and phrased as questions or conjectures (*Is Min Cut-Path
  polynomial on planar graphs?*), not *several interesting directions remain*.
- No new result, no new citation except those attached to open problems.

## 11. End of the document

| Part | Content |
|---|---|
| Acknowledgments | people (for what), grants with their number exactly as the funder requires; no bold type |
| Statements | as the venue requires: code and data availability, conflict of interest, author contributions, use of generative AI ([submission.md](submission.md) §1) |
| Appendices | omitted proofs, full tables, prompts, settings; each appendix is mentioned in the main text |
| References | cited works only; rules in [../bibliography/README.md](../bibliography/README.md) |

## 12. Length split

Guideline for a paper without a page limit; under a limit, shorten the core by moving proofs to an appendix, never the
introduction below intelligibility.

| Part | Share |
|---|---|
| Introduction including related work | 10–15 % |
| Preliminaries | 5–10 % |
| Core | 65–80 % |
| Conclusion | up to 5 % |

If the introduction exceeds a fifth of the paper, look for scene-setting and repetition first. A short introduction can
still be mostly padding: article 1 spends 9.4 % of its words on the introduction (665 of 7,045 in the summary of
`check-text.ps1`), but only 11 of its 31 sentences carry a checkable statement ([academic-style.md](academic-style.md) §9).

## 13. From the master's thesis to a paper

1. Choose the result and its dependencies (results map in `knowledge/research/<topic>.md`); a paper is not a shortened
   thesis but one story.
2. Check the statements against the list of known errors of the thesis.
3. Rewrite, do not shorten: write the introduction and motivation anew by §5; replace the exposition of known basics
   with a reference.
4. Unify terminology and notation with the paper (*chapter* → *section*, *Claim* → *Lemma*, macros).
5. Cite the thesis and say in the introduction what is taken over and what is new.
6. Check the venue's rules on text based on a thesis (venue card; preprint and self-archiving rules in
   [submission.md](submission.md) §6).

The opposite direction (papers → dissertation): [thesis.md](thesis.md).
