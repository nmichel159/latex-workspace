"""Planted paths with mates (agent r5-classes, r5-classes.md section 3.1).

Base: an abstract planted path (typ, cont) of hyp_h.py, realised with private nodes; every member is its own class.
Mates: for a member a (type t = typ[a]) a switch in the class of a with
  same-type side Z' (type t): a private node shared with X'_q for every member q of the other type (P2 with q by
  the type-t sides), the hub node of the type-t mates, and, for a *local* mate at b0, a private node of X_{b0};
  other side Z (type 1 - t): a private node shared with X'_b for every member b != a of type t other than b0.
P2 between mates of different classes: same type: the hub; different types: a random *cell*, either Z'_1 meets the
other side of mate 2 (cell 'same1') or the other side of mate 1 meets Z'_2 (cell 'same2'), by a private node.
"""
import random
import sys
import ccore as C
import cfam
import hyp_h as H


def build(typ, cont, mates, rng, pcell=0.5):
    """mates: list of (a, b0) with a a member index, b0 None (dead mate) or a member index of type typ[a]."""
    B = cfam.Builder()
    r = len(typ)
    xs = [B.switch(("x", j), cls=("x", j)) for j in range(r)]

    def mem(j, *nm):
        B.add(xs[j], typ[j], *nm)

    def par(j, *nm):
        B.add(xs[j], 1 - typ[j], *nm)
    mem(0, "s")
    mem(r - 1, "t")
    for j in range(r - 1):
        mem(j, ("y", j))
        mem(j + 1, ("y", j))
    for a in range(r):
        for c in cont[a]:
            par(a, ("z", a, c))
            mem(c, ("z", a, c))
    for a in range(r):
        for b in range(a + 2, r):
            if typ[a] == typ[b]:
                par(a, ("w", a, b))
                par(b, ("w", a, b))
    fwd = [bool(cont[j]) and min(cont[j]) > j for j in range(r)]
    bwd = [bool(cont[j]) and max(cont[j]) < j for j in range(r)]
    ms = []
    for i, (a, b0) in enumerate(mates):
        t = typ[a]
        m = B.switch(("m", i), cls=("x", a))
        ms.append((m, a, t))
        B.add(m, t, ("hub", t))
        for q in range(r):
            if typ[q] != t:
                nm = ("mq", i, q)
                safe = b0 is None or (q < b0 and not bwd[q]) or (q > b0 and not fwd[q])
                if safe:
                    B.add(m, t, nm)          # Z' meets X'_q (type t)
                    par(q, nm)
                else:
                    B.add(m, 1 - t, nm)      # Z meets X_q (type 1 - t)
                    mem(q, nm)
        for b in range(r):
            if typ[b] == t and b != a and b != b0:
                nm = ("mb", i, b)
                B.add(m, 1 - t, nm)
                par(b, nm)
        if b0 is not None:
            nm = ("loc", i)
            B.add(m, t, nm)
            mem(b0, nm)
    for i in range(len(ms)):
        for j in range(i + 1, len(ms)):
            m1, a1, t1 = ms[i]
            m2, a2, t2 = ms[j]
            if a1 == a2 or t1 == t2:
                continue
            nm = ("cell", i, j)
            if rng.random() < pcell:
                B.add(m1, t1, nm)        # Z'_1 (type t1) and other side of m2 (type 1 - t2 = t1)
                B.add(m2, 1 - t2, nm)
            else:
                B.add(m1, 1 - t1, nm)    # other side of m1 (type t2) and Z'_2 (type t2)
                B.add(m2, t2, nm)
    I = B.inst()
    P = tuple(2 * xs[j] + typ[j] for j in range(r))
    return I, P


def check(I, P):
    L, paths = C.shortest_valid_paths(I, limit=1, maxlen=len(P))
    return C.p2_ok(I), (L == len(P))


if __name__ == "__main__":
    import cdesc2 as D
    seed = int(sys.argv[1])
    W = sys.argv[2]
    nm = int(sys.argv[3])
    loc = sys.argv[4] if len(sys.argv) > 4 else "dead"
    rng = random.Random(seed)
    typ, cont = H.rword_start(W)
    r = len(typ)
    mates = []
    for i in range(nm):
        a = rng.randrange(r)
        b0 = None
        if loc == "local":
            cands = [b for b in range(r) if typ[b] == typ[a] and b != a]
            b0 = rng.choice(cands) if cands else None
        mates.append((a, b0))
    I, P = build(typ, cont, mates, rng)
    p2, sh = check(I, P)
    sols = D.solutions_masks(I)
    print("W", W, "mates", mates, "P2", p2, "P shortest", sh, "classes", I.k, "sides", len(I.sides),
          "solutions", len(sols), flush=True)
    for f, g in ((0, 1), (1, 0), (1, 1), (2, 1)):
        print("  desc_cost", f, g, D.desc_cost(I, f, g, sols, want=True), flush=True)
