"""Adversarial search for false positives of path consistency (PC) on 2CHC + P2 instances (ties: switch classes
forced into one mode, P2 only between members of different classes), the case that dc-algorithm/hunt2.py does not
generate.  Hill climbing on no-instances with the score of hunt2.score (largest AC window that says 'yes', then the
largest PC window), P2 repaired after every mutation.

Modes:
  rand    random 2CHC + P2 seeds
  occ     seeds = occurrence encodings of random unsatisfiable 3-CNF formulas (one class per variable, one member
          per literal occurrence, useful side = the clause gap), P2-completed by random private connectors; only
          seeds that stay unsatisfiable are kept
Every PC false positive is appended to OUTFILE (JSON lines) and printed.
Usage: python ties_hunt.py MODE SEED STEPS OUTFILE [MAXMEM]"""
import os
import sys
import json
import random
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "dc-algorithm"))
import ties  # noqa: E402
import hunt2  # noqa: E402  (read-only import: score function)

MAXMEM = 10
MAXN = 14
ZMAX = 40


def repair(rng, inst):
    N, E, F, s, t, cls = inst
    E, F = list(E), list(F)
    for i, l in ties.p2_missing(E, F, cls):
        if (E[i] & E[l]) or (F[i] & F[l]):
            continue
        if rng.random() < 0.5 and N < MAXN:
            z = N
            N += 1
        else:
            z = rng.randrange(N)
        if rng.random() < 0.5:
            E[i] |= 1 << z
            E[l] |= 1 << z
        else:
            F[i] |= 1 << z
            F[l] |= 1 << z
    return (N, E, F, s, t, cls)


def rand_seed(rng):
    N = rng.randint(4, 8)
    n = rng.randint(4, MAXMEM)
    k = rng.randint(2, min(n, 5))
    return ties.random_p2_instance(rng, N, n, k, rng.choice([0.15, 0.25]), rng.choice([0.15, 0.25]),
                                   fresh=rng.choice([0.3, 0.7]))


def occ_seed(rng):
    """occurrence encoding of a random formula, P2-completed by random private connectors, kept if unsat"""
    for _ in range(200):
        nv = rng.randint(2, 3)
        m = rng.randint(3, 5)
        clauses = []
        for _ in range(m):
            k = rng.choice([1, 2, 2, 3])
            vs = rng.sample(range(nv), min(k, nv))
            clauses.append([(v, rng.random() < 0.5) for v in vs])
        b = ties.Builder()
        for j, cl in enumerate(clauses):
            for v, pos in cl:
                i = b.member(("occ", j, v, pos), v)
                b.add(i, "E" if pos else "F", ("b", j), ("b", j + 1))
        inst = b.inst(("b", 0), ("b", m))
        if ties.solve(inst) is not None:
            continue
        N, E, F, s, t, cls = inst
        E, F = list(E), list(F)
        ok = True
        for i, l in ties.p2_missing(E, F, cls):
            z = N
            N += 1
            if rng.random() < 0.5:
                E[i] |= 1 << z
                E[l] |= 1 << z
            else:
                F[i] |= 1 << z
                F[l] |= 1 << z
        inst = (N, E, F, s, t, cls)
        if ties.solve(inst) is None:
            return inst
    return rand_seed(rng)


def mutate(rng, inst):
    N, E, F, s, t, cls = inst
    E, F, cls = list(E), list(F), list(cls)
    n = len(E)
    r = rng.random()
    if r < 0.3:
        i = rng.randrange(n)
        E[i] ^= 1 << rng.randrange(N)
    elif r < 0.6:
        i = rng.randrange(n)
        F[i] ^= 1 << rng.randrange(N)
    elif r < 0.72:
        i = rng.randrange(n)
        cls[i] = rng.randrange(max(cls) + 2)
    elif r < 0.8 and n < MAXMEM:
        E.append(1 << rng.randrange(N))
        F.append(1 << rng.randrange(N))
        cls.append(rng.randrange(max(cls) + 2))
    elif r < 0.86 and n > 3:
        i = rng.randrange(n)
        del E[i], F[i], cls[i]
    elif r < 0.92 and N < MAXN:
        N += 1
    else:
        x = rng.randrange(N)
        if rng.random() < 0.5 and x != s:
            t = x
        elif x != t:
            s = x
    if s == t:
        return inst
    # renumber classes densely
    ids = {c: k for k, c in enumerate(sorted(set(cls)))}
    cls = [ids[c] for c in cls]
    return repair(rng, (N, E, F, s, t, cls))


def main():
    global MAXMEM
    mode, seed, steps, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    if len(sys.argv) > 5:
        MAXMEM = int(sys.argv[5])
    rng = random.Random(seed)
    seedfn = rand_seed if mode == "rand" else occ_seed
    found = {"ac-fp": 0, "pc-fp": 0, "no": 0, "evals": 0}
    cur, cur_score, since = None, -1, 0
    t0 = time.time()
    for step in range(steps):
        if cur is None or since > 300:
            cur = seedfn(rng)
            z, _ = ties.to_zz(cur)
            sc, kind = hunt2.score(z, False)
            cur_score = -1 if sc is None else sc
            since = 0
        cand = mutate(rng, cur)
        if cand is cur:
            since += 1
            continue
        z, _ = ties.to_zz(cand)
        if z.n > ZMAX:
            since += 1
            continue
        sc, kind = hunt2.score(z, cur_score >= 10000)
        found["evals"] += 1
        since += 1
        if sc is None:
            continue
        found["no"] += 1
        if kind in ("ac-fp", "pc-fp"):
            found[kind] += 1
            if kind == "pc-fp" or found["ac-fp"] <= 10:
                N, E, F, s, t, cls = cand
                rec = {"mode": mode, "seed": seed, "step": step, "kind": kind, "N": N, "E": E, "F": F, "s": s,
                       "t": t, "cls": cls, "zn": z.n, "zR": len(z.R)}
                with open(out, "a") as f:
                    f.write(json.dumps(rec) + "\n")
            if kind == "pc-fp":
                print("PC FALSE POSITIVE at step", step, ties.fmt(cand), flush=True)
        if sc >= cur_score:
            if sc > cur_score:
                since = 0
            cur, cur_score = cand, sc
        if step % 500 == 0:
            print(step, found, "%.0fs" % (time.time() - t0), flush=True)
    print(mode, seed, found, "%.0fs" % (time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
