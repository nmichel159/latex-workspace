"""Shared helpers of the agent `frames`: imports the referee library read-only, restricted state graphs, generators of instances."""
import os
import random
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS = os.path.normpath(os.path.join(HERE, "..", "..", "checks"))
sys.path.insert(0, CHECKS)
from zz_core import Budget, ClaimFail, Inst, bits, chk, popcnt  # noqa: E402,F401
from zz_design import BASES, Design, zipper  # noqa: E402,F401


# ------------------------------------------------------------------ state graph
class StateGraph:
    """Labelled states: (x, low) allowed if x in LOK, (x, high) allowed if x in HOK.  An edge joins (a, low) and (b, high) for ab in R."""

    def __init__(self, I, LOK=None, HOK=None):
        self.I = I
        self.LOK = I.ALL if LOK is None else LOK
        self.HOK = I.ALL if HOK is None else HOK

    def bfs_from(self, start_is_low, start):
        """Distances: returns (dL, dH), dicts element -> distance from the start state."""
        I = self.I
        dL, dH = {}, {}
        if start_is_low:
            if not self.LOK >> start & 1:
                return dL, dH
            dL[start] = 0
            fL, fH = 1 << start, 0
        else:
            if not self.HOK >> start & 1:
                return dL, dH
            dH[start] = 0
            fL, fH = 0, 1 << start
        vL, vH = fL, fH
        k = 0
        while fL or fH:
            k += 1
            nL, nH = 0, 0
            for x in bits(fL):
                nH |= I.HI[x]
            for x in bits(fH):
                nL |= I.LO[x]
            nH &= self.HOK & ~vH
            nL &= self.LOK & ~vL
            for x in bits(nH):
                dH[x] = k
            for x in bits(nL):
                dL[x] = k
            vH |= nH
            vL |= nL
            fL, fH = nL, nH
        return dL, dH

    def shortest(self, rng=None):
        """A shortest walk from (u, low) to (v, high), or None.  Tie-break random if rng is given."""
        I = self.I
        dL, dH = self.bfs_from(True, I.u)
        if I.v not in dH:
            return None
        out = [I.v]
        cur, hi = I.v, True
        k = dH[I.v]
        while k > 0:
            if hi:
                c = [y for y in bits(I.LO[cur]) if dL.get(y) == k - 1]
            else:
                c = [y for y in bits(I.HI[cur]) if dH.get(y) == k - 1]
            cur = rng.choice(c) if rng else c[0]
            hi = not hi
            k -= 1
            out.append(cur)
        return out[::-1]

    def dist(self):
        I = self.I
        dL, dH = self.bfs_from(True, I.u)
        return dH.get(I.v)

    def alive(self, bound=None):
        """States on some walk u -> v of length <= bound (default: any length): returns masks (low, high)."""
        I = self.I
        dL, dH = self.bfs_from(True, I.u)
        eL, eH = self.bfs_from(False, I.v)
        if I.v not in dH:
            return 0, 0
        aL, aH = 0, 0
        for x, k in dL.items():
            if x in eL and (bound is None or k + eL[x] <= bound):
                aL |= 1 << x
        for x, k in dH.items():
            if x in eH and (bound is None or k + eH[x] <= bound):
                aH |= 1 << x
        return aL, aH


def walk_highs_lows(W):
    """Positions 0, 2, ... are low, 1, 3, ... are high for a walk that starts at u."""
    return W[1::2], W[0::2]


def conflicts(I, W):
    highs, lows = walk_highs_lows(W)
    return [(h, l) for h in highs for l in lows if I.leq(h, l)]


def is_valid(I, W):
    return I.is_valid_walk(W)


# ------------------------------------------------------------------ data of a walk
class WData:
    def __init__(self, I, P):
        self.I, self.P = I, P
        if P[0] != I.u:
            P = P[::-1]
            self.P = P
        highs, lows = walk_highs_lows(P)
        self.highs, self.lows = highs, lows
        self.pos = {x: i for i, x in enumerate(P)}
        self.A = [x for x in highs if not any(I.lt(y, x) for y in highs)]
        self.B = [x for x in lows if not any(I.lt(x, y) for y in lows)]
        Am = sum(1 << x for x in self.A)
        Bm = sum(1 << x for x in self.B)
        self.Am, self.Bm = Am, Bm
        self.U = I.up(sum(1 << x for x in highs))
        self.L = I.dn(sum(1 << x for x in lows))

    def far_pairs_A(self):
        return [(x, y) for x in self.A for y in self.A if self.pos[x] + 6 <= self.pos[y]]

    def far_pairs_B(self):
        return [(x, y) for x in self.B for y in self.B if self.pos[x] + 6 <= self.pos[y]]


def planted(family, rng):
    d = BASES[family](rng)
    return d.build()


# ------------------------------------------------------------------ tiny random instances (same generator as run_tiny.py, re-implemented so that sizes can be chosen)
def random_preorder(rng, m, p=None):
    up = [1 << i for i in range(m)]
    if p is None:
        p = rng.uniform(0.05, 0.5)
    for i in range(2, m):
        up[0] |= 1 << i
        up[i] |= 1 << 1
    up[0] |= 1 << 1
    for i in range(2, m):
        for j in range(2, m):
            if i != j and rng.random() < p:
                up[i] |= 1 << j
    changed = True
    while changed:
        changed = False
        for i in range(m):
            for j in bits(up[i]):
                if up[j] & ~up[i]:
                    up[i] |= up[j]
                    changed = True
    return up


def random_p2_instance(rng, mlo=4, mhi=11, sparse=False):
    m = rng.randint(mlo, mhi)
    up = random_preorder(rng, m, rng.uniform(0.0, 0.25) if sparse else None)
    I0 = Inst(m, up, [], 0, 1)
    if not I0.lt(0, 1):
        return None
    pairs = [(x, y) for x in range(m) for y in bits(I0.USTR[x])]
    q = rng.uniform(0.05, 0.3) if sparse else rng.uniform(0.1, 0.8)
    edges = {e for e in pairs if rng.random() < q}
    if (0, 1) in edges:
        edges.discard((0, 1))
    I = Inst(m, up, edges, 0, 1)
    for _ in range(60):
        viol = I.p2_violations()
        if not viol:
            return I
        x, y = rng.choice(viol)
        below = I.DSTR[x] & I.DSTR[y]
        above = I.USTR[x] & I.USTR[y]
        c = list(bits(below)) + list(bits(above))
        if not c:
            return None
        z = rng.choice(c)
        if I.lt(z, x):
            edges |= {(z, x), (z, y)}
        else:
            edges |= {(x, z), (y, z)}
        I = Inst(m, up, edges, 0, 1)
    return None


def all_valid_downsets(I):
    return [D for D in I.downsets() if I.connected_in_GD(D)]
