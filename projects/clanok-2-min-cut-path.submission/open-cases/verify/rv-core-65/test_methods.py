"""Self-check of the reviewer's exact routines: the two methods for all shortest valid paths (down-set enumeration
and state BFS + DFS) agree, every path returned is valid, and yes/no agrees with brute force over down-sets.

usage: python test_methods.py SEED COUNT MMIN MMAX
"""
import sys
import random
from collections import Counter
from gsf import random_inst
from planted import planted_inst

seed, count, mmin, mmax = (int(a) for a in sys.argv[1:5])
rng = random.Random(seed)
st = Counter()
for it in range(count):
    m = rng.randint(mmin, mmax)
    if it % 2:
        I = random_inst(rng, m, p_order=rng.choice([0.2, 0.4, 0.6]), p_tie=rng.choice([0, 0.5]),
                        p_side=rng.choice([0.1, 0.2]), p_med=rng.choice([0.1, 0.4]))
    else:
        r = rng.randint(3, max(3, m - 2))
        rest = m - r
        nu = rng.randint(0, rest)
        nd = rng.randint(0, rest - nu)
        I = planted_inst(rng, r=r, n_up=nu, n_down=nd, n_free=rest - nu - nd)
    I.validate()
    if not I.p2():
        st["P2 FAILS"] += 1
        continue
    r1, p1 = I.all_shortest_paths()
    r2, p2 = I.all_shortest_paths_dfs()
    yes = I.yes()
    st["yes" if yes else "no"] += 1
    if (r1 is not None) != yes or (r2 is not None) != yes:
        st["YES/NO DISAGREES"] += 1
    if r1 != r2:
        st["LENGTH DISAGREES"] += 1
    if set(p1) != set(p2):
        st["PATH SETS DISAGREE"] += 1
    for P in p1:
        if not I.is_valid_path(list(P)) or len(P) != r1:
            st["INVALID PATH"] += 1
    st["paths"] += len(p1)
print("test_methods seed %d count %d m %d-%d: %s" % (seed, count, mmin, mmax, dict(sorted(st.items()))))
