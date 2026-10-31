"""Saturation adversary for Hypothesis P (r4-classes.md §2.1) with classes.

Start: planted path of a random type word with a random class assignment (classes of one type only; k classes per
type), P2 links as in r5-classes/plant.base_word (forward or backward contacts for opposite types, partner-partner
links for same-type far pairs of different classes).  Keep it only if the planted path is a shortest valid path.
Then add, in random order, extra links (partner of a meets member c; partner of a meets partner of b) and keep a link
only if the planted path stays shortest.  For every shortest valid path P of the result compute
  hP(P)   = min over types T of: 0 if the T-members lie in at most 3 classes, else
            min over T-members u, b of different classes, |u - b| >= 3, of |f(u) | f(b)|;
  hErr(P) = the same with |f(u) | f(b)| replaced by the number of O-classes all of whose members on P lie in
            f(u) | f(b) (the misclassification of Lemma PP of r5-classes once dead mates are added).
Usage: python satc.py SEED COUNT LMIN LMAX KCLS [PPART]"""
import os
import sys
import random
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "r5-classes"))
import ccore as C  # noqa: E402
import plant  # noqa: E402


def fsets(I, P):
    r = len(P)
    out = []
    for a in range(r):
        x = P[a]
        m = I.mask.get(x ^ 1, 0)
        out.append({c for c in range(r) if c != a and (P[c] & 1) != (x & 1) and (m & I.mask[P[c]])})
    return out


def _pairs_cost(I, P, use_err):
    f = fsets(I, P)
    r = len(P)
    cl = [I.cl[x >> 1] for x in P]
    best = None
    for T in (0, 1):
        mem = [a for a in range(r) if (P[a] & 1) == T]
        if len(set(cl[a] for a in mem)) <= 3:
            return 0
        omem = {}
        for c in range(r):
            if (P[c] & 1) != T:
                omem.setdefault(cl[c], set()).add(c)
        for i, u in enumerate(mem):
            for b in mem[i + 1:]:
                if b - u >= 3 and cl[u] != cl[b]:
                    U = f[u] | f[b]
                    if use_err:
                        v = sum(1 for D, ms in omem.items() if ms <= U)
                    else:
                        v = len(U)
                    if best is None or v < best:
                        best = v
    return best


def hP(I, P):
    return _pairs_cost(I, P, False)


def hErr(I, P):
    return _pairs_cost(I, P, True)


def shortest_ok(pl):
    I, P = pl.realise()
    L, paths = C.shortest_valid_paths(I, limit=1, maxlen=pl.r)
    return L == pl.r


def saturate(rng, word, kcls, ppart=0.3):
    typ = [0 if ch == "E" else 1 for ch in word]
    cls = [("E", rng.randrange(kcls)) if t == 0 else ("F", rng.randrange(kcls)) for t in typ]
    pl = plant.base_word(word, cls, forward=rng.random() < 0.5)
    if not shortest_ok(pl):
        return None
    r = pl.r
    cands = []
    for a in range(r):
        for c in range(r):
            if c != a:
                cands.append((a, 1 - typ[a], c, typ[c]))
        for b in range(a + 2, r):
            if rng.random() < ppart:
                cands.append((a, 1 - typ[a], b, 1 - typ[b]))
    rng.shuffle(cands)
    for (u, tu, v, tv) in cands:
        L = plant.Planted.canon(u, tu, v, tv)
        if L in pl.links:
            continue
        pl.links.add(L)
        if not shortest_ok(pl):
            pl.links.discard(L)
    return pl


if __name__ == "__main__":
    seed, count, lmin, lmax, kcls = (int(x) for x in sys.argv[1:6])
    ppart = float(sys.argv[6]) if len(sys.argv) > 6 else 0.3
    rng = random.Random(seed)
    hist = {}
    worst = None
    n = 0
    t0 = time.time()
    for it in range(count):
        L = rng.randint(lmin, lmax)
        word = "".join(rng.choice("EF") for _ in range(L))
        pl = saturate(rng, word, kcls, ppart)
        if pl is None:
            continue
        n += 1
        I, P0 = pl.realise()
        assert C.p2_ok(I)
        Ls, paths = C.shortest_valid_paths(I, limit=20)
        for P in paths:
            v = (hP(I, P), hErr(I, P))
            hist[v] = hist.get(v, 0) + 1
            if worst is None or v[1] > worst[0][1]:
                worst = (v, word, [I.cl[x >> 1] for x in P])
    print("seed", seed, "kcls", kcls, "instances", n, "(hP, hErr) histogram", dict(sorted(hist.items())),
          "worst by hErr", worst, "%.1fs" % (time.time() - t0), flush=True)
