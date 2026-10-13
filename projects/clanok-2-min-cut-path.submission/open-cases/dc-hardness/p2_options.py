"""Single-node P2 options of the SW encoding of small unsatisfiable formulas (dc-algorithm/sw_sat.encode, imported
read-only).  For every switch pair without a common bottom or top, list the additions of one node (a shared existing
bottom 'b', a shared existing top 't', a new private bottom 'nb', a new private top 'nt') that keep the answer 'no'.
Adding nodes is monotone (it can only connect more), so a pair with an empty list cannot be given P2 by any
completion of the encoding on the same switches.
Usage: python p2_options.py FORMULA [FORMULA ...]   (names from sw_sat.FORMULAS)"""
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dc-algorithm"))
sys.setrecursionlimit(100000)
import sw_sat  # noqa: E402
import sw2  # noqa: E402

for name in sys.argv[1:]:
    nv, cls = sw_sat.FORMULAS[name]
    inst, label = sw_sat.encode(nv, cls)
    print("formula", name, cls, "switches", len(inst[3]), "answer", sw_sat.answer(inst),
          "satisfiable", sw_sat.satisfiable(nv, cls))
    print(sw2.fmt(tuple(inst)))
    res = sw_sat.isolated_options(inst)
    empty = 0
    for (a, b), opts in sorted(res.items()):
        print("  pair", a, label[a], b, label[b], "options keeping 'no':", opts)
        empty += (not opts)
    print("  pairs without P2:", len(res), " pairs with no option:", empty, flush=True)
