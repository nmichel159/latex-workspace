# Round 6, agent r6-review: adversarial review of r5-classes.md (Theorem Q) and r5-core.md (Proposition D, CDESC, Lemma G, CF, ADESC, Theorem 5.2)

Status: partial, in progress (2026-10-22). Reviewer: agent r6-review. Scripts and logs: `verify/r6-review/` and
`verify/r6-review/runs/`. All code is written from the definitions in the reports; code of `r5-classes/`, `r5-core/`
is imported only in the separate final cross-check (§6). Labels: **holds**, **holds with repair**, **gap**, **false**,
**not checked**.

**Overall verdict (provisional).** Theorem Q of r5-classes (2CH with classes + P2 in time `m^{O(log m)}`, hence not
NP-hard unless NP ⊆ QP) holds as written, together with A1-A5, Lemma 2a.1, Corollary 2a.2, Lemma W, Lemma D and Lemma
PP. In r5-core, Proposition D, the soundness of CDESC and ADESC, Lemma G, Proposition CF and Proposition 5.2' hold;
**Theorem 5.2 (E2)/(F2) is false as stated**: the flip set `Φ = f*_A(b_1) ∪ f*_A(b_2)` misses minimal E-members whose
sides meet the centre only through the contraction (counterexamples CE2, CE3, CE4, `runs/ce-e2.json`); it holds with a
repair (§3.6), and the consequence "TCA(c) ⇒ ADESC(5, 2, c) accepts" holds for the repaired centre definition.

## 1. Verdicts

| # | Statement | Verdict | Notes |
|---|---|---|---|
| C1 | r5-classes A1-A5 (§2), Key Lemma K | holds | §2.1 |
| C2 | §2a: `σ_U`, `σ_U^Φ`, Lemma 2a.1, DESC soundness and time | holds | §2.2 |
| C3 | Corollary 2a.2 (DESC(6, 12, 18) decides 2CH + P2) | holds | §2.2; rests on r4-switch Thm 8, Lemma 7 and the reviewed remark |
| C4 | Lemma W | holds | §2.3 |
| C5 | Lemma D | holds | §2.3 |
| C6 | **Theorem Q** | holds | §2.4: every step re-derived (minimax, sampling, both cases, Lemma W bound, misclassification, time) |
| C7 | Corollary Q ("not NP-hard unless NP ⊆ QP"; ETH) | holds | §2.4 |
| C8 | Lemma PP and the remark after it | holds | §2.5 |
| K1 | r5-core Proposition D (i)-(iv) | holds | §3.1; checked `k <= 7` ((i)-(iii)), HYB `k <= 6` |
| K2 | CDESC soundness and time (§3.1) | holds | §3.2 |
| K3 | Lemma G (§3.2) | holds | §3.3 |
| K4 | Proposition CF (i)-(iv) | holds | §3.4; (iv) re-checked on rebuilt `Z_k`, `Z^B_k`, `k <= 4` |
| K5 | ADESC soundness and guided cost with anchors (§5.1) | holds | §3.5; the guided cost needs `A_0 ⊆ W_E`, `B_0 ⊆ W_F` (implicit) |
| K6 | Theorem 5.2 (E1), (F1) | holds | §3.6 |
| K7 | **Theorem 5.2 (E2), (F2)** | **false as stated; holds with repair** | §3.6: counterexamples; repair in full |
| K8 | Theorem 5.2 "Consequently ... ADESC(5, 2, c) accepts" | gap (holds with the repair) | §3.6 |
| K9 | Proposition 5.2' | holds | §3.7 (with `B_0 ⊆ W_F`, implicit) |

(Sections 2-7 are being written; computations recorded in §4.)
