# Solver min-formula: how many elements does a description of the down-set need?

Working file of an AI agent; nothing here is a result until an independent referee has read it. Programs: `min-formula/`. Logs: `min-formula/runs/`.
Status: in progress (session interrupted once at about 10:12 on 2026-11-02, resumed 20:06). Labels: proved, tested, conjecture.

## 0. State

### Programs
- `mf_core.py`: class `Measure`: exact least formula in the free grammar by a Pareto dynamic programme on values `(D cap B_P, D cap A_P)`; union and intersection are monotone for domination, so only maximal values per cost are kept. Atoms: `dn x`, `Q - up x`, `S(x) = dn x - [x]`, `T(x) = Q - (up x - [x])`, `EP(x)`, `FR(x, y)`, `ER(x, y)`. Cost = element slots of the tree.
- `gen.py`: hub-free planted instances (class `Abs`), `sa.py`: adversarial annealing, `t_base*.py`, `t_block.py`: first measurements.

### Findings so far
1. **Tested.** All planted bases of `zz_design.py` have a formula with **one or two elements** (one seed per base, 13 bases): `S(a)` for a high `a` of the block `A*`, or `EP(a)`, without strict atoms; `allstrict` needs 2. So these families reach Shapes A, B of the proof but are trivial for the free grammar.
2. **Proved (one line).** For `a in A_P`, the set `S(a) = dn a - [a]` is a down-set that misses `U_P` and contains every `b in B_P` with `b < a`. So `EP` and `S'` can be dropped from `F^1`: this saves six elements of the F-formula at once.
3. Tie-free case: see Section 3 (to be written): `R_0 x C_0` is all strict.
