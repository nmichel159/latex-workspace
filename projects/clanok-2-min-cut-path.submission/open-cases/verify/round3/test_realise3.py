"""Validation of realise3.py (agent verify-round3): on random P2 instances, the graph checks (d = 2, c = N, DC,
PIMC search on G(Pi)) agree with the ZZ answer of r3core (down-set enumeration).
Usage: python test_realise3.py seed count"""
import random
import sys

import networkx as nx

from r3core import random_instance
from realise3 import realise, Flow, pimc_search, dc_check

if __name__ == "__main__":
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    st = {"inst": 0, "yes": 0, "viol": 0, "maxV": 0, "skipped_N<=3": 0}
    for it in range(count):
        inst = random_instance(rng, nb=rng.randint(1, 2), nm=rng.randint(1, 5), nt=rng.randint(1, 2),
                               p_rel=0.3, p_edge=rng.choice([0.3, 0.5, 0.7]), p_eqmid=rng.choice([0, 0.15]))
        inst.check()
        assert inst.p2()
        G, N = realise(inst, M=1)
        if N <= 3:
            st["skipped_N<=3"] += 1
            continue
        st["inst"] += 1
        st["maxV"] = max(st["maxV"], G.number_of_nodes())
        ans = inst.solve_downsets()[0]
        st["yes"] += ans
        fl = Flow(G)
        c = fl.value([inst.u], [inst.v])
        d = nx.shortest_path_length(G, inst.u, inst.v)
        ok = dc_check(G)[0]
        P, _ = pimc_search(G, inst.u, inst.v, c, fl)
        if c != N or d != 2 or not ok or (P is not None) != ans:
            st["viol"] += 1
            print("VIOLATION", inst.q, inst.R, c, N, d, ok, P, ans)
    print(st)
    print("violations:", st["viol"])
