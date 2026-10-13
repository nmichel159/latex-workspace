"""Construction of Section 2.1 of theory-hardness.md, re-implemented from the text only.

A formula is a list of clauses; a clause is a non-empty list of non-zero integers
(+i = literal x_i, -i = literal not x_i), repetitions allowed.

Vertex names (strings):
  KA:  'h0'..'hm', 'a1', 'a2', 'fA0', ... (fillers)       u = 'h0'
  KB:  'B0'..'Bm' (beta), 'b1', 'b2', 'fB0', ...           v = 'B<m>'
  occurrence vertices: 'o<k>_<j>' for the j-th literal (j = 1..) of clause C_k (k = 1..m)
"""
import itertools
import networkx as nx


def params(phi):
    m = len(phi)
    L = sum(len(C) for C in phi)
    c0 = (m + 1) + 2 * L
    M = c0 + 2
    return m, L, c0, M


def build(phi, sync_order=None):
    """Return (G, u, v, info). sync_order: optional dict var -> list of occurrence names (path order)."""
    m, L, c0, M = params(phi)
    assert m >= 1 and all(len(C) >= 1 for C in phi)
    G = nx.Graph()
    KA = [f'h{k}' for k in range(m + 1)] + ['a1', 'a2']
    nfill = M - len(KA)
    assert nfill == 2 * L, (nfill, L)
    KA += [f'fA{i}' for i in range(nfill)]
    KB = [f'B{k}' for k in range(m + 1)] + ['b1', 'b2'] + [f'fB{i}' for i in range(nfill)]
    assert len(KA) == M and len(KB) == M
    G.add_nodes_from(KA)
    G.add_nodes_from(KB)
    G.add_edges_from(itertools.combinations(KA, 2))
    G.add_edges_from(itertools.combinations(KB, 2))
    F = [(f'h{k}', f'B{k}') for k in range(m + 1)]
    G.add_edges_from(F)
    occ = {}            # name -> (k, literal)
    O = {}              # var -> list of occurrence names
    for k, C in enumerate(phi, start=1):
        for j, lit in enumerate(C, start=1):
            o = f'o{k}_{j}'
            occ[o] = (k, lit)
            O.setdefault(abs(lit), []).append(o)
            G.add_node(o)
            if lit > 0:
                G.add_edges_from([(o, f'B{k-1}'), (o, f'B{k}'), (o, 'a1'), (o, 'a2')])
            else:
                G.add_edges_from([(o, f'h{k-1}'), (o, f'h{k}'), (o, 'b1'), (o, 'b2')])
    sync = []
    for i, lst in O.items():
        order = sync_order[i] if sync_order and i in sync_order else lst
        for x, y in zip(order, order[1:]):
            sync.append((x, y))
    G.add_edges_from(sync)
    u, v = 'h0', f'B{m}'
    # sanity on the counts stated in the text
    assert G.number_of_nodes() == 2 * M + L
    assert G.number_of_edges() == M * (M - 1) + (m + 1) + 4 * L + sum(len(l) - 1 for l in O.values())
    info = dict(m=m, L=L, c0=c0, M=M, KA=KA, KB=KB, F=F, occ=occ, O=O, sync=sync)
    return G, u, v, info


def A_tau(info, tau):
    """tau: dict var -> bool. A_tau = KA + union of O_i with tau(x_i) true."""
    A = set(info['KA'])
    for i, lst in info['O'].items():
        if tau[i]:
            A |= set(lst)
    return frozenset(A)


def satisfies(phi, tau):
    return all(any((lit > 0) == tau[abs(lit)] for lit in C) for C in phi)


def assignments(phi):
    vars_ = sorted({abs(l) for C in phi for l in C})
    for bits in itertools.product([False, True], repeat=len(vars_)):
        yield dict(zip(vars_, bits))
