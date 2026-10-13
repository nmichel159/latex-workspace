"""Own exact routines (independent of hardness/exact.py and checks/mcp.py).

- maxflow(G, s, t): unit-capacity undirected max flow by BFS augmentation; returns (value, flow dict).
- min_cuts_pq(G, s, t): all minimum s-t cuts (as frozensets of the s side) as the closed sets of the
  residual digraph of one maximum flow (Picard-Queyranne), own enumeration of ideals.
- cut_sizes_bruteforce(G, s, t): numpy array of |delta(A)| over ALL A with s in A, t notin A (n <= ~25).
- cp_bruteforce(G, s, t): cp(s,t) = min over A of |delta(A)| + dist_{0/1}(s,t), where edges of delta(A)
  cost 0 and others cost 1 (independent of every lemma of theory-hardness.md).
"""
from collections import deque
import numpy as np
import networkx as nx


def maxflow(G, s, t):
    f = {}  # f[(a,b)] = net flow a->b in {-1,0,1}

    def fl(a, b):
        return f.get((a, b), 0)

    val = 0
    while True:
        par = {s: None}
        dq = deque([s])
        while dq and t not in par:
            x = dq.popleft()
            for y in G[x]:
                if y not in par and fl(x, y) < 1:
                    par[y] = x
                    dq.append(y)
        if t not in par:
            return val, f
        y = t
        while par[y] is not None:
            x = par[y]
            f[(x, y)] = fl(x, y) + 1
            f[(y, x)] = fl(y, x) - 1
            y = x
        val += 1


def residual_succ(G, f):
    return {x: [y for y in G[x] if f.get((x, y), 0) < 1] for x in G}


def reach(succ, start):
    seen = {start}
    dq = deque([start])
    while dq:
        x = dq.popleft()
        for y in succ[x]:
            if y not in seen:
                seen.add(y)
                dq.append(y)
    return seen


def min_cuts_pq(G, s, t, limit=10**6):
    val, f = maxflow(G, s, t)
    succ = residual_succ(G, f)
    pred = {x: [] for x in G}
    for x in G:
        for y in succ[x]:
            pred[y].append(x)
    forced_in = reach(succ, s)
    forced_out = reach(pred, t)
    assert not (forced_in & forced_out)
    free = [x for x in G if x not in forced_in and x not in forced_out]
    H = nx.DiGraph()
    H.add_nodes_from(free)
    for x in free:
        for y in succ[x]:
            if y in H:
                H.add_edge(x, y)
            else:
                assert y in forced_in, 'free vertex with residual arc to forced_out'
    C = nx.condensation(H)
    members = nx.get_node_attributes(C, 'members')
    order = list(reversed(list(nx.topological_sort(C))))  # successors first
    succC = {x: set(C.successors(x)) for x in C}
    out = []

    def rec(i, chosen):
        if len(out) > limit:
            raise RuntimeError('too many cuts')
        if i == len(order):
            A = set(forced_in)
            for x in chosen:
                A |= members[x]
            out.append(frozenset(A))
            return
        x = order[i]
        rec(i + 1, chosen)
        if succC[x] <= chosen:
            chosen.add(x)
            rec(i + 1, chosen)
            chosen.remove(x)

    rec(0, set())
    return val, out


def cut_size(G, A):
    return sum(1 for a, b in G.edges() if (a in A) != (b in A))


def cut_sizes_chunks(G, s, t, chunk_bits=18):
    """Yield (others, start, sizes) chunk by chunk; sizes[j] = |delta({s} + {others[i] : bit i of start+j})|."""
    others = [x for x in G if x not in (s, t)]
    k = len(others)
    idx = {x: i for i, x in enumerate(others)}
    step = 1 << min(chunk_bits, k)
    for start in range(0, 1 << k, step):
        masks = np.arange(start, start + step, dtype=np.uint32)
        sizes = np.zeros(step, dtype=np.int16)
        for a, b in G.edges():
            def side(x):
                if x == s:
                    return np.uint32(1)
                if x == t:
                    return np.uint32(0)
                return (masks >> np.uint32(idx[x])) & np.uint32(1)
            sizes += (side(a) ^ side(b)).astype(np.int16)
        yield others, start, sizes


def cut_sizes_bruteforce(G, s, t):
    """Return (others, sizes) with sizes[mask] = |delta({s} + {others[i] : bit i of mask})| (small n only)."""
    parts = list(cut_sizes_chunks(G, s, t))
    return parts[0][0], np.concatenate([p[2] for p in parts])


def dist01(G, s, t, A):
    """0-1 BFS: edges of delta(A) cost 0, others 1."""
    INF = 10**9
    d = {s: 0}
    dq = deque([s])
    while dq:
        x = dq.popleft()
        for y in G[x]:
            w = 0 if ((x in A) != (y in A)) else 1
            nd = d[x] + w
            if nd < d.get(y, INF):
                d[y] = nd
                if w == 0:
                    dq.appendleft(y)
                else:
                    dq.append(y)
    return d[t]


def cp_bruteforce(G, s, t):
    """Exact cp(s,t), c(s,t), and the list of minimum cuts, all by enumeration of all vertex sets."""
    c = None
    for others, start, sizes in cut_sizes_chunks(G, s, t):
        mn = int(sizes.min())
        c = mn if c is None else min(c, mn)
    d = nx.shortest_path_length(G, s, t)
    bound = c + d - 1
    cand = []
    for others, start, sizes in cut_sizes_chunks(G, s, t):
        for j in np.nonzero(sizes <= bound)[0]:
            cand.append((start + int(j), int(sizes[j])))
    best = None
    mincuts = []
    for mask, sz in cand:
        A = {s} | {others[i] for i in range(len(others)) if (mask >> i) & 1}
        if sz == c:
            mincuts.append(frozenset(A))
        val = sz + dist01(G, s, t, A)
        if best is None or val < best:
            best = val
    return best, c, d, mincuts


def cut_graph(G, A):
    H = nx.Graph()
    H.add_nodes_from(G)
    H.add_edges_from((a, b) for a, b in G.edges() if (a in A) != (b in A))
    return H
