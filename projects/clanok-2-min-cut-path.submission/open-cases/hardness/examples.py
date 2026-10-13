"""Small explicit instances of the reduction (theory-hardness.md, Corollary 2.6 and Section 6), with full edge lists.

E1  phi = (x1) and (x1): every u-v path inside a minimum cut has length 5 (no path of length 3).
E2  phi = (x1) and (x2) and (not x3) and (not x4): 16 minimum cuts, exactly one contains a u-v path, and it is
    neither the smallest minimum cut containing a vertex nor the largest one avoiding a vertex.
E3  phi = (x1) and (not x1): unsatisfiable, cp(u,v) = c(u,v) + 1.
Each is checked by three methods (Picard-Queyranne cuts, branching cuts, definition-based test).
Output: results-examples.txt.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import exact as ex  # noqa: E402
import reduction as rd  # noqa: E402


def main():
    lines = ["examples.py: explicit reduction instances (one-literal clauses)", ""]
    for name, phi in (("E1", [[1], [1]]), ("E2", [[1], [2], [-3], [-4]]), ("E3", [[1], [-1]])):
        g, u, v, info = rd.build(phi)
        c, cuts = ex.min_cuts_pq(g, u, v)
        cb, cutsb = ex.min_cuts_branch(g, u, v)
        good = [A for A in cuts if ex.cut_graph_path(g, A, u, v) is not None]
        ans, best, count = ex.path_in_min_cut(g, u, v, cuts)
        dfn = ex.cp_equals_c_paths(g, u, v)
        diam, cls, _ = ex.diameter_and_classes(g)
        gen = set()
        for x in range(g.n):
            inc = [A for A in cuts if x in A]
            exc = [A for A in cuts if x not in A]
            if inc:
                gen.add(min(inc, key=len))
            if exc:
                gen.add(max(exc, key=len))
        lines.append("%s phi=%s satisfiable=%s: |V|=%d |E|=%d u=%d v=%d c=%d d=%d diam=%d" %
                     (name, phi, rd.satisfiable(phi), g.n, g.m, u, v, c, ex.bfs_dist(g, u)[v], diam))
        lines.append("  minimum cuts: %d (branching agrees: %s); with a u-v path: %d; shortest such path: %s; "
                     "definition-based test (answer, c, candidate edges, paths tried, lengths): %s"
                     % (len(cuts), set(cuts) == set(cutsb) and cb == c, len(good), best, dfn))
        lines.append("  a path-containing cut is single-generated: %s" % bool(set(good) & gen))
        for A in good:
            p = ex.cut_graph_path(g, A, u, v)
            lines.append("  cut side A = %s; a shortest path inside delta(A): %s" % (sorted(A), p))
        lines.append("  K_A = %s, K_B = %s, h = %s, beta = %s, a = %s, b = %s, occurrence vertices = %s"
                     % (info["KA"], info["KB"], info["h"], info["beta"], info["a"], info["b"], info["occ"]))
        lines.append("  edges: " + " ".join("%d-%d" % e for e in g.edges))
        lines.append("")
    with open(os.path.join(HERE, "results-examples.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
