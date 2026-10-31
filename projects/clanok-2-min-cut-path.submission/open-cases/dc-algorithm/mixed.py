"""Mixed witnesses in ZZ + P2 (dc-algorithm.md Section 11).

Instances are zz.ZZ objects (preorder `le`, real edges R, u least, v greatest).
- witness kinds of an incomparable pair {x, y}: common R-neighbours w strictly below both ('B' if w ~ u, else 'ML')
  or strictly above both ('T' if w ~ v, else 'MU');
- the lower-only graph U (incomparable pairs with no witness below both) and the upper-only graph Lg (no witness
  above both);
- the k-guess algorithm: D_A = Q - up(A + {v}) for |A| <= k ("low" side) or D^B = down(B + {u}) for |B| <= k ("up"
  side); sound for every k;
- generator numbers of a solution down-set D: g_low(D) = number of minimal classes of Q - D other than the class of v
  (0 if Q - D is the class of v), g_up(D) dually;
- globally shortest consistent zigzags: over all down-sets D, BFS paths of G_D of the least length.
Down-sets are bit masks, as in zz.downsets.
"""
import itertools
import random
from collections import deque
import zz


class Info:
    def __init__(self, z):
        self.z = z
        n, le = z.n, z.le
        self.n = n
        self.full = (1 << n) - 1
        self.down = [sum(1 << a for a in range(n) if le[a][b]) for b in range(n)]   # down[b] = {a : a <= b}
        self.up = [sum(1 << b for b in range(n) if le[a][b]) for a in range(n)]     # up[a] = {b : a <= b}
        self.cls = [self.down[x] & self.up[x] for x in range(n)]                     # class of x
        self.adj = z.adj()
        self.ucls = self.cls[z.u]
        self.vcls = self.cls[z.v]

    def incomparable(self, x, y):
        return not self.z.le[x][y] and not self.z.le[y][x]


def witness_kinds(z, I=None):
    """dict {(x, y): set of kinds} over incomparable pairs x < y (indices)."""
    I = I or Info(z)
    lt = z.lt
    out = {}
    for x in range(z.n):
        for y in range(x + 1, z.n):
            if not I.incomparable(x, y):
                continue
            ks = set()
            for w in I.adj[x] & I.adj[y]:
                if lt[w][x] and lt[w][y]:
                    ks.add('B' if (I.ucls >> w) & 1 else 'ML')
                elif lt[x][w] and lt[y][w]:
                    ks.add('T' if (I.vcls >> w) & 1 else 'MU')
            out[(x, y)] = ks
    return out


def has_lower(ks):
    return 'B' in ks or 'ML' in ks


def has_upper(ks):
    return 'T' in ks or 'MU' in ks


def p2_holds(z, I=None):
    return all(has_lower(k) or has_upper(k) for k in witness_kinds(z, I).values())


def cut_path(z, D, adj):
    return zz.zigzag_in(z, D, adj)


def solutions(z, I=None):
    """list of (D, shortest path in G_D) over all down-sets D with a u-v path in G_D."""
    I = I or Info(z)
    out = []
    for D in zz.downsets(z):
        p = zz.zigzag_in(z, D, I.adj)
        if p is not None:
            out.append((D, p))
    return out


def classes_count(I, mask):
    seen = 0
    c = 0
    m = mask
    while m:
        low = m & -m
        x = low.bit_length() - 1
        m ^= low
        if not (seen >> x) & 1:
            seen |= I.cls[x]
            c += 1
    return c


def g_low(I, D):
    comp = I.full & ~D
    if comp == I.vcls:
        return 0
    mins = 0
    m = comp
    while m:
        low = m & -m
        x = low.bit_length() - 1
        m ^= low
        # x minimal in comp iff no element of comp strictly below x
        if (I.down[x] & ~I.cls[x]) & comp == 0:
            mins |= 1 << x
    return classes_count(I, mins)


def g_up(I, D):
    if D == I.ucls:
        return 0
    maxs = 0
    m = D
    while m:
        low = m & -m
        x = low.bit_length() - 1
        m ^= low
        if (I.up[x] & ~I.cls[x]) & D == 0:
            maxs |= 1 << x
    return classes_count(I, maxs)


def candidate_sets(n, k, exclude=()):
    els = [x for x in range(n) if x not in exclude]
    for r in range(k + 1):
        for A in itertools.combinations(els, r):
            yield A


def guess_low(z, k, I=None):
    """some D_A = Q - up(A + {v}) with |A| <= k has a u-v path in G_{D_A}; returns (D, path) or None."""
    I = I or Info(z)
    for A in candidate_sets(z.n, k, exclude=(z.u, z.v)):
        U = I.up[z.v]
        for a in A:
            U |= I.up[a]
        D = I.full & ~U
        if not (D >> z.u) & 1:
            continue
        p = zz.zigzag_in(z, D, I.adj)
        if p is not None:
            return D, p
    return None


def guess_up(z, k, I=None):
    I = I or Info(z)
    for B in candidate_sets(z.n, k, exclude=(z.u, z.v)):
        D = I.down[z.u]
        for b in B:
            D |= I.down[b]
        if (D >> z.v) & 1:
            continue
        p = zz.zigzag_in(z, D, I.adj)
        if p is not None:
            return D, p
    return None


def peaks_valleys(path):
    return path[1::2], path[0::2]


def minimal_peak_classes(I, path):
    """minimal classes among the peaks of `path` that are not equivalent to v."""
    P = [x for x in path[1::2] if not (I.vcls >> x) & 1]
    pm = sum(1 << x for x in P)
    mins = 0
    for x in P:
        if (I.down[x] & ~I.cls[x]) & pm == 0:
            mins |= 1 << x
    return classes_count(I, mins), mins


def maximal_valley_classes(I, path):
    V = [x for x in path[0::2] if not (I.ucls >> x) & 1]
    vm = sum(1 << x for x in V)
    maxs = 0
    for x in V:
        if (I.up[x] & ~I.cls[x]) & vm == 0:
            maxs |= 1 << x
    return classes_count(I, maxs), maxs


def globally_shortest(z, I=None, sols=None):
    """(length, list of (D, path)) of the globally shortest consistent zigzags found by BFS in each G_D."""
    I = I or Info(z)
    if sols is None:
        sols = solutions(z, I)
    if not sols:
        return None, []
    m = min(len(p) for _, p in sols)
    return m - 1, [(D, p) for D, p in sols if len(p) == m]


def lower_only_graph(z, I=None, kinds=None):
    """edges {x, y}: incomparable, no common R-neighbour strictly below both (so P2 needs one above)."""
    kinds = kinds if kinds is not None else witness_kinds(z, I)
    return [e for e, ks in kinds.items() if not has_lower(ks)]


def upper_only_graph(z, I=None, kinds=None):
    kinds = kinds if kinds is not None else witness_kinds(z, I)
    return [e for e, ks in kinds.items() if not has_upper(ks)]


def clique_number(n, edges):
    import networkx as nx
    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from(edges)
    if not edges:
        return 1
    return max(len(c) for c in nx.find_cliques(G))


# ------------------------------------------------------------------------------------------------------------
# random instances
# ------------------------------------------------------------------------------------------------------------

def random_preorder(rng, nb, nm, nt, p_order, p_tie=0.0):
    """elements: 0..nb-1 equivalent to u = 0; middle nb..nb+nm-1; nb+nm..n-1 equivalent to v = n-1.
    Middle: random order on a random linear extension, then random ties (merged pairs)."""
    n = nb + nm + nt
    M = list(range(nb, nb + nm))
    T = list(range(nb + nm, n))
    perm = M[:]
    rng.shuffle(perm)
    le = [[a == b for b in range(n)] for a in range(n)]
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            if rng.random() < p_order:
                le[perm[i]][perm[j]] = True
    for a in M:
        for b in M:
            if a != b and rng.random() < p_tie / max(1, nm):
                le[a][b] = le[b][a] = True
    for b in range(nb):
        for x in range(n):
            le[b][x] = True
    for t in T:
        for x in range(n):
            le[x][t] = True
    for k in range(n):
        for i in range(n):
            if le[i][k]:
                for j in range(n):
                    if le[k][j]:
                        le[i][j] = True
    # u = 0 and v = n-1 must not be equivalent; they cannot be (only middle elements were merged)
    assert not le[n - 1][0]
    return n, le


def p2_complete_dir(rng, z_n, le, R, mode, u, v):
    """add witness edges until every incomparable pair has a witness of the required direction.
    mode 'low': a lower witness for every pair; 'up': an upper witness; 'mixed': any witness, direction random
    per pair; 'lowB' / 'upT': only bottom / top witnesses (Theorem F setting)."""
    n = z_n
    lt = [[le[a][b] and not le[b][a] for b in range(n)] for a in range(n)]
    R = set(R)
    adj = [set() for _ in range(n)]
    for a, b in R:
        adj[a].add(b)
        adj[b].add(a)
    pairs = [(x, y) for x in range(n) for y in range(x + 1, n) if not le[x][y] and not le[y][x]]
    rng.shuffle(pairs)
    for x, y in pairs:
        com = adj[x] & adj[y]
        low_ok = any(lt[w][x] and lt[w][y] for w in com)
        up_ok = any(lt[x][w] and lt[y][w] for w in com)
        if mode == 'low' and low_ok:
            continue
        if mode == 'up' and up_ok:
            continue
        if mode == 'mixed' and (low_ok or up_ok):
            continue
        if mode == 'lowB' and any(lt[w][x] and lt[w][y] and le[w][u] for w in com):
            continue
        if mode == 'upT' and any(lt[x][w] and lt[y][w] and le[v][w] for w in com):
            continue
        lows = [w for w in range(n) if lt[w][x] and lt[w][y]]
        ups = [w for w in range(n) if lt[x][w] and lt[y][w]]
        if mode == 'low':
            cands = lows
        elif mode == 'up':
            cands = ups
        elif mode == 'lowB':
            cands = [w for w in lows if le[w][u]]
        elif mode == 'upT':
            cands = [w for w in ups if le[v][w]]
        else:
            cands = lows if rng.random() < 0.5 else ups
        # prefer middle witnesses half of the time (stress the middle kinds)
        mids = [w for w in cands if not le[w][u] and not le[v][w]]
        if mids and rng.random() < 0.5:
            cands = mids
        w = rng.choice(cands)
        for t in (x, y):
            e = (w, t) if lt[w][t] else (t, w)
            if e != (u, v):
                R.add(e)
                adj[e[0]].add(e[1])
                adj[e[1]].add(e[0])
    return R


def random_instance(rng, mode, nb=None, nm=None, nt=None, p_order=None, p_R=None, p_tie=None):
    nb = nb if nb is not None else rng.randint(1, 3)
    nm = nm if nm is not None else rng.randint(2, 10)
    nt = nt if nt is not None else rng.randint(1, 3)
    p_order = p_order if p_order is not None else rng.choice([0.0, 0.1, 0.25, 0.4])
    p_R = p_R if p_R is not None else rng.choice([0.1, 0.2, 0.35])
    p_tie = p_tie if p_tie is not None else rng.choice([0.0, 0.0, 0.5, 1.0])
    n, le = random_preorder(rng, nb, nm, nt, p_order, p_tie)
    u, v = 0, n - 1
    strict = [(a, b) for a in range(n) for b in range(n) if le[a][b] and not le[b][a] and (a, b) != (u, v)]
    R = {e for e in strict if rng.random() < p_R}
    R = p2_complete_dir(rng, n, le, R, mode, u, v)
    return zz.ZZ(n, None, sorted(R), u, v, le=le)


def to_json(z):
    return {"n": z.n, "u": z.u, "v": z.v, "le": [[int(b) for b in row] for row in z.le], "R": [list(e) for e in z.R]}


def from_json(d):
    le = [[bool(b) for b in row] for row in d["le"]]
    return zz.ZZ(d["n"], None, [tuple(e) for e in d["R"]], d["u"], d["v"], le=le)
