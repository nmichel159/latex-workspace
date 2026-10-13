"""Validation of vlib.py: all connected graphs with 2..7 vertices (networkx atlas), every ordered pair (u, v),
plus random connected graphs with 8..9 vertices.

Compared per pair:
  c:      maxflow_py, flow_value (scipy), brute force over vertex sets, networkx local edge connectivity
  cuts:   min_cuts_residual == min_cuts_brute == min_cuts_branch (as sets of vertex sets)
  answer: [some minimum cut contains a u-v path] (residual cuts + cut graph)
          == [cp_eq_c_bb] == [cp_paths == c] == [cp_definition == c] (m <= 12 edges)
          == [mcp.cp_brute == c] (third-party brute force, checks/mcp.py, imported read-only)
Output: results-vlib.txt
"""

import os
import random
import sys
import time
from multiprocessing import Pool

import networkx as nx

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import vlib  # noqa: E402

CHECKS = os.path.normpath(os.path.join(HERE, "..", "..", "..", "checks"))


def check_graph(args):
    n, edges, tag = args
    sys.path.insert(0, CHECKS)
    import mcp  # read-only
    g = vlib.Gr(n, edges)
    mg = mcp.Gr(n, edges)
    fails = []
    stats = dict(pairs=0, yes=0)
    Gx = nx.Graph()
    Gx.add_nodes_from(range(n))
    Gx.add_edges_from(edges)
    for u in range(n):
        for v in range(n):
            if u == v:
                continue
            stats["pairs"] += 1
            c1, _, _ = vlib.maxflow_py(g, [u], [v])
            c2 = vlib.flow_value(g, [u], [v])
            c3, cb = vlib.min_cuts_brute(g, u, v)
            c4 = nx.edge_connectivity(Gx, u, v)
            if not (c1 == c2 == c3 == c4):
                fails.append(("c", tag, edges, u, v, c1, c2, c3, c4))
                continue
            c = c1
            _, cr = vlib.min_cuts_residual(g, u, v)
            cbr, _ = vlib.min_cuts_branch(g, u, v, c)
            if not (set(cr) == set(cb) == set(cbr) and len(cr) == len(set(cr))):
                fails.append(("cuts", tag, edges, u, v, len(cr), len(cb), len(cbr)))
                continue
            ans1 = any(vlib.cut_graph_connects(g, A, u, v) for A in cr)
            ans2, _, _ = vlib.cp_eq_c_bb(g, u, v, c)
            d = nx.shortest_path_length(Gx, u, v)
            cpp = vlib.cp_paths(g, u, v, cutoff=c + d)  # |P| <= cp <= d + c
            ans3 = (cpp == c)
            cpb = mcp.cp_brute(mg, u, v)
            cpb = cpb[0] if isinstance(cpb, tuple) else cpb
            ans5 = (cpb == c)
            ans4 = ans3
            if g.m <= 12:
                cpd = vlib.cp_definition(g, u, v)
                ans4 = (cpd == c)
                if cpd != cpp:
                    fails.append(("cpdef", tag, edges, u, v, cpd, cpp))
            if cpb != cpp:
                fails.append(("cp-mcp", tag, edges, u, v, cpb, cpp))
            if not (ans1 == ans2 == ans3 == ans4 == ans5):
                fails.append(("answer", tag, edges, u, v, ans1, ans2, ans3, ans4, ans5))
            stats["yes"] += ans1
    return tag, stats, fails


def main():
    t0 = time.time()
    jobs = []
    for i, G in enumerate(nx.graph_atlas_g()):
        if G.number_of_nodes() < 2 or not nx.is_connected(G):
            continue
        jobs.append((G.number_of_nodes(), list(G.edges()), "atlas%d" % i))
    natlas = len(jobs)
    rng = random.Random(20261012)
    while len(jobs) < natlas + 300:
        n = rng.randint(8, 9)
        p = rng.uniform(0.25, 0.6)
        G = nx.gnp_random_graph(n, p, seed=rng.randrange(10 ** 9))
        if nx.is_connected(G):
            jobs.append((n, list(G.edges()), "rand%d" % len(jobs)))
    tot = dict(pairs=0, yes=0)
    allf = []
    with Pool(30) as pool:
        for tag, st, fl in pool.imap_unordered(check_graph, jobs, chunksize=4):
            for k in tot:
                tot[k] += st[k]
            allf.extend(fl)
    lines = ["check_vlib.py: %d atlas graphs (connected, 2..7 vertices) + %d random graphs (8..9 vertices)"
             % (natlas, len(jobs) - natlas),
             "ordered pairs: %d, yes-pairs (some minimum cut contains a u-v path): %d" % (tot["pairs"], tot["yes"]),
             "failures: %d" % len(allf)]
    lines += [repr(f) for f in allf[:50]]
    lines.append("time %.1f s" % (time.time() - t0))
    with open(os.path.join(HERE, "results-vlib.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
