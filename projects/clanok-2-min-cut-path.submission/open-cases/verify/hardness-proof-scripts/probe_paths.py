"""Probe: which vertices and edges can a u-v path inside a minimum cut of the reduction graph use?

For every formula of families (a) m <= 2 over x1, x2 (clauses multisets of size 1..3) and 100 random
3-CNF formulas with m <= 5, every minimum cut A_tau (own Picard-Queyranne enumeration), ALL simple u-v paths in
H_A = (V, delta(A)) are enumerated. Checked: every path uses only h_k, beta_k (k = 0..m) and occurrence vertices
whose literal is true under tau; no clique edge, no sync edge; the length is odd and >= 2m+1; for (x1)(x1) the only
length is 5.
Run: python -I probe_paths.py
"""
import sys, os, itertools, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from multiprocessing import Pool
import networkx as nx
from construct import build, A_tau, satisfies, assignments
from vexact import min_cuts_pq, cut_graph


def job(phi):
    G, u, v, info = build(phi)
    m = info['m']
    _, cuts = min_cuts_pq(G, u, v)
    inv = {A_tau(info, t): t for t in assignments(phi)}
    errs = []
    npaths = 0
    lengths = set()
    syncset = {frozenset(e) for e in info['sync']}
    for A in cuts:
        t = inv.get(A)
        if t is None:
            errs.append('cut not A_tau')
            continue
        H = cut_graph(G, A)
        if not nx.has_path(H, u, v):
            continue
        allowed = {f'h{k}' for k in range(m + 1)} | {f'B{k}' for k in range(m + 1)}
        allowed |= {o for o, (k, lit) in info['occ'].items() if (lit > 0) == t[abs(lit)]}
        for p in nx.all_simple_paths(H, u, v):
            npaths += 1
            l = len(p) - 1
            lengths.add(l)
            if not set(p) <= allowed:
                errs.append(f'path uses {set(p) - allowed}')
            if any(frozenset(e) in syncset for e in zip(p, p[1:])):
                errs.append('sync edge on path')
            if l % 2 == 0 or l < 2 * m + 1:
                errs.append(f'length {l}')
            if npaths > 200000:
                errs.append('too many paths; stopped')
                return phi, npaths, sorted(lengths), errs
    return phi, npaths, sorted(lengths), errs


def main():
    lits = [1, -1, 2, -2]
    ms = [list(c) for r in (1, 2, 3) for c in itertools.combinations_with_replacement(lits, r)]
    fs = [[C] for C in ms] + [[C1, C2] for C1 in ms for C2 in ms]
    rnd = random.Random(7)
    for _ in range(100):
        nv = rnd.randint(2, 5)
        m = rnd.randint(2, 5)
        fs.append([[rnd.choice([1, -1]) * rnd.randint(1, nv) for _ in range(3)] for _ in range(m)])
    with Pool(30) as pool:
        res = pool.map(job, fs, chunksize=4)
    tot = sum(r[1] for r in res)
    bad = [r for r in res if r[3]]
    lines = [f'formulas {len(res)}, paths enumerated {tot}, formulas with a violation {len(bad)}']
    for r in res:
        if r[0] == [[1], [1]]:
            lines.append(f'(x1)(x1): {r[1]} paths, lengths {r[2]}')
    for r in bad[:10]:
        lines.append(f'VIOLATION {r[0]}: {r[3][:3]}')
    txt = '\n'.join(lines)
    print(txt)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results-probe-paths.txt'), 'w') as fh:
        fh.write(txt + '\n')


if __name__ == '__main__':
    main()
