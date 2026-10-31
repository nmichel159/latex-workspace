"""Adversarial and random checks of r5-core.md Section 8 (own code).

usage:
  python adv8.py rigid SEED COUNT NMIN NMAX [LOG]     rigid-word designs with many X/Y extras (several levels)
  python adv8.py layered SEED COUNT NMIN NMAX [LOG]   designs built to force several levels (S_i of size about theta)
  python adv8.py random SEED COUNT MMIN MMAX [LOG]    random general switch-form instances (brute force, all paths)
  python adv8.py hill SEED RESTARTS STEPS NMIN NMAX [LOG]  hill climbing on the number of levels (proof mode)

On every path: Lemma 6.3 bound, proof8.levels in mode 'proof' (adversarial cover choice and first cover) and mode
'stress'; the final intersection is tested in the switch form and in the ZZ realisation (zzl.sw_to_zz).  Rigid
designs: the rigidity certificate (gen8.rigid_certificate) and, for n <= 14, the exact list of shortest valid paths.
Every failure is saved as JSON in runs/fail/; designs with at least 3 levels in runs/deep/.
"""
import sys
import os
import json
import time
import random
from collections import Counter
from zzl import SW, Skel, bits, popcount, all_shortest_valid_paths, sw_to_zz, zz_connects, kparam, Budget
import gen8
import proof8

HERE = os.path.dirname(os.path.abspath(__file__))


def dump(I, P, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    d = {"m": I.m, "le": [[int(b) for b in row] for row in I.le], "E": [hex(x) for x in I.E],
         "F": [hex(x) for x in I.F], "s": I.s, "t": I.t,
         "nn": I.nn, "me": I.me, "P": P}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f)


def load(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    conv = lambda x: int(x, 16) if isinstance(x, str) else x
    I = SW(d["m"], [[bool(b) for b in row] for row in d["le"]], [conv(x) for x in d["E"]],
           [conv(x) for x in d["F"]], d["s"], d["t"], d["nn"],
           [tuple(x) for x in d["me"]])
    return I, [tuple(x) for x in d["P"]]


def zz_check_D(I, D, zzc):
    q, u, v, le, R, swi, bott = zzc
    if le is not None and bott != sum(1 << a for a in range(q) if le[a][u]):
        raise RuntimeError("bottoms of the realisation inconsistent")
    Df = bott
    for i in bits(D):
        Df |= 1 << swi[i]
    return zz_connects(q, u, v, R, Df)


def privacy_violations(I):
    """Private nodes of middle edges z v must lie only in F_z and E_v."""
    priv = {p: (z, v) for (z, v, p) in I.me}
    viol = 0
    for w in range(I.m):
        for ty, side in ((0, I.E[w]), (1, I.F[w])):
            for nd in bits(side):
                if nd in priv:
                    z, v = priv[nd]
                    if not ((ty == 1 and w == z) or (ty == 0 and w == v)):
                        viol += 1
    return viol


def run_path(I, P, st, tag, zzc=None, save_prefix=None):
    Sk = Skel(I, P)
    proof8.lemma63_check(I, Sk, st)
    nb = 0
    for x in bits(Sk.NF_ & ~Sk.A):
        for y in bits(Sk.NE_ & ~Sk.B):
            if I.le[y][x] and not I.le[x][y]:
                nb += 1
    st["bad pairs"] += nb
    st["max bad pairs on a path"] = max(st["max bad pairs on a path"], nb)
    st["max |A|"] = max(st["max |A|"], popcount(Sk.A))
    res = {}
    for mode, pick in (("proof", "adversarial"), ("proof", "first"), ("proof", "sample"), ("stress", "adversarial")):
        before = sum(v for k2, v in st.items() if k2.endswith("FAIL"))
        D, terms, nlev, status = proof8.levels(I, Sk, mode, st, ccap=40, pick=pick)
        key = "%s/%s" % (mode, pick)
        res[key] = nlev
        st["max levels %s" % key] = max(st["max levels %s" % key], nlev)
        if status == "final" and zzc is not None:
            if not zz_check_D(I, D, zzc):
                st["FINAL D DOES NOT CONNECT IN ZZ FAIL"] += 1
        if status == "error":
            st["PROOF ERROR FAIL"] += 1
        after = sum(v for k2, v in st.items() if k2.endswith("FAIL"))
        if after > before and save_prefix:
            dump(I, P, os.path.join(HERE, "runs", "fail", "%s-%s.json" % (save_prefix, key.replace("/", "-"))))
            st["saved failures"] += 1
    return res


def words(rng, n):
    r = rng.random()
    if r < 0.4:
        return "".join("EF"[i % 2] for i in range(n))
    if r < 0.6:
        return "".join("FE"[i % 2] for i in range(n))
    w = [rng.choice("EF") for _ in range(n)]
    if "E" not in w:
        w[0] = "E"
    if "F" not in w:
        w[-1] = "F"
    return "".join(w)


def gen_rigid(rng, n, layered=False):
    word = words(rng, n)
    nE = word.count("E")
    m_guess = n + 2 * max(2, n // 4)
    k, N = kparam(m_guess)
    theta = max(1, nE // (2 * k))
    if layered:
        nx = rng.randint(2, max(2, k + 2))
        ny = rng.randint(2, max(2, k + 2))
        smax = theta + rng.randint(0, 1)
        sfix = []
        E_idx = list(range(nE))
        rng.shuffle(E_idx)
        for i in range(nx):
            sz = max(1, min(theta, nE))
            sfix.append(E_idx[(i * sz) % nE:(i * sz) % nE + sz] or [E_idx[0]])
        return gen8.rigid_design(rng, word, nx, ny, smax, rng.randint(1, 3), pbad=rng.choice([0.3, 0.6, 1.0]),
                                 pchain=rng.choice([0.0, 0.0, 0.1]), ptie_ex=rng.choice([0.0, 0.0, 0.2]),
                                 ptie_mem=rng.choice([0.0, 0.0, 0.1]), pme=rng.choice([0.0, 0.05, 0.2]),
                                 hub=rng.random() < 0.3, sfix=sfix)
    nx = rng.randint(1, max(2, n // 3))
    ny = rng.randint(1, max(2, n // 3))
    return gen8.rigid_design(rng, word, nx, ny, rng.randint(1, max(1, theta + 1)), rng.randint(1, 3),
                             pbad=rng.choice([0.2, 0.5, 0.8, 1.0]), pchain=rng.choice([0.0, 0.1, 0.3]),
                             ptie_ex=rng.choice([0.0, 0.1, 0.3]), ptie_mem=rng.choice([0.0, 0.05, 0.15]),
                             pme=rng.choice([0.0, 0.05, 0.2, 0.5]), hub=rng.random() < 0.3)


def main():
    mode = sys.argv[1]
    st = Counter()
    t0 = time.time()
    logp = None
    if mode in ("rigid", "layered", "random", "deep"):
        seed, count, lo, hi = map(int, sys.argv[2:6])
        logp = sys.argv[6] if len(sys.argv) > 6 else None
    elif mode == "hill":
        seed, restarts, steps, lo, hi = map(int, sys.argv[2:7])
        logp = sys.argv[7] if len(sys.argv) > 7 else None
    logf = open(logp, "a", encoding="utf-8") if logp else None

    def out(s):
        print(s, flush=True)
        if logf:
            logf.write(s + "\n")
            logf.flush()
    out("adv8 %s args=%s pid=%d" % (mode, " ".join(sys.argv[2:]), os.getpid()))
    rng = random.Random(seed)
    if mode in ("rigid", "layered"):
        done = 0
        tries = 0
        while done < count:
            tries += 1
            n = rng.randint(lo, hi)
            g = gen_rigid(rng, n, layered=(mode == "layered"))
            if g is None:
                st["designs rejected (planted path invalid)"] += 1
                continue
            I, P, info = g
            bad = gen8.rigid_certificate(I, P, info)
            if bad:
                st["RIGIDITY CERTIFICATE FAIL"] += 1
                out("certificate: %s" % bad[:3])
                continue
            if not I.p2_switch():
                st["DESIGN WITHOUT P2 FAIL"] += 1
                continue
            if privacy_violations(I):
                st["PRIVATE NODE IN A THIRD SIDE FAIL"] += 1
                continue
            done += 1
            st["designs"] += 1
            st["max m"] = max(st["max m"], I.m)
            if n <= 14:
                r, paths = all_shortest_valid_paths(I, cap=5)
                if r != len(P) or len(paths) != 1 or [tuple(x) for x in paths[0]] != P:
                    st["PLANTED PATH NOT THE UNIQUE SHORTEST FAIL"] += 1
                else:
                    st["planted path unique shortest (exact search, n<=14)"] += 1
            zzc = sw_to_zz(I)
            if not zz_check_D(I, I.dnc(sum(1 << w for (w, ty) in P if ty == 1)), zzc):
                st["PLANTED SOLUTION NOT A ZZ SOLUTION FAIL"] += 1
            res = run_path(I, P, st, mode, zzc, "%s-%d-%d" % (mode, seed, done))
            if res["proof/adversarial"] >= 3 or res["stress/adversarial"] >= 4:
                dump(I, P, os.path.join(HERE, "runs", "deep", "%s-%d-%d.json" % (mode, seed, done)))
                st["saved deep designs"] += 1
            if done % 20 == 0:
                out("  %d designs, %.0fs, levels max proof/adv %d, proof/first %d, stress %d" % (
                    done, time.time() - t0, st["max levels proof/adversarial"], st["max levels proof/first"],
                    st["max levels stress/adversarial"]))
    elif mode == "deep":
        # lo = L (levels targeted), hi = k; count designs with random perturbations
        L, kk = lo, hi
        for it in range(count):
            pert = it % 4
            g = gen8.deep_design(rng, L, kk, ny=kk + rng.randint(0, 3),
                                 ptie_ex=0.15 if pert == 1 else 0.0, ptie_mem=0.1 if pert == 2 else 0.0,
                                 pme=0.1 if pert == 3 else 0.0, hub=rng.random() < 0.5,
                                 extra_x=rng.randint(0, 3) if pert else 0)
            if g is None:
                st["designs rejected (planted path invalid)"] += 1
                continue
            I, P, info = g
            if kparam(I.m)[0] != kk:
                st["deep design with other k"] += 1
            bad = gen8.rigid_certificate(I, P, info)
            if bad or not I.p2_switch() or privacy_violations(I):
                st["DEEP DESIGN INVALID FAIL"] += 1
                continue
            st["designs"] += 1
            st["max m"] = max(st["max m"], I.m)
            zzc = sw_to_zz(I)
            if not zz_check_D(I, I.dnc(sum(1 << w for (w, ty) in P if ty == 1)), zzc):
                st["PLANTED SOLUTION NOT A ZZ SOLUTION FAIL"] += 1
            res = run_path(I, P, st, mode, zzc, "deep-%d-%d" % (seed, it))
            st["deep pert %d levels proof/adv=%d" % (pert, res["proof/adversarial"])] += 1
            if res["proof/adversarial"] >= 3:
                dump(I, P, os.path.join(HERE, "runs", "deep", "deep-L%d-k%d-%d-%d.json" % (L, kk, seed, it)))
                st["saved deep designs"] += 1
            out("  design %d m=%d k=%d levels %s %.0fs" % (it, I.m, kparam(I.m)[0], res, time.time() - t0))
    elif mode == "random":
        for it in range(count):
            m = rng.randint(lo, hi)
            I = gen8.random_sw(rng, m, rng.randint(2, 2 * m), rng.choice([0.08, 0.15, 0.25]),
                               rng.choice([0.1, 0.25, 0.4]), rng.choice([0.0, 0.1, 0.3]),
                               rng.choice([0.0, 0.1, 0.3]))
            st["instances"] += 1
            if not I.p2_switch():
                st["RANDOM WITHOUT P2 FAIL"] += 1
                continue
            if privacy_violations(I):
                st["PRIVATE NODE IN A THIRD SIDE FAIL"] += 1
                continue
            yes = None
            zzc = sw_to_zz(I)
            if m <= 12:
                yes = False
                for D in I.downsets():
                    a = I.connects(D)
                    if a != zz_check_D(I, D, zzc):
                        st["SWITCH FORM != ZZ REALISATION FAIL"] += 1
                    yes = yes or a
            try:
                r, paths = all_shortest_valid_paths(I, cap=12, budget=300000)
            except Budget:
                st["skipped: path search over budget"] += 1
                continue
            if yes is not None and yes != (r is not None):
                st["VALID PATH EXISTS != BRUTE FORCE FAIL"] += 1
            if r is None:
                st["no"] += 1
                continue
            st["yes"] += 1
            for P in paths:
                st["paths"] += 1
                run_path(I, [tuple(x) for x in P], st, "random", zzc, "random-%d-%d" % (seed, it))
            if (it + 1) % 200 == 0:
                out("  %d instances, %.0fs" % (it + 1, time.time() - t0))
    elif mode == "hill":
        best_overall = 0
        for rs in range(restarts):
            n = rng.randint(lo, hi)
            cur = None
            cur_score = -1
            seedr = rng.randrange(1 << 30)
            for step in range(steps):
                r2 = random.Random(seedr + step * 7919)
                g = gen_rigid(r2, n, layered=r2.random() < 0.7)
                if g is None:
                    continue
                I, P, info = g
                if gen8.rigid_certificate(I, P, info) or not I.p2_switch():
                    st["HILL DESIGN INVALID FAIL"] += 1
                    continue
                st["designs"] += 1
                zzc = sw_to_zz(I)
                res = run_path(I, P, st, "hill", zzc, "hill-%d-%d-%d" % (seed, rs, step))
                sc = res["proof/adversarial"] * 100 + res["proof/first"]
                if sc > cur_score:
                    cur_score = sc
                    cur = (I, P)
                    if res["proof/adversarial"] >= 3:
                        dump(I, P, os.path.join(HERE, "runs", "deep", "hill-%d-%d-%d.json" % (seed, rs, step)))
                        st["saved deep designs"] += 1
            best_overall = max(best_overall, cur_score)
            out("  restart %d n=%d best score %d (levels proof/adv*100 + proof/first) %.0fs" % (
                rs, n, cur_score, time.time() - t0))
    out("SUMMARY adv8 %s %s (%.0fs)" % (mode, " ".join(sys.argv[2:]), time.time() - t0))
    for key in sorted(st):
        out("  %s: %d" % (key, st[key]))
    fails = [key for key in st if key.endswith("FAIL") and st[key]]
    out("FAILURES: %s" % (", ".join(fails) if fails else "none"))
    if logf:
        logf.close()


if __name__ == "__main__":
    main()
