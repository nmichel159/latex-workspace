# walk-dp: searching for the walk directly (working report, in progress)

Agent `walk-dp`, started 2026-11-02, resumed the same evening after a session limit (about 25 minutes used before it). Programs: `elegant/walk-dp/`, logs: `elegant/walk-dp/logs/`. Nothing here is a result until a referee has read it.

## State (updated as I go)

1. **Q1, window search: refuted as stated (tested, `q1_window.py`, `logs/q1-1.txt`).** Even with all far-pair atoms of the true `A_P`, `B_P` (union of all `FR`, intersection of all `ER`), a shortest locally valid walk is shorter than `P` and invalid on every family except `two`, for windows `k = 1, 2, 4, 6` (larger windows ran out of the state cap). Reason: pumping. On `small`, seed 3: `... E9 t9 F79 t80 E80 F81 ...` has the conflict `F79 ~ F81` at distance 3; with `k = 4` the search returns `... F79 t80 E80 t80 E80 F81 ...`. A walk may repeat a short cycle until the conflict leaves the window, so the span grows with `k` (3, 3, 5, 7).
2. **Q3, closure on the double cover (`closure.py`).** Nodes: `x` low, `x` high. Rules: block-cut chain from `u` low to `v` high, nodes off the chain die, forced nodes (cut vertices of the chain) kill their conflict partners. SAC = probe each node.
   - tiny random P2 instances (`q3_tiny.py`, 60 s, 178419 instances, 106193 no): SAC refutes all no-instances; the closure alone all but 87.
   - earlier families (`q3_old.py`, `logs/old-1.txt`): hub families `H(2,2)`, `H(2,3)`, `H(3,3)` (where path consistency fails) are refuted by SAC, not by the closure.
   - calibration without P2 (`calib.py`): K4 with 3 colours and K5 with 4 colours pass SAC; all 105 unsatisfiable 3-SAT encodings pass SAC. So the test separates P2 from no P2 at these sizes.
3. **Fixing a literal keeps P2 (proved, `literal.py`).** See the section below.
4. **SAC does not decide ZZ with P2 (tested, counterexamples saved: `logs/hunt-lit-1.txt.FOUND.json`).** Planted yes-instances with one or more fixed literals are P2 no-instances on which SAC passes: 68 of 79 no-instances in 74 s (`hunt_lit.py`). The tiny random instances could not reach this.
5. Next: closure with learned conflicts (a monotone closure on a growing conflict graph). See below when written.

## Fixing a literal keeps P2 (proved)

For a down-set move: `I|x in D` moves `dn x` into the class of `u`; `I|x notin D` moves `up x` into the class of `v`; edges that stop being strict are removed. The yes-solutions of the new instance are the solutions of `I` with the literal.
P2 stays. Take the first move, `M = dn x` with the class of `u`. Let `p, q` be incomparable in the new order. Then neither is in `M`, and the order outside `M` is unchanged, so they were incomparable before, and they had a witness `z`. A lower witness stays a lower witness: `z < p, q` holds also when `z` moved, and the edges `zp`, `zq` stay strict. An upper witness `z` has `p, q < z`, and `z notin M`, as `M` is a down-set and `p notin M`. The other move is dual.
