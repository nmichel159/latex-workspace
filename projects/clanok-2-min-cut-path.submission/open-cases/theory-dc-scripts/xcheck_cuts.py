"""Cross-check of dctools.min_cut_sets against mcp.min_cuts_by_sets, and of the length claim, on the
examples of ex_long_path.py."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dctools as T, mcp
from ex_long_path import example10, family
for name, (n, E, u, v) in [("ex10", example10()), ("k2cl", family(2, True)), ("k3cl", family(3, True)), ("k4cl", family(4, True))]:
    g = T.gr(n, E)
    c1, A = T.min_cut_sets(g, u, v)
    masks1 = sorted(mcp.mask_of(T.cut_edges(g, a)) for a in A)
    if n <= 16:
        c2, masks2 = mcp.min_cuts_by_sets(g, u, v)
        same = (c1 == c2 and masks1 == masks2)
    else:
        same = "skipped"
    # all u-v paths of length 3 and whether one lies in a min cut (O3 test), independent of enumeration
    L3 = [vs for vs, es in mcp.simple_paths(g, u, v, maxlen=3) if len(es) == 3]
    ok3 = [p for p in L3 if T.path_in_some_min_cut(g, list(p), c1)]
    print(name, "n=%d c=%d #mincuts=%d agree=%s; length-3 paths=%d, in a min cut=%d; inDC=%s" % (n, c1, len(A), same, len(L3), len(ok3), mcp.in_dc(g)[0]))
