# Mathematical writing

How to write notation, definitions, theorems, proofs and algorithms. Sentence style:
[academic-style.md](academic-style.md); LaTeX mechanics (environments, `\qedhere`, pseudocode, figures):
[latex-guide.md](latex-guide.md); house rules (macros, labels, problem box): [latex-conventions.md](latex-conventions.md).

## 1. Notation

- **One symbol, one meaning; one object, one symbol**, across the whole document. Resolve a clash by renaming, not by a
  remark *(by abuse of notation)*.
- Introduce a symbol where it is first used; after a long gap, remind the reader in words (*the cut $C$*).
- Replace a symbol used fewer than three times with words.
- A multi-letter operator or a problem name gets a macro (`\cp`, `\diam`, `\MinCutPath`); macros live in
  `preamble/macros.tex` ([latex-conventions.md](latex-conventions.md) §6).
- Bound variables in lemmas must not clash with global ones (if `u, v` are the fixed vertices of the problem, a lemma
  quantifies over `x, y`).
- A value and an object get different symbols (`c(u,v)` is a number; the cut is `C`).

Fixed letters in the author's texts; new texts keep them:

| Letters | Meaning |
|---|---|
| `G, H` | graphs; `V, E` vertex and edge sets; `n = \|V\|`, `m = \|E\|` |
| `u, v` | distinguished vertices of the problem; `x, y, w` other vertices; `e, f` edges |
| `P, Q` | paths; `C` cut; `S, A, B` sets; `F` solution |
| `i, j, k, r, t` | indices and counts; `d` distance; `c` cut size |
| `\alpha, \beta` | model constants; `\varepsilon` small positive constant; `p` edge probability |

Asymptotics and probability:

- With `O`, `\Omega`, `\Theta`, `o`, make clear which variable grows and what is constant (*for fixed $\alpha$, as
  $n \to \infty$*).
- Define *with high probability* once in the Preliminaries (e.g., with probability `1 - o(1)` as `n \to \infty`) and use
  only that term afterwards, not alternately *almost surely*, *a.a.s.*, *w.h.p.*
- State the base of the logarithm once.
- Do not mix the quantifier *for all $n \ge n_0$* with a limit in the same statement.

## 2. Formulas in sentences

- Do not start a sentence with a symbol: *$G$ is connected* → *The graph $G$ is connected*.
- Separate two formulas by a word: *for $i < k$, $x_i = 0$* → *we have $x_i = 0$ for all $i < k$*.
- `\forall`, `\exists`, `\Rightarrow`, `\Leftrightarrow` do not belong in running text; write them as words.
- A displayed formula is part of the sentence and carries its punctuation. Display a formula that is long, important or
  referenced later; number only the ones that are referenced ([latex-guide.md](latex-guide.md) §5).
- House convention: in a definition, *if* means "if and only if"; in a theorem, write the equivalence in full: *if and
  only if*.
- Hyphenate a compound adjective before the noun (*polynomial-time algorithm*, *$k$-connected graph*), not after the
  verb (*runs in polynomial time*). A pair of vertices takes an en dash: `$u$--$v$ path`.
- Numbers up to ten in words when they count things (*two paths*, *diameter two*), digits in formulas and measurements.

## 3. Definitions

- The defined term is emphasized (`\emph`) and defined exactly once.
- All variables of a definition are quantified inside it; hypotheses are not hidden in the text before the environment.
- Use the `definition` environment for notions referenced later; a simple notion can be introduced in a sentence.
- A non-trivial definition is followed by an example; a subtle boundary also by a counterexample.
- One sentence of intuition before a formal definition helps; a paragraph of intuition must not replace it, and
  *Formally:* does not introduce the environment ([academic-style.md](academic-style.md) §9).
- A definition has a name: `\begin{definition}[Cut-path]`.
- No figure or algorithm inside a `definition` environment ([latex-conventions.md](latex-conventions.md) §4).

## 4. Statements

**A theorem can be quoted on its own**: it contains all its hypotheses and introduces all its objects (*Let $G$ be a
connected graph of diameter two and let $u, v$ be distinct vertices. Then ...*).

| Environment | Use |
|---|---|
| Theorem | the main results of the paper (few) |
| Proposition | a smaller result of interest in itself |
| Lemma | a tool for proving a theorem |
| Corollary | an immediate consequence; proof of a few lines at most |
| Claim | a statement inside a proof, not used outside it |
| Observation / Remark | an evident fact that is used later / a remark the logic does not rely on |
| Conjecture | an unproved statement with its stated reason |

The house preamble defines `theorem`, `proposition`, `lemma`, `corollary`, `claim`, `remark` (and `definition`,
`example`): [latex-conventions.md](latex-conventions.md) §4. It defines no `observation` and no `conjecture`.

- Shape: *Let ... . If ..., then ... .* or *For every ..., ... .* The order of quantifiers is unambiguous.
- Constants are explicit, or the statement says what they depend on (*there exist constants $0 < \beta_1 < \beta_2$
  depending only on $\alpha$*).
- Algorithmic theorem: *There is an algorithm that, given ..., computes ... in time $O(\dots)$.*
- A decision problem is *NP-complete*, an optimization problem *NP-hard*; membership in NP is proved or explicitly
  stated.
- A probabilistic theorem names the model, the parameter regime and the sense of probability (*Let $\alpha > 1$ and
  $p \ge \alpha \log n / n$. Then with high probability $G(n,p)$ ...*).
- A quoted theorem says what the source says and is cited with a location: `\cite[Theorem~7.3]{Bollobas2001}`. Check
  the wording in the source, not in secondary literature.
- Do not assert what is neither proved nor cited.
- The hypotheses of a theorem match those of the lemmas it uses (`p = ...` vs. `p \ge ...`, `\alpha > 0` vs.
  `\alpha > 1`).

## 5. Proofs

- **Strategy in one sentence** before a proof longer than half a page (*We reduce from 3-SAT: the chain encodes a truth
  assignment and each thread encodes a clause.*).
- **Structure**: steps or claims with names; cases are named, exhaustive, and the text says why (*Case 1:
  $d(u,v) = 1$.*).
- **Every step has a reason**: *by Lemma 3*, *since $G$ is connected*, *by the choice of $P$*. *Clearly*, *obviously*,
  *trivially*, *it is easy to see* do not replace a reason.
- Prefer a direct proof or contraposition to contradiction. A proof by contradiction states its assumption explicitly
  and ends by saying what it contradicts.
- *Without loss of generality* only with the symmetry that justifies it.
- Induction: say on what, the base case and the induction hypothesis.
- A computation is a chain of aligned relations; a non-standard step is justified right after it.
- Level of detail: a reader from the field verifies every step without paper. In a conference version, routine checks go
  to an appendix.
- A figure supports a proof; it does not replace it.
- A proof starts with a sentence, never with an algorithm, a figure or `\paragraph`; layout rules (`\qedhere`, blank
  lines): [latex-conventions.md](latex-conventions.md) §4.

Fixed outlines:

| Type of proof | Outline |
|---|---|
| Algorithmic theorem | 1. Correctness → 2. Optimality (if claimed) → 3. Running time, step by step |
| NP-completeness | source problem in its exact form → construction (a figure for each gadget) → size and time → direction ⇒ → direction ⇐ → membership in NP |
| Probabilistic bound | event and its probability → inequality used, with citation and exact form → union over how many events → resulting probability |
| Structural theorem | lower bound → upper bound (or construction → optimality) |

## 6. Algorithms

- Pseudocode is for the reader: mathematical notation, no programming-language syntax, the same symbols as the text.
- Header: name, **Input**, **Output**. Number the lines if the text refers to them. Split anything longer than about
  25 lines into procedures.
- The caption (`\caption`) says what the algorithm computes and, if useful, its complexity.
- The text explains the idea and the invariant; it does not retell the pseudocode line by line.
- Mention data structures where the complexity depends on them.
- State the complexity as a theorem with its parameters (`n`, `m`) and the model of computation when it matters.
- Packages and markup: [latex-guide.md](latex-guide.md) §7.

## 7. Figures for constructions

- One figure per construction or gadget; labels in the figure are the symbols of the text.
- The caption says what the reader should see (*A chain link: the two $p$–$q$ paths have equal length.*), not only what
  the figure is.
- Vector graphics (TikZ or PDF) and the document font; formats and tools: [latex-guide.md](latex-guide.md) §8.
- Every figure is mentioned in the text before the place where it appears.
