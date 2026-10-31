"""Cross-check (named as such): reviewer's Y^d_k against the author's r5-core/fool.yd (imported read-only), and the
author's propagation r4-general/gsw.refutes/prune (read-only) applied to the reviewer's instances.

usage: python cross_d.py KMAX
"""
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
OC = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.append(os.path.join(OC, "r5-core"))
sys.path.append(os.path.join(OC, "r4-general"))
from fams import yfam                       # noqa: E402
from sw import prune as my_prune, bits      # noqa: E402
import fool                                  # noqa: E402  (author, read-only)
import gsw                                   # noqa: E402  (author, read-only)


class Adapter:
    def __init__(self, G):
        self.m = G.m
        self.E, self.F, self.s, self.t = G.E, G.F, G.s, G.t
        self.le = [[G.leq(a, b) for b in range(G.m)] for a in range(G.m)]
        self.sides = [i for i in range(2 * G.m) if G.side[i]]


def signature(E, F, m):
    return sorted((bin(E[w]).count("1"), bin(F[w]).count("1")) for w in range(m))


def main(KMAX):
    for k in range(2, KMAX + 1):
        for contact in (False, True):
            for back in (False, True):
                G = yfam(k, contact=contact, d=True, back=back)
                A, nodes = fool.yd(k, back=back, contact=contact)
                sigA = signature(A.E, A.F, A.m)
                sigG = signature(G.E, G.F, G.m)
                # node-degree signature: how many sides contain each node
                def degs(E, F, m, N):
                    c = [0] * N
                    for w in range(m):
                        for x in bits(E[w]):
                            c[x] += 1
                        for x in bits(F[w]):
                            c[x] += 1
                    return sorted(c)
                same = (sigA == sigG and A.N == G.N and degs(A.E, A.F, A.m, A.N) == degs(G.E, G.F, G.m, G.N))
                fx_author, dead = gsw.prune(Adapter(G))
                fx_mine = my_prune(G)
                print("k=%d contact=%s back=%s: same size signatures as fool.yd: %s; author's gsw.prune on reviewer's "
                      "instance fixes %s; reviewer's prune fixes %s" % (
                          k, contact, back, same,
                          sorted("%s:%s" % (G.names[w], "EF"[mo]) for w, mo in fx_author.items()),
                          sorted("%s:%s" % (G.names[w], mo) for w, mo in fx_mine.items())), flush=True)


if __name__ == "__main__":
    main(int(sys.argv[1]))
