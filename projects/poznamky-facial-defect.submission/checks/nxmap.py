"""Conversion of networkx planar embeddings to PlaneMap, and some graph families."""
import random
import networkx as nx
from planemap import PlaneMap


def from_embedding(emb):
    """PlaneMap of a networkx PlanarEmbedding (simple graph). Returns (map, edge list)."""
    edges = []
    dart = {}
    for u, v in emb.edges():
        if (u, v) in dart:
            continue
        i = len(edges)
        edges.append((u, v))
        dart[(u, v)] = 2 * i
        dart[(v, u)] = 2 * i + 1
    sigma = [0] * (2 * len(edges))
    for v in emb.nodes():
        nb = list(emb.neighbors_cw_order(v))
        for i, w in enumerate(nb):
            sigma[dart[(v, w)]] = dart[(v, nb[(i + 1) % len(nb)])]
    return PlaneMap(sigma), edges


def from_graph(G):
    ok, emb = nx.check_planarity(G)
    if not ok:
        return None, None
    return from_embedding(emb)


def from_rotation(rot):
    """rot: dict v -> list of neighbours in cyclic order (simple graph)."""
    edges = []
    dart = {}
    for v, nb in rot.items():
        for w in nb:
            if (v, w) not in dart:
                i = len(edges)
                edges.append((v, w))
                dart[(v, w)] = 2 * i
                dart[(w, v)] = 2 * i + 1
    sigma = [0] * (2 * len(edges))
    for v, nb in rot.items():
        for i, w in enumerate(nb):
            sigma[dart[(v, w)]] = dart[(v, nb[(i + 1) % len(nb)])]
    return PlaneMap(sigma), edges


def random_triangulation(n, rng):
    """Random plane triangulation by repeated vertex insertion into faces and edge flips."""
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (0, 2)])
    faces = [(0, 1, 2), (0, 2, 1)]
    for v in range(3, n):
        i = rng.randrange(len(faces))
        a, b, c = faces.pop(i)
        G.add_edges_from([(v, a), (v, b), (v, c)])
        faces += [(a, b, v), (b, c, v), (c, a, v)]
    return G


def random_planar(n, m, rng):
    """Random connected planar graph: random triangulation with edges removed down to m."""
    G = random_triangulation(n, rng)
    edges = list(G.edges())
    rng.shuffle(edges)
    for e in edges:
        if G.number_of_edges() <= m:
            break
        G.remove_edge(*e)
        if not nx.is_connected(G):
            G.add_edge(*e)
    return G
