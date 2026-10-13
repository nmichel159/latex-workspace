"""Adversarial search for false positives of the AC and PC relaxations (zz.py) on ZZ + P2 instances.

Search space (mode 'sw'): switch-model instances (sw2.py) with P2; (mode 'zz'): general ZZ instances given by a
generating relation and real edges, P2-completed after every mutation.
Score of a 'no' instance: values surviving arc consistency (propagation continued after a wipe-out), plus a large
bonus when AC says 'yes', plus the surviving PC pairs when PC is run.  'yes' instances are rejected.
Hill climbing with restarts; every AC / PC false positive found is printed and appended to the output file.
Usage: python hunt_pc.py MODE SEED STEPS OUTFILE"""
import os
import sys
import random
import json

sys.setrecursionlimit(100000)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import zz  # noqa: E402
import sw2  # noqa: E402


def ac_survival(csp):
    L = csp.L
    doms = csp.init_domains()
    changed = True
    while changed:
        changed = False
        for j in range(L):
            for k in range(L):
                if j == k:
                    continue
                keep = 0
                dk = doms[k]
                for i in zz.bits(doms[j]):
                    if csp.rel(j, k, i) & dk:
                        keep |= 1 << i
                if keep != doms[j]:
                    doms[j] = keep
                    changed = True
    return sum(bin(d).count("1") for d in doms), all(doms)


# ---------------------------------------------------------------- switch model
def sw_random(rng):
    while True:
        inst = sw2.random_inst(rng, rng.randint(2, 5), rng.randint(2, 5), rng.randint(3, 7), 0.1, 3, 3)
        if sw2.p2(inst[3], inst[4]):
            return inst


def sw_repair(rng, inst):
    nb, nt, F, Nb, Nt = inst
    Nb, Nt = [set(x) for x in Nb], [set(x) for x in Nt]
    k = len(Nb)
    for a in range(k):
        for b in range(a + 1, k):
            if not (Nb[a] & Nb[b]) and not (Nt[a] & Nt[b]):
                if rng.random() < 0.5:
                    x = rng.randrange(nb)
                    Nb[a].add(x)
                    Nb[b].add(x)
                else:
                    x = rng.randrange(nt)
                    Nt[a].add(x)
                    Nt[b].add(x)
    return nb, nt, F, [frozenset(x) for x in Nb], [frozenset(x) for x in Nt]


def sw_mutate(rng, inst):
    return sw_repair(rng, sw_mutate_raw(rng, inst))


def sw_mutate_raw(rng, inst):
    nb, nt, F, Nb, Nt = inst
    F = list(F)
    Nb, Nt = [set(x) for x in Nb], [set(x) for x in Nt]
    r = rng.random()
    k = len(Nb)
    if r < 0.25 and k:
        s = rng.randrange(k)
        x = rng.randrange(nb)
        Nb[s] ^= {x}
    elif r < 0.5 and k:
        s = rng.randrange(k)
        x = rng.randrange(nt)
        Nt[s] ^= {x}
    elif r < 0.65:
        e = (rng.randrange(nb), rng.randrange(nt))
        if e != (0, 0):
            if e in F:
                F.remove(e)
            else:
                F.append(e)
    elif r < 0.75 and k < 8:
        Nb.append({rng.randrange(nb)})
        Nt.append({rng.randrange(nt)})
    elif r < 0.82 and k > 2:
        s = rng.randrange(k)
        del Nb[s]
        del Nt[s]
    elif r < 0.91 and nb < 5:
        nb += 1
    elif nt < 5:
        nt += 1
    Nb = [frozenset(x) for x in Nb]
    Nt = [frozenset(x) for x in Nt]
    return nb, nt, F, Nb, Nt


def sw_mutate_free(rng, inst):
    """as sw_mutate, without the P2 repair (control)"""
    return sw_mutate_raw(rng, inst)


def sw_to_zz(inst):
    return zz.from_sw(*inst)


# ---------------------------------------------------------------- general ZZ
def zz_random(rng):
    n = rng.randint(7, 11)
    lt = zz.random_order(rng, n, rng.choice([0.1, 0.2]))
    less = {(a, b) for a in range(n) for b in range(n) if lt[a][b]}
    R = {e for e in less if e != (0, n - 1) and rng.random() < 0.25}
    return n, less, R


def zz_build(rng, st, p2=True):
    n, less, R = st
    try:
        lt = zz.closure(n, less)
    except AssertionError:
        return None
    R = {e for e in R if lt[e[0]][e[1]] and e != (0, n - 1)}
    if p2:
        R = zz.p2_complete(rng, n, lt, R)
    return zz.ZZ(n, lt, R)


def zz_mutate(rng, st):
    n, less, R = st
    less, R = set(less), set(R)
    r = rng.random()
    a, b = rng.sample(range(1, n - 1), 2) if n > 3 else (0, n - 1)
    if r < 0.35:
        less ^= {(a, b)}
    elif r < 0.85:
        R ^= {(a, b)}
        if rng.random() < 0.3:
            R ^= {(0, a)}
        if rng.random() < 0.3:
            R ^= {(a, n - 1)}
    elif n < 13:
        x = n - 1
        n2 = n + 1
        # new element n-1, v becomes n
        less = {(p, q if q != x else n2 - 1) for p, q in less}
        less = {(p if p != x else n2 - 1, q) for p, q in less}
        R = {(p if p != x else n2 - 1, q if q != x else n2 - 1) for p, q in R}
        less |= {(0, x), (x, n2 - 1)}
        n = n2
    return n, less, R


# ---------------------------------------------------------------- search
def ac_window_score(z):
    """largest window w (0..L) such that AC of the window-w CSP says yes; -1 if none."""
    csp = zz.CSP(z)
    lo, hi = -1, csp.L
    # AC_w is monotone in w (more constraints for larger w)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        csp.window = mid
        if zz.arc_consistency(csp, csp.init_domains()) is not None:
            lo = mid
        else:
            hi = mid - 1
    return lo, csp.L


def score(z, want_pc):
    ex, _ = zz.exact_dfs(z)
    if ex:
        return None, "yes"
    w, L = ac_window_score(z)
    surv = 100 * w // max(L, 1)
    ac_yes = w >= L
    if not ac_yes:
        return surv, "ac-no"
    if not want_pc:
        return 10000, "ac-fp"
    wp, L = pc_window_score(z)
    if wp < L:
        return 10000 + 100 * wp // max(L, 1), "ac-fp"
    return 100000, "pc-fp"


def pc_window_score(z):
    """largest window w such that PC of the window-w CSP says yes (PC_w is monotone in w)."""
    lo, hi = -1, (z.n if z.n % 2 else z.n - 1)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if pc_window(z, mid):
            lo = mid
        else:
            hi = mid - 1
    return lo, (z.n if z.n % 2 else z.n - 1)


def pc_window(z, w):
    orig = zz.CSP.window
    zz.CSP.window = w
    try:
        return zz.pc_numpy(z)
    finally:
        zz.CSP.window = orig


def main():
    mode, seed, steps, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    rng = random.Random(seed)
    if mode == "sw":
        rnd, mut, build = sw_random, sw_mutate, lambda rng, s: sw_to_zz(s)
    elif mode == "swfree":
        rnd, mut, build = sw_random, sw_mutate_free, lambda rng, s: sw_to_zz(s)
    elif mode == "zzfree":
        rnd, mut, build = zz_random, zz_mutate, lambda rng, s: zz_build(rng, s, p2=False)
    else:
        rnd, mut, build = zz_random, zz_mutate, zz_build
    found = {"ac-fp": 0, "pc-fp": 0}
    cur = None
    cur_score = -1
    since = 0
    for step in range(steps):
        if cur is None or since > 400:
            cur = rnd(rng)
            z = build(rng, cur)
            if z is None:
                cur = None
                continue
            sc, kind = score(z, False)
            cur_score = -1 if sc is None else sc
            since = 0
        cand = mut(rng, cur)
        z = build(rng, cand)
        if z is None:
            continue
        sc, kind = score(z, cur_score >= 10000)
        since += 1
        if sc is None:
            continue
        if kind in ("ac-fp", "pc-fp"):
            found[kind] += 1
            if kind == "pc-fp" or found["ac-fp"] <= 20:
                rec = {"mode": mode, "seed": seed, "step": step, "kind": kind, "n": z.n, "u": z.u, "v": z.v,
                       "le": [[int(x) for x in row] for row in z.le], "R": z.R}
                with open(out, "a") as f:
                    f.write(json.dumps(rec) + "\n")
            if kind == "pc-fp":
                print("PC false positive at step", step, "n =", z.n, flush=True)
        if sc >= cur_score:
            if sc > cur_score:
                since = 0
            cur, cur_score = cand, sc
    print(mode, seed, found)


if __name__ == "__main__":
    main()
