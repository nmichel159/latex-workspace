# Notes on facial defect colorings (working notes, first version)

Research notes on a problem from the talk abstract of S. Volesková (joint work with I. Fabrici), CSGT 2026:
*is there a plane graph without a `[1,1,2]`-edge coloring?* Started 2026-10-13 on the owner's request
("try to solve the problems, mainly examples for the smaller cases they did not solve").
**Written by an AI assistant in one session; the owner has not read it and no second reader checked the proofs.**
The session was stopped early on the owner's request (credits); "How to continue" lists what is left.

## Intent

| | |
|---|---|
| Type | working notes (not an article yet), 5 pages |
| Language | English (American spelling) |
| Main file | `main.tex`, one file, class `article` of the TeX distribution (no venue, no template files) |
| Bibliography | `references.bib`, 8 entries, all cited, copied from the canonical file (section "Facially constrained colorings of plane graphs") |
| Figure | `two-color-examples.pdf` (TikZ source in `poznamky-facial-defect.submission/figures/`) |
| Knowledge base | [knowledge/research/facial-defect-colorings.md](../knowledge/research/facial-defect-colorings.md) |
| PDF | [outputs/poznamky-facial-defect/main.pdf](../outputs/poznamky-facial-defect/main.pdf) |

The project name `poznamky-<topic>` is a new type beside `clanok-`, `praca-`, `cv` (notes, not a manuscript).

## Answer to the owner's question (state of 2026-10-13)

- **No example was found.** Every plane graph that was examined has a `[1,1,2]`-edge coloring, also in the
  stronger trail reading: all 3-connected plane graphs with at most 22 edges (693 855), all connected plane
  multigraphs with at most 8 edges (77 274 graphs, two programs), 2.8 million random plane graphs with 10 to 45
  edges. The run over the 4 820 218 plane multigraphs with 9 and 10 edges was still computing when the session
  was stopped (see "How to continue", item 1); the PDF therefore states the result for at most 8 edges.
- The same holds for `[1,1,2]`-vertex colorings (this would strengthen Jendroľ's `[2,2,2]` theorem) and for facial
  total-colorings with five colors on the 3-connected graphs with at most 22 edges.
- The evidence points the other way: `[1,1,2]` probably always exists (Conjecture 5.1 of the notes).
- **Two colors (not in the abstract; a by-product):** the lists `[2,2]` and `[1,3]` fail for edges; the notes show a
  3-connected graph for each (Figure 1). `[2,3]`, `[3,3]`, `[1,4]`: no failure found. It is not known to us whether
  the authors considered two colors; the owner asked about this and was told so.
- TODO(verify): which cases the talk named as open. Only the one-page abstract was available.
- TODO(verify): the authors' definition of the defect of a total coloring; the notes use a type-wise reading
  (vertices and edges separately, incident elements always different).

## What the notes contain

| Section | Content | Status |
|---|---|---|
| 1 | definitions (corner, facial trail and facial path, defect list), trail reading and path reading, known results, the question | written |
| 2 | computer search: sets (M), (P), (R); Proposition 2.1; Table 1 (smallest graphs without a coloring) | (M) is stated for at most 8 edges; to be raised to 10 when the run is in |
| 3 | Theorem 3.1 (parity criterion for the third color class), Proposition 3.2 (product construction from a vertex 2-coloring and a face 2-coloring), Corollary 3.3 (quadrangulations), Proposition 3.4 (reduction; a smallest counterexample has no vertex of degree one and no face of length one) | proofs written, **not refereed** |
| 4 | two colors: Proposition 4.1 and Figure 1 | verified by two programs |
| 5 | Conjectures 5.1 (edges) and 5.2 (vertices), open questions | written |

Theorem 3.1 was tested by program on every subset `S` of every plane multigraph with at most 7 edges
(`checks/logs/hyp_parity_m7.log`: 0 mismatches).

## Files

```
projects/poznamky-facial-defect/           main.tex, references.bib, two-color-examples.pdf
projects/poznamky-facial-defect.md         these notes
projects/poznamky-facial-defect.submission/
  figures/two-color-examples.tex           TikZ source of the figure (standalone)
  checks/                                  programs and logs (README.md there)
knowledge/research/facial-defect-colorings.md   topic map: definitions, known results, our results, proof ideas
knowledge/literature/                      notes Voleskova2026FacialDefect, Jendrol2026ThreeColoring,
                                           Czap2021FacialPaths, Czap2019FacialRST; searches.md rows of 2026-10-13
knowledge/sources/papers/Voleskova2026FacialDefect.pdf, .txt   the abstract the owner linked
```

## How to continue

1. **Finish set (M).** The run `node allmaps.js 10 9` over all plane multigraphs with at most 10 edges was at the
   last level when the session stopped. A watcher copies its log to `checks/logs/allmaps10.log` when it ends; if
   that file is missing, rerun the command in `checks/` (about one hour, 1 GB). Then check that the lines
   `E[1,1,2]`, `V[1,1,2]`, `V[1,2,2]`, `T[...]` are absent from "NOT colorable" and raise (M) in `main.tex` from
   eight to ten edges: the abstract, item (M) (4 897 492 graphs), the sentence on the unfinished run, the bound
   "at least nine edges" after Proposition 2.1 (then eleven), and column "(M)" of Table 1 (smallest `m` of each
   line of the log).
2. **Referee pass** on Theorem 3.1, Propositions 3.2 and 3.4, Corollary 3.3 (independent reader or subagent).
3. **Prove or refute Conjecture 5.1.** Ideas collected in the topic map, section "Proof ideas": exchange argument
   on inclusion-minimal admissible sets; the 4-coloring form (a facially proper 4-edge-coloring with two colors that
   never alternate `XYX` on a face; true for all multigraphs with at most 8 edges); reduction plus discharging.
   The product construction alone cannot prove it for all graphs (fails for the theta graph with three paths of
   three edges) and for 3-connected graphs it would imply a case of Conjecture 3 of Czap, Fabrici and Jendroľ.
4. **Larger search.** 3-connected graphs with 23 edges (1 645 576 graphs, about one hour with `poly.js 23 main`);
   plane multigraphs with 11 edges need a generator that does not store a level (37 million graphs).
5. **Ask the authors or the owner** for the two TODO(verify) items above.
6. If the notes are sent to anybody: add an AI-use statement (the packager reports `[ai-declaration]`), then run
   `package-project.ps1 -Project poznamky-facial-defect -KeepComments`.

## Build and checks

```powershell
.\scripts\build-project.ps1 -Project poznamky-facial-defect
.\scripts\check-text.ps1 -Project poznamky-facial-defect
.\scripts\check-bib.ps1 -Project poznamky-facial-defect
.\scripts\package-project.ps1 -Project poznamky-facial-defect -CheckOnly
```

State of 2026-10-13: build clean, 5 pages; static package check `Verdict: PASS` (one note: no AI declaration).

## Known problems

- The proofs are unrefereed (item 2).
- Bibliography: `Jendrol2026Corrigendum`, `Czap2021FacialPaths` and `Czap2019FacialRST` are `PARTIAL` in the
  canonical file (issue number not seen on the publisher's PDF); complete them before any submission.
- Tutte's wheel theorem is cited through the notes of Chapter 3 of Diestel's book, not from Tutte's paper.
- The abstract of Volesková is the only source for the theorems `[1,2,2]` and `[1,1,1,2,2]`; no paper was found.
- Session incident: at the start of the computations a hung run was stopped with `taskkill /F /IM python.exe`,
  which ended every Python process on the machine (four processes), not only the run. Reported to the owner.

## Change history

- 2026-10-13: project created; programs, searches, first version of the notes.
