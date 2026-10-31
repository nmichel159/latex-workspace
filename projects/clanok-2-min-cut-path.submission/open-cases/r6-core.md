# Round 6, agent r6-core: the general core of ZZ + P2

Status: version 0.1 in progress (started 2026-10-22). Scripts: `r6-core/`, logs `r6-core/runs/`. Code of `r5-core/`
and `r4-general/` (and through them earlier folders) is imported read-only after validation (§1).
Labels: **proved**, **checked** (exact computation on named instances), **sketch**, **conjecture**, **refuted**.
Notation of `r5-core.md` (general switch form, `W_E`, `W_F`, `Up = ↑W_E`, `L = ↓W_F`, `A` minimal E-members, `B`
maximal F-members, compatible sides, windows, CDESC, ADESC, TCA) and `r5-classes.md` (Theorem Q, Lemma W, Lemma D).

Target (coordinator, 2026-10-22): for the general core (strict comparabilities between free switches after
propagation, free middle witnesses) either (a) prove TCA(c) for some shortest valid path, or another complete
polynomial algorithm with a complete proof; or (b) build a family on which ADESC, CDESC and HYB all fail with
bounded parameters.

## 0. Results so far

| # | Statement | Status |
|---|---|---|
| | (in progress) | |

## 1. Validation of the imported code

(in progress)

## 2. Plan

1. Extend the minimax argument of Theorem Q (`r5-classes.md` §2b) from classes to the general order. Theorem Q
   needs a *duality*: every pair of a needed side of one type and a needed side of the other type is "dominated" in
   one of the two games. In the general model the duality holds for incomparable pairs (P2) and fails for comparable
   pairs `y < x` with `y ∈ L`, `x ∈ Up`. *Pivots* (protect everything strictly below an element of `Up`, re-adding
   the minimal E-members below it; dually) restore the duality for comparable pairs with a cheap pivot on one side.
2. Study the remaining comparable pairs (both pivots expensive): prove they do not occur on a suitable shortest
   path, or that they can be handled otherwise, or build a family from them (target (b)).
