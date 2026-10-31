"""Theorem F of dc-algorithm.md (agent verify-round3), own implementation (r3core.Inst.thmF).

Families (all with P2 after repair):
  bottom : bottom witnesses added for every incomparable pair, then P2 repair (which keeps the witnesses)
  top    : top witnesses
  bottie : bottom witnesses, ties between middle elements (p_eqmid > 0), denser order
  mixed  : witnesses of random kind (bottom / top / none) then P2 repair  -> hypothesis usually fails; recorded
For every instance whose hypothesis holds: thmF (bottom or dual) = exact answer (down-sets) = DFS answer; for every
down-set D connecting u, v, every shortest u-v path of G_D (up to 200 per D) satisfies claim (ii): incomparable peaks
(bottom version; valleys for the dual) are consecutive, and |A| <= 2. AC and PC (L = largest odd <= q) on a sample
of no-instances.
Usage: python testF.py tag baseseed count jobs [procs]"""
import random
import sys
import time
from multiprocessing import Pool

from r3core import random_instance

FAMS = ["bottom", "top", "bottie", "mixed"]
import os
if os.environ.get("FAMS"):
    FAMS = os.environ["FAMS"].split(",")


def shortest_paths(inst, D, limit=200):
    res = inst.gd_shortest_dist(D)
    if res is None:
        return []
    dist, nb = res
    if inst.v not in dist:
        return []
    out = []
    # enumerate shortest paths backwards from v
    def rec(x, acc):
        if len(out) >= limit:
            return
        if x == inst.u:
            out.append(list(reversed(acc)))
            return
        for y in nb[x]:
            if dist.get(y, -1) == dist[x] - 1:
                acc.append(y)
                rec(y, acc)
                acc.pop()
    rec(inst.v, [inst.v])
    return out


def check_ii(inst, P, dual):
    """Claim (ii) on a shortest path P; returns (ok, |A|)."""
    le = inst.le
    if not dual:
        pos = list(range(1, len(P), 2))       # peaks
        mid = [i for i in pos if inst.middle(P[i])]
    else:
        pos = list(range(0, len(P), 2))       # valleys
        mid = [i for i in pos if inst.middle(P[i])]
    for a in range(len(mid)):
        for b in range(a + 1, len(mid)):
            i, j = mid[a], mid[b]
            if not inst.comparable(P[i], P[j]) and abs(i - j) != 2:
                return False, None
    els = [P[i] for i in mid]
    # minimal classes (bottom version) or maximal classes (dual)
    if not dual:
        mins = [x for x in els if not any(inst.lt(y, x) for y in els)]
    else:
        mins = [x for x in els if not any(inst.lt(x, y) for y in els)]
    reps = []
    for x in mins:
        if not any(inst.eq(x, y) for y in reps):
            reps.append(x)
    return len(reps) <= 2, len(reps)


def job(args):
    fam, seed, count = args
    rng = random.Random(seed)
    st = {"n": 0, "hyp": 0, "yes": 0, "viol_alg": 0, "viol_dfs": 0, "viol_ii": 0, "paths_ii": 0, "maxA": 0,
          "mixed_alg_wrong": 0, "pc_runs": 0, "ac_fp": 0, "pc_fp": 0}
    bad = []
    for _ in range(count):
        if fam == "bottom":
            inst = random_instance(rng, nb=rng.randint(1, 3), nm=rng.randint(2, 9), nt=rng.randint(1, 3),
                                   p_rel=rng.choice([0.1, 0.25, 0.4]), p_edge=rng.choice([0.2, 0.35, 0.5]),
                                   witness='bottom')
            dual = False
        elif fam == "top":
            inst = random_instance(rng, nb=rng.randint(1, 3), nm=rng.randint(2, 9), nt=rng.randint(1, 3),
                                   p_rel=rng.choice([0.1, 0.25, 0.4]), p_edge=rng.choice([0.2, 0.35, 0.5]),
                                   witness='top')
            dual = True
        elif fam == "bottie":
            inst = random_instance(rng, nb=rng.randint(1, 3), nm=rng.randint(3, 9), nt=rng.randint(1, 3),
                                   p_rel=rng.choice([0.3, 0.5]), p_edge=rng.choice([0.3, 0.5]),
                                   witness='bottom', p_eqmid=rng.choice([0.1, 0.25]))
            dual = False
        elif fam in ("bottombig", "topbig"):
            inst = random_instance(rng, nb=rng.randint(1, 2), nm=rng.randint(8, 12), nt=rng.randint(1, 2),
                                   p_rel=rng.choice([0.05, 0.15, 0.3]), p_edge=rng.choice([0.08, 0.15, 0.25]),
                                   witness='bottom' if fam == "bottombig" else 'top',
                                   p_eqmid=rng.choice([0, 0, 0.08]))
            dual = (fam == "topbig")
        else:
            inst = random_instance(rng, nb=rng.randint(1, 3), nm=rng.randint(3, 9), nt=rng.randint(1, 3),
                                   p_rel=rng.choice([0.1, 0.25, 0.4]), p_edge=rng.choice([0.15, 0.3]),
                                   witness='mixed')
            dual = False
        inst.check()
        assert inst.p2()
        st["n"] += 1
        ans, D, nd = inst.solve_downsets()
        dfs = inst.solve_dfs()
        st["yes"] += ans
        if (dfs is not None) != ans or (dfs is not None and not inst.is_consistent_zigzag(dfs)):
            st["viol_dfs"] += 1
            bad.append(("dfs", inst.q, inst.R))
        hyp = inst.top_witness_ok() if dual else inst.bottom_witness_ok()
        if fam == "mixed":
            a1 = inst.thmF()[0]
            a2 = inst.thmF(dual=True)[0]
            if (a1 or a2) != ans:
                st["mixed_alg_wrong"] += 1
            if inst.bottom_witness_ok() or inst.top_witness_ok():
                st["hyp"] += 1
                hb = inst.bottom_witness_ok()
                if inst.thmF(dual=not hb)[0] != ans:
                    st["viol_alg"] += 1
                    bad.append(("alg-mixed", inst.q, inst.R))
            continue
        if not hyp:
            continue
        st["hyp"] += 1
        a = inst.thmF(dual=dual)
        if a[0] != ans:
            st["viol_alg"] += 1
            bad.append(("alg", fam, inst.q, [list(r) for r in inst.le.astype(int)], inst.R))
        if a[0] and not inst.is_downset(a[2]):
            st["viol_alg"] += 1
        # claim (ii) on all down-sets
        if ans:
            for Dx in inst.downsets():
                if not inst.gd_connected(Dx):
                    continue
                for P in shortest_paths(inst, Dx):
                    st["paths_ii"] += 1
                    ok, k = check_ii(inst, P, dual)
                    if not ok:
                        st["viol_ii"] += 1
                        bad.append(("ii", fam, inst.q, inst.R, P))
                    elif k is not None:
                        st["maxA"] = max(st["maxA"], k)
        elif st["pc_runs"] < 40 and inst.q <= 12:
            L = inst.q if inst.q % 2 == 1 else inst.q - 1
            st["pc_runs"] += 1
            if inst.ac(L)[0]:
                st["ac_fp"] += 1
                if inst.pc(L):
                    st["pc_fp"] += 1
    return fam, seed, st, bad[:5]


if __name__ == "__main__":
    tag, base, count, jobs = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    procs = min(int(sys.argv[5]) if len(sys.argv) > 5 else 6, 8)
    tasks = [(FAMS[j % len(FAMS)], base + j, count) for j in range(jobs)]
    t0 = time.time()
    tot = {}
    out = open("results-F-%s.txt" % tag, "w")
    with Pool(procs) as pool:
        for fam, seed, st, bad in pool.imap_unordered(job, tasks):
            d = tot.setdefault(fam, {})
            for k, x in st.items():
                d[k] = max(d.get(k, 0), x) if k == "maxA" else d.get(k, 0) + x
            line = "%s seed %d: %s" % (fam, seed, st)
            print(line, flush=True)
            out.write(line + "\n")
            for b in bad:
                out.write("  BAD %r\n" % (b,))
            out.flush()
    out.write("\nTOTALS (%.0fs)\n" % (time.time() - t0))
    viol = 0
    for fam, d in sorted(tot.items()):
        out.write("%s: %s\n" % (fam, d))
        viol += d["viol_alg"] + d["viol_dfs"] + d["viol_ii"]
    out.write("violations: %d\n" % viol)
    out.close()
    print("violations:", viol)
