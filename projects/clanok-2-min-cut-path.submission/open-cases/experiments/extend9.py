"""Tasks 2, 4, 5 on 9 vertices, exhaustively (with repetitions).

Every connected graph on 9 vertices is a connected graph on 8 vertices plus a vertex joined to a non-empty subset
(remove a non-cut vertex).  We take the 11117 connected 8-vertex graphs and all 255 subsets: 2,834,835 labelled
candidates, which cover every isomorphism class of connected 9-vertex graphs at least once.

A u-v path of length L inside a minimum cut gives c(u,v) >= L, so a path of length >= 5 needs deg u, deg v >= 5
and c(u,v) >= 5; on 9 vertices such a pair has d(u,v) <= 2 (two disjoint neighborhoods of size 5 do not fit),
and d(u,v) = 1 gives the length-1 path in every minimum cut.  So only pairs with d(u,v) = 2 and c(u,v) >= 5 can
have a shortest path of length >= 5 (weak type) or any path of length >= 5 (strong type); for these we enumerate
all paths inside minimum cuts.  Pairs with d(u,v) = 2, c(u,v) in {3, 4} only have paths of length 3 (counted too).
"""

import os
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cutpaths as cpz  # noqa: E402
from cutpaths import mcp, Gr, PairInfo  # noqa: E402

CACHE = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "tmp", "clanok-2-checks"))


def work(es8):
    stats = {"cand": 0, "pairs_d2_c3": 0, "pairs_d2_c3_yes": 0, "pairs_c5": 0, "weak": [], "strong": [],
             "cand_wrong": 0}
    for S in range(1, 256):
        edges = list(es8) + [(i, 8) for i in range(8) if (S >> i) & 1]
        stats["cand"] += 1
        deg = [0] * 9
        for a, b in edges:
            deg[a] += 1
            deg[b] += 1
        g = Gr(9, edges)
        D = None
        for u in range(9):
            if deg[u] < 3:
                continue
            du = mcp.bfs(g, u)
            for v in range(u + 1, 9):
                if deg[v] < 3 or du[v] != 2:
                    continue
                if min(deg[u], deg[v]) < 3:
                    continue
                P = PairInfo(g, u, v)
                if P.c < 3:
                    continue
                stats["pairs_d2_c3"] += 1
                if P.c < 5:
                    paths = P.cut_paths()
                    if paths:
                        stats["pairs_d2_c3_yes"] += 1
                        assert all(len(p) == 4 for p in paths)
                    continue
                stats["pairs_c5"] += 1
                paths = P.cut_paths()
                if paths:
                    stats["pairs_d2_c3_yes"] += 1
                lens = sorted(set(len(p) - 1 for p in paths))
                if paths and lens[0] >= 5:
                    stats["weak"].append((edges, u, v, lens))
                if paths and lens[-1] >= 5:
                    stats["strong"].append((edges, u, v, lens))
                if paths and (3 not in lens):
                    stats["cand_wrong"] += 1
    return stats


def main():
    t0 = time.time()
    base = mcp.connected_graphs(8, CACHE)
    tot = {"cand": 0, "pairs_d2_c3": 0, "pairs_d2_c3_yes": 0, "pairs_c5": 0, "weak": [], "strong": [], "cand_wrong": 0}
    with Pool(32) as pool:
        done = 0
        for st in pool.imap_unordered(work, [es for _, es in base], chunksize=4):
            for k in ("cand", "pairs_d2_c3", "pairs_d2_c3_yes", "pairs_c5", "cand_wrong"):
                tot[k] += st[k]
            tot["weak"] += st["weak"]
            tot["strong"] += st["strong"]
            done += 1
            if done % 1000 == 0:
                print(done, tot["cand"], tot["pairs_c5"], len(tot["weak"]), len(tot["strong"]),
                      "%.0f s" % (time.time() - t0), flush=True)
    lines = ["extend9.py: all connected 8-vertex graphs (11117) plus one vertex joined to every non-empty subset",
             "",
             "labelled candidates on 9 vertices: %d" % tot["cand"],
             "pairs (u < v) with d(u,v) = 2 and c(u,v) >= 3 (with repetitions): %d" % tot["pairs_d2_c3"],
             "  of them with a u-v path inside some minimum cut: %d" % tot["pairs_d2_c3_yes"],
             "  of them with c(u,v) >= 5: %d" % tot["pairs_c5"],
             "pairs with paths inside minimum cuts, all of length >= 5 (weak type): %d" % len(tot["weak"]),
             "pairs with some path of length >= 5 inside a minimum cut (strong type): %d" % len(tot["strong"]),
             "pairs where the length-3 test (O3) misses an existing path: %d" % tot["cand_wrong"]]
    for name in ("weak", "strong"):
        for edges, u, v, lens in tot[name][:10]:
            g = Gr(9, edges)
            lines.append("  %s: n=9 m=%d u=%d v=%d lengths %s in DC %s: %s"
                         % (name, g.m, u, v, lens, cpz.in_dc(g), cpz.fmt(g)))
    lines.append("Time %.0f s." % (time.time() - t0))
    with open(os.path.join(HERE, "results-extend9.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
