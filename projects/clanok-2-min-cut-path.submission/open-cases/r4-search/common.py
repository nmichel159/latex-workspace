"""Shared helpers of agent r4-search (round 4): imports of the other agents' code (read-only), instance conversion,
JSON input and output, exact solvers.

Representations
  ZZ instance: zz.ZZ (dc-algorithm/zz.py): n elements, preorder le, strict lt, real edges R (oriented low -> high),
  u least, v greatest.
  2CH instance: tuple (N, E, F, s, t) with E[i], F[i] bit masks of nodes (dc-hardness/twoch.py); converted to ZZ by
  dc-hardness/swlib.to_zz (bottoms ~ u, tops ~ v, switches pairwise incomparable).
  gcert instance: gcert.Inst (dc-general/gcert.py), same data with bit masks.

JSON instance file (instances/*.json):
  {"name": str, "n": int, "u": int, "v": int, "le": [[0/1]*n]*n, "R": [[a, b], ...], "names": [str]*n (optional),
   "2ch": {"N": int, "s": int, "t": int, "E": [[nodes]], "F": [[nodes]]} (optional, switch-model instances),
   "verdict": {...} (portfolio output, optional), "notes": str (optional)}
"""
import os
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
OC = os.path.dirname(HERE)
for _d in ("dc-hardness", "dc-general", "dc-algorithm"):
    _p = os.path.join(OC, _d)
    if _p not in sys.path:
        sys.path.insert(0, _p)
sys.setrecursionlimit(100000)

import zz          # noqa: E402  (read-only import, dc-algorithm)
import gcert       # noqa: E402  (read-only import, dc-general)
import twoch       # noqa: E402  (read-only import, dc-hardness)
import swlib       # noqa: E402  (read-only import, dc-hardness)


def bits(m):
    out = []
    while m:
        low = m & -m
        out.append(low.bit_length() - 1)
        m ^= low
    return out


# ----------------------------------------------------------------------------------------------------------------
# conversions
# ----------------------------------------------------------------------------------------------------------------

def to_gc(z):
    """zz.ZZ -> gcert.Inst"""
    return gcert.Inst(z.n, [list(r) for r in z.le], [tuple(e) for e in z.R], z.u, z.v)


def make_zz(n, le, R, u=0, v=None):
    if v is None:
        v = n - 1
    return zz.ZZ(n, None, [tuple(e) for e in R], u, v, le=[[bool(x) for x in row] for row in le])


def sw_to_zz(inst):
    """2CH -> (zz.ZZ, names) by swlib.to_zz."""
    return swlib.to_zz(tuple(inst))


def zz_to_sw(z):
    """If z is a switch-model instance (middle elements pairwise incomparable, every element ~ u or ~ v or middle,
    no R-edge between two middle elements), return the contracted 2CH instance (N, E, F, s, t) and the map
    switch index -> middle element; else None.  Nodes = components of the graph of bottom-top edges (bottoms = class
    of u, tops = class of v)."""
    n, le = z.n, z.le
    u, v = z.u, z.v
    B = [x for x in range(n) if le[x][u]]
    T = [x for x in range(n) if le[v][x]]
    Bs, Ts = set(B), set(T)
    M = [x for x in range(n) if x not in Bs and x not in Ts]
    for i, a in enumerate(M):
        for b in M[i + 1:]:
            if le[a][b] or le[b][a]:
                return None
    Ms = set(M)
    for a, b in z.R:
        if a in Ms and b in Ms:
            return None
    # components of bottoms/tops under fixed edges
    parent = {x: x for x in B + T}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in z.R:
        if a in Bs and b in Ts:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb
    roots = sorted({find(x) for x in B + T})
    node = {r: i for i, r in enumerate(roots)}
    N = len(roots)
    s = node[find(u)]
    t = node[find(v)]
    E, F = [], []
    for x in M:
        e = f = 0
        for a, b in z.R:
            if b == x and a in Bs:
                e |= 1 << node[find(a)]
            if a == x and b in Ts:
                f |= 1 << node[find(b)]
        E.append(e)
        F.append(f)
    if s == t:
        return None
    return (N, E, F, s, t), M


# ----------------------------------------------------------------------------------------------------------------
# exact solvers
# ----------------------------------------------------------------------------------------------------------------

def exact(z, both=True):
    """Exact answer by zz.exact_dfs; with both=True also by gcert.exact (independent code of another agent); raises
    on disagreement.  Returns (answer, walk)."""
    a, w = zz.exact_dfs(z)
    if both:
        b = gcert.exact(to_gc(z))
        if a != b:
            raise AssertionError("exact solvers disagree")
    return a, w


def solution_downsets(z):
    """All solution down-sets (bit masks) by enumerating all down-sets (small instances only)."""
    adj = z.adj()
    return [D for D in zz.downsets(z) if zz.zigzag_in(z, D, adj) is not None]


def check_walk(z, w):
    """w is a consistent zigzag walk of z (alternating, real edges, no valley >= peak)."""
    if not w or w[0] != z.u or w[-1] != z.v or len(w) % 2 != 0:
        return False
    Rs = set(z.R)
    for i in range(len(w) - 1):
        a, b = w[i], w[i + 1]
        if i % 2 == 0:
            if (a, b) not in Rs:
                return False
        elif (b, a) not in Rs:
            return False
    for x in w[0::2]:
        for y in w[1::2]:
            if z.le[y][x]:
                return False
    return True


def check_downset_solution(z, D):
    """D (bit mask) is a down-set with u in D, v not in D and G_D connects u, v."""
    n, le = z.n, z.le
    if not (D >> z.u) & 1 or (D >> z.v) & 1:
        return False
    for b in range(n):
        if (D >> b) & 1:
            for a in range(n):
                if le[a][b] and not (D >> a) & 1:
                    return False
    return zz.zigzag_in(z, D) is not None


# ----------------------------------------------------------------------------------------------------------------
# JSON
# ----------------------------------------------------------------------------------------------------------------

def sw_to_json(inst):
    N, E, F, s, t = inst
    return {"N": N, "s": s, "t": t, "E": [bits(m) for m in E], "F": [bits(m) for m in F]}


def sw_from_json(d):
    return (d["N"], [sum(1 << x for x in e) for e in d["E"]], [sum(1 << x for x in f) for f in d["F"]],
            d["s"], d["t"])


def to_json(z, name="", names=None, sw=None, verdict=None, notes=None):
    d = {"name": name, "n": z.n, "u": z.u, "v": z.v, "le": [[int(b) for b in row] for row in z.le],
         "R": [list(e) for e in z.R]}
    if names is not None:
        d["names"] = [str(x) for x in names]
    if sw is not None:
        d["2ch"] = sw_to_json(sw)
    if verdict is not None:
        d["verdict"] = verdict
    if notes is not None:
        d["notes"] = notes
    return d


def from_json(d):
    """returns (z, sw or None, names or None)"""
    z = make_zz(d["n"], d["le"], d["R"], d["u"], d["v"])
    sw = sw_from_json(d["2ch"]) if "2ch" in d else None
    return z, sw, d.get("names")


def save(path, d):
    with open(path, "w") as f:
        json.dump(d, f)


def load(path):
    with open(path) as f:
        return from_json(json.load(f))


def p2_bad(z):
    return z.p2_bad()


def width(z):
    """Width of the order on the classes (largest antichain of classes), by bipartite matching (Dilworth)."""
    n, le = z.n, z.le
    reps = []
    seen = set()
    for x in range(n):
        if x in seen:
            continue
        cl = [y for y in range(n) if le[x][y] and le[y][x]]
        seen |= set(cl)
        reps.append(x)
    m = len(reps)
    lt = [[le[reps[i]][reps[j]] and not le[reps[j]][reps[i]] for j in range(m)] for i in range(m)]
    match_r = [-1] * m

    def aug(i, vis):
        for j in range(m):
            if lt[i][j] and not vis[j]:
                vis[j] = True
                if match_r[j] < 0 or aug(match_r[j], vis):
                    match_r[j] = i
                    return True
        return False
    msize = sum(1 for i in range(m) if aug(i, [False] * m))
    return m - msize
