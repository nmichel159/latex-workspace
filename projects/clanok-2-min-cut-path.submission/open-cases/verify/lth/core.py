"""Own implementations for the verification of dc-hardness.md (agent verify-LTH).

Written from the definitions in dc-hardness.md and theory-dc.md only; no import of other agents' scripts.

2CH instance: (N, s, t, sw) with nodes 0..N-1, terminals s, t, and sw a list of switches (E, F), each side an int
bitmask over the nodes (0 = empty side). Side id of side m (0 = E, 1 = F) of switch w is 2*w + m; partner = id ^ 1.
A mode vector picks one side per switch; the question is whether s and t are connected in the hypergraph of the
picked sides (s == t counts as connected).

TIC instance: (K, sw) with sw a list of (E, F), each None or (l, r), 0 <= l <= r <= K (spans of junctions);
equivalent 2CH: nodes 0..K, s = 0, t = K.
"""
import itertools
import random
from collections import deque


# ----------------------------------------------------------------------------------------------- 2CH basics

def popcount(x):
    return bin(x).count("1")


def bits(x):
    out = []
    i = 0
    while x:
        if x & 1:
            out.append(i)
        x >>= 1
        i += 1
    return out


def reach_from(s, sides):
    """Node mask reachable from node s through the given side masks."""
    reach = 1 << s
    rem = [x for x in sides if x]
    changed = True
    while changed:
        changed = False
        nr = []
        for x in rem:
            if x & reach:
                if x & ~reach:
                    reach |= x
                changed = True
            else:
                nr.append(x)
        rem = nr
    return reach


def connects(inst, modes):
    N, s, t, sw = inst
    if s == t:
        return True
    sides = [sw[w][modes[w]] for w in range(len(sw))]
    return bool(reach_from(s, sides) >> t & 1)


def brute_2ch(inst, all_solutions=False):
    """Exhaustive search over all 2^n mode vectors. Returns (answer, list of solutions or first one)."""
    N, s, t, sw = inst
    n = len(sw)
    if s == t:
        return True, [tuple([0] * n)]
    sols = []
    for code in range(1 << n):
        modes = tuple((code >> w) & 1 for w in range(n))
        sides = [sw[w][modes[w]] for w in range(n)]
        if reach_from(s, sides) >> t & 1:
            sols.append(modes)
            if not all_solutions:
                return True, sols
    return bool(sols), sols


def relaxation_2ch(inst):
    """Both sides of every switch picked."""
    N, s, t, sw = inst
    if s == t:
        return True
    sides = [x for pair in sw for x in pair]
    return bool(reach_from(s, sides) >> t & 1)


def p2_2ch(inst):
    N, s, t, sw = inst
    for a in range(len(sw)):
        for b in range(a + 1, len(sw)):
            if not (sw[a][0] & sw[b][0]) and not (sw[a][1] & sw[b][1]):
                return False
    return True


def p2_violations(sw):
    return [(a, b) for a in range(len(sw)) for b in range(a + 1, len(sw))
            if not (sw[a][0] & sw[b][0]) and not (sw[a][1] & sw[b][1])]


# ----------------------------------------------------------------------------------------------- TIC basics

def span_mask(sp):
    if sp is None:
        return 0
    l, r = sp
    return ((1 << (r + 1)) - 1) ^ ((1 << l) - 1)


def tic_to_2ch(K, sw):
    return (K + 1, 0, K, [(span_mask(E), span_mask(F)) for (E, F) in sw])


def edge_mask(sp):
    """Edges (j-1, j), j = 1..K, covered by span sp, as bitmask with bit j."""
    if sp is None:
        return 0
    l, r = sp
    if r <= l:
        return 0
    return ((1 << (r + 1)) - 1) ^ ((1 << (l + 1)) - 1)


def brute_tic(K, sw, all_solutions=False):
    n = len(sw)
    if K == 0:
        return True, [tuple([0] * n)]
    full = ((1 << (K + 1)) - 1) ^ 1
    em = [(edge_mask(E), edge_mask(F)) for (E, F) in sw]
    sols = []
    for code in range(1 << n):
        cov = 0
        for w in range(n):
            cov |= em[w][(code >> w) & 1]
        if cov == full:
            sols.append(tuple((code >> w) & 1 for w in range(n)))
            if not all_solutions:
                return True, sols
    return bool(sols), sols


def p2_tic(sw):
    def meet(a, b):
        return a is not None and b is not None and max(a[0], b[0]) <= min(a[1], b[1])
    for a in range(len(sw)):
        for b in range(a + 1, len(sw)):
            if not meet(sw[a][0], sw[b][0]) and not meet(sw[a][1], sw[b][1]):
                return False
    return True


# ----------------------------------------------------------------------------------------------- Theorem T

def tic_T(K, sw, full_guesses=False, want_witness=False):
    """Algorithm of Theorem T (dc-hardness.md Section 5), implemented from the text.

    Guess phi = (phi_g) for the four groups g = (type, index parity), each a junction or None. BFS over states
    (previous span, current span, parity of the current index, set of members so far that contain a phi junction).
    Chain conditions: left and right ends strictly increase, consecutive spans share a junction,
    right(prev) < left(next); first span contains 0, last contains K.
    (i) partner of every member is empty or contains phi of its group;
    (ii) no two stored members (members containing some phi junction) belong to one switch.
    With full_guesses=False the guesses run over one junction per class of junctions with the same membership in
    all spans (the conditions depend on phi only through membership, so this is exact).
    """
    if K == 0:
        return (True, None) if want_witness else True
    span = {}
    for w, (E, F) in enumerate(sw):
        if E is not None:
            span[2 * w] = E
        if F is not None:
            span[2 * w + 1] = F
    sids = sorted(span)
    if full_guesses:
        cand = list(range(K + 1))
    else:
        seen = {}
        for j in range(K + 1):
            sig = tuple(span[i][0] <= j <= span[i][1] for i in sids)
            seen.setdefault(sig, j)
        cand = sorted(seen.values())
    vals = cand + [None]

    def inside(j, sp):
        return j is not None and sp[0] <= j <= sp[1]

    succ = {i: [k for k in sids if span[k][0] > span[i][0] and span[k][1] > span[i][1]
                and span[k][0] <= span[i][1]] for i in sids}
    starts = [i for i in sids if span[i][0] == 0]
    for phi in itertools.product(vals, repeat=4):
        def adm(i, par):
            p = span.get(i ^ 1)
            if p is None:
                return True
            g = (i & 1) * 2 + par
            return inside(phi[g], p)
        cphi = {i: any(inside(phi[g], span[i]) for g in range(4)) for i in sids}
        q = deque()
        seen_states = set()
        for i in starts:
            if not adm(i, 1):
                continue
            st = (None, i, 1, frozenset([i]) if cphi[i] else frozenset())
            if st not in seen_states:
                seen_states.add(st)
                q.append((st, (i,)))
        while q:
            (prev, cur, par, stored), chain = q.popleft()
            if span[cur][1] == K:
                return (True, (phi, chain)) if want_witness else True
            for nx in succ[cur]:
                if prev is not None and not span[prev][1] < span[nx][0]:
                    continue
                npar = par ^ 1
                if not adm(nx, npar):
                    continue
                ns = stored
                if cphi[nx]:
                    if (nx ^ 1) in stored:
                        continue
                    ns = stored | {nx}
                st = (cur, nx, npar, ns)
                if st not in seen_states:
                    seen_states.add(st)
                    q.append((st, chain + (nx,)))
    return (False, None) if want_witness else False


# ----------------------------------------------------------------------------------------------- Theorem H

def node_classes(inst):
    """One representative per class of nodes with the same membership in all non-empty sides."""
    N, s, t, sw = inst
    seen = {}
    for x in range(N):
        sig = tuple(((side >> x) & 1) for pair in sw for side in pair)
        seen.setdefault(sig, x)
    return sorted(seen.values())


def h_search(inst, tpar, want_witness=False, reps=True, max_per_node=2):
    """Search of Theorem H (dc-hardness.md Section 5), implemented from the text.

    Guess Phi_g (g = (type, parity)), sets of at most tpar nodes. BFS over walks of sides (repetitions allowed,
    consecutive sides share a node), state = (current side, parity, set of members so far that meet
    Phi = union of the Phi_g). Requirements: (i) every member's partner is empty or meets Phi_g of its group;
    (ii) no two stored members are the two sides of one switch; at most max_per_node stored members through each
    node of Phi. Start: a side containing s at index 1; accept: current side contains t.
    reps=True restricts the nodes in the guesses to one per membership class (exact).
    """
    N, s, t, sw = inst
    if s == t:
        return (True, None) if want_witness else True
    side = {}
    for w, (E, F) in enumerate(sw):
        if E:
            side[2 * w] = E
        if F:
            side[2 * w + 1] = F
    sids = sorted(side)
    nodes = node_classes(inst) if reps else list(range(N))
    cands = [0]
    for k in range(1, tpar + 1):
        for comb in itertools.combinations(nodes, k):
            m = 0
            for x in comb:
                m |= 1 << x
            cands.append(m)
    nbr = {i: [k for k in sids if side[k] & side[i]] for i in sids}
    starts = [i for i in sids if side[i] >> s & 1]
    for Phi in itertools.product(cands, repeat=4):
        PhiU = Phi[0] | Phi[1] | Phi[2] | Phi[3]
        phinodes = bits(PhiU)

        def adm(i, par):
            p = side.get(i ^ 1, 0)
            if not p:
                return True
            g = (i & 1) * 2 + par
            return bool(p & Phi[g])

        def ok_store(stored, i):
            if (i ^ 1) in stored:
                return False
            ns = stored | {i}
            for x in phinodes:
                if sum(1 for j in ns if side[j] >> x & 1) > max_per_node:
                    return False
            return True

        q = deque()
        seen_states = set()
        for i in starts:
            if not adm(i, 1):
                continue
            if side[i] & PhiU:
                if not ok_store(frozenset(), i):
                    continue
                stored = frozenset([i])
            else:
                stored = frozenset()
            st = (i, 1, stored)
            if st not in seen_states:
                seen_states.add(st)
                q.append((st, (i,)))
        while q:
            (cur, par, stored), walk = q.popleft()
            if side[cur] >> t & 1:
                return (True, (Phi, walk)) if want_witness else True
            for nx in nbr[cur]:
                npar = par ^ 1
                if not adm(nx, npar):
                    continue
                ns = stored
                if side[nx] & PhiU:
                    if nx not in stored:
                        if not ok_store(stored, nx):
                            continue
                        ns = stored | {nx}
                    elif (nx ^ 1) in stored:
                        continue
                st = (nx, npar, ns)
                if st not in seen_states:
                    seen_states.add(st)
                    q.append((st, walk + (nx,)))
    return (False, None) if want_witness else False


def walk_is_consistent(inst, walk):
    """A walk of side ids is a valid certificate: consistent modes, consecutive sides meet, s in first, t in last."""
    N, s, t, sw = inst
    mode = {}
    for i in walk:
        w, m = i >> 1, i & 1
        if mode.get(w, m) != m:
            return False
        mode[w] = m
    sides = [sw[i >> 1][i & 1] for i in walk]
    if not (sides[0] >> s & 1) or not (sides[-1] >> t & 1):
        return False
    return all(sides[a] & sides[a + 1] for a in range(len(sides) - 1))


# ----------------------------------------------------------------------------------------------- shortest sequences

def shortest_sequences(inst, modes, limit=2000):
    """All shortest sequences of picked sides (side ids) from s to t for the given mode vector."""
    N, s, t, sw = inst
    picked = [2 * w + modes[w] for w in range(len(sw)) if sw[w][modes[w]]]
    side = {i: sw[i >> 1][i & 1] for i in picked}
    dist = {}
    q = deque()
    for i in picked:
        if side[i] >> s & 1:
            dist[i] = 1
            q.append(i)
    while q:
        i = q.popleft()
        for k in picked:
            if k not in dist and side[k] & side[i]:
                dist[k] = dist[i] + 1
                q.append(k)
    ends = [i for i in picked if i in dist and side[i] >> t & 1]
    if not ends:
        return []
    L = min(dist[i] for i in ends)
    out = []

    def back(seq):
        if len(out) >= limit:
            return
        i = seq[0]
        if dist[i] == 1:
            out.append(tuple(seq))
            return
        for k in picked:
            if dist.get(k) == dist[i] - 1 and side[k] & side[i]:
                back([k] + seq)

    for e in ends:
        if dist[e] == L:
            back([e])
    return out


def piercing_number(masks, N):
    """Smallest number of nodes meeting every mask (masks non-empty)."""
    if not masks:
        return 0
    for k in range(0, N + 1):
        for comb in itertools.combinations(range(N), k):
            m = 0
            for x in comb:
                m |= 1 << x
            if all(x & m for x in masks):
                return k
    return None


def group_partner_families(inst, seq):
    N, s, t, sw = inst
    fam = {g: [] for g in range(4)}
    for a, i in enumerate(seq, start=1):
        g = (i & 1) * 2 + (a % 2)
        p = sw[i >> 1][(i & 1) ^ 1]
        if p:
            fam[g].append(p)
    return fam


def is_helly(masks):
    """Every pairwise intersecting subfamily has a common node (brute force over subfamilies; small inputs)."""
    masks = [m for m in masks if m]
    k = len(masks)
    # Berge-type reduction is not used; plain enumeration of cliques of the intersection graph.
    adj = [[bool(masks[a] & masks[b]) for b in range(k)] for a in range(k)]
    def rec(chosen, common, start):
        for b in range(start, k):
            if all(adj[a][b] for a in chosen):
                nc = common & masks[b]
                if not nc:
                    return False
                if not rec(chosen + [b], nc, b + 1):
                    return False
        return True
    return rec([], -1, 0)


# ----------------------------------------------------------------------------------------------- ZZ

class ZZ:
    """ZZ instance: elements 0..q-1, leq[a][b] preorder, R set of frozensets {a, b} with a < b strictly, u, v."""

    def __init__(self, q, leq, R, u, v):
        self.q, self.leq, self.R, self.u, self.v = q, leq, R, u, v
        self.adj = [[] for _ in range(q)]
        for e in R:
            a, b = tuple(e)
            self.adj[a].append(b)
            self.adj[b].append(a)

    def lt(self, a, b):
        return self.leq[a][b] and not self.leq[b][a]

    def comparable(self, a, b):
        return self.leq[a][b] or self.leq[b][a]

    def check_instance(self):
        q, leq = self.q, self.leq
        for a in range(q):
            assert leq[a][a]
            assert leq[self.u][a] and leq[a][self.v]
            for b in range(q):
                for c in range(q):
                    if leq[a][b] and leq[b][c]:
                        assert leq[a][c]
        for e in self.R:
            a, b = tuple(e)
            assert self.lt(a, b) or self.lt(b, a)
        assert frozenset((self.u, self.v)) not in self.R

    def p2(self):
        for x in range(self.q):
            for y in range(x + 1, self.q):
                if self.comparable(x, y):
                    continue
                ok = False
                for z in self.adj[x]:
                    if z in self.adj[y] and ((self.lt(z, x) and self.lt(z, y)) or (self.lt(x, z) and self.lt(y, z))):
                        ok = True
                        break
                if not ok:
                    return False
        return True

    def solve(self, want_path=False):
        """DFS over simple alternating paths, pruning inconsistent prefixes (consistency is hereditary)."""
        u, v = self.u, self.v
        path = [u]
        onpath = {u}
        valleys = [u]
        peaks = []

        def dfs():
            x = path[-1]
            pos = len(path) - 1
            for y in self.adj[x]:
                if y in onpath:
                    continue
                if pos % 2 == 0:   # x valley, y peak: x < y
                    if not self.lt(x, y):
                        continue
                    if any(self.leq[y][a] for a in valleys):
                        continue
                    if y == v:
                        path.append(y)
                        return True
                    path.append(y); onpath.add(y); peaks.append(y)
                    if dfs():
                        return True
                    path.pop(); onpath.discard(y); peaks.pop()
                else:              # x peak, y valley: y < x
                    if not self.lt(y, x):
                        continue
                    if y == v:
                        continue
                    if any(self.leq[b][y] for b in peaks):
                        continue
                    path.append(y); onpath.add(y); valleys.append(y)
                    if dfs():
                        return True
                    path.pop(); onpath.discard(y); valleys.pop()
            return False

        r = dfs()
        return (r, list(path) if r else None) if want_path else r


def twoch_to_zz(inst):
    """SW form of a 2CH instance: node n -> bottom b_n = n and top t_n = N + n with the real edge b_n t_n;
    switch w -> element 2N + w with real edges to the bottoms of E_w and the tops of F_w; bottoms equivalent to
    u = b_s, tops equivalent to v = t_t, switches pairwise incomparable between them."""
    N, s, t, sw = inst
    n = len(sw)
    q = 2 * N + n
    rank = [0] * N + [2] * N + [1] * n
    leq = [[(rank[a] < rank[b]) or (rank[a] == rank[b] and (rank[a] != 1 or a == b)) for b in range(q)]
           for a in range(q)]
    R = set()
    for x in range(N):
        R.add(frozenset((x, N + x)))
    for w, (E, F) in enumerate(sw):
        for x in bits(E):
            R.add(frozenset((x, 2 * N + w)))
        for x in bits(F):
            R.add(frozenset((2 * N + w, N + x)))
    u, v = s, N + t
    if frozenset((u, v)) in R:     # s == t: the instance is trivially yes; keep the edge out of R
        R.discard(frozenset((u, v)))
    return ZZ(q, leq, R, u, v)


# ----------------------------------------------------------------------------------------------- generators

def rand_span(rng, K, p_zero=0.15, maxlen=None):
    if maxlen is None:
        maxlen = K
    l = rng.randint(0, K)
    if rng.random() < p_zero:
        return (l, l)
    r = min(K, l + rng.randint(1, max(1, maxlen)))
    if r == l:
        l = max(0, l - 1)
    return (l, r)


def repair_p2_tic(rng, K, sw):
    sw = [list(x) for x in sw]
    def meet(a, b):
        return a is not None and b is not None and max(a[0], b[0]) <= min(a[1], b[1])
    for _ in range(10000):
        bad = [(a, b) for a in range(len(sw)) for b in range(a + 1, len(sw))
               if not meet(sw[a][0], sw[b][0]) and not meet(sw[a][1], sw[b][1])]
        if not bad:
            return [tuple(x) for x in sw]
        a, b = rng.choice(bad)
        types = [m for m in (0, 1) if sw[a][m] is not None and sw[b][m] is not None]
        if not types:
            m = rng.randint(0, 1)
            if sw[a][m] is None:
                sw[a][m] = rand_span(rng, K)
            else:
                sw[b][m] = rand_span(rng, K)
            continue
        m = rng.choice(types)
        x, y = (a, b) if rng.random() < 0.5 else (b, a)
        X, Y = sw[x][m], sw[y][m]
        # extend X towards Y until they meet
        if X[1] < Y[0]:
            newX = (X[0], Y[0] + (rng.random() < 0.3 and Y[0] < Y[1]))
            newX = (newX[0], min(newX[1], K))
        else:
            newX = (Y[1] - (rng.random() < 0.3 and Y[0] < Y[1]), X[1])
            newX = (max(newX[0], 0), newX[1])
        sw[x][m] = newX
    raise RuntimeError("repair failed")


def rand_tic(rng, K, n, p_empty=0.1, p_zero=0.1, maxlen=None, p2=True):
    sw = []
    for _ in range(n):
        E = None if rng.random() < p_empty else rand_span(rng, K, p_zero, maxlen)
        F = None if rng.random() < p_empty else rand_span(rng, K, p_zero, maxlen)
        if E is None and F is None:
            E = rand_span(rng, K, p_zero, maxlen)
        sw.append((E, F))
    if p2:
        sw = repair_p2_tic(rng, K, sw)
    return sw


def rand_2ch(rng, N, n, dens=0.3, p_empty=0.1, p2=True, s=0, t=None):
    if t is None:
        t = N - 1
    sw = []
    for _ in range(n):
        pair = []
        for m in range(2):
            if rng.random() < p_empty:
                pair.append(0)
            else:
                x = 0
                while not x:
                    for y in range(N):
                        if rng.random() < dens:
                            x |= 1 << y
                pair.append(x)
        sw.append(pair)
    if p2:
        for _ in range(10000):
            bad = p2_violations(sw)
            if not bad:
                break
            a, b = rng.choice(bad)
            m = rng.randint(0, 1)
            y = rng.randrange(N)
            sw[a][m] |= 1 << y
            sw[b][m] |= 1 << y
    return (N, s, t, [tuple(x) for x in sw])


def rand_tree(rng, N):
    par = [None] + [rng.randrange(i) for i in range(1, N)]
    adj = [[] for _ in range(N)]
    for i in range(1, N):
        adj[i].append(par[i]); adj[par[i]].append(i)
    return adj


def tree_path(adj, a, b):
    prev = {a: None}
    q = deque([a])
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y not in prev:
                prev[y] = x
                q.append(y)
    p = []
    x = b
    while x is not None:
        p.append(x)
        x = prev[x]
    return p


def rand_subtree(rng, adj, size):
    N = len(adj)
    start = rng.randrange(N)
    S = {start}
    while len(S) < size:
        front = [y for x in S for y in adj[x] if y not in S]
        if not front:
            break
        S.add(rng.choice(front))
    m = 0
    for x in S:
        m |= 1 << x
    return m


def rand_tree_2ch(rng, N, n, p_empty=0.1, maxsize=3):
    """2CH + P2 instance whose sides are subtrees of a random tree (Helly)."""
    adj = rand_tree(rng, N)
    sw = []
    for _ in range(n):
        pair = []
        for m in range(2):
            if rng.random() < p_empty:
                pair.append(0)
            else:
                pair.append(rand_subtree(rng, adj, rng.randint(1, maxsize)))
        if not pair[0] and not pair[1]:
            pair[0] = rand_subtree(rng, adj, rng.randint(1, maxsize))
        sw.append(pair)
    for _ in range(10000):
        bad = p2_violations(sw)
        if not bad:
            break
        a, b = rng.choice(bad)
        types = [m for m in (0, 1) if sw[a][m] and sw[b][m]]
        if not types:
            m = rng.randint(0, 1)
            if not sw[a][m]:
                sw[a][m] = rand_subtree(rng, adj, rng.randint(1, maxsize))
            else:
                sw[b][m] = rand_subtree(rng, adj, rng.randint(1, maxsize))
            continue
        m = rng.choice(types)
        x, y = (a, b) if rng.random() < 0.5 else (b, a)
        # connect subtree x to subtree y along the tree path between them (keeps a subtree)
        xa = bits(sw[x][m])[0]
        yb = bits(sw[y][m])[0]
        for z in tree_path(adj, xa, yb):
            sw[x][m] |= 1 << z
    s, t = rng.sample(range(N), 2)
    return (N, s, t, [tuple(x) for x in sw]), adj
