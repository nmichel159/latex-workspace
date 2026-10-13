"""Search for PC false positives in the pure switch model 2CH + P2 (switches pairwise incomparable) with a lower hub:
every E-side contains the hub node beta, so P2 holds.  Nodes: a line s = n_0, ..., n_K = a, the hub beta and t.
Switches: entries (E = {a, beta}), exits (E = {beta, t}), fillers (E = {beta}); every F-side is a random set of line
nodes (an interval, or with probability p_gap a random subset).  Random instances, then hill climbing on
no-instances with the score "AC window, then PC window" of hunt2.py.  Exact answer: zz.exact_dfs, cross-checked by
the hub algorithm of Theorem F (at most two switches in E-mode).
Usage: python hub2ch_hunt.py SEED STEPS OUTFILE"""
import sys
import json
import random
import time
import itertools
import chlib
import hunt2
import zz


def random_inst(rng):
    K = rng.randint(3, 8)
    ne, nx, nf = rng.randint(1, 3), rng.randint(1, 3), rng.randint(0, 4)
    p_gap = rng.choice([0.0, 0.2, 0.5])
    return mutate_fix(rng, {"K": K, "sw": [("e", rand_F(rng, K, p_gap)) for _ in range(ne)]
                            + [("x", rand_F(rng, K, p_gap)) for _ in range(nx)]
                            + [("f", rand_F(rng, K, p_gap)) for _ in range(nf)], "p_gap": p_gap})


def rand_F(rng, K, p_gap):
    if rng.random() < p_gap:
        return frozenset(x for x in range(K + 1) if rng.random() < 0.4) or frozenset([rng.randint(0, K)])
    l = rng.randint(0, K - 1)
    r = rng.randint(l + 1, min(K, l + rng.randint(1, 3)))
    return frozenset(range(l, r + 1))


def mutate_fix(rng, st):
    return st


def to_ch(st):
    b = chlib.Builder()
    K = st["K"]
    line = ["s"] + ["n%d" % p for p in range(1, K)] + ["a"]
    b.node("s")
    b.node("t")
    for kind, F in st["sw"]:
        Eset = {"e": ["a", "beta"], "x": ["beta", "t"], "f": ["beta"]}[kind]
        b.switch(kind, Eset, [line[p] for p in sorted(F)])
    return b.inst("s", "t")


def hub_exact(inst):
    n = len(inst[1])
    for k in range(3):
        for P in itertools.combinations(range(n), k):
            modes = [0 if i in P else 1 for i in range(n)]
            if chlib.connected(inst, modes):
                return True
    return False


def mutate(rng, st):
    st = {"K": st["K"], "sw": list(st["sw"]), "p_gap": st["p_gap"]}
    r = rng.random()
    K = st["K"]
    if r < 0.5 and st["sw"]:
        i = rng.randrange(len(st["sw"]))
        kind, F = st["sw"][i]
        F = set(F) ^ {rng.randint(0, K)}
        if F:
            st["sw"][i] = (kind, frozenset(F))
    elif r < 0.65 and st["sw"]:
        i = rng.randrange(len(st["sw"]))
        st["sw"][i] = (st["sw"][i][0], rand_F(rng, K, st["p_gap"]))
    elif r < 0.8 and len(st["sw"]) < 12:
        st["sw"].append((rng.choice("exf"), rand_F(rng, K, st["p_gap"])))
    elif r < 0.9 and len(st["sw"]) > 2:
        del st["sw"][rng.randrange(len(st["sw"]))]
    elif K < 10:
        st["K"] = K + 1
    return st


def main():
    seed, steps, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    rng = random.Random(seed)
    found = {"no": 0, "ac-fp": 0, "pc-fp": 0, "evals": 0}
    cur, cur_score, since = None, -1, 0
    t0 = time.time()
    for step in range(steps):
        if cur is None or since > 200:
            cur = random_inst(rng)
            cur_score, since = -1, 0
        cand = mutate(rng, cur)
        inst = to_ch(cand)
        z = chlib.to_zz(inst)
        found["evals"] += 1
        since += 1
        ex = zz.exact_dfs(z)[0]
        assert ex == hub_exact(inst), "Theorem F algorithm disagrees"
        if ex:
            continue
        found["no"] += 1
        sc, kind = hunt2.score(z, cur_score >= 10000)
        if sc is None:
            continue
        if kind in ("ac-fp", "pc-fp"):
            found[kind] += 1
            if kind == "pc-fp":
                print("PC false positive at step", step, flush=True)
                with open(out, "a") as f:
                    f.write(json.dumps({"seed": seed, "step": step, "n": z.n, "le": [[int(x) for x in r] for r in z.le],
                                        "R": z.R, "u": z.u, "v": z.v, "st": [(k, sorted(F)) for k, F in cand["sw"]],
                                        "K": cand["K"]}) + "\n")
        if sc >= cur_score:
            if sc > cur_score:
                since = 0
            cur, cur_score = cand, sc
        if step % 1000 == 0:
            print(step, found, "%.0fs" % (time.time() - t0), flush=True)
    print("final", seed, found, "%.0fs" % (time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
