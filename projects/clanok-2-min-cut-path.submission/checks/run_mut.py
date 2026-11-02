"""Task B3: mutation test.  The constants and terms of the proof are changed one at a time (class Cfg); the harness must then report a failure on the
instances built for this purpose, and must report none on the same instances with the constants of the text (control).  Also the variants proposed by the
referee (margin 4, Shape A up to 4 classes), which must pass, and walks made non-shortest.

Usage: run_mut.py SEED ROUNDS LOG
"""
import os
import random
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from zz_core import ClaimFail, Inst, bits  # noqa: E402
from zz_design import BASES, zipper  # noqa: E402
from zz_proof import Cfg, Walk, construct  # noqa: E402
from run_planted import add_element, design_move  # noqa: E402


def far2_instance(rng):
    d = BASES["far2"](rng)
    I, P = d.build()
    g1, g2 = I.el[d.info["g"][0]], I.el[d.info["g"][1]]
    i = P.index(g1)
    chk_t = P[i + 1]
    # o above all elements except the two highs g_1, g_2 and the top class; common lower neighbour with them
    dnset = 0
    for x in range(I.m):
        if x not in (g1, g2) and not I.tied(x, I.v):
            dnset |= 1 << x
    up, m, o = add_element(I.UP, I.m, dnset, I.CL[I.v])
    edges = set(I.edges)
    edges.add((chk_t, o))
    J = Inst(m, up, edges, I.u, I.v)
    return J, P


def kappa_instance(rng):
    """base_kappa plus one off-walk element y below all lows of the zipper and incomparable with kappa_1 and kappa_4: y keeps the zipper outside EP(a_1), EP(a_2), so Shape B
    is reached, and every class of the zipper touches kappa_1, so only the term up A_kappa removes kappa_1 from the value."""
    d = BASES["kappa"](rng)
    I, P = d.build()
    upset = 0
    for pr in d.info["H"]:
        for z in pr:
            upset |= I.UP[I.el[z]]
    up, m, y = add_element(I.UP, I.m, I.CL[I.u], upset)
    names = list(I.names) + ["y"]
    edges = set(I.edges)
    edges.add((y, I.names.index("hubT")))
    edges.add((I.names.index("hubB"), y))
    return Inst(m, up, edges, I.u, I.v, names), P


def plain(base):
    def f(rng):
        return BASES[base](rng).build()
    return f


def climbed(base, moves=25):
    """A base with random accepted design moves."""
    def f(rng):
        d = BASES[base](rng)
        for _ in range(moves):
            d2 = d.copy()
            if design_move(d2, rng) == "none":
                continue
            I2, P2 = d2.build()
            if I2.p2() and I2.shortest_walk(bound=len(P2) - 1, budget=60000) is None:
                d = d2
        return d.build()
    return f


def nonshortest(rng):
    """A valid walk that is not shortest: random contacts are added until the solver finds a shorter walk."""
    d = BASES[rng.choice(["B", "stair", "cross", "mix"])](rng)
    for _ in range(200):
        d2 = d.copy()
        if design_move(d2, rng) == "none":
            continue
        I2, P2 = d2.build()
        if not I2.p2():
            continue
        if I2.shortest_walk(bound=len(P2) - 1, budget=60000) is not None:
            return I2, P2
        d = d2
    return d.build()


MUTS = [
    ("control: text", Cfg, ["margin2", "kappay", "far2x", "A", "cross", "stair", "B", "mix", "two"]),
    ("margin 6 -> 2", lambda: Cfg(margin=2), ["margin2"]),
    ("margin 6 -> 4 (referee: must pass)", lambda: Cfg(margin=4), ["margin2", "kappay", "far2x", "A", "cross", "stair", "B", "mix", "ties", "two"]),
    ("margin 4 and five classes in Shape B (referee: must pass)", lambda: Cfg(margin=4, shape_a_max=4), ["kappay", "A", "cross", "stair", "B", "mix", "ties"]),
    ("far pair among the first 2, distance 2", lambda: Cfg(first=2), ["far2x"]),
    ("lem:pa-atoms at distance 2", lambda: Cfg(atom_far=2), ["far2x"]),
    ("drop up A_kappa", lambda: Cfg(use_Akappa=False), ["kappay"]),
    ("drop the EP term of F^1", lambda: Cfg(use_EP=False), ["A"]),
    ("drop the pair h_3, h_4", lambda: Cfg(use_second_pair=False), ["cross"]),
    ("bound of lem:pa-one 4 -> 2", lambda: Cfg(one_bound=2), ["two"]),
    ("bound of lem:pa-two 8 -> 6", lambda: Cfg(two_bound=6), ["two"]),
]


def get_inst(name, rng):
    if name == "far2x":
        return far2_instance(rng)
    if name == "kappay":
        return kappa_instance(rng)
    if name == "two":
        return plain("two")(rng)
    if name in ("A", "cross", "stair", "B", "mix", "ties", "margin2"):
        if name == "margin2":
            return plain(name)(rng)
        return climbed(name, moves=8)(rng) if rng.random() < 0.5 else plain(name)(rng)
    raise ValueError(name)


def main():
    seed, rounds, logf = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    rng = random.Random(seed)
    out = []
    t0 = time.time()
    # the pool of instances, verified once
    pool = {}
    names = {n for _, _, fam in MUTS for n in fam}
    st0 = Counter()
    for n in sorted(names):
        lst = []
        for _ in range(rounds):
            I, P = get_inst(n, rng)
            I.validate()
            if not I.p2():
                st0["%s: P2 fails (dropped)" % n] += 1
                continue
            if I.shortest_walk(bound=len(P) - 1, budget=200000) is not None:
                st0["%s: P not shortest (dropped)" % n] += 1
                continue
            lst.append((I, P))
        pool[n] = lst
        out.append("pool %s: %d instances" % (n, len(lst)))
    for k, v in sorted(st0.items()):
        out.append("%s %d" % (k, v))
    for label, mk, fams in MUTS:
        cfg = mk()
        fired = Counter()
        runs = 0
        exits = Counter()
        st = Counter()
        for fam in fams:
            for I, P in pool[fam]:
                J = I.reversed_instance()
                for K, Q in ((I, P), (I, P[::-1]), (J, P), (J, P[::-1])):
                    for _ in range(3):
                        runs += 1
                        try:
                            exits[construct(Walk(K, Q), cfg, rng, st)] += 1
                        except ClaimFail as e:
                            fired[str(e)] += 1
        out.append("MUTATION %s: runs %d, fired %d" % (label, runs, sum(fired.values())))
        out.append("   exits %s" % dict(exits))
        for k, v in fired.most_common(6):
            out.append("   %5d  %s" % (v, k))
        out.append("   two max sum %d, one(a) max span %d, one(b) max span %d, two tested %d" % (
            st["two max sum"], st["one(a) max span"], st["one(b) max span"], st["two tested"]))
        print(out[-1], flush=True)
    # walks made non-shortest
    st = Counter()
    fired = Counter()
    n = 0
    cfg = Cfg()
    for _ in range(rounds * 4):
        I, P = nonshortest(rng)
        if I.shortest_walk(bound=len(P) - 1, budget=200000) is None:
            continue
        n += 1
        try:
            construct(Walk(I, P), cfg, rng, st)
            fired["no assertion fired"] += 1
        except ClaimFail as e:
            fired[str(e)] += 1
    out.append("MUTATION walk not shortest: %d instances" % n)
    for k, v in fired.most_common(8):
        out.append("   %5d  %s" % (v, k))
    out.append("time %.1f" % (time.time() - t0))
    with open(logf, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
