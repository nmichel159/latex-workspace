"""Compare the layer algorithm with brute-force cp. Usage: run_compare.py SEED COUNT [GENS]

Every instance: three runs of the algorithm (Tarjan order; random flow and random linear extension;
flow changed along random cycles of D). All must agree on the value when no pair is recorded.
Prints a summary; any failure raises and prints the instance.
"""
import json
import random
import sys
import time
from collections import Counter

from core import (solve, brute_cp, brute_brute_cp, in_dc, sample_instance, bfs, connected, path_edges, flow,
                  check_cutpath, edges_of, cut_value)


def check_one(adj, u, v, rng, stats, g):
    du, _ = bfs(adj, u)
    d = du[v]
    cp = brute_cp(adj, u, v)
    assert cp in (d, d + 1), ("cp bound", cp, d)
    dc = in_dc(adj)
    stats['n'] += 1
    stats['gen_' + g] += 1
    stats['dc' if dc else 'notdc'] += 1
    stats['cp=d' if cp == d else 'cp=d+1'] += 1
    stats[('dc' if dc else 'notdc') + ('_cp=d' if cp == d else '_cp=d+1')] += 1
    if len(adj) >= 3:
        # pendant parts and bridges
        bridges = 0
        for a, b in edges_of(adj):
            if not connected(adj, a, b, frozenset([(a, b)])):
                bridges += 1
        if bridges:
            stats['has_bridge'] += 1
    runs = [dict(), dict(shuffle_order=True), dict(shuffle_order=True, cycles=3)]
    vals = set()
    for kw in runs:
        res = solve(adj, u, v, rng=rng, **kw)
        o = res['outcome']
        stats['out_' + o] += 1
        if o == 'found':
            R = res['rpath']
            assert R[0] == u and R[-1] == v and len(R) - 1 == d and len(set(R)) == len(R), "not a shortest path"
            for a, b in zip(R, R[1:]):
                assert b in adj[a]
            assert not connected(adj, u, v, frozenset(path_edges(R))), "returned path does not separate"
            assert cp == d, "found but brute force says d+1"
            vals.add(d)
        elif o == 'none':
            assert cp == d + 1, ("algorithm says d+1 but brute force says d", cp, d)
            assert check_cutpath(adj, u, v, res['cutpath']) and len(res['cutpath']) == d + 1
            vals.add(d + 1)
        elif o == 'record':
            x, y = res['pair']
            dx, _ = bfs(adj, x)
            assert dx[y] >= 3 and flow(adj, x, y, 3)[0] >= 3, "recorded pair is no witness"
            assert not dc, "record in DC"
            assert check_cutpath(adj, u, v, res['cutpath']) and len(res['cutpath']) == d + 1
        else:
            raise AssertionError("unexpected outcome " + o)
    assert len(vals) <= 1, ("runs disagree", vals)


def main():
    seed = int(sys.argv[1])
    count = int(sys.argv[2])
    gens = tuple(sys.argv[3].split(',')) if len(sys.argv) > 3 else ('sparse', 'chain', 'mutant')
    rng = random.Random(seed)
    stats = Counter()
    t0 = time.time()
    tries = 0
    while stats['n'] < count:
        tries += 1
        s = sample_instance(rng, gens=gens)
        if s is None:
            continue
        g, adj, u, v = s
        try:
            check_one(adj, u, v, rng, stats, g)
        except AssertionError as e:
            print("FAILURE", e)
            print(json.dumps(dict(n=len(adj), edges=edges_of(adj), u=u, v=v)))
            raise
        if stats['n'] % 5000 == 0:
            print(stats['n'], "done", round(time.time() - t0), "s", flush=True)
    stats['tries'] = tries
    print(json.dumps(dict(sorted(stats.items()))))
    print("seconds", round(time.time() - t0))


if __name__ == '__main__':
    main()
