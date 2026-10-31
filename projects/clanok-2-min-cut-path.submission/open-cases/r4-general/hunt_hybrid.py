"""Adversarial search for yes-instances of general ZZ + P2 on which the hybrid algorithm (pruning by forced-exit
propagation, then the side-set search with conflict families) needs large parameters.

State: a gcert.Inst (preorder with ties and one-way relations, middle edges).  Moves: add or delete an R-edge
between strictly comparable elements, add or delete a cover relation between middle classes (transitive closure
recomputed), merge two middle elements into a tie class, split a class.  An instance is kept only if it satisfies
P2 and is a yes-instance (gcert.exact).  Score = index of the first parameter set of LADDER that solves the pruned
instance (len(LADDER) if none), then the number of unfixed switches, then the length of a shortest solution.
Usage: python hunt_hybrid.py SEED STEPS NMID [START.json]
Output: progress lines and, for every new best score, the instance in JSON (runs/hunt-hybrid-SEED.jsonl).
"""
import sys
import json
import random
import time
import os
from common_r4 import gcert, dump, HERE
from gsw import GSW, prune, pruned_copy

LADDER = [(0, 0, 0, 0), (1, 0, 0, 2), (1, 0, 1, 3), (1, 1, 2, 4), (1, 1, 2, 6), (2, 1, 2, 6)]

seed, steps, nmid = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rng = random.Random(seed)
os.makedirs(os.path.join(HERE, "runs"), exist_ok=True)
out = open(os.path.join(HERE, "runs", "hunt-hybrid-%d.jsonl" % seed), "w")


def closure(le):
    n = len(le)
    le = [row[:] for row in le]
    for k in range(n):
        for i in range(n):
            if le[i][k]:
                for j in range(n):
                    if le[k][j]:
                        le[i][j] = True
    return le


def build(n, rel, R):
    """rel: set of pairs (a, b) meaning a <= b among all elements; u = 0, v = n - 1."""
    le = [[a == b for b in range(n)] for a in range(n)]
    for a, b in rel:
        le[a][b] = True
    for x in range(n):
        le[0][x] = True
        le[x][n - 1] = True
    le = closure(le)
    lt = [[le[a][b] and not le[b][a] for b in range(n)] for a in range(n)]
    R2 = [(a, b) for a, b in R if lt[a][b] and (a, b) != (0, n - 1)]
    return gcert.Inst(n, le, R2, 0, n - 1)


def score(I):
    G = GSW(I)
    fixed, dead = prune(G)
    if dead is None:
        return None
    H = pruned_copy(G, dead)
    for i, par in enumerate(LADDER):
        if H.decide(*par):
            break
    else:
        i = len(LADDER)
    ok, walk = gcert.exact(I, want_walk=True)
    D = I.downclose(sum(1 << x for x in walk[0::2]))
    p = gcert.cut_path(I, D)
    return (i, G.m - len(fixed), len(p) if p else 0)


def random_start():
    n = nmid + 4                 # u, one more bottom, middle, one more top, v
    rel = set()
    rel.add((1, 0))              # element 1 ~ u
    rel.add((n - 1, n - 2))      # element n-2 ~ v
    mids = list(range(2, n - 2))
    for a in mids:
        for b in mids:
            if a < b and rng.random() < 0.15:
                rel.add((a, b))
    I0 = build(n, rel, [])
    lt = I0.lt
    R = {(a, b) for a in range(n) for b in range(n) if lt[a][b] and rng.random() < 0.3}
    R = gcert.p2_complete(rng, n, I0.le, R)
    return n, rel, set(R)


def mutate(n, rel, R):
    rel, R = set(rel), set(R)
    mids = list(range(2, n - 2))
    r = rng.random()
    if r < 0.45:
        a, b = rng.randrange(n), rng.randrange(n)
        if (a, b) in R:
            R.discard((a, b))
        else:
            R.add((a, b))
    elif r < 0.7:
        a, b = rng.sample(mids, 2)
        if (a, b) in rel:
            rel.discard((a, b))
        else:
            rel.add((a, b))
    elif r < 0.85:
        a, b = rng.sample(mids, 2)
        rel.add((a, b))
        rel.add((b, a))
    else:
        if R:
            R.discard(rng.choice(sorted(R)))
    return n, rel, R


best = None
cur = None
t0 = time.time()
tries = 0
if len(sys.argv) > 4:
    # seeded start: an instance file (r4-search JSON format); the middle elements must be 2..n-3 for the moves, so
    # the instance is renumbered: u = 0, one element ~ u, middle, one element ~ v, v = n - 1 (added if missing)
    from common_r4 import load_json
    I0, d0 = load_json(sys.argv[4])
    order = [I0.u] + [x for x in range(I0.n) if x != I0.u and x != I0.v and (I0.B >> x) & 1]
    mids0 = [x for x in range(I0.n) if not (I0.B >> x) & 1 and not (I0.T >> x) & 1]
    tops0 = [x for x in range(I0.n) if x != I0.v and x != I0.u and (I0.T >> x) & 1]
    order = order + mids0 + tops0 + [I0.v]
    pos = {x: i for i, x in enumerate(order)}
    n = len(order)
    rel = {(pos[a], pos[b]) for a in range(I0.n) for b in range(I0.n) if I0.le[a][b] and a != b}
    R = {(pos[a], pos[b]) for a, b in I0.R}
    I = build(n, rel, R)
    assert I.p2() and gcert.exact(I)
    cur = (n, rel, R, score(I))
while cur is None:
    n, rel, R = random_start()
    I = build(n, rel, R)
    if I.p2() and gcert.exact(I):
        sc = score(I)
        if sc is not None:
            cur = (n, rel, R, sc)
    tries += 1
best = cur[3]
for step in range(steps):
    n, rel, R = mutate(cur[0], cur[1], cur[2])
    I = build(n, rel, R)
    if not I.p2() or not gcert.exact(I):
        continue
    sc = score(I)
    if sc is None:
        continue
    if sc >= cur[3] or rng.random() < 0.05:
        cur = (n, rel, R, sc)
        if sc > best:
            best = sc
            out.write(json.dumps(dump(I, {"score": list(sc), "step": step})) + "\n")
            out.flush()
            print("step %d best %s (q=%d |R|=%d) %.0fs" % (step, sc, I.n, len(I.R), time.time() - t0), flush=True)
    if step % 2000 == 0:
        print("step %d current %s best %s %.0fs" % (step, cur[3], best, time.time() - t0), flush=True)
print("done: best", best)
