# Article 1 - Min Cut-Path Problem

## Intent

| | |
|---|---|
| Type | journal article (manuscript) |
| Language | English (American spelling) |
| Main file | `main.tex` (wrapper; text in `sections/`) |
| Class | `new-aiaa.cls` (`journal`), bibliography `new-aiaa.bst` via natbib - **temporary**; the article will later be moved to the template of the target journal (not chosen yet) |
| Template folder | `templates/new-aiaa/`; `new-aiaa.cls` and `new-aiaa.bst` here are byte-identical to it (SHA-256 compared 2026-10-08) and are never edited in the project |
| Bibliography | `references.bib` (12 entries, all cited and verified) |
| Origin | Overleaf export `archives/clanok_1_min_cut_path.zip` (2026-10-07) |
| Knowledge base | [knowledge/research/min-cut-path.md](../../knowledge/research/min-cut-path.md) |

## Status

Builds without errors or warnings (2026-10-08, after the split into files): 23 pages, no undefined references or
citations, no overfull lines, BibTeX without warnings. The text went through a full revision (formal errors,
consistency, language, sources) - see "Change history".

**Before submission the author must check the content changes** listed in "Content changes to review".

## Article contents

| Section | Label | Contents |
|---|---|---|
| I Introduction | `sec:introduction` | motivation, related problems, contributions, relation to the master's thesis |
| II Fundamentals | `sec:fundamentals` | cut-path, `CP(u,v)`, `cp(u,v)`, optimization version, Lemma *Basic Bounds*, average (1+ε)-approximation scheme |
| III NP-completeness | `sec:np-completeness` | 3-SAT → Separating Shortest Path (`sec:ssp`: chain, threads, calibration) → Min Cut-Path (`sec:ssp-to-mcp`) |
| IV Graphs of Diameter Two | `sec:diameter-two` | decomposition `I, J, K, L`, odd intersection of path and cut, `cp = c + d − 1` |
| V Graphs with Cut-Value at Most Two | `sec:cut-two` | cactus structure, `cp = c + d − 1` |
| VI Erdős–Rényi Graphs | `sec:random-graphs` | diameter 2 in dense graphs, properties of sparse ones, approximation scheme |
| VII Conclusion | `sec:conclusion` | summary, further directions |

Labels of statements: `lem:basic-bounds`, `thm:ssp-np-complete`, `alg:reduction`, `thm:mcp-np-complete`, `lem:cut-decomposition`,
`lem:empty-i-or-l`, `lem:odd-intersection`, `thm:diameter-two`, `rem:algorithm`, `thm:cut-two`, `thm:random-diameter-two`, `thm:random-diameter`,
`thm:random-connectivity`, `lem:degree-bounds`, `lem:connectivity-bounds`, `thm:approximation-scheme`.

## Files

```
main.tex                    wrapper, the only class-dependent file: \documentclass{new-aiaa}, \let\openbox/\Bbbk,
                            \setstretch in algorithmic, title, author, abstract wrapper, \input of the parts, \bibliography
preamble/packages.tex       graphicx, float, amsmath, tcolorbox, etoolbox, amsthm, amssymb, algorithm, algpseudocode
preamble/environments.tex   equation numbering, theorem environments (\newtheorem, shared counter), problem box
preamble/macros.tex         notation macros \cp, \CP, \diam, \OPT, \MinCutPath, \SSP, \ThreeSAT
sections/00-abstract.tex    abstract text
sections/01-introduction.tex, 02-fundamentals.tex, 03-np-completeness.tex, 04-diameter-two.tex,
sections/05-cut-two.tex, 06-random-graphs.tex, 07-conclusion.tex
sections/90-acknowledgment.tex   acknowledgment text (heading in main.tex)
references.bib              bibliography
new-aiaa.cls                document class (Overleaf, v1.2)
new-aiaa.bst                bibliography style
img/                        chain.png, chain-link.png, chain-link-types.png, chain-threads.png, threading.png, diameter-two-structure.png
```

Version before the revision: `archives/removed-from-projects/clanok-1-min-cut-path/main-before-revision-2026-10-07.tex`
(compare with the single-file version `main-before-split-2026-10-07.tex` in the same folder, or with `sections/`).

## Build

```powershell
.\scripts\build-project.ps1 -Project clanok-1-min-cut-path
```

PDF: [outputs/clanok-1-min-cut-path/main.pdf](../../outputs/clanok-1-min-cut-path/main.pdf)

Package (the only form in which the article is sent to a reviewer, a co-author or a journal; rule:
[latex-conventions.md](../../knowledge/writing/latex-conventions.md) §1.1):

```powershell
.\scripts\package-project.ps1 -Project clanok-1-min-cut-path -Template new-aiaa -CheckOnly   # after a new file, a new package, a touched class file
.\scripts\package-project.ps1 -Project clanok-1-min-cut-path -Template new-aiaa              # before sending: zip and PDF in outputs/clanok-1-min-cut-path/package/
```

Send only on `Verdict: PASS`. What the checks meet in this project:

- `main.tex` has no `\bibliographystyle`: the class sets `new-aiaa` itself (`new-aiaa.cls`, line 104).
- `main.tex` holds one layout-related line, `\AtBeginEnvironment{algorithmic}{\setstretch{1}}` (single spacing inside
  algorithms under the class option `journal`); deliberate, stays until the port.
- The folder was zipped by hand, unpacked elsewhere and compiled to the same 23 pages on 2026-10-08, before the
  script existed; the first `Verdict` of the script is not recorded here yet.

## Known problems

### Assessment (2026-10-07)

The article as a whole makes sense: definitions → NP-completeness → two polynomial classes → random graphs follow
from each other, and I found no error in the proofs in their current wording (I went through the reduction from
3-SAT, the theorem on diameter 2 and the theorem on cut ≤ 2 step by step and checked the formula on `K_n`, `C_4`, `C_5`,
`K_{2,3}` and the Petersen graph). Weak points, ordered by importance:

1. **Related work.** A comparison with close problems is missing. The closest one is the *non-separating st-path*
   (a path whose edge removal leaves the graph connected) - the mirror notion to Separating Shortest Path; its existence
   is NP-hard on general graphs (X. Mao, arXiv:2101.03519). Further, shortest-path interdiction / "most vital edges"
   and the Force Path Cut problem. A reviewer will almost certainly ask; the claim "not studied elsewhere" needs a
   paragraph on these works to back it.
2. **Definition II.5 vs. Theorem VI.6** - see below; moreover, "approximation scheme" usually means a family of
   algorithms parametrized by `ε`. Here it is one algorithm whose ratio tends to 1 - the result could be stated more
   simply and more strongly ("asymptotically optimal with high probability").
3. **Abstract and title** - the abstract does not state the results, the title is generic.
4. **Theorem VI.2** - the statement for `α > 1` holds, but the exact source is Chung, Lu: *The Diameter of Sparse
   Random Graphs* (2001): the diameter is `(1 + o(1)) log n / log(np)`; I recommend citing this work alongside [9].
5. **Motivation** - the introduction now says in one sentence what the cut guarantees in the model; the article does
   not return to the application later (fine for a theoretical article).

### Open points (unchanged)

- **Definition II.5** measures "almost all inputs" by the ratio `|I_opt(n)| / |I(n)|`, i.e. uniformly over all graphs
  (this corresponds to `p = 1/2`), while Theorem VI.6 speaks about `G(n, p)`. Proposal: add to item 3 a sentence that
  for inputs drawn from a probability distribution the ratio is replaced by a probability.
- **Abstract** does not state the results (NP-completeness, the formula `cp = c + d − 1`, the approximation scheme) -
  only the motivation.
- **Theorems VI.2 and VI.3** are cited after [9] and [10]; the exact wording and the theorem numbers in the books need
  checking (`TODO(verify)`); I did not have the books.
- Citation [3] for the cactus structure is given as "cf." - the work concerns the cactus representation of 2-cuts;
  the statement itself is justified directly in the article.
- Target journal and its template (to be decided later).
- The "Intent" section does not yet answer the four questions of
  [paper-structure.md](../../knowledge/writing/paper-structure.md) §1 (main claim, contributions, closest work, reader
  and venue): for the author to fill in.

### Deviations from the rules in `knowledge/writing/` (fix during the port to the target journal)

- References with `Theorem~\ref{...}`; no `cleveref` (`hyperref` and `natbib` are loaded by the class `new-aiaa`).
- Theorem environments with `\newtheorem[definition]` (correct only while cleveref is not loaded).
- Floats placed with `[H]` (package `float`).
- Figures are PNG drawings, not vector PDF.
- Acknowledgment file is `90-acknowledgment.tex` (convention: `90-acknowledgments.tex`).
- The PDF has empty Title and Author metadata (`pdfinfo outputs/clanok-1-min-cut-path/main.pdf`, 2026-10-08); rule:
  [latex-guide.md](../../knowledge/writing/latex-guide.md) §16.
- The algorithm prints "Require:" / "Ensure:" (`\Require`, `\Ensure` in `sections/03-np-completeness.tex`); the house
  rule is Input / Output ([math-writing.md](../../knowledge/writing/math-writing.md) §6). Apply when the article is ported.
- Template conformance ([latex-conventions.md](../../knowledge/writing/latex-conventions.md) §1.1): `new-aiaa` is not
  the target venue, and `templates/new-aiaa/` holds no sample file of the venue (its `main.tex` is a workspace
  skeleton), so "wrapper written from the venue's sample" cannot be checked for the current wrapper. The port writes
  a new wrapper from the target template's sample and moves `new-aiaa.cls` and `new-aiaa.bst` to
  `archives/removed-from-projects/clanok-1-min-cut-path/`.

## Content changes to review

These edits change the mathematical content or claims about the literature. They were made on the basis of findings
from the revision, but the author is responsible for them.

1. **The proof of NP-completeness of Separating Shortest Path (Theorem III.5) is rewritten.**
   - The procedure `Calibrate` was added (equalizing the lengths of both paths of each link of the chain; extending
     the connecting paths of the threads to at least `Λ` edges) and is called in the algorithm.
   - The correctness proof now has the steps: shortest paths are exactly the paths of the chain → the path must "hit"
     every thread → synchronization threads force consistent signs → clause threads correspond to satisfying the
     clauses → analysis of `G ∖ P` through "unused paths" and dead ends.
   - The algorithm uses the occurrence sets `O_i` and the indices `L_{j,k,i}` (position `j`, clause `k`, variable `i`)
     instead of `ℓ[0], ℓ[1]`; brackets fixed.
   - The definition of a thread now states that a thread contains no simple edges of the chain; the chain has `r`
     links (instead of `m`).
2. **Lemma II.4 (Basic Bounds) is new** - `max{c, d} ≤ cp ≤ c + d − 1` with a proof (in the master's thesis Claim 6
   and 7). The proofs of Theorems IV.5 and V.1 refer to it.
3. **Theorem V.1 (cut at most 2) has a proper proof** - taken from the master's thesis (Theorem 18) and completed with
   the argument about the bridge and the arcs of the cycles.
4. **Vertex degrees in `G(n, α log n / n)`**: the original "Degree Concentration" (all degrees in `(1 ± ε) α log n` for
   every fixed `ε`) does not hold for fixed `α` - the minimum and maximum degree are a constant factor away from
   `α log n`. Replaced by Lemma VI.4 (*Degree Bounds*): there are constants `0 < β₁ < β₂` depending only on `α` such that
   all degrees lie in `[β₁ log n, β₂ log n]`, with a proof via Chernoff bounds. Lemma VI.5 (bounds for `c(u,v)`) and the
   proof of Theorem VI.6 were adjusted accordingly. The resulting theorem on the approximation scheme does not change.
   **The same error is in the master's thesis (Theorem 28, Claim 29).**
5. **Theorem VI.6** (approximation scheme): the assumption `p ≥ α log n / n` is kept; the proof gained the monotonicity
   argument (adding edges does not increase distances and does not decrease `c(u,v)`).
6. **Theorem VI.1** (diameter 2 for constant `p`): `α > 1` instead of `α > 0`, and a citation [Bollobás] was added.
7. **Definition of cut-path in the problem boxes**: "contains subsets `P, C ⊆ S`" instead of "can be partitioned into
   `S = P ∪ C`" (consistent with Definition II.1).
8. **The optimization version is NP-hard** (originally "NP-complete").
9. **Introduction**: the problem is presented as introduced in the master's thesis [5]; a sentence was added that the
   NP-completeness is new and that the results on graph classes and random graphs come from the master's thesis.
   The conclusion refers to partial results for the class "diam or cut 2".
10. **Introduction, related work**: the wording at citations [1]–[3] is adjusted to match the content of the cited works
    (multi-terminal minimum cuts; representations of all minimum cuts; small cuts and edge connectivity).
11. Minor refinements: `u, v` lie in the same component; the odd-intersection lemma is stated for a cut `C` with two
    sides (originally the cut was called `c(u,v)`, which clashed with the value of the minimum cut); definition of the
    diameter ("at most `k`"); bound variables in the lemmas are `x, y`, so they do not clash with `u, v`.

12. **Added in the stylistic revision** (2026-10-07, second round): Remark IV.6 (if `cp = c + d − 1` holds, the union of
    any minimum cut and any shortest path is a minimum cut-path - this backs the sentence about the "simple
    algorithm"); item 4 in the definition of the chain (parts of the chain share a vertex only when they are adjacent);
    a one-sentence definition of `G(n, p)`; a sentence that for dense random graphs the problem can be solved exactly
    in polynomial time on almost all inputs.

## Change history

**2026-10-08 - bibliography synchronized with the canonical file**
- `references.bib`: the 12 entries are now identical to `knowledge/bibliography/references.bib`; header in English;
  author names with diacritics written as LaTeX escapes (Bollobás, Frieze–Karoński), printed output unchanged.
- One visible change in the PDF: the Nagamochi–Kameda reference now ends with its DOI
  `10.15807/jorsj.39.135` (Crossref record, resolves to J-STAGE). The extracted text of the paper before and after
  differs in that line only; still 23 pages.
- `.\scripts\check-bib.ps1 -Project clanok-1-min-cut-path`: 0 findings.

**2026-10-07 - split into files**
- The single `main.tex` became the wrapper `main.tex` plus `preamble/` and `sections/`:
  - `preamble/packages.tex`: the `\usepackage` lines (graphicx, float, amsmath, tcolorbox, etoolbox, amsthm, amssymb,
    algorithm, algpseudocode);
  - `preamble/environments.tex`: `\numberwithin`, the `\newtheorem` block and the `problem` tcolorbox;
  - `preamble/macros.tex`: the notation block (`\cp`, `\CP`, `\diam`, `\OPT`, `\MinCutPath`, `\SSP`, `\ThreeSAT`);
  - `sections/00-abstract.tex` … `07-conclusion.tex` and `90-acknowledgment.tex`: the text, verbatim;
  - `main.tex` keeps the class-dependent lines: `\documentclass`, `inputenc`, `\let\openbox\relax`, `\let\Bbbk\relax`,
    `\AtBeginEnvironment{algorithmic}{\setstretch{1}}`, title, author, the abstract and acknowledgment wrappers,
    `\bibliography`.
- The PDF is unchanged: the 23 page renders have identical SHA-256 hashes (`archives/test-evidence/2026-10-08/split-before-hashes.txt` vs
  `split-after-hashes.txt`) and the extracted text is identical (`split-before.txt` vs `split-after.txt`, same folder);
  re-checked 2026-10-08.
- The single-file version is archived at `archives/removed-from-projects/clanok-1-min-cut-path/main-before-split-2026-10-07.tex`.

**2026-10-07 - stylistic revision (second round)**
- Repetitions removed: the definition of cut-path no longer appears three times (the problem boxes refer to
  Definition II.1), doubled introductory sentences before definitions and theorems, the free-standing sentence
  "Without loss of generality… `L = ∅`".
- Shortened wordy phrasings (*It is a well-established result…*, *Building on the structural insights…*, *For a better
  understanding…*), statements of theorems and lemmas without "Formally:" where the formula only repeated the text.
- Uniform: *graphs of diameter two* (in words), *minimum cut-value*, `G(n, p)` (without `p(n)`), heading *Erdős–Rényi*
  with a dash, subheadings in proofs (`\paragraph{…}` with a period, the same names of steps in both NP-completeness
  proofs), figure captions.
- Parameters of the procedure `Thread` renamed to `(K_1, σ_1), …, (K_t, σ_t)`, so that they do not clash with the links
  `L_i`, the literal links `L_{j,k}` and the clause index `k`.
- Section VI: first the theorem on diameter 2, only then its consequence for Min Cut-Path (originally the other way round).
- Acknowledgment without bold type.
- The article has 23 pages.

**2026-10-07 - revision**
- Formal: removed a paragraph from the master's thesis referring to a nonexistent figure; caption for the figure of
  link types of the chain + a reference to it in the text; figures taken out of definitions; `\deg`, `\[ … \]`,
  removed `\Bigr.`; `c(v,v)` → `c(u,v)`; "Chapter/This chapter" → sections; QED marks at the ends of proofs
  (`\qedhere`); an opening sentence of the proof, so that "Proof." does not jump into the algorithm.
- Consistency: notation via macros (`\cp`, `\CP`), `CP(u,v)` everywhere; "Lemma~\ref"; labels according to the
  convention (`sec:`, `def:`, `lem:`, `thm:`, `fig:`); heading of section IV; uniform `$…$`.
- Language: typos and grammar in the whole text (e.g. *egde*, *prove show*, *a Average*, *for large random.*, *More
  Formally*, *Firstly/Secondly* → *First/Second*, missing dashes and articles), removed doubled sentences.
- Preamble: removed unused packages of the template (`textcomp`, `mhchem`, `siunitx`, `longtable`, `tabularx`,
  `fancyvrb`, `listings`, `subcaption`).
- Figures renamed: `chain_threads` → `chain-threads`, `chain_link` → `chain-link`, `Chain_link_example` →
  `chain-link-types`, `Threading` → `threading`, `2_diam_2` → `diameter-two-structure`.
- Bibliography (everything verified against the DOI / publisher page):
  | Entry | Correction |
  |---|---|
  | Mehlhorn, Neumann, Schmidt | journal *Algorithmica* 77(2), 309–335, 2017 (originally ACM TALG 12(1), 2016); key `Mehlhorn2017Certifying` |
  | Gomory, Hu | DOI `10.1137/0109047` (originally `…045`) |
  | Cormen et al. | ISBN 978-0-262-04630-5 (the original had an invalid check digit) |
  | Diestel | the 6th edition appeared in 2025, ISBN 978-3-662-70106-5 (originally 2023 and an invalid ISBN); key `Diestel2025` |
  | Frieze, Karoński | ISBN 978-1-107-11850-8 |
  | Godsil, Royle | ISBN 978-0-387-95220-8 |
  | Bollobás | added the series Cambridge Studies in Advanced Mathematics 73 |
  | Cook | type `@inproceedings`, key in `\cite` identical to the `.bib` |
  | Micheľ 2025 | new entry - master's thesis |
  | Itai–Shiloach, Henzinger et al., Nagamochi–Kameda | verified, data unchanged (Nagamochi–Kameda: DOI added 2026-10-08, see above) |

**2026-10-07 - import from Overleaf**
- `sample.bib` → `references.bib` (sample AIAA entries removed); `graph.jpg` (sample figure of the template) to the archive.
- Added to the preamble: `\let\openbox\relax` and `\let\Bbbk\relax` (conflict of `newtxmath` with `amsthm`/`amssymb`,
  which Overleaf skips).
- 25 MiKTeX packages installed: `newtx`, `xpatch`, `xstring`, `carlisle`, `binhex`, `footmisc`, `setspace`, `abstract`, `preprint`,
  `titlesec`, `lettrine`, `caption`, `quoting`, `natbib`, `mhchem`, `chemgreek`, `siunitx`, `translations`, `amscls`, `algorithmicx`,
  `algorithms`, `float`, `fancyvrb`, `txfonts`, `tex-gyre`. On another computer they have to be installed again (`-InstallMissing`).
