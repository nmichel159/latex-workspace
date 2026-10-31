"""Hypothesis H (agent r5-classes): in every shortest valid path of a 2CH + P2 instance some member's partner
meets few members of the other type.

Abstract planted path: positions 1..r with types typ[j] in {0, 1} (0 = E); contact sets cont[j] (positions c != j
with X'_j meeting X_c).  Realisation (singleton classes): nodes s in X_1, t in X_r, y_j in X_j and X_{j+1}; a
private node in X'_a and X_c for every contact c of a; a private node in X'_a and X'_b for every same-type pair
with |a - b| >= 2 (P2 by partners).  P2 for an opposite-type pair a, b needs b in cont[a] or a in cont[b]; for an
adjacent same-type pair it is met by y.  The only sides are the members and the partners.

hill(seed, r, steps): hill climbing on the contact sets, maximising min over members of |f(u)| (f(u) = members of
the other type in cont[u]) subject to P2 and to P being a shortest valid path (exact check by ccore).
"""
import random
import sys
import ccore as C


def realise(typ, cont):
    r = len(typ)
    nodes = {}

    def nd(name):
        if name not in nodes:
            nodes[name] = len(nodes)
        return nodes[name]
    mem = [set() for _ in range(r)]     # member side X_j (type typ[j])
    par = [set() for _ in range(r)]     # partner side X'_j
    mem[0].add(nd("s"))
    mem[r - 1].add(nd("t"))
    for j in range(r - 1):
        y = nd(("y", j))
        mem[j].add(y)
        mem[j + 1].add(y)
    for a in range(r):
        for c in cont[a]:
            z = nd(("z", a, c))
            par[a].add(z)
            mem[c].add(z)
    for a in range(r):
        for b in range(a + 2, r):
            if typ[a] == typ[b]:
                w = nd(("w", a, b))
                par[a].add(w)
                par[b].add(w)
    sw = []
    for j in range(r):
        m = C.orbits(mem[j])
        p = C.orbits(par[j])
        if typ[j] == 0:
            sw.append((m, p))
        else:
            sw.append((p, m))
    inst = C.Inst(len(nodes), nodes["s"], nodes["t"], sw, list(range(r)))
    P = tuple(2 * j + typ[j] for j in range(r))
    return inst, P


def p2_abstract(typ, cont):
    r = len(typ)
    for a in range(r):
        for b in range(a + 1, r):
            if typ[a] != typ[b] and b not in cont[a] and a not in cont[b]:
                return False
    return True


def fvals(typ, cont):
    return [sum(1 for c in cont[u] if typ[c] != typ[u]) for u in range(len(typ))]


def is_shortest(typ, cont):
    inst, P = realise(typ, cont)
    if not C.p2_ok(inst):
        return False, None
    L, paths = C.shortest_valid_paths(inst, limit=1, maxlen=len(typ))
    return (L == len(typ)), inst


def random_start(rng, r):
    typ = [rng.randrange(2) for _ in range(r)]
    cont = [set() for _ in range(r)]
    # minimal P2: for every opposite pair pick a direction (forward from the earlier one)
    for a in range(r):
        for b in range(a + 1, r):
            if typ[a] != typ[b]:
                if rng.random() < 0.5:
                    cont[a].add(b)
                else:
                    cont[b].add(a)
    return typ, cont


def rword_start(W):
    typ = [0 if ch == "E" else 1 for ch in W]
    r = len(typ)
    cont = [set() for _ in range(r)]
    for a in range(r):
        for b in range(a + 1, r):
            if typ[a] != typ[b]:
                cont[a].add(b)
    return typ, cont


def repair_shortest(rng, typ, cont, tries=200):
    """remove contacts until P2 still holds and P is shortest (greedy random)"""
    ok, _ = is_shortest(typ, cont)
    t = 0
    while not ok and t < tries:
        t += 1
        a = rng.randrange(len(typ))
        if not cont[a]:
            continue
        c = rng.choice(sorted(cont[a]))
        cont[a].discard(c)
        if not p2_abstract(typ, cont):
            # move the obligation to the other direction
            cont[c].add(a)
        ok, _ = is_shortest(typ, cont)
    return ok


def score(typ, cont):
    fv = fvals(typ, cont)
    srt = sorted(fv)
    return (srt[0], srt[1] if len(srt) > 1 else 0, sum(fv))


def hill(seed, r, steps, start="random", log=None):
    rng = random.Random(seed)
    if start == "random":
        typ, cont = random_start(rng, r)
    elif start == "word":
        typ, cont = rword_start("".join(rng.choice("EF") for _ in range(r)))
    else:
        typ, cont = rword_start(start)
        r = len(typ)
    if not repair_shortest(rng, typ, cont, tries=5000):
        return None
    best = score(typ, cont)
    for it in range(steps):
        typ2 = list(typ)
        cont2 = [set(x) for x in cont]
        mv = rng.random()
        a = rng.randrange(r)
        if mv < 0.55:
            c = rng.randrange(r)
            if c == a:
                continue
            cont2[a].add(c)
        elif mv < 0.85:
            if not cont2[a]:
                continue
            c = rng.choice(sorted(cont2[a]))
            cont2[a].discard(c)
            if typ2[a] != typ2[c] and a not in cont2[c]:
                cont2[c].add(a)
        else:
            # flip direction of one opposite pair
            c = rng.randrange(r)
            if c == a or typ2[a] == typ2[c]:
                continue
            if c in cont2[a]:
                cont2[a].discard(c)
                cont2[c].add(a)
            else:
                cont2[c].discard(a)
                cont2[a].add(c)
        if not p2_abstract(typ2, cont2):
            continue
        sc = score(typ2, cont2)
        if sc < best:
            continue
        ok, _ = is_shortest(typ2, cont2)
        if not ok:
            continue
        typ, cont, best = typ2, cont2, sc
        if log is not None and it % 200 == 0:
            print("  it", it, "score", best, flush=True, file=log)
    return typ, cont, best


if __name__ == "__main__":
    seed = int(sys.argv[1])
    count = int(sys.argv[2])
    r = int(sys.argv[3])
    steps = int(sys.argv[4])
    start = sys.argv[5] if len(sys.argv) > 5 else "word"
    hist = {}
    worst = None
    for i in range(count):
        res = hill(seed * 1000 + i, r, steps, start=start)
        if res is None:
            print("start failed", i, flush=True)
            continue
        typ, cont, best = res
        hist[best[0]] = hist.get(best[0], 0) + 1
        print("run", i, "min|f| =", best[0], "second", best[1], "sum", best[2],
              "types", "".join("EF"[x] for x in typ), flush=True)
        if worst is None or best > worst[0]:
            worst = (best, typ, [sorted(x) for x in cont])
    print("histogram of min|f|:", hist)
    print("best:", worst)
