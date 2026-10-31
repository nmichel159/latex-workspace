"""Theorem NG (r4-general.md, Section 2): neighbourhood generators.

For pins Gamma (direct generators), Pi (piercers) and Y (exceptions):
    G = (Gamma | N^-(Pi)) - down(Y + {u}),   D = Q - up(G + {v}),
N^-(Pi) = elements with an R-neighbour in Pi strictly above them.  D is always a down-set with u in D, v not in D, so
a u-v path of G_D is a solution (sound for every choice).  The search NG(budget, s) tries all Gamma, Pi with
|Gamma| + |Pi| <= budget and all Y = Y0 + Y1 with Y0 a set of at most 2|Pi| valley-capable elements of N^-(Pi) and
Y1 a set of at most s valley-capable elements; the dual search runs the same on the reversed instance.
"""
import itertools
from common_r4 import gcert, bits, dual


def _prep(I):
    full = (1 << I.n) - 1
    peakcap = [x for x in range(I.n) if I.lo[x] and not (I.B >> x) & 1]
    valcap_mask = sum(1 << x for x in range(I.n) if I.hi[x] and not (I.T >> x) & 1 and not (I.B >> x) & 1)
    pin_cands = [x for x in range(I.n) if I.lo[x] and not (I.B >> x) & 1]
    return full, peakcap, valcap_mask, pin_cands


def d_of(I, Gm, Pi, Y):
    """D(Gamma, Pi, Y) as a bit mask (Gm: mask of Gamma, Pi: list, Y: list)."""
    NM = 0
    for p in Pi:
        NM |= I.lo[p]
    dY = I.down[I.u]
    for y in Y:
        dY |= I.down[y]
    G = (Gm | NM) & ~dY
    U = I.up[I.v]
    for g in bits(G):
        U |= I.up[g]
    return ((1 << I.n) - 1) & ~U


def ng_search(I, budget=2, s=0, y0max=None, stats=None, want=True):
    """Peak-side search.  Returns (D, path, (Gamma, Pi, Y)) for the first success, or None."""
    full, peakcap, valcap, pin_cands = _prep(I)
    seen = set()
    tried = 0
    for size in range(0, budget + 1):
        for ng in range(0, size + 1):
            npi = size - ng
            for Gam in itertools.combinations(peakcap, ng):
                Gm = 0
                for g in Gam:
                    Gm |= 1 << g
                for Pi in itertools.combinations(pin_cands, npi):
                    NM = 0
                    for p in Pi:
                        NM |= I.lo[p]
                    y0c = bits(NM & valcap)
                    k0 = 2 * npi if y0max is None else min(2 * npi, y0max)
                    y1c = bits(valcap)
                    for a in range(0, k0 + 1):
                        for Y0 in itertools.combinations(y0c, a):
                            for b in range(0, s + 1):
                                for Y1 in itertools.combinations(y1c, b):
                                    Y = list(Y0) + list(Y1)
                                    D = d_of(I, Gm, Pi, Y)
                                    if D in seen:
                                        continue
                                    seen.add(D)
                                    tried += 1
                                    path = gcert.cut_path(I, D)
                                    if path is not None:
                                        if stats is not None:
                                            stats["tried"] = tried
                                        return D, path, (list(Gam), list(Pi), Y)
    if stats is not None:
        stats["tried"] = tried
    return None


def ng(I, budget=2, s=0, both=True, stats=None):
    """Peak side, then valley side (dual instance).  Returns (side, D, path, pins) or None.  For the valley side the
    returned D is converted back to a down-set of I (complement of the dual down-set)."""
    r = ng_search(I, budget, s, stats=stats)
    if r is not None:
        return ("peak",) + r
    if both:
        J = dual(I)
        r = ng_search(J, budget, s, stats=stats)
        if r is not None:
            Dd, path, pins = r
            D = ((1 << I.n) - 1) & ~Dd
            return ("valley", D, path[::-1], pins)
    return None
