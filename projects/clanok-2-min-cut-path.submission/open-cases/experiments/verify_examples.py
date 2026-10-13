"""Independent re-check of the examples reported in experiments.md, using only checks/mcp.py (no code of
cutpaths.py): membership in DC, d(u,v), all minimum u-v cuts by vertex sets, all u-v paths inside them, cp(u,v)
by cp_brute (and cp_subsets for n <= 10), and the isomorphism classes of the 17-edge examples on 10 vertices.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS = os.path.normpath(os.path.join(HERE, "..", "..", "checks"))
sys.path.insert(0, CHECKS)
import mcp  # noqa: E402
import networkx as nx  # noqa: E402


def parse(s):
    return [tuple(int(t) for t in e.split("-")) for e in s.split()]


EXAMPLES = [
    ("E10 (DC, n=10, m=17)", 10, "0-1 1-2 2-3 3-4 4-5 0-2 0-6 2-6 0-4 0-7 4-7 1-5 1-8 5-8 3-5 3-9 5-9", 0, 5),
    ("E10 + 6-7 (not DC, n=10, m=18)", 10,
     "0-1 1-2 2-3 3-4 4-5 0-2 0-6 2-6 0-4 0-7 4-7 1-5 1-8 5-8 3-5 3-9 5-9 6-7", 0, 5),
    ("F(3) with cliques (DC, n=14, m=31)", 14,
     "0-1 1-2 2-3 3-4 4-5 5-6 6-7 0-2 0-8 8-2 0-4 0-9 9-4 0-6 0-10 10-6 1-7 1-11 11-7 3-7 3-12 12-7 5-7 5-13 13-7 "
     "0-2 0-4 0-6 2-4 2-6 4-6 1-3 1-5 1-7 3-5 3-7 5-7", 0, 7),
    ("strong form only (DC, n=10, m=19, lengths 3 and 5)", 10,
     "0-1 0-2 0-4 0-7 0-8 1-2 1-3 1-5 2-3 2-4 3-4 3-5 3-6 3-9 4-5 4-7 4-8 5-6 5-9", 0, 5),
    ("G(3) of repaired_family.py (DC, n=17, m=31)", 17,
     "0-1 0-2 0-4 0-6 0-8 0-9 0-10 0-15 1-2 1-7 1-11 2-3 2-8 2-14 2-15 3-4 3-7 3-12 4-5 4-9 5-6 5-7 5-13 5-14 "
     "5-16 6-7 6-10 7-11 7-12 7-13 7-16", 0, 7),
]


def check(name, n, es, u, v):
    g = mcp.Gr(n, parse(es))
    dc, bad = mcp.in_dc(g)
    d = mcp.bfs(g, u)[v]
    c, cuts = mcp.min_cuts_by_sets(g, u, v)
    full = g.full()
    paths = set()
    for C in cuts:
        for vs, _ in mcp.simple_paths(g, u, v, removed=full ^ C):
            paths.add(vs)
    cpb = mcp.cp_brute(g, u, v)[0]
    cps = mcp.cp_subsets(g, u, v) if n <= 10 else None
    far = [(x, y, mcp.bfs(g, x)[y], mcp.edge_conn(g, x, y)) for x in range(n) for y in range(x + 1, n)
           if mcp.bfs(g, x)[y] > 2]
    return ("%s: m=%d in_dc=%s %s d(u,v)=%d c(u,v)=%d minimum cuts=%d cp_brute=%d cp_subsets=%s; "
            "paths inside minimum cuts: %s\n    pairs at distance >= 3 (x, y, d, c): %s"
            % (name, g.m, dc, bad or "", d, c, len(cuts), cpb, cps, sorted(paths), far))


def main():
    lines = ["verify_examples.py (mcp.py only)", ""]
    for ex in EXAMPLES:
        lines.append(check(*ex))
        print(lines[-1], flush=True)
    # isomorphism classes of the 17-edge examples found by climb.py on 10 vertices (u = 0, v = 5 marked)
    lines.append("")
    reps = []
    for fname in ("results-climb-n10-L5-dc.txt", "results-climb-n10-L5-any.txt"):
        path = os.path.join(HERE, fname)
        if not os.path.exists(path):
            continue
        for line in open(path):
            if line.startswith("  m=17"):
                es = parse(line.split(": ", 1)[1])
                G = nx.Graph(es)
                nx.set_node_attributes(G, {x: (1 if x == 0 else 2 if x == 5 else 0) for x in G}, "t")
                for H in reps:
                    if nx.is_isomorphic(G, H, node_match=lambda a, b: a["t"] == b["t"]):
                        break
                else:
                    reps.append(G)
    E10 = nx.Graph(parse(EXAMPLES[0][2]))
    nx.set_node_attributes(E10, {x: (1 if x == 0 else 2 if x == 5 else 0) for x in E10}, "t")
    same = [nx.is_isomorphic(E10, H, node_match=lambda a, b: a["t"] == b["t"]) for H in reps]
    lines.append("17-edge examples on 10 vertices listed by climb.py: %d isomorphism classes (with u, v marked); "
                 "isomorphic to E10: %s" % (len(reps), same))
    print(lines[-1])
    with open(os.path.join(HERE, "results-verify-examples.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
