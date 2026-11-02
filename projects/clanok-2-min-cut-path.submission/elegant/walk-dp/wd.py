"""Shared helpers of the walk-dp experiments: walk structure, atoms, window search, closures.

Elements and sets as in checks/zz_core.py (integer bit masks).  Node convention for the double cover: 2*x = x used as a low, 2*x+1 = x used as a high.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS = os.path.normpath(os.path.join(HERE, "..", "..", "checks"))
sys.path.insert(0, CHECKS)
from zz_core import Budget, ClaimFail, Inst, bits, popcnt  # noqa: E402,F401


class WS:
    """Structure of a valid walk P: positions, A_P, B_P."""

    def __init__(self, I, P):
        self.I, self.P = I, P
        if P[0] == I.u:
            self.lowpar = 0
        else:
            self.lowpar = 1
        self.pos = {}
        self.highs = 0
        self.lows = 0
        for i, x in enumerate(P):
            self.pos[x] = i
            if i % 2 == self.lowpar:
                self.lows |= 1 << x
            else:
                self.highs |= 1 << x
        self.A = [a for a in bits(self.highs) if not (I.DSTR[a] & self.highs)]
        self.B = [b for b in bits(self.lows) if not (I.USTR[b] & self.lows)]
        self.UP = I.up(self.highs)
        self.LP = I.dn(self.lows)
        self.q = len(P) - 1

    def far_pairs_A(self, d=6):
        out = []
        for i, a in enumerate(self.A):
            for b in self.A[:i]:
                if abs(self.pos[a] - self.pos[b]) >= d:
                    out.append((a, b))
        return out

    def far_pairs_B(self, d=6):
        out = []
        for i, a in enumerate(self.B):
            for b in self.B[:i]:
                if abs(self.pos[a] - self.pos[b]) >= d:
                    out.append((a, b))
        return out


def best_atoms(I, W):
    """Union of FR over all far pairs of A_P, intersection of ER over all far pairs of B_P: the best any number of far pairs can do."""
    F = I.DN[I.u]
    for a, b in W.far_pairs_A():
        F |= I.FR(a, b)
    E = I.ALL & ~I.UP[I.v]
    for a, b in W.far_pairs_B():
        E &= I.ER(a, b)
    return F, E


def window_search(I, lowok, highok, k, bound=None, cap_states=400000):
    """Shortest locally valid walk from u to v, lows in lowok, highs in highok; state = last k elements (at least the current one).  A new element is checked against
    the elements in the window only.  Returns the walk (a list) or None; length < bound if bound is given.  Raises Budget when the state cap is hit."""
    # distance to v in the allowed double cover
    INF = 10 ** 9
    dist = {2 * I.v + 1: 0}
    cur = [2 * I.v + 1]
    while cur:
        nxt = []
        for st in cur:
            x, hi = st >> 1, st & 1
            d = dist[st]
            if hi:
                for y in bits(I.LO[x] & lowok):
                    if 2 * y not in dist:
                        dist[2 * y] = d + 1
                        nxt.append(2 * y)
            else:
                for y in bits(I.HI[x] & highok):
                    if 2 * y + 1 not in dist:
                        dist[2 * y + 1] = d + 1
                        nxt.append(2 * y + 1)
        cur = nxt
    if 2 * I.u not in dist:
        return None
    k = max(k, 1)
    start = (I.u,)
    # state: tuple of the last elements; the label of the last element is implied by parity of the step
    seen = {(start, 0)}
    layer = [(start, 0)]
    parent = {(start, 0): None}
    steps = 0
    while layer:
        nxt = []
        for s in layer:
            win, hi = s
            x = win[-1]
            if hi and x == I.v:
                out = []
                t = s
                while t is not None:
                    out.append(t[0][-1])
                    t = parent[t]
                return out[::-1]
        steps += 1
        for s in layer:
            win, hi = s
            x = win[-1]
            if hi:
                # next is a low y: y must not be >= a high in the window
                cand = I.LO[x] & lowok
                n = len(win)
                for i in range(n - 1, -1, -2):  # highs: same parity as the last
                    cand &= ~I.UP[win[i]]
                for y in bits(cand):
                    if bound is not None and steps + dist.get(2 * y, INF) >= bound:
                        continue
                    w2 = (win + (y,))[-k:]
                    t = (w2, 0)
                    if t not in seen:
                        seen.add(t)
                        parent[t] = s
                        nxt.append(t)
            else:
                cand = I.HI[x] & highok
                n = len(win)
                for i in range(n - 1, -1, -2):  # lows
                    cand &= ~I.DN[win[i]]
                for y in bits(cand):
                    if bound is not None and steps + dist.get(2 * y + 1, INF) >= bound:
                        continue
                    w2 = (win + (y,))[-k:]
                    t = (w2, 1)
                    if t not in seen:
                        seen.add(t)
                        parent[t] = s
                        nxt.append(t)
            if len(seen) > cap_states:
                raise Budget()
        layer = nxt
    return None


def conflicts(I, W):
    """Conflicts of a walk from u to v: pairs of positions (i, j) with the high at i <= the low at j."""
    lab = [(i % 2 == 1) for i in range(len(W))]  # u low at position 0
    out = []
    for i, h in enumerate(W):
        if lab[i]:
            for j, l in enumerate(W):
                if not lab[j] and I.leq(h, l):
                    out.append((i, j))
    return out
