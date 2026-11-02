"""Run CL2 on the saved no-instances on which SAC passes.  Usage: t_found.py FILE [limit]"""
import json
import sys
import time

from wd import Inst
from closure import Graph, Refuted, sac
from closure2 import cl2_pass


def load(d):
    return Inst(d["m"], [int(x, 16) for x in d["up"]], [tuple(e) for e in d["edges"]], d["u"], d["v"])


def main():
    data = json.load(open(sys.argv[1]))
    lim = int(sys.argv[2]) if len(sys.argv) > 2 else len(data)
    for d in data[:lim]:
        I = load(d)
        ex = I.shortest_walk(budget=300000)
        G = Graph(I)
        try:
            sac(G, I.ALL, I.ALL)
            s = "pass"
        except Refuted:
            s = "REF"
        t0 = time.time()
        p, c = cl2_pass(I)
        print(d.get("fam"), "m", I.m, "p2", I.p2(), "exact", ex is not None, "sac", s, "cl2", "pass" if p else "REF", dict(c.stats), "t=%.1f" % (time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
