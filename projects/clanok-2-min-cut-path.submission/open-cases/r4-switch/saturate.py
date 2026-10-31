"""Adversarial instances for the certificate theorem: start from a planted path (gen.planted, all cross pairs
forward), then add extra contact nodes (a new node in a partner X'_a and a member X_c, or in two partners) in random
order, keeping a contact only if the planted path stays a shortest valid path.  Saturated instances have partners
with as many contacts as shortness allows.  Then the constructive proof (prove.certificate) is run on every shortest
valid path.  Usage: python saturate.py SEED COUNT LMIN LMAX [PPART]"""
import sys
import random
import time

import sw
import gen
import prove
from test_prove import run_one


def shortest_len(inst, cap):
    L, paths = sw.shortest_valid_paths(inst, limit=1, maxlen=cap)
    return L


def add_node(inst, sid1, sid2):
    N, E, F, s, t = inst
    E, F = list(E), list(F)
    for sid in (sid1, sid2):
        w, typ = sid >> 1, sid & 1
        if typ:
            F[w] |= 1 << N
        else:
            E[w] |= 1 << N
    return (N + 1, E, F, s, t)


def saturate(rng, word, ppart=0.2):
    mode = rng.choice(["f", "b", "fb"])
    inst, P = gen.planted(word, None, lambda p, q: rng.choice(mode))
    L0 = shortest_len(inst, len(P))
    if L0 != len(P):
        return None, None
    r = len(P)
    cands = []
    for a in range(r):
        for c in range(r):
            if c != a and abs(c - a) >= 1:
                cands.append((P[a] ^ 1, P[c]))
    for a in range(r):
        for b in range(a + 2, r):
            if rng.random() < ppart:
                cands.append((P[a] ^ 1, P[b] ^ 1))
    rng.shuffle(cands)
    for x, y in cands:
        if sw.side_mask(inst, x) & sw.side_mask(inst, y):
            continue
        inst2 = add_node(inst, x, y)
        L = shortest_len(inst2, r)
        if L is not None and L < r:
            continue
        inst = inst2
    return inst, P


if __name__ == "__main__":
    seed, count, lmin, lmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    ppart = float(sys.argv[5]) if len(sys.argv) > 5 else 0.2
    rng = random.Random(seed)
    stats = dict(yes=0, no=0, paths=0, fail=0, maxdom=0, maxsing=0, maxstore=0)
    t0 = time.time()
    tried = 0
    for it in range(count):
        L = rng.randint(lmin, lmax)
        word = "".join(rng.choice("EF") for _ in range(L))
        inst, P = saturate(rng, word, ppart)
        if inst is None:
            continue
        tried += 1
        assert sw.p2_ok(inst)
        run_one(inst, stats, word)
    print("seed", seed, "saturated", tried, stats, "%.1fs" % (time.time() - t0), flush=True)
