"""Generator aimed at step (3) of Theorem 8 with rich forward rows: forward zone, critical run R of forward
T-members, backward zone; the cross pairs between R and the backward O-members are drawn as a matrix (p in f(a),
a in b(p), or both); non-tight straddles (which would be shortcuts by Lemma 7) are rejected before the expensive
shortest-path test.  reverse=True reverses the path (s and t swapped), which turns forward rows into backward rows.
"""
import random
from core import Inst, p2
from proof import Ctx, straddles


def gen_run(rng, kw, m, lw, T=None, hub=0.0, pM=0.6, pB=0.2, p_extra=0.0, reverse=False, off=0, off_dens=0.1,
            ensure_backward=True, two_spans=False):
    """kw, lw: words (lists of 'T'/'O') of the forward and backward zones; m: length of the run."""
    if T is None:
        T = rng.randrange(2)
    O = 1 - T
    word = [None] + [T if c == 'T' else O for c in kw] + [T] * m + [T if c == 'T' else O for c in lw]
    kind = [None] + ['F'] * len(kw) + ['F'] * m + ['B'] * len(lw)
    r = len(word) - 1
    k = len(kw)
    Rpos = list(range(k + 1, k + m + 1))
    Bz = [q for q in range(k + m + 1, r + 1) if word[q] == O]
    N = [2]

    def new():
        N[0] += 1
        return N[0] - 1
    ys = [0] + [new() for _ in range(r - 1)] + [1]
    X = [None] + [{ys[a - 1], ys[a]} for a in range(1, r + 1)]
    Xp = [None] + [set() for _ in range(r)]

    def allowed(a, c):
        if kind[a] == 'F':
            return c >= a + 1
        if kind[a] == 'B':
            return c <= a - 1
        return abs(c - a) == 1

    # matrix for R x backward O-members
    mat = {}
    if two_spans and len(Bz) >= 6 and m >= 2:
        # two groups of rows with disjoint spans: left rows contact the left half, right rows the right half
        half = rng.randint(3, len(Bz) - 3)
        cut = rng.randint(1, m - 1)
        orient = rng.random() < 0.5
        for i, a in enumerate(Rpos):
            for j, q in enumerate(Bz):
                same = (j < half) == (i < cut)
                inside = same if orient else not same
                if inside:
                    u = rng.random()
                    mat[(a, q)] = (1, 0) if u < pM else ((1, 1) if u < pM + pB else (0, 1))
                else:
                    mat[(a, q)] = (0, 1)
    else:
        for a in Rpos:
            for q in Bz:
                u = rng.random()
                if u < pM:
                    mat[(a, q)] = (1, 0)
                elif u < pM + pB:
                    mat[(a, q)] = (1, 1)
                else:
                    mat[(a, q)] = (0, 1)
    hubs = {}
    for a in range(1, r + 1):
        for b in range(a + 1, r + 1):
            if word[a] == word[b]:
                if b - a >= 2:
                    if rng.random() < hub:
                        key = (word[a], rng.randrange(3))
                        if key not in hubs:
                            hubs[key] = new()
                        x = hubs[key]
                    else:
                        x = new()
                    Xp[a].add(x)
                    Xp[b].add(x)
                continue
            if (a, b) in mat:
                ch = mat[(a, b)]          # (b in f(a), a in b(b))
            else:
                o1, o2 = allowed(a, b), allowed(b, a)
                if not o1 and not o2:
                    return None
                if o1 and o2:
                    ch = rng.choice([(1, 0), (0, 1), (1, 1)])
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
    if ensure_backward:
        for q in range(1, r + 1):
            if kind[q] == 'B' and not any(Xp[q] & X[c] for c in range(1, q - 1)):
                cands = [c for c in range(1, q - 1)]
                if not cands:
                    return None
                c = rng.choice(cands)
                x = new()
                Xp[q].add(x)
                X[c].add(x)
    for a in range(1, r + 1):
        for c in range(1, r + 1):
            if c != a and allowed(a, c) and rng.random() < p_extra:
                x = new()
                Xp[a].add(x)
                X[c].add(x)
    sw = []
    for a in range(1, r + 1):
        sw.append((X[a], Xp[a]) if word[a] == 0 else (Xp[a], X[a]))
    for _ in range(off):
        E = {x for x in range(N[0]) if rng.random() < off_dens}
        F = {x for x in range(N[0]) if rng.random() < off_dens}
        sw.append((E, F))
    for w in range(len(sw)):
        for v in range(w + 1, len(sw)):
            if not (sw[w][0] & sw[v][0]) and not (sw[w][1] & sw[v][1]):
                typ = rng.randrange(2)
                x = new()
                sw[w][typ].add(x)
                sw[v][typ].add(x)
    s, t = (1, 0) if reverse else (0, 1)
    inst = Inst(N[0], s, t, sw)
    assert p2(inst)
    P = [inst.idx[(a - 1, word[a])] for a in range(1, r + 1)]
    if reverse:
        P = P[::-1]
    ctx = Ctx(inst, P)
    for TT in (0, 1):
        for st in straddles(ctx, TT):
            x, p, x1, x2, p1, p2_ = st
            if not (x1 == x - 1 and x2 == x + 1 and p1 == p - 1 and p2_ == p + 1):
                return None
    return inst, P, T
