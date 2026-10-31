"""Planted-path generators designed to reach step (3) of Theorem 8 and to produce straddles.

A planted instance has path switches 1..r with path sides X_a = {y_{a-1}, y_a} (y_0 = s, y_r = t) of a prescribed
type word, intended kinds (forward zone, critical run with forward then backward members, backward zone), every P2
requirement met by a private node (or, with probability hub, by a shared hub node), extra contacts that respect the
intended kinds, and optional off-path switches.  The planted path is kept only if it is a shortest valid path.
"""
import random
from core import Inst, shortest_valid_paths, p2


class Builder:
    def __init__(self):
        self.N = 2
        self.sets = {}

    def node(self):
        self.N += 1
        return self.N - 1


def gen_planted(rng, k, m1, m2, l, T=None, zone_T=0.0, hub=0.0, p_contact=0.8, p_both=0.2, p_extra=0.1,
                off=0, off_dens=0.15, straddle=0):
    """Word: forward zone of length k, critical run of m1 forward and m2 backward T-members, backward zone of
    length l.  Zones consist of O-members, each position turned into a T-member with probability zone_T."""
    if T is None:
        T = rng.randrange(2)
    O = 1 - T
    word, kind = [], []
    for _ in range(k):
        word.append(T if rng.random() < zone_T else O)
        kind.append('F')
    for _ in range(m1):
        word.append(T)
        kind.append('F')
    for _ in range(m2):
        word.append(T)
        kind.append('B')
    for _ in range(l):
        word.append(T if rng.random() < zone_T else O)
        kind.append('B')
    r = len(word)
    if r < 1:
        return None
    word = [None] + word
    kind = [None] + kind
    N = [2]

    def new():
        N[0] += 1
        return N[0] - 1
    ys = [0] + [new() for _ in range(r - 1)] + [1]
    X = [None] + [{ys[a - 1], ys[a]} for a in range(1, r + 1)]
    Xp = [None] + [set() for _ in range(r)]

    def allowed(a, c):
        """May c be a contact of a under the intended kinds?"""
        if kind[a] == 'F':
            return c >= a + 1
        if kind[a] == 'B':
            return c <= a - 1
        return abs(c - a) == 1

    hubs = {}
    for a in range(1, r + 1):
        for b in range(a + 1, r + 1):
            if word[a] == word[b]:
                if b - a >= 2:
                    if rng.random() < hub:
                        key = (word[a], rng.randrange(2))
                        if key not in hubs:
                            hubs[key] = new()
                        x = hubs[key]
                    else:
                        x = new()
                    Xp[a].add(x)
                    Xp[b].add(x)
            else:
                o1 = allowed(a, b)
                o2 = allowed(b, a)
                if not o1 and not o2:
                    return None
                if o1 and o2:
                    u = rng.random()
                    if u < p_both:
                        ch = (1, 1)
                    elif u < p_both + (1 - p_both) * p_contact:
                        # prefer a contact of the T-member (it raises |f(a)|)
                        ch = (1, 0) if word[a] == T else (0, 1)
                    else:
                        ch = (0, 1) if word[a] == T else (1, 0)
                else:
                    ch = (1 if o1 else 0, 1 if o2 else 0)
                if ch[0]:
                    x = new()
                    Xp[a].add(x)
                    X[b].add(x)
                if ch[1]:
                    x = new()
                    Xp[b].add(x)
                    X[a].add(x)
    for a in range(1, r + 1):
        for c in range(1, r + 1):
            if c != a and allowed(a, c) and rng.random() < p_extra:
                x = new()
                Xp[a].add(x)
                X[c].add(x)
    # planted straddles: x (T) and p (O) with x-1, x+1 T-members and p-1, p+1 O-members
    for _ in range(straddle):
        xs = [a for a in range(2, r) if word[a] == T and word[a - 1] == T and word[a + 1] == T]
        ps = [a for a in range(2, r) if word[a] == O and word[a - 1] == O and word[a + 1] == O]
        cand = [(x, p) for x in xs for p in ps if abs(x - p) >= 3]
        if not cand:
            break
        x, p = rng.choice(cand)
        for c in (x - 1, x + 1):
            z = new()
            Xp[p].add(z)
            X[c].add(z)
        for c in (p - 1, p + 1):
            z = new()
            Xp[x].add(z)
            X[c].add(z)
    sw = []
    for a in range(1, r + 1):
        if word[a] == 0:
            sw.append((X[a], Xp[a]))
        else:
            sw.append((Xp[a], X[a]))
    # off-path switches
    for _ in range(off):
        E = {x for x in range(N[0]) if rng.random() < off_dens}
        F = {x for x in range(N[0]) if rng.random() < off_dens}
        sw.append((E, F))
    # P2 repair with private nodes
    for w in range(len(sw)):
        for v in range(w + 1, len(sw)):
            if not (sw[w][0] & sw[v][0]) and not (sw[w][1] & sw[v][1]):
                typ = rng.randrange(2)
                x = new()
                sw[w][typ].add(x)
                sw[v][typ].add(x)
    inst = Inst(N[0], 0, 1, sw)
    assert p2(inst)
    P = [inst.idx[(a - 1, word[a])] for a in range(1, r + 1)]
    return inst, P, T


def is_shortest(inst, P):
    L, _ = shortest_valid_paths(inst, limit=1, maxlen=len(P) - 1) if len(P) > 1 else (None, [])
    return L is None


def saturate(rng, inst, P, tries, max_add=1):
    """Add random memberships (an existing node to a random set, or a new node to two random sets) as long as P stays
    a shortest valid path.  P2 is monotone, so it is kept."""
    sw = [(set(E), set(F)) for E, F in inst.sw]
    N = inst.N
    added = 0
    for _ in range(tries):
        trial = [(set(E), set(F)) for E, F in sw]
        N2 = N
        if rng.random() < 0.5:
            x = rng.randrange(2, N)
            w = rng.randrange(len(trial))
            trial[w][rng.randrange(2)].add(x)
        else:
            x = N2
            N2 += 1
            for _ in range(2):
                w = rng.randrange(len(trial))
                trial[w][rng.randrange(2)].add(x)
        cand = Inst(N2, 0, 1, trial)
        # the path sides must keep their identity (no side may become empty, none does: we only add)
        P2_ = [cand.idx[inst.sides[x]] for x in P]
        from core import is_valid_path
        if not is_valid_path(cand, P2_):
            continue
        if is_shortest(cand, P2_):
            sw, N = trial, N2
            inst, P = cand, P2_
            added += 1
    return inst, P, added
