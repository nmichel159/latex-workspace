# Changes in fragment A (front matter, Sections 1-2)

Word count (check-text.ps1): 1061 words, 71 sentences before; 1621 words, 104 sentences after. Build: +44 text lines
in the PDF before Section 3 (about two thirds of a page).

## Language
- Abstract: the sentence defining c(u,v) and d(u,v) now precedes the formula (was after it); "which are secured" added to the motivation sentence.
- Introduction: "max-flow min-cut duality" -> "max-flow min-cut theorem"; "These papers" -> "These works"; first sentence of the classical paragraph split in two.
- Introduction, motivation: long sentence on path and cut split in two; one sentence added on what selecting an edge means ("The selected edges are the links that we secure; a route through one of them is closed to the adversary.").
- Introduction, contributions: c(u,v), d(u,v), cp(u,v) are now explained before the formula; "dense Erdős–Rényi random graphs" -> "with constant edge probability"; "sparser random graphs" -> "edge probabilities p >= alpha log n / n with alpha > 1"; "graphs with minimum cut-value at most two" -> "graphs in which c(x,y) <= 2 for every two distinct vertices" (hypothesis of Theorem 5.1, verbatim meaning).
- Introduction, roadmap: tightened (the two classes named once).
- Section 2 heading "Fundamentals" -> "Preliminaries" (academic-style.md §10); label `sec:fundamentals` unchanged.
- Section 2: "Throughout the paper, we use ... following the conventions of" -> "We use ... and follow the conventions of"; "We often deal with" -> "Most statements concern"; "The value d(u,v) denotes the distance ..., i.e., the length" -> "The distance d(u,v) is the length"; "which are assumed to lie" -> "and we assume that u and v lie"; "For any path" -> "For a path".
- Definition 2.1: colon after "such that" removed; items end with ", and" / "." .
- Definitions 2.2, 2.3: "denoted by ..., is defined as:" -> "is denoted by ...:".
- Before Lemma 2.4: announcement "they are used repeatedly in the subsequent sections" dropped; the rest of the sentence kept.
- Before Definition 2.5: second sentence split in two; "i.e." -> "that is"; "(Section 6)" added after "For random graphs".
- Definition 2.5: "if it meets the following criteria:" -> "if the following three conditions hold."
- Lead-in "The corresponding optimization problem is stated as follows." removed (the problem box title says it).

## Exposition
- Introduction, related work: thin paragraph kept (claims and four citations unchanged) and followed by four short paragraphs on the closest problems: non-disconnecting paths, Shortest Path Most Vital Edges, Network Diversion, Matching Cut, and one sentence comparing the diameter-two behavior with Theorem 4.5.
- Introduction: "The Min Cut-Path problem asks for ..." moved to the end of the first paragraph (it now precedes the related work); the novelty sentence and "We settle ..." follow the related work.
- Introduction, contributions: theorem references added (Theorems 3.6, 3.5, 4.5, 5.1, 6.1, 6.6); "In both classes ... polynomial time" made a sentence of its own.
- Introduction: new paragraph with the idea of the reduction (chain of cycles, threads, synchronization and clause threads, and the one-line reason for the second reduction); it restates the construction of Section 3 and the proof of Theorem 3.6.
- Section 2: one sentence defining "cut separating u and v" / "u-v cut" with the wording of Definition 2.1 (removal disconnects u from v).

## Made explicit
- After Definition 2.3: E is a cut-path when u and v lie in one component, so CP(u,v) is nonempty and the minimum exists.
- Proof of Lemma 2.4: "C ∪ P is a cut-path by Definition 2.1, since it contains the cut C and the path P"; |C ∪ P| <= |C| + |P| - 1 written out; the coincidence of the bounds for c = 1 or d = 1 written out for each case.

## Formatting
- Empty line before \end{abstract} removed; stray double blank lines removed in Sections 1-2.
- One sentence per line throughout the fragment.

## Citations
- New citations in the introduction: Mao2021NonSeparating, Abhinav2022NonSeparating, Bazgan2019MostVital, Bentert2025NetworkDiversion, LeLe2019MatchingCut, Komusiewicz2020MatchingCut (no theorem numbers; Bazgan's numbers are those of the preprint).
- Existing citations kept: GomoryHu1961, NagamochiKameda1996, Mehlhorn2017Certifying, Cormen2022, Diestel2025.

### bib keys to add
All six have a VERIFIED status line in knowledge/bibliography/references.bib:
- Mao2021NonSeparating
- Abhinav2022NonSeparating
- Bazgan2019MostVital
- Bentert2025NetworkDiversion
- LeLe2019MatchingCut
- Komusiewicz2020MatchingCut

### check-text.ps1 findings left (justified)
- l.57 "These works": countable (publications, one of them a textbook); requested by the brief.
- l.63, 67, 77 "\cite ... proved/studied/gave": false positives, the authors are named before \cite.
- l.67, 80 "Vital": part of the problem name Shortest Path Most Vital Edges.
- l.83 "To the best of our knowledge": the single novelty claim, backed by searches.md (2026-10-07, 2026-10-09).
