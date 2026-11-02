"""ex:zz-instance and tab:pa-exits: the numbers stated in the example of G_b, computed from the definitions, and the element counts of the table."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from graph_level import G, has_path  # noqa: E402
from zz_core import Inst, bits  # noqa: E402

names = "uvabst"
ix = {c: i for i, c in enumerate(names)}
edges = "ua us sb ab at tv bv av ub".split()
g = G(6, [(ix[e[0]], ix[e[1]]) for e in edges])
u, v = ix["u"], ix["v"]
c = g.cvalue(u, v)
assert c == 3
rest = [i for i in range(6) if i not in (u, v)]
subs = [0]
for b in rest:
    subs += [s | 1 << b for s in subs]
mins = sorted({s | 1 << u for s in subs if g.delta(s | 1 << u) == c}, key=lambda A: bin(A).count("1"))
show = ["".join(names[i] for i in bits(A)) for A in mins]
print("minimum sides", show)
assert {frozenset(x) for x in show} == {frozenset(x) for x in ["u", "us", "usb", "usba", "usbat"]}
Q = [u] + [x for x in range(6) if x != u and g.cvalue(u, x) >= 3]
print("Q", sorted(names[x] for x in Q))
assert sorted(names[x] for x in Q) == sorted("uabv")
idx = {x: i for i, x in enumerate(Q)}
up = [0] * len(Q)
for x in Q:
    for y in Q:
        if all((A >> x & 1) or not (A >> y & 1) for A in mins):
            up[idx[x]] |= 1 << idx[y]
Rl = []
for a, b in g.edges:
    if a in idx and b in idx:
        ab, ba = up[idx[a]] >> idx[b] & 1, up[idx[b]] >> idx[a] & 1
        assert ab != ba
        Rl.append((a, b) if ab else (b, a))
print("R", sorted(names[a] + names[b] for a, b in Rl))
assert sorted(names[a] + names[b] for a, b in Rl) == sorted(["ua", "ub", "ba", "av", "bv"])
I = Inst(len(Q), up, [(idx[a], idx[b]) for a, b in Rl], idx[u], idx[v], [names[x] for x in Q])
I.validate()
assert I.p2()
W = [idx[ix[c_]] for c_ in "uabv"]
assert I.is_valid_walk(W) and I.shortest_walk() is not None and len(I.shortest_walk()) == 4
D = (1 << idx[u]) | (1 << idx[ix["b"]])
assert I.is_downset(D) and I.connected_in_GD(D)
A = (1 << u) | (1 << ix["s"]) | (1 << ix["b"])
assert A in mins and [M for M in mins if sum(1 << idx[x] for x in Q if M >> x & 1) == D] == [A]
de = g.delta_edges(A)
print("delta(A)", sorted(names[a] + names[b] for a, b in de))
assert {frozenset((names[a], names[b])) for a, b in de} == {frozenset("ua"), frozenset("ab"), frozenset("bv")}
assert has_path(de, u, v)
# tab:pa-exits: x-roles + S + S'
table = dict(smallA=3, smallB=3, Fstar=4 + 12, Estar=4 + 12, few=4 + 12 + 4, ShapeA=6 + (12 + 7) + 6, ShapeB=8 + (12 + 4))
print(table)
assert table == dict(smallA=3, smallB=3, Fstar=16, Estar=16, few=20, ShapeA=31, ShapeB=24)
print("ex:zz-instance and tab:pa-exits: OK")
