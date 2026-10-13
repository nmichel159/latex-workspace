"""Exhaustive run: every connected graph with 2..8 vertices (atlas for n <= 7, graphs8.g6 for n = 8),
every ordered pair (u, v): checks.check_graph. Usage: python run_small.py [workers] > results-small.txt"""
import sys, time
from collections import Counter
from multiprocessing import Pool
import networkx as nx
from networkx.generators.atlas import graph_atlas_g
from checks import check_graph


def work(item):
    n, edges = item
    return check_graph(n, edges, ordered=True, do_cp=True)


def graphs():
    for g in graph_atlas_g():
        n = g.number_of_nodes()
        if 2 <= n <= 7 and nx.is_connected(g):
            yield n, sorted((min(a, b), max(a, b)) for a, b in g.edges())
    with open("graphs8.g6", "rb") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            g = nx.from_graph6_bytes(line)
            if nx.is_connected(g):
                yield 8, sorted((min(a, b), max(a, b)) for a, b in g.edges())


if __name__ == "__main__":
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    t0 = time.time()
    items = list(graphs())
    bysize = Counter(n for n, _ in items)
    print("connected graphs by order:", dict(sorted(bysize.items())))
    total = Counter()
    viol = []
    with Pool(workers) as pool:
        for st, vi in pool.imap_unordered(work, items, chunksize=20):
            total.update(st)
            viol.extend(vi)
    for k in sorted(total):
        print("%-55s %d" % (k, total[k]))
    print("violations:", len(viol))
    for x in viol[:40]:
        print("  ", x)
    print("time %.1fs" % (time.time() - t0))
