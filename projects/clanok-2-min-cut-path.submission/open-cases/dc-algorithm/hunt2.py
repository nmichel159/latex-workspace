"""Second adversarial search for false positives of path consistency (PC) on ZZ instances, larger sizes than
hunt_pc.py, fast PC (pcfast.py).

Modes:
  zz      general ZZ (random generating relation + real edges), P2-completed after every mutation; n in [NMIN, NMAX]
  zzfree  the same without P2 (control)
  sw      switch model (sw2.py) with P2 repair, up to 7 bottoms, 7 tops, 12 switches
  swfree  the same without P2 (control)
  rigid   two-choice hypergraphs (dc-hardness/twoch.py form) seeded with the rigid family R_L (L = 3..7) turned into
          no-instances (t moved, nodes deleted), mutated with P2 repair
Score of a 'no' instance: largest window w with AC_w 'yes' (scaled), then largest window with PC_w 'yes'; 'yes'
instances are rejected.  Every PC false positive is written to OUTFILE (JSON lines), with the first 20 AC false
positives.
Usage: python hunt2.py MODE SEED STEPS OUTFILE [NMIN NMAX]"""
import os
import sys
import random
import json
import time

sys.setrecursionlimit(100000)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import zz  # noqa: E402
import sw2  # noqa: E402
import pcfast  # noqa: E402
import hunt_pc  # noqa: E402

NMIN, NMAX = 12, 17


# ------------------------------------------------------------------ general ZZ, larger
def zz_random(rng):
    n = rng.randint(NMIN, NMAX)
    lt = zz.random_order(rng, n, rng.choice([0.05, 0.1, 0.15, 0.2]))
    less = {(a, b) for a in range(n) for b in range(n) if lt[a][b]}
    R = {e for e in less if e != (0, n - 1) and rng.random() < rng.choice([0.1, 0.15, 0.2])}
    return n, less, R


def zz_mutate(rng, st):
    n, less, R = st
    if n >= NMAX:
        # no growth
        for _ in range(10):
            c = hunt_pc.zz_mutate(rng, st)
            if c[0] == n:
                return c
        return st
    return hunt_pc.zz_mutate(rng, st)


# ------------------------------------------------------------------ switch model, larger
def sw_random(rng):
    while True:
        inst = sw2.random_inst(rng, rng.randint(3, 7), rng.randint(3, 7), rng.randint(5, 12),
                               rng.choice([0.0, 0.03, 0.06]), 2, 2)
        inst = hunt_pc.sw_repair(rng, inst)
        if sw2.p2(inst[3], inst[4]):
            return inst


def sw_mutate_raw(rng, inst):
    nb, nt, F, Nb, Nt = inst
    F = list(F)
    Nb, Nt = [set(x) for x in Nb], [set(x) for x in Nt]
    r = rng.random()
    k = len(Nb)
    if r < 0.25 and k:
        s = rng.randrange(k)
        Nb[s] ^= {rng.randrange(nb)}
    elif r < 0.5 and k:
        s = rng.randrange(k)
        Nt[s] ^= {rng.randrange(nt)}
    elif r < 0.65:
        e = (rng.randrange(nb), rng.randrange(nt))
        if e != (0, 0):
            if e in F:
                F.remove(e)
            else:
                F.append(e)
    elif r < 0.75 and k < 12:
        Nb.append({rng.randrange(nb)})
        Nt.append({rng.randrange(nt)})
    elif r < 0.82 and k > 2:
        s = rng.randrange(k)
        del Nb[s]
        del Nt[s]
    elif r < 0.91 and nb < 7:
        nb += 1
    elif nt < 7:
        nt += 1
    return nb, nt, F, [frozenset(x) for x in Nb], [frozenset(x) for x in Nt]


def sw_mutate(rng, inst):
    return hunt_pc.sw_repair(rng, sw_mutate_raw(rng, inst))


# ------------------------------------------------------------------ two-choice hypergraphs (2CH)
def ch_to_sw(inst):
    """2CH (N, E, F, s, t) with bit masks -> switch model.  A node in some E-set (or s) gets a bottom, a node in some
    F-set (or t) gets a top, a node with both gets the fixed edge between them; E-mode of a switch joins bottoms
    (peak mode), F-mode joins tops (valley mode).  u = bottom of s (index 0), v = top of t (index 0)."""
    N, E, F, s, t = inst
    inE = [any((m >> x) & 1 for m in E) or x == s for x in range(N)]
    inF = [any((m >> x) & 1 for m in F) or x == t for x in range(N)]
    border = [s] + [x for x in range(N) if x != s and inE[x]]
    torder = [t] + [x for x in range(N) if x != t and inF[x]]
    bi = {x: i for i, x in enumerate(border)}
    ti = {x: i for i, x in enumerate(torder)}
    Fx = [(bi[x], ti[x]) for x in range(N) if inE[x] and inF[x]]
    Nb = [frozenset(bi[x] for x in range(N) if (E[i] >> x) & 1) for i in range(len(E))]
    Nt = [frozenset(ti[x] for x in range(N) if (F[i] >> x) & 1) for i in range(len(F))]
    return len(border), len(torder), Fx, Nb, Nt


def ch_repair(rng, inst):
    N, E, F, s, t = inst
    E, F = list(E), list(F)
    n = len(E)
    for i in range(n):
        for l in range(i + 1, n):
            if not (E[i] & E[l]) and not (F[i] & F[l]):
                r = rng.random()
                if r < 0.5 and N < 40:
                    z = N
                    N += 1
                else:
                    z = rng.randrange(N)
                if rng.random() < 0.5:
                    E[i] |= 1 << z
                    E[l] |= 1 << z
                else:
                    F[i] |= 1 << z
                    F[l] |= 1 << z
    return N, E, F, s, t


def rigid(L):
    """The rigid family R_L of dc-hardness.md Section 2 (same construction as dc-hardness/rigid.py, re-typed here
    so that nothing is imported from another agent's folder)."""
    names = {}

    def node(name):
        if name not in names:
            names[name] = len(names)
        return names[name]

    path = [0] * (L + 1)
    flip = [0] * (L + 1)
    s, t = node("s"), node("t")
    path[1] |= 1 << s
    path[L] |= 1 << t
    for k in range(1, L):
        y = node(("y", k))
        path[k] |= 1 << y
        path[k + 1] |= 1 << y
    for p in range(1, L + 1):
        for q in range(p + 1, L + 1):
            if (q - p) % 2 == 1:
                x = node(("z", p, q))
                flip[p] |= 1 << x
                path[q] |= 1 << x
            else:
                x = node(("w", p, q))
                flip[p] |= 1 << x
                flip[q] |= 1 << x
    E, F = [0] * L, [0] * L
    for k in range(1, L + 1):
        if k % 2 == 1:
            E[k - 1], F[k - 1] = path[k], flip[k]
        else:
            F[k - 1], E[k - 1] = path[k], flip[k]
    return len(names), E, F, s, t


def rigid_seed(rng):
    L = rng.randint(3, 7)
    N, E, F, s, t = rigid(L)
    E, F = list(E), list(F)
    r = rng.random()
    if r < 0.5:
        # move t into a random set (other than the last path set)
        for i in range(L):
            E[i] &= ~(1 << t)
            F[i] &= ~(1 << t)
        i = rng.randrange(L)
        if rng.random() < 0.5:
            E[i] |= 1 << t
        else:
            F[i] |= 1 << t
    else:
        # delete a random y node from its sets
        x = rng.randrange(N)
        if x not in (s, t):
            for i in range(L):
                E[i] &= ~(1 << x)
                F[i] &= ~(1 << x)
    return ch_repair(rng, (N, E, F, s, t))


def ch_mutate(rng, inst):
    N, E, F, s, t = inst
    E, F = list(E), list(F)
    n = len(E)
    r = rng.random()
    if r < 0.35:
        i = rng.randrange(n)
        E[i] ^= 1 << rng.randrange(N)
    elif r < 0.7:
        i = rng.randrange(n)
        F[i] ^= 1 << rng.randrange(N)
    elif r < 0.8 and n < 10:
        E.append(1 << rng.randrange(N))
        F.append(1 << rng.randrange(N))
    elif r < 0.85 and n > 2:
        i = rng.randrange(n)
        del E[i]
        del F[i]
    elif r < 0.92 and N < 40:
        N += 1
    else:
        # move t or s
        x = rng.randrange(N)
        if rng.random() < 0.5 and x != s:
            t = x
        elif x != t:
            s = x
    if s == t:
        return inst
    return ch_repair(rng, (N, E, F, s, t))


# ------------------------------------------------------------------ scoring
def window_score(z, fn, Lmax):
    lo, hi = -1, Lmax
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if fn(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


def score(z, want_pc, limit=2000000):
    try:
        ex, _ = zz.exact_dfs(z, limit=limit)
    except RuntimeError:
        return None, "limit"
    if ex:
        return None, "yes"
    L = z.n if z.n % 2 else z.n - 1
    csp = zz.CSP(z)

    def acw(w):
        csp.window = w
        return zz.arc_consistency(csp, csp.init_domains()) is not None
    w = window_score(z, acw, L)
    if w < L:
        return 100 * w // max(L, 1), "ac-no"
    if not want_pc:
        return 10000, "ac-fp"
    wp = window_score(z, lambda w: pcfast.pc_answer(z, window=w), L)
    if wp < L:
        return 10000 + 100 * wp // max(L, 1), "ac-fp"
    return 100000, "pc-fp"


def main():
    global NMIN, NMAX
    mode, seed, steps, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    if len(sys.argv) > 6:
        NMIN, NMAX = int(sys.argv[5]), int(sys.argv[6])
    rng = random.Random(seed)
    if mode == "zz":
        rnd, mut, build = zz_random, zz_mutate, hunt_pc.zz_build
    elif mode == "zzfree":
        rnd, mut, build = zz_random, zz_mutate, lambda rng, s: hunt_pc.zz_build(rng, s, p2=False)
    elif mode == "sw":
        rnd, mut, build = sw_random, sw_mutate, lambda rng, s: zz.from_sw(*s)
    elif mode == "swfree":
        rnd, mut, build = sw_random, sw_mutate_raw, lambda rng, s: zz.from_sw(*s)
    elif mode == "rigid":
        rnd, mut, build = rigid_seed, ch_mutate, lambda rng, s: zz.from_sw(*ch_to_sw(s))
    else:
        raise SystemExit("unknown mode")
    found = {"ac-fp": 0, "pc-fp": 0, "no": 0, "evals": 0}
    cur, cur_score, since = None, -1, 0
    t0 = time.time()
    for step in range(steps):
        if cur is None or since > 300:
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
        found["evals"] += 1
        since += 1
        if sc is None:
            continue
        found["no"] += 1
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
        if step % 500 == 0:
            print(step, found, "%.0fs" % (time.time() - t0), flush=True)
    print(mode, seed, found, "%.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
