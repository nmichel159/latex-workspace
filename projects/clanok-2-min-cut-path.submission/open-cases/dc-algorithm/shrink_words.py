"""Rigid switch-model instances for an arbitrary mode word and their greedy shrinking (dc-algorithm.md 11.6).

R(w): switches x_1..x_n in path order, path side h_k of type w[k] ('E' or 'F'), flip side Fl_k of the other type;
nodes s in h_1, t in h_n, y_k in h_k & h_{k+1}; for p < q: z_pq in Fl_p & h_q if w[p] != w[q] (same type then),
w_pq in Fl_p & Fl_q if w[p] == w[q].  P2 holds by construction, and the first-flip argument of dc-hardness.md
Section 2 (a flipped side is entered only from a later path side) shows that the path modes form the only solution.
Usage: python shrink_words.py K SEEDS  (all words with K letters E and K letters F; prints the best size per word)"""
import sys
import json
import random
import itertools
import hunt_antichain as ha


def rigid_word(w):
    n = len(w)
    nodes = {}

    def node(name):
        if name not in nodes:
            nodes[name] = len(nodes)
        return nodes[name]
    s, t = node("s"), node("t")
    h = [0] * n
    fl = [0] * n
    h[0] |= 1 << s
    h[n - 1] |= 1 << t
    for k in range(n - 1):
        y = node(("y", k))
        h[k] |= 1 << y
        h[k + 1] |= 1 << y
    for p in range(n):
        for q in range(p + 1, n):
            if w[p] != w[q]:
                z = node(("z", p, q))
                fl[p] |= 1 << z
                h[q] |= 1 << z
            else:
                x = node(("w", p, q))
                fl[p] |= 1 << x
                fl[q] |= 1 << x
    E = [h[k] if w[k] == "E" else fl[k] for k in range(n)]
    F = [fl[k] if w[k] == "E" else h[k] for k in range(n)]
    return [len(nodes), E, F, s, t]


if __name__ == "__main__":
    K, seeds = int(sys.argv[1]), int(sys.argv[2])
    words = sorted({"".join(p) for p in itertools.permutations("E" * K + "F" * K)})
    overall = None
    for w in words:
        inst = rigid_word(w)
        mc = ha.mode_counts(inst)
        okw = ha.ok(inst, K)
        best = None
        for sd in range(seeds):
            small, sz = ha.shrink(random.Random(sd), inst, K)
            if best is None or sz < best[0]:
                best = (sz, small)
        print(w, "rigid ok", okw, "mode counts", mc, "size", ha.zz_size(inst), "-> shrunk", best[0], json.dumps(best[1]),
              flush=True)
        if overall is None or best[0] < overall[0]:
            overall = (best[0], w, best[1])
    print("BEST", overall[0], overall[1], json.dumps(overall[2]), flush=True)
