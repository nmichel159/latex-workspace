"""Referee's test of the statements of drafts/core.tex, Sections 3-5, written from the text.

For a pair (u, v) with c(u,v) = 2 and for F' = the union of a family of minimum u-v cuts (the full family gives
the decomposition of the paper; proper sub-families give the coarser decompositions of rem:coarser), the
function check_pair tests, on every u-v path where a statement speaks about paths:

  ORI    lem:orientation (i)-(iii)                 PIE    lem:pieces (i) restricted, (ii), (iii)
  DEG    lem:degrees                               STR1-4 thm:structure (i)-(iv)
  STR5   thm:structure (v)  (full family: must hold; sub-family: failures are only counted)
  CRI    lem:criterion                             CHA    thm:characterization (G-distances), both directions
  CHA+   every walk R_x, p, R_y built in the proof is a separating shortest path (all choices of R_x, R_y)
  LEN    prop:lengths (ii) with i = 1, 1 < i < k, i = k;  LAM  the lambda form of the characterization
  RES    lem:residual (i), (ii)                    ALG    alg:cut-two as printed, when (*) holds
  ALG3   alg:cut-two is right whenever no eligible pair has l >= 3 (referee's strengthening)

Counters of informative events (not failures) are returned as well.
"""

import itertools
import os
import random
import sys
from collections import Counter, deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ref
from ref import E


def sub_families(cuts, rng, cap):
    n = len(cuts)
    fams = []
    if n <= cap:
        for r in range(1, n + 1):
            for c in itertools.combinations(cuts, r):
                fams.append(c)
    else:
        fams.append(tuple(cuts))
        fams.extend((c,) for c in cuts)
        seen = set()
        while len(fams) < (1 << cap):
            k = rng.randint(2, n - 1)
            c = tuple(sorted(rng.sample(range(n), k)))
            if c not in seen:
                seen.add(c)
                fams.append(tuple(cuts[i] for i in c))
    return fams


def residual(adj, p1, p2):
    """Arcs of the digraph D of the text: both arcs for an edge outside p1, p2; the reversed arc otherwise."""
    fwd = set()
    for p in (p1, p2):
        for a, b in zip(p, p[1:]):
            fwd.add((a, b))
    out = {x: set() for x in adj}
    for x in adj:
        for y in adj[x]:
            if (x, y) in fwd:
                continue                     # traversed from x to y: only the arc y -> x
            out[x].add(y)
    return out


def reach(out, s):
    seen = {s}
    q = deque([s])
    while q:
        x = q.popleft()
        for y in out[x]:
            if y not in seen:
                seen.add(y)
                q.append(y)
    return seen


def shortest_paths(adj, s, t):
    d = ref.bfs(adj, s)[t]
    return [p for p in ref.all_simple_paths(adj, s, t, maxlen=d) if len(p) - 1 == d]


def algorithm_as_printed(adj, u, v, D, du, dv, reading):
    """Lines line:loop to line:not-found of alg:cut-two for the decomposition D.

    reading = 'along': a neighbour of x on q is the vertex before or after x on q;
    reading = 'adjacent': any vertex of q adjacent to x in G.
    Returns (value, edge set, saw_l_ge_3, number of candidate paths tested at most per pair)."""
    d = du[v]
    saw3 = False
    maxcand = 0
    for i, S in enumerate(D.squares):
        a, b, c, dd = D.terminals(i)
        for x, al in ((a, b), (b, a)):
            for y, be in ((c, dd), (dd, c)):
                if x == y or al == be:
                    continue
                l = d - du[x] - dv[y]
                if l >= 3:
                    saw3 = True
                cand = []
                if l == 1 and y in adj[x]:
                    cand = [(x, y)]
                elif l == 2:
                    # q: an alpha-beta path of S_i (the BFS path)
                    par = {al: None}
                    qu = deque([al])
                    while qu:
                        z = qu.popleft()
                        for w in sorted(adj[z], key=str):
                            if w in S and w not in par:
                                par[w] = z
                                qu.append(w)
                    q = [be]
                    while par[q[-1]] is not None:
                        q.append(par[q[-1]])
                    q.reverse()
                    ws = []
                    if reading == "along":
                        for z in (x, y):
                            if z in q:
                                j = q.index(z)
                                if j > 0:
                                    ws.append(q[j - 1])
                                if j + 1 < len(q):
                                    ws.append(q[j + 1])
                    else:
                        ws = [w for w in q if w in adj[x] or w in adj[y]]
                    for w in dict.fromkeys(ws):
                        if w != x and w != y and w in S and w in adj[x] and w in adj[y]:
                            cand.append((x, w, y))
                maxcand = max(maxcand, len(cand))
                for p in cand:
                    pe = set(ref.path_edges(p))
                    if be not in ref.bfs(adj, al, pe, allowed=S):
                        # R_x, R_y: BFS-tree paths
                        Rx = shortest_paths(adj, u, x)[0]
                        Ry = shortest_paths(adj, y, v)[0]
                        return d, set(ref.path_edges(Rx)) | pe | set(ref.path_edges(Ry)), saw3, maxcand
    R = shortest_paths(adj, u, v)[0]
    C = set(D.lea[D.squares[0]])
    return d + 1, set(ref.path_edges(R)) | C, saw3, maxcand


def check_pair(adj, u, v, rng, cap=6, path_pairs=2, max_paths=4000):
    """Returns (Counter of checks done, Counter of info events, list of failures)."""
    done, info, fails = Counter(), Counter(), []

    def test(name, cond, detail=None):
        done[name] += 1
        if not cond:
            fails.append((name, detail))

    cuts = ref.min_cuts2(adj, u, v)
    paths = ref.all_simple_paths(adj, u, v)
    if len(paths) > max_paths:
        info["skipped: too many paths"] += 1
        return done, info, fails
    pes = [ref.path_edges(P) for P in paths]
    pset = [set(x) for x in pes]
    du, dv = ref.bfs(adj, u), ref.bfs(adj, v)
    d = du[v]
    alledges = ref.edges_of(adj)
    sep = [not ref.connected(adj, u, v, s) for s in pset]
    cp_is_d = any(sep[i] and len(pes[i]) == d for i in range(len(paths)))

    disjoint = [(i, j) for i in range(len(paths)) for j in range(len(paths)) if i != j and not pset[i] & pset[j]]
    chosen = [disjoint[0]] + (rng.sample(disjoint, min(path_pairs - 1, len(disjoint))) if path_pairs > 1 else [])
    Fall = set().union(*cuts)

    # ORI (i): every minimum cut has one edge on each of p1, p2 -- for all pairs of edge-disjoint paths
    for i, j in disjoint[:200]:
        for C in cuts:
            test("ORI-i", len(C & pset[i]) == 1 and len(C & pset[j]) == 1)
    # ORI (ii): every path has exactly one edge of every minimum cut, before it in A, after it outside
    sides = {C: ref.comp(adj, u, C) for C in cuts}
    for C in cuts:
        A = sides[C]
        test("MINCUT-two-components", len(ref.components(adj, C)) == 2)
        test("MINCUT-delta", ref.delta(adj, A) == set(C))
        for P, pe in zip(paths, pes):
            idx = [k for k, e in enumerate(pe) if e in C]
            ok = len(idx) == 1 and all(x in A for x in P[:idx[0] + 1]) and all(x not in A for x in P[idx[0] + 1:])
            test("ORI-ii", ok)

    # RES: for each chosen pair of paths
    for i, j in chosen:
        p1, p2 = paths[i], paths[j]
        out = residual(adj, p1, p2)
        others = [x for x in adj if x != u and x != v]
        if len(others) <= 12:
            for r in range(len(others) + 1):
                for sub in itertools.combinations(others, r):
                    A = set(sub) | {u}
                    closed = not any(y not in A for x in A for y in out[x])
                    test("RES-i", closed == (frozenset(ref.delta(adj, A)) in set(cuts)) and
                         (not closed or len(ref.delta(adj, A)) == 2), (p1, p2, A))
        rs = {x: reach(out, x) for x in adj}
        for p in (p1, p2):
            for a, b in zip(p, p[1:]):
                same = b in rs[a] and a in rs[b]
                test("RES-ii", (E(a, b) in Fall) == (not same), (p1, p2, a, b))
        scc = {frozenset(y for y in rs[x] if x in rs[y]) for x in adj}
        if scc != set(ref.components(adj, Fall)):
            info["strong components of D differ from the pieces"] += 1

    for fam in sub_families(cuts, rng, cap):
        full = len(fam) == len(cuts)
        for i, j in (chosen if full else chosen[:1]):
            p1, p2 = paths[i], paths[j]
            D = ref.Decomposition(adj, u, v, fam, p1, p2, allcuts=cuts)
            F = D.F
            k = len(D.squares)
            tag = "" if full else "'"
            test("ORI-iii" + tag, not D.tail_conflict)
            # PIE (i) restricted to the minimum cuts contained in F'
            for C in cuts:
                A = sides[C]
                whole = all(P <= A or not (P & A) for P in D.pieces)
                if C <= F:
                    test("PIE-i" + tag, whole)
                elif not whole:
                    info["PIE-i fails for a minimum cut not contained in F' (expected)"] += 1
            for e in F:
                test("PIE-ii" + tag, D.piece_of[D.tail[e]] != D.piece_of[D.head[e]])
            test("PIE-ii-conv" + tag, all((e in F) == (D.piece_of[min(e, key=str)] != D.piece_of[max(e, key=str)])
                                          for e in alledges))
            # DEG
            Pu, Pv = D.piece_of[u], D.piece_of[v]
            test("DEG-i" + tag, Pu != Pv)
            test("DEG-u" + tag, len(D.ent[Pu]) == 0 and len(D.lea[Pu]) == 2)
            test("DEG-v" + tag, len(D.ent[Pv]) == 2 and len(D.lea[Pv]) == 0)
            for P in D.pieces:
                vis = [bool(P & set(p1)), bool(P & set(p2))]
                test("DEG-iii-visited" + tag, any(vis))
                if P not in (Pu, Pv):
                    test("DEG-count" + tag, len(D.ent[P]) == sum(vis) == len(D.lea[P]))
                    test("DEG-link" + tag, D.is_square[P] == all(vis))
                for q, qe in ((p1, set(pes[i])), (p2, set(pes[j]))):
                    n_in = sum(1 for e in D.ent[P] if e in qe)
                    n_out = sum(1 for e in D.lea[P] if e in qe)
                    visits = bool(P & set(q))
                    test("DEG-ii" + tag, n_in == (1 if visits and u not in P else 0) and
                         n_out == (1 if visits and v not in P else 0))
            test("STR-k>=2" + tag, k >= 2 and u in D.squares[0] and v in D.squares[-1])
            # STR (i)
            for idx, S in enumerate(D.squares):
                if idx >= 1:
                    test("STR1-enter" + tag, frozenset(D.ent[S]) in set(cuts) and len(D.ent[S]) == 2)
                if idx < k - 1:
                    test("STR1-leave" + tag, frozenset(D.lea[S]) in set(cuts) and len(D.lea[S]) == 2)
            # STR (iii)
            gp = {}
            ok3 = True
            for idx in range(k - 1):
                S = D.squares[idx]
                for jj, qe in ((1, set(pes[i])), (2, set(pes[j]))):
                    first = [e for e in D.lea[S] if e in qe]
                    if len(first) != 1:
                        ok3 = False
                        continue
                    es_, ls_, end = D.general_path(first[0])
                    if end != D.squares[idx + 1] or not set(es_) <= qe:
                        ok3 = False
                    gp[(idx, jj)] = (es_, ls_)
            alle = [e for g in gp.values() for e in g[0]]
            alll = [L for g in gp.values() for L in g[1]]
            test("STR3" + tag, ok3 and Counter(alle) == Counter(F) and Counter(alll) == Counter(D.links))
            # terminals
            T = [D.terminals(idx) for idx in range(k)]
            for idx in range(k):
                a, b, c, dd = T[idx]
                for s, t in itertools.combinations(sorted(set((a, b, c, dd)), key=str), 2):
                    good = ref.cutvalue(adj, s, t, limit=3) >= 3
                    if full:
                        test("STR5", good, (s, t))
                    elif not good:
                        info["STR5 fails for a coarser decomposition (expected)"] += 1

            # statements about all u-v paths
            for P, pe, ps, issep in zip(paths, pes, pset, sep):
                pos = {x: n for n, x in enumerate(P)}
                # PIE (iii) and ORI (iii)
                okp = True
                for X in D.pieces:
                    idxs = sorted(pos[x] for x in X if x in pos)
                    if not idxs:
                        continue
                    if idxs != list(range(idxs[0], idxs[-1] + 1)):
                        okp = False
                        continue
                    cnt = sum(1 for e in pe if e in F and (e & X))
                    want = (0 if u in X else 1) + (0 if v in X else 1)
                    if cnt != want:
                        okp = False
                    if u not in X:
                        e = pe[idxs[0] - 1]
                        if not (e in F and D.head[e] == P[idxs[0]]):
                            okp = False
                    if v not in X:
                        e = pe[idxs[-1]]
                        if not (e in F and D.tail[e] == P[idxs[-1]]):
                            okp = False
                test("PIE-iii" + tag, okp)
                test("ORI-iii-direction" + tag, all(D.tail[e] == P[n] for n, e in enumerate(pe) if e in F))
                # STR (ii)
                order = []
                for x in P:
                    X = D.piece_of[x]
                    if D.is_square[X] and X not in order:
                        order.append(X)
                test("STR2" + tag, order == D.squares)
                # STR (iv)
                ok4 = True
                visited_links = {D.piece_of[x] for x in P if not D.is_square[D.piece_of[x]]}
                for idx in range(k - 1):
                    st = []
                    for jj in (1, 2):
                        es_, ls_ = gp.get((idx, jj), ([], []))
                        alle_ = all(e in ps for e in es_) and all(L in visited_links for L in ls_)
                        none_ = not any(e in ps for e in es_) and not any(L in visited_links for L in ls_)
                        st.append((alle_, none_))
                    if not ((st[0][0] and st[1][1]) or (st[1][0] and st[0][1])):
                        ok4 = False
                test("STR4" + tag, ok4)
                # CRI
                allsame = True
                for idx, S in enumerate(D.squares):
                    a, b, c, dd = T[idx]
                    if idx == 0:
                        al = u
                    else:
                        used = [e for e in D.ent[S] if e in ps]
                        other = [e for e in D.ent[S] if e not in ps]
                        if len(used) != 1 or len(other) != 1:
                            allsame = None
                            break
                        al = D.head[other[0]]
                    if idx == k - 1:
                        be = v
                    else:
                        used = [e for e in D.lea[S] if e in ps]
                        other = [e for e in D.lea[S] if e not in ps]
                        if len(used) != 1 or len(other) != 1:
                            allsame = None
                            break
                        be = D.tail[other[0]]
                    if be not in ref.bfs(adj, al, ps, allowed=S):
                        allsame = False
                test("CRI" + tag, allsame is not None and (not issep) == allsame)

            # CHA: witnesses with G-distances
            found = False
            for idx, S in enumerate(D.squares):
                a, b, c, dd = T[idx]
                for x, al in dict.fromkeys(((a, b), (b, a))):
                    for y, be in dict.fromkeys(((c, dd), (dd, c))):
                        for p in ref.all_simple_paths(adj, x, y, allowed=S):
                            if du[x] + len(p) - 1 + dv[y] != d:
                                continue
                            ppe = set(ref.path_edges(p))
                            if be in ref.bfs(adj, al, ppe, allowed=S):
                                continue
                            found = True
                            test("CHA-p-has-an-edge" + tag, len(p) >= 2)
                            # the proof: every choice of R_x, R_y gives a separating shortest path
                            for Rx in shortest_paths(adj, u, x):
                                for Ry in shortest_paths(adj, y, v):
                                    R = Rx + p[1:] + Ry[1:]
                                    okR = len(set(R)) == len(R) and len(R) - 1 == d and \
                                        not ref.connected(adj, u, v, set(ref.path_edges(R)))
                                    test("CHA+" + tag, okR, (fam, x, al, y, be, p, R))
                                    trace = tuple(z for z in R if z in S)
                                    if trace != p:
                                        info["witness p is a proper part of the trace of R" + tag] += 1
                                        if trace[0] != x:
                                            info["... and R enters the square at alpha" + tag] += 1
                            if all(tuple(z for z in R if z in S) != p for R in shortest_paths(adj, u, v)
                                   if set(p) <= set(R)):
                                info["witness p is the trace of NO shortest u-v path" + tag] += 1
            test("CHA" + tag, found == cp_is_d, (fam, found, cp_is_d))

            # LEN and LAM (directed distances)
            def darcs(x):
                for y in adj[x]:
                    e = E(x, y)
                    if e in F and D.tail[e] != x:
                        continue
                    yield y
            outd = {x: set(darcs(x)) for x in adj}
            ind = {x: set() for x in adj}
            for x in adj:
                for y in outd[x]:
                    ind[y].add(x)

            def ddist(nb, s):
                dist = {s: 0}
                q = deque([s])
                while q:
                    z = q.popleft()
                    for w in nb[z]:
                        if w not in dist:
                            dist[w] = dist[z] + 1
                            q.append(w)
                return dist
            fromu, tov = ddist(outd, u), ddist(ind, v)
            test("LEN-i" + tag, all(all(D.tail[e] == P[n] for n, e in enumerate(pe) if e in F) for P, pe in zip(paths, pes)))
            foundlam = False
            for idx, S in enumerate(D.squares):
                ents = D.ent[S] if idx > 0 else [None]
                leas = D.lea[S] if idx < k - 1 else [None]
                for g in ents:
                    for h in leas:
                        x = u if g is None else D.head[g]
                        y = v if h is None else D.tail[h]
                        og = [e for e in ents if e != g]
                        oh = [e for e in leas if e != h]
                        al = u if g is None else D.head[og[0]]
                        be = v if h is None else D.tail[oh[0]]
                        for p in ref.all_simple_paths(adj, x, y, allowed=S):
                            formula = len(p) - 1
                            formula += 0 if g is None else fromu.get(D.tail[g], 10 ** 6) + 1
                            formula += 0 if h is None else tov.get(D.head[h], 10 ** 6) + 1
                            best = None
                            for P, ps in zip(paths, pset):
                                if (g is None or g in ps) and (h is None or h in ps) and \
                                        tuple(z for z in P if z in S) == p:
                                    if best is None or len(P) - 1 < best:
                                        best = len(P) - 1
                            test("LEN-ii" + tag, best == formula, (idx, g, h, p, best, formula))
                            if formula == d and be not in ref.bfs(adj, al, set(ref.path_edges(p)), allowed=S):
                                foundlam = True
            test("LAM" + tag, foundlam == cp_is_d)

            # ALG as printed
            star = all(ref.bfs(adj, x)[y] <= 2 for idx in range(k) for x in T[idx][:2] for y in T[idx][2:])
            for reading in ("along", "adjacent"):
                val, S_, saw3, maxcand = algorithm_as_printed(adj, u, v, D, du, dv, reading)
                truth = d if cp_is_d else d + 1
                is_cp = (not ref.connected(adj, u, v, S_)) and \
                    ref.connected({x: {y for y in adj[x] if E(x, y) in S_} for x in adj}, u, v)
                test("ALG-returns-a-cut-path" + tag + "-" + reading, is_cp and len(S_) == val, (val, S_))
                if star:
                    test("ALG-star" + tag + "-" + reading, val == truth)
                if not saw3:
                    test("ALG3" + tag + "-" + reading, val == truth)
                elif val != truth:
                    info["ALG wrong when some l >= 3 (outside the class)" + tag] += 1
                if reading == "along":
                    test("ALG-at-most-4-candidates" + tag, maxcand <= 4)
                elif maxcand > 4:
                    info["reading 'adjacent': more than 4 candidates" + tag] += 1
                if saw3:
                    info["some eligible pair has l >= 3" + tag] += 1
    return done, info, fails


def merge(tot, part):
    for a, b in zip(tot, part):
        if isinstance(a, list):
            a.extend(b[:20])
        else:
            a.update(b)
