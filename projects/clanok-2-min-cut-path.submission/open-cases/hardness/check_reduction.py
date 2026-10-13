"""Verification of the reduction 3-SAT -> PATH-IN-MIN-CUT (theory-hardness.md, Theorem 2.4) on small formulas.

For every formula phi the graph G = build(phi) is constructed and the following are checked exactly:
  R1  c(u,v) = c0 = (m + 1) + 2L
  R2  d(u,v) = 2 and diam(G) = 3
  R3  the minimum u-v cuts (Picard-Queyranne enumeration) are exactly the sets A_tau, one per assignment
  R4  the same set of minimum cuts by branching (if |V| <= BRANCH_MAX) and by all vertex sets (if |V| <= 24)
  R5  some minimum cut contains a u-v path  <=>  phi is satisfiable (brute force over assignments)
  R6  the shortest such path has the length predicted from phi (shortest_route)
  R7  cp(u,v) = c(u,v) decided from the definition (cp_equals_c_paths, alternating pruning; if |V| <= PATH_MAX)
      agrees with R5
  R8  G is not in DC and not in "d <= 2 or c <= 3"; every pair has d <= 3
Families: (a) all 3-CNF formulas over 1 or 2 variables with 1 or 2 clauses (clauses as multisets of literals);
(b) random 3-CNF formulas, n = 2..6 variables, m = 3..8 clauses (satisfiable and unsatisfiable ones);
(c) random 3-CNF formulas over 2 or 3 variables with 4..10 clauses, 40 unsatisfiable and 20 satisfiable ones.
Output: results-reduction.txt.
"""

import itertools
import os
import random
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import exact as ex  # noqa: E402
import reduction as rd  # noqa: E402

BRANCH_MAX = 110
PATH_MAX = 150
NUMPY_MAX = 24


def check(phi):
    t0 = time.time()
    g, u, v, info = rd.build(phi)
    out = {"phi": phi, "n": g.n, "m_edges": g.m, "fail": []}
    sat = rd.satisfiable(phi)
    out["sat"] = sat
    c = ex.cut_value(g, u, v)
    out["c"] = c
    if c != info["c0"]:
        out["fail"].append("R1 c=%d c0=%d" % (c, info["c0"]))
    du = ex.bfs_dist(g, u)
    diam, cls, example = ex.diameter_and_classes(g)
    out["d"] = du[v]
    out["diam"] = diam
    out["cls"] = cls
    if du[v] != 2 or diam != 3:
        out["fail"].append("R2 d=%s diam=%s" % (du[v], diam))
    vars_, intended = rd.intended_cuts(info)
    cq, cuts_q = ex.min_cuts_pq(g, u, v)
    if cq != c or set(cuts_q) != set(intended.values()) or len(cuts_q) != len(intended):
        out["fail"].append("R3 PQ cuts differ (%d found, %d intended)" % (len(cuts_q), len(intended)))
    out["cuts"] = len(cuts_q)
    methods = ["PQ"]
    if g.n <= BRANCH_MAX:
        order = sorted((x for x in range(g.n) if x not in (u, v)), key=lambda x: (x >= 2 * info["M"], x))
        cb, cuts_b = ex.min_cuts_branch(g, u, v, order=order)
        methods.append("branching")
        if cb != c or set(cuts_b) != set(cuts_q):
            out["fail"].append("R4 branching differs")
    if g.n <= NUMPY_MAX:
        cn, cuts_n = ex.min_cuts_numpy(g, u, v)
        methods.append("all vertex sets")
        if cn != c or set(cuts_n) != set(cuts_q):
            out["fail"].append("R4 numpy differs")
    out["methods"] = methods
    ans, best, count = ex.path_in_min_cut(g, u, v, cuts_q)
    out["answer"] = ans
    out["shortest"] = best
    out["cuts_with_path"] = count
    if ans != sat:
        out["fail"].append("R5 answer %s sat %s" % (ans, sat))
    pred = rd.shortest_route(phi)
    if best != pred:
        out["fail"].append("R6 shortest %s predicted %s" % (best, pred))
    if g.n <= PATH_MAX:
        a2, c2, nstar, tried, lens = ex.cp_equals_c_paths(g, u, v, alternating=True)
        out["def"] = (a2, nstar, tried, lens)
        if a2 != sat:
            out["fail"].append("R7 definition-based answer %s sat %s" % (a2, sat))
    if cls["d>2,c>2 (not DC)"] == 0 or cls["d>2,c>3 (not 'd<=2 or c<=3')"] == 0 or cls["d>3,c>2 (not 'd<=3 or c<=2')"] != 0:
        out["fail"].append("R8 classes %s" % cls)
    out["time"] = time.time() - t0
    return out


def family_a():
    res = []
    for nv in (1, 2):
        lits = [i for i in range(1, nv + 1)] + [-i for i in range(1, nv + 1)]
        clauses = list(itertools.combinations_with_replacement(lits, 3))
        for m in (1, 2):
            for combo in itertools.combinations_with_replacement(clauses, m):
                phi = [list(C) for C in combo]
                if len({abs(l) for C in phi for l in C}) == nv:
                    res.append(phi)
    return res


def family_b(seed=20261012):
    rng = random.Random(seed)
    res = []
    for n in range(2, 7):
        for m in range(3, 9):
            for _ in range(4):
                res.append(rd.random_formula(rng, n, m))
    # a few unsatisfiable formulas over two variables with all four sign patterns
    res.append([[1, 2, 2], [1, -2, -2], [-1, 2, 2], [-1, -2, -2]])
    res.append([[1, 1, 1], [-1, -1, -1]])
    res.append([[1, 2, 3], [1, 2, -3], [1, -2, 3], [1, -2, -3], [-1, 2, 3], [-1, 2, -3], [-1, -2, 3], [-1, -2, -3]])
    return res


def family_c(seed=7):
    rng = random.Random(seed)
    uns, sat = [], []
    while len(uns) < 40 or len(sat) < 20:
        n = rng.choice((2, 3))
        m = rng.randint(4, 10)
        phi = rd.random_formula(rng, n, m)
        if len({abs(l) for C in phi for l in C}) != n:
            continue
        if rd.satisfiable(phi):
            if len(sat) < 20:
                sat.append(phi)
        elif len(uns) < 40:
            uns.append(phi)
    return uns + sat


def main():
    t0 = time.time()
    fa = family_a()
    fb = family_b()
    fc = family_c()
    jobs = fa + fb + fc
    with Pool(30) as pool:
        results = pool.map(check, jobs, chunksize=1)
    lines = ["check_reduction.py: reduction 3-SAT -> PATH-IN-MIN-CUT, checks R1-R8 of the docstring", ""]
    for name, part in (("(a) all 3-CNF over 1-2 variables, 1-2 clauses", results[:len(fa)]),
                       ("(b) random 3-CNF, n = 2..6, m = 3..8, plus 3 unsatisfiable formulas", results[len(fa):len(fa) + len(fb)]),
                       ("(c) random 3-CNF over 2-3 variables, m = 4..10", results[len(fa) + len(fb):])):
        nsat = sum(r["sat"] for r in part)
        nf = sum(1 for r in part if r["fail"])
        meth = {}
        for r in part:
            for mth in r["methods"]:
                meth[mth] = meth.get(mth, 0) + 1
        ndef = sum(1 for r in part if "def" in r)
        lines.append("%s: %d formulas (%d satisfiable, %d unsatisfiable), formulas with a failed check: %d"
                     % (name, len(part), nsat, len(part) - nsat, nf))
        lines.append("  |V| from %d to %d, |E| from %d to %d, c(u,v) from %d to %d"
                     % (min(r["n"] for r in part), max(r["n"] for r in part), min(r["m_edges"] for r in part),
                        max(r["m_edges"] for r in part), min(r["c"] for r in part), max(r["c"] for r in part)))
        lines.append("  minimum cuts computed by: %s; definition-based test (R7) on %d formulas"
                     % (", ".join("%s %d" % kv for kv in sorted(meth.items())), ndef))
        lens = {}
        for r in part:
            if r["answer"]:
                key = (len(r["phi"]), r["shortest"])
                lens[key] = lens.get(key, 0) + 1
        lines.append("  (m, shortest path in a minimum cut) for satisfiable formulas: %s" % sorted(lens.items()))
        for r in part:
            if r["fail"]:
                lines.append("  FAIL %s: %s" % (r["phi"], r["fail"]))
    lines.append("")
    lines.append("Examples:")
    for r in results[:3] + results[-3:]:
        lines.append("  phi=%s |V|=%d |E|=%d c=%d d=%d diam=%d sat=%s answer=%s shortest=%s cuts=%d cuts_with_path=%d "
                     "def=%s classes=%s (%.1f s)" % (r["phi"], r["n"], r["m_edges"], r["c"], r["d"], r["diam"], r["sat"],
                                                    r["answer"], r["shortest"], r["cuts"], r["cuts_with_path"],
                                                    r.get("def"), r["cls"], r["time"]))
    total_fail = sum(1 for r in results if r["fail"])
    lines.append("")
    lines.append("Total: %d formulas, %d with a failed check.  Time %.0f s." % (len(results), total_fail, time.time() - t0))
    with open(os.path.join(HERE, "results-reduction.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
