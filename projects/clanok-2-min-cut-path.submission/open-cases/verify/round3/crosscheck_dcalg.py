"""Cross-check, after the own checks were finished (agent verify-round3): own AC, PC, exact solver and Theorem F
algorithm (r3core) against dc-algorithm/zz.py (ac_answer, pc_answer, pc_numpy, exact_dfs) and
dc-algorithm/bottom_witness.py, imported read-only. Also the 9-element AC counterexample of dc-algorithm.md §4 (D1),
built with the own code. Usage: python crosscheck_dcalg.py seed count"""
import os
import random
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from r3core import Inst, random_instance, preorder_from_relations  # noqa: E402

sys.path.insert(1, os.path.join(HERE, "..", "..", "dc-algorithm"))
import zz  # noqa: E402


def to_theirs(inst):
    le = [[bool(inst.le[a, b]) for b in range(inst.q)] for a in range(inst.q)]
    return zz.ZZ(inst.q, None, list(inst.R), u=inst.u, v=inst.v, le=le)


def d1_instance():
    # bottoms b0 = u, b1, b2, b3 (0..3), switches s0, s1, s2 (4..6), tops t1 (7), t0 = v (8)
    B, S, T = [0, 1, 2, 3], [4, 5, 6], [7, 8]
    rel = [(b, x) for b in B for x in S + T] + [(s, t) for s in S for t in T]
    le = preorder_from_relations(9, rel, [B, T])
    Nb = {4: [0, 2, 3], 5: [1, 2, 3], 6: [2, 3]}
    Nt = {4: [7], 5: [8, 7], 6: [8]}
    R = [(1, 7)] + [(b, s) for s in S for b in Nb[s]] + [(s, t) for s in S for t in Nt[s]]
    return Inst(9, le, R, 0, 8)


if __name__ == "__main__":
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    I = d1_instance()
    I.check()
    print("D1 instance: q=%d |R|=%d P2=%s answer=%s AC(L=9)=%s PC(L=9)=%s" % (
        I.q, len(I.R), I.p2(), I.solve_downsets()[0], I.ac(9)[0], I.pc(9)))
    rng = random.Random(seed)
    st = {"inst": 0, "p2": 0, "yes": 0, "ac_mis": 0, "pc_mis": 0, "pcnp_mis": 0, "exact_mis": 0, "acfp": 0,
          "pcfp": 0}
    for _ in range(count):
        inst = random_instance(rng, nb=rng.randint(1, 2), nm=rng.randint(2, 7), nt=rng.randint(1, 2),
                               p_rel=rng.choice([0.2, 0.4]), p_edge=rng.choice([0.2, 0.35, 0.5]),
                               p2='repair' if rng.random() < 0.7 else None, p_eqmid=rng.choice([0, 0.1]))
        z = to_theirs(inst)
        L = inst.q if inst.q % 2 == 1 else inst.q - 1
        mine_ac, mine_pc = inst.ac(L)[0], inst.pc(L)
        th_ac, th_pc, th_np = zz.ac_answer(z, L), zz.pc_answer(z, L), zz.pc_numpy(z, L)
        ex = inst.solve_downsets()[0]
        th_ex = zz.exact_dfs(z)
        th_ex = th_ex[0] if isinstance(th_ex, tuple) else th_ex
        st["inst"] += 1; st["p2"] += inst.p2(); st["yes"] += ex
        st["ac_mis"] += mine_ac != th_ac
        st["pc_mis"] += mine_pc != th_pc
        st["pcnp_mis"] += mine_pc != th_np
        st["exact_mis"] += ex != bool(th_ex)
        st["acfp"] += mine_ac and not ex
        st["pcfp"] += mine_pc and not ex
    print(st)
    print("violations:", st["ac_mis"] + st["pc_mis"] + st["pcnp_mis"] + st["exact_mis"])
