"""Certificate search of Theorem H (dc-hardness.md Section 5) generalised to guessed side sets, for 2CH with classes.

Sides: (switch w, type 0 = E / 1 = F, node mask), non-empty only.  Groups g = (type, parity of the position).
A certificate assigns to every group g a set K_g of sides of the other type (or None = no condition).
Search: walks X_1, X_2, ... of sides (consecutive ones meet), X_1 contains s, the last contains t; positions start at 1.
  (i)      the partner of X (the other side of its switch) is empty or lies in K_g, g = group of X;
  (i-tie)  [ties=True] every non-empty side of the other type of every member of the class of X lies in K_g;
  storage  X is stored if it lies in some K_g; at most `cap` stored sides per K_g; no two stored sides of one class
           with different types (one switch, if ties=False).
Soundness (any family of sets): a conflict X_b = partner(X_a) (or, with ties=True, X_a, X_b of one class and different
types) puts X_b into K_{g(a)} and X_a into K_{g(b)}, so both are stored and the walk is rejected.  So a 'yes' always
comes with a consistent walk.  Completeness depends on the family (Theorem H: node stars; here also maximal cliques).

Families:
  'node'    K(phi) = sides of the required type containing node phi (Theorem H with t = 1)
  'clique'  maximal cliques of the intersection graph of the sides of one type (networkx.find_cliques)
"""
import itertools
from collections import deque
import networkx as nx


def sides_of(inst):
    N, E, F, cls, s, t = inst
    S = []
    for w in range(len(E)):
        if E[w]:
            S.append((w, 0, E[w]))
        if F[w]:
            S.append((w, 1, F[w]))
    return S


def family(inst, kind):
    """dict type -> list of frozensets of side indices (sides of that type)."""
    S = sides_of(inst)
    N = inst[0]
    out = {0: [], 1: []}
    if kind == "node":
        for typ in (0, 1):
            seen = set()
            for x in range(N):
                K = frozenset(i for i, (w, T, m) in enumerate(S) if T == typ and (m >> x) & 1)
                if K and K not in seen:
                    seen.add(K)
                    out[typ].append(K)
    elif kind == "clique":
        for typ in (0, 1):
            idx = [i for i, (w, T, m) in enumerate(S) if T == typ]
            G = nx.Graph()
            G.add_nodes_from(idx)
            for a, b in itertools.combinations(idx, 2):
                if S[a][2] & S[b][2]:
                    G.add_edge(a, b)
            out[typ] = [frozenset(c) for c in nx.find_cliques(G)]
    else:
        raise ValueError(kind)
    return out


def search(inst, K, ties=True, cap=2):
    """K: dict group (type, parity) -> frozenset of side indices or None.  Returns a walk (list of side indices) or None."""
    N, E, F, cls, s, t = inst
    S = sides_of(inst)
    side_index = {(w, T): i for i, (w, T, m) in enumerate(S)}
    groups = [(0, 0), (0, 1), (1, 0), (1, 1)]
    inK = [[g for g in groups if K.get(g) is not None and i in K[g]] for i in range(len(S))]
    # partner-type sides that condition (i) / (i-tie) requires to lie in K_g
    req = []
    for i, (w, T, m) in enumerate(S):
        if ties:
            mates = [x for x in range(len(E)) if cls[x] == cls[w]]
        else:
            mates = [w]
        r = [side_index[(x, 1 - T)] for x in mates if (x, 1 - T) in side_index]
        req.append(r)

    def ok(i, par):
        g = (S[i][1], par)
        r = req[i]
        if not r:
            return True
        Kg = K.get(g)
        if Kg is None:
            return False
        return all(j in Kg for j in r)

    def add(i, stored):
        if not inK[i]:
            return stored
        if i in stored:
            return stored
        w, T, m = S[i]
        for k in stored:
            w2, T2, m2 = S[k]
            same = (cls[w2] == cls[w]) if ties else (w2 == w)
            if same and T2 != T:
                return None
        new = stored | {i}
        for g in inK[i]:
            if sum(1 for k in new if g in inK[k]) > cap:
                return None
        return new

    seen = set()
    dq = deque()
    par0 = 1
    for i, (w, T, m) in enumerate(S):
        if (m >> s) & 1 and ok(i, par0):
            st0 = add(i, frozenset())
            if st0 is None:
                continue
            st = (i, par0, st0)
            if st not in seen:
                seen.add(st)
                dq.append((st, None))
    parent = {}
    while dq:
        st, prev = dq.popleft()
        i, par, stored = st
        if (S[i][2] >> t) & 1:
            walk = [i]
            cur = st
            while cur in parent:
                cur = parent[cur]
                walk.append(cur[0])
            return walk[::-1]
        npar = 1 - par
        for j in range(len(S)):
            if not (S[i][2] & S[j][2]):
                continue
            if not ok(j, npar):
                continue
            st2 = add(j, stored)
            if st2 is None:
                continue
            nst = (j, npar, st2)
            if nst in seen:
                continue
            seen.add(nst)
            parent[nst] = st
            dq.append((nst, st))
    return None


def solve(inst, kind="clique", ties=True, cap=2, fam=None):
    """Try every certificate from the family (each group: a set of the partner type, or None)."""
    if fam is None:
        fam = family(inst, kind)
    groups = [(0, 0), (0, 1), (1, 0), (1, 1)]
    options = {g: [None] + fam[1 - g[0]] for g in groups}
    for combo in itertools.product(*(options[g] for g in groups)):
        K = dict(zip(groups, combo))
        w = search(inst, K, ties=ties, cap=cap)
        if w is not None:
            return w, K
    return None, None


def search_union(inst, sets, ties=True, cap=2):
    """Union form: `sets` is a list of side sets U_1..U_q (any types); U = their union.
    (i')  every non-empty side of the other type of every member of the class of X (of X's switch, if ties=False)
          lies in U;
    storage: X is stored if it lies in U; at most `cap` stored sides per U_j; no two stored sides of one class
          (switch) with different types.
    Sound for any sets (a conflicting pair is stored on both sides); complete when the partner sides of the classes
    used by some shortest consistent walk are covered by q sets each containing at most `cap` sides of that walk."""
    N, E, F, cls, s, t = inst
    S = sides_of(inst)
    side_index = {(w, T): i for i, (w, T, m) in enumerate(S)}
    U = set()
    for K in sets:
        U |= set(K)
    inK = [[j for j, K in enumerate(sets) if i in K] for i in range(len(S))]
    okside = []
    for i, (w, T, m) in enumerate(S):
        mates = [x for x in range(len(E)) if cls[x] == cls[w]] if ties else [w]
        okside.append(all(side_index[(x, 1 - T)] in U for x in mates if (x, 1 - T) in side_index))

    def add(i, stored):
        if not inK[i] or i in stored:
            return stored
        w, T, m = S[i]
        for k in stored:
            w2, T2, m2 = S[k]
            same = (cls[w2] == cls[w]) if ties else (w2 == w)
            if same and T2 != T:
                return None
        new = stored | {i}
        for j in inK[i]:
            if sum(1 for k in new if j in inK[k]) > cap:
                return None
        return new

    seen = set()
    dq = deque()
    parent = {}
    for i, (w, T, m) in enumerate(S):
        if (m >> s) & 1 and okside[i]:
            st0 = add(i, frozenset())
            if st0 is None:
                continue
            st = (i, st0)
            if st not in seen:
                seen.add(st)
                dq.append(st)
    while dq:
        st = dq.popleft()
        i, stored = st
        if (S[i][2] >> t) & 1:
            walk = [i]
            cur = st
            while cur in parent:
                cur = parent[cur]
                walk.append(cur[0])
            return walk[::-1]
        for j in range(len(S)):
            if not (S[i][2] & S[j][2]) or not okside[j]:
                continue
            st2 = add(j, stored)
            if st2 is None:
                continue
            nst = (j, st2)
            if nst in seen:
                continue
            seen.add(nst)
            parent[nst] = st
            dq.append(nst)
    return None


def solve_union(inst, kind="clique", q=4, ties=True, cap=2, fam=None):
    if fam is None:
        fam = family(inst, kind)
    allsets = fam[0] + fam[1]
    for r in range(q + 1):
        for combo in itertools.combinations(allsets, r):
            w = search_union(inst, list(combo), ties=ties, cap=cap)
            if w is not None:
                return w, combo
    return None, None


def walk_consistent(inst, walk, ties=True):
    """Check a walk of side indices: consecutive meet, s in first, t in last, no class (switch) used in both modes."""
    N, E, F, cls, s, t = inst
    S = sides_of(inst)
    if not walk or not (S[walk[0]][2] >> s) & 1 or not (S[walk[-1]][2] >> t) & 1:
        return False
    for a, b in zip(walk, walk[1:]):
        if not (S[a][2] & S[b][2]):
            return False
    mode = {}
    for i in walk:
        w, T, m = S[i]
        key = cls[w] if ties else w
        if mode.setdefault(key, T) != T:
            return False
    return True
