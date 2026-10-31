"""Search for instances on which one GDESC term is not enough (r5-core.md Section 8.5).

usage: python hunt_single.py SEED COUNT NMIN NMAX OUTDIR
Random rigid-word designs (test_rgen.make).  An instance is a *candidate* if on every shortest valid path (at most 40)
no single term of the kind used in the proof exists (inter.min_single: least damage of a one-level E-term > 0 and no
one-level F-term).  Candidates are saved as JSON (gen_io) and tested with the exhaustive single-term search
gdesc.decide(G, 1, 1, 2) (any tools, any flags, any anchor, flips among the caught switches), and with pairs of
one-tool terms (idesc2: intersections of two E- or F-terms with one tool, any flag, no anchor, at most 2 flips).
"""
import os
import sys
import json
import random
import time
import itertools
from collections import Counter
from gcore import bits
import gstar
import gdesc
import inter
from test_rgen import make


def save(G, path, extra=None):
    d = dict(N=G.N, s=G.s, t=G.t, E=[str(x) for x in G.E], F=[str(x) for x in G.F],
             le=[[int(b) for b in row] for row in G.le], medge={str(k): v for k, v in G.medge.items()},
             names=[list(n) if isinstance(n, tuple) else n for n in (G.names or [])], extra=extra or {})
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f)


def load(path):
    from gcore import Gen
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    G = Gen(d["N"], [int(x) for x in d["E"]], [int(x) for x in d["F"]], d["le"], d["s"], d["t"],
            medge={int(k): tuple(v) for k, v in d["medge"].items()}, names=[tuple(n) for n in d["names"]])
    return G, d.get("extra", {})


def single_terms(G, St, k=1, e=2):
    """All D of single GDESC terms with <= k tools (any flags), no anchors, flips (<= e) among caught switches."""
    out = set()
    m = G.m
    for kind in (0, 1):
        for kk in range(k + 1):
            for T in itertools.combinations(range(m), kk):
                caught = 0
                for x in T:
                    caught |= St.NEstar[x] if kind == 0 else St.NFstar[x]
                for nfl in range(len(T) + 1):
                    for flags in itertools.combinations(T, nfl):
                        for ne in range(e + 1):
                            for Phi in itertools.combinations(bits(caught), ne):
                                out.add(gdesc.describe(G, St, kind, list(T), list(flags), [],
                                                       sum(1 << w for w in Phi)))
    return out


def idesc2(G, St, e=2):
    """Is there an intersection of two one-tool anchor-free terms (flips <= e) that connects?"""
    terms = list(single_terms(G, St, 1, e))
    for i in range(len(terms)):
        for j in range(i, len(terms)):
            if G.connects(terms[i] & terms[j]):
                return True, (terms[i], terms[j])
    return False, None


def main():
    seed, count, nmin, nmax = (int(a) for a in sys.argv[1:5])
    outdir = sys.argv[5]
    os.makedirs(outdir, exist_ok=True)
    rng = random.Random(seed)
    st = Counter()
    t0 = time.time()
    for it in range(count):
        G, W, pp = make(rng, rng.randint(nmin, nmax))
        if G.p2_bad():
            continue
        Lsh, _ = G.shortest()
        if Lsh is None or Lsh == 0:
            continue
        st["yes"] += 1
        St = gstar.Stars(G)
        paths = G.all_shortest(limit=40, length=Lsh)
        ok = False
        for P in paths:
            ms = inter.min_single(G, P, St)
            if ms["edmg"] == 0 or ms["fone"]:
                ok = True
                break
        if ok:
            continue
        st["candidates"] += 1
        name = os.path.join(outdir, "single-%d-%d.json" % (seed, it))
        d1 = gdesc.decide(G, 1, 1, 2)
        st["decide(1,1,2) accepts"] += bool(d1)
        two = None
        if not d1:
            two, _ = idesc2(G, St, 2)
            st["idesc2 accepts"] += bool(two)
        save(G, name, dict(W=W, paths=len(paths), decide112=bool(d1), idesc2=two))
        print("candidate it=%d m=%d W=%s paths=%d decide(1,1,2)=%s idesc2=%s (%.0fs)" % (
            it, G.m, W, len(paths), bool(d1), two, time.time() - t0), flush=True)
    print("hunt_single seed %d count %d n %d-%d (%.0fs)" % (seed, count, nmin, nmax, time.time() - t0))
    for kk in sorted(st):
        print("  %-30s %s" % (kk, st[kk]))


if __name__ == "__main__":
    main()
