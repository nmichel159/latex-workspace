# Literature notes

What we actually read in other people's papers and what we use from it. Every claim a manuscript makes about the
literature traces to a note with a location in the source; related-work comparisons are never written from memory.

## Files

| File | Contents |
|---|---|
| `<BibKey>.md` | note on one paper; the file name is its key in [../bibliography/references.bib](../bibliography/references.bib) |
| [searches.md](searches.md) | log of literature searches: date, source, query, what was found |
| [_template.md](_template.md) | template for a note |
| `../sources/papers/<BibKey>.pdf` | full text, if the author supplied it (+ `.txt` from `pdftotext`) |
| `../research/<topic>.md` | topic map: how papers group, what is known, what is open |

Write a note for every paper a text relies on (uses its theorem, compares against it, adopts its definition).
A paper cited only for a standard notion needs no note.

## Notes in this folder

Notes for the map [../research/min-cut-path.md](../research/min-cut-path.md) (article 1), written 2026-10-09:

| Note | Topic | Reading status |
|---|---|---|
| [Abhinav2022NonSeparating.md](Abhinav2022NonSeparating.md) | shortest non-separating and non-disconnecting s-t paths (MFCS 2022) | full text |
| [Mao2021NonSeparating.md](Mao2021NonSeparating.md) | non-separating s-t path, edge version; NP-hard; chordal graphs (preprint) | sections 1, 2, 9 |
| [Bazgan2019MostVital.md](Bazgan2019MostVital.md) | most vital edges for shortest paths; diameter two easy, three hard | preprint: section 1, theorems |
| [Bentert2025NetworkDiversion.md](Bentert2025NetworkDiversion.md) | network diversion: minimal cut containing a given edge | section 1 |
| [LeLe2019MatchingCut.md](LeLe2019MatchingCut.md) | matching cut by diameter: two polynomial, three and more NP-complete | sections 1, 2, 4.2 |
| [Komusiewicz2020MatchingCut.md](Komusiewicz2020MatchingCut.md) | matching cut, kernels and exact algorithms (DAM) | abstract, section 1 |
| [ChungLu2001.md](ChungLu2001.md) | diameter of G(n, p) near the connectivity threshold (tool for Section 7 of article 1) | theorem statements, one proof |
| [Feige1998Threshold.md](Feige1998Threshold.md) | gap version of 3-SAT with five occurrences of every variable (tool for Theorem 4.3 of article 1, no PTAS; written 2026-10-10) | abstract, Section 2.1 |
| [Marx2013Separators.md](Marx2013Separators.md) | treewidth reduction: small minimal separators lie in a torso of bounded treewidth (tool for Section 8 of article 1; written 2026-10-10) | preprint: Sections 1, 2, 3.1-3.3 |
| [Stuart2009Eavesdropping.md](Stuart2009Eavesdropping.md) | in graphs of diameter two the cut-value of every pair is the smaller of the two degrees (known theorem behind Corollary 5.7 of article 1; written 2026-10-10) | abstract, Section 4, references |
| [Baier2010LengthBounded.md](Baier2010LengthBounded.md) | length-bounded cuts: definition, NP-hard to approximate within 1.1377 (written 2026-10-10) | published abstract; authors' manuscript: Table I, Theorems 3.9, 3.11 |
| [EilamTzoreff1998Disjoint.md](EilamTzoreff1998Disjoint.md) | two disjoint paths, one of them shortest: NP-complete (mirror of Separating Shortest Path, Discrete Applied Mathematics; written 2026-10-10) | pp. 113-120, read by a search subagent |

Notes written for article 2 (same map), 2026-10-12:

| Note | Topic | Reading status |
|---|---|---|
| [PicardQueyranne1980.md](PicardQueyranne1980.md) | all minimum s-t cuts are the closed sets of the residual graph of one maximum flow (source of the structure behind the square decomposition, Sections 3 and 5 of article 2) | authors' technical report in full; of the published chapter the abstract |
| [Mehlhorn2017Certifying.md](Mehlhorn2017Certifying.md) | 3-edge-connected components as vertex classes; cactus of the 2-edge cuts (Lemma 11) | arXiv v3: abstract, Sections 1, 2, 4, 10-12 |
| [NagamochiKameda1996.md](NagamochiKameda1996.md) | cactus representation of all global minimum cuts; credits Dinits, Karzanov, Lomonosov and Picard, Queyranne | publisher's PDF: abstract, Sections 1, 3.1-3.3 |
| [BaswanaPandey2025Carcass.md](BaswanaPandey2025Carcass.md) | connectivity carcass of Dinitz and Vainshtein; the strip (balanced DAG) of all minimum cuts between two vertices | arXiv v4: abstract, Sections 1, 1.1, 4.1 |
| [Aboulker2017Coloring.md](Aboulker2017Coloring.md) | graph classes defined by bounded local edge-connectivity (nearest named classes to the class of article 2) | arXiv v2: abstract, Section 1 |
| [Erickson2019Algorithms.md](Erickson2019Algorithms.md) | textbook statements: breadth-first search, strong components, augmenting paths and flow decomposition (Section 5 of article 2) | Sections 6.5, 6.6, 8.4, 10.3, 10.4 |
| [Schmidt2013TwoConnectivity.md](Schmidt2013TwoConnectivity.md) | bridges and 2-edge-connectivity in linear time by chain decomposition | arXiv v1 in full |

Notes for the map [../research/facial-defect-colorings.md](../research/facial-defect-colorings.md) (project `poznamky-facial-defect`), written 2026-10-13:

| Note | Topic | Reading status |
|---|---|---|
| [Voleskova2026FacialDefect.md](Voleskova2026FacialDefect.md) | talk abstract: every plane graph has a `[1,2,2]`-edge coloring and a `[1,1,1,2,2]`-total coloring | full (one page) |
| [Jendrol2026ThreeColoring.md](Jendrol2026ThreeColoring.md) | 3-coloring of the vertices with monochromatic facial paths of at most two vertices; corrigendum | Sections 1-3, end of the proof; corrigendum Sections 1-2 |
| [Czap2021FacialPaths.md](Czap2021FacialPaths.md) | 2- and 3-colorings of the vertices without long monochromatic facial paths; conjectures | full |
| [Czap2019FacialRST.md](Czap2019FacialRST.md) | facial `[r,s,t]`-colorings; source of the statements on facial edge- and total-colorings | abstract, Section 1, Section 4.1 |

The notes below belong to the map [../research/llm-optimization.md](../research/llm-optimization.md); all were written 2026-10-08.

| Note | Topic | Reading status |
|---|---|---|
| [RomeraParedes2024FunSearch.md](RomeraParedes2024FunSearch.md) | FunSearch: evolutionary program search with an LLM | main text and Methods |
| [Liu2024EoH.md](Liu2024EoH.md) | EoH: co-evolving thoughts and code | sections 1-6 |
| [Ye2024ReEvo.md](Ye2024ReEvo.md) | ReEvo: reflective evolution, LLM as hyper-heuristic | sections 3-8, Appendix C |
| [Zhang2024EvolutionarySearch.md](Zhang2024EvolutionarySearch.md) | critical study: is the evolutionary search needed? | sections 1-5, Appendices A-B |
| [Sim2025BeyondHype.md](Sim2025BeyondHype.md) | critical study: LLM-evolved bin-packing heuristics vs. classical rules | full text |
| [Gideoni2026SimpleBaselines.md](Gideoni2026SimpleBaselines.md) | critical study: simple baselines vs. code evolution | sections 1-7 |

## Rules

- Write in your own words; at most one verbatim quotation, short, with its page or section.
- Give every result a **location in the source** (Theorem 3.2, p. 14) and every note a **reading status**
  (full / parts / abstract only). Take no precise claim into a manuscript from a paper read only as an abstract.
- Record notation or definitions that differ from ours explicitly; this is the most common source of errors when a result is reused.
- "Difference from our work": one or two English sentences, reusable in a Related work section.
- A novelty claim in a manuscript (*has not been studied*) needs an entry in [searches.md](searches.md) no older than three months before submission.
- Mark unverified facts `TODO(verify)`.

## Adding a paper

1. Entry in `references.bib` following [../bibliography/README.md](../bibliography/README.md).
2. If a PDF is available: `knowledge/sources/papers/<BibKey>.pdf` and its text via `pdftotext -layout -enc UTF-8`.
3. Note `<BibKey>.md` from the template.
4. Update the topic map `knowledge/research/<topic>.md` (where the paper belongs, what it changes).
