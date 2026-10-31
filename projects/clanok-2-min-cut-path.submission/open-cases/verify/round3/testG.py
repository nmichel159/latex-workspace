"""Lemma G of dc-algorithm.md and the CSP facts of its Section 4 (agent verify-round3).

Random ZZ instances (with and without P2), q <= 11; for odd L = 1, 3, ..., Lmax:
 (a) CSP(L) has a solution (own backtracking) iff a consistent zigzag of length <= L exists (exact shortest length
     = min over down-sets D of dist_{G_D}(u, v));
 (b) PC(L) => AC(L); a solvable CSP(L) is never refuted by AC or PC;
 (c) Lemma G: PC(L) non-empty => PC(L + 2) non-empty; and the explicit network N' of the proof (positions L+1, L+2
     copies of L) built from the PC closure N at L is a certificate at L + 2 (pc_cert.certify: inside the base
     constraints of CSP(L+2), path consistent, no empty relation).
Usage: python testG.py tag baseseed count jobs [procs]"""
import random
import sys
import time
from multiprocessing import Pool

import numpy as np

from r3core import random_instance
from pc_cert import certify


def shortest_zigzag(inst):
    best = None
    for D in inst.downsets():
        r = inst.gd_shortest_dist(D)
        if r is None:
            continue
        dist, _ = r
        if inst.v in dist and (best is None or dist[inst.v] < best):
            best = dist[inst.v]
    return best


def csp_solvable(inst, L):
    E, unary, base = inst.csp(L)
    m = len(E)
    if m == 0:
        return False
    assign = []

    def rec(j):
        if j == L:
            return True
        for a in range(m):
            if not unary[j][a]:
                continue
            if all(base[(i, j)][assign[i], a] for i in range(j)):
                assign.append(a)
                if rec(j + 1):
                    return True
                assign.pop()
        return False

    return rec(0)


def extend_network(N, L):
    """N' of the proof of Lemma G: positions L, L+1 (0-based) copies of position L-1."""
    Lp = L + 2
    m = N.shape[2]
    Np = np.zeros((Lp, Lp, m, m), dtype=bool)
    Np[:L, :L] = N
    src = lambda i: i if i < L else L - 1
    for i in range(Lp):
        for j in range(Lp):
            if i < L and j < L:
                continue
            si, sj = src(i), src(j)
            if si == sj:
                Np[i, j] = N[si, si]           # identity on the domain (N[si, si] is diagonal)
            else:
                Np[i, j] = N[si, sj]
    return Np


def job(args):
    seed, count = args
    rng = random.Random(seed)
    st = {"n": 0, "p2": 0, "csp_mismatch": 0, "pc_not_ac": 0, "unsound": 0, "G_viol": 0, "Gcert_bad": 0,
          "Gcert_runs": 0, "pc_fp_L": 0, "ac_fp_L": 0, "ac_nonmono": 0}
    bad = []
    for _ in range(count):
        p2 = rng.random() < 0.6
        inst = random_instance(rng, nb=rng.randint(1, 2), nm=rng.randint(2, 6), nt=rng.randint(1, 2),
                               p_rel=rng.choice([0.2, 0.4]), p_edge=rng.choice([0.3, 0.5]),
                               p2='repair' if p2 else None, p_eqmid=rng.choice([0, 0.1]))
        inst.check()
        st["n"] += 1
        st["p2"] += inst.p2()
        ell = shortest_zigzag(inst)
        Lmax = inst.q + 4
        prev_pc = None
        prev_ac = None
        for L in range(1, Lmax + 1, 2):
            sol = csp_solvable(inst, L) if L <= 9 else (ell is not None and ell <= L)
            truth = ell is not None and ell <= L
            if L <= 9 and sol != truth:
                st["csp_mismatch"] += 1
                bad.append(("csp", inst.q, inst.R, L))
            a = inst.ac(L)[0]
            p, N, E = inst.pc(L, return_net=True)
            if p and not a:
                st["pc_not_ac"] += 1
            if truth and (not a or not p):
                st["unsound"] += 1
                bad.append(("unsound", inst.q, inst.R, L))
            if not truth:
                st["pc_fp_L"] += p
                st["ac_fp_L"] += a
            if prev_pc and not p:
                st["G_viol"] += 1
                bad.append(("G", inst.q, inst.R, L))
            if prev_ac and not a:
                st["ac_nonmono"] += 1
            if p and st["Gcert_runs"] < 60 and L <= 11:
                Np = extend_network(N, L)
                b, e = certify(inst, L + 2, Np, E)
                st["Gcert_runs"] += 1
                if b or e:
                    st["Gcert_bad"] += 1
                    bad.append(("Gcert", inst.q, inst.R, L, b, e))
            prev_pc, prev_ac = p, a
    return seed, st, bad[:5]


if __name__ == "__main__":
    tag, base, count, jobs = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    procs = min(int(sys.argv[5]) if len(sys.argv) > 5 else 6, 8)
    t0 = time.time()
    tot = {}
    out = open("results-G-%s.txt" % tag, "w")
    with Pool(procs) as pool:
        for seed, st, bad in pool.imap_unordered(job, [(base + j, count) for j in range(jobs)]):
            for k, x in st.items():
                tot[k] = tot.get(k, 0) + x
            out.write("seed %d: %s\n" % (seed, st))
            for b in bad:
                out.write("  BAD %r\n" % (b,))
            out.flush()
            print(seed, st, flush=True)
    viol = tot["csp_mismatch"] + tot["pc_not_ac"] + tot["unsound"] + tot["G_viol"] + tot["Gcert_bad"]
    out.write("\nTOTALS (%.0fs): %s\nviolations: %d\n" % (time.time() - t0, tot, viol))
    out.close()
    print(tot, "violations:", viol)
