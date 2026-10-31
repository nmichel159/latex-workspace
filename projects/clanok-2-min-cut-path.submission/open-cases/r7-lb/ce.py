"""Agent r7-lb (2026-10-31): cross-entropy search over the structured designs of adv.py (r7-lb.md Section 3.3).

usage: python ce.py SEED WORD SECONDS OUTPREFIX [BATCH] [ELITE] [ALPHA]
The design is the one of adv.py (hubs bottom/top, no bad-pair extras): path word WORD (e.g. E5F5), same-type contacts
(E-E: FF or UW(top); F-F: EE or LW(bottom)), cross contacts one of E F L U C per pair of an E-member and an F-member
(C = F-member below E-member, no contact).  Each cell has its own categorical distribution; every round draws BATCH
designs, evaluates them (adv.evaluate: exact least single-term cost, minimum over all minimal pairs, plus the mean cost
of the single pairs), keeps the best ELITE fraction and moves the distributions towards the elite (smoothing ALPHA).
Logs every new maximum cost and saves it (genome and instance) under OUTPREFIX.
"""
import sys
import os
import time
import random
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import design
import lbcore
import adv

CROSS = "EFLUC"


def build_genome(word, cross, same, rng):
    n = len(word)
    bottom, top = n, n + 1
    g = design.new_genome(word, 2, default="R", seed=rng.randrange(10 ** 6))
    m = n + 2
    rel = []
    for v in range(m):
        if v != bottom:
            rel.append((bottom, v))
        if v != top:
            rel.append((v, top))
    cont = {}
    for (i, j), c in same.items():
        if word[i] == "E":
            cont[design.pair_key(i, j)] = "FF" if c == 0 else ["UW", top]
        else:
            cont[design.pair_key(i, j)] = "EE" if c == 0 else ["LW", bottom]
    for (e, f), c in cross.items():
        key = design.pair_key(e, f)
        if c == "E":
            cont[key] = "EE"
        elif c == "F":
            cont[key] = "FF"
        elif c == "L":
            cont[key] = ["LW", bottom]
        elif c == "U":
            cont[key] = ["UW", top]
        else:
            rel.append((f, e))
    g["rel"] = rel
    g["contact"] = cont
    return g


def draw(rng, probs):
    x = rng.random()
    acc = 0.0
    for k, p in probs.items():
        acc += p
        if x <= acc:
            return k
    return k


def main():
    seed = int(sys.argv[1])
    word = adv.parse_word(sys.argv[2])
    seconds = float(sys.argv[3])
    out = sys.argv[4]
    batch = int(sys.argv[5]) if len(sys.argv) > 5 else 400
    elite_frac = float(sys.argv[6]) if len(sys.argv) > 6 else 0.05
    alpha = float(sys.argv[7]) if len(sys.argv) > 7 else 0.6
    rng = random.Random(seed)
    n = len(word)
    cells = [(i, j) for i in range(n) for j in range(n) if word[i] == "E" and word[j] == "F"]
    sames = [(i, j) for i in range(n) for j in range(i + 1, n) if word[i] == word[j]]
    cp = {c: {k: 1.0 / len(CROSS) for k in CROSS} for c in cells}
    sp = {c: {0: 0.5, 1: 0.5} for c in sames}
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    f = open(out + ".log", "a", encoding="utf-8")

    def say(s):
        print(s, flush=True)
        f.write(s + "\n")
        f.flush()
    say("ce seed %d word %s seconds %.0f batch %d elite %.2f alpha %.2f pid %d" % (
        seed, word, seconds, batch, elite_frac, alpha, os.getpid()))
    t0 = time.time()
    best_cost = -1
    rnd = 0
    while time.time() - t0 < seconds:
        rnd += 1
        pop = []
        hist = Counter()
        for _ in range(batch):
            cross = {c: draw(rng, cp[c]) for c in cells}
            same = {c: draw(rng, sp[c]) for c in sames}
            g = build_genome(word, cross, same, rng)
            I = design.build(g)
            if I is None:
                continue
            try:
                sc, info = (adv.evaluate2 if os.environ.get("ADV_OBJ") == "2" else adv.evaluate)(I)
            except RuntimeError:
                continue
            if sc is None:
                continue
            hist[info["cost"]] += 1
            pop.append((sc, cross, same, g, info, I))
            if info["cost"] > best_cost:
                best_cost = info["cost"]
                design.save_genome(g, out + "-cost%d.json" % best_cost, dict(info))
                lbcore.dump(I, out + "-cost%d-inst.json" % best_cost, dict(cost=best_cost, npairs=info["npairs"]))
                say("round %d NEW MAX cost %d mean %.2f npairs %d m %d (%.0fs)" % (
                    rnd, best_cost, info["mean"], info["npairs"], I.m, time.time() - t0))
        if not pop:
            continue
        pop.sort(key=lambda p: -p[0])
        ne = max(5, int(elite_frac * len(pop)))
        elite = pop[:ne]
        for c in cells:
            cnt = Counter(e[1][c] for e in elite)
            for k in CROSS:
                cp[c][k] = alpha * (cnt[k] / ne) + (1 - alpha) * cp[c][k]
            tot = sum(cp[c].values())
            for k in CROSS:
                cp[c][k] = max(0.02, cp[c][k] / tot)
            tot = sum(cp[c].values())
            for k in CROSS:
                cp[c][k] /= tot
        for c in sames:
            cnt = Counter(e[2][c] for e in elite)
            for k in (0, 1):
                sp[c][k] = alpha * (cnt[k] / ne) + (1 - alpha) * sp[c][k]
            tot = sum(sp[c].values())
            for k in (0, 1):
                sp[c][k] = max(0.02, sp[c][k] / tot)
            tot = sum(sp[c].values())
            for k in (0, 1):
                sp[c][k] /= tot
        say("round %d pop %d costs %s elite score %.2f..%.2f best cost %d (%.0fs)" % (
            rnd, len(pop), dict(sorted(hist.items())), elite[0][0], elite[-1][0], best_cost, time.time() - t0))
    say("END best cost %d rounds %d (%.0fs)" % (best_cost, rnd, time.time() - t0))


if __name__ == "__main__":
    main()
