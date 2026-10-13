"""Task E: data on the open cases, for a later phase (report only, no assertions).

(a) pairs with d(u,v) = 2 and c(u,v) >= 3 in all connected graphs with at most --maxn vertices (all graphs
    with at most seven vertices lie in DC): how often cp = c and how often cp = c + 1; for cp = c the lengths
    of the u-v paths that lie inside a minimum cut; the three smallest examples of each kind.
(b) all connected graphs of diameter exactly 3: the distribution of (c + d - 1) - cp by (d, c), the largest
    gap, the smallest graphs with cp < c + d - 1, and how many of the graphs lie in DC.

Pairs are unordered (cp, d, c are symmetric); pairs that are equivalent under an automorphism of the graph are
counted separately.  "Smallest" means fewest vertices, then fewest edges, then the order of the atlas / of the
generated list.

Run:  python explore_open_cases.py [--maxn 8]
Output: results-open-cases.txt
"""

import argparse
import os
import sys
import time
from collections import Counter, defaultdict
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp import *  # noqa: E402,F401,F403


def run_graph(args):
    idx, n, es = args
    g = Gr(n, es)
    D = dist_matrix(g)
    diam = max(max(row) for row in D)
    dc, bad = in_dc(g, D)
    out = dict(a=Counter(), hist=Counter(), perpair=Counter(), sides=Counter(), b=Counter(), ex=defaultdict(list),
               graphs=Counter())
    out["graphs"]["n=%d" % n] += 1
    if not dc:
        out["graphs"]["n=%d not in DC" % n] += 1
    if diam == 3:
        out["graphs"]["diameter 3, n=%d" % n] += 1
        out["graphs"]["diameter 3, n=%d, in DC" % n if dc else "diameter 3, n=%d, not in DC" % n] += 1
    for u in range(n):
        for v in range(u + 1, n):
            d = D[u][v]
            c = edge_conn(g, u, v)
            cp, S = cp_brute(g, u, v)
            if d == 2 and c >= 3:
                cat = "cp = c" if cp == c else "cp = c + 1"
                out["a"][(n, c, cat)] += 1
                out["a"][("all", c, cat)] += 1
                rec = (n, g.m, idx, dict(edges=list(g.edges), u=u, v=v, c=c, cp=cp, dc=dc))
                if cp == c:
                    cc, cuts = min_cuts_by_sets(g, u, v)
                    full = g.full()
                    lens = set()
                    info = []
                    for C in cuts:
                        for vs, ps in simple_paths(g, u, v, removed=full ^ C):
                            out["hist"][len(ps)] += 1
                            lens.add(len(ps))
                            info.append((bits(C), vs))
                            # sides of the cut: A = component of u in G - C
                            A = component_mask(g, u, C)
                            out["sides"][(popcount(A), n - popcount(A))] += 1
                    out["perpair"][tuple(sorted(lens))] += 1
                    rec[3]["cuts_with_paths"] = [([g.edges[e] for e in cut], vs) for cut, vs in info]
                out["ex"][("a", cat, c)].append(rec)
                out["ex"][("a", cat)].append(rec)
            if diam == 3:
                gap = (c + d - 1) - cp
                out["b"][(n, d, c, gap)] += 1
                out["b"][("all", d, c, gap)] += 1
                if gap > 0:
                    rec = (n, g.m, idx, dict(edges=list(g.edges), u=u, v=v, c=c, d=d, cp=cp, dc=dc, gap=gap))
                    out["ex"][("b", "gap>0")].append(rec)
                    out["ex"][("b", "gap>0", d, c)].append(rec)
                    out["ex"][("b", "gap", d, c, gap)].append(rec)
    # keep only the three smallest examples per category
    for k in list(out["ex"]):
        out["ex"][k] = sorted(out["ex"][k], key=lambda r: r[:3])[:3]
    out["ex"] = dict(out["ex"])
    return out


def merge(total, part):
    for key in ("a", "hist", "perpair", "sides", "b", "graphs"):
        total[key].update(part[key])
    for k, lst in part["ex"].items():
        cur = total["ex"].setdefault(k, [])
        cur.extend(lst)
        cur.sort(key=lambda r: r[:3])
        del cur[3:]


def fmt_example(rec):
    n, m, idx, info = rec
    s = "n=%d m=%d: edges %s; u=%d v=%d" % (n, m, fmt_edges(info["edges"]), info["u"], info["v"])
    s += "; c=%d" % info["c"]
    if "d" in info:
        s += " d=%d" % info["d"]
    s += " cp=%d" % info["cp"]
    if "gap" in info:
        s += " (c+d-1-cp = %d)" % info["gap"]
    s += "; in DC: %s" % info["dc"]
    if "cuts_with_paths" in info:
        for cut, vs in info["cuts_with_paths"][:2]:
            s += "\n        minimum cut %s contains the path %s" % (fmt_edges(cut), "-".join(map(str, vs)))
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--maxn", type=int, default=8)
    ap.add_argument("--jobs", type=int, default=24)
    opts = ap.parse_args()
    lines = []

    def out(s=""):
        print(s, flush=True)
        lines.append(s)

    started = time.time()
    graphs = []
    for n in range(2, opts.maxn + 1):
        graphs.extend(connected_graphs(n, SCRATCH))
    out("explore_open_cases.py: all %d connected graphs with 2..%d vertices, unordered pairs" % (len(graphs), opts.maxn))
    total = dict(a=Counter(), hist=Counter(), perpair=Counter(), sides=Counter(), b=Counter(), ex={}, graphs=Counter())
    with Pool(opts.jobs) as pool:
        for part in pool.imap(run_graph, [(i, n, es) for i, (n, es) in enumerate(graphs)], chunksize=8):
            merge(total, part)
    G = total["graphs"]
    out("")
    out("Graphs: " + ", ".join("%d vertices: %d" % (n, G["n=%d" % n]) for n in range(2, opts.maxn + 1)))
    out("Graphs not in DC: " + (", ".join("%d vertices: %d" % (n, G["n=%d not in DC" % n]) for n in range(2, opts.maxn + 1) if G["n=%d not in DC" % n]) or "none"))

    out("")
    out("=== (a) pairs with d(u,v) = 2 and c(u,v) >= 3 ===")
    A = total["a"]
    out("%-10s %6s %12s %12s %10s" % ("graphs", "c", "cp = c", "cp = c + 1", "share cp=c"))
    for scope in list(range(5, opts.maxn + 1)) + ["all"]:
        for c in range(3, opts.maxn):
            x, y = A[(scope, c, "cp = c")], A[(scope, c, "cp = c + 1")]
            if x + y:
                out("%-10s %6d %12d %12d %9.2f%%" % ("n=%s" % scope if scope != "all" else "all", c, x, y, 100.0 * x / (x + y)))
        x = sum(A[(scope, c, "cp = c")] for c in range(3, opts.maxn))
        y = sum(A[(scope, c, "cp = c + 1")] for c in range(3, opts.maxn))
        out("%-10s %6s %12d %12d %9.2f%%" % ("n=%s" % scope if scope != "all" else "all", "any", x, y, 100.0 * x / max(x + y, 1)))
    out("")
    out("Pairs with cp = c: lengths of the u-v paths contained in a minimum cut")
    out("  number of (pair, minimum cut, path) triples by path length: %s" % dict(sorted(total["hist"].items())))
    out("  number of pairs by the set of lengths of their paths in minimum cuts: %s" % {k: v for k, v in sorted(total["perpair"].items())})
    out("  (|A|, |V - A|) of the cut that contains the path, A = u side: %s" % dict(sorted(total["sides"].items())))
    for kind in ("cp = c", "cp = c + 1"):
        out("")
        out("Three smallest examples with %s:" % kind)
        for rec in total["ex"].get(("a", kind), []):
            out("    " + fmt_example(rec))
        for c in range(3, opts.maxn):
            lst = total["ex"].get(("a", kind, c), [])
            if lst:
                out("  smallest with c = %d:" % c)
                out("    " + fmt_example(lst[0]))

    out("")
    out("=== (b) connected graphs of diameter exactly 3 ===")
    out("diameter-3 graphs: " + ", ".join("%d vertices: %d (in DC: %d, not in DC: %d)" % (
        n, G["diameter 3, n=%d" % n], G["diameter 3, n=%d, in DC" % n], G["diameter 3, n=%d, not in DC" % n]) for n in range(4, opts.maxn + 1)))
    B = total["b"]
    out("")
    out("Distribution of the gap (c + d - 1) - cp over all pairs of diameter-3 graphs, by (d, c); columns: gap 0, 1, 2, ...")
    maxgap = max((k[3] for k in B if k[0] == "all"), default=0)
    out("%-8s %-8s " % ("d", "c") + " ".join("%10s" % ("gap %d" % x) for x in range(maxgap + 1)))
    for d in (1, 2, 3):
        for c in range(1, opts.maxn):
            row = [B[("all", d, c, x)] for x in range(maxgap + 1)]
            if any(row):
                out("%-8d %-8d " % (d, c) + " ".join("%10d" % x for x in row))
    out("")
    out("Largest gap: %d" % maxgap)
    for n in range(4, opts.maxn + 1):
        pairs_n = sum(v for k, v in B.items() if k[0] == n)
        bad_n = sum(v for k, v in B.items() if k[0] == n and k[3] > 0)
        out("  n = %d: %d pairs in diameter-3 graphs, %d with cp < c + d - 1" % (n, pairs_n, bad_n))
    out("")
    out("Three smallest examples with cp < c + d - 1:")
    for rec in total["ex"].get(("b", "gap>0"), []):
        out("    " + fmt_example(rec))
    for d in (2, 3):
        for c in range(2, opts.maxn):
            for gap in range(1, maxgap + 1):
                lst = total["ex"].get(("b", "gap", d, c, gap), [])
                if lst:
                    out("  smallest with d = %d, c = %d, gap %d:" % (d, c, gap))
                    out("    " + fmt_example(lst[0]))
    out("")
    out("Time %.0f s." % (time.time() - started))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results-open-cases.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
