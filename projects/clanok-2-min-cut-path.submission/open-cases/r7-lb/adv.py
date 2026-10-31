"""Agent r7-lb, round of 2026-10-31: anchor-hostile designs and a smoother objective (r7-lb.md Section 3.3).

usage:
  python adv.py sample SEED K Q COUNT [PROBS] LOG      random structured instances, distribution of the cost
  python adv.py sa SEED K Q SECONDS OUTPREFIX [PROBS] [START] [T0]
                                                      annealing with the smooth objective from the best of 40 samples
                                                      (or from the genome file START)
PROBS: letters E F L U C and weights, e.g. "E3F3L1U1C1" (cross pairs a_i b_j: E = EE contact, F = FF contact,
  L = LW witness at the hub 'bottom', U = UW witness at the hub 'top', C = relation b_j < a_i, no contact).

Design (all through design.py, so P2 and the validity of the planted path hold by construction):
  path word E^K F^K: members a_0..a_{K-1} (E), b_0..b_{K-1} (F) = switches 0..2K-1; hubs bottom = 2K (below everything)
  and top = 2K+1 (above everything); Q bad-pair extras Y_1..Y_Q (E-side nodes, below every X) and X_1..X_Q
  (F-side nodes), Y_i < X_j for all i, j, Y_i < some b, X_j > some a (bad pairs of r5-core.md Section 6.4).
  Contacts of same-type pairs that cannot shortcut the planted path: a_i a_j: FF or UW(top); b_i b_j: EE or LW(bottom).
  Cross pairs a_i b_j by PROBS.  Extras get random contacts.
Objective (smooth): S = 10 * cost + min(mean, 6) - 0.1 * log2(1 + N), where cost is the exact least single-term
cost (lbcore.mincost, minimum over all minimal pairs), mean is the mean over (at most 40 of) the minimal pairs of the
exact least single-term cost of that pair alone (so that raising the cost of the cheap pairs is rewarded) and N the
number of optimal terms.
"""
import sys
import os
import math
import time
import random
import copy
import json

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import design
import lbcore
import sa_lb
from lbcore import bits

lbcore.WORK_CAP = 200000
CAP = 8


def pair_cost(I, Irev, L, Up, cap):
    for c in range(0, cap + 1):
        for kind, J, Lm, Um in (("E", I, L, Up), ("F", Irev, Up, L)):
            try:
                r = lbcore.e_term(J, Lm, Um, c, None)
            except RuntimeError:
                return cap + 1
            if r is not None:
                return c
    return cap + 1


def evaluate(I, maxpairs=40):
    """(score, info) with info = dict(cost, N, mean, npairs, costs)."""
    pairs = lbcore.valid_pairs(I, state_cap=300_000)
    if not pairs:
        return None, None
    Irev = lbcore.reverse(I)
    costs = []
    for (L, Up) in pairs[:maxpairs]:
        costs.append(pair_cost(I, Irev, L, Up, 6))
    cmin = min(costs)
    if len(pairs) > maxpairs:               # cheapest pair may be among the rest: use the exact minimum
        r = lbcore.mincost(I, cap=CAP, pairs=pairs, Irev=Irev)
        cmin = r["total"] if isinstance(r["total"], int) else CAP + 1
    N = lbcore.count_terms(I, cmin, limit=500) if cmin <= 2 else 1
    mean = sum(costs) / len(costs)
    sc = 10 * cmin + min(mean, 6) - 0.1 * math.log2(1 + N)
    return sc, dict(cost=cmin, N=N, mean=mean, npairs=len(pairs), costs=sorted(costs))


OBJ = os.environ.get("ADV_OBJ", "1")


def evaluate2(I, maxpairs=40):
    """Objective 2: S = 8 * cost + (c0 + c1 + c2 + c3) / 2 + mean / 2 - 0.1 log2(1 + N), c_t = least single-term cost
    with at most t tools (capped at 9)."""
    sc, info = evaluate(I, maxpairs)
    if sc is None:
        return None, None
    pairs = lbcore.valid_pairs(I, state_cap=300_000)
    Irev = lbcore.reverse(I)
    cs = []
    for t in range(4):
        try:
            r = lbcore.mincost(I, cap=9, tmax=t, pairs=pairs, Irev=Irev)
            tot = r["total"]
            cs.append(tot if isinstance(tot, int) else 10)
        except RuntimeError:
            cs.append(10)
    info["ct"] = cs
    sc2 = 8 * info["cost"] + sum(cs) / 2 + min(info["mean"], 6) / 2 - 0.1 * math.log2(1 + info["N"])
    return sc2, info


def parse_probs(s):
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        j = i + 1
        while j < len(s) and (s[j].isdigit() or s[j] == "."):
            j += 1
        out.append((c, float(s[i + 1:j]) if j > i + 1 else 1.0))
        i = j
    return out


def pick(rng, probs):
    tot = sum(w for _, w in probs)
    x = rng.random() * tot
    for c, w in probs:
        x -= w
        if x <= 0:
            return c
    return probs[-1][0]


def parse_word(w):
    """'E4F4' -> 'EEEEFFFF'; a literal word like 'EEFF' is returned as is."""
    if any(ch.isdigit() for ch in w):
        out = ""
        i = 0
        while i < len(w):
            c = w[i]
            j = i + 1
            while j < len(w) and w[j].isdigit():
                j += 1
            out += c * (int(w[i + 1:j]) if j > i + 1 else 1)
            i = j
        return out
    return w


def cross_contact(rng, probs, x, y, bottom, top):
    """Random contact for the path positions x (type tx) and y; returns ('rel',) for a comparable pair."""
    c = pick(rng, probs)
    return {"E": "EE", "F": "FF", "L": ["LW", bottom], "U": ["UW", top], "C": "REL"}[c]


def same_contact(rng, tx, bottom, top):
    """Same-type pair: E-E gets FF or UW(top), F-F gets EE or LW(bottom) (no shortcut of the planted path)."""
    if tx == "E":
        return "FF" if rng.random() < 0.5 else ["UW", top]
    return "EE" if rng.random() < 0.5 else ["LW", bottom]


def seed_genome(rng, word, Q, probs, seed=0):
    word = parse_word(word)
    n = len(word)
    bottom, top = n, n + 1
    Y = [n + 2 + i for i in range(Q)]
    X = [n + 2 + Q + j for j in range(Q)]
    nx = 2 + 2 * Q
    g = design.new_genome(word, nx, default="R", seed=seed)
    m = n + nx
    rel = []
    for v in range(m):
        if v != bottom:
            rel.append((bottom, v))
        if v != top:
            rel.append((v, top))
    for y in Y:
        for x in X:
            rel.append((y, x))
    Fpos = [i for i in range(n) if word[i] == "F"]
    Epos = [i for i in range(n) if word[i] == "E"]
    for y in Y:
        if Fpos:
            rel.append((y, rng.choice(Fpos)))
    for x in X:
        if Epos:
            rel.append((rng.choice(Epos), x))
    cont = {}
    for i in range(n):
        for j in range(i + 1, n):
            if word[i] == word[j]:
                cont[design.pair_key(i, j)] = same_contact(rng, word[i], bottom, top)
            else:
                e, f = (i, j) if word[i] == "E" else (j, i)
                c = cross_contact(rng, probs, e, f, bottom, top)
                if c == "REL":
                    rel.append((f, e))
                else:
                    cont[design.pair_key(i, j)] = c
    g["rel"] = rel
    g["contact"] = cont
    return g


def mutate(rng, g, moves="crvtm"):
    mv = rng.choice(moves)
    if mv != "m":
        return sa_lb.mutate(rng, g, moves.replace("m", "") or "c")
    g = copy.deepcopy(g)
    word = g["word"]
    n = len(word)
    m = n + g["nx"]
    bottom, top = n, n + 1
    x, y = rng.sample(range(n), 2)
    key = design.pair_key(x, y)
    if word[x] == word[y]:
        g["contact"][key] = same_contact(rng, word[x], bottom, top)
        return g
    e, f = (x, y) if word[x] == "E" else (y, x)
    g["rel"] = [r for r in g["rel"] if tuple(r) != (f, e)]
    c = rng.choice("EFLUC")
    if c == "E":
        g["contact"][key] = "EE"
    elif c == "F":
        g["contact"][key] = "FF"
    elif c == "L" and bottom < m:
        g["contact"][key] = ["LW", bottom]
    elif c == "U" and top < m:
        g["contact"][key] = ["UW", top]
    else:
        g["rel"].append((f, e))
    return g


def log_line(f, s):
    print(s, flush=True)
    f.write(s + "\n")
    f.flush()


def cmd_sample(args):
    seed, K, Q, count = int(args[0]), args[1], int(args[2]), int(args[3])
    K = "E%dF%d" % (int(K), int(K)) if K.isdigit() else K
    probs = parse_probs(args[4]) if len(args) > 5 else parse_probs("E3F3L1U1C1")
    logp = args[-1]
    rng = random.Random(seed)
    os.makedirs(os.path.dirname(os.path.abspath(logp)), exist_ok=True)
    f = open(logp, "a", encoding="utf-8")
    log_line(f, "adv sample seed %d word %s Q %d count %d probs %s pid %d" % (seed, K, Q, count, probs, os.getpid()))
    hist = {}
    best = (-1, None)
    t0 = time.time()
    for it in range(count):
        g = seed_genome(rng, K, Q, probs, seed=rng.randrange(10 ** 6))
        I = design.build(g)
        if I is None:
            hist["invalid"] = hist.get("invalid", 0) + 1
            continue
        sc, info = (evaluate2 if OBJ == "2" else evaluate)(I)
        if sc is None:
            hist["no"] = hist.get("no", 0) + 1
            continue
        key = "cost%d" % info["cost"]
        hist[key] = hist.get(key, 0) + 1
        if sc > best[0]:
            best = (sc, g)
            design.save_genome(g, logp + ".best.json", dict(info))
            lbcore.dump(I, logp + ".best-inst.json", dict(cost=info["cost"], npairs=info["npairs"]))
            log_line(f, "  it %d new best score %.2f cost %d mean %.2f npairs %d m %d (%.0fs)" % (
                it, sc, info["cost"], info["mean"], info["npairs"], I.m, time.time() - t0))
    log_line(f, "SUMMARY %s (%.0fs)" % (json.dumps(hist, sort_keys=True), time.time() - t0))


def cmd_sa(args):
    seed, K, Q, seconds = int(args[0]), args[1], int(args[2]), float(args[3])
    K = "E%dF%d" % (int(K), int(K)) if K.isdigit() else K
    out = args[4]
    probs = parse_probs(args[5]) if len(args) > 5 and args[5] != "-" else parse_probs("E3F3L1U1C1")
    start = args[6] if len(args) > 6 and args[6] != "-" else None
    T0 = float(args[7]) if len(args) > 7 else 0.6
    rng = random.Random(seed)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    f = open(out + ".log", "a", encoding="utf-8")
    log_line(f, "adv sa seed %d word %s Q %d seconds %.0f probs %s start %s T0 %.2f pid %d" % (
        seed, K, Q, seconds, probs, start, T0, os.getpid()))
    t0 = time.time()
    if start:
        g = design.load_genome(start)
        I = design.build(g)
        sc, info = (evaluate2 if OBJ == "2" else evaluate)(I)
    else:
        best = (None, None, None)
        for _ in range(40):
            g1 = seed_genome(rng, K, Q, probs, seed=rng.randrange(10 ** 6))
            I1 = design.build(g1)
            if I1 is None:
                continue
            sc1, info1 = (evaluate2 if OBJ == "2" else evaluate)(I1)
            if sc1 is not None and (best[0] is None or sc1 > best[0]):
                best = (sc1, g1, info1)
        sc, g, info = best
    if sc is None:
        log_line(f, "no yes-instance in the start population")
        return
    cur, cur_sc = g, sc
    best_sc, best_info, best_g = sc, info, g
    log_line(f, "start score %.2f cost %d mean %.2f npairs %d" % (sc, info["cost"], info["mean"], info["npairs"]))
    it = 0
    while time.time() - t0 < seconds:
        it += 1
        T = T0 * max(0.05, 1 - (time.time() - t0) / seconds)
        g2 = mutate(rng, cur)
        I2 = design.build(g2)
        if I2 is None:
            continue
        try:
            sc2, info2 = (evaluate2 if OBJ == "2" else evaluate)(I2)
        except RuntimeError:
            continue
        if sc2 is None:
            continue
        if sc2 >= cur_sc or rng.random() < math.exp((sc2 - cur_sc) / T):
            cur, cur_sc = g2, sc2
            if sc2 > best_sc:
                best_sc, best_info, best_g = sc2, info2, g2
                design.save_genome(g2, out + "-best.json", dict(info2))
                lbcore.dump(I2, out + "-best-inst.json", dict(cost=info2["cost"], npairs=info2["npairs"]))
                log_line(f, "it %d new best score %.2f cost %d mean %.2f npairs %d m %d (%.0fs)" % (
                    it, sc2, info2["cost"], info2["mean"], info2["npairs"], I2.m, time.time() - t0))
        if it % 500 == 0:
            log_line(f, "  it %d cur %.2f best %.2f (cost %d) (%.0fs)" % (it, cur_sc, best_sc, best_info["cost"],
                                                                       time.time() - t0))
    log_line(f, "END best score %.2f cost %d mean %.2f npairs %d costs %s steps %d (%.0fs)" % (
        best_sc, best_info["cost"], best_info["mean"], best_info["npairs"], best_info["costs"][:12], it,
        time.time() - t0))


if __name__ == "__main__":
    if sys.argv[1] == "sample":
        cmd_sample(sys.argv[2:])
    else:
        cmd_sa(sys.argv[2:])
