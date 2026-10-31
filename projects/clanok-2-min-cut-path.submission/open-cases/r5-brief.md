# Round 5 on the open case of DC: brief (coordinator, 2026-10-19)

Question of the author (2026-10-19): settle whether the open case of the class DC is polynomial or NP-complete.
Open case: `G ∈ DC` (every pair has `d <= 2` or `c <= 2`), `d(u,v) = 2`, `c(u,v) >= 3`; `cp(u,v) ∈ {c, c+1}` and
`cp = c` iff some minimum `u`-`v` cut contains a `u`-`v` path. Membership in NP is known (a minimum cut containing a
path is checked by one closure computation, `theory-dc.md` Lemma 6); the question is P versus NP-complete.
Labels in every report: **proved**, **checked** (exact computation on named instances), **sketch**, **conjecture**,
**refuted**; verifiers use **holds**, **holds with repair**, **gap**, **false**.

## 1. Where round 4 ended (read `r4-brief.md` §1 for the models)

The open case is polynomially equivalent to **ZZ + P2** (`theory-dc.md` Theorem 13, re-verified in
`verify/equivalence.md`); every ZZ + P2 instance is realised by a graph of DC, so a hardness proof may build posets
freely. General switch form (`r4-general.md` §5.1): switches = middle elements with sides `E_w` (nodes of lower
neighbours) and `F_w` (nodes of upper neighbours); the modes form a down-set of the preorder (F-mode = in `D`); a
middle-middle edge `y x` (`y < x`) is a private node of `F_y ∩ E_x`; a *conflict pair* is `{E_w, F_z}` with `w <= z`;
yes-instance iff a walk of sides from `s` to `t` contains no conflict pair. P2 is required only between incomparable
switches and may be met by a common node or by a middle witness (a *conditional connector*).

| Result | Status | File |
|---|---|---|
| **2CH + P2 (switches pairwise incomparable, no ties) is in P**, `O(D^{122})` (side-set certificates, Theorem 10) | proved; adversarially reviewed: holds | `r4-switch.md`, `verify/r4-switch-review.md` |
| **Theorem R**: after a sound fixing (forced-exit propagation), if the free switches are pairwise incomparable and every pair of free switches has a common node or a fixed middle witness, contracting the fixed sides gives an equivalent 2CH + P2 instance | proved, **not yet reviewed** | `r4-general.md` §8 |
| With only ties among the free switches, the contraction is an instance of **2CH with classes + P2** (classes forced into one mode, P2 only between switches of different classes) | proved, not reviewed | `r4-general.md` §9.1 |
| Theorem 5' (side-set search with conflict families and declarations, sound), HYB (propagation + search, sound, polynomial for fixed parameters), Lemma Sub, Lemma Mon, Example MW2, families `X_L`, `Y_k`, `Y'_k`, `Z_k`, `Z^B_k` | proved / checked, not reviewed | `r4-general.md` |
| HYB with parameters `(1, 0, 1, 3)` solves every known yes-instance (196 family instances, all core instances of random runs, adversarial hill climbing); 176 of the 196 are rigid (propagation fixes every switch) | checked | `r4-general.md` §7.3, §8 |
| **T3**: with P2 weakened to one-sided witnesses (distance `<= 3`), ZZ is NP-complete; graph form: `cp = c` is NP-complete on graphs in which every pair has `d <= 3` or `c <= 2`, even with `d(u,v) = 2`, `c(u,v) >= 3` | proved, **not yet reviewed** | `r4-hard.md` §6 |
| O1 counting obstruction (series class encodings with node witnesses are never assignment-faithful), hub lemma L4, liveness form L1, link lemma L2 | proved, not reviewed | `r4-hard.md` §1-§4 |
| Earlier: FPT in `c`, XP in the width, Theorems F, F+, Fω, T, H, L, GC; PC/AC refuted as decision procedures | proved, reviewed | `dc-algorithm.md`, `dc-hardness.md`, `dc-general.md`, `verify/round3.md` |

So **every NP-hardness proof must keep, after propagation, either strictly comparable free switches, or ties among
free switches (classes), or free middle witnesses**; and every polynomial algorithm must handle exactly these.

## 2. Targets of round 5

- **A. 2CH with classes + P2** (ties only; the middle classes form an antichain). Decide it: polynomial algorithm with
  a complete proof, or NP-hardness. Hardness here gives hardness of the open case; polynomiality here plus Theorem R
  covers every instance whose propagation kills the strict relations between free switches.
- **B. The general core**: strict comparabilities between free switches and free middle witnesses. A polynomial
  algorithm with a complete proof (for example a version of r4-switch's Theorem 8 for conflict families after
  propagation, a proof that HYB with bounded parameters is complete, or a reduction of the general case to target A),
  or a hardness proof.
- **C. NP-hardness of ZZ + P2** by a construction that uses what the switch model lacks and survives the known
  algorithms (non-rigid, comparable free switches or classes after propagation, not a series class encoding with node
  witnesses, Corollary 4.2 of `r4-hard.md`); T3 shows that distance 3 suffices, the gap is distance 3 to 2.
- **D. Adversarial review** of what round 4 left unreviewed: `r4-hard.md` T3 first (a hardness theorem the article may
  cite), then `r4-general.md` Theorem R, Theorem 5', HYB soundness, Lemmas Sub and Mon, MW2, then the families and O1.

## 3. Observations of the coordinator for targets A and B (unchecked; prove or refute before you rely on them)

Setting of A. Nodes, terminals `s != t`, switches partitioned into classes; a mode vector gives every class E or F;
picked sides `E_w` or `F_w` by the mode of the class of `w`; yes iff `s`, `t` are connected in the hypergraph of the
picked sides. A *valid path* `X_1 .. X_r`: `s ∈ X_1`, `t ∈ X_r`, `X_i ∩ X_{i+1} != ∅`, distinct switches, no two sides
of switches of one class with different types. A shortest sequence of picked sides is a valid path and conversely.

- (A1) F1 of r4-switch holds: `X_a ∩ X_b = ∅` for `|a - b| >= 2`.
- (A2) Same type, different classes, `|a - b| >= 2`: the partners `X'_a`, `X'_b` meet (P2 and A1). Opposite types,
  `|a - b| >= 2`: `X'_a ∩ X_b != ∅` or `X_a ∩ X'_b != ∅`. Positions of one class have one type; P2 says nothing about
  them.
- (A3) *Span lemma.* Let class `C` occupy the positions `a_1 < .. < a_k` of a shortest valid path `P`, with type `T`,
  and let `Z` be any side of type `O` of any switch of `C`. If `Z` meets `X_d` and `X_c` with `d < c` and all positions
  of `C` lie in `(d, c)`, then `X_1 .. X_d Z X_c .. X_r` is a valid path, so `c - d <= 2`. For `k >= 2` the contacts of
  `Z` therefore lie on one side of the class span (or inside it). This replaces Lemma 1 of r4-switch, which fails for
  classes with several positions.
- (A4) *Unused same-type sides.* A side `Z` of type `T` of a switch of a class used with type `T`, not on `P`, meets at
  most three consecutive positions of `P` (shortcut through `Z`). With P2 between its switch and a member `b` of
  another class this gives dominations: for a `T`-member `b` outside that window, `Z' ∩ X'_b != ∅`.
- (A5) The search of r4-switch Theorem 5 stays sound when the partner of a member is replaced by the family of all
  opposite-type sides of its class and "stored side" by "stored (class, type)". If the walk uses at most `k` classes,
  guessing their modes is `n^k`; hard instances use many classes, some possibly with many positions.

Setting of B. For a valid path `P` with E-members `W_E` and F-members `W_F`, every solution through `P` puts `↑W_E` into
E-mode and `↓W_F` into F-mode; validity is `↑W_E ∩ ↓W_F = ∅`.
- (B1) A side `E_{w'}` with `w' ∈ ↑W_E`, not on `P`, can shortcut `P`; but the shortcut is valid only if the member
  that forces `w'` is kept or no kept F-member lies above `w'`. State the right window lemma.
- (B2) P2 between such a `w'` and an incomparable member `b` gives `F_{w'} ∈ N_F[X'_b]` (E-member `b`) whenever
  `E_{w'} ∩ X_b = ∅`, so conflict families are dominated by partner neighbourhoods; the families `Y_k`, `Y'_k` show
  that the storage of such a neighbourhood is the obstacle, and propagation removes them because they are rigid.
- (B3) The yes-question is "path avoiding forbidden pairs" in the side graph, with forbidden pairs given by the order
  (`{E_w, F_z}`, `w <= z`) and with P2 forcing intersections between incomparable switches. Literature on PAFP:
  `literature.md` L5-L8 (polynomial for hierarchical, NP-complete for halving structure, both on DAGs only).

## 3a. Round-5 results so far (first run of 2026-10-19, stopped by a usage limit; restarted 2026-10-21)

- `verify/r5-review.md` (complete): **T3 holds** as written (ten realised graphs, own max-flow). Theorem R (a)-(c),
  Corollary R', the ties version of §9.1, Theorem 5', the conversion, forced-exit propagation, HYB soundness, Lemmas
  Sub and Mon, MW2, Propositions X (i)-(iii), Y', Theorem Y (i)-(iii), r4-hard L1, L2, Prop. 2.4, Lemmas 4.1, 4.3,
  Corollary 4.2 hold. Repairs of wording: propagation stops once the component contains the other terminal; a fixing
  gives each switch at most one mode. **Strengthening: the exception of Theorem R (b) is vacuous** (a middle witness
  of two free switches is comparable with both, so it is never free); hence the contracted instance always satisfies
  P2 and "free middle witnesses" is not a separate case of the core.
- `r5-core.md` version 0.1 (partial, not reviewed): **HYB is incomplete**. The families `Y^d_k`, `Y'^d_k` (`Y_k`,
  `Y'_k` plus one switch `d` incomparable with everything, offering a second, useless exit at `s`) satisfy P2, have
  exactly two solutions, propagation fixes at most one switch, and HYB with any fixed parameters rejects them for
  large `k` (Proposition D). Propagation by forced exits is the weak point; the mates stay free and comparable.
- `r5-classes/` holds scripts of the first run (`ccore.py`, `cdecide.py`, `cfam.py`, `branchfam.py`, `cdesc.py`) but
  no report; `r5-hard` left nothing.

- Second run (2026-10-21) stopped by the author after about 40 minutes; the partial reports are the state to continue
  from: `r5-core.md` 0.2 (adds CF: closure-based mode descriptions CDESC, sound, solve `Y_k`, `Y'_k`, `Y^d_k`,
  `Y'^d_k`, `X_L`, `Z_k`, `Z^B_k` with one centre and at most one flip; Lemma G), `r5-classes.md` 0.1 (skeleton and
  script list), `r5-hard.md` (skeleton). None reviewed.

So after the first run the core is: **strictly comparable free switches, or ties among free switches**, after any
sound fixing; and a correct algorithm must detect rigidity that local forced exits miss (or avoid needing it).

## 4. Rules for the agents of this round

- Read this brief, then the reports named for your target; `verify/*.md` record what was re-checked.
- Write only your own report `open-cases/r5-<name>.md` and your own script folder `open-cases/r5-<name>/`. Save the
  report as you go: a partial report must survive an interruption (usage limits stop agents without warning; the
  first run lost every result that was not in a report). Write the report skeleton at once and update it after every
  result, at least every 20 minutes of work. If your report or folder already exists, continue from it. Import other folders' code read-only.
- Files in English. No edit of the manuscript, the project notes or other agents' files. No git commit.
- Write Python scripts with the file-writing tool, not with shell heredocs (heredocs halve backslashes here). Stop a
  process only by its PID, never by image name. Run long computations in the background with a log file.
- Python 3.13 and numpy are available; installing packages needs the author's consent, so do not install anything.
- Every claim labelled; every computation recorded with script, seed, size and outcome; a claimed proof must be
  complete enough for an independent check, every case written out. A claim of the final answer (P or NP-complete)
  must state exactly which problem it is about and how it implies the answer for the open case of DC.
