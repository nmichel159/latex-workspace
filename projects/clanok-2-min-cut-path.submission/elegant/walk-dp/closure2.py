"""Closure with learned conflicts on the double cover (the rule CL2).

State: alive nodes (AL, AH) and a symmetric conflict relation NG on nodes (masks NGL[n], NGH[n]).  Initially NG = the order conflicts: x high and y low with x <= y.
Meaning of the invariant: every simple valid walk (a simple path of the double cover from u low to v high with no high <= low) uses only alive nodes and no pair of NG.

closure(S, assumed): repeat: chain of blocks from s to t; nodes off the chain die; forced nodes (s, t, the cut vertices of the chain, the assumed nodes) kill their NG partners.
fixpoint(): for every alive node n with an alive partner: S(n) = closure(S, {n}).  If it is refuted, n dies.  Otherwise every node alive in S and dead in S(n) gets a conflict with n.  Repeat until nothing changes.
Every step is sound for the set of all simple valid walks.  Refuted at the top level means: no valid walk.
"""
from collections import Counter

from wd import bits
from closure import Graph, Refuted


class CL2:
    def __init__(self, I):
        self.I = I
        self.G = Graph(I)
        m = I.m
        self.NGL = [0] * (2 * m)
        self.NGH = [0] * (2 * m)
        for x in range(m):
            self.NGH[2 * x] = I.DN[x]      # x low kills highs <= x
            self.NGL[2 * x + 1] = I.UP[x]  # x high kills lows >= x
        self.stats = Counter()

    def closure(self, AL, AH, assume=()):
        G = self.G
        NGL, NGH = self.NGL, self.NGH
        while True:
            r = G.chain(AL, AH)
            if r is None:
                raise Refuted()
            AL2, AH2, forced = r
            for n in forced:
                x = n >> 1
                if n & 1:
                    if not AH2 >> x & 1:
                        raise Refuted()
                else:
                    if not AL2 >> x & 1:
                        raise Refuted()
                AL2 &= ~NGL[n]
                AH2 &= ~NGH[n]
            for n in assume:
                x = n >> 1
                if n & 1:
                    if not AH2 >> x & 1:
                        raise Refuted()
                else:
                    if not AL2 >> x & 1:
                        raise Refuted()
                AL2 &= ~NGL[n]
                AH2 &= ~NGH[n]
            if AL2 == AL and AH2 == AH:
                return AL, AH, forced
            AL, AH = AL2, AH2

    def add_conflict(self, n, p):
        """Returns True if new."""
        new = False
        for a, b in ((n, p), (p, n)):
            y = b >> 1
            if b & 1:
                if not self.NGH[a] >> y & 1:
                    self.NGH[a] |= 1 << y
                    new = True
            else:
                if not self.NGL[a] >> y & 1:
                    self.NGL[a] |= 1 << y
                    new = True
        return new

    def nodes_with_partner(self, AL, AH):
        out = []
        for x in bits(AL):
            n = 2 * x
            if self.NGL[n] & AL or self.NGH[n] & AH:
                out.append(n)
        for x in bits(AH):
            n = 2 * x + 1
            if self.NGL[n] & AL or self.NGH[n] & AH:
                out.append(n)
        return out

    def fixpoint(self, AL=None, AH=None, deadline=None):
        """Returns (AL, AH); raises Refuted.  The conflicts stay in self."""
        I = self.I
        if AL is None:
            AL, AH = I.ALL, I.ALL
        AL, AH, _ = self.closure(AL, AH)
        while True:
            changed = False
            self.stats["sweeps"] += 1
            for n in self.nodes_with_partner(AL, AH):
                x = n >> 1
                if n & 1:
                    if not AH >> x & 1:
                        continue
                elif not AL >> x & 1:
                    continue
                self.stats["probes"] += 1
                try:
                    L2, H2, _ = self.closure(AL, AH, (n,))
                except Refuted:
                    self.stats["kills"] += 1
                    if n & 1:
                        AH &= ~(1 << x)
                    else:
                        AL &= ~(1 << x)
                    AL, AH, _ = self.closure(AL, AH)
                    changed = True
                    continue
                for y in bits(AL & ~L2):
                    if self.add_conflict(n, 2 * y):
                        changed = True
                        self.stats["conflicts"] += 1
                for y in bits(AH & ~H2):
                    if self.add_conflict(n, 2 * y + 1):
                        changed = True
                        self.stats["conflicts"] += 1
            if not changed:
                return AL, AH
            if deadline is not None:
                import time
                if time.time() > deadline:
                    raise TimeoutError()


def cl2_pass(I, deadline=None):
    c = CL2(I)
    try:
        c.fixpoint(deadline=deadline)
        return True, c
    except Refuted:
        return False, c
