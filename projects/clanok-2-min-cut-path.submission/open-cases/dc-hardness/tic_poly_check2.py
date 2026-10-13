"""Harder checks of tic_poly.poly_solve against brute force: (a) larger random TIC + P2 instances,
(b) local SAT instances (tic.local_sat_instance) made P2 by random span extension (repair_p2),
(c) no-instances whose relaxation is yes (the interesting ones), counted separately.
Usage: python tic_poly_check2.py SEED COUNT"""
import sys
import random
import tic
from tic_poly import poly_solve


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    st = {}
    for it in range(count):
        mode = rng.choice(["rand", "sat"])
        if mode == "rand":
            K = rng.randint(3, 10)
            n = rng.randint(3, 9)
            K, E, F = tic.random_tic(rng, K, n, longp=rng.choice([0.0, 0.1, 0.3, 0.6]))
        else:
            nv = rng.randint(1, 3)
            m = rng.randint(2, 4)
            clauses = []
            for _ in range(m):
                c = sorted({rng.choice([1, -1]) * rng.randint(1, nv) for _ in range(rng.randint(1, 3))})
                if not any(-l in c for l in c):
                    clauses.append(c)
            if not clauses:
                continue
            try:
                K, E, F, occ = tic.local_sat_instance(nv, clauses)
            except ValueError:
                continue
            if len(E) > 9:
                continue
            E, F = tic.repair_p2(rng, K, E, F)
        ex = tic.exact(K, E, F) is not None
        rel = tic.relaxed(K, E, F)
        po = poly_solve(K, E, F)[0]
        key = (mode, "yes" if ex else ("no-relaxed-yes" if rel else "no-relaxed-no"), "agree" if ex == po else "DISAGREE")
        st[key] = st.get(key, 0) + 1
        if ex != po:
            print("MISMATCH", K, E, F, flush=True)
    for k in sorted(st):
        print(k, st[k])


if __name__ == "__main__":
    main()
