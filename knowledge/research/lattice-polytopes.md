# Lattice polytopes inside the n-dimensional cube – overview of the bachelor's thesis

Source: *Mrežové mnohosteny v n-rozmernej kocke* (Lattice polytopes inside the n-dimensional cube), bachelor's thesis,
UPJŠ Košice 2024, supervisor Mgr. Martin Vodička, 42 pages, in Slovak. Full text:
`knowledge/sources/bakalarska-praca-2024-mriezkove-mnohosteny.txt`.

English title in the assignment: *Lattice polytopes inside n-dimensional cube*.
Keywords: lattice, lattice basis, convex polytopes, centre-polytope, truncated polyhedron, mixed volume.

## Topic

Volumes of convex polytopes whose vertices lie at vertices of the `n`-dimensional cube: the average volume of a
random polytope, the volume of a convex combination of two polytopes, and extreme (maximum and minimum) volumes.

## Structure and main results

Numbered statements are labeled `Veta` (theorem) and `Definícia` (definition) in the Slovak text; search the `.txt`
for e.g. `Veta 4.2.2`.

| Chapter | Contents | Key statements |
|---|---|---|
| 1 Foundations | lattice polytope, vertex, lattice basis, isomorphism, volume via determinant; gamma function, Stirling's formula, volume of a pyramid and of a ball | Theorem 1.2.7: `V(M) ≤ ∏\|m₀ − mᵢ\| / n!` for a simplex |
| 2 Average volume of a polytope in the cube | centre-polytope `M_{n,k}` (vertices with coordinates 0, 1, 0.5; exactly `k` coordinates equal 0.5) | Theorem 2.1.2: `M_{n,k+1} ⊆ M_{n,k}`; Theorem 2.2.1: if every vertex of the cube is chosen independently with probability `p ∈ (0,1)`, then `E[V(conv A)] → 1` as `n → ∞` |
| 3 Mixed volume and convex combinations | Minkowski sum, mixed volume, truncated polyhedron (pyramid) | Theorem 3.0.4: `c_k² ≥ c_{k−1}·c_{k+1}`; Theorem 3.1.1: the volume of `conv(M, O)` is not bounded above; Theorem 3.2.2: formula for the volume of a truncated polyhedron; Theorem 3.4.1: the minimum volume of `conv(M, N)` between parallel hyperplanes is the volume of a truncated pyramid |
| 4 Extreme volumes in the cube | maximum with `k` vertices, maximum for a simplex (connection to Hadamard's maximal determinant problem), minimum | Theorem 4.1.1: for `k ≥ 2^{n−1}`, `V ≤ 1 − (2ⁿ − k)/n!`; Theorem 4.2.2: `V(M) ≤ √(n+1)^{n+1} · 0.5ⁿ / n!` for a simplex, equality only if `n + 1 = 4k`; Theorem 4.2.3: construction of an extreme simplex in dimension `2n + 1`; Conjecture on the recurrence `D(n, m)` for minimum volumes; Theorem 4.3.3: the average of the minimum volumes `→ 1 + ln(1/2)` |

Note: the formulas in the table were transcribed from the extracted text, where typeset fractions and roots break
apart. Before citing, check the exact wording in the PDF (`knowledge/sources/bakalarska-praca-2024-mriezkove-mnohosteny.pdf`).

## Terminology introduced in the thesis

| SK | EN (abstract) |
|---|---|
| mriežkový mnohosten | lattice polytope |
| Stred-mnohosten | centre-polytope |
| skosený mnohosten / sklonený ihlan | truncated polyhedron |
| zmiešaný objem | mixed volume |
| minimálny rozdielový odhad `D(n, m)` | – |

## References of the thesis

Correct data (verified 2026-10-07 unless stated otherwise); what is wrong in the PDF of the thesis is in the last column.

| # | Source | Wrong in the thesis PDF |
|---|---|---|
| 1 | Haase, Nill, Paffenholz: *Lecture Notes on Lattice Polytopes*, preprint TU Darmstadt, 2020 (unverified) | name order ("A. P. Christian Haase, Benjamin Nill") |
| 2 | Smith, Vamanamurthy: *How Small Is a Unit Ball?*, Mathematics Magazine 62(2), 1989, 101–107 | year 2018, an ISBN is given |
| 3 | Gubner: *The Gamma Function and Stirling's Formula*, notes, 2021 (unverified) | – |
| 4 | Martini, Montejano, Oliveros: *Bodies of Constant Width*, Birkhäuser 2019, ISBN 978-3-030-03866-3 (e-book 978-3-030-03868-7) | name order |
| 5 | Stein: *A Note on the Volume of a Simplex*, The American Mathematical Monthly 73(3), 1966 (pages unverified) | an ISBN is given |
| 6 | Hedayat, Wallis: *Hadamard Matrices and Their Applications*, The Annals of Statistics 6(6), 1978, 1184–1238, DOI 10.1214/aos/1176344370 | name order, an ISBN is given |
| 7 | Weisstein: *Hadamard's Maximum Determinant Problem*, MathWorld (unverified) | – |

Verified entries are in `knowledge/bibliography/references.bib` (section "Convex geometry").

## Relation to other work

Thematically the bachelor's thesis stands alone (convex geometry); it shares only a common toolkit with Min Cut-Path:
probabilistic estimates and limiting behavior as `n → ∞`.
