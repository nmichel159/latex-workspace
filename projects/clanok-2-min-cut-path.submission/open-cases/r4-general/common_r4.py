"""Shared helpers of agent r4-general (round 4).  Other agents' code is imported read-only.

Instance representation: gcert.Inst (dc-general/gcert.py): n, le, lt, R (oriented low -> high), bit masks
down[x], up[x], lo[x] (R-neighbours strictly below), hi[x] (above), B (class of u), T (class of v).
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

import gcert      # noqa: E402
import zz         # noqa: E402

bits = gcert.bits


def from_zz(z):
    """zz.ZZ -> gcert.Inst"""
    return gcert.Inst(z.n, [list(map(bool, r)) for r in z.le], [tuple(e) for e in z.R], z.u, z.v)


def to_zz(I):
    return zz.ZZ(I.n, None, list(I.R), I.u, I.v, le=[list(r) for r in I.le])


def make(n, le, R, u=0, v=None):
    if v is None:
        v = n - 1
    return gcert.Inst(n, [[bool(x) for x in row] for row in le], [tuple(e) for e in R], u, v)


def load_json(path):
    d = json.load(open(path))
    return make(d["n"], d["le"], d["R"], d["u"], d["v"]), d


def dump(I, extra=None):
    d = {"n": I.n, "u": I.u, "v": I.v, "le": [[int(x) for x in r] for r in I.le], "R": [list(e) for e in I.R]}
    if extra:
        d.update(extra)
    return d


def dual(I):
    """Reverse the order and exchange u and v: same edges, same answer, P2 kept (lower and upper witnesses swap)."""
    n = I.n
    le = [[I.le[b][a] for b in range(n)] for a in range(n)]
    return gcert.Inst(n, le, [(b, a) for a, b in I.R], I.v, I.u)


def is_downset(I, D):
    for x in bits(D):
        if I.down[x] & ~D:
            return False
    return True


def check_solution(I, D):
    """D a down-set with u in D, v not in D, and a u-v path in G_D."""
    if not is_downset(I, D):
        return False
    if not (D >> I.u) & 1 or (D >> I.v) & 1:
        return False
    return gcert.cut_path(I, D) is not None


def exact(I):
    return gcert.exact(I)


def solutions(I):
    """All solution down-sets (enumeration; small instances only)."""
    return [D for D in gcert.downsets(I) if gcert.cut_path(I, D) is not None]


def p2(I):
    return I.p2()


def middle(I):
    return [x for x in range(I.n) if not (I.B >> x) & 1 and not (I.T >> x) & 1]
