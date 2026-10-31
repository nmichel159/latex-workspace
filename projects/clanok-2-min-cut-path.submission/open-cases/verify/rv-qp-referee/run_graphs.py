"""Referee qp-referee: the chain of qp-proof.md on every open-case pair of every connected graph with at most 8 vertices.

Graph lists: networkx atlas (n <= 7) and verify/equivalence/graphs8.g6 (all graphs with 8 vertices; read as data).
Per graph: DC test by brute-force cut values; per ordered pair (u, v) with d = 2, c >= 3: Section 2 (Lemmas 2.1-2.8,
Theorem 2.9 against cp from Definition 1.1), Construction 3.1 and Lemmas 3.2, 3.3 (per down-set), Lemma 4.5, and for
yes-instances with s != t: all shortest valid paths with Lemmas 3.4, 4.2-4.4 and Theorem 5.3 (with Lemma 5.2 by the
proof's construction); exact IDESC (Definition 6.1) on every yes-instance and on every 10th no-instance.

usage: python run_graphs.py [workers] [stride]   (stride > 1: every stride-th graph only, for a smoke test)
"""
import os
import sys
import json
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import qpr_lib as L


def graphs():
    import networkx as nx
    gl = [g for g in nx.graph_atlas_g() if g.number_of_nodes() >= 3]
    g8 = os.path.join(os.path.dirname(HERE), "equivalence", "graphs8.g6")
    gl += list(nx.read_graph6(g8))
    out = []
    for g in gl:
        if not nx.is_connected(g):
            continue
        g = nx.convert_node_labels_to_integers(g)
        out.append((g.number_of_nodes(), [tuple(e) for e in g.edges()]))
    return out


def work(batch):
    stats = {}
    errs = []
    for gi, (n, edges) in batch:
        g = L.G(n, edges)
        c, cv = L.cvals_all(g)
        d = [g.dist(x) for x in range(n)]
        if any(d[x][y] > 2 and c[(x, y)] > 2 for x in range(n) for y in range(n) if x != y):
            stats["graphs not DC"] = stats.get("graphs not DC", 0) + 1
            continue
        stats["graphs DC"] = stats.get("graphs DC", 0) + 1
        for u in range(n):
            for v in range(n):
                if u == v or d[u][v] != 2 or c[(u, v)] < 3:
                    continue
                try:
                    zz, info = L.graph_to_zz(n, edges, u, v, stats)
                    sf, cinfo = L.zz_to_sf(zz)
                    same = L.check_lemma32_33(zz, sf, cinfo)
                    L.need(same, "L3.3: answers differ")
                    L.check_lemma45(sf, stats)
                    yes = zz.answer()
                    stats["max m"] = max(stats.get("max m", 0), sf.m)
                    if sf.s == sf.t:
                        stats["s = t"] = stats.get("s = t", 0) + 1
                        L.need(yes, "s = t but no-instance")
                    allD = sf.downsets()
                    if yes and sf.s != sf.t:
                        Ps = L.shortest_valid_paths(sf)
                        L.need(Ps, "L3.4(b): yes-instance without valid path")
                        for P in Ps:
                            L.need(L.is_valid(sf, P), "path not valid")
                            po = L.PathObj(sf, P)
                            L.check_lemma34(sf, P, po, allD)
                            L.check_section4(sf, P, po, stats)
                            L.theorem53(sf, P, stats)
                            stats["shortest paths checked"] = stats.get("shortest paths checked", 0) + 1
                    if not yes and sf.s != sf.t:
                        L.need(L.shortest_valid_paths(sf) == [], "L3.4: no-instance with a valid path")
                    stats["seen"] = stats.get("seen", 0) + 1
                    if yes or stats["seen"] % 10 == 0:
                        r = L.idesc_exact(sf)
                        if r is not None:
                            L.need(r == yes, "IDESC exact differs from the answer")
                            stats["IDESC exact run"] = stats.get("IDESC exact run", 0) + 1
                except L.Fail as e:
                    errs.append({"graph": gi, "n": n, "edges": edges, "u": u, "v": v, "err": str(e)})
                except Exception as e:
                    errs.append({"graph": gi, "n": n, "edges": edges, "u": u, "v": v, "err": "EXC " + repr(e),
                                 "tb": traceback.format_exc()})
    return stats, errs


def merge(tot, st):
    for k, v in st.items():
        if k.startswith("max"):
            tot[k] = max(tot.get(k, 0), v)
        elif isinstance(v, dict):
            h = tot.setdefault(k, {})
            for a, b in v.items():
                h[a] = h.get(a, 0) + b
        else:
            tot[k] = tot.get(k, 0) + v


def main():
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    stride = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    gl = graphs()
    items = [(i, gl[i]) for i in range(0, len(gl), stride)]
    batches = [items[i:i + 60] for i in range(0, len(items), 60)]
    t0 = time.time()
    tot = {}
    allerrs = []
    tag = "graphs-n8" + ("" if stride == 1 else "-stride%d" % stride)
    os.makedirs(os.path.join(HERE, "runs"), exist_ok=True)
    from multiprocessing import Pool
    with Pool(workers) as pool:
        for i, (st, errs) in enumerate(pool.imap_unordered(work, batches)):
            merge(tot, st)
            allerrs.extend(errs)
            if (i + 1) % 20 == 0:
                print("  %d/%d batches, %.0fs, pairs %d, errors %d" % (i + 1, len(batches), time.time() - t0,
                                                                     tot.get("pairs", 0), len(allerrs)), flush=True)
    with open(os.path.join(HERE, "runs", tag + ".txt"), "w") as f:
        f.write("%s: %d connected graphs, %.0fs\n" % (tag, len(items), time.time() - t0))
        for k in sorted(tot, key=str):
            f.write("  %-32s %s\n" % (k, tot[k]))
        f.write("  errors: %d\n" % len(allerrs))
        for e in allerrs[:30]:
            f.write("  " + json.dumps(e) + "\n")
    print(open(os.path.join(HERE, "runs", tag + ".txt")).read())


if __name__ == "__main__":
    main()
