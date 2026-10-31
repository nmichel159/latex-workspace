"""Hill climbing on ZZ + P2 instances (dc-algorithm.md Section 11.6).

Usage: python hunt_mixed.py SEED STEPS GOAL [MAXMID] [ANTICHAIN]
GOAL 'fplus': P2 with lower witnesses only; score = largest number of minimal peak classes over the globally shortest
      zigzags found (Theorem F+ says <= 2) plus a bonus for the least lower generator number; a score >= 3 on
      either count is a counterexample and is printed.
GOAL 'both': P2 with witnesses of random direction; only yes-instances are kept; score = min(kl, ku), where kl (ku)
      is the least k <= 3 for which the k-guess on the low (up) side finds a solution (4 if none); instances with
      score >= 3 (every guess of at most two generators fails on both sides) are written to
      runs/hunt-mixed-SEED.jsonl; smaller instances are preferred at equal score.
ANTICHAIN = 1 keeps the middle elements pairwise incomparable (switch model).
Instance state: nb elements ~ u, nt elements ~ v, middle elements with a generating relation `gens`, real edges R.
"""
import sys
import json
import random
import zz
import mixed as mx


def build(st):
    nb, nm, nt, gens, R = st["nb"], st["nm"], st["nt"], st["gens"], st["R"]
    n = nb + nm + nt
    le = [[a == b for b in range(n)] for a in range(n)]
    for a, b in gens:
        le[a][b] = True
    for b in range(nb):
        for x in range(n):
            le[b][x] = True
    for t in range(nb + nm, n):
        for x in range(n):
            le[x][t] = True
    for k in range(n):
        for i in range(n):
            if le[i][k]:
                for j in range(n):
                    if le[k][j]:
                        le[i][j] = True
    u, v = 0, n - 1
    Rs = set()
    for a, b in R:
        if a < n and b < n and le[b][a] and not le[a][b]:
            a, b = b, a
        if a < n and b < n and le[a][b] and not le[b][a] and (a, b) != (u, v):
            Rs.add((a, b))
    return n, le, Rs


def repair(rng, st, mode):
    n, le, R = build(st)
    R = mx.p2_complete_dir(rng, n, le, R, mode, 0, n - 1)
    st["R"] = sorted(R)
    return zz.ZZ(n, None, sorted(R), 0, n - 1, le=le)


def insert_at(st, x):
    """make room for a new element at index x (indices >= x shift by one)."""
    def sh(i):
        return i + 1 if i >= x else i
    st["gens"] = [(sh(a), sh(b)) for a, b in st["gens"]]
    st["R"] = [(sh(a), sh(b)) for a, b in st["R"]]
    return st


def delete_at(st, x):
    def sh(i):
        return i - 1 if i > x else i
    st["gens"] = [(sh(a), sh(b)) for a, b in st["gens"] if x not in (a, b)]
    st["R"] = [(sh(a), sh(b)) for a, b in st["R"] if x not in (a, b)]
    return st


def mutate(rng, st, maxmid, antichain):
    st = {k: (list(v) if isinstance(v, list) else v) for k, v in st.items()}
    nb, nm, nt = st["nb"], st["nm"], st["nt"]
    n = nb + nm + nt
    M = list(range(nb, nb + nm))
    r = rng.random()
    if r < 0.45:
        _, le, _ = build(st)
        strict = [(a, b) for a in range(n) for b in range(n) if le[a][b] and not le[b][a] and (a, b) != (0, n - 1)]
        e = rng.choice(strict)
        R = set(map(tuple, st["R"]))
        R ^= {e}
        st["R"] = sorted(R)
    elif r < 0.6 and not antichain and nm >= 2:
        a, b = rng.sample(M, 2)
        g = set(map(tuple, st["gens"]))
        g ^= {(a, b)}
        st["gens"] = sorted(g)
    elif r < 0.75 and nm < maxmid:
        x = nb + nm
        st = insert_at(st, x)
        st["nm"] = nm + 1
        n += 1
        if not antichain:
            for y in M:
                if rng.random() < 0.15:
                    st["gens"].append((y, x) if rng.random() < 0.5 else (x, y))
        for y in range(n):
            if y != x and rng.random() < 0.25:
                st["R"].append((min(x, y), max(x, y)))
    elif r < 0.9 and nm > 2:
        x = rng.choice(M)
        st = delete_at(st, x)
        st["nm"] = nm - 1
    elif rng.random() < 0.5:
        if nb < 3 and (nb == 1 or rng.random() < 0.5):
            st = insert_at(st, nb)
            st["nb"] = nb + 1
        elif nb >= 2:
            st = delete_at(st, nb - 1)
            st["nb"] = nb - 1
    else:
        if nt < 3 and (nt == 1 or rng.random() < 0.5):
            st = insert_at(st, n - 1)
            st["nt"] = nt + 1
        elif nt >= 2:
            st = delete_at(st, n - 2)
            st["nt"] = nt - 1
    return st


def score_fplus(z):
    I = mx.Info(z)
    sols = mx.solutions(z, I)
    if not sols:
        return -1, None
    _, short = mx.globally_shortest(z, I, sols)
    mp = max(mx.minimal_peak_classes(I, p)[0] for _, p in short)
    gl = min(mx.g_low(I, D) for D, _ in sols)
    return max(mp, gl) + 0.1 * len(short) / (1 + len(short)), (mp, gl)


def least_k(z, side, kmax=3):
    I = mx.Info(z)
    f = mx.guess_low if side == "low" else mx.guess_up
    for k in range(kmax + 1):
        if f(z, k, I) is not None:
            return k
    return kmax + 1


def score_both(z):
    if not zz.exact_dfs(z)[0]:
        return -1, None
    kl = least_k(z, "low")
    ku = least_k(z, "up")
    return min(kl, ku) - 0.01 * z.n, (kl, ku)


def main():
    seed, steps, goal = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    maxmid = int(sys.argv[4]) if len(sys.argv) > 4 else 12
    antichain = len(sys.argv) > 5 and sys.argv[5] == "1"
    rng = random.Random(seed)
    mode = "low" if goal == "fplus" else "mixed"
    scorer = score_fplus if goal == "fplus" else score_both
    out = open(f"runs/hunt-mixed-{goal}-{seed}.jsonl", "w")
    best_record = {}
    while True:
        nm0 = rng.randint(4, maxmid)
        gens0 = [] if antichain else [(a, b) for a in range(2, 2 + nm0) for b in range(2, 2 + nm0)
                                      if a < b and rng.random() < 0.15]
        st = {"nb": 2, "nm": nm0, "nt": 2, "gens": gens0, "R": []}
        n0, le0, _ = build(st)
        st["R"] = [(a, b) for a in range(n0) for b in range(n0)
                   if le0[a][b] and not le0[b][a] and (a, b) != (0, n0 - 1) and rng.random() < 0.3]
        z = repair(rng, st, mode)
        s, det = scorer(z)
        if s >= 0:
            break
    cur, cur_s = st, s
    for step in range(steps):
        st2 = mutate(rng, cur, maxmid, antichain)
        z2 = repair(rng, st2, mode)
        s2, det2 = scorer(z2)
        if s2 < 0:
            continue
        if s2 >= cur_s or rng.random() < 0.03:
            cur, cur_s = st2, s2
            key = int(s2 + 0.5) if goal == "both" else int(s2)
            if goal == "fplus" and det2 and (det2[0] > 2 or det2[1] > 2):
                print("FPLUS COUNTEREXAMPLE", det2, json.dumps(mx.to_json(z2)), flush=True)
            if goal == "both" and det2 and min(det2) >= 3:
                rec = best_record.get(min(det2))
                if rec is None or z2.n < rec:
                    best_record[min(det2)] = z2.n
                    out.write(json.dumps({"det": det2, "n": z2.n, "z": mx.to_json(z2)}) + "\n")
                    out.flush()
                    print("BOTH>=3", step, det2, "n =", z2.n, flush=True)
        if step % 500 == 0:
            print("step", step, "score", round(cur_s, 3), "nm", cur["nm"], "best", best_record, flush=True)
    print("done", seed, goal, "best", best_record, flush=True)


if __name__ == "__main__":
    main()
