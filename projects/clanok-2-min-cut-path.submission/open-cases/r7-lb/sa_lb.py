"""Simulated annealing on planted-path designs (design.py) maximising the exact single-term cost (r7-lb.md Section 3).

usage: python sa_lb.py SEED WORD NX STEPS OUTPREFIX [T0] [MOVES] [DEFAULT] [SECONDS]
  WORD: path word over E, F (or 'rand:N'); NX: extra switches; MOVES: letters c (contact), r (relation),
  v (voluntary node), t (tie), default 'crvt'.  DEFAULT: default contact 'R', 'EE', 'FF'.
Score of an instance = 4 * cost + sum_{t=0..3} min(t + p_t, CAP), with cost the exact least total cost of one
connecting term and p_t the least anchors + flips with at most t tools (lbcore.mincost, lbcore.profile).
The best genome and instance are saved as OUTPREFIX-best.json (genome) and OUTPREFIX-best-inst.json (lbcore.dump),
each improvement of the best cost is logged; every best instance is re-verified (term rebuilt and tested).
"""
import sys
import os
import math
import time
import random
import copy
import design
import lbcore
lbcore.WORK_CAP = 200000

CAP = 12


def score(I):
    """10 * cost - min(log2(1 + N), 9.9), N = number of connecting terms of cost exactly `cost` (cost <= 2)."""
    pairs = lbcore.valid_pairs(I, state_cap=300_000)
    if not pairs:
        return None, None
    Irev = lbcore.reverse(I)
    r = lbcore.mincost(I, cap=CAP, pairs=pairs, Irev=Irev)
    c = r["total"] if isinstance(r["total"], int) else CAP + 1
    N = lbcore.count_terms(I, c, limit=1000) if c <= 2 else 1
    return 10 * c - min(math.log2(1 + N), 9.9), (c, N, r, len(pairs))


def mutate(rng, g, moves):
    g = copy.deepcopy(g)
    n = len(g["word"])
    m = n + g["nx"]
    mv = rng.choice(moves)
    if mv == "c":
        x, y = rng.sample(range(m), 2)
        kinds = ["EE", "FF", "LW", "UW"]
        k = rng.choice(kinds)
        if k in ("LW", "UW"):
            g["contact"][design.pair_key(x, y)] = [k, rng.randrange(m)]
        else:
            g["contact"][design.pair_key(x, y)] = k
    elif mv == "r":
        if g["rel"] and rng.random() < 0.4:
            g["rel"].pop(rng.randrange(len(g["rel"])))
        else:
            a, b = rng.sample(range(m), 2)
            g["rel"].append((a, b))
    elif mv == "t":
        a, b = rng.sample(range(m), 2)
        g["rel"].append((a, b))
        g["rel"].append((b, a))
    elif mv == "v":
        if g["vol"] and rng.random() < 0.4:
            g["vol"].pop(rng.randrange(len(g["vol"])))
        else:
            w1, w2 = rng.sample(range(m), 2)
            g["vol"].append(((w1, rng.randrange(2)), (w2, rng.randrange(2))))
    return g


def main():
    seed = int(sys.argv[1])
    word = sys.argv[2]
    nx = int(sys.argv[3])
    steps = int(sys.argv[4])
    out = sys.argv[5]
    T0 = float(sys.argv[6]) if len(sys.argv) > 6 else 2.0
    moves = sys.argv[7] if len(sys.argv) > 7 else "crvt"
    default = sys.argv[8] if len(sys.argv) > 8 else "R"
    seconds = float(sys.argv[9]) if len(sys.argv) > 9 else 1e9
    rng = random.Random(seed)
    if word.startswith("rand:"):
        n = int(word[5:])
        word = "".join(rng.choice("EF") for _ in range(n))
    g = design.new_genome(word, nx, default=default, seed=seed)
    I = design.build(g)
    sc, info = score(I)
    cur, cur_sc = g, sc
    best_sc, best_info, best_g = sc, info, g
    t0 = time.time()
    log = open(out + ".log", "a", encoding="utf-8")

    def say(s):
        print(s, flush=True)
        log.write(s + "\n")
        log.flush()
    say("sa_lb seed %d word %s nx %d steps %d T0 %.2f moves %s default %s pid %d" % (
        seed, word, nx, steps, T0, moves, default, os.getpid()))
    say("start score %.2f cost %s N %s" % (sc, info[0], info[1]))
    best_cost = info[0]
    for it in range(steps):
        if time.time() - t0 > seconds:
            break
        T = T0 * (1 - it / steps) + 0.05
        g2 = mutate(rng, cur, moves)
        I2 = design.build(g2)
        if I2 is None:
            continue
        try:
            sc2, info2 = score(I2)
        except RuntimeError:
            continue
        if sc2 is None:
            continue
        if sc2 >= cur_sc or rng.random() < math.exp((sc2 - cur_sc) / T):
            cur, cur_sc = g2, sc2
            if sc2 > best_sc:
                best_sc, best_info, best_g = sc2, info2, g2
                if info2[0] > best_cost or it % 50 == 0:
                    say("it %d score %.2f cost %s N %s pairs %d m %d (%.0fs)" % (
                        it, sc2, info2[0], info2[1], info2[3], I2.m, time.time() - t0))
                best_cost = max(best_cost, info2[0])
                Ib = design.build(best_g)
                r = best_info[2]
                design.save_genome(best_g, out + "-best.json",
                                   dict(cost=best_info[0], N=best_info[1], verified=r.get("verified"),
                                        term=[r.get("kind"), r.get("T"), r.get("Tp"), r.get("anchors"),
                                              r.get("flips")]))
                lbcore.dump(Ib, out + "-best-inst.json", dict(cost=best_info[0], N=best_info[1]))
        if it % 500 == 0:
            say("  it %d cur %.2f best %.2f (cost %s) (%.0fs)" % (it, cur_sc, best_sc, best_info[0], time.time() - t0))
    say("END best score %.2f cost %s N %s term %s verified %s (%.0fs)" % (
        best_sc, best_info[0], best_info[1],
        (best_info[2].get("kind"), best_info[2].get("T"), best_info[2].get("Tp"), best_info[2].get("anchors"),
         best_info[2].get("flips")), best_info[2].get("verified"), time.time() - t0))


if __name__ == "__main__":
    main()
