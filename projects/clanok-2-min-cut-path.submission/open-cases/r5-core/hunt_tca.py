"""Adversarial hill climbing against TCA (r5-core.md Section 5.3).

State: a planted path of r members (word of types) with links (nodes in two sides) and, in the general mode, order
relations between members (never an E-member below an F-member, so the planted path stays valid).  Every candidate is
realised (gplant), and kept only if P2 holds and the planted path is a shortest valid path.  Objective: the least TCA
cost (tca.py, distance DIST) over the shortest valid paths (at most LIMIT of them); ties broken by the least ADESC
guided cost of the planted path.

usage: python hunt_tca.py SEED RUNS R STEPS [sw|gen] [DIST] [log]
"""
import random
import sys
import time
from gplant import GPlanted
import tca

LIMIT = 30


class State:
    def __init__(self, typ):
        self.typ = list(typ)
        self.r = len(typ)
        self.links = set()      # ((u, tu), (v, tv)) canonical, u-side < v-side
        self.rel = set()        # (a, b): a < b, members only

    def copy(self):
        o = State(self.typ)
        o.links = set(self.links)
        o.rel = set(self.rel)
        return o

    @staticmethod
    def canon(x, y):
        return (x, y) if x <= y else (y, x)

    def mem(self, a):
        return (a, self.typ[a])

    def par(self, a):
        return (a, 1 - self.typ[a])

    def realise(self):
        pl = GPlanted(self.typ)
        for (x, y) in sorted(self.links):
            pl.link(x, y)
        for (a, b) in sorted(self.rel):
            pl.le(a, b)
        return pl.realise()


def base_state(rng, r):
    while True:
        typ = [rng.randrange(2) for _ in range(r)]
        if 0 < sum(typ) < r:
            break
    st = State(typ)
    for a in range(r):
        for b in range(a + 1, r):
            if typ[a] == typ[b]:
                if b >= a + 2:
                    st.links.add(State.canon(st.par(a), st.par(b)))
            else:
                st.links.add(State.canon(st.par(a), st.mem(b)))     # forward contact of the earlier member
    return st


def valid_rel(st, a, b):
    """may we add a < b?  (closure must not put an E-member below an F-member, and no cycle)"""
    rel = set(st.rel) | {(a, b)}
    r = st.r
    le = [[i == j for j in range(r)] for i in range(r)]
    for (x, y) in rel:
        le[x][y] = True
    for k in range(r):
        for i in range(r):
            if le[i][k]:
                for j in range(r):
                    if le[k][j]:
                        le[i][j] = True
    for i in range(r):
        for j in range(r):
            if i != j and le[i][j] and le[j][i]:
                return False
            if i != j and le[i][j] and st.typ[i] == 0 and st.typ[j] == 1:
                return False
    return True


def evaluate(st, dist):
    G, P = st.realise()
    if G.p2_bad():
        return None
    if not G.is_valid_walk(P):
        return None
    L, _ = G.shortest()
    if L != st.r:
        return None
    paths = G.all_shortest(limit=LIMIT, length=L)
    best = None
    for Q in paths:
        v = tca.tca_path(G, Q, check=False, dist=dist)["tca"]
        if best is None or v < best:
            best = v
    return best


def mutate(rng, st, mode):
    o = st.copy()
    r = st.r
    u = rng.random()
    if u < 0.45:
        a, c = rng.sample(range(r), 2)
        if o.typ[a] != o.typ[c]:
            o.links.add(State.canon(o.par(a), o.mem(c)))
        else:
            o.links.add(State.canon(o.par(a), o.par(c)))
    elif u < 0.8:
        if o.links:
            L = rng.choice(sorted(o.links))
            o.links.discard(L)
    elif mode == "gen":
        if u < 0.92 or not o.rel:
            a, b = rng.sample(range(r), 2)
            if valid_rel(o, a, b):
                o.rel.add((a, b))
        else:
            o.rel.discard(rng.choice(sorted(o.rel)))
    else:
        a, c = rng.sample(range(r), 2)
        o.links.add(State.canon(o.par(a), o.mem(c)) if o.typ[a] != o.typ[c] else State.canon(o.par(a), o.par(c)))
    return o


def main():
    seed, runs, r, steps = (int(x) for x in sys.argv[1:5])
    mode = sys.argv[5] if len(sys.argv) > 5 else "sw"
    dist = int(sys.argv[6]) if len(sys.argv) > 6 else 3
    rng = random.Random(seed)
    t0 = time.time()
    hist = {}
    top = None
    for run in range(runs):
        st = None
        for _ in range(100):
            cand = base_state(rng, r)
            v = evaluate(cand, dist)
            if v is not None:
                st, val = cand, v
                break
        if st is None:
            print("run %d: no start" % run, flush=True)
            continue
        for it in range(steps):
            cand = mutate(rng, st, mode)
            v = evaluate(cand, dist)
            if v is None:
                continue
            if v >= val or rng.random() < 0.02:
                st, val = cand, v
            if (it + 1) % 200 == 0:
                print("  run %d it %d tca %d links %d rel %d (%.0fs)" % (run, it + 1, val, len(st.links), len(st.rel),
                                                                       time.time() - t0), flush=True)
        hist[val] = hist.get(val, 0) + 1
        word = "".join("EF"[x] for x in st.typ)
        print("run %d final tca %d word %s rel %s" % (run, val, word, sorted(st.rel)), flush=True)
        if top is None or val > top[0]:
            top = (val, word, sorted(st.links), sorted(st.rel))
    print("histogram %s" % hist)
    print("top %s" % (top,), flush=True)


if __name__ == "__main__":
    main()
