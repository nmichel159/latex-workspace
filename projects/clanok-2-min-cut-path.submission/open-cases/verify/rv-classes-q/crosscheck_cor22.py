"""Cross-check of Corollary 2a.2 (r5-classes.md §2a) with the certificate construction of the reviewed
r4-switch proof.  Imports verify/r4-switch-review/ (the independent reviewer's code of r4-switch, read-only) for
the generators of critical-run and planted switch-model instances, the straddle enumeration, Lemma 7 and the
case distinction of Theorem 8.  Everything about descriptions (sigma_U, misclassification, connectivity) is
computed with this review's own qcore.

usage: python crosscheck_cor22.py SEED TASKS WORKERS
For each instance and each shortest valid path (limit 10) and each type T: the T-certificate K_T of Lemma 7 (if a
T-straddle exists; path P* = the swap) or of Theorem 8 (otherwise); asserted: K_T contains the partners of all
T-members of the path; mis_P(K_T) = storage |P n K_T| (Corollary 2a.2); sigma_{K_T}^Phi with Phi = the
misclassified classes picks the path and connects s, t; the shape is within DESC(6, 12, 18): at most 6 sets
N_O[Z], at most 12 single sides, storage at most 18 (remark of verify/r4-switch-review.md §2.6).
"""
import json
import os
import random
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
REV = os.path.join(HERE, "..", "r4-switch-review")
sys.path.insert(0, HERE)
sys.path.append(REV)

from qcore import Inst  # noqa: E402
import core as rcore  # noqa: E402  (verify/r4-switch-review/core.py)
import proof as rproof  # noqa: E402
from gen_run import gen_run  # noqa: E402
from planted import gen_planted, is_shortest, saturate  # noqa: E402


def to_mine(inst):
    sw = [(set(E), set(F)) for E, F in inst.sw]
    return Inst(inst.N, inst.s, inst.t, sw, list(range(inst.n)))


def side_id(inst, i):
    w, typ = inst.sides[i]
    return 2 * w + typ


def check(inst, P, T, st):
    O = 1 - T
    ctx = rproof.Ctx(inst, P)
    sts = rproof.straddles(ctx, T)
    if sts:
        x, p, x1, x2, p1, p2 = sts[0]
        Ps = list(P)
        Ps[x - 1] = ctx.pidx[p]
        Ps[p - 1] = ctx.pidx[x]
        KT = set(inst.N_of(O, P[p - 1]))
        singles = [inst.partner[Ps[c - 1]] for c in (x - 1, x + 1)
                   if 1 <= c <= len(P) and inst.typ[Ps[c - 1]] == T and inst.partner[Ps[c - 1]] is not None]
        KT |= set(singles)
        nZ, ns, Pc = 1, len(singles), Ps
        st["swap"] = st.get("swap", 0) + 1
        step = "swap"
    else:
        Zs, singles, step = rproof.theorem8(ctx, T, st)
        KT = rproof.build_K(inst, T, Zs, singles)
        nZ, ns, Pc = len(Zs), len(singles), list(P)
        st["step%s" % step] = st.get("step%s" % step, 0) + 1
    I = to_mine(inst)
    Pm = [side_id(inst, i) for i in Pc]
    assert I.is_valid_path(Pm) and len(Pm) == len(P), "certificate path valid and shortest length"
    U = 0
    for i in KT:
        assert inst.typ[i] == O, "K_T has O-sides only"
        U |= 1 << side_id(inst, i)
    for a, x in enumerate(Pm):
        if (x & 1) == T and I.mask[x ^ 1]:
            assert (U >> (x ^ 1)) & 1, "partner of a T-member in K_T"
    storage = sum(1 for x in Pm if (U >> x) & 1)
    modes = I.sigma(U, O)
    Phi = I.misclassified(Pm, modes)
    assert len(Phi) == storage, ("mis = storage", len(Phi), storage)
    assert sorted(Phi) == sorted(I.cl[x >> 1] for x in Pm if (U >> x) & 1), "Phi = classes of stored members"
    m2 = modes
    for C in Phi:
        m2 ^= 1 << C
    assert I.picks_path(Pm, m2) and I.connects(m2), "sigma^Phi connects"
    assert nZ <= 6 and ns <= 12 and storage <= 18, ("shape within DESC(6,12,18)", nZ, ns, storage, step)
    st["maxZ"] = max(st.get("maxZ", 0), nZ)
    st["maxsingles"] = max(st.get("maxsingles", 0), ns)
    st["maxstorage"] = max(st.get("maxstorage", 0), storage)
    st["checked"] = st.get("checked", 0) + 1


def one(seed):
    rng = random.Random(seed)
    st = {}
    fails = []
    for it in range(40):
        kind = rng.random()
        if kind < 0.6:
            kw = [rng.choice('OOOT') for _ in range(rng.randint(0, 4))]
            lw = [rng.choice('OOOOT') for _ in range(rng.randint(4, 10))]
            m = rng.randint(1, 6)
            g = gen_run(rng, kw, m, lw, hub=rng.choice([0, 0, 0.3]), pM=rng.choice([0.5, 0.65, 0.8, 0.95]),
                        pB=rng.choice([0.0, 0.1, 0.25]), p_extra=rng.choice([0, 0, 0.03]),
                        reverse=rng.random() < 0.5, off=rng.choice([0, 0, 1, 2]), off_dens=rng.choice([0.03, 0.08]),
                        two_spans=rng.random() < 0.4)
        else:
            g = gen_planted(rng, rng.randint(0, 4), rng.randint(0, 4), rng.randint(0, 4), rng.randint(0, 4),
                            zone_T=rng.choice([0, 0.2]), hub=rng.choice([0, 0.3]), off=rng.choice([0, 1]),
                            straddle=rng.choice([0, 0, 1]))
        if g is None:
            continue
        inst, P, T0 = g
        if not rcore.p2(inst) or not is_shortest(inst, P):
            continue
        if rng.random() < 0.3 and inst.N > 2:
            try:
                inst, P, _ = saturate(rng, inst, P, rng.randint(5, 25))
            except ValueError:
                pass
        st["inst"] = st.get("inst", 0) + 1
        L, paths = rcore.shortest_valid_paths(inst, limit=10)
        for Q in [tuple(P)] + [q for q in paths if tuple(q) != tuple(P)]:
            for T in (0, 1):
                try:
                    check(inst, list(Q), T, st)
                except (AssertionError, rproof.ClaimFailure) as ex:
                    fails.append((repr(ex), inst.to_json(), list(Q), T))
    return st, fails


def main():
    seed, tasks, workers = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    tot = {}
    allf = []
    with Pool(workers) as pool:
        for st, fails in pool.imap_unordered(one, [seed * 100000 + i for i in range(tasks)]):
            for k, v in st.items():
                if k.startswith("max"):
                    tot[k] = max(tot.get(k, 0), v)
                else:
                    tot[k] = tot.get(k, 0) + v
            allf.extend(fails)
    print(json.dumps(tot, sort_keys=True), flush=True)
    print("failures", len(allf), flush=True)
    if allf:
        with open(os.path.join(HERE, "runs", "fail-cor22-%d.json" % seed), "w") as fh:
            json.dump(allf[:20], fh)
        print(allf[0][0])


if __name__ == "__main__":
    main()
