"""Candidate counterexample to the strong form of O4: a minimum u-v cut whose only u-v path has length 5.

Vertices x0..x5 = 0..5 (u = x0, v = x5), single-vertex ears a = 6 (x0, x2), b = 7 (x0, x4), c = 8 (x1, x5),
d = 9 (x3, x5).  A = {x0, x2, x4, a, b}.  Also the family with path length 2k+1 (cliques on both sides).
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dctools as T
import mcp


def example10():
    E = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5),
         (0, 2), (0, 4), (1, 5), (3, 5),
         (0, 6), (6, 2), (0, 7), (7, 4), (1, 8), (8, 5), (3, 9), (9, 5)]
    return 10, E, 0, 5


def family(k, cliques=True):
    """Path x0..x_{2k+1}; evens on side A, odds on side B; x0 joined to every even vertex by an edge and by a
    one-vertex ear; v = x_{2k+1} likewise to every odd vertex; with cliques=True the evens form a clique and
    the odds form a clique."""
    L = 2 * k + 1
    n = L + 1
    E = [(i, i + 1) for i in range(L)]
    ev = list(range(0, L + 1, 2))
    od = list(range(1, L + 1, 2))
    u, v = 0, L
    nxt = n
    for x in ev[1:]:
        E.append((u, x))
        E.append((u, nxt)); E.append((nxt, x)); nxt += 1
    for y in od[:-1]:
        E.append((y, v))
        E.append((y, nxt)); E.append((nxt, v)); nxt += 1
    if cliques:
        for a in ev:
            for b in ev:
                if a < b:
                    E.append((a, b))
        for a in od:
            for b in od:
                if a < b:
                    E.append((a, b))
    return nxt, sorted(set((min(a, b), max(a, b)) for a, b in E)), u, v


if __name__ == "__main__":
    n, E, u, v = example10()
    g, info = T.analyse(n, E, u, v)
    print("example10:", T.fmt(info))
    for A, sh, lens in info["cuts_with_path"]:
        print("   cut side", [x for x in range(n) if (A >> x) & 1], "shortest", sh, "lengths", lens)
    for k in (2, 3):
        for cl in (False, True):
            n, E, u, v = family(k, cl)
            g, info = T.analyse(n, E, u, v, want_cp=(n <= 16))
            print("family k=%d cliques=%s:" % (k, cl), T.fmt(info))
            for A, sh, lens in info["cuts_with_path"]:
                print("   cut side", [x for x in range(n) if (A >> x) & 1], "shortest", sh, "lengths", lens)
