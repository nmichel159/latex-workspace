"""Greedy shrinking of a PC false positive: repeatedly delete one real edge or one middle element (not u, v) while
the instance keeps P2, stays a no-instance, and PC (L = largest odd <= n) still says yes.
Usage: python shrink_pcfp.py IN.json OUT.json SEED"""
import sys
import json
import random
import zz
import pcfast


def make(n, le, R, u, v):
    return zz.ZZ(n, None, R, u, v, le=le)


def ok(z):
    if z.p2_bad():
        return False
    if zz.exact_dfs(z)[0]:
        return False
    return zz.ac_answer(z) and pcfast.pc_answer(z)


def delete_element(n, le, R, u, v, x):
    keep = [y for y in range(n) if y != x]
    pos = {y: i for i, y in enumerate(keep)}
    le2 = [[le[a][b] for b in keep] for a in keep]
    R2 = [(pos[a], pos[b]) for a, b in R if a != x and b != x]
    return len(keep), le2, R2, pos[u], pos[v]


if __name__ == "__main__":
    d = json.load(open(sys.argv[1]))
    rng = random.Random(int(sys.argv[3]))
    n, u, v = d["n"], d["u"], d["v"]
    le = [[bool(x) for x in r] for r in d["le"]]
    R = [tuple(e) for e in d["R"]]
    assert ok(make(n, le, R, u, v))
    improved = True
    while improved:
        improved = False
        moves = [("e", e) for e in R] + [("x", x) for x in range(n) if x not in (u, v)]
        rng.shuffle(moves)
        for kind, w in moves:
            if kind == "e":
                R2 = [e for e in R if e != w]
                if ok(make(n, le, R2, u, v)):
                    R = R2
                    improved = True
                    print("deleted edge", w, "-> n", n, "|R|", len(R), flush=True)
                    break
            else:
                cand = delete_element(n, le, R, u, v, w)
                if ok(make(*cand)):
                    n, le, R, u, v = cand
                    improved = True
                    print("deleted element", w, "-> n", n, "|R|", len(R), flush=True)
                    break
    z = make(n, le, R, u, v)
    print("final n", n, "|R|", len(z.R))
    json.dump({"n": n, "le": [[int(x) for x in r] for r in le], "R": z.R, "u": u, "v": v,
               "source": "shrink_pcfp.py from %s, seed %s" % (sys.argv[1], sys.argv[3])}, open(sys.argv[2], "w"))
