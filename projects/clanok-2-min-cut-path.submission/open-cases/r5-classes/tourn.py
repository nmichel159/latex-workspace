"""Random mate tournaments on a planted base path (agent r5-classes, third run).

Base: a planted switch-model path read from a hunt log (``top:`` line) or built by plant.base_word.  For every class
of P, M dead mates (deadmates.add_dead, floating: no window); between a dead T-mate and a dead O-mate the P2 pair is
chosen at random (O-sides meet: the O-mate covers the T-mate for the T-certificate; T-sides meet: the T-mate covers
the O-mate for the O-certificate).  Reports P2, shortest, number of solutions, the guided DESC costs and the least
number of usable-side centres of Theorem Q for each type.

usage: python tourn.py BASE M SEED   (BASE = hunt log file or a word like EEEEFFFF)
"""
import ast
import random
import sys
import ccore as C
import plant
import deadmates
import fastdesc
import test_q


def load_base(src):
    if all(ch in "EF" for ch in src):
        return plant.base_word(src, None, forward=True)
    txt = open(src).read()
    obj = ast.literal_eval(txt.split("top:")[1].strip())
    typ, links = obj[1], obj[-1]
    cls = obj[2] if len(obj) == 4 else list(range(len(typ)))
    pl = plant.Planted(typ, cls)
    for L in links:
        pl.links.add(tuple(L))
    return pl


def build(src, M, seed):
    rng = random.Random(seed)
    pl = load_base(src)
    for a in range(pl.r):
        for _ in range(M):
            deadmates.add_dead(pl, a)
    deadmates.finish(pl, rng)
    return pl


if __name__ == "__main__":
    src = sys.argv[1]
    M = int(sys.argv[2])
    seed = int(sys.argv[3])
    pl = build(src, M, seed)
    I, P = pl.realise()
    print("P2", C.p2_ok(I), "shortest", pl.shortest_ok(I, P), "classes", I.k, "switches", I.n, "sides",
          len(I.sides), flush=True)
    pr = fastdesc.Prep(I, P)
    for f, g in ((1, 0), (1, 1), (2, 0)) if len(I.sides) > 120 else ((1, 0), (1, 1), (2, 0), (2, 1), (3, 0)):
        print(" guided", f, g, pr.guided(f, g, want=True), flush=True)
    # least numbers of usable-side centres (Theorem Q certificate) per type
    pt = {I.scls[x]: x & 1 for x in P}
    for T in (0, 1):
        O = 1 - T
        Tsw = [w for w in range(I.n) if pt.get(I.cl[w]) == T]
        Osw = [v for v in range(I.n) if pt.get(I.cl[v]) == O]
        needA = [2 * w + O for w in Tsw if I.sw[w][O]]
        centA = [2 * v + O for v in Osw if I.sw[v][O]]
        needB = [2 * v + T for v in Osw if I.sw[v][T]]
        centB = [2 * w + T for w in Tsw if I.sw[w][T]]
        print(" T=%s cover-from-O-usable %s  cover-from-T-usable %s" % (
            "EF"[T], test_q.min_cover(I, needA, centA)[0], test_q.min_cover(I, needB, centB)[0]), flush=True)
    if I.k <= 16:
        import cdesc2
        sols = cdesc2.solutions_masks(I)
        print(" solutions", len(sols), "exact desc(1,1)", cdesc2.desc_cost(I, 1, 1, sols),
              "exact desc(2,0)", cdesc2.desc_cost(I, 2, 0, sols), flush=True)
