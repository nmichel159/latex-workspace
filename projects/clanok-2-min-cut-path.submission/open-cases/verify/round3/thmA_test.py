"""Theorem A, own implementation (thmA.py) against references (agent verify-round3).
Families:
  rand  : connected G(n, p), n = 4..12, 30% multigraphs, u, v at distance >= 2 when possible;
          reference: brute force over all vertex sets; all lemma checks of thmA.ThmA.check_lemmas.
  gpi   : the graph G(Pi) of Theorem 13(b) (M = 1) of a random P2 instance (d = 2, c = N, up to ~100 vertices);
          reference: ZZ answer by down-set enumeration (r3core) and the flow-pruned path search (realise3).
Every "yes" witness is checked: its edges lie in the cut of the union of the closures of their tails, which has
value c, and they form a u-v walk; Lemma A4 (largest values form a solution) is checked on every solved CSP.
Usage: python thmA_test.py tag baseseed count jobs [procs]"""
import random
import sys
import time
from collections import deque, defaultdict
from multiprocessing import Pool

from thmA import ThmA, brute_pimc, rand_graph
from r3core import random_instance
from realise3 import realise, Flow, pimc_search


def dist2(n, edges, u):
    adj = defaultdict(set)
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    d = {u: 0}
    dq = deque([u])
    while dq:
        x = dq.popleft()
        for y in adj[x]:
            if y not in d:
                d[y] = d[x] + 1; dq.append(y)
    return d


def job(args):
    fam, seed, count = args
    rng = random.Random(seed)
    st = {"inst": 0, "yes": 0, "mismatch": 0, "lemma_bad": 0, "a4_bad": 0, "witness_bad": 0, "maxnodes": 0,
          "maxc": 0, "len": {}, "far": 0}
    bad = []
    for _ in range(count):
        if fam == "rand":
            n = rng.randint(4, 12)
            edges = rand_graph(rng, n, rng.choice([0.3, 0.45, 0.6, 0.8]), multi=rng.random() < 0.3)
            u = rng.randrange(n)
            d = dist2(n, edges, u)
            far = [x for x in range(n) if d[x] >= 2]
            v = rng.choice(far) if far else rng.choice([x for x in range(n) if x != u])
            st["far"] += bool(far)
            T = ThmA(n, edges, u, v)
            ref, cuts = brute_pimc(n, edges, u, v, T.c)
            lb = T.check_lemmas(cuts)
            if lb:
                st["lemma_bad"] += 1
                bad.append(("lemma", set(lb), n, edges, u, v))
        else:
            inst = random_instance(rng, nb=rng.randint(1, 2), nm=rng.randint(2, 5), nt=rng.randint(1, 2),
                                   p_rel=rng.choice([0.2, 0.4]), p_edge=rng.choice([0.3, 0.5, 0.7]),
                                   p_eqmid=rng.choice([0, 0.1]))
            G, N = realise(inst, M=1)
            if N <= 3:
                continue
            n = G.number_of_nodes()
            edges = list(G.edges())
            u, v = inst.u, inst.v
            T = ThmA(n, edges, u, v)
            ref = inst.solve_downsets()[0]
            P, _ = pimc_search(G, u, v, T.c, Flow(G))
            if (P is not None) != ref or T.c != N:
                st["mismatch"] += 1
                bad.append(("reference", N, T.c))
        ans, sol, a4 = T.solve()
        st["inst"] += 1; st["yes"] += ref
        st["maxnodes"] = max(st["maxnodes"], T.nodes); st["maxc"] = max(st["maxc"], T.c)
        if ans != ref:
            st["mismatch"] += 1
            bad.append(("answer", fam, n, edges, u, v, ans, ref))
        if not a4:
            st["a4_bad"] += 1
        if ans:
            if not T.check_witness(sol, None):
                st["witness_bad"] += 1
                bad.append(("witness", fam, n, edges, u, v, sol))
            st["len"][len(sol)] = st["len"].get(len(sol), 0) + 1
    return fam, seed, st, bad[:5]


if __name__ == "__main__":
    tag, base, count, jobs = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    procs = min(int(sys.argv[5]) if len(sys.argv) > 5 else 6, 8)
    fams = ["rand", "gpi"]
    t0 = time.time()
    tot = {}
    out = open("results-A-%s.txt" % tag, "w")
    with Pool(procs) as pool:
        for fam, seed, st, bad in pool.imap_unordered(job, [(fams[j % 2], base + j, count) for j in range(jobs)]):
            d = tot.setdefault(fam, {})
            for k, x in st.items():
                if k == "len":
                    dl = d.setdefault("len", {})
                    for a, b in x.items():
                        dl[a] = dl.get(a, 0) + b
                elif k in ("maxnodes", "maxc"):
                    d[k] = max(d.get(k, 0), x)
                else:
                    d[k] = d.get(k, 0) + x
            line = "%s seed %d: %s" % (fam, seed, st)
            print(line, flush=True)
            out.write(line + "\n")
            for b in bad:
                out.write("  BAD %r\n" % (b,))
            out.flush()
    viol = 0
    out.write("\nTOTALS (%.0fs)\n" % (time.time() - t0))
    for fam, d in sorted(tot.items()):
        out.write("%s: %s\n" % (fam, d))
        viol += d["mismatch"] + d["lemma_bad"] + d["a4_bad"] + d["witness_bad"]
    out.write("violations: %d\n" % viol)
    out.close()
    print("violations:", viol)
