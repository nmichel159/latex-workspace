# Article 2 - Min Cut-Path on Graphs with Distance or Cut-Value at Most Two (first complete draft)

**Layout since 2026-10-09: the folder is what is sent.** `projects/clanok-2-min-cut-path/` holds eleven files and
no sub-folders: `main.tex` (the template's sample `sn-article.tex` with the content places filled in, one file, no
`\input`), `sn-jnl.cls`, `sn-mathphys-num.bst` (byte-identical to `templates/sn-jnl/`), `references.bib` and seven
figure PDFs, all used (`transformations.pdf` was retired on 2026-10-12, see "Change history").
To send: zip the content of the folder and submit it, after `package-project.ps1 -Template sn-jnl -Flat
-KeepComments` ends with `Verdict: PASS` (2026-10-12: PASS, 24 pages) and after the items under "Open items for the
author" are settled. **The manuscript is a first complete draft written on 2026-10-12 by an AI assistant from
Section 3.3 of the master's thesis, revised the same day after an independent referee pass; the author has not
read it yet** (see "Content to review").
Differences from the sample outside the content places: `\RequirePackage{float}` before `\documentclass`,
`\usepackage[T1]{fontenc}`, `thmtools` and `cleveref`, the sample's `proposition` line commented out and three
`\declaretheorem` lines, two `\algrenewcommand` lines, four notation macros, `\hypersetup` with the PDF title and
author (section "Preamble additions"); and line 28, where the two typographic quotes of the publisher's comment are
re-encoded from Windows-1252 to UTF-8 (the packager reads only UTF-8).
Working material that is never sent lies in `projects/clanok-2-min-cut-path.submission/`: `SPEC.md` (blueprint),
`drafts/` (math core, its notes, literature), `figures/` (TikZ sources), `checks/` (programs and results), `review/` (referee report `referee-math.md` and its
scripts), `integration-notes.md` (what the integration changed and noticed; its Section 8 lists the referee pass),
`ai-declaration.tex` (draft), `open-cases/` (a later phase, another session).

## Intent

| | |
|---|---|
| Type | journal article, theory (graph algorithms) |
| Language | English (American spelling) |
| Content source | **master's thesis *Min Cut-Path* (2025), Section 3.3**, the author's decision of 2026-10-07; restructured with the author's permission (new wording, new figures, complete proofs) |
| Main file | `main.tex` (the template's sample `sn-article.tex` filled in; the whole manuscript in one file) |
| Target journal | Algorithmica (Springer), the author's request of 2026-10-08; venue card [knowledge/venues/algorithmica.md](../knowledge/venues/algorithmica.md) |
| Class | `sn-jnl.cls` (Springer Nature journal article template 3.1, December 2024; `\ProvidesClass`: `sn-jnl 2019/11/18 v0.1`), options `pdflatex,sn-mathphys-num` (the reference style is inferred from Algorithmica's numbered citations, TODO(verify) on the venue card); bibliography `sn-mathphys-num.bst`, which the class selects itself (natbib `numbers,sort&compress`) |
| Template folder | `templates/sn-jnl/` (the template the Algorithmica submission guidelines recommend; download URL and SHA-256 in `templates/SOURCES.tsv`); `sn-jnl.cls` and `sn-mathphys-num.bst` here are byte-identical to it (packager, 2026-10-12) and are never edited in the project |
| Bibliography | `references.bib`: 17 entries copied from the canonical file by the literature step, 15 cited |
| Origin | empty folder `clanok_2 min cut-path`, renamed by the convention on 2026-10-07; skeleton 2026-10-08, flat folder 2026-10-09, text 2026-10-12 |
| Knowledge base | [knowledge/research/min-cut-path.md](../knowledge/research/min-cut-path.md) |

The four answers of `knowledge/writing/paper-structure.md` §1:

| Question | Answer |
|---|---|
| **Main claim** | For a pair of vertices with cut-value two, a minimum cut-path has `d(u,v)` edges exactly when one square of the chain formed by the minimum `u`-`v` cuts contains a path that lies on a shortest `u`-`v` path and separates two terminals of the square; in graphs in which every pair has distance or cut-value at most two this is decided in linear time, and without this class it is NP-complete. |
| **Contributions** | (1) Characterization for cut-value two in every graph: Theorem 11 (`thm:characterization`), with the separation criterion Lemma 10 and the square decomposition Theorem 9. (2) Linear time in the class for every pair with cut-value at most two, the decomposition included, by an algorithm that does not test membership in the class and on any connected graph returns a minimum cut-path or two vertices with distance and cut-value at least three: Theorem 15 (`thm:linear-time`) with Algorithm 1 and Lemma 14; all solved pairs of the class: Corollary 16. (3) NP-completeness of deciding `cp = d` for pairs with cut-value two in general graphs: Theorem 17 (`thm:hardness`). (4) What is known about the remaining pairs (`d = 2`, `c >= 3`): Proposition 18. |
| **Closest work** | Own: Section 3.3 of the thesis (Theorems 20, 22, 23: decomposition by three transformations, polynomial and linear algorithm, with proof sketches) and article 1 (NP-completeness of Separating Shortest Path; unpublished). Published: the structure of all minimum cuts between two vertices (Picard and Queyranne 1980; the strip of Dinitz and Vainshtein, read through Baswana and Pandey 2025; the cactus of 2-edge cuts, Mehlhorn, Neumann and Schmidt 2017). The square decomposition is this structure for cut-value two and is attributed, not claimed. No published work asks for a shortest path that is a cut, or for a cut-path under a bound on the cut-value (searches of 2026-10-12, `knowledge/literature/searches.md`, rows "article 2"). |
| **Reader and venue** | researchers in graph algorithms and connectivity; Algorithmica; no page limit; abstract 150-250 words (239), 4 to 6 keywords (5) |

## Status

First complete draft with the referee's findings applied, 2026-10-12: 24 pages A4 (text to page 22, declarations
and references on pages 23 and 24), 8764 words, 582 sentences (abstract 239 words, Introduction 1360 words =
15.5 %, Conclusion 266 words).
The build and all four checks are green (section "Build and checks"). Not ready to submit: every item under "Open
items for the author" and "Content to review" is open.

**Referee pass (2026-10-12).** An independent referee read `drafts/core.tex` line by line and tested it by its own
programs: report `projects/clanok-2-min-cut-path.submission/review/referee-math.md`. Verdict: no error; one gap
(G1: how `p_1`, `p_2` come out of the augmentations), three unclear places (U1 candidate rule, U2 promise
`G in DC_2`, U3 attribution of known structure), twelve minor points (M1-M12). Coverage of the review scripts:
11895 instances (7395 pairs on all graphs with 2 to 7 vertices, 3000 chains, 1500 random graphs) for the statements
of Sections 3 to 5, 81 example values, 0 failures. Applied on the coordinator's decision: G1, U1, U2, U3, M1-M9,
M11, M12; not applied: M10 (open item 13). What changed where: `integration-notes.md` §8. The numbering of the
statements did not change; Algorithm 1 has 29 lines instead of 22.

**Open case of the class (pairs with `d = 2`, `c >= 3`; working material, not in the manuscript).** Rounds 1-5 of AI
agents (2026-10-12 to 2026-10-22) in `projects/clanok-2-min-cut-path.submission/open-cases/`; state, review status and
how to resume: `open-cases/status.md`. Reviewed: equivalence to the zigzag problem ZZ + P2, the switch model is in P,
reduction to it after propagation (Theorem R), NP-completeness for distance three, quasi-polynomial algorithm.
**Since 2026-10-31 also reviewed: the open case is in P (`open-cases/r7-desc.md` Theorem B, `verify/rv-r7-desc.md`).** The
author has not read it. Nothing of it changes Section 7 of this manuscript ("we do not know a polynomial-time
algorithm"): the author decided on 2026-10-31 to write a new article (diameter three, the squares, ZZ + P2), and this
manuscript stays as it is until the author decides what happens to it.

### Open items for the author (before submission)

1. **Read the manuscript.** Every definition, statement and proof is new text written by an AI assistant
   ("Content to review").
2. **Title.** Working title: *Min Cut-Path on Graphs with Distance or Cut-Value at Most Two*. Alternatives:
   - *Min Cut-Path for Pairs of Vertices with Cut-Value Two*;
   - *Separating Shortest Paths and Minimum Cuts with Two Edges*;
   - *Min Cut-Path: A Linear-Time Case and NP-Completeness for Cut-Value Two*.

   The CV lists the working title *Polynomial-Time Solutions for Island Structures in the Min Cut-Path Problem*;
   reconcile the CV once the title is final (`knowledge/author.md`, open question). The title also stands in
   `\hypersetup{pdftitle=...}` in the preamble: change both.
3. **Declarations** (`\section*{Declarations}`). Placeholders "Statement." as in the sample, to be written by the
   author: *Funding*, *Conflict of interest/Competing interests* (the sample's double heading, choose one) and
   *Author contribution*. Filled in: ethics approval, consent for publication and materials "Not applicable.";
   data availability "No datasets were generated or analyzed during the current study."; code availability "Not
   applicable." (confirm: the checking programs are not part of the paper; if the AI statement mentions them,
   decide whether to offer them). Algorithmica returns a submission without the relevant declarations as
   incomplete; funding, competing interests and author contribution are also entered in the submission system.
4. **AI-use statement.** The manuscript has none. Draft for the author:
   `projects/clanok-2-min-cut-path.submission/ai-declaration.tex` (what the assistant did, where to insert it,
   placeholder for the model name and version). The use is far beyond copy editing, so Springer Nature requires
   the statement. All seven figures are TikZ drawings written by the assistant: decide whether the captions need
   a disclosure (`knowledge/writing/submission.md` §1.1). The sentence "the author reviewed ..." can be signed only
   after item 1.
5. **Article 1 must be public before article 2 is submitted.** Algorithmica's reference list holds only published
   or accepted works (`drafts/related-work.md` 4.4). Entry [2] prints "Manuscript (2026)". Theorem 17 rests on the
   NP-completeness of Separating Shortest Path, which exists only in article 1. Post article 1 on arXiv (or have
   it accepted), rewrite the entry, and re-read the locators: Theorem 3.10 (twice), Lemma 6.1, and the question
   about bounded `c(u,v)` in its conclusion. Article 1 is cited in four places; everything else is cited from the
   thesis.
6. **What the Introduction says about the thesis** (Section 1.4 and the third paragraph of Section 1): confirm.
   Thesis locators used: Section 3.3, Claims 7 and 17, Definitions 37 to 40, Figure 3.3, Theorems 15, 18, 20, 22,
   23 (read in the extracted text on 2026-10-12).
7. **Reference order.** The list is in citation order (default of `sn-mathphys-num.bst`); published Algorithmica
   lists are alphabetical ("Known problems").
8. **Figure file names and format.** The figures are PDF files named by content; Algorithmica's guide asks for
   `Fig1.eps` etc. ("Known problems", "Figures"). Renaming changes seven `\includegraphics` lines.
9. **`[referee]` option.** The template's user manual asks for double line spacing (`\documentclass[referee,...]`)
   "for the peer review and editorial stages"; the sample's active line and Algorithmica's guidelines do not use
   it. Decide at submission.
10. **Acknowledgements.** Text: "The idea of the Min Cut-Path problem is due to Martin Loebl, who supervised the
    master's thesis on which this paper is based." (facts of `knowledge/author.md`; no funding is named). Heading
    and placement: "Known problems".
11. **Bibliography, for the owner of the `.bib`:** two uncited entries (`Cormen2022`,
    `Schmidt2013TwoConnectivity`); entry [9] prints the pages `6:1--6:15` as "pp. 6-1615"; entry [8] prints no
    arXiv number; the thesis entry has no handle; no verified source for "submodularity of the cut function"
    (the sentence after Lemma 3 stands without a citation). Details: `integration-notes.md` §3, §4.
12. **`transformations.pdf`** (settled 2026-10-12): the unused drawing of the thesis's three transformations was
    moved to `archives/removed-from-projects/clanok-2-min-cut-path/2026-10-12-unused-figure/`; its TikZ source
    stays in `projects/clanok-2-min-cut-path.submission/figures/`. It returns only if the article describes the
    transformations with a figure.
13. **Mathematical points left after the referee pass** (from `review/referee-math.md`, `drafts/core-notes.md` §8,
    `checks/README.md` and `integration-notes.md` §6):
    - **Notation of the terminals (referee's M10, not applied).** `c_i`, `d_i` are vertices while `c(.,.)`,
      `d(.,.)` are the cut-value and the distance, and both occur in the statement of Theorem 11 (`d(d_i, v)` is
      one substitution away). The referee proposes `a_i'`, `b_i'` for the leaving terminals. Left as it is,
      because `a, b, c, d` is the notation of the thesis and the figures use it: the author decides (a change
      touches Definition 4, Theorems 9 and 11, Algorithm 1, the examples and Figure 3). Also `p` is a path in a
      square while `p_1`, `p_2` are the two fixed paths; `m` is an index, `m(A,B)` and `m_i`; `s`, `t` are
      vertices of `G_a`, a tail and a head in Proposition 12 and two terminals in Theorem 9(v). No clash makes a
      statement ambiguous.
    - Remark 2: it is not proved that every run of the thesis's construction ends with a union of minimum cuts;
      the remark describes the construction and does not claim it (the referee did not check it either).
    - Theorem 17 needs that the graph of the reduction of article 1 has `2n + 7m` pairwise edge-disjoint `u`-`v`
      paths (the count is in article 1, text after its Theorem 3.10). It no longer needs that this graph is
      connected, which article 1 does not state: since 2026-10-12 the proof restricts the graph to the component
      of `u` (one sentence, "Every `u`-`v` path lies in the component of `u`, ..."). Re-check the count and the
      theorem number if article 1 changes.
    - Section 1.1 and the first paragraph of Section 3 call the square decomposition "an explicit form" of the
      strip and say that Theorem 9(v) "corresponds to" the cactus of 2-edge cuts; neither is proved in the text.
    - The decomposition of the flow of value two into `p_1`, `p_2` is now proved in the text (referee's G1); the
      augmentation step itself is cited from Erickson, Section 10.4.
    - Proposition 12 is correct and tested but not used by Theorem 15; it can be cut if the paper must be shorter.
      Corollary 13 is no longer used in the proof of Theorem 15 (it explains why no pair is recorded in the class).
    - The paper makes no claim about the complexity of recognizing the class; Theorem 15 does not need it.
    - The vertices of `G_1` are digits, so edges print as `12`, `36`.
    - Observation 8 of `core-notes.md` (a separating trace has at most three distinct terminals) is false (21-vertex
      graph in `checks/README.md`); it is not in the manuscript.

## Article contents

| Section | Label | Contents |
|---|---|---|
| Abstract, keywords | - | problem; characterization for cut-value two; the class; linear time; the same algorithm on other graphs; NP-completeness; what stays open. Keywords: Separating shortest path, Edge connectivity, Minimum cuts, Linear-time algorithm, NP-completeness |
| 1 Introduction | `sec:introduction` | definition, bounds; results of the thesis and of article 1; the class and the two kinds of remaining pairs |
| 1.1 Related Work | `sec:related-work` | structure of minimum cuts (Menger, Picard-Queyranne, strip, cactus) and the attribution of the decomposition; paths whose removal keeps or breaks connections; local edge-connectivity, novelty of the class (one "to the best of our knowledge"), diameter two in Matching Cut and Most Vital Edges |
| 1.2 Our Results | `sec:results` | four numbered items with theorem numbers; item 3 says once that Theorem 17 answers, for the cut-value, the question of article 1 on bounded `c(u,v)` |
| 1.3 Techniques | `sec:techniques` | the decomposition localizes the question to the squares; traces of at most two edges; four candidates; residual graph; the padding of Theorem 17 |
| 1.4 Relation to the Thesis | `sec:thesis` | what is taken over, what is new |
| 2 Preliminaries | `sec:preliminaries` | |
| 2.1 Cut-Paths and Minimum Cuts | `sec:cut-paths` | notation, Definition 1, Lemmas 1 to 3 |
| 2.2 Graphs with Distance or Cut-Value at Most Two | `sec:class` | Definition 2, Proposition 4, Figures 1 and 2, Example 1, Proposition 5, Remark 1 |
| 3 Minimum Cuts of a Pair with Cut-Value Two | `sec:structure` | attribution paragraph; Lemma 6, Definition 3, Lemmas 7 and 8, Definition 4, Theorem 9, Figures 3 to 5, Examples 2 and 3 |
| 4 Separating Shortest Paths | `sec:separating` | Figure 6, Lemma 10, Theorem 11, Example 4, Proposition 12 |
| 5 A Linear-Time Algorithm | `sec:algorithm` | Corollary 13, Lemma 14 (attributed to Picard and Queyranne for directed networks), Algorithm 1 (no promise `G in DC_2`: it records a pair of terminals with `l >= 3`), Theorem 15 (for every connected graph: a minimum cut-path, or two vertices with `c >= 3` and `d >= 3` and a cut-path with `d(u,v) + 1` edges; the second outcome does not occur in the class), Example 5, Corollary 16, Remark 2 |
| 6 Hardness for Pairs with Cut-Value Two | `sec:hardness` | Theorem 17, Figure 7, the decomposition of the padded graph |
| 7 Pairs at Distance Two | `sec:distance-two` | Proposition 18; "we do not know a polynomial-time algorithm" for the class and `d = 2`, `c >= 3` |
| 8 Conclusion | `sec:conclusion` | what is known for the class and why cut-value two alone does not suffice; three numbered open questions (pairs with `d = 2`, `c >= 3` in the class; linear time for distance bound `k >= 3`; cut bound three). Nothing is said about deciding `cp = c` in general graphs or about graphs of diameter three |
| Acknowledgements, Declarations | - | back matter of the template |

### Numbered statements (as compiled on 2026-10-12)

Theorem, lemma, proposition and corollary share one counter; definition, example and remark have their own.
Parts of a statement are typed inline as (i), (ii) and cited as `\cref{lem:pieces}(iii)`.

| No. | Label | Content |
|---|---|---|
| Definition 1 | `def:cut-path` | cut-path, `cp(u,v)`, minimum cut-path |
| Lemma 1 | `lem:basic-bounds` | `max{c,d} <= cp <= c+d-1`; `cp = d` iff a separating shortest path exists |
| Lemma 2 | `lem:minimum-cuts` | a minimum cut leaves two components and is `delta(A)` for one `A`; parity |
| Lemma 3 | `lem:uncrossing` | `\|delta(A∩B)\| + \|delta(A∪B)\| = \|delta(A)\| + \|delta(B)\| - 2m(A,B)` |
| Definition 2 | `def:class` | the class `DC_2` (thesis, Definition 37) |
| Proposition 4 | `prop:class` | `c >= 3` is an equivalence relation; the class by distances inside its classes; diameter two and cactus graphs lie in it |
| Example 1 | `ex:counterexamples` | `G_a`, `G_b` |
| Proposition 5 | `prop:easy-pairs` | the four kinds of pairs (i)-(iv) |
| Remark 1 | `rem:bridges` | bridges change nothing |
| Lemma 6 | `lem:orientation` | (i) one edge on each of `p_1`, `p_2`; (ii) a path meets a minimum cut once; (iii) tail and head |
| Definition 3 | `def:pieces` | tail, head, piece, enters, leaves, square, link |
| Lemma 7 | `lem:pieces` | (i)-(iii) pieces and paths |
| Lemma 8 | `lem:degrees` | (i)-(iii) entering and leaving edges of pieces |
| Definition 4 | `def:decomposition` | order of the squares, terminals `a_i, b_i, c_i, d_i`, general path |
| Theorem 9 | `thm:structure` | square decomposition (i)-(v); (v): distinct terminals of a square have `c >= 3` |
| Examples 2, 3 | `ex:decomposition`, `ex:worked` | decompositions of `G_a` and `G_1` |
| Lemma 10 | `lem:criterion` | separation criterion (states its hypothesis `c(u,v) = 2` since the referee pass, as does Proposition 12) |
| Theorem 11 | `thm:characterization` | `cp = d` iff a square has a path `p` with (i) and (ii) |
| Example 4 | `ex:criterion` | `G_a`, `G_1`, `G_1'`, `G_1''` |
| Proposition 12 | `prop:lengths` | lengths through directed distances |
| Corollary 13 | `cor:two-edges` | in the class a shortest path has at most two edges in a square |
| Lemma 14 | `lem:residual` | minimum cuts and `F` from the residual graph |
| Algorithm 1 | `alg:cut-two` | 29 lines; labels `line:bfs`, `line:paths`, `line:residual`, `line:pieces`, `line:loop`, `line:length`, `line:record`, `line:edge`, `line:q`, `line:candidates`, `line:test`, `line:found`, `line:union`, `line:certificate`, `line:not-found` |
| Theorem 15 | `thm:linear-time` | for every connected graph, in linear time: decide `c(u,v) <= 2`; if so, `cp(u,v)` and a minimum cut-path, or two vertices `x, y` with `c(x,y) >= 3`, `d(x,y) >= 3` and a cut-path with `d(u,v) + 1` edges; the second outcome does not occur in the class |
| Example 5 | `ex:two-edges` | `G_a^+` |
| Corollary 16 | `cor:class-pairs` | the solved pairs of the class |
| Remark 2 | `rem:coarser` | coarser decompositions; relation to the thesis's construction |
| Theorem 17 | `thm:hardness` | NP-completeness for `c(u,v) = 2` |
| Proposition 18 | `prop:open-pairs` | `cp = c` iff a minimum cut contains a `u`-`v` path |

Figures: 1 `fig:graph-classes`, 2 `fig:counterexamples`, 3 `fig:square-decomposition`, 4
`fig:decomposition-example`, 5 `fig:worked-example`, 6 `fig:square-terminals`, 7 `fig:padding`; all cited in the
text, captions of one line, included at natural size.

## Files

```
projects/clanok-2-min-cut-path/     (everything in it is sent; no sub-folders)
main.tex                    sn-article.tex (template 3.1) with the content places filled in: preamble additions
                            (below), \title, \author*, \email, \affil (one author, no numbers), \abstract,
                            \keywords, Sections 1 to 8, \backmatter, \bmhead{Acknowledgements},
                            \section*{Declarations} with the sample's eight items, \bibliography{references};
                            the publisher's comments are kept
references.bib              17 entries (literature step), 15 cited
sn-jnl.cls, sn-mathphys-num.bst   venue files, byte-identical to templates/sn-jnl/ (the .bst from its bst/ folder)
graph-classes.pdf           Figure 1
counterexamples.pdf         Figure 2
square-decomposition.pdf    Figure 3
decomposition-example.pdf   Figure 4
worked-example.pdf          Figure 5
square-terminals.pdf        Figure 6
padding.pdf                 Figure 7

beside the folder (never sent)
projects/clanok-2-min-cut-path.md              these notes
projects/clanok-2-min-cut-path.submission/     SPEC.md, drafts/, figures/ (TikZ sources and README), checks/
                                               (README, programs, results), integration-notes.md,
                                               ai-declaration.tex, open-cases/ (later phase)
```

## Preamble additions

Everything is in `main.tex` at the places the sample provides; no layout override.

| Addition | Where | Why |
|---|---|---|
| `\RequirePackage{float}` | before the active `\documentclass` line | the class loads hyperref; `float`, loaded later by `algorithm`, would write every float anchor twice (pdfTeX "destination with the same identifier"). With the line: no such message for 7 figures and 1 algorithm |
| `\usepackage[T1]{fontenc}` | first line of the package block (since 2026-10-08) | "Known problems" |
| `\usepackage{thmtools}`, `\usepackage[capitalise,noabbrev]{cleveref}` | after the sample's package block | references by `\cref` |
| sample's `\newtheorem{proposition}[theorem]{Proposition}` commented out; `\declaretheorem[name=..., style=thmstyleone, sibling=theorem]` for `proposition`, `lemma`, `corollary` | the sample's theorem block; `theorem`, `example`, `remark`, `definition` keep the sample's `\newtheorem` lines and its numbering scheme | **route chosen after a test.** Plain route (cleveref, `\newtheorem{lemma}[theorem]{Lemma}`): builds, but `\cref` prints "Theorem 6(iii)" for Lemma 6 and "Theorem 5(ii)" for Proposition 5, because the class loads hyperref before amsthm and cleveref then cannot tell environments on a shared counter apart. With `thmtools`: "Lemma 6(iii)", "Proposition 5", "Corollary 13", "Lemmas 6 to 8" (checked in the PDF text). `thmtools` was installed already |
| `\algrenewcommand\algorithmicrequire{\textbf{Input:}}`, `\algrenewcommand\algorithmicensure{\textbf{Output:}}` | after the theorem block | the algorithm states input and output |
| `\cp`, `\DC`, `\MinCutPath`, `\SSP` | after them | notation (`\CP` is not used and not defined) |
| `\hypersetup{pdftitle=..., pdfauthor=...}` | after them | the class leaves both empty; `pdfinfo`: title and "Norbert Micheľ" |

## Build and checks

```powershell
.\scripts\build-project.ps1 -Project clanok-2-min-cut-path
.\scripts\check-text.ps1 -Project clanok-2-min-cut-path
.\scripts\check-bib.ps1 -Project clanok-2-min-cut-path
.\scripts\package-project.ps1 -Project clanok-2-min-cut-path -Template sn-jnl -Flat -KeepComments -CheckOnly    # after a structural change
.\scripts\package-project.ps1 -Project clanok-2-min-cut-path -Template sn-jnl -Flat -KeepComments               # before the folder is sent
```

`-Flat`: Springer Nature asks for all files in one directory. `-KeepComments`: the folder is sent with its comments.
No `-MaxPages`: Algorithmica states no page limit.

Results of 2026-10-12, after the referee pass:

| Check | Result |
|---|---|
| Build | exit code 0; 24 pages A4; no undefined reference or citation, no `??` or `[?]` in the PDF text, no multiply defined label, no overfull or underfull line; BibTeX: no warning, no error; 58 fonts, all Type 1 and embedded, no Type 3. Remaining messages are those of the class and its sample ("Known problems") |
| Pages | all pages rendered at 60 dpi (`tmp/clanok-2-integration/`) and inspected in the first pass (23 pages): title page, figures, algorithm, lists, declarations, references; after the referee pass the changed pages again (1, 3, 4, 16 to 22) |
| `check-text.ps1` | 3 findings, all kept: `[hedge]` "To the best of our knowledge" (once, for the class; rests on the search rows "task B1" of 2026-10-12 in `knowledge/literature/searches.md`); `[ai-tic]` "Vital" (part of the problem name Shortest Path Most Vital Edges); `[spelling]` "Acknowledgements" (the sample's heading). Resolved: three sentences over 40 words (abstract, results item 1, proof of Corollary 13) and one "the fact that" |
| `check-bib.ps1` | 17 entries, 15 keys cited; 3 findings: `[unused]` `Cormen2022`, `[unused]` `Schmidt2013TwoConnectivity`, `[recommended]` `LeLe2019MatchingCut` has no issue number (none in its Crossref record). The `.bib` belongs to the literature step and was not edited |
| Packager, `-CheckOnly` | `Verdict: PASS`; 1 finding `[ai-declaration]` (the reminder); `Trace scan: 9 files, 0 hits`; venue files identical to the template (run after `transformations.pdf` was retired) |
| Packager, full run | `Verdict: PASS`; 24 pages; 12 files in the zip (the eleven of the folder and `main.bbl`); 91 comment lines kept; `Trace scan: 12 files, 0 hits (0 allowed)`; 1 finding `[ai-declaration]` (run after `transformations.pdf` was retired and the proof of Theorem 17 was reworded) |
| Robust form of Algorithm 1 | `checks/check_robust.py`: all 12112 connected graphs with at most 8 vertices, 2983 chains in the class, 4789 random instances outside it; 1,758,504 assertions, no failure; without a recorded pair the value equals `cp` in every graph; no pair is recorded in the class; 7 mutation tests detected |
| Referee's scripts | `review/scripts/` (independent of `checks/`): 11895 instances for the statements of Sections 3 to 5 in their written form (7395 pairs on all graphs with 2 to 7 vertices, 3000 chains, 1500 random graphs), 81 example values, 0 failures; the algorithm without the promise (now Algorithm 1 and Theorem 15) is its test `ALG3` |
| Computational checks of the mathematics | `checks/README.md`: all 12112 connected graphs with at most 8 vertices (662244 ordered pairs, 181892 with `c = 2`) and 2953 random chains in the class (up to 40 vertices), every statement S0-S15 and every statement, example and named graph of the body (113 claims of named graphs, 0 mismatches); the algorithm against brute force on 258424 pairs with `c <= 2` and 2983 chains; 18 mutation tests, all detected; running time linear in measurements up to 218118 vertices. No statement of the manuscript failed. The evidence supports the statements and proves none of them |

## Known problems

- **Loose pages.** The sample sets `\raggedbottom`, and a page break before a theorem-like environment is
  preferred, so some pages end early (pages 7 and 13 of the build of 2026-10-12, both under two figures). No
  layout override was added. In the same build the statement of Theorem 15 starts at the foot of page 17 and ends
  under Algorithm 1 at the top of page 18.
- **"Figure 3" in the text, "Fig. 3" in the caption.** The class abbreviates in captions; `\cref` with the house
  options `capitalise,noabbrev` does not. Dropping `noabbrev` gives "Fig. 3" in the text and "Eq." for equations;
  not done, the author decides.
- **Algorithm 1.** Lines that do not fit (the output line, 6 and 20) continue at the left margin (`algpseudocode`
  default).
- **Abstract.** The class prints the math of the abstract in bold. It has 239 words of the 250 allowed.
- **Reference list as printed by `sn-mathphys-num.bst`:** [2] "Manuscript (2026)" (open item 5); [8] "arXiv
  preprint (2021)" without the number; [9] "pp. 6-1615" for `6:1--6:15`; [14] is a self-published book with a URL;
  the thesis entry has no handle.
- **AI declaration draft and the packager.** The packager looks for a draft in `projects/<project>/submission/`;
  the draft lies beside the folder, so the reminder says "no draft". Infrastructure, not changed.
- **T1 font encoding added to `main.tex`.** The class leaves `\RequirePackage[T1]{fontenc}` commented out; with its
  default OT1 the surname printed as "l" with a caron above instead of "ľ" and the PDF text lost every accent
  (`pdftotext`: "Michel", "Saf´arik"). The added line changes the encoding only (Computer Modern stays, Type 1 from
  `cm-super`); remove it if the journal objects.
- **Diacritics as TeX code.** Springer Nature's LaTeX page asks to write special characters as TeX code
  (`Miche\v{l}`, `Ko\v{s}ice`); the front matter and the `\hypersetup` line do, and new text should do the same.
- **Figures.** Springer Nature wants every file in one directory (the folder has no sub-folders) and Algorithmica prefers EPS for
  vector figures; the template's user manual still says the compiler "accepts only .eps", although the class's default
  option is `pdflatex`. An EPS figure (the template's `fig.eps`, tested in the modular layout) builds here: pdfLaTeX
  converts it with `epstopdf` (test: `archives/test-evidence/2026-10-09/sn-jnl-float/`). Whether submission.nature.com accepts
  PDF figures: TODO(verify); the seven figures are PDF. Captions print "Fig. 1" (class).
  Algorithmica's guide also asks for figure files named "Fig" plus the number (`Fig1.eps`), while the house rule
  names files by content; whether this applies to LaTeX source uploads: TODO(verify). Renaming changes every
  `\includegraphics` path.
- **Labelled lists.** In `sn-jnl` the optional argument of `enumerate` sets only the label width; the labels are fixed
  (`1.`, `(a)`, `(i)` by depth), so `\begin{enumerate}[(a)]` (article 1, thesis) silently prints `1.`. Loading
  `enumerate` or `enumitem` would replace the class's list layout. The manuscript uses plain `enumerate` only (results,
  open questions) and types the parts of statements inline as (i), (ii).
- **No `\DoNotLoadEpstopdf`.** The house template sets it when cleveref gets options; here it is left out on
  purpose, because it switches off `epstopdf` and EPS figures would stop building (`grfext`, the reason for it, is
  installed since 2026-10-08).
- **Reference order.** `sn-mathphys-num.bst` numbers references in citation order (its default); Algorithmica's
  guide says "numbered consecutively", while published Algorithmica lists are alphabetical. The `.bst` has an `alpha`
  option (an `@settings` entry with `options = "alpha"`, untested). TODO(verify) which order the journal wants.
- **Acknowledgments placement.** Algorithmica's guide puts acknowledgments on the title page; the template sets them
  with `\bmhead{...}` in the back matter. `main.tex` follows the template; since 2026-10-09 the heading is the
  sample's "Acknowledgements" (article 1 has "Acknowledgments", American English; `check-text.ps1` reports the
  British form). Decide before submission.
- **Class messages** (the pristine sample shows them too): `U/rsfs/m/n` size substitutions (from `mathrsfs` of the
  sample's package block), hyperref "Difference (4) between bookmark levels", one "Underfull \vbox (badness 10000) has
  occurred while \output is active" per page (24).
- **`\RequirePackage{float}` before `\documentclass`: in `main.tex` again since 2026-10-12** (it was left out on
  2026-10-09, when the sample's preamble was kept as it is, and came back with the first figure). The sample's block
  loads `float` (through `algorithm.sty`) after the class has loaded `hyperref`, so every figure and table anchor
  would be written twice (pdfTeX "destination with the same identifier (name{figure.1})"; the pristine sample shows
  it for each float). Loading `float` first removes it. Same fix as article 1 under `cas-sc`; not a layout change.

## Content to review

Everything. The manuscript was written on 2026-10-12 by an AI assistant (math core, figures, literature, checks
and integration as separate steps) and has been read by nobody else. The checks by computation
(`checks/README.md`) found no failing statement, but they are not proofs.

What deviates from the thesis, by place (details: `drafts/core-notes.md` §2 and §3):

1. **Definitions 3 and 4** (pieces, squares, links, terminals, general paths): defined from the union `F` of all
   minimum `u`-`v` cuts, not by the three transformations and Algorithm 5 of the thesis. The decomposition is
   therefore unique and is the finest one; the thesis's can stop earlier (Remark 2).
2. **Lemmas 6 to 8 and Theorem 9** are proved in full; the thesis uses most of them without proof. **Theorem
   9(v)** (distinct terminals of a square have cut-value at least three) replaces condition 2 of Definition 39 of
   the thesis, which put the distance bound into the definition; its proof by uncrossing is new.
3. **Lemma 10** (separation criterion) is the equivalence that the proof of Theorem 22 of the thesis asserts.
4. **Theorem 11** holds for every graph with `c(u,v) = 2` and uses distances in `G`:
   `d(u,x) + |p| + d(y,v) = d(u,v)`. The proof treats a case the thesis misses (the path `p` can be only the last
   part of the trace). **Proposition 12** gives the form with directed distances.
5. **Corollary 13** (at most two edges in a square) has a new proof; Claim 21 of the thesis argued from a figure.
6. **Lemma 14, Algorithm 1 and Theorem 15**: the decomposition is computed from two edge-disjoint paths and the
   strong components of the residual graph, so the whole computation is linear; the thesis assumes the
   decomposition as given. The rule "at most four candidates" is stated and proved (a separating path `x, w, y`
   shares an edge with a fixed path between the other two terminals); the algorithm removes edges, not vertices.
   The theorem is stated for `c(u,v) <= 2`, not for "every pair except `d = 2`, `c >= 3`": a pair with `d = 1` and
   `c >= 3` needs one minimum cut (Corollary 16). **Since the referee pass the theorem and the algorithm are
   stronger than in the thesis and in the first draft** (item 11).
7. **Theorem 17** (NP-completeness for cut-value two) is new and rests on article 1.
8. **Proposition 18** is the argument inside the proof of Theorem 15 of the thesis, stated for every pair.
9. **Written by the integration step and not in the math core:** title, abstract, keywords, Section 1, Section 8,
   acknowledgements, declarations; in the body the attribution sentences and citations listed in
   `integration-notes.md` §1 (first paragraph of Section 3, the sentences before Lemma 1 and Lemma 14, the
   folklore sentence on cactus graphs, the sentence on 3-edge-connected components, one sentence in the proof of
   Corollary 16, the reworded sentence on diameter two in Section 7, the shortened caption of Figure 3). No
   statement and no proof was changed.
10. **Claims about the literature** (Sections 1.1 and 3) come from `drafts/related-work.md`; several sources were
    read as preprints or reports, so no statement numbers are cited for them (its §4.2).
11. **Changed in the referee pass** (old and new wording of each: `integration-notes.md` §8). Statements:
    - **Theorem 15** (referee's U2): no hypothesis `G in DC_2`. For every connected graph the algorithm decides
      `c(u,v) <= 2` in linear time and then returns `cp(u,v)` with a minimum cut-path, or two vertices `x, y` with
      `c(x,y) >= 3` and `d(x,y) >= 3` (they show that the graph is not in the class) with a cut-path of
      `d(u,v) + 1 <= cp(u,v) + 1` edges; the second outcome does not occur in the class.
    - **Algorithm 1** (U1, U2): input "a connected graph"; a pair of terminals with `l >= 3` is recorded; the
      candidates are the paths `x, w, y` such that `xw` or `wy` is an edge of `q`; a recorded pair is returned with
      `R ∪ C` if no separating path is found; new caption and output line.
    - **Lemma 10 and Proposition 12** (M9): the hypothesis `c(u,v) = 2` is part of the statement.

    Proofs and other text: proof of Theorem 15, first step (G1: `p_1`, `p_2` are read from the flow of value two
    by two searches, with the argument), its correctness part (U2: three new steps, Corollary 13 no longer used)
    and its running time (U1, M8: adjacency lists, at most two edges of `q` at `x` and at `y`, cost of marking);
    the paragraph after Theorem 15; proof of Corollary 16; Example 5 (wording of the candidate); the sentence
    before Lemma 14 (U3); proof of Theorem 9(v) (M5, M11); proof of Lemma 2 (M11); proof of Corollary 13 (M6);
    the sentence after Proposition 12 on the directed form of Theorem 11 (M7); proof of Theorem 17 (M2:
    `2n + 7m >= 9` threads for a formula with at least one clause); opening of Section 6 (M4); last paragraph of
    Section 7 (M3); and one sentence each in the abstract, Sections 1.2 (items 2 and 3), 1.3 and 8.

## Change history

**2026-10-08 - template for Algorithmica (sn-jnl, Springer Nature template 3.1)**
- Template: `templates/sn-jnl/` from the zip linked by https://www.springernature.com/gp/authors/campaigns/latex-author-support
  (recommended by the Algorithmica submission guidelines), `\ProvidesClass` line: `sn-jnl 2019/11/18 v0.1`.
- Skeleton: `preamble/`, `sections/`, `img/`, `references.bib` copied from `templates/article-modular`; `sn-jnl.cls` and
  `bst/sn-mathphys-num.bst` copied from the template unchanged.
- Wrapper: new `main.tex` from `sn-article.tex`: class options of the sample's active line, its standard package block,
  front matter for one author (`\author*`, `\affil*` without numbers; `\affil` since 2026-10-09), back matter
  (`\backmatter`, `\bmhead{Acknowledgments}`, `\section*{Declarations}`); added `\usepackage[T1]{fontenc}`, cleveref,
  `\hypersetup` with title and author.
- preamble/: removed amsmath, amssymb, amsthm, graphicx, booktabs, algorithm, algpseudocode from `packages.tex`
  (loaded by the sample's block in `main.tex` or by the class; restored 2026-10-09); theorem styles switched to the class's `thmstyleone`,
  `thmstyletwo`, `thmstylethree` as the sample assigns them; Min Cut-Path macro block added.
- sections/: new `92-declarations.tex`; the abstract's comment states Algorithmica's 150-250 words.
- Bibliography: `sn-mathphys-num` (numbered, square brackets, as Algorithmica asks); no BibTeX warnings beyond the empty list.
- Build: 2 pages, undefined references 0, overfull 0; fonts Type 1 only.
- Package: `package-project.ps1 -Template sn-jnl -Flat`: Verdict PASS; `[layout]`: none.
- MiKTeX packages installed with the author's consent: `threeparttable`, `jknappen`, `ncctools`.

**2026-10-09 - float anchors, review fixes**
- `main.tex`: `\RequirePackage{float}` before `\documentclass` (duplicate float destinations otherwise, see "Known
  problems"); heading `\bmhead{Acknowledgments}` in American spelling (`check-text.ps1` finding); `\affil` instead of
  `\affil*` (with one author the starred form printed an asterisk that pointed to nothing); comments on what is
  class-dependent and on the absent `\DoNotLoadEpstopdf`.
- `preamble/packages.tex`: amsmath, amssymb, amsthm, graphicx, booktabs, algorithm, algpseudocode back in (no-ops after
  the sample's block); `preamble/environments.tex`: comment that the style names belong to `sn-jnl`.
- `sections/92-declarations.tex`, `sections/02-preliminaries.tex`: comments only (submission-system items; figure
  names point to "Figures" under "Known problems").
- Known problems added: figure file names, labelled lists, `\DoNotLoadEpstopdf`, the per-page underfull message.
- Build: 2 pages, no undefined references, no overfull lines. Package: `-Template sn-jnl -Flat` Verdict PASS.

**2026-10-09 - flat folder** (recorded here on 2026-10-12 from the former header of these notes)
- The modular layout was replaced by the template's sample filled in: one `main.tex` without `\input`, the venue
  files and `references.bib` beside it; the old files are in
  `archives/removed-from-projects/clanok-2-min-cut-path/2026-10-09-before-flat/`. cleveref, `\hypersetup`,
  `\RequirePackage{float}`, the extra environments and the macros were not taken over then.
- Package: `-Template sn-jnl -Flat -KeepComments` Verdict PASS, 2 pages, 82 comment lines kept.

**2026-10-12 - first complete draft from Section 3.3 of the thesis**
- Steps (each with its own files in `projects/clanok-2-min-cut-path.submission/`): blueprint `SPEC.md`; math core
  `drafts/core.tex` with `core-notes.md`; literature `drafts/related-work.md`, 17 entries in `references.bib`, seven
  reading notes; eight figures (`figures/`, PDFs in the project folder); computational checks `checks/`;
  integration (this entry).
- `main.tex`, preamble: `\RequirePackage{float}` before the class; `thmtools` and `cleveref`; `proposition`, `lemma`,
  `corollary` by `\declaretheorem` on the counter of `theorem` (plain `\newtheorem` route tested first and rejected:
  `\cref` named a lemma "Theorem"); `Input:`/`Output:` for the algorithm; macros `\cp`, `\DC`, `\MinCutPath`, `\SSP`;
  `\hypersetup` with the PDF title and author.
- `main.tex`, content: title, abstract (216 words), five keywords; Section 1 (problem, known results, the class,
  related work by idea, four numbered results, techniques, relation to the thesis); Sections 2 to 7 from
  `drafts/core.tex` with citation keys and locators, attribution sentences and every `% CITE` comment replaced
  (list: `integration-notes.md` §1; no statement or proof changed); Section 8 (what is known, three numbered open
  questions); acknowledgements; declarations (three placeholders left for the author).
- Citations: the thesis for everything the thesis contains; article 1 in four places (Theorem 3.10 twice, Lemma 6.1,
  the question on bounded `c(u,v)`).
- Drafts beside the folder: `ai-declaration.tex` (not in the manuscript), `integration-notes.md`.
- Build: 23 pages, no undefined references, no overfull lines, BibTeX clean. `check-text.ps1`: 3 findings kept.
  `check-bib.ps1`: 2 unused, 1 recommended. Packager `-Template sn-jnl -Flat -KeepComments`: `-CheckOnly` PASS; full
  run PASS with `[unused]` `transformations.pdf` and the `[ai-declaration]` reminder.
- Resolved from the former "Known problems": the empty PDF title and author; the messages of the empty
  bibliography. The former section "Needed before writing" is settled (scope: Section 3.3; intent above; the text
  was written from the PDF and the extracted text of the thesis).

**2026-10-12 - referee pass**
- Report: `projects/clanok-2-min-cut-path.submission/review/referee-math.md` (no error; G1, U1-U3, M1-M12); its
  scripts: 11895 instances, 81 example values, 0 failures.
- Applied in `main.tex` on the coordinator's decision (statements and proofs changed on purpose): G1 with M12
  (`p_1`, `p_2` from the flow of value two), U1 (candidate rule by the edges of `q`), U2 (Algorithm 1 and Theorem 15
  without the promise `G in DC_2`; dependent sentences in the caption, after the theorem, in Corollary 16, the
  abstract, Sections 1.2, 1.3 and 8), U3 (sentence before Lemma 14 sharpened; the other two places were covered),
  M2 to M9 and M11; M1 was already satisfied. Not applied: M10 (names of the terminals; open item 13).
- No claim about the complexity of recognizing the class and no citation for robust algorithms was added.
- Numbering of statements unchanged; Algorithm 1: 29 lines (22 before); the caption of Algorithm 1 kept to one line.
- Build: 24 pages (23 before), no undefined references, no overfull lines, BibTeX clean. `check-text.ps1`: 3
  findings kept (one new long sentence split). `check-bib.ps1`: unchanged. Packager: `-CheckOnly` PASS, full run
  PASS (`[unused]` `transformations.pdf`, `[ai-declaration]`).
- Record of every change with the old and the new wording: `integration-notes.md` §8.

**2026-10-12 - after the referee pass (coordinator)**
- `main.tex`, proof of Theorem 17: "is connected and contains" became "contains", and one sentence was added
  ("Every `u`-`v` path lies in the component of `u`, so restricting a graph to this component changes neither its
  shortest `u`-`v` paths nor whether one of them is separating."). Reason: article 1 does not state that the
  graph of its reduction is connected; the proof now does not need it.
- `transformations.pdf` moved from the project folder to
  `archives/removed-from-projects/clanok-2-min-cut-path/2026-10-12-unused-figure/` (not used by the build).
- The robust form of Algorithm 1 was tested against brute force: `checks/check_robust.py`, `results-robust.txt`
  (1,758,504 assertions, no failure; 7 mutation tests detected).
- Build: 24 pages, no undefined references, no overfull lines. `check-text.ps1`: the same 3 findings. Packager
  `-CheckOnly`: `Verdict: PASS`, 1 finding (`[ai-declaration]`); the folder has eleven files.
- Knowledge base: `knowledge/research/min-cut-path.md` (Section 3a on article 2, related structures, open
  problems, glossary) and `knowledge/literature/README.md` (seven new notes) updated.
