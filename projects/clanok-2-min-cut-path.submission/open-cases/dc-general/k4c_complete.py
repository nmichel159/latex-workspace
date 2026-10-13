"""Search for a P2 completion of the K4 encoding with classes (k4c.py) that keeps the answer 'no'.

Connectors are private new nodes (a private node joins only the two sides it is added to; reusing an existing node
or putting one node into more sides only adds connectivity, so private nodes are the best case for keeping 'no').
Pairs e-e get their node in the empty F-sides, pairs f-f in the empty E-sides ('dead-dead', harmless by Lemma D of
dc-hardness.md with ties).  Every remaining pair (e(sigma), f(sigma')) needs option A (node in F(e(sigma)), which is
empty, and in the route side F(f(sigma'))) or option B (node in the route side E(e(sigma)) and in E(f(sigma')), which
is empty).  The answer is monotone in the connectors, so a depth-first search with forced choices (an option whose
addition alone makes the instance a yes-instance is excluded) decides whether a completion exists.
Usage: python k4c_complete.py [ORDER_SEED]
"""
import sys
import random
import time
import itertools
import gzz
import tools
import k4c


def add_node(inst, pairs):
    """pairs: list of (member, type) to receive one new private node."""
    N, E, F, cls, s, t = inst
    E, F = list(E), list(F)
    z = N
    for m, T in pairs:
        if T == 0:
            E[m] |= 1 << z
        else:
            F[m] |= 1 << z
    return (N + 1, E, F, cls, s, t)


def main():
    oseed = int(sys.argv[1]) if len(sys.argv) > 1 else None
    order = None
    if oseed is not None:
        rng = random.Random(oseed)
        order = {}
        for p in range(4):
            for c in range(3):
                nb = [q for q in range(4) if q != p]
                rng.shuffle(nb)
                order[(p, c)] = nb
    inst, info = k4c.build(order=order)
    mlab = info["mlab"]
    n = len(inst[1])
    # dead-dead connectors
    for i, l in gzz.p2_missing(inst):
        ki, kl = mlab[i][1], mlab[l][1]
        if ki == "e" and kl == "e":
            inst = add_node(inst, [(i, 1), (l, 1)])
        elif ki == "f" and kl == "f":
            inst = add_node(inst, [(i, 0), (l, 0)])
    rest = gzz.p2_missing(inst)
    print("after dead-dead connectors: answer", tools.bb_solve(inst) is not None, "; e-f pairs left:", len(rest),
          flush=True)

    def opt(inst, i, l, which):
        e, f = (i, l) if mlab[i][1] == "e" else (l, i)
        if which == "A":
            return add_node(inst, [(e, 1), (f, 1)])
        return add_node(inst, [(e, 0), (f, 0)])

    t0 = time.time()
    calls = [0]

    def options(inst, pairs):
        res = {}
        for p in pairs:
            ok = []
            for w in "AB":
                calls[0] += 1
                if tools.bb_solve(opt(inst, p[0], p[1], w)) is None:
                    ok.append(w)
            res[p] = ok
        return res

    best = [len(rest)]

    def dfs(inst, pairs, depth):
        if not pairs:
            return inst
        res = options(inst, pairs)
        pairs = sorted(pairs, key=lambda p: len(res[p]))
        p = pairs[0]
        if len(pairs) < best[0]:
            best[0] = len(pairs)
            print("depth", depth, "pairs left", len(pairs), "options of the hardest:", res[p],
                  "calls", calls[0], "%.0fs" % (time.time() - t0), flush=True)
        if not res[p]:
            return None
        for w in res[p]:
            r = dfs(opt(inst, p[0], p[1], w), pairs[1:], depth + 1)
            if r is not None:
                return r
        return None

    out = dfs(inst, rest, 0)
    if out is None:
        print("NO P2 completion exists (with private connectors, dead-dead choice for e-e and f-f pairs)")
    else:
        print("P2 completion found; P2:", gzz.p2_ok(out), "answer:", tools.bb_solve(out) is not None)
        z, _ = gzz.to_zz(out)
        L0 = tools.shortest_relaxed_L(z)
        print("L0", L0, "AC", tools.ac_L(z, L0), "PC", tools.pc_L(z, L0), flush=True)
        print(gzz.fmt(out))


if __name__ == "__main__":
    main()
