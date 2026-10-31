"""Greedy shrinking of core instances on which HYB needs more than given parameters (agent r4-search).

Property P(I): P2, yes-instance (zz.exact_dfs), the core (Theorem R does not apply after propagation; optional), and
HYB fails with every parameter set of FAIL (default: (1, 0, 1, 3)); optionally also the level-2 portfolio fails.
Moves as in shrink.py (mode zz): delete one real edge, one element (not u, v), or one cover relation between classes.
Usage: python shrink_hyb.py SRC.jsonl|SRC.json INDEX SEED OUT.json [--fail 1,0,1,3;1,1,2,6] [--nocore] [--port]"""
import sys
import json
import random
import time
from common import zz, make_zz, from_json, to_json, save
from shrink import zz_moves, apply_zz
from hyb import analyse
from portfolio import portfolio


def prop(z, fail, need_core=True, port=False):
    if z.p2_bad():
        return False
    if not zz.exact_dfs(z)[0]:
        return False
    a = analyse(z, ladder=fail, with_thr=False)
    if a["prop_refutes"]:
        return False
    if need_core and not a["core"]:
        return False
    if a["hyb"] is not None:
        return False
    if port:
        r = portfolio(z, level=2, exact_ans=True)
        if not r["hard"]:
            return False
    return True


def main():
    src, index, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    fail = [(1, 0, 1, 3)]
    if "--fail" in sys.argv:
        s = sys.argv[sys.argv.index("--fail") + 1]
        fail = [tuple(int(x) for x in p.split(",")) for p in s.split(";")]
    need_core = "--nocore" not in sys.argv
    port = "--port" in sys.argv
    if src.endswith(".jsonl"):
        d = json.loads(open(src).readlines()[index])
    else:
        d = json.load(open(src))
    z, sw, names = from_json(d)
    rng = random.Random(seed)
    t0 = time.time()
    assert prop(z, fail, need_core, port), "start instance lacks the property"
    size = (z.n, len(z.R))
    print("start", size, flush=True)
    improved = True
    while improved:
        improved = False
        moves = zz_moves(z)
        rng.shuffle(moves)
        for m in moves:
            nxt = apply_zz(z, m)
            if nxt is None:
                continue
            ns = (nxt.n, len(nxt.R))
            if ns >= size:
                continue
            if prop(nxt, fail, need_core, port):
                z, size = nxt, ns
                improved = True
                print("[%.0fs] %s -> %s" % (time.time() - t0, m[0], size), flush=True)
                break
    a = analyse(z, all_params=True, with_ng=True)
    save(out, to_json(z, name=out.split("/")[-1][:-5], verdict=a,
                      notes="shrink_hyb.py from %s[%d] seed %d fail %s core %s port %s" % (src, index, seed, fail,
                                                                                         need_core, port)))
    print("final", size, a, flush=True)


if __name__ == "__main__":
    main()
