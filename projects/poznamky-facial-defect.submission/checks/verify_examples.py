"""Checks the example graphs of the note with the Python implementation (planemap.py).

Each example is a rotation system sigma (edge i has the darts 2i, 2i+1; sigma[d] is the next dart around the
origin of d). For every example the script prints the graph and decides the listed colourings.
"""
import json, sys
from planemap import PlaneMap, edge_constraints, vertex_constraints, solve

EXAMPLES = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "examples.json", encoding="utf-8"))


def total_constraints(g, variant):
    """Type-wise total colouring: vertex runs, edge runs (shifted by nv), incident elements differ."""
    vr = vertex_constraints(g)
    er = edge_constraints(g, variant)
    nv = g.nv
    forb = {}
    for k in (2, 3, 4):
        forb[k] = set(vr.get(k, ())) | {tuple(x + nv for x in t) for t in er.get(k, ())}
    vert = g.vertices()
    inc = set()
    for e in range(g.m):
        for v in {vert[2 * e], vert[2 * e + 1]}:
            inc.add((v, nv + e))
    return forb, inc


def total_colorable(g, defects, variant):
    forb, inc = total_constraints(g, variant)
    # incidences must differ in every colour: add them as 2-tuples for all colours by a second solve layer
    ncol = len(defects)
    # encode: colour c with defect d forbids constant (d+1)-tuples; incidences forbid constant pairs for all colours.
    # solve() takes one dict per defect size, so merge the pairs into forb[2] only for defect-1 colours and
    # check the remaining colours by enumeration of solutions is too slow; instead split the colours:
    from planemap import solve as _s
    cons_pairs = inc
    # build explicit constraint list through a small local solver
    cons = []
    for c in range(ncol):
        for t in forb.get(defects[c] + 1, ()):
            cons.append((c, t))
        for t in cons_pairs:
            cons.append((c, t))
    nvars = g.nv + g.m
    col = [-1] * nvars
    by_var = [[] for _ in range(nvars)]
    for i, (c, t) in enumerate(cons):
        for v in t:
            by_var[v].append(i)

    def ok(v):
        for i in by_var[v]:
            c, t = cons[i]
            if all(col[w] == c for w in t):
                return False
        return True

    order = sorted(range(nvars), key=lambda v: -len(by_var[v]))

    def rec(i):
        if i == nvars:
            return True
        v = order[i]
        for c in range(ncol):
            col[v] = c
            if ok(v) and rec(i + 1):
                return True
        col[v] = -1
        return False

    return rec(0)


for ex in EXAMPLES:
    g = PlaneMap(ex["sigma"])
    assert g.genus_ok(), "not a plane map"
    deg = sorted(g.degrees())
    fl = sorted(len(w) for w in g.faces())
    print(f"{ex['name']}: n={g.nv} m={g.m} simple={g.is_simple()} degrees={deg} face lengths={fl}")
    for claim in ex["claims"]:
        kind, defects, variant, expected = claim
        if kind == "E":
            r = solve(g.m, edge_constraints(g, variant), defects) is not None
        elif kind == "V":
            r = solve(g.nv, vertex_constraints(g), defects) is not None
        else:
            r = total_colorable(g, defects, variant)
        flag = "ok" if r == expected else "MISMATCH"
        print(f"   {kind}{defects} {variant or ''}: {'colourable' if r else 'NOT colourable'}  [{flag}]")
