"""Monotone closure on the double cover.

A state is (AL, AH): AL = elements still allowed as lows, AH = elements still allowed as highs.  The double cover has the nodes 2x (x low, x in AL) and 2x+1 (x high, x in AH) and the
edges (a low)-(b high) for ab in R.  A valid walk that is shortest for its own label set never repeats a node, so it is a simple path from s = 2u to t = 2v+1 of the double cover.

closure(): repeat until stable
  * block-cut tree of the component of s; if t is not there: refuted;
  * nodes outside the blocks of the s-t chain are killed;
  * a node that is forced (s, t, a cut vertex of the chain, an assumed node) kills its conflict partners:
    x low kills the highs y <= x, x high kills the lows y >= x;
  * an assumed node that was killed: refuted.
sac(): singleton consistency.  For every alive node with an alive conflict partner, closure with this node assumed; refuted nodes are killed.
"""
import sys

from wd import bits

sys.setrecursionlimit(10000)


class Refuted(Exception):
    pass


class Graph:
    def __init__(self, I):
        self.I = I
        self.s = 2 * I.u
        self.t = 2 * I.v + 1
        self.up = I.UP
        self.dn = I.DN
        self.nbr = [None] * (2 * I.m)
        for x in range(I.m):
            self.nbr[2 * x] = [2 * y + 1 for y in bits(I.HI[x])]
            self.nbr[2 * x + 1] = [2 * y for y in bits(I.LO[x])]

    def chain(self, AL, AH):
        """Block-cut chain from s to t.  Returns (relevant nodes as AL', AH', list of forced nodes) or None if t is not reached."""
        s, t = self.s, self.t
        nbr = self.nbr
        n = len(nbr)
        alive = [False] * n
        x = AL
        while x:
            b = x & -x
            alive[2 * (b.bit_length() - 1)] = True
            x ^= b
        x = AH
        while x:
            b = x & -x
            alive[2 * (b.bit_length() - 1) + 1] = True
            x ^= b
        if not alive[s] or not alive[t]:
            return None
        num = [0] * n
        low = [0] * n
        owner = [-1] * n    # index of the block in which the node is not the root
        blocks = []         # (root, nodes)
        cnt = 1
        num[s] = low[s] = 1
        vst = []
        st = [(s, -1, 0)]
        stack_it = [0] * n
        path = [s]
        parent = [-1] * n
        while path:
            x = path[-1]
            nb = nbr[x]
            i = stack_it[x]
            adv = False
            while i < len(nb):
                y = nb[i]
                i += 1
                if not alive[y]:
                    continue
                if num[y] == 0:
                    cnt += 1
                    num[y] = low[y] = cnt
                    parent[y] = x
                    stack_it[x] = i
                    path.append(y)
                    vst.append(y)
                    adv = True
                    break
                elif y != parent[x] and num[y] < low[x]:
                    low[x] = num[y]
            if adv:
                continue
            stack_it[x] = i
            path.pop()
            p = parent[x]
            if p >= 0:
                if low[x] < low[p]:
                    low[p] = low[x]
                if low[x] >= num[p]:
                    # block with root p
                    b = []
                    while True:
                        w = vst.pop()
                        b.append(w)
                        owner[w] = len(blocks)
                        if w == x:
                            break
                    blocks.append((p, b))
        if num[t] == 0:
            return None
        relL = 0
        relH = 0
        forced = []
        v = t
        while v != s:
            root, b = blocks[owner[v]]
            for w in b:
                if w & 1:
                    relH |= 1 << (w >> 1)
                else:
                    relL |= 1 << (w >> 1)
            forced.append(v)
            v = root
        forced.append(s)
        relL |= 1 << (s >> 1)
        return relL, relH, forced


def closure(G, AL, AH, assume=()):
    """Returns (AL, AH, forced nodes) or raises Refuted."""
    I = G.I
    UP, DN = I.UP, I.DN
    while True:
        r = G.chain(AL, AH)
        if r is None:
            raise Refuted()
        AL2, AH2, forced = r
        fs = list(forced) + list(assume)
        for n in fs:
            x = n >> 1
            if n & 1:
                if not AH2 >> x & 1:
                    raise Refuted()
                AL2 &= ~UP[x]
            else:
                if not AL2 >> x & 1:
                    raise Refuted()
                AH2 &= ~DN[x]
        if AL2 == AL and AH2 == AH:
            return AL, AH, forced
        AL, AH = AL2, AH2


def alive_conflicts(I, AL, AH):
    """Nodes with an alive conflict partner, as a list of node numbers."""
    out = []
    for x in bits(AL):
        if I.DN[x] & AH:
            out.append(2 * x)
    for x in bits(AH):
        if I.UP[x] & AL:
            out.append(2 * x + 1)
    return out


def sac(G, AL, AH, stats=None):
    """Singleton consistency.  Returns (AL, AH) or raises Refuted."""
    I = G.I
    AL, AH, _ = closure(G, AL, AH)
    changed = True
    while changed:
        changed = False
        for n in alive_conflicts(I, AL, AH):
            x = n >> 1
            if n & 1:
                if not AH >> x & 1:
                    continue
            else:
                if not AL >> x & 1:
                    continue
            try:
                closure(G, AL, AH, (n,))
                if stats is not None:
                    stats["probes"] += 1
            except Refuted:
                if stats is not None:
                    stats["kills"] += 1
                if n & 1:
                    AH &= ~(1 << x)
                else:
                    AL &= ~(1 << x)
                AL, AH, _ = closure(G, AL, AH)
                changed = True
    return AL, AH


def bfs_walk(G, AL, AH):
    """A shortest s-t path in the alive double cover, as a list of elements (u first), or None."""
    s, t = G.s, G.t
    par = {s: None}
    cur = [s]
    I = G.I
    while cur:
        nxt = []
        for n in cur:
            x = n >> 1
            if n == t:
                out = []
                while n is not None:
                    out.append(n >> 1)
                    n = par[n]
                return out[::-1]
            if n & 1:
                for y in bits(I.LO[x] & AL):
                    m = 2 * y
                    if m not in par:
                        par[m] = n
                        nxt.append(m)
            else:
                for y in bits(I.HI[x] & AH):
                    m = 2 * y + 1
                    if m not in par:
                        par[m] = n
                        nxt.append(m)
        cur = nxt
    return None


def exact_alive(I, AL, AH, budget=None):
    """Exact: a shortest valid walk with lows in AL and highs in AH, or None.  Same method as Inst.shortest_walk, with masks."""
    from wd import Budget
    if not AL >> I.u & 1 or not AH >> I.v & 1:
        return None
    states = []
    seen = {}
    layer = []

    def push(st, U, Dn, par):
        lst = seen.setdefault(st, [])
        for (u0, d0) in lst:
            if u0 & ~U == 0 and d0 & ~Dn == 0:
                return
        lst[:] = [(u0, d0) for (u0, d0) in lst if not (U & ~u0 == 0 and Dn & ~d0 == 0)]
        lst.append((U, Dn))
        states.append((st, U, Dn, par))
        layer.append(len(states) - 1)

    push(2 * I.u, 0, I.DN[I.u], None)
    target = 2 * I.v + 1
    while layer:
        for i in layer:
            if states[i][0] == target:
                out = []
                j = i
                while j is not None:
                    out.append(states[j][0] >> 1)
                    j = states[j][3]
                return out[::-1]
        cur = layer
        layer = []
        for i in cur:
            st, U, Dn, _ = states[i]
            x, hi = st >> 1, st & 1
            if hi:
                for y in bits(I.LO[x] & AL & ~U):
                    push(2 * y, U, Dn | I.DN[y], i)
            else:
                for y in bits(I.HI[x] & AH & ~Dn):
                    push(2 * y + 1, U | I.UP[y], Dn, i)
            if budget is not None and len(states) > budget:
                raise Budget()
    return None


def is_valid(I, w):
    return I.is_valid_walk(w)


def solve(G, stats, AL=None, AH=None, depth=0, level=1):
    """Search: closure or sac, a BFS walk; when it has a conflict h <= l, branch on killing h as a high or l as a low.  Returns a valid walk or None.
    stats counts the nodes, the branches and the deep failures (subtrees that passed the consistency test and still contain no solution)."""
    I = G.I
    if AL is None:
        AL, AH = I.ALL, I.ALL
    stats["nodes"] += 1
    stats["maxdepth"] = max(stats["maxdepth"], depth)
    try:
        if level == 0:
            AL, AH, _ = closure(G, AL, AH)
        else:
            AL, AH = sac(G, AL, AH, stats)
    except Refuted:
        stats["refuted"] += 1
        return None
    w = bfs_walk(G, AL, AH)
    assert w is not None
    n = len(w)
    cf = None
    for i in range(1, n, 2):
        for j in range(0, n, 2):
            if I.leq(w[i], w[j]):
                cf = (w[i], w[j])
                break
        if cf:
            break
    if cf is None:
        return w
    stats["branches"] += 1
    h, l = cf
    r = solve(G, stats, AL, AH & ~(1 << h), depth + 1, level)
    if r is not None:
        return r
    r = solve(G, stats, AL & ~(1 << l), AH, depth + 1, level)
    if r is None:
        stats["deep-failures"] += 1
    return r
