"""Adversarial ear structures for Lemma 4 / Proposition 5 / Theorem 13(a): a small dense core and ears that are
K4 blobs, long paths, triangles with tails, ears hanging from ears, ears whose two boundary edges meet the same
core vertex (p = s), ears between u and v, pendant trees (bridges). 9..16 vertices; graphs are kept only if they
are in DC (repair loop of randgraphs). Usage: python run_ears.py SEED COUNT [workers]"""
import sys, time, random
from collections import Counter
from multiprocessing import Pool
from checks import check_graph
from randgraphs import _repair


def gen(rng):
    n_t = rng.randint(9, 16)
    q = rng.randint(4, 7)
    p = rng.choice([0.5, 0.7, 0.9, 1.0])
    E = set()
    for i in range(q):
        for j in range(i + 1, q):
            if rng.random() < p:
                E.add((i, j))
    nxt = q
    while nxt < n_t:
        typ = rng.choice(["k4", "path4", "tritail", "short", "pendant", "earonear", "uv"])
        size = {"k4": 4, "path4": 4, "tritail": 4, "short": 1, "pendant": 2, "earonear": 2, "uv": 2}[typ]
        if nxt + size > n_t:
            typ, size = "short", 1
        V = list(range(nxt, nxt + size))
        core = list(range(q))
        p_ = rng.choice(core)
        s_ = p_ if rng.random() < 0.25 else rng.choice(core)
        if typ == "k4":
            for i in range(4):
                for j in range(i + 1, 4):
                    E.add((V[i], V[j]))
            E.add((p_, V[0]))
            E.add((s_, V[rng.choice([0, 1])]))
        elif typ in ("path4", "uv"):
            for i in range(size - 1):
                E.add((V[i], V[i + 1]))
            if typ == "uv":
                p_, s_ = 0, 1
            E.add((p_, V[0]))
            E.add((s_, V[-1]))
        elif typ == "tritail":
            E |= {(V[0], V[1]), (V[1], V[2]), (V[0], V[2]), (V[2], V[3])}
            E.add((p_, V[0]))
            E.add((s_, V[3]))
        elif typ == "short":
            if p_ == s_:
                s_ = (p_ + 1) % q
            E.add((p_, V[0]))
            E.add((s_, V[0]))
        elif typ == "pendant":
            E.add((p_, V[0]))
            E.add((V[0], V[1]))
        elif typ == "earonear":
            if nxt == q:
                E.add((p_, V[0])); E.add((V[0], V[1])); E.add((s_, V[1]))
            else:
                w = rng.randrange(q, nxt)
                E.add((w, V[0])); E.add((V[0], V[1])); E.add((rng.choice([w] + core), V[1]))
        nxt += size
    E = {(min(a, b), max(a, b)) for a, b in E if a != b}
    edges = _repair(nxt, E, 2, list(range(q)), rng)
    return (nxt, edges) if edges else None


def work(seed):
    rng = random.Random(seed)
    for _ in range(50):
        g = gen(rng)
        if g:
            n, edges = g
            st, vi = check_graph(n, edges, ordered=False, do_cp=(n <= 10))
            return st, [(seed,) + tuple(x) for x in vi]
    return Counter(), []


if __name__ == "__main__":
    seed = int(sys.argv[1]); count = int(sys.argv[2])
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    t0 = time.time()
    total = Counter(); viol = []
    with Pool(workers) as pool:
        for st, vi in pool.imap_unordered(work, [seed * 10 ** 7 + i for i in range(count)], chunksize=4):
            total.update(st); viol.extend(vi)
    print("adversarial ears seed", seed, "count", count)
    for k in sorted(total):
        print("%-55s %d" % (k, total[k]))
    print("violations:", len(viol))
    for x in viol[:30]:
        print("  ", x)
    print("time %.1fs" % (time.time() - t0))
