"""Random graphs of the class "every pair has d <= 2 or c <= k" (k = 2: DC, k = 3: DC') with 9..16 vertices.
Two generators: core + ears (short, long, triangle ears, ears on ears, pendant trees for bridges), and planted
alternating structures (a u-v path alternating between two dense sides, balanced by degree-2 or degree-3 ears).
A repair loop adds edges for pairs with d >= 3 and c > k; graphs that cannot be repaired are rejected."""
import random
from eqcore import Small, adj_masks, all_dist


def _repair(n, E, k, core, rng, rounds=6):
    for _ in range(rounds):
        edges = sorted(E)
        sm = Small(n, [(a, b, 1) for a, b in edges])
        dist = all_dist(adj_masks(n, edges))
        bad = [(x, y) for x in range(n) for y in range(x + 1, n)
               if (dist[x][y] == -1 or dist[x][y] > 2) and sm.conn(x, y) > k]
        if not bad:
            return edges
        rng.shuffle(bad)
        for x, y in bad[:3]:
            if rng.random() < 0.5:
                E.add((x, y))
            else:
                # common neighbour among the core
                z = rng.choice(core)
                if z not in (x, y):
                    E.add((min(x, z), max(x, z)))
                    E.add((min(y, z), max(y, z)))
                else:
                    E.add((x, y))
    return None


def gen_core_ears(rng, k=2, nmin=9, nmax=16):
    n_t = rng.randint(nmin, nmax)
    q = rng.randint(4, min(10, n_t - 2))
    p = rng.choice([0.3, 0.45, 0.6, 0.75, 0.9])
    E = set()
    for i in range(q):
        for j in range(i + 1, q):
            if rng.random() < p:
                E.add((i, j))
    nxt = q
    while nxt < n_t:
        typ = rng.choice(["short", "short", "short", "path2", "path3", "tri", "y3" if k >= 3 else "short",
                          "pendant"])
        size = {"short": 1, "path2": 2, "path3": 3, "tri": 3, "y3": 1, "pendant": 1}[typ]
        if nxt + size > n_t:
            typ, size = "short", 1
        anchors = list(range(q)) if rng.random() < 0.85 else list(range(nxt))
        pick = lambda: (rng.choice([0, 1]) if rng.random() < 0.3 else rng.choice(anchors))
        p_, s_ = pick(), pick()
        V = list(range(nxt, nxt + size))
        if typ == "short":
            if p_ == s_:
                s_ = rng.choice(anchors)
                if p_ == s_:
                    continue
            E.add((min(p_, V[0]), V[0]))
            E.add((min(s_, V[0]), V[0]))
        elif typ == "pendant":
            E.add((p_, V[0]))
        elif typ == "y3":
            t_ = pick()
            for a in {p_, s_, t_}:
                E.add((a, V[0]))
        else:
            for i in range(size - 1):
                E.add((V[i], V[i + 1]))
            if typ == "tri":
                E.add((V[0], V[2]))
            E.add((p_, V[0]))
            E.add((s_, V[-1]))
        nxt += size
    E = {(min(a, b), max(a, b)) for a, b in E if a != b}
    edges = _repair(nxt, E, k, list(range(q)), rng)
    return (nxt, edges) if edges else None


def gen_planted(rng, k=2, nmin=9, nmax=16):
    n_t = rng.randint(nmin, nmax)
    L = rng.choice([3, 3, 5, 5, 7])
    h = (L + 1) // 2
    extraE = rng.randint(0, 2)
    extraO = rng.randint(0, 2)
    Ev = list(range(h + extraE))
    Od = list(range(h + extraE, 2 * h + extraE + extraO))
    n = 2 * h + extraE + extraO
    if n + 2 > n_t:
        return None
    u = Ev[0]
    v = Od[h - 1]
    pe = [u] + rng.sample(Ev[1:], h - 1)
    po = rng.sample([x for x in Od if x != v], h - 1) + [v]
    path = []
    for i in range(h):
        path += [pe[i], po[i]]
    E = set()
    for i in range(L):
        a, b = path[i], path[i + 1]
        E.add((min(a, b), max(a, b)))
    pin = rng.choice([0.5, 0.7, 0.9, 1.0])
    for S in (Ev, Od):
        for i in range(len(S)):
            for j in range(i + 1, len(S)):
                if rng.random() < pin:
                    E.add((S[i], S[j]))
    pc = rng.choice([0.0, 0.05, 0.15])
    for a in Ev:
        for b in Od:
            if (a, b) != (u, v) and rng.random() < pc:
                E.add((min(a, b), max(a, b)))
    cutdeg = {x: 0 for x in range(n)}
    for a, b in E:
        if (a in Ev) != (b in Ev):
            cutdeg[a] += 1
            cutdeg[b] += 1
    nxt = n
    jobs = []
    for x in Ev[1:]:
        jobs += [("E", x)] * rng.randint(0, cutdeg[x])
    for y in Od:
        if y != v:
            jobs += [("O", y)] * rng.randint(0, cutdeg[y])
    rng.shuffle(jobs)
    for side, x in jobs:
        if nxt >= n_t:
            break
        w = nxt
        nxt += 1
        if side == "E":
            E.add((u, w))
            E.add((x, w))
            if k >= 3 and rng.random() < 0.3:
                E.add((rng.choice(Ev), w))
        else:
            E.add((x, w))
            E.add((v, w))
            if k >= 3 and rng.random() < 0.3:
                E.add((rng.choice(Od), w))
    while nxt < nmin:
        # pad with short ears between random core vertices
        a, b = rng.sample(range(n), 2)
        E.add((a, nxt))
        E.add((b, nxt))
        nxt += 1
    E = {(min(a, b), max(a, b)) for a, b in E if a != b}
    edges = _repair(nxt, E, k, list(range(n)), rng)
    return (nxt, edges, u, v) if edges else None
