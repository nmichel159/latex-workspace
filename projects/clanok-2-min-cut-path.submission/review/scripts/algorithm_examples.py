"""alg:cut-two as printed (statements.algorithm_as_printed) on ex:two-edges and on the 21-vertex graph of
checks/README.md (a witness with two edges and four distinct terminals)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ref, statements

def run(name, edges, u, v):
    adj = ref.graph(edges)
    cuts = ref.min_cuts2(adj, u, v)
    p1, p2 = ref.two_disjoint_paths(adj, u, v)
    D = ref.Decomposition(adj, u, v, cuts, p1, p2, allcuts=cuts)
    du, dv = ref.bfs(adj, u), ref.bfs(adj, v)
    for reading in ("along", "adjacent"):
        val, S, saw3, maxcand = statements.algorithm_as_printed(adj, u, v, D, du, dv, reading)
        print("%s [%s]: returns %d, edges %s, cp by brute force %d, d = %d, in the class: %s, some l >= 3: %s" % (
            name, reading, val, sorted(ref.fmt_e(e) for e in S), ref.cp_bruteforce(adj, u, v)[0], du[v],
            ref.in_class(adj)[0], saw3))

run("G_a^+", [(w[0], w[1:]) for w in "ua us sb ab at tv bv ur rb".split()], "u", "v")
E21 = "0-1 0-2 1-13 2-13 2-14 2-15 3-4 3-9 4-15 5-14 5-16 6-8 6-10 6-18 7-9 7-10 7-19 8-9 8-10 10-11 11-12 12-20 16-17 17-18 19-20"
run("21-vertex graph", [tuple(map(int, w.split("-"))) for w in E21.split()], 1, 11)
