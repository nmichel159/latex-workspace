"""Experiment E1: in solvable 2CH+P2 instances, how many switches must deviate from a common mode?
For each solvable instance compute k* = least k such that 'all switches in mode M except k of them' connects s, t.
Random instances plus hill climbing that maximises k*.
Usage: python exp_exceptional.py SEED COUNT CLIMBSTEPS"""
import sys, random
from twoch import solve, exceptional_solve, random_p2_instance, p2_ok, fmt_inst


def kstar(inst):
    if solve(inst) is None:
        return None
    r = exceptional_solve(inst, len(inst[1]))
    return r[0]


def mutate(rng, inst):
    N, E, F, s, t = inst
    E = E[:]
    F = F[:]
    n = len(E)
    for _ in range(rng.randint(1, 3)):
        i = rng.randrange(n)
        x = rng.randrange(N)
        if rng.random() < 0.5:
            E[i] ^= 1 << x
        else:
            F[i] ^= 1 << x
    return (N, E, F, s, t)


def main():
    seed, count, steps = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    dist = {}
    best = (-1, None)
    for it in range(count):
        N = rng.randint(4, 9)
        n = rng.randint(3, 9)
        inst = random_p2_instance(rng, N, n, rng.uniform(0.1, 0.4), rng.uniform(0.1, 0.4))
        k = kstar(inst)
        dist[k] = dist.get(k, 0) + 1
        if k is not None and k > best[0]:
            best = (k, inst)
    print("random: k* distribution", dict(sorted(dist.items(), key=lambda z: (z[0] is None, z[0]))))
    print("random best", best[0], fmt_inst(best[1]))
    # hill climbing from the best
    cur = best
    for st in range(steps):
        cand = mutate(rng, cur[1])
        if not p2_ok(cand[1], cand[2]):
            continue
        if len(cand[1]) > 11:
            continue
        k = kstar(cand)
        if k is not None and k >= cur[0]:
            if k > cur[0]:
                print("climb step %d: k* = %d" % (st, k), fmt_inst(cand), flush=True)
            cur = (k, cand)
    print("final best k* =", cur[0], fmt_inst(cur[1]))


if __name__ == "__main__":
    main()
