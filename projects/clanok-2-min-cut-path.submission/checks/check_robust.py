"""The referee's version of the algorithm (algorithm.solve_robust): no promise "G in the class".

For every connected graph and pair with c(u,v) = 2 the algorithm returns
  outcome "path"         d(u,v) and a cut-path R_x u p u R_y with d(u,v) edges
  outcome "value"        d(u,v) + 1 and R u C, no pair recorded
  outcome "certificate"  d(u,v) + 1 and R u C, and a pair (x, y) of distinct terminals of one square with l >= 3
Claims (counted assertions; names in the first column of the output):
  R1  a returned path is a cut-path with d(u,v) = cp(u,v) edges
  R2  if no pair is recorded, the returned value equals cp(u,v)
        (R2c: and in the case "value" the returned set is a cut-path with d(u,v) + 1 edges)
  R3a a recorded pair satisfies d(x,y) >= 3 and c(x,y) >= 3 (all pairs with l >= 3 are tested, not only the first)
  R3b no pair is ever recorded for G in the class (so the outcome "certificate" does not occur)
  R4  with a recorded pair and no path, the returned set is a cut-path with d(u,v) + 1 edges; reported: how often
      the value d(u,v) + 1 is then wrong (cp = d)
  R5  p_1, p_2 from the flow of value two by two searches in the digraph of the flow-carrying edges are two
      edge-disjoint u-v paths that follow the flow; also for flows that contain a cycle (random flows)
and, as consistency checks of the new pipeline: R-F (F and the orientation computed from p_1, p_2 and the
residual digraph D of the flow along p_1 and p_2 equal the brute-force ones), R6 (the version that returns at the
first path gives the same outcome and value as the exhaustive scan), R0 (the algorithm applies exactly when
c(u,v) = 2 and the squares have two entering and two leaving edges).

Instances: all connected graphs with at most 8 vertices (all ordered pairs with c = 2; for graphs with at most 7
vertices also random flows of value two, half of them with an added cycle, as input), random chains in DC,
random instances outside DC, and the hand-built family crossed_path_instance(k).

Run:  python check_robust.py [--maxn 8] [--instances 4500] [--general 12000] [--jobs 24]
Output: results-robust.txt (including the mutation tests)
"""

import argparse
import os
import random
import sys
import time
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp import *  # noqa: E402,F401,F403
from check_structure import Tally  # noqa: E402
from check_algorithm import crossed_path_instance  # noqa: E402
import algorithm  # noqa: E402


# ---------------------------------------------------------------------------------------------------------
# flows with cycles
# ---------------------------------------------------------------------------------------------------------

def random_flow(g, u, v, rng, cycle):
    """A flow of value two (integral, 0/+-1 per edge) from random augmenting paths (breadth-first or depth-first,
    random neighbor order); with cycle=True a circulation along a random cycle of flow-free edges is added."""
    flow = [0] * g.m
    for _ in range(2):
        par = {u: None}
        if rng.random() < 0.5:
            todo = [u]
            while todo and v not in par:
                x = todo.pop()                     # depth first: long augmenting paths, more cancellations
                nb = list(g.adj[x])
                rng.shuffle(nb)
                for y, e in nb:
                    if y in par:
                        continue
                    a = g.edges[e][0]
                    cap = (1 - flow[e]) if x == a else (1 + flow[e])
                    if cap > 0:
                        par[y] = (x, e)
                        todo.append(y)
        else:
            q = [u]
            for x in q:
                if v in par:
                    break
                nb = list(g.adj[x])
                rng.shuffle(nb)
                for y, e in nb:
                    if y in par:
                        continue
                    a = g.edges[e][0]
                    cap = (1 - flow[e]) if x == a else (1 + flow[e])
                    if cap > 0:
                        par[y] = (x, e)
                        q.append(y)
        if v not in par:
            return None
        y = v
        while y != u:
            x, e = par[y]
            flow[e] += 1 if x == g.edges[e][0] else -1
            y = x
    if cycle:
        add_cycle(g, flow, rng)
    return flow


def add_cycle(g, flow, rng):
    """Push one unit around a random cycle that uses only edges without flow (a circulation: the flow stays a
    flow of the same value).  Returns True if a cycle was found."""
    verts = list(range(g.n))
    rng.shuffle(verts)
    for s in verts:
        path, pos, pe = [s], {s: 0}, []
        x = s
        for _ in range(4 * g.n):
            nb = [(y, e) for y, e in g.adj[x] if flow[e] == 0 and (not pe or e != pe[-1])]
            if not nb:
                break
            y, e = rng.choice(nb)
            if y in pos:
                i = pos[y]
                cyc = path[i:] + [y]
                for j, ee in enumerate(pe[i:] + [e]):
                    flow[ee] = 1 if cyc[j] == g.edges[ee][0] else -1
                return True
            pos[y] = len(path)
            path.append(y)
            pe.append(e)
            x = y
    return False


def paths_valid(g, u, v, paths, flow):
    """Two simple u-v paths, edge-disjoint, every edge traversed in the direction of its flow."""
    used = set()
    for vs, es in paths:
        if vs[0] != u or vs[-1] != v or len(set(vs)) != len(vs) or len(es) != len(vs) - 1:
            return False
        for j, e in enumerate(es):
            if not g.has_edge(vs[j], vs[j + 1]) or g.edge_id(vs[j], vs[j + 1]) != e:
                return False
            a = g.edges[e][0]
            f = flow[e]
            if not ((f > 0 and vs[j] == a) or (f < 0 and vs[j] != a)):
                return False
        if used & set(es):
            return False
        used |= set(es)
    return True


# ---------------------------------------------------------------------------------------------------------
# the claims
# ---------------------------------------------------------------------------------------------------------

def check_pair(g, u, v, T, mut, dc, cls, flow=None, fast=False):
    """All claims for one ordered pair with c(u,v) = 2 (flow: a given flow of value two, else the algorithm's)."""
    T.ctx = (g, u, v)
    d = bfs(g, u)[v]
    res = algorithm.solve_robust(g, u, v, mutation=mut, exhaustive=True, flow=flow)
    T.ok("R0", res is not None and res["c"] == 2, "solve_robust did not apply to a pair with c = 2")
    if res is None or res["c"] != 2:
        return
    used_flow = flow if flow is not None else res["flow"]
    T.ok("R5", res["paths"] is not None and paths_valid(g, u, v, res["paths"], used_flow),
         lambda: "the two searches in the flow digraph do not give two edge-disjoint u-v paths along the flow: %s" % (res["paths"],))
    if res["paths"] is None:
        return
    inpaths = sum(len(es) for vs, es in res["paths"])
    if sum(1 for f in used_flow if f) > inpaths:
        T.stat("%s: flows with a cycle (flow-carrying edges outside p_1, p_2)" % cls)
    T.ok("R0-structure", "error" not in res, lambda: res.get("error"))
    if "error" in res:
        return
    cpb = cp_brute(g, u, v)[0]
    dec, cuts, problems = brute_decomp(g, u, v, fast=fast)
    T.ok("R-F", res["F"] == dec.F and res["tail"] == dec.tail,
         lambda: "F from p_1, p_2 and D: %s, brute force: %s" % (res["F"], dec.F))
    outcome, S = res["outcome"], res["cutpath"]
    T.stat("%s: pairs with c = 2" % cls)
    T.stat("%s: outcome %s" % (cls, outcome))
    if outcome == "path":
        T.ok("R1", is_cutpath(g, u, v, S) and popcount(S) == d and cpb == d,
             lambda: "returned set has %d edges, cut-path: %s, d = %d, cp = %d" % (popcount(S), is_cutpath(g, u, v, S), d, cpb))
    if outcome in ("path", "value"):
        T.ok("R2", res["cp"] == cpb, lambda: "no pair recorded, returned value %d, cp = %d, d = %d" % (res["cp"], cpb, d))
    if outcome == "value":
        T.ok("R2c", is_cutpath(g, u, v, S) and popcount(S) == d + 1,
             lambda: "value d + 1 = %d: returned set has %d edges, cut-path: %s" % (d + 1, popcount(S), is_cutpath(g, u, v, S)))
    for x, y in res["pairs"]:
        T.ok("R3a", bfs(g, x)[y] >= 3 and edge_conn(g, x, y, limit=3) >= 3,
             lambda: "recorded pair (%d, %d): d = %d, c = %d" % (x, y, bfs(g, x)[y], edge_conn(g, x, y)))
    if res["pairs"]:
        T.stat("%s: pairs with l >= 3 exist" % cls)
    if dc:
        T.ok("R3b", not res["pairs"] and outcome != "certificate", lambda: "G is in the class but pairs %s were found" % (res["pairs"],))
    if outcome == "certificate":
        T.ok("R4", is_cutpath(g, u, v, S) and popcount(S) == d + 1 and res["cp"] == d + 1,
             lambda: "certificate: returned set has %d edges (d + 1 = %d), cut-path: %s" % (popcount(S), d + 1, is_cutpath(g, u, v, S)))
        T.stat("%s: certificate, value d + 1 wrong (cp = d)" % cls if cpb == d else "%s: certificate, value d + 1 right (cp = d + 1)" % cls)
        T.ok("R3c", not dc, "outcome certificate for a graph in the class")
    # the algorithm that returns at the first path
    early = algorithm.solve_robust(g, u, v, mutation=mut, exhaustive=False, flow=flow)
    T.ok("R6", early is not None and early["outcome"] == outcome and early["cp"] == res["cp"] and popcount(early["cutpath"]) == popcount(S)
         and (outcome == "path" or early["recorded"] == res["recorded"]),
         lambda: "early return: %s %s, exhaustive scan: %s %s" % (early and early["outcome"], early and early["cp"], outcome, res["cp"]))


# ---------------------------------------------------------------------------------------------------------
# drivers
# ---------------------------------------------------------------------------------------------------------

def run_small(args):
    n, es, mut = args
    g = Gr(n, es)
    dc, _ = in_dc(g)
    cls = "small graphs in DC" if dc else "small graphs outside DC"
    rng = random.Random(n * 100003 + g.m * 31 + sum(a * 7 + b for a, b in g.edges))
    T = Tally()
    T.ctx = (g, 0, 1)
    T.stat("%s: graphs" % cls)
    for u in range(n):
        for v in range(n):
            if u == v:
                continue
            c = edge_conn(g, u, v, limit=3)
            if c == 2:
                check_pair(g, u, v, T, mut, dc, cls)
            if n <= 7 and c >= 2 and mut in (None, "p2-no-removal"):
                for k in range(2):
                    flow = random_flow(g, u, v, rng, cycle=(k == 1))
                    if flow is None:
                        continue
                    if c == 2:
                        check_pair(g, u, v, T, mut, dc, cls + " (random flows)", flow=flow)
                    else:
                        T.ctx = (g, u, v)
                        paths = algorithm.flow_paths(g, flow, u, v, mut)
                        T.ok("R5", paths is not None and paths_valid(g, u, v, paths, flow),
                             lambda: "pair with c >= 3, random flow: the two searches fail")
                        if sum(1 for f in flow if f) > (sum(len(p[1]) for p in paths) if paths else 0):
                            T.stat("pairs with c >= 3: random flows with a cycle")
    return T.clean()


def run_chain(args):
    seed, kind, mut = args
    import chains
    rng = random.Random(seed)
    inst = chains.random_dc_chain(rng) if kind == "dc" else chains.random_general_chain(rng)
    T = Tally()
    if inst is None:
        return T
    g, u, v = inst
    cls = "chains in DC" if kind == "dc" else "random instances outside DC"
    T.ctx = (g, u, v)
    T.stat("%s: instances" % cls)
    check_pair(g, u, v, T, mut, kind == "dc", cls, fast=True)
    return T.clean()


def run_crossed(mut):
    T = Tally()
    for k in range(3, 9):
        g, u, v = crossed_path_instance(k)
        T.stat("crossed family: instances")
        check_pair(g, u, v, T, mut, in_dc(g)[0], "crossed family", fast=True)
    return T.clean()


NAMES = [
    ("R0", "the algorithm applies to every pair with c = 2"), ("R0-structure", "every square has two entering and two leaving edges"),
    ("R5", "p_1, p_2 from two searches in the flow digraph: edge-disjoint u-v paths along the flow"),
    ("R-F", "F and orientation from p_1, p_2 and D equal the brute-force ones"),
    ("R1", "a returned path is a cut-path with d(u,v) = cp(u,v) edges"),
    ("R2", "no pair recorded: the returned value equals cp(u,v)"), ("R2c", "outcome value: the returned set is a cut-path with d + 1 edges"),
    ("R3a", "every pair with l >= 3 has d(x,y) >= 3 and c(x,y) >= 3"), ("R3b", "G in the class: no pair is recorded"),
    ("R3c", "outcome certificate only outside the class"),
    ("R4", "pair recorded, no path: the returned set is a cut-path with d + 1 edges"),
    ("R6", "stopping at the first path gives the same outcome and value as the exhaustive scan"),
]

# mutation -> assertions of which at least one must fail
MUTATIONS = [
    ("record-ge4", "R2", "a pair is recorded only if l >= 4 (a trace with three edges is missed)"),
    ("record-ge2", "R3a", "a pair is recorded already if l >= 2"),
    ("never-record", "R2", "no pair is ever recorded (the certificate is dropped)"),
    ("skip-l2", "R2", "the paths x, w, y (l = 2) are never tested"),
    ("l1-nosep", "R1", "the edge xy (l = 1) is accepted without the separation test"),
    ("cut-missing", "R2c", "the returned d + 1 set is the shortest path alone, without the cut"),
    ("p2-no-removal", "R5", "the second search does not remove the arcs of the first path"),
]


def run_all(mut, opts, pool, with_crossed=True):
    T = Tally()
    graphs = []
    for n in range(2, opts.maxn + 1):
        graphs.extend(connected_graphs(n, SCRATCH))
    for r in pool.imap(run_small, [(n, es, mut) for n, es in graphs], chunksize=4):
        T.merge(r)
    for r in pool.imap(run_chain, [(opts.seed + i, "dc", mut) for i in range(opts.instances)], chunksize=4):
        T.merge(r)
    for r in pool.imap(run_chain, [(opts.seed + i, "general", mut) for i in range(opts.general)], chunksize=4):
        T.merge(r)
    if with_crossed:
        T.merge(run_crossed(mut))
    return T


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--maxn", type=int, default=8)
    ap.add_argument("--instances", type=int, default=4500)
    ap.add_argument("--general", type=int, default=12000)
    ap.add_argument("--seed", type=int, default=20261012)
    ap.add_argument("--jobs", type=int, default=24)
    ap.add_argument("--out", default="results-robust.txt")
    opts = ap.parse_args()
    lines = []

    def out(s=""):
        print(s, flush=True)
        lines.append(s)

    started = time.time()
    out("check_robust.py: algorithm.solve_robust (the version without the promise G in DC) against brute force")
    out("graphs with 2..%d vertices (all connected graphs, all ordered pairs with c = 2), %d random chains in DC (seeds from %d), "
        "%d random instances outside DC, crossed_path_instance(3..8)" % (opts.maxn, opts.instances, opts.seed, opts.general))
    with Pool(opts.jobs) as pool:
        T = run_all(None, opts, pool)
        out("")
        out("Statistics")
        for key in sorted(T.stats):
            out("  %-84s %d" % (key, T.stats[key]))
        out("")
        out("%-13s %-84s %10s %7s" % ("assertion", "claim", "count", "failed"))
        for name, text in NAMES:
            if T.count.get(name):
                out("%-13s %-84s %10d %7d  %s" % (name, text, T.count[name], T.nfail[name], "PASS" if not T.nfail[name] else "FAIL"))
        for name, text in NAMES:
            if name in T.first:
                key, rec = T.first[name]
                out("FAILURE %s: n=%d, u=%d, v=%d, edges %s" % (name, rec["n"], rec["u"], rec["v"], fmt_edges(rec["edges"])))
                out("    %s" % rec["info"])
        total, failed = sum(T.count.values()), sum(T.nfail.values())
        out("")
        out("Assertions: %d, failed: %d." % (total, failed))
        # claim 4: how often the value d + 1 of the outcome "certificate" is wrong
        out("")
        out("Claim 4 (outcome certificate: how often is the value d + 1 wrong, i.e. cp = d?)")
        for cls in ("small graphs in DC", "small graphs outside DC", "small graphs outside DC (random flows)", "chains in DC",
                    "random instances outside DC", "crossed family"):
            wrong = T.stats.get("%s: certificate, value d + 1 wrong (cp = d)" % cls, 0)
            right = T.stats.get("%s: certificate, value d + 1 right (cp = d + 1)" % cls, 0)
            if wrong + right:
                out("  %-45s certificates %6d, value wrong (cp = d) %6d (%.1f %%), right %6d" % (cls, wrong + right, wrong, 100.0 * wrong / (wrong + right), right))
        # mutation tests
        out("")
        out("Mutation tests (graphs with 2..7 vertices, 600 chains in DC, 1500 instances outside DC, crossed family)")
        small = argparse.Namespace(maxn=7, instances=600, general=1500, seed=opts.seed)
        ok_all = True
        for mut, target, text in MUTATIONS:
            M = run_all(mut, small, pool)
            f = M.nfail[target]
            others = {name: M.nfail[name] for name, _ in NAMES if M.nfail[name] and name != target}
            ok_all &= f > 0
            out("  %-14s %-5s %-76s failed %7d of %8d  %s%s" % (mut, target, text, f, M.count[target], "DETECTED" if f else "NOT DETECTED",
                                                              "   (also: %s)" % ", ".join("%s %d" % kv for kv in sorted(others.items())) if others else ""))
            if target in M.first:
                key, rec = M.first[target]
                out("      smallest failing instance: n=%d, u=%d, v=%d, edges %s" % (rec["n"], rec["u"], rec["v"], fmt_edges(rec["edges"])))
                out("      %s" % rec["info"])
        out("All mutations detected: %s." % ok_all)
    out("Total time %.0f s." % (time.time() - started))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), opts.out), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
