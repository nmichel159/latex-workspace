"""Point (d): try to break thm:characterization where condition (i) is met by a path p although every
shortest u-x path enters the square at the other entering terminal alpha.

Graph H1 (built by hand for the full decomposition): the square contains alpha, x, w, y and two long
alpha-y routes; the entering edges end in alpha (from u directly) and in x (after a detour); the leaving edges
start in y (to v directly) and in w (detour).  d(u,x) = 2 only through alpha, p = x,w,y.
Then a random search for more instances, and the full battery of statements.py on each.
"""

import os
import random
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ref
import statements
from ref import fmt, fmt_e

H1 = [("u", "A"), ("u", "s1"), ("s1", "s2"), ("s2", "s3"), ("s3", "x"),
      ("A", "x"), ("x", "w"), ("w", "y"),
      ("A", "k1"), ("k1", "k2"), ("k2", "k3"), ("k3", "y"),
      ("A", "m1"), ("m1", "m2"), ("m2", "m3"), ("m3", "y"),
      ("y", "v"), ("w", "B"), ("B", "t1"), ("t1", "t2"), ("t2", "t3"), ("t3", "v")]


def report(name, edges, u, v):
    adj = ref.graph(edges)
    cuts = ref.min_cuts2(adj, u, v)
    p1, p2 = ref.two_disjoint_paths(adj, u, v)
    D = ref.Decomposition(adj, u, v, cuts, p1, p2)
    du, dv = ref.bfs(adj, u), ref.bfs(adj, v)
    print("%s: n = %d, m = %d, c(u,v) = %d, d(u,v) = %d, cp(u,v) = %d, in the class: %s" % (
        name, len(adj), len(ref.edges_of(adj)), ref.cutvalue(adj, u, v), du[v],
        ref.cp_bruteforce(adj, u, v)[0], ref.in_class(adj)[0]))
    print("  squares:", [fmt(S) for S in D.squares], "links:", sorted(fmt(L) for L in D.links))
    for i, S in enumerate(D.squares):
        a, b, c, d = D.terminals(i)
        for x, al in dict.fromkeys(((a, b), (b, a))):
            for y, be in dict.fromkeys(((c, d), (d, c))):
                for p in ref.all_simple_paths(adj, x, y, allowed=S):
                    if du[x] + len(p) - 1 + dv[y] != du[v]:
                        continue
                    if be in ref.bfs(adj, al, set(ref.path_edges(p)), allowed=S):
                        continue
                    sx = statements.shortest_paths(adj, u, x)
                    via = [al in R for R in sx]
                    print("  witness: square %d, (x,alpha) = (%s,%s), (y,beta) = (%s,%s), p = %s; "
                          "shortest u-x paths: %d, through alpha: %d" % (
                              i + 1, x, al, y, be, ",".join(map(str, p)), len(sx), sum(via)))
    done, info, fails = statements.check_pair(adj, u, v, random.Random(1), cap=6)
    print("  statements.py: %d checks, failures: %d" % (sum(done.values()), len(fails)))
    for k in sorted(info):
        if "witness" in k or "enters" in k:
            print("    info:", k, info[k])
    for f in fails[:5]:
        print("    FAIL", f)
    return fails


fails = report("H1", H1, "u", "v")

# random search: blocks with a hub structure, biased to long detours
rng = random.Random(11)
tot = Counter()
allfails = []
found_full = 0
examples = []
for trial in range(6000):
    n_in = rng.randint(4, 8)
    es = set()
    for i in range(1, n_in):
        es.add((rng.randrange(i), i))
    for _ in range(rng.randint(1, 6)):
        a, b = rng.sample(range(n_in), 2)
        es.add((min(a, b), max(a, b)))
    nxt = n_in
    U, V = "u", "v"
    edges = [(a, b) for a, b in es]

    def route(a, b, length):
        global nxt
        prev = a
        for _ in range(length - 1):
            edges.append((prev, nxt))
            prev = nxt
            nxt += 1
        edges.append((prev, b))
    ea, ex, ly, lb = [rng.randrange(n_in) for _ in range(4)]
    route(U, ea, 1)
    route(U, ex, rng.randint(2, 5))
    route(ly, V, 1)
    route(lb, V, rng.randint(2, 5))
    adj = ref.graph(edges)
    if ref.cutvalue(adj, U, V, limit=3) != 2:
        continue
    done, info, fails = statements.check_pair(adj, U, V, rng, cap=3)
    tot.update(info)
    allfails += fails
    if info.get("... and R enters the square at alpha", 0):
        found_full += 1
        if len(examples) < 3:
            examples.append(sorted(edges, key=str))
print("random search: instances with c(u,v) = 2: %d" % sum(1 for _ in [0]) if False else "random search finished")
for k in sorted(tot):
    if "witness" in k or "enters" in k or "skipped" in k:
        print("  info:", k, tot[k])
print("  instances (full decomposition) where a witness p is met only after entering at alpha:", found_full)
for ex in examples:
    print("   example:", " ".join("%s-%s" % e for e in ex))
print("  failures:", len(allfails) + len(fails))
for f in allfails[:5]:
    print("   FAIL", f)
