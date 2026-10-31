"""Agent r7-lb: planted-path designs in general switch form, given by a genome (r7-lb.md Section 3).

A genome fixes: a word over {E, F} (the planted path, base switches 0..n-1), nx extra switches (n..n+nx-1), a set
of relations (a, b) meaning a <= b (closed transitively), a contact for every incomparable pair, and voluntary
nodes shared by two sides.  build(g) returns the instance (zzl.SW) or None if the planted path is not valid.

Nodes: s, t, path nodes c_0..c_{n-2} (c_j in h_j and h_{j+1}), s in h_0 only, t in h_{n-1} only; every other node is
fresh and shared by exactly the sides named.  h_j is E_j if word[j] == 'E', else F_j.
Contacts of an incomparable pair {x, y} (P2): 'EE' (fresh node in E_x and E_y), 'FF' (fresh node in F_x and F_y),
('LW', z) (middle edges (z, x), (z, y), needs z < x and z < y), ('UW', z) (middle edges (x, z), (y, z), needs
z > x, z > y).  A witness contact whose condition fails falls back to 'EE'.  Pairs without a stored contact get 'EE'
if g['default'] == 'EE', 'FF' if 'FF', or a pseudo-random choice from a hash of the pair if 'R'.
Voluntary nodes: ((w1, ty1), (w2, ty2)) with ty 0 = E-side, 1 = F-side: a fresh node in both sides.
Middle edges: one per ordered strict pair, private node fresh (lies in F_z and E_v only).
The instance satisfies P2 by construction (checked by zzl.SW.p2_switch in the tests) and is a yes-instance, since
the planted path h_0 .. h_{n-1} is valid whenever no E-member is <= an F-member (checked).
"""
import os
import sys
import json
import random

HERE = os.path.dirname(os.path.abspath(__file__))
OC = os.path.dirname(HERE)
for _d in (os.path.join(OC, "verify", "rv-r6-core"), HERE):
    if _d not in sys.path:
        sys.path.append(_d)

from zzl import SW  # noqa: E402


def closure(m, rel):
    le = [[i == j for j in range(m)] for i in range(m)]
    for (a, b) in rel:
        le[a][b] = True
    for k in range(m):
        for i in range(m):
            if le[i][k]:
                rk = le[k]
                ri = le[i]
                for j in range(m):
                    if rk[j]:
                        ri[j] = True
    return le


def new_genome(word, nx, default="R", seed=0):
    return {"word": word, "nx": nx, "rel": [], "contact": {}, "vol": [], "default": default, "seed": seed}


def pair_key(x, y):
    return "%d,%d" % (min(x, y), max(x, y))


def _default_kind(g, x, y):
    d = g.get("default", "R")
    if d in ("EE", "FF"):
        return d
    r = random.Random("%s-%d-%d" % (g.get("seed", 0), min(x, y), max(x, y)))
    return "EE" if r.random() < 0.5 else "FF"


def build(g, check=False):
    word = g["word"]
    n = len(word)
    m = n + g["nx"]
    le = closure(m, [tuple(r) for r in g["rel"]])
    for a in range(n):
        for b in range(n):
            if word[a] == "E" and word[b] == "F" and le[a][b]:
                return None
    nn = [0]

    def node():
        nn[0] += 1
        return nn[0] - 1
    s = node()
    t = node()
    E = [0] * m
    F = [0] * m

    def addside(w, ty, nd):
        if ty == 0:
            E[w] |= 1 << nd
        else:
            F[w] |= 1 << nd
    pty = [0 if c == "E" else 1 for c in word]
    addside(0, pty[0], s)
    addside(n - 1, pty[n - 1], t)
    for j in range(n - 1):
        c = node()
        addside(j, pty[j], c)
        addside(j + 1, pty[j + 1], c)
    strict = lambda a, b: le[a][b] and not le[b][a]
    me = {}

    def medge(z, v):
        if (z, v) not in me:
            p = node()
            me[(z, v)] = p
            F[z] |= 1 << p
            E[v] |= 1 << p
    for x in range(m):
        for y in range(x + 1, m):
            if le[x][y] or le[y][x]:
                continue
            k = g["contact"].get(pair_key(x, y))
            if k is None:
                k = _default_kind(g, x, y)
            if isinstance(k, (list, tuple)):
                kind, z = k[0], int(k[1])
                if kind == "LW" and 0 <= z < m and strict(z, x) and strict(z, y):
                    medge(z, x)
                    medge(z, y)
                    continue
                if kind == "UW" and 0 <= z < m and strict(x, z) and strict(y, z):
                    medge(x, z)
                    medge(y, z)
                    continue
                k = "EE"
            c = node()
            if k == "EE":
                E[x] |= 1 << c
                E[y] |= 1 << c
            else:
                F[x] |= 1 << c
                F[y] |= 1 << c
    for (s1, s2) in g["vol"]:
        (w1, t1), (w2, t2) = s1, s2
        if not (0 <= w1 < m and 0 <= w2 < m):
            continue
        c = node()
        addside(w1, t1, c)
        addside(w2, t2, c)
    for (z, v, p) in g.get("medges", []):
        if 0 <= z < m and 0 <= v < m and strict(z, v):
            medge(z, v)
    mel = [(z, v, p) for (z, v), p in me.items()]
    I = SW(m, le, E, F, s, t, nn[0], mel)
    if check and not I.p2_switch():
        raise RuntimeError("P2 fails")
    return I


def planted_pair(g, I):
    """(L, Up) of the planted path."""
    word = g["word"]
    WE = [j for j, c in enumerate(word) if c == "E"]
    WF = [j for j, c in enumerate(word) if c == "F"]
    return I.dnc(sum(1 << b for b in WF)), I.upc(sum(1 << a for a in WE))


def save_genome(g, path, extra=None):
    d = dict(g)
    d["extra"] = extra or {}
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f)


def load_genome(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    d["rel"] = [tuple(r) for r in d["rel"]]
    d["vol"] = [tuple(tuple(s) for s in v) for v in d["vol"]]
    return d
