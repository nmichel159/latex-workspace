# Open case of DC: status after rounds 4 and 5 (coordinator, 2026-10-22)

> **Goal (author, 2026-10-28): the only question is whether the class "diam or cut 2" (DC) is in P**, i.e. whether
> the open case (`d(u,v) = 2`, `c(u,v) >= 3`) has a polynomial algorithm. Everything else (the quasi-polynomial
> write-up, hardness attempts, subclasses, side reviews and records) is of no interest unless it serves that question.

Question of the author: is deciding `cp(u,v) = c(u,v)` for pairs with `d(u,v) = 2`, `c(u,v) >= 3` in graphs of DC
(every pair has `d <= 2` or `c <= 2`) polynomial or NP-complete? Every other pair of DC is solved (article 2).
All work below is by AI agents; "reviewed" means an independent agent re-derived the proof and re-computed with own
code. Nothing of it is in the manuscript, and the author has read none of it.

All agents and all background runs were stopped on 2026-10-22 at the author's request (credits).

## 1. Where it stands

Chain of the intended proof: open case of DC ⇔ ZZ + P2 → forced-mode propagation → (a) switch model, (b) switch
model with classes, (c) the general core.

| Step | Statement | Status | File |
|---|---|---|---|
| 0 | Open case of DC is polynomially equivalent to ZZ + P2 (both directions) | proved, reviewed | `theory-dc.md` Thm 13, `verify/equivalence.md` |
| a | **2CH + P2 (switch model) is in P** (`O(D^122)` as written, `O(D^74)` with the referee's remark) | proved, reviewed: holds, no repair | `r4-switch.md` Thm 10, `verify/r4-switch-review.md` |
| R | **Theorem R**: after sound forced-mode propagation, if the free switches are pairwise incomparable, the instance contracts to 2CH + P2; with only ties among the free switches it contracts to 2CH with classes + P2 | proved, reviewed: holds (two wording repairs) | `r4-general.md` §8, §9.1, `verify/r5-review.md` §3.4 |
| b | **2CH with classes + P2 in time `m^{O(log m)}`** (quasi-polynomial; not NP-hard unless NP ⊆ QP) | proved; review: line-by-line reading complete, holds; its computations were stopped before finishing | `r5-classes.md` Thm Q, `verify/rv-classes-q.md` |
| a' | 2CH + P2 in time `O(D^36)` by one certificate type (`DESC(6, 12, 18)`) | proved, reviewed: holds | `r5-classes.md` Cor. 2a.2, `verify/rv-classes-q.md` §2.4 |
| c | General core: strict comparabilities between switches (middle witnesses cost nothing by Lemmas 6.3, 6.4) | **open** | `r5-core.md` §6, `r4-general.md` §9 |
| c0 | **Theorem 6.5**: Theorem Q extends to general ZZ + P2 up to the *bad pairs* (`y < x`, `x ∈ Up` not a minimal E-member, `y ∈ L` not a maximal F-member, of a shortest valid path): time `m^{O(κ + log m)}` with `κ` a vertex cover of the bad pairs; `κ = 0` is Theorem Q | proved; review 2026-10-27: Lemmas 6.2-6.4 and Theorem 6.5 hold (Lemma 6.3 even with 5 positions), Cor. 6.5' holds with repair of its proof; computations of the review stopped before finishing | `r5-core.md` §6.4, `verify/rv-core-65.md` |
| **QP** | **Theorem 8.2, Corollary 8.3: ZZ + P2, hence the open case of DC, is decidable in time `m^{O(log² m)}` = `2^{O(log³ n)}`; so it is not NP-complete unless NP ⊆ QP.** Intersections of at most `k = ⌊log2 m⌋ + 1` GDESC terms (pivots `↓x − [x]` cover the bad pairs; their damage is halved per level; heavy rows by `O(log² m)` E-anchors). Chain: Thm 13 → general switch form → Lemmas 6.2-6.4 → Thm 8.2 (no Theorem R, Q, 6.5 needed) | proved, checked; **reviewed twice, holds** (2026-10-27): proof review `verify/rv-r6-core.md` (all items hold, two wording repairs: `m = 1`, sequence count of the time bound; all 1.5 M ZZ instances with 4 middle elements, ~3100 adversarial designs); chain review `verify/rv-r6-chain.md` (Thm 13(a) → switch form → Thm 8.2 holds; wording repairs: `s = t`, "if ETH holds, not NP-hard"; IDESC = graph brute force on all 121 588 open-case pairs of graphs with ≤ 8 vertices, 0 mismatches) | `r5-core.md` §8.2-§8.5 |
| M, T | Member stars (Prop. M, variant of TCA) and the zone theorem: bad pairs matter only on paths where TCA fails, and then the path has long stretches without minimal E-members; family `BP_n` (`K_{n,n}` of bad pairs) is accepted by one GDESC term | proved, checked; not reviewed | `r5-hard.md` §2-§3 |
| c1 | HYB (propagation + side-set search) is sound but incomplete: families `Y^d_k`, `Y'^d_k` | proved, reviewed: holds (repair of the wording of (iii)) | `r5-core.md` §2, `verify/rv-core.md` §2 |
| c2 | ADESC sound; §5.2 (E2)/(F2) **false as written** (counterexample), repaired with uncontracted centres; "TCA ⇒ ADESC" holds in 2CH, has a gap in general unless ADESC enumerates the repaired centres; 5.2' holds with repair; CDESC, Lemma G, CF hold | reviewed | `r5-core.md` §3, §5, `verify/rv-core.md` |
| H | No NP-hardness proof. Series class encodings are never faithful (O1); with P2 weakened to distance 3 the problem is NP-complete (T3, graph form = class "`d <= 3` or `c <= 2`", known before) | proved, reviewed | `r4-hard.md`, `verify/r5-review.md` §2, §6 |
| S | Search: PC decides ZZ + P2 for `q <= 7` (exhaustive); smallest instances defeating level-2 methods: `q = 10`; instance files in `r4-search/instances/` | checked | `r4-search.md` (report of 2026-10-17; later runs not written up) |

Also proved earlier (rounds 1-3): FPT in `c`; XP in the width; Theorems F, F+, Fω, T, H, L, GC; AC and PC are not
decision procedures (`dc-algorithm.md`, `dc-hardness.md`, `dc-general.md`, `verify/round3.md`).

## 2. What remains (in order)

0. **(2026-10-27) Review Lemma 8.1, Theorem 8.2, Corollary 8.3 of `r5-core.md` §8** by an independent agent: if
   they hold, item 2 below is settled in the quasi-polynomial sense and the hardness side is closed (NP ⊆ QP).
   Then finish the computations of `verify/rv-core-65.md` §3 and `verify/rv-classes-q.md` §3.
1. ~~Review Theorem 6.5~~ (done 2026-10-27, holds); finish the computations of `verify/rv-classes-q.md` (§3 empty).
2. **Bad pairs** (the real gap): bound the vertex cover of the bad pairs of some shortest valid path (this gives
   quasi-polynomial time for the whole open case, so not NP-complete unless NP ⊆ QP), or handle them by other tools,
   or find a family where they defeat every description; an NP-hardness proof must live in them.
3. **Classes and the polynomial side**: lower `m^{O(log m)}` to a polynomial bound (TCA of `r5-core.md` §5.3 with the
   repair of `verify/rv-core.md`).
4. **Assemble** the chain of Section 1 into one proof with one numbering, and referee it as a whole.
5. **Write-up**: a separate article (estimate 35-50 pages in `sn-jnl`) or new sections of article 2 (24 pages now).

## 3. Stopped on 2026-10-22 (to relaunch if needed)

Agents: r4-general, r4-classes (continuation of r4-switch), r4-search (session "Trieda z materiálov: polynomiálna
alebo NP-úplna"); r5-classes, r5-core, r5-hard (round 5) had their runs stopped as well. Their reports end where they
stopped; `r4-classes.md` and `r5-hard.md` contain no results yet.

Background runs killed (partial outputs may exist; relaunch from the folder named):
- `r5-core/`: `python hunt_tca.py 12 6 14 3000 sw 5`; `python hunt_tca.py 14 6 14 3000 gen 5`
- `r4-search/`: `python anneal_core.py instances/hybshr-core-hunt-9-8-14-0-s1.json S 30000 instances/anneal-core-A-sS.json`
  for `S = 1, 2, 3`; the same with `instances/hybshr-core-hunt-3-10-16-1-s1.json`, `S = 4, 5`, output
  `anneal-core-B-sS.json`; `python anneal_core.py rand:10 S 30000 instances/anneal-core-R-sS.json` for `S = 6, 7, 8`;
  `python anneal_core.py ZB2 9 30000 instances/anneal-core-ZB-s9.json`;
  `python enum_yes.py 10 --m 8 --range 9240 9937 --tag -m8-11b`

**Resumed 2026-10-22, evening** (workflow run `wf_18fb670d-ae3`, three agents at a time): review of Theorem Q
(`verify/rv-classes-q.md`), review of `r5-core.md` §1-§5 (`verify/rv-core.md`), and `r5-core` extending the minimax
argument of Theorem Q to general ZZ + P2 (new sections §6 onward); then reviews of the new results, `r5-classes`
towards a polynomial bound, and `r5-summary.md`. Stopped by the author the same evening, about 20:40, after the
first phase: `verify/rv-core.md` complete, `verify/rv-classes-q.md` reading complete (computations not), `r5-core.md`
§6 in progress; no follow-up phase, no `r5-summary.md`; no Python process left.

**Resumed 2026-10-23** (workflow run `wf_d0b705b5-1f0`, three agents at a time): review of `r5-core.md` §6
(`verify/rv-core-65.md`); `r5-core` on the bad pairs (§7 corrections, §8 onward); `r5-hard` on the bad pairs from the
hardness side; then reviews of the new results, the computations of `verify/rv-classes-q.md` §3, and `r5-summary.md`.

**Resumed 2026-10-27** (workflow run `wf_138deda4-8fb`, three agents at a time): `rv-core-65` finishes the review of
Theorem 6.5, then `rv-classes-q` does the computations of its §3; `r5-core` on the bad pairs (`r5-core.md` §8);
`r5-hard` on hardness from the bad pairs; every result newly labelled proved goes to a reviewer (`verify/rv-r6-*.md`).
Stopped by the author 2026-10-27 about 10:55, during the first phase (no reviewer of §8 started, no `rv-r6-*.md`);
the 17 Python processes of the agents were stopped by PID. Results: Theorem 8.2 / Corollary 8.3 (row QP of §1,
not reviewed); review of §6 (row c0); `r5-hard.md` Prop. M, Theorem T, family `BP_n` (row M, T).

**Resumed 2026-10-27, round 6b** (workflow run `wf_2175b7d0-315`, at most three agents at a time): two independent
reviews of `r5-core.md` §8, one of the proof (`verify/rv-r6-core.md`), one of the chain from graphs end to end
(`verify/rv-r6-chain.md`); computations of `verify/rv-core-65.md` §3 and `verify/rv-classes-q.md` §3; then, if both
reviews hold, `qp-proof.md` (one self-contained proof) and a referee of it (`verify/rv-qp-referee.md`), otherwise a
repair (`r5-core.md` §8.6) and a referee of the repair.
Stopped by the author the same day about 17:08, a few minutes after the start: `verify/rv-r6-core.md` and
`verify/rv-r6-chain.md` hold only skeletons (no verdict), `verify/rv-core-65.md` §3 relaunched its runs but has no
new outcome; the 7 remaining Python processes were stopped by PID. Resume with round 6b as described above.
Relaunched 2026-10-27 evening, same script, workflow run `wf_52e05843-f7f`. All four agents stopped about 19:20 by the
session limit, after writing: `verify/rv-r6-core.md` final (holds), `verify/rv-r6-chain.md` with every verdict filled
(holds; status line not finalised), `verify/rv-core-65.md` §3 runs finished (adversarial runs `*-rerun2`: no failure,
empty `.err`; not yet written into the report), `verify/rv-classes-q.md` §3 runs started, not recorded.

**Round 6c, 2026-10-28**: finalise the records of the three review reports; assemble `qp-proof.md` (one
self-contained proof of the quasi-polynomial bound) and referee it (`verify/rv-qp-referee.md`); two agents at a time.
Outcome: records finalised (`verify/rv-core-65.md`, `verify/rv-r6-chain.md`, `verify/rv-classes-q.md` §3);
`qp-proof.md` assembled (809 lines, no gap found while assembling); the referee was **stopped by the coordinator at
11:30** after the author set the goal above (the QP write-up is not needed for the question of P); its report holds
only a skeleton.

**Round 7, 2026-10-28: polynomiality.** Conjecture C1: every yes-instance of ZZ + P2 has a connecting down-set given
by a *single* GDESC term with `O(1)` tools, anchors and flips (on every instance computed so far, one term with at most
two tools sufficed: `r5-core.md` §8.4, `r5-hard.md` §3.1, `verify/rv-r6-core.md` §3). C1 gives a polynomial algorithm.
Three agents: `r7-desc` (prove C1 through descriptions), `r7-cert` (a polynomial algorithm by certificates, generalising
`r4-switch.md` Theorem 10), `r7-lb` (search for instances that need many tools in one term); reviews of new proofs in
`verify/rv-r7-*.md`.
First run (`wf_b5c57047-a52`, 2026-10-28 11:30) ended with the session after writing only skeletons; relaunched
2026-10-29 10:10 with the same script; stopped by the usage limit about 10:40 (r7-lb wrote definitions and scripts
and started the annealing runs `r7-lb/runs/sa/sa21-26`, the others only skeletons). Third launch 2026-10-29 11:25
(`wf_963552cb-874`): only `r7-desc` (Opus) and `r7-lb` (Sonnet), with instructions to read selectively; `r7-cert`
postponed. **Stopped by the author 2026-10-29 11:29**, a few minutes after the third launch; no Python process left.

State of round 7 at the stop (nothing reviewed, nothing proved):
- `r7-desc.md`, `r7-cert.md`: skeletons only.
- `r7-lb.md`: §1 definitions (single GDESC term with arbitrary flips, cost = tools + anchors + flips, profile by
  number of tools); scripts `r7-lb/lbcore.py` (exact minimum single-term cost), `enum_lb.py`, `design.py`, `sa_lb.py`,
  `zone.py` (started at the stop), `test_lb.py`, `scan_files.py`; logs `runs/scan-saved.txt` (saved instance files),
  `runs/test-lb-*.txt`, `runs/enum/`, `runs/sa-old/`. Not written into the report: the six simulated-annealing runs
  `sa_lb.py 21..26` (rigid words `EFEFEFEFEF`, `EEEEEFFFFF`, `EEEEEEFFFFFF`, `EFEFEFEF`, `EEFFEEFFEEFF`, `FFEEFFEE`,
  50 min each, 60 000-100 000 steps, logs `runs/sa/sa2*.log`) all ended with **best single-term cost 1 or 2**, every
  best instance solved by a term with **no tool and one or two anchors** (verified). So the adversarial search found
  no yes-instance needing more than cost 2 in one term: evidence for Conjecture C1, not a proof.

**How to resume round 7:** relaunch `r7-desc` (the proof of C1, the only thing that answers the question) first and
alone or with `r7-lb`; read selectively (the usage limit stops agents within about 30 minutes when they read whole
reports); `r7-lb` should first write the sa21-26 outcomes above into its report. That session ended about 10:40; the six annealing runs of `r7-lb`
(`sa_lb.py 21..26`, started 10:36) kept running. Relaunched 2026-10-29 about 11:00 from the session "Trieda z
materiálov: polynomiálna alebo NP-úplna": the same three agents continue their own reports.
Relaunched 2026-10-31 10:55 from the same session: `r7-desc` (Opus, resumed) and `r7-lb` (Sonnet, new agent, first
records sa21-26), both told to read selectively; `r7-cert` postponed.

**2026-10-31: claimed answer to the question.** `r7-desc.md` §2-§3, Theorem B and Corollary B1: every yes-instance of
ZZ + P2 has a connecting down-set given by one of four monotone formulas of bounded atoms built from at most 91
switches, so **ZZ + P2, hence the open case of DC, is in P** (time `m^91 · poly`). Literal C1 (one term) stays open and
is not needed. Status: proved by `r7-desc`; read line by line by the coordinator (no gap found); **independent referee
running, `verify/rv-r7-desc.md`; not a result until it holds**. Computations of `r7-desc` reached Stage 0 and Stage 1
Case I only; Shapes B, A', B' and Case II are untested (the referee was asked to build instances for them).
`r7-lb` stopped on 2026-10-31 (C1 is no longer needed): its report records the annealing runs and cost-3/cost-4
instances (`r7-lb/inst/`, `r7-lb/runs/adv/`), used as test instances by the referee; its three last runs were stopped
by PID. `r7-cert` not needed unless the referee finds a gap.

**Stopped by the author 2026-10-31 (usage limit)**: the referee of Theorem B was stopped after its first pass; no agent
and no Python process left. Saved in `verify/rv-r7-desc.md`: hand derivation, first pass, no gap in Lemmas S, R, X, J, G,
Theorem A, Stage 0, Orientation, (★), Case I; "Case II is vacuous apart from a trivial exit" (stated, not written out).
Not done: the written verdicts, Shapes B, A', B', the computations. **Resume: relaunch only this referee**, one agent,
same task (`verify/rv-r7-desc.md` holds its findings and `verify/rv-r7-desc/` its scripts); nothing else is needed for
the question whether DC is in P.

**Resumed 2026-10-31 14:00**: the referee alone. Author's plan after the reviews: keep the notes current, write the
whole article in order, then improve it and look for simpler proofs.

**Referee finished 2026-10-31: Theorem B and Corollary B1 hold** (`verify/rv-r7-desc.md`): every step re-derived, no gap,
no counterexample; own code, 44 logs end with `FAILURES: none`; Stages reached on planted designs: Shape A 3,478 runs,
Shape B 614; 17.1 M... see its §4. One-line repair of Cor. B1: also enumerate the exit formulas `⋂_{a∈S}(M−↑a)`,
`⋃_{b∈S}↓b`, `|S| <= 9`. Simplification (Proposition C, §3): Case II is vacuous after Orientation, so Shapes A', B' can be
deleted (81 switches suffice; 71 after deleting them, per the report). The chain from graphs (Theorem 2.9, Construction
3.1, Lemma 3.3 of `qp-proof.md`) was reviewed separately: `verify/rv-r6-chain.md`, holds. **So the open case of DC is in P,
as reviewed by AI agents; the author has not read it; the assembled text has not been refereed as a whole.**

**Article plan (author, 2026-10-31): one article in two parts.** (1) NP-completeness, for now only diameter 3:
`theory-hardness.md` Thm 2.5, Cor. 2.6 (`cp = c` and Min Cut-Path on diameter 3, with `d(u,v) = 2`); article 2 Thm 17 is
left out for now. (2) "Diam or cut 2" is in P, by two proofs: pairs with `c <= 2` through the squares (article 2, Thm 9,
11, 15, the author's result) and pairs with `d = 2`, `c >= 3` through ZZ + P2 (`qp-proof.md` §1-§4 for the reduction,
`r7-desc.md` Theorem B).
Written 2026-10-31 as project `clanok-3-min-cut-path` (44 pages, exponent 71 after Proposition C; notes in
`projects/clanok-3-min-cut-path.md`); referee of the assembled text: `projects/clanok-3-min-cut-path.submission/review/referee-article.md`.
Article 2 is not changed. Next: apply the referee's findings; then improve the article and look for simpler proofs.

## 4. How to resume

Read this file, then `r5-brief.md` (targets A, B, C of round 5) and the reports named above. Run at most two or three
Opus agents at a time: four in parallel exhausted the session limit repeatedly (2026-10-16 to 2026-10-22). Every new
proof goes to an independent reviewer before it is reported as a result.

## Article 3, state at the last stop (2026-10-31)

Second version of `projects/clanok-3-min-cut-path/main.tex`, 37 pages: Sections 5 and 6 rewritten directly on the preorder, time `O(n^30)`.
Referee of the rewrite: `projects/clanok-3-min-cut-path.submission/review/referee-direct.md`, holds. Details and next steps: `projects/clanok-3-min-cut-path.md`.
