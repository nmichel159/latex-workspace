"""Random ZZ instances (with or without P2) and the flow-based pipeline G -> H -> ZZ for large graphs."""
import random
from eqcore import (Small, Flow, adj_masks, all_dist, bit_list, bridges, component, build_H, H_weights,
                    preorder_from_cuts, leq, lt, is_downset, check_P2, zz_dfs, zz_downsets, popcount)


def random_preorder(q, rng, p_rel=None, p_eq=0.15):
    """Elements 0..q-1, u = 0 least, v = q-1 greatest. Returns down masks."""
    if p_rel is None:
        p_rel = rng.choice([0.15, 0.3, 0.45, 0.6])
    # classes: 0 = class of u, K-1 = class of v, others middle
    K = rng.randint(2, q)
    cls = [0] * q
    cls[0] = 0
    cls[q - 1] = K - 1
    mids = list(range(1, K - 1))
    for x in range(1, q - 1):
        if mids and rng.random() > p_eq:
            cls[x] = rng.choice(mids)
        else:
            cls[x] = rng.choice([0, K - 1] + mids) if mids else rng.choice([0, K - 1])
    # random DAG on classes, ordered by index; 0 below all, K-1 above all
    below = [set([i]) for i in range(K)]  # below[j] = classes <= j
    for j in range(K):
        for i in range(j):
            if i == 0 or j == K - 1 or rng.random() < p_rel:
                below[j] |= below[i]
    # transitive closure (indices increase)
    for j in range(K):
        acc = set(below[j])
        for i in list(below[j]):
            acc |= below[i]
        below[j] = acc
    down = [0] * q
    for y in range(q):
        for x in range(q):
            if cls[x] in below[cls[y]]:
                down[y] |= 1 << x
    return down


def strict_pairs(q, down):
    return [(a, b) for a in range(q) for b in range(q) if a != b and lt(down, a, b)]


def random_R(q, down, rng, p_r=None, u=None, v=None):
    if p_r is None:
        p_r = rng.choice([0.2, 0.35, 0.5, 0.7])
    u = 0 if u is None else u
    v = q - 1 if v is None else v
    R = set()
    for a, b in strict_pairs(q, down):
        if {a, b} == {u, v}:
            continue
        if rng.random() < p_r:
            R.add((min(a, b), max(a, b)))
    return R


def enforce_P2(q, down, R, rng, u=0, v=None, avoid_uv=0.85):
    v = q - 1 if v is None else v
    Radj = adj_masks(q, R)
    for x in range(q):
        for y in range(x + 1, q):
            if leq(down, x, y) or leq(down, y, x):
                continue
            ok = any((leq(down, x, z) and leq(down, y, z)) or (leq(down, z, x) and leq(down, z, y))
                     for z in bit_list(Radj[x] & Radj[y]))
            if ok:
                continue
            cand = [z for z in range(q) if z not in (x, y) and
                    ((lt(down, x, z) and lt(down, y, z)) or (lt(down, z, x) and lt(down, z, y)))]
            inner = [z for z in cand if z not in (u, v)]
            z = rng.choice(inner) if inner and rng.random() < avoid_uv else rng.choice(cand)
            for w in (x, y):
                e = (min(w, z), max(w, z))
                if e not in R:
                    R.add(e)
                    Radj[w] |= 1 << z
                    Radj[z] |= 1 << w
    return R


def zz_answer(q, down, R, u=0, v=None):
    v = q - 1 if v is None else v
    Radj = adj_masks(q, R)
    a1, path = zz_dfs(q, down, Radj, u, v)
    a2, D = zz_downsets(q, down, Radj, u, v)
    assert a1 == a2, "zz solvers disagree"
    return a1, path


def pipeline_flow(n, edges, u, v, qmax=20):
    """G (any size, simple) -> K (Lemma 1) -> Q(u) by flows -> ears -> H -> preorder by enumeration of the
    subsets of Q -> ZZ instance. Returns dict or None if q too large."""
    br = set(bridges(n, edges))
    rest = [e for e in edges if e not in br]
    adj = adj_masks(n, rest)
    Kmask = component(adj, u)
    assert (Kmask >> v) & 1
    K = bit_list(Kmask)
    idx = {x: i for i, x in enumerate(K)}
    Ke = [(idx[a], idx[b]) for a, b in rest if a in idx and b in idx]
    k = len(K)
    F = Flow(k, Ke)
    adjK = adj_masks(k, Ke)
    cu = {}

    def conn_u(x):
        if x not in cu:
            cu[x] = F.conn(idx[u], x, cap=3)
        return cu[x]

    H = build_H(k, Ke, adjK, idx[u], conn_u)
    Q = H["Q"]
    q = len(Q)
    if q > qmax:
        return None
    W = H_weights(q, H["real"], H["earE"])
    smH = Small(q, [(a, b, w) for (a, b), w in W.items()])
    qi = H["qi"]
    cH, cutsH = smH.min_cuts(qi[idx[u]], qi[idx[v]])
    down = preorder_from_cuts(q, cutsH)
    R = [(a, b) for a, b in H["real"] if not (leq(down, a, b) and leq(down, b, a))]
    Radj = adj_masks(q, R)
    a1, path = zz_dfs(q, down, Radj, qi[idx[u]], qi[idx[v]])
    a2, _ = zz_downsets(q, down, Radj, qi[idx[u]], qi[idx[v]])
    return dict(Q=[K[x] for x in Q], q=q, cH=cH, down=down, R=R, ans=a1, ans2=a2, bad=H["bad"],
                ears=H["ears"], P2fail=check_P2(q, down, Radj), mincuts=len(cutsH))
