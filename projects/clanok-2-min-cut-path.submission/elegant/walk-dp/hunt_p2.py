"""Adversarial hunt for a no-instance with P2 on which singleton consistency passes.

Start from a no-instance without P2 on which singleton consistency passes (K4 encoding, small random instances).  Repair the P2 violations one by one, by an order relation between the two
elements, by a private top or bottom witness, or by edges to an existing element above or below both.  A move is kept only if the instance stays a no-instance (exact solver) and
singleton consistency still passes.  Objective: zero violations, which would refute the conjecture.

Usage: hunt_p2.py SEED SECONDS LOG
"""
import json
import random
import sys
import time
from collections import Counter

from wd import Budget, Inst, bits
from closure import Graph, Refuted, exact_alive, sac
import oldfam


def transitive(up):
    up = list(up)
    ch = True
    while ch:
        ch = False
        for i in range(len(up)):
            for j in bits(up[i]):
                if up[j] & ~up[i]:
                    up[i] |= up[j]
                    ch = True
    return up


def make(up, edges, u, v):
    return Inst(len(up), up, edges, u, v)


def sac_pass(I):
    G = Graph(I)
    try:
        sac(G, I.ALL, I.ALL)
        return True
    except Refuted:
        return False


def random_start(rng):
    kind = rng.random()
    if kind < 0.25:
        import k4
        import zz
        import hunt2
        inst = k4.build()
        z = zz.from_sw(*hunt2.ch_to_sw(inst[:5]))
        return oldfam.from_zz(z)
    while True:
        k = rng.randint(4, 16)
        m = k + 2
        p = rng.uniform(0.02, 0.25)
        up = [1 << i for i in range(m)]
        up[0] = (1 << m) - 1
        for i in range(m):
            up[i] |= 2
        for i in range(2, m):
            for j in range(2, m):
                if i != j and rng.random() < p:
                    up[i] |= 1 << j
        up = transitive(up)
        I0 = Inst(m, up, [], 0, 1)
        pairs = [(x, y) for x in range(m) for y in bits(I0.USTR[x])]
        q = rng.uniform(0.05, 0.4)
        edges = {e for e in pairs if rng.random() < q}
        I = Inst(m, up, edges, 0, 1)
        if not I.lt(0, 1):
            continue
        if (0, 1) in edges:
            edges.discard((0, 1))
            I = Inst(m, up, edges, 0, 1)
        if I.shortest_walk() is None and sac_pass(I):
            return I


def try_move(I, x, y, rng):
    """One repair of the violating pair (x, y).  Returns a new instance or None."""
    kind = rng.choice(["rel", "rel", "top", "bot", "exist", "exist"])
    up = list(I.UP)
    edges = set(I.edges)
    m = I.m
    if kind == "rel":
        a, b = (x, y) if rng.random() < 0.5 else (y, x)
        for p in bits(I.DN[a]):
            up[p] |= I.UP[b]
        J0 = Inst(m, up, [], I.u, I.v)
        if not J0.lt(I.u, I.v):
            return None
        for e in edges:
            if not J0.lt(*e):
                return None
    elif kind == "top":
        b = 1 << m
        for p in range(m):
            up[p] |= b
        up.append(I.CL[I.v] | b)
        for z in bits(I.CL[I.v]):
            up[z] |= b
        edges |= {(x, m), (y, m)}
        m += 1
    elif kind == "bot":
        b = 1 << m
        up.append((1 << (m + 1)) - 1)
        for z in bits(I.CL[I.u]):
            up[z] |= b
        edges |= {(m, x), (m, y)}
        m += 1
    else:
        above = I.USTR[x] & I.USTR[y]
        below = I.DSTR[x] & I.DSTR[y]
        c = list(bits(above)) + list(bits(below))
        if not c:
            return None
        z = rng.choice(c)
        if I.lt(x, z):
            edges |= {(x, z), (y, z)}
        else:
            edges |= {(z, x), (z, y)}
    return Inst(m, up, edges, I.u, I.v)


def main():
    seed, secs, logf = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    rng = random.Random(seed)
    t0 = time.time()
    st = Counter()
    best = None
    found = []
    while time.time() - t0 < secs:
        I = random_start(rng)
        st["starts"] += 1
        viol = I.p2_violations()
        v0 = len(viol)
        fails = 0
        while viol and fails < 60 and time.time() - t0 < secs:
            x, y = rng.choice(viol)
            J = try_move(I, x, y, rng)
            if J is None:
                fails += 1
                continue
            try:
                if J.shortest_walk(budget=200000) is not None:
                    fails += 1
                    st["rej yes"] += 1
                    continue
            except Budget:
                fails += 1
                st["rej budget"] += 1
                continue
            if not sac_pass(J):
                fails += 1
                st["rej sac refutes"] += 1
                continue
            I = J
            viol = I.p2_violations()
            fails = 0
            st["accepted"] += 1
        n = len(viol)
        st["end viol 0" if n == 0 else "end viol >0"] += 1
        if best is None or n < best[0]:
            best = (n, I.m, v0)
            data = dict(m=I.m, up=[hex(x) for x in I.UP], edges=sorted(I.edges), u=I.u, v=I.v, viol=n)
            with open(logf + ".best.json", "w", encoding="utf-8") as f:
                json.dump(data, f)
        if n == 0:
            found.append(dict(m=I.m, up=[hex(x) for x in I.UP], edges=sorted(I.edges), u=I.u, v=I.v))
            with open(logf + ".FOUND.json", "w", encoding="utf-8") as f:
                json.dump(found, f)
        with open(logf, "w", encoding="utf-8") as f:
            print("time", round(time.time() - t0), "best (viol, m, viol at start)", best, dict(sorted(st.items())), file=f)


if __name__ == "__main__":
    main()
