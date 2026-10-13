"""Cross-check of exact.py against the brute-force routines of checks/mcp.py (imported read-only) on all connected
graphs with 2..7 vertices (networkx atlas) and all ordered pairs (u, v).

Compared per pair: c(u,v); the set of minimum cuts (branching, Picard-Queyranne, all vertex sets of mcp);
PATH-IN-MIN-CUT from the cuts versus cp_brute(u,v) == c(u,v) (mcp) versus cp_equals_c_paths with and without the
alternation pruning.  Output: results-exact.txt.
"""

import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "checks")))

import mcp  # noqa: E402  (read-only import)
import exact as ex  # noqa: E402


def main():
    t0 = time.time()
    graphs = mcp.atlas_pairs(2, 7)
    pairs = 0
    fails = []
    yes = 0
    for n, es in graphs:
        g = ex.UG(n, es)
        G = mcp.Gr(n, es)
        for u in range(n):
            for v in range(n):
                if u == v:
                    continue
                pairs += 1
                cb, cuts_b = ex.min_cuts_branch(g, u, v)
                cq, cuts_q = ex.min_cuts_pq(g, u, v)
                cm, masks = mcp.min_cuts_by_sets(G, u, v)
                # mcp gives edge masks; convert ours to edge masks of mcp's numbering (same sorted edge order)
                set_b = sorted(sum(1 << e for e in ex.boundary(g, A)) for A in cuts_b)
                set_q = sorted(sum(1 << e for e in ex.boundary(g, A)) for A in cuts_q)
                if not (cb == cq == cm and set_b == set_q == sorted(masks)):
                    fails.append(("cuts", n, es, u, v))
                ans, _, _ = ex.path_in_min_cut(g, u, v, cuts_b)
                cp = mcp.cp_brute(G, u, v)[0]
                ans2 = ex.cp_equals_c_paths(g, u, v, alternating=True)[0]
                ans3 = ex.cp_equals_c_paths(g, u, v, alternating=False)[0]
                if not (ans == (cp == cb) == ans2 == ans3):
                    fails.append(("answer", n, es, u, v, ans, cp, cb, ans2, ans3))
                yes += ans
    lines = ["check_exact.py: exact.py versus checks/mcp.py on all connected graphs with 2..7 vertices", "",
             "graphs: %d, ordered pairs: %d, pairs with a u-v path inside a minimum cut: %d" % (len(graphs), pairs, yes),
             "comparisons: c(u,v) and the set of minimum cuts (3 methods); PATH-IN-MIN-CUT from the cuts, cp_brute == c,",
             "  definition-based test with and without the alternation pruning",
             "failures: %d" % len(fails)]
    for f in fails[:20]:
        lines.append("  " + repr(f))
    lines.append("Time %.0f s." % (time.time() - t0))
    with open(os.path.join(HERE, "results-exact.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
