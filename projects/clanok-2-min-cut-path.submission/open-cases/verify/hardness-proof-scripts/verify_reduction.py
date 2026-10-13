"""Independent check of Lemmas 2.2-2.4, Theorem 2.5 and Corollary 2.6 of theory-hardness.md.

Per formula phi (construction re-implemented in construct.py):
 V1  c(u,v) = c0 (own max flow)
 V2  d(u,v) = 2 and diameter = 3; a filler pair fA0, fB0 is at distance 3; c(fA0, fB0) recorded
 V3  the minimum cuts (own Picard-Queyranne enumeration) are exactly the sets A_tau, 2^(#variables) of them
 V4  Lemma 2.4: for every tau, u-v connected in H_tau iff tau satisfies phi
 V5  answer (some minimum cut contains a u-v path) = satisfiability (brute force over assignments)
 V6  Cor. 2.6 (d): if satisfiable, the shortest u-v path inside any minimum cut has length >= 2m+1, and odd
 V7  Lemma 2.3 cut formula on random sets K_A <= A <= V - K_B; random sets splitting a clique have cut >= c0+1
 V8  (small graphs, n <= NMAX) brute force over ALL vertex sets: c, the set of minimum cuts, and the exact cp
     by cp = min_A |delta(A)| + dist01_A(u,v) (no lemma used); cp == c iff satisfiable; cp in {c, c+1}
Run: python -I verify_reduction.py
"""
import sys, os, time, random, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from multiprocessing import Pool
import networkx as nx
from construct import build, A_tau, satisfies, assignments, params
from vexact import maxflow, min_cuts_pq, cut_size, cut_graph, cp_bruteforce

NMAX = 25


def check(phi, brute=False, seed=0):
    rnd = random.Random(seed)
    G, u, v, info = build(phi)
    m, L, c0, M = info['m'], info['L'], info['c0'], info['M']
    errs = []
    c, _ = maxflow(G, u, v)
    if c != c0:
        errs.append(f'V1 c={c} c0={c0}')
    du = nx.single_source_shortest_path_length(G, u)
    if du[v] != 2:
        errs.append(f'V2 d={du[v]}')
    ecc = nx.eccentricity(G)
    diam = max(ecc.values())
    if diam != 3:
        errs.append(f'V2 diam={diam}')
    dff = nx.shortest_path_length(G, 'fA0', 'fB0')
    cff, _ = maxflow(G, 'fA0', 'fB0')
    if dff != 3:
        errs.append(f'V2 d(fA0,fB0)={dff}')
    val, cuts = min_cuts_pq(G, u, v)
    taus = list(assignments(phi))
    Aset = {A_tau(info, t): t for t in taus}
    if set(cuts) != set(Aset) or len(cuts) != len(Aset) or len(Aset) != 2 ** len(info['O']):
        errs.append(f'V3 #cuts={len(cuts)} #Atau={len(Aset)}')
    sat = any(satisfies(phi, t) for t in taus)
    ans = False
    minlen = None
    for A, t in Aset.items():
        if cut_size(G, A) != c0:
            errs.append('V3 |delta(A_tau)| != c0')
        H = cut_graph(G, A)
        conn = nx.has_path(H, u, v)
        if conn != satisfies(phi, t):
            errs.append(f'V4 tau={t} conn={conn}')
        if conn:
            ans = True
            l = nx.shortest_path_length(H, u, v)
            minlen = l if minlen is None else min(minlen, l)
            if l < 2 * m + 1 or l % 2 == 0:
                errs.append(f'V6 length {l} < 2m+1={2*m+1} or even')
    if ans != sat:
        errs.append(f'V5 ans={ans} sat={sat}')
    # V7
    occs = list(info['occ'])
    syncset = {frozenset(e) for e in info['sync']}
    for _ in range(30):
        S = {o for o in occs if rnd.random() < 0.5}
        A = set(info['KA']) | S
        s = sum(1 for e in syncset if len(e & S) == 1)
        if cut_size(G, A) != c0 + s:
            errs.append('V7 formula')
        # split a clique: move a random nonempty proper part of K_A out or of K_B in (u, v fixed)
        B = set(A)
        if rnd.random() < 0.5:
            moved = [x for x in info['KA'] if x != u and rnd.random() < 0.3] or [info['KA'][-1]]
            B -= set(moved)
        else:
            moved = [x for x in info['KB'] if x != v and rnd.random() < 0.3] or [info['KB'][-1]]
            B |= set(moved)
        if cut_size(G, B) < c0 + 1:
            errs.append('V7 split clique cut <= c0')
    rec = dict(phi=phi, n=G.number_of_nodes(), e=G.number_of_edges(), c=c, sat=sat, ans=ans,
               ncuts=len(cuts), minlen=minlen, cff=cff, M=M, brute=None)
    if brute and G.number_of_nodes() <= NMAX:
        cp, cb, d, mc = cp_bruteforce(G, u, v)
        ok = (cb == c0 and set(mc) == set(Aset) and (cp == cb) == sat and cb <= cp <= cb + 1)
        if not ok:
            errs.append(f'V8 cp={cp} c={cb} #mc={len(mc)} sat={sat}')
        rec['brute'] = (cp, cb, len(mc))
    rec['errs'] = errs
    return rec


def formulas():
    lits = [1, -1, 2, -2]
    ms = [tuple(sorted(c)) for r in (1, 2, 3) for c in itertools.combinations_with_replacement(lits, r)]
    out = []
    # (a) all formulas with m = 1, 2 over x1, x2, clauses multisets of size 1..3
    for C in ms:
        out.append(('a', [list(C)]))
    for C1 in ms:
        for C2 in ms:
            out.append(('a', [list(C1), list(C2)]))
    # (b) m = 3, clauses of size 1..2 over x1, x2
    ms2 = [c for c in ms if len(c) <= 2]
    for Cs in itertools.product(ms2, repeat=3):
        out.append(('b', [list(c) for c in Cs]))
    # (c) random 3-CNF, n = 2..7 variables, m = 2..14 clauses; (d) random mixed lengths 1..4
    rnd = random.Random(20261012)
    for _ in range(400):
        nv = rnd.randint(2, 7)
        m = rnd.randint(2, 14)
        out.append(('c', [[rnd.choice([1, -1]) * rnd.randint(1, nv) for _ in range(3)] for _ in range(m)]))
    for _ in range(200):
        nv = rnd.randint(1, 5)
        m = rnd.randint(1, 10)
        out.append(('d', [[rnd.choice([1, -1]) * rnd.randint(1, nv) for _ in range(rnd.randint(1, 4))]
                          for _ in range(m)]))
    # (e) small unsatisfiable cores: (x1)(-x1), (x1 x2)(x1 -x2)(-x1 x2)(-x1 -x2), all 8 clauses on 3 vars
    out.append(('e', [[1], [-1]]))
    out.append(('e', [[1, 2], [1, -2], [-1, 2], [-1, -2]]))
    out.append(('e', [[a * 1, b * 2, c * 3] for a in (1, -1) for b in (1, -1) for c in (1, -1)]))
    return out


def job(arg):
    i, (fam, phi) = arg
    m, L, c0, M = params(phi)
    n = 2 * M + L
    brute = n <= NMAX
    t = time.time()
    rec = check(phi, brute=brute, seed=i)
    rec['fam'] = fam
    rec['time'] = time.time() - t
    return rec


def main():
    t0 = time.time()
    fs = formulas()
    with Pool(30) as pool:
        recs = pool.map(job, list(enumerate(fs)), chunksize=4)
    nfail = sum(1 for r in recs if r['errs'])
    lines = []
    lines.append(f'formulas {len(recs)}; failures {nfail}; time {time.time()-t0:.0f} s')
    for fam in 'abcde':
        R = [r for r in recs if r['fam'] == fam]
        if not R:
            continue
        lines.append(f'family {fam}: {len(R)} formulas, sat {sum(r["sat"] for r in R)}, '
                     f'unsat {sum(not r["sat"] for r in R)}, n {min(r["n"] for r in R)}-{max(r["n"] for r in R)}, '
                     f'edges {min(r["e"] for r in R)}-{max(r["e"] for r in R)}, c {min(r["c"] for r in R)}-{max(r["c"] for r in R)}, '
                     f'brute-force (all vertex sets, exact cp) {sum(1 for r in R if r["brute"])}, '
                     f'failures {sum(1 for r in R if r["errs"])}')
    cffs = {(r['M'], r['cff']) for r in recs}
    lines.append('c(fA0,fB0) vs M: ' + ', '.join(f'M={a}: c={b}' for a, b in sorted(cffs)[:8]) + ' ...')
    lines.append('c(fA0,fB0) == M-2 for all: ' + str(all(r['cff'] == r['M'] - 2 for r in recs)))
    br = [r for r in recs if r['brute']]
    lines.append('brute-force instances (phi, n, cp, c, #mincuts, sat):')
    for r in br[:60]:
        lines.append(f'  {r["phi"]}  n={r["n"]} cp={r["brute"][0]} c={r["brute"][1]} #mc={r["brute"][2]} sat={r["sat"]} minlen={r["minlen"]}')
    for r in recs:
        if r['errs']:
            lines.append(f'FAIL {r["phi"]}: {r["errs"][:5]}')
    txt = '\n'.join(lines)
    print(txt)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results-verify-reduction.txt'), 'w') as fh:
        fh.write(txt + '\n')


if __name__ == '__main__':
    main()
