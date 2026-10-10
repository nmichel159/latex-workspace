# Feige1998Threshold

| | |
|---|---|
| Paper | Feige: *A Threshold of ln n for Approximating Set Cover*. Journal of the ACM 45(4), 1998, 634-652. DOI 10.1145/285055.285059 |
| Key | `Feige1998Threshold` |
| Reading status | parts read 2026-10-10 in the journal PDF (copy on a Duke course page, `courses.cs.duke.edu/spring07/cps296.2/papers/p634-feige.pdf`): abstract, Section 2.1 (pp. 639-641) |
| Full text | - |
| Topic | [../research/min-cut-path.md](../research/min-cut-path.md), section 6 |

## What the paper does

- Set cover cannot be approximated within `(1 - o(1)) ln n` unless NP has slightly superpolynomial algorithms; the
  proof starts from a gap version of 3-SAT with a regular structure (not read beyond Section 2.1).
- Section 2.1, definition of MAX 3SAT-5: a CNF formula with `n` variables and `5n/3` clauses, every clause with
  exactly three literals, every variable in exactly five clauses, no variable twice in a clause ("3CNF-5 formula").
- Theorem 2.1.1 (attributed to Arora et al. 1992 and Papadimitriou and Yannakakis 1991): for some `eps > 0` it is
  NP-hard to distinguish satisfiable 3CNF-B formulas from those in which at most a `(1 - eps)`-fraction of the
  clauses can be satisfied.
- Proposition 2.1.2: the same for 3CNF-5 formulas. The proof is sketched (replace the occurrences of a variable by
  fresh variables on a cycle of equality clauses, pad short clauses, add dummy variables); four properties of the
  reduction are "left to the reader".

## Definitions and notation that differ from ours

| Theirs | Ours | Note |
|---|---|---|
| a variable "appears in exactly five clauses", never twice in one clause | "occurrence" = a literal position; `M[x_i]` lists the occurrences of `x_i` | for 3CNF-5 formulas both counts are five, and `5n = 3m` |
| at most a `(1 - eps)`-fraction of the clauses satisfiable | every truth assignment leaves at least `delta m` clauses unsatisfied | same statement; `eps` is our `delta` |

## What we use from it

| Result | Location in source | Where we use it (project, statement) | Exact assumptions |
|---|---|---|---|
| NP-hardness of distinguishing satisfiable 3CNF-5 formulas from those with at most a `(1 - eps)`-fraction satisfiable | Proposition 2.1.2, p. 640 | article 1, Section 7.1, Theorem `thm:no-ptas` (7.3, no PTAS unless P = NP) | formulas of the 3CNF-5 shape; perfect completeness (the yes-case is "satisfiable"), which the proof of `thm:no-ptas` needs |

## Difference from our work

The paper is used only as the source of the gap problem; it does not study cuts or paths.

## Doubts and open questions

- The proof of Proposition 2.1.2 is a sketch and rests on Theorem 2.1.1, i.e. on the PCP theorem; neither Arora et
  al. nor Papadimitriou and Yannakakis is in our bibliography or was read.
- The value of the constant is not given, so `eps_0 = delta / 200` in Theorem `thm:no-ptas` is not explicit.
