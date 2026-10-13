"""Adversarial search for false positives of AC / PC (path-position CSP of dc-algorithm/zz.py) on 2CH WITH CLASSES
(ties) + P2.  No earlier hunt used ties among the middle elements (hunt2.py: strict orders, switch model, 2CH).

Hill climbing on 2CHC instances (gzz.py): mutations of sides and classes, P2 repaired after every mutation.
Score of a no-instance (branch-and-bound exact answer): largest window w with AC_w 'yes' (positions L = min(default,
L0 + PAD), L0 = shortest relaxed walk), then the largest window with PC_w 'yes'; yes-instances are rejected.
A no-instance with PC 'yes' for some L is a false positive of the default PC test (padding, tools.py).
Usage: python hunt_tie.py SEED STEPS OUTFILE [NMAX nMAX]
"""
import os
import sys
import json
import time
import random

for _v in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gzz  # noqa: E402
import tools  # noqa: E402
from tools import zz, pcfast  # noqa: E402

NMAX, nMAX, PAD = 7, 9, 4


def rnd(rng):
    """A random 2CHC + P2 no-instance whose relaxation (both sides of every switch) is a yes-instance."""
    while True:
        N = rng.randint(4, NMAX)
        n = rng.randint(4, nMAX)
        ncls = rng.randint(2, max(2, n - 2))
        inst = gzz.random_inst(rng, N, n, ncls, rng.uniform(0.1, 0.3), rng.uniform(0.1, 0.3), p2=True,
                               newnode=rng.choice([0.5, 0.8, 1.0]), maxN=NMAX + 8)
        N, E, F, cls, s, t = inst
        # make t rare: keep it in at most two sides
        holders = [(i, 0) for i in range(len(E)) if (E[i] >> t) & 1] + [(i, 1) for i in range(len(F)) if (F[i] >> t) & 1]
        rng.shuffle(holders)
        E, F = list(E), list(F)
        for i, T in holders[2:]:
            if T == 0:
                E[i] &= ~(1 << t)
            else:
                F[i] &= ~(1 << t)
        inst = gzz.repair(rng, (N, E, F, cls, s, t), 1.0, NMAX + 8)
        if gzz.relaxed(inst) and tools.bb_solve(inst) is None:
            return inst


def mutate(rng, inst):
    N, E, F, cls, s, t = inst
    E, F, cls = list(E), list(F), list(cls)
    n = len(E)
    r = rng.random()
    if r < 0.3:
        i = rng.randrange(n)
        E[i] ^= 1 << rng.randrange(N)
    elif r < 0.6:
        i = rng.randrange(n)
        F[i] ^= 1 << rng.randrange(N)
    elif r < 0.72:
        i = rng.randrange(n)
        cls[i] = rng.choice(cls + [max(cls) + 1])
    elif r < 0.8 and n < nMAX:
        E.append(1 << rng.randrange(N))
        F.append(1 << rng.randrange(N))
        cls.append(rng.choice(cls))
    elif r < 0.86 and n > 3:
        i = rng.randrange(n)
        del E[i], F[i], cls[i]
    elif r < 0.92 and N < NMAX + 6:
        N += 1
    else:
        x = rng.randrange(N)
        if x != s:
            t = x
    # drop node bits beyond N (none), renumber classes compactly
    m = {c: j for j, c in enumerate(sorted(set(cls)))}
    cls = [m[c] for c in cls]
    inst = gzz.repair(rng, (N, E, F, cls, s, t), 0.3, NMAX + 6)
    return inst


def window_score(fn, Lmax):
    lo, hi = -1, Lmax
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if fn(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


def score(inst, want_pc):
    if not gzz.p2_ok(inst):
        return None, "nop2"
    if tools.bb_solve(inst) is not None:
        return None, "yes"
    z, _ = gzz.to_zz(inst)
    L0 = tools.shortest_relaxed_L(z)
    if L0 is None:
        return 0, "relax-no"
    Ld = z.n if z.n % 2 else z.n - 1
    L = min(Ld, L0 + PAD)
    if L % 2 == 0:
        L -= 1
    csp = zz.CSP(z, L)

    def acw(w):
        csp.window = w
        return zz.arc_consistency(csp, csp.init_domains()) is not None
    w = window_score(acw, L)
    if w < L:
        return 1 + 100 * w // max(L, 1), "ac-no"
    if not want_pc:
        return 10000, "ac-fp"
    wp = window_score(lambda ww: pcfast.pc_answer(z, L, window=ww), L)
    if wp < L:
        return 10000 + 100 * wp // max(L, 1), "ac-fp"
    return 100000, "pc-fp"


def main():
    global NMAX, nMAX
    seed, steps, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    if len(sys.argv) > 5:
        NMAX, nMAX = int(sys.argv[4]), int(sys.argv[5])
    rng = random.Random(seed)
    found = {"ac-fp": 0, "pc-fp": 0, "no": 0, "evals": 0}
    cur, cur_score, since = None, -1, 0
    t0 = time.time()
    for step in range(steps):
        if cur is None or since > 300:
            cur = rnd(rng)
            sc, kind = score(cur, False)
            cur_score = -1 if sc is None else sc
            since = 0
        cand = mutate(rng, cur)
        sc, kind = score(cand, cur_score >= 10000)
        found["evals"] += 1
        since += 1
        if sc is None:
            continue
        found["no"] += 1
        if kind in ("ac-fp", "pc-fp"):
            found[kind] += 1
            if kind == "pc-fp" or found["ac-fp"] <= 30:
                rec = {"seed": seed, "step": step, "kind": kind, "inst": [cand[0], cand[1], cand[2], cand[3],
                                                                         cand[4], cand[5]]}
                with open(out, "a") as f:
                    f.write(json.dumps(rec) + "\n")
            if kind == "pc-fp":
                print("PC false positive at step", step, gzz.fmt(cand), flush=True)
        if sc >= cur_score:
            if sc > cur_score:
                since = 0
            cur, cur_score = cand, sc
        if step % 500 == 0:
            print(step, found, "%.0fs" % (time.time() - t0), flush=True)
    print("done", seed, found, "%.0fs" % (time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
