"""Pivot duality for the minimax argument (r6-core.md §3).

For a Gen G (r5-core/gcore.py, read-only) and a valid path P (side ids):
  WE, WF (masks of switches), Up = up-closure of WE, Dn = L = down-closure of WF,
  A = minimal E-members (switches), B = maximal F-members,
  NE = switches in L with non-empty E-side (needed E-sides), NF = switches in Up with non-empty F-side.
  For x in Up: Abelow(x) = minimal E-members strictly below x (pivot cost; 0 if x is itself minimal),
  for y in L: Babove(y) = maximal F-members strictly above y.
E-tool(x), x in Up: centre E_x (covers y in NE iff E_x meets E_y), the sibling set Sib(x) (switches sharing a
  lower middle neighbour with x; covers y iff y in Sib(x)) and, if |Abelow(x)| <= c, the pivot at x
  (covers y iff y < x strictly).
F-tool(y), y in L: centre F_y (covers x in NF iff F_x meets F_y) and, if |Babove(y)| <= c, the pivot at y
  (covers x iff x > y).
Duality: for every x in NF and y in NE, E-tool(x) covers y or F-tool(y) covers x.  pair_classes reports, for every
such pair, which alternative holds, and lists the pairs where neither does ('fail'), split into comparable pairs
(y < x) and incomparable pairs (P2 only by a middle witness).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OC = os.path.dirname(HERE)
for _d in ("r5-core", "r4-general", "dc-hardness", "dc-general", "dc-algorithm", "r4-switch"):
    _p = os.path.join(OC, _d)
    if _p not in sys.path:
        sys.path.append(_p)

import gcore                      # noqa: E402  (r5-core, read-only)
from gcore import bits            # noqa: E402


def lt(G, a, b):
    return G.le[a][b] and not G.le[b][a]


class Skel:
    def __init__(self, G, P):
        self.G, self.P = G, P
        WE = [i >> 1 for i in P if not i & 1]
        WF = [i >> 1 for i in P if i & 1]
        self.WE, self.WF = WE, WF
        Up = 0
        for w in WE:
            Up |= G.up[w]
        Dn = 0
        for w in WF:
            Dn |= G.dn[w]
        assert not (Up & Dn)
        self.Up, self.Dn = Up, Dn
        self.A = [w for w in WE if not any(lt(G, v, w) for v in WE)]
        self.B = [w for w in WF if not any(lt(G, w, v) for v in WF)]
        self.NE = [w for w in bits(Dn) if G.E[w]]
        self.NF = [w for w in bits(Up) if G.F[w]]
        self.Abelow = {x: [a for a in self.A if lt(G, a, x)] for x in bits(Up)}
        self.Babove = {y: [b for b in self.B if lt(G, y, b)] for y in bits(Dn)}


def siblings(G):
    """Sib[x] = switches v != x sharing a lower middle neighbour with x (edges w-x, w-v, w < x, v);
    SibUp[y] = switches v != y sharing an upper middle neighbour with y (edges y-w, v-w)."""
    low = {}
    up = {}
    for z, (y, x) in G.medge.items():        # y < x
        low.setdefault(x, set()).add(y)
        up.setdefault(y, set()).add(x)
    m = G.m
    Sib = [set() for _ in range(m)]
    SibUp = [set() for _ in range(m)]
    for w, xs in up.items():                # w is a lower middle neighbour of every x in xs
        for x in xs:
            Sib[x] |= xs - {x}
    for w, ys in low.items():               # w is an upper middle neighbour of every y in ys
        for y in ys:
            SibUp[y] |= ys - {y}
    return Sib, SibUp


def pair_classes(G, P, c=0, use_sib=True):
    S = Skel(G, P)
    Sib, SibUp = siblings(G) if use_sib else ([set()] * G.m, [set()] * G.m)
    out = {"centreE": 0, "sibE": 0, "pivotE": 0, "centreF": 0, "sibF": 0, "pivotF": 0, "fail_comp": [],
           "fail_incomp": [], "pairs": 0}
    for x in S.NF:
        cheapx = len(S.Abelow[x]) <= c
        for y in S.NE:
            out["pairs"] += 1
            if G.E[x] & G.E[y]:
                out["centreE"] += 1
                continue
            if y in Sib[x]:
                out["sibE"] += 1
                continue
            if cheapx and lt(G, y, x):
                out["pivotE"] += 1
                continue
            if G.F[x] & G.F[y]:
                out["centreF"] += 1
                continue
            if x in SibUp[y]:
                out["sibF"] += 1
                continue
            if len(S.Babove[y]) <= c and lt(G, y, x):
                out["pivotF"] += 1
                continue
            if lt(G, y, x):
                out["fail_comp"].append((x, y))
            else:
                out["fail_incomp"].append((x, y))
    return S, out
