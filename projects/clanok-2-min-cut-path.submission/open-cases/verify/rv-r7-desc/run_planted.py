"""Referee rv-r7-desc: large planted instances that reach Stage 1 and the shapes.  Usage: run_planted.py SEED BASE ROUNDS MOVES LOG.
BASE in: B (all non-strict), A (few non-strict with the early a), stair (staircase strict pairs with E-contacts to core a), ties, mix
(R_0 and C_0 positions interleaved), small (few classes of R_0: Case II as written), cegis (random layout, shortcuts blocked by strict
pairs).  Every instance: P2 asserted, P verified shortest by the exact solver; run on P, on P reversed, on the reversed instance, on both.
Then MOVES random perturbations, each kept only if P2 holds and P stays shortest; targeted attacks on the claim of Shape B are among them.
"""
import os
import random
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from swf import ClaimFail, Budget, path_rev, path_op  # noqa: E402
from proof import run_all  # noqa: E402
from design import Design, zipper  # noqa: E402

BUDGET = 400_000


def h_positions(d):
    return d.info["H"]


def base_B(rng):
    return zipper(rng.randint(24, 34), rng.randint(30, 38))


def base_A(rng):
    p, q = rng.randint(26, 34), rng.randint(14, 30)
    k = rng.randint(1, 12)
    nonstrict = set(rng.sample(range(q), k))
    cut = rng.randint(22, p)
    return zipper(p, q, seed_strict=lambda i, j: i < cut and j not in nonstrict,
                  contact_a=(None if rng.random() < 0.5 else (lambda i, j: not (i < cut and j not in nonstrict))))


def base_stair(rng):
    p, q = rng.randint(26, 34), rng.randint(30, 38)
    sigma = [rng.randint(0, p // 2) if rng.random() < 0.8 else rng.randint(0, p - 1) for _ in range(q)]
    d = zipper(p, q, seed_strict=lambda i, j: i < sigma[j])
    Apos = d.info["Apos"]
    for j, (x, y) in enumerate(d.info["H"]):
        for z in (x, y):
            d.T[z].add(Apos[sigma[j]])
    return d


def base_ties(rng):
    d = base_stair(rng) if rng.random() < 0.5 else base_B(rng)
    Apos = d.info["Apos"]
    H = d.info["H"]
    for _ in range(rng.randint(1, len(Apos) // 3)):
        x, y = rng.sample(Apos, 2)
        d.tie(x, y)
    for _ in range(rng.randint(1, len(H) // 4)):
        (x, _a), (y, _b) = rng.sample(H, 2)
        d.tie(x, y)
    return d


def base_mix(rng):
    """R_0 and C_0 positions interleaved: each a has a member left of f_0 and a member in a zone M; each h has members x', x'' around
    its member of M, then x, v, y further right."""
    p, q = rng.randint(22, 28), rng.randint(26, 32)
    naux = 12
    d = Design()
    d.fill("F", 2)
    aux = d.add("E")
    Astar = [aux] + [d.add("E", cls=d.cls[aux - 1]) for _ in range(naux - 1)]
    auxc = d.cls[aux - 1]
    d.fill("F", 1)
    e0 = d.add("E")
    d.fill("F", 6)
    Apos = [d.add("E") for _ in range(p)]
    d.fill("F", 6)
    f0 = d.add("F")
    d.fill("E", 6)
    x1s = {}
    z1s = {}
    order = list(range(max(p, q)))
    M_a = {}
    n_mid = min(p, q)
    perm = list(range(p))
    rng.shuffle(perm)
    for k in range(n_mid):
        x1 = d.add("F")
        am = d.add("E", cls=d.cls[Apos[perm[k]] - 1])
        x2 = d.add("F", cls=d.cls[x1 - 1])
        x1s[k] = (x1, x2)
        M_a[k] = am
    d.fill("E", 6)
    H, Vs = [], []
    for j in range(q):
        if j < n_mid:
            x = d.add("F", cls=d.cls[x1s[j][0] - 1])
        else:
            x = d.add("F")
        v = d.add("E", cls=auxc)
        y = d.add("F", cls=d.cls[x - 1])
        H.append((x, y))
        Vs.append(v)
    d.fill("E", 6)
    f1 = d.add("F")
    b0 = d.add("F")
    Bstar = [b0] + [d.add("F", cls=d.cls[b0 - 1]) for _ in range(naux - 1)]
    d.fill("F", 3)
    allh = [z for pr in H for z in pr] + [z for pr in x1s.values() for z in pr]
    Aall = Apos + list(M_a.values())
    for a in Astar + Vs + [e0]:
        d.S[a] = set(allh)
    for a in Aall:
        d.S[a] = {f0, f1} | set(allh)
    d.T[f0] = {e0}
    d.T[f1] = {e0}
    for b in Bstar:
        d.T[b] = set(Aall)
    for j, (x, y) in enumerate(H):
        d.T[x] = {e0, Vs[j]}
        d.T[y] = {e0, Vs[j]}
        if j in x1s:
            d.T[x1s[j][0]] = {e0, Vs[j], M_a[j]}
            d.T[x1s[j][1]] = {e0, Vs[j], M_a[j]}
            d.T[x] |= {M_a[j]}
            d.T[y] |= {M_a[j]}
    allb = [f0, f1] + allh + Bstar
    for b in allb:
        for a in Astar + [e0]:
            d.set_strict(b, a)
    for a in Apos:
        for b in [f0, f1] + Bstar:
            d.set_strict(b, a)
    d.info = {"Apos": Aall, "H": H + list(x1s.values()), "Vs": Vs, "e0": e0, "f0": f0, "f1": f1, "Astar": Astar, "Bstar": Bstar}
    return d


def base_cross(rng):
    """Classes a_k = {a^L_k, a^Z_k} touched completely by h_k: a^L_k early in the left zone (h_k strictly below the a_i with i < k), a^Z_k
    sandwiched between two members of h_k in the zone M; singletons c_i right of all a^L_k form kappa.  One pair (h_i, h_j) keeps a_i, a_j;
    only the second pair of Shape B removes them."""
    n, mc, q0 = rng.randint(22, 28), rng.randint(22, 26), rng.randint(6, 12)
    naux = 12
    d = Design()
    d.fill("F", 2)
    aux = d.add("E")
    Astar = [aux] + [d.add("E", cls=d.cls[aux - 1]) for _ in range(naux - 1)]
    auxc = d.cls[aux - 1]
    d.fill("F", 1)
    e0 = d.add("E")
    d.fill("F", 6)
    aL = [d.add("E") for _ in range(n)]
    cs = [d.add("E") for _ in range(mc)]
    d.fill("F", 6)
    f0 = d.add("F")
    d.fill("E", 6)
    aZ, xs = [], []
    for k in range(n):
        x1 = d.add("F")
        am = d.add("E", cls=d.cls[aL[k] - 1])
        x2 = d.add("F", cls=d.cls[x1 - 1])
        aZ.append(am)
        xs.append((x1, x2))
    d.fill("E", 6)
    H, Vs = [], []
    for j in range(n + q0):
        x = d.add("F") if j >= n else d.add("F", cls=d.cls[xs[j][0] - 1])
        v = d.add("E", cls=auxc)
        y = d.add("F", cls=d.cls[x - 1])
        H.append((x, y))
        Vs.append(v)
    d.fill("E", 6)
    f1 = d.add("F")
    b0 = d.add("F")
    Bstar = [b0] + [d.add("F", cls=d.cls[b0 - 1]) for _ in range(naux - 1)]
    d.fill("F", 3)
    allh = [z for pr in H for z in pr] + [z for pr in xs for z in pr]
    Aall = aL + cs + aZ
    for a in Astar + Vs + [e0]:
        d.S[a] = set(allh)
    for a in Aall:
        d.S[a] = {f0, f1} | set(allh)
    d.T[f0] = {e0}
    d.T[f1] = {e0}
    for b in Bstar:
        d.T[b] = set(Aall)
    for j, (x, y) in enumerate(H):
        d.T[x] = {e0, Vs[j]}
        d.T[y] = {e0, Vs[j]}
        if j < n:
            for z in (x, y, xs[j][0], xs[j][1]):
                d.T[z] = {e0, Vs[j], aL[j], aZ[j]}
            for i in range(j):
                d.set_strict(x, aL[i])
    allb = [f0, f1] + allh + Bstar
    for b in allb:
        for a in Astar + [e0]:
            d.set_strict(b, a)
    for a in aL + cs:
        for b in [f0, f1] + Bstar:
            d.set_strict(b, a)
    d.info = {"Apos": Aall, "H": H + xs, "Vs": Vs, "e0": e0, "f0": f0, "f1": f1, "Astar": Astar, "Bstar": Bstar}
    return d


def base_allstrict(rng):
    """Tie-free path, the regime of Theorem A: core a left, core h right, every pair strict, far contacts at e_0, e*, f_0, f_1.  The auxiliary
    E-members are singletons above all F-members and the auxiliary F-members singletons below all E-members."""
    p, q, naux = rng.randint(30, 40), rng.randint(30, 40), 12
    d = Design()
    d.fill("F", 2)
    Astar = [d.add("E") for _ in range(naux)]
    d.fill("F", 1)
    e0 = d.add("E")
    d.fill("F", 6)
    Apos = [d.add("E") for _ in range(p)]
    d.fill("F", 6)
    f0 = d.add("F")
    d.fill("E", 6)
    es = d.add("E")
    d.fill("E", 6)
    Hs = [d.add("F") for _ in range(q)]
    d.fill("E", 6)
    f1 = d.add("F")
    Bstar = [d.add("F") for _ in range(naux)]
    d.fill("F", 3)
    for a in Astar + [e0, es]:
        d.S[a] = set(Hs)
    for a in Apos:
        d.S[a] = {f0, f1} | set(Hs)
    d.T[f0] = {e0}
    d.T[f1] = {e0}
    for b in Bstar:
        d.T[b] = set(Apos)
    for b in Hs:
        d.T[b] = {e0, es}
    allb = [f0, f1] + Hs + Bstar
    for b in allb:
        for a in Astar + [e0, es] + Apos:
            d.set_strict(b, a)
    d.info = {"Apos": Apos, "H": [(b, b) for b in Hs], "Vs": [], "e0": e0, "f0": f0, "f1": f1, "Astar": Astar, "Bstar": Bstar}
    return d


def base_small(rng):
    return zipper(rng.randint(11, 24), rng.randint(24, 34))


def base_cegis(rng):
    """Random layout with full contacts; shorter walks are blocked by strict pairs or by removing a contact."""
    naux = 12
    d = Design()
    d.fill("F", 2)
    aux = d.add("E")
    Astar = [aux] + [d.add("E", cls=d.cls[aux - 1]) for _ in range(naux - 1)]
    auxc = d.cls[aux - 1]
    d.fill("F", 1)
    e0 = d.add("E")
    d.fill("F", 6)
    na, nh = rng.randint(14, 30), rng.randint(14, 30)
    ca = [None] * na
    typs = ["a"] * na + ["h"] * nh + ["v"] * rng.randint(0, 12) + ["w"] * rng.randint(0, 10) + ["z"] * rng.randint(0, 10)
    rng.shuffle(typs)
    # f_0 somewhere in the first half
    fpos = rng.randint(0, len(typs) // 2)
    typs.insert(fpos, "f0")
    aclasses = []
    hclasses = []
    Aall, Hall, Vs = [], [], []
    f0 = None
    for ty in typs:
        if ty == "a":
            if aclasses and rng.random() < 0.4:
                p = d.add("E", cls=rng.choice(aclasses))
            else:
                p = d.add("E")
                aclasses.append(d.cls[p - 1])
            Aall.append(p)
        elif ty == "h":
            if hclasses and rng.random() < 0.4:
                p = d.add("F", cls=rng.choice(hclasses))
            else:
                p = d.add("F")
                hclasses.append(d.cls[p - 1])
            Hall.append(p)
        elif ty == "v":
            Vs.append(d.add("E", cls=auxc))
        elif ty == "w":
            d.fill("E")
        elif ty == "z":
            d.fill("F")
        else:
            f0 = d.add("F")
    d.fill("E", 6)
    f1 = d.add("F")
    b0 = d.add("F")
    Bstar = [b0] + [d.add("F", cls=d.cls[b0 - 1]) for _ in range(naux - 1)]
    d.fill("F", 3)
    for a in Astar + Vs + [e0]:
        d.S[a] = set(Hall)
    for a in Aall:
        d.S[a] = {f0, f1} | set(Hall)
    d.T[f0] = {e0}
    d.T[f1] = {e0}
    for b in Bstar:
        d.T[b] = set(Aall)
    for b in Hall:
        far = [v for v in Vs if v > b]
        d.T[b] = {e0} | set(rng.sample(Vs, min(len(Vs), rng.randint(0, 3)))) | set(far[:1])
        if rng.random() < 0.3 and Aall:
            d.T[b] |= set(rng.sample(Aall, min(len(Aall), rng.randint(1, 3))))
    allb = [f0, f1] + Hall + Bstar
    for b in allb:
        for a in Astar + [e0] + Vs:
            d.set_strict(b, a)
    for a in Aall:
        for b in [f0, f1] + Bstar:
            d.set_strict(b, a)
    d.info = {"Apos": Aall, "H": [(b, b) for b in Hall], "Vs": Vs, "e0": e0, "f0": f0, "f1": f1, "Astar": Astar, "Bstar": Bstar}
    # block shorter walks
    for it in range(3000):
        I, P = d.build()
        w = I.shortest(bound=len(P), budget=BUDGET)
        if w is None:
            break
        block(d, w, set(P), rng)
    else:
        return None
    return d


def block(d, w, Pset, rng):
    r = len(d.word)
    flips = [x for x in w if x not in Pset and x >> 1 < r]
    H = [x >> 1 for x in flips if x & 1 == 0]      # E-sides of F-members
    G = [x >> 1 for x in flips if x & 1 == 1]      # F-sides of E-members
    if H and G:
        h, a = rng.choice(H), rng.choice(G)
        d.set_strict(h + 1, a + 1)
        return
    # one type only: remove the contacts of a flip side with the members of the walk
    flip = rng.choice(flips)
    w0 = flip >> 1
    if flip & 1 == 0:
        kept = {x >> 1 for x in w if x in Pset and x & 1 == 0}
        q = [g for g in d.T[w0 + 1] if g - 1 in kept]
        g = rng.choice(q) if q else None
        if g is not None:
            d.T[w0 + 1].discard(g)
            if d.is_a(g) and (w0 + 1) not in d.S.get(g, ()):
                d.set_strict(w0 + 1, g)
    else:
        kept = {x >> 1 for x in w if x in Pset and x & 1 == 1}
        q = [g for g in d.S[w0 + 1] if g - 1 in kept]
        g = rng.choice(q) if q else None
        if g is not None:
            d.S[w0 + 1].discard(g)
            if d.is_b(g) and (w0 + 1) not in d.T.get(g, ()):
                d.set_strict(g, w0 + 1)


BASES = {"B": base_B, "A": base_A, "stair": base_stair, "ties": base_ties, "mix": base_mix, "small": base_small, "cegis": base_cegis, "cross": base_cross, "allstrict": base_allstrict}


def move(d, rng, st):
    """A random perturbation; returns its kind."""
    A, B = d.members()
    Apos = d.info["Apos"]
    Bpos = [z for pr in d.info["H"] for z in pr]
    r = len(d.word)
    kind = rng.choice(["addS", "addT", "unstrict", "tieA", "tieH", "wit", "attack", "attack", "addTcore", "addScore"])
    if kind == "addS":
        a = rng.choice(Apos)
        g = rng.choice([p for p in range(1, r + 1) if d.word[p - 1] == "F"])
        d.S[a].add(g)
    elif kind == "addScore":
        a = rng.choice(Apos)
        d.S[a].add(rng.choice(Bpos))
    elif kind == "addT":
        b = rng.choice(Bpos)
        q = rng.choice([p for p in range(1, r + 1) if d.word[p - 1] == "E"])
        d.T[b].add(q)
    elif kind == "addTcore":
        b = rng.choice(Bpos)
        d.T[b].add(rng.choice(Apos))
    elif kind == "unstrict":
        pairs = [(b, a) for a in Apos for b in Bpos if d.is_strict(b, a)]
        if not pairs:
            return "none"
        b, a = rng.choice(pairs)
        d.unset_strict(b, a)
        bs = [p for p in Bpos if d.cls[p - 1] == d.cls[b - 1]]
        aa = [p for p in Apos if d.cls[p - 1] == d.cls[a - 1]]
        for x in bs:
            for y in aa:
                if x not in d.S[y] and y not in d.T[x]:
                    d.S[y].add(x)
    elif kind == "tieA":
        x, y = rng.sample(Apos, 2)
        d.tie(x, y)
    elif kind == "tieH":
        x, y = rng.sample(Bpos, 2)
        d.tie(x, y)
    elif kind == "wit":
        # realize a contact by a middle witness
        if rng.random() < 0.5:
            a = rng.choice(Apos)
            q = [g for g in d.S[a] if d.is_b(g) and (a, g) not in d.wS]
            if not q:
                return "none"
            d.wS.add((a, rng.choice(q)))
        else:
            b = rng.choice(Bpos)
            q = [g for g in d.T[b] if d.is_a(g) and (b, g) not in d.wT]
            if not q:
                return "none"
            d.wT.add((b, rng.choice(q)))
    elif kind == "attack":
        # all positions of one class of A into the E-stars of 2..4 classes of B: the configuration the claim of Shape B excludes
        a = rng.choice(Apos)
        aa = [p for p in Apos if d.cls[p - 1] == d.cls[a - 1]]
        for _ in range(rng.randint(2, 4)):
            b = rng.choice(Bpos)
            bs = [p for p in Bpos if d.cls[p - 1] == d.cls[b - 1]]
            for x in bs:
                d.T[x] |= set(aa)
    return kind


def all_variants(I, P):
    yield "id", I, P
    yield "rev", I.reversed_st(), path_rev(P)
    op = I.op()
    yield "op", op, path_op(P)
    yield "oprev", op.reversed_st(), path_rev(path_op(P))


def main():
    seed, base, rounds, moves = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    log = open(sys.argv[5], "w", encoding="utf-8")
    rng = random.Random(seed)
    st = Counter()
    acc = Counter()
    rej = Counter()
    fails = []
    t0 = time.time()
    tl = float(os.environ.get("RV_TIME", "480"))

    def test(I, P, tag):
        for name, J, Q in all_variants(I, P):
            try:
                run_all(J, Q, rng, st, trials=3)
            except ClaimFail as e:
                fn = os.path.join(HERE, "ce", "planted-%s-%d-%d-%s.json" % (base, seed, len(fails), name))
                J.dump(fn, {"P": Q, "fail": str(e), "tag": tag})
                fails.append((fn, str(e)))
                print("FAIL", fn, e, file=log, flush=True)

    for rd in range(rounds):
        if time.time() - t0 > tl:
            break
        d = BASES[base](rng)
        if d is None:
            st["base: cegis gave up"] += 1
            continue
        I, P = d.build()
        I.validate()
        assert I.p2(), "P2 of the base"
        w = I.shortest(bound=len(P), budget=BUDGET)
        if w is not None:
            st["base: planted path not shortest (dropped)"] += 1
            print("base not shortest", base, "r", len(P), "found", len(w), file=log, flush=True)
            continue
        st["base instances verified"] += 1
        st["max r"] = max(st["max r"], len(P))
        st["max m"] = max(st["max m"], I.m)
        test(I, P, "base")
        for mv in range(moves):
            if time.time() - t0 > tl:
                break
            d2 = d.copy()
            d2.info = d.info
            kind = move(d2, rng, st)
            if kind == "none":
                continue
            I2, P2 = d2.build()
            if not I2.p2():
                rej[kind + " (P2)"] += 1
                continue
            try:
                w = I2.shortest(bound=len(P2), budget=BUDGET)
            except Budget:
                rej[kind + " (budget)"] += 1
                continue
            if w is not None:
                rej[kind] += 1
                continue
            acc[kind] += 1
            d = d2
            I, P = I2, P2
            if acc.total() % 10 == 0:
                test(I, P, "move")
        I.validate()
        test(I, P, "saturated")
        # another shortest path, if the solver finds one different from P
        w = I.shortest(bound=len(P) + 1, budget=BUDGET)
        if w is not None and w != P and len(w) == len(P):
            st["other shortest path"] += 1
            test(I, w, "other")
    print("base", base, "seed", seed, "time", round(time.time() - t0, 1), file=log)
    print("accepted moves", dict(acc), file=log)
    print("rejected moves", dict(rej), file=log)
    for k in sorted(st):
        print(k, st[k], file=log)
    print("FAILURES:", fails if fails else "none", file=log)
    log.close()


if __name__ == "__main__":
    main()
