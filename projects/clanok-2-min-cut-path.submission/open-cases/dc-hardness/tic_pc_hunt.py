"""AC / PC of the path-position CSP (dc-algorithm/zz.py) on TIC no-instances (TIC is a special case of SW + P2).
Random TIC + P2 instances and P2-repaired local-SAT instances; for every no-instance whose relaxation is yes: AC,
and PC when AC says yes.  Then hill climbing from the AC false positives (mutate spans, repair P2, keep no-instances
with AC yes) to look for a PC false positive.  Every PC false positive is printed with the instance.
Usage: python tic_pc_hunt.py SEED COUNT CLIMB"""
import sys
import random
import time
import tic
from swlib import to_zz, zz


def relax_answers(K, E, F):
    z, _ = to_zz(tic.to_2ch(K, E, F))
    ac = zz.ac_answer(z)
    pc = zz.pc_numpy(z) if ac else False
    return ac, pc, z


def mutate(rng, K, E, F):
    E, F = list(E), list(F)
    for _ in range(rng.randint(1, 2)):
        w = rng.randrange(len(E))
        S = E if rng.random() < 0.5 else F
        if S[w] is None:
            continue
        a, b = S[w]
        if rng.random() < 0.5:
            a = max(0, min(b, a + rng.choice([-1, 1])))
        else:
            b = min(K, max(a, b + rng.choice([-1, 1])))
        S[w] = (a, b)
    E, F = tic.repair_p2(rng, K, E, F)
    return E, F


def main():
    seed, count, climb = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    st = {"no_rel_yes": 0, "ac_fp": 0, "pc_fp": 0}
    pool = []
    t0 = time.time()
    for it in range(count):
        K = rng.randint(3, 9)
        n = rng.randint(3, 8)
        K, E, F = tic.random_tic(rng, K, n, longp=rng.choice([0.0, 0.1, 0.3]))
        if tic.exact(K, E, F) is not None or not tic.relaxed(K, E, F):
            continue
        st["no_rel_yes"] += 1
        ac, pc, z = relax_answers(K, E, F)
        if ac:
            st["ac_fp"] += 1
            pool.append((K, E, F))
        if pc:
            st["pc_fp"] += 1
            print("PC FALSE POSITIVE", K, E, F, flush=True)
    print("random phase:", st, "%.0fs" % (time.time() - t0), flush=True)
    # climbing: keep no-instances with AC yes, prefer more switches / longer CSP
    climbed = {"steps": 0, "ac_fp": 0, "pc_fp": 0}
    if pool:
        cur = rng.choice(pool)
        for stp in range(climb):
            K, E, F = cur
            E2, F2 = mutate(rng, K, E, F)
            if tic.exact(K, E2, F2) is not None or not tic.relaxed(K, E2, F2):
                continue
            ac, pc, z = relax_answers(K, E2, F2)
            climbed["steps"] += 1
            if ac:
                climbed["ac_fp"] += 1
                cur = (K, E2, F2)
            if pc:
                climbed["pc_fp"] += 1
                print("PC FALSE POSITIVE (climb)", K, E2, F2, flush=True)
            if rng.random() < 0.02:
                cur = rng.choice(pool)
    print("climb phase:", climbed, "%.0fs" % (time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
