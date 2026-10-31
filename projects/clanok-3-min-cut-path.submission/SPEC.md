# Article 3: blueprint (coordinator, 2026-10-31)

Author's request: one article with (1) NP-completeness on diameter three only, (2) "diam or cut 2" in P by two proofs:
the squares for `c <= 2` and ZZ + P2 for `d = 2`, `c >= 3`. First complete version in order; it will be improved and
simplified later. Folder of sources: `projects/clanok-2-min-cut-path.submission/open-cases/` ("open-cases").

## 1. Sections of the article

| No. | Title | Draft file (in `projects/clanok-3-min-cut-path.submission/drafts/`) | Written by | Sources |
|---|---|---|---|---|
| 1 | Introduction | `01-intro.tex` | coordinator | article 2 lines 169-269, status.md |
| 2 | Preliminaries | `02-prelim.tex` | W-squares | article 2 `main.tex` lines 270-452; Prop. 18 from lines 1092-1116 |
| 3 | NP-Completeness on Graphs of Diameter Three | `03-diameter-three.tex` | W-hard | open-cases/theory-hardness.md §1, §2; verify/hardness-proof.md |
| 4 | Pairs with Cut-Value at Most Two (the squares) | `04-squares.tex` | W-squares | article 2 `main.tex` lines 453-1047 |
| 5 | From Pairs at Distance Two to a Zigzag Problem | `05-zigzag.tex` | W-zigzag | open-cases/qp-proof.md §1.2-§3 |
| 6 | A Polynomial Algorithm for Pairs at Distance Two | `06-polynomial.tex` | W-zigzag | open-cases/qp-proof.md §4; open-cases/r7-desc.md §2.2, §3; open-cases/verify/rv-r7-desc.md §2.6, §3 |
| 7 | Conclusion, main theorem | `07-conclusion.tex` | coordinator | |

Main theorem (stated in Section 1, proved at the end of Section 6): `\MinCutPath` restricted to graphs of `\DC` is solvable
in polynomial time.

## 2. Rules for every draft

- A draft is plain LaTeX body text (no preamble), `\section{...}` first, compiled later inside `main.tex` of class `sn-jnl`
  (theorem environments `theorem, lemma, proposition, corollary, definition, example, remark`, `proof`; `\cref`; packages
  amsmath, amssymb, mathrsfs, algorithm, algpseudocode, booktabs, graphicx; do not add packages or layout commands).
- Language: American English. **One sentence per source line.** Diacritics as TeX code.
- Style: read `knowledge/writing/academic-style.md` and `knowledge/writing/math-writing.md` once (they are short enough; the
  phrase list `writing/phrase-list.tsv` is not needed). Every sentence carries a definition, a result, a reason or a cited
  fact. No filler, no announcements, no recaps. Avoid semicolons and explanatory colons (the house rule). Run
  `.\scripts\check-text.ps1 -Path <draft>` from PowerShell at the end and resolve or justify each finding.
- **Keep every definition, statement and proof step of the source** (author's rule: revise without compressing, tidy only).
  Rewrite markdown into prose and LaTeX. Do not change mathematics beyond this spec; if you find an error or a gap, keep the
  text, mark it with a LaTeX comment `% TODO(check): ...` that names no tool and no file of this workspace, and report it in
  your final message and in your notes file.
- Comments in the `.tex` must not name this workspace, its paths, Markdown files or AI tools.
- No "Source:" or "Reviewed:" lines, no internal names (`r5-core`, `Theorem 8.2`, `Round 6`, "agent", "referee").
- Labels with prefixes (`sec:`, `def:`, `thm:`, `lem:`, `prop:`, `cor:`, `fig:`, `alg:`, `eq:`, `con:` for constructions), and
  each draft keeps its own label prefix after the colon to avoid clashes: `dt-` in Section 3, `zz-` in Section 5, `pa-` in
  Section 6 (for example `lem:pa-windows`). Section 2 and Section 4 keep the labels of article 2.
- Citations only with keys present in `projects/clanok-3-min-cut-path/references.bib`. Never add an entry.
- Macros available: `\cp`, `\DC`, `\MinCutPath`. New notation macros go in a block at the top of your draft inside a comment
  block starting `% MACROS:`; the integrator moves them to the preamble (use `\newcommand`, no redefinitions).
- Save the draft after every subsection (a stop can come at any time). Own notes:
  `projects/clanok-3-min-cut-path.submission/drafts/notes-<section>.md` (English): what changed, what is unclear.
- Nothing is built by you unless you are told to; a quick syntax sanity by eye is enough. Do not edit `main.tex`, this file,
  the projects `clanok-1`, `clanok-2`, or `open-cases`.
- Read selectively. The usage limit is tight: `sed -n` the exact line ranges; do not read other reports.

## 3. Notation across sections

Common (Section 2): `G = (V, E)`, `n = |V|`, `u`, `v`, `d(u,v)`, `c(u,v)`, `\cp(u,v)`, `\delta(S)`, class `\DC`. In Sections 5 and 6
`m` is the number of switches, as in the sources; say so where it is defined, since `|E|` is written `|E|`.
Section 4 keeps article 2's names (`A`, `B` are vertex sets of cuts; `a_i, b_i, c_i, d_i` terminals of a square).
**Section 6 renames** the objects of a valid path `P` to avoid clashes: minimal E-members `A_P`, maximal F-members `B_P`,
`W_E`, `W_F`, `U_P` for `Up`, `L_P` for `L`; the positions thresholds `L, R, U, V` of the proof become `\ell^*, r^*, u^*, v^*`
(with `\ell(a), r(a), u(b), v(b)` for the functions), the classes `E^*` and `F^*` stay.
Sections 5, 6 use `M` (switches), `\Omega` (nodes), `s, t` (terminals), `D` (down-set, mode vector).

## 4. What each writer must do

### W-hard (Section 3)
Statements to include: the construction of `theory-hardness.md` §2.1, Lemmas 2.2, 2.3, 2.4, Theorem 2.5 and Corollary 2.6 (a), (b),
(c) with the correction E2 of `verify/hardness-proof.md` (wording of (c)) and E1, E3 where they touch the text; (d) on lengths is
left out. NP membership: the certificate is the edge set itself (a set `S` with `|S| <= b` containing a `u`-`v` path and separating
`u` from `v` is checked in polynomial time); use this instead of Corollary 1.4 and Lemma 1.3, which are not in the article. `cp = c`
iff a minimum cut contains a path is `\cref{prop:open-pairs}` of Section 2. Reduction from 3-SAT: cite `Michel2026MinCutPath` only if
needed; 3-SAT is standard (no citation key for Cook or Karp exists, so write "3-SAT" without a citation and report it in the notes).
Say in one sentence why the graph is not in `\DC` (fillers). Look at `projects/clanok-3-min-cut-path/hardness-construction.pdf`: if it is a
drawing of this construction, include it as `\cref{fig:dt-construction}` with a one-line caption; otherwise say so in your notes.

### W-squares (Sections 2 and 4)
Copy from article 2 `main.tex` and edit as little as possible. Section 2: lines 270-452, plus Prop. 18 (`prop:open-pairs`, lines 1092-1116,
statement and proof) moved to the end of §2.1; drop the sentence on the open status there. Section 4 title "Pairs with Cut-Value at Most Two"
with subsections from lines 453-704 (minimum cuts of a pair with cut-value two), 705-844 (separating shortest paths), 845-1047 (a linear-time
algorithm). Remove: Proposition 12 (`prop:lengths`, not used by Theorem 15; check first that nothing cites it and report if something does), and every
reference to Theorem 17 (`thm:hardness`) or Section 6 of article 2, and "the thesis" comparisons that serve only a thesis-to-paper relation, moving none
of it elsewhere (the Introduction will carry one sentence on the thesis). Keep the Examples, figures and Remark 2 for now. Figures keep their files.
Results stay as they are. Keep citations and labels.

### W-zigzag (Sections 5 and 6)
Section 5: `qp-proof.md` §1.2-§1.4 (preorders, ZZ, general switch form), §2 (reduction of the open case to ZZ + P2: Lemmas 2.1-2.4, Definition 2.5,
Lemmas 2.6-2.8, Theorem 2.9) and §3 (Construction 3.1, Lemmas 3.2-3.4), with every repair listed in `qp-proof.md` §8. Definitions from §1.1 that are already in
Section 2 of the article are not repeated (check `\cref{}` names against article 2 lines 270-452: cut-path `def:cut-path`, `lem:basic-bounds`, `lem:minimum-cuts`,
`lem:uncrossing`, `def:class`, `prop:class`, `prop:open-pairs`).
Section 6: `qp-proof.md` §4 up to and including Lemma 4.5, then from `r7-desc.md`: the atoms (terms defined directly, as down-sets of Definition 5.1 without flips, pivots
and anchors only as the atoms need them; do not introduce GDESC or IDESC), Lemma R, Lemmas J and G, Theorem B, Corollary B1. Apply `rv-r7-desc.md`:
the one-line repair of Corollary B1 (§2.6) and **Proposition C with its optional simplification** (§3): Case II and Shapes A', B' are deleted, the proof uses the exits, Shape A and Shape B only, `κ` = the first 10 classes of `R_0` by last position, and the count is at most 71 switches.
Do not include Lemma S, Lemma X, Theorem A, Corollary A1 (Theorem B covers them; Lemma X's chains and conflict list go into the proof of Lemma G, written out in full). Write Orientation with all four sign cases.
End with: **Theorem (open case).** `\cp(u,v) = c(u,v)` is decided in polynomial time for `G \in \DC`, `d(u,v) = 2`, `c(u,v) >= 3`, with the construction of a minimum cut-path; time `n^{71} \cdot n^{O(1)}`, since `m <= n - 2` (`verify/rv-r6-chain.md` §0, L1).
No word about quasi-polynomial time.
Give the algorithm in one paragraph or a short `algorithm` environment: enumerate formulas, test connectivity, lift the mode vector to a minimum cut of `G` (Theorem 2.9 and its proof).
