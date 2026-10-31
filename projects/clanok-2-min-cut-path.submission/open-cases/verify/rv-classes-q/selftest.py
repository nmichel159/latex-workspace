"""Self-test of qcore/qchecks: solvers against each other on random instances.
usage: python selftest.py SEED COUNT"""
import itertools
import random
import sys

from qcore import Inst, desc_literal, hyper_dist, desc_emin, solve_game, min_cover, popcount
from qchecks import class_search, walk_ok
from qgen import random_instance


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    st = {"inst": 0, "yes": 0, "paths": 0, "desc": 0, "games": 0, "covers": 0, "search": 0}
    for it in range(count):
        N = rng.randint(3, 7)
        n = rng.randint(1, 7)
        c = rng.randint(1, n)
        I = random_instance(rng, N, n, c, rng.choice([0.2, 0.35, 0.5]), rng.choice([0.2, 0.35, 0.5]),
                            fresh=rng.random(), p2=rng.random() < 0.7)
        st["inst"] += 1
        sols = I.solutions()
        yes = bool(sols)
        r1, P1 = I.shortest_paths_dfs()
        r2, P2 = I.shortest_paths_modes()
        assert (r1 is not None) == yes == (r2 is not None), "existence"
        if yes:
            st["yes"] += 1
            assert r1 == r2, ("length", r1, r2)
            assert sorted(P1) == sorted(P2), "path sets"
            for P in P1:
                assert I.is_valid_path(P) and len(P) == r1
            st["paths"] += len(P1)
        # exact search with K = all sides
        W = class_search(I, I.sideset, 10 ** 6)
        assert (W is not None) == yes, "class search exact"
        if W is not None:
            assert walk_ok(I, W)
        st["search"] += 1
        # DESC literal vs distance array
        if I.c <= 6 and len(I.sides) <= 10:
            dist = hyper_dist(I.c, sols)
            for (f, g, e) in ((0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 1, 1), (1, 1, 0), (2, 0, 1)):
                lit, _ = desc_literal(I, f, g, e)
                em, _ = desc_emin(I, f, g, dist)
                assert lit == (em <= e), ("desc", f, g, e, lit, em)
                if lit:
                    assert yes
                st["desc"] += 1
    # games
    for it in range(count // 4):
        R, C = rng.randint(1, 7), rng.randint(1, 7)
        A = [[rng.randrange(2) for _ in range(C)] for _ in range(R)]
        lam, p, q = solve_game(A)
        st["games"] += 1
    # covers vs brute force
    for it in range(count // 4):
        nU = rng.randint(1, 9)
        sets = [rng.randrange(1 << nU) for _ in range(rng.randint(1, 8))]
        univ = (1 << nU) - 1
        h, idx = min_cover(univ, sets)
        best = None
        for k in range(len(sets) + 1):
            for combo in itertools.combinations(range(len(sets)), k):
                u = 0
                for i in combo:
                    u |= sets[i]
                if u & univ == univ:
                    best = k
                    break
            if best is not None:
                break
        assert h == best, (h, best, sets)
        if h:
            u = 0
            for i in idx:
                u |= sets[i]
            assert u & univ == univ and len(idx) == h
        st["covers"] += 1
    print(st, flush=True)


if __name__ == "__main__":
    main()
