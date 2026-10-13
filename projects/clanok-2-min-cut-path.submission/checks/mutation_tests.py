"""Mutation tests: every check must be able to fail.

For each statement (S2, S5, S6, S7, S8, S9) the check is run once with the tested statement broken on purpose
(check_structure.py, option mut), for the algorithm (S11) with one of its steps broken (algorithm.py, option
mutation).  The mutated run must report failures of the named assertion; the unmutated run (results-structure.txt,
results-algorithm.txt) has none.

Run:  python mutation_tests.py      (about a minute)
Output: results-mutations.txt
"""

import os
import sys
import time
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp import *  # noqa: E402,F401,F403
import check_structure as cs  # noqa: E402
import check_algorithm as ca  # noqa: E402

STRUCTURE = [
    ("S5-order", "S5c", "expected order of the squares reversed"),
    ("S5-cut", "S5a", "an entering and a leaving edge of one square taken as the minimum cut"),
    ("S5-both", "S5e", "a path claimed to use the F-edges of both sequences"),
    ("S6-all", "S6", "c >= 3 claimed for any two vertices of a square, not only terminals"),
    ("S6-4", "S6", "c >= 4 claimed for distinct terminals"),
    ("S7-swap", "S7", "(x_i, y_i) used instead of (alpha_i, beta_i) in the separation criterion"),
    ("S9-nolen", "S9a", "length condition (count = d) dropped from S9"),
    ("S9-nosep", "S9a", "separation condition dropped from S9"),
    ("S8-off", "S8b", "length formula of S8 off by one"),
    ("S2-flip", "S2d", "orientation of F reversed"),
    ("S9core-nolen", "S9-core", "condition (i) d(u,x) + |p| + d(y,v) = d(u,v) of the theorem in core.tex dropped"),
    ("S11-res-flip", "S11-res-i", "arcs of the path edges in the residual graph D point along the paths (statement (ii) cannot see this: reversing\n"
                     "                                      all arcs of D does not change its strong components)"),
    ("S11-res-both", "S11-res-ii", "path edges keep both arcs in the residual graph D"),
]
ALGORITHM = [
    ("skip-l2", "never test l = 2"),
    ("l1-nosep", "l = 1 accepted without the separation test"),
    ("no-l1", "never test l = 1"),
    ("swap-lambda", "lambda^+ of the tail used instead of lambda^- in the count"),
    ("first-square", "only the first square is examined"),
]


def run_structure(mut, chains, jobs):
    T = cs.Tally()
    graphs = []
    for n in range(2, 8):
        graphs.extend(atlas_pairs(n, n))
    with Pool(jobs) as pool:
        for r in pool.imap(cs.run_graph, [(n, es, mut) for n, es in graphs], chunksize=4):
            T.merge(r)
        for r in pool.imap(cs.run_chain, [(20261012 + i, mut, 20000) for i in range(chains)], chunksize=4):
            T.merge(r)
    return T


def run_algorithm(mut, chains, jobs):
    T = cs.Tally()
    graphs = []
    for n in range(2, 8):
        graphs.extend(atlas_pairs(n, n))
    with Pool(jobs) as pool:
        for dc, r in pool.imap(ca.run_small, [(n, es, mut) for n, es in graphs], chunksize=4):
            T.merge(r)
        for r in pool.imap(ca.run_chain, [(20261012 + i, mut) for i in range(chains)], chunksize=4):
            T.merge(r)
    return T


def main():
    started = time.time()
    lines = []

    def out(s=""):
        print(s, flush=True)
        lines.append(s)

    out("mutation_tests.py: each check is run with the tested statement broken on purpose.")
    out("All connected graphs with 2..7 vertices plus 600 random chains (structure) / 600 random DC instances (algorithm).")
    out("")
    out("%-14s %-8s %-72s %12s %10s  %s" % ("mutation", "target", "what is broken", "assertions", "failed", "result"))
    verdict = True
    for mut, target, text in STRUCTURE:
        T = run_structure(mut, 600, 24)
        n, f = T.count[target], T.nfail[target]
        ok = f > 0
        verdict &= ok
        out("%-14s %-8s %-72s %12d %10d  %s" % (mut, target, text, n, f, "DETECTED" if ok else "NOT DETECTED"))
        if target in T.first:
            key, rec = T.first[target]
            out("    smallest failing instance: n=%d, u=%d, v=%d, edges %s" % (rec["n"], rec["u"], rec["v"], fmt_edges(rec["edges"])))
            out("      %s" % rec["info"])
    out("")
    out("%-14s %-8s %-72s %12s %10s  %s" % ("mutation", "target", "what is broken", "pairs", "wrong", "result"))
    for mut, text in ALGORITHM:
        T = run_algorithm(mut, 600, 24)
        n = T.count["ALG-value"]
        f = T.nfail["ALG-value"] + T.nfail["ALG-cutpath"]
        ok = f > 0
        verdict &= ok
        out("%-14s %-8s %-72s %12d %10d  %s" % (mut, "ALG", text, n, f, "DETECTED" if ok else "NOT DETECTED"))
        for name in ("ALG-value", "ALG-cutpath"):
            if name in T.first:
                key, rec = T.first[name]
                out("    smallest failing instance (%s): n=%d, u=%d, v=%d, edges %s" % (name, rec["n"], rec["u"], rec["v"], fmt_edges(rec["edges"])))
                out("      %s" % rec["info"])
                break
    out("")
    out("All mutations detected: %s.  Time %.0f s." % (verdict, time.time() - started))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results-mutations.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    sys.exit(0 if verdict else 1)


if __name__ == "__main__":
    main()
