"""2CH + P2 (= SW + P2) and TIC as special cases of ZZ + P2 and of the open case of DC (agent verify-LTH).

Part 1: random 2CH instances (with and without P2) -> SW form -> ZZ (own conversion): the preorder is valid, R joins
strictly comparable elements, P2 of ZZ <=> P2 of 2CH, ZZ answer (own DFS for a consistent zigzag) = 2CH brute force.
Part 2: small instances realised as graphs by theory-dc.md Theorem 13(b) (M = 1); in the graph: c(u,v) = number of
strict pairs, d(u,v) = 2, DC membership, and "some minimum u-v cut contains a u-v path" (every u-v path of (Q, R)
of odd length tested by theory-dc.md Lemma 6 with networkx max-flow) = 2CH answer.
Usage: python test_zz.py <seed> <count part 1> <count part 2>
"""
import sys
import random
import itertools
import networkx as nx

sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
from core import *


def realise(zz, M=1):
    G = nx.Graph()
    q = zz.q
    G.add_nodes_from(range(q))
    nxt = [q]

    def ear(a, b):
        e = nxt[0]; nxt[0] += 1
        G.add_edge(a, e); G.add_edge(e, b)

    Nst = 0
    for a in range(q):
        for b in range(q):
            if a != b and zz.lt(a, b):
                Nst += 1
                if frozenset((a, b)) in zz.R:
                    G.add_edge(a, b)
                else:
                    ear(a, b)
                if a != zz.u:
                    ear(zz.u, a)
                if b != zz.v:
                    ear(b, zz.v)
    for a in range(q):
        for b in range(a + 1, q):
            if zz.leq[a][b] and zz.leq[b][a]:
                for _ in range(M):
                    ear(a, b)
    return G, Nst


def flow_value(G, sources, sinks):
    D = nx.DiGraph()
    for a, b in G.edges():
        D.add_edge(a, b, capacity=1)
        D.add_edge(b, a, capacity=1)
    S, T = "S*", "T*"
    for x in sources:
        D.add_edge(S, x, capacity=10 ** 9)
    for y in sinks:
        D.add_edge(y, T, capacity=10 ** 9)
    return nx.maximum_flow_value(D, S, T)


def pimc_graph(G, zz, c):
    RG = nx.Graph()
    RG.add_nodes_from(range(zz.q))
    for e in zz.R:
        a, b = tuple(e)
        RG.add_edge(a, b)
    for path in nx.all_simple_paths(RG, zz.u, zz.v):
        L = len(path) - 1
        if L % 2 == 0:
            continue
        ev = path[0::2]
        od = path[1::2]
        if flow_value(G, ev, od) == c:
            return True, path
    return False, None


def in_dc(G):
    T = nx.gomory_hu_tree(nx.Graph([(a, b, {"capacity": 1}) for a, b in G.edges()]))
    dist = dict(nx.all_pairs_shortest_path_length(G))
    nodes = list(G.nodes())
    for i, x in enumerate(nodes):
        for y in nodes[i + 1:]:
            if dist[x][y] <= 2:
                continue
            path = nx.shortest_path(T, x, y)
            c = min(T[path[k]][path[k + 1]]["weight"] for k in range(len(path) - 1))
            if c > 2:
                return False
    return True


if __name__ == "__main__":
    seed, c1, c2 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    st = {"inst": 0, "p2": 0, "yes": 0, "viol": 0}
    for it in range(c1):
        N = rng.randint(2, 6); n = rng.randint(1, 6)
        inst = rand_2ch(rng, N, n, dens=rng.choice([0.2, 0.35, 0.5]), p_empty=0.15, p2=rng.random() < 0.7,
                        s=0, t=N - 1)
        zz = twoch_to_zz(inst)
        zz.check_instance()
        a = brute_2ch(inst)[0]
        z = zz.solve()
        p = p2_2ch(inst)
        st["inst"] += 1; st["p2"] += p; st["yes"] += a
        if a != z or p != zz.p2():
            st["viol"] += 1
            print("VIOLATION part 1", inst, a, z, p, zz.p2())
    print("part 1:", st, flush=True)
    st2 = {"inst": 0, "yes": 0, "viol": 0, "maxV": 0}
    for it in range(c2):
        N = rng.randint(2, 3); n = rng.randint(1, 3)
        inst = rand_2ch(rng, N, n, dens=0.4, p_empty=0.1, p2=True, s=0, t=N - 1)
        zz = twoch_to_zz(inst)
        G, Nst = realise(zz)
        st2["maxV"] = max(st2["maxV"], G.number_of_nodes())
        c = flow_value(G, [zz.u], [zz.v])
        d = nx.shortest_path_length(G, zz.u, zz.v)
        dc = in_dc(G)
        pim, path = pimc_graph(G, zz, c)
        a = brute_2ch(inst)[0]
        st2["inst"] += 1; st2["yes"] += a
        if c != Nst or d != 2 or not dc or pim != a:
            st2["viol"] += 1
            print("VIOLATION part 2", inst, "c", c, Nst, "d", d, "dc", dc, "pimc", pim, "2ch", a, flush=True)
    print("part 2:", st2, flush=True)
    print("violations:", st["viol"] + st2["viol"])
