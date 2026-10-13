"""Small helpers for two-choice hypergraph (2CH) instances: (N, E, F, s, t), E and F lists of node bit masks.
Conversion to ZZ (hunt2.ch_to_sw + zz.from_sw), brute force, P2 test, and a report line with exact / AC / PC
(full length L = largest odd number <= n of the ZZ form)."""
import os
import sys
import itertools
import time

sys.setrecursionlimit(100000)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import zz  # noqa: E402
import hunt2  # noqa: E402
import pcfast  # noqa: E402


class Builder:
    """Named nodes and switches."""

    def __init__(self):
        self.nodes = {}
        self.E, self.F, self.labels = [], [], []

    def node(self, name):
        if name not in self.nodes:
            self.nodes[name] = len(self.nodes)
        return self.nodes[name]

    def switch(self, label, Eset, Fset):
        self.E.append(sum(1 << self.node(x) for x in Eset))
        self.F.append(sum(1 << self.node(x) for x in Fset))
        self.labels.append(label)
        return len(self.E) - 1

    def add(self, i, side, name):
        if side == "E":
            self.E[i] |= 1 << self.node(name)
        else:
            self.F[i] |= 1 << self.node(name)

    def inst(self, s, t):
        return (len(self.nodes), list(self.E), list(self.F), self.node(s), self.node(t))


def to_zz(inst):
    return zz.from_sw(*hunt2.ch_to_sw(inst))


def connected(inst, modes):
    N, E, F, s, t = inst
    comp = 1 << s
    sides = [E[i] if m == 0 else F[i] for i, m in enumerate(modes)]
    changed = True
    while changed:
        changed = False
        for X in sides:
            if X & comp and X & ~comp:
                comp |= X
                changed = True
    return bool((comp >> t) & 1)


def brute(inst):
    n = len(inst[1])
    for modes in itertools.product((0, 1), repeat=n):
        if connected(inst, modes):
            return modes
    return None


def p2_bad(inst):
    N, E, F, s, t = inst
    n = len(E)
    return [(i, l) for i in range(n) for l in range(i + 1, n) if not (E[i] & E[l]) and not (F[i] & F[l])]


def report(name, inst, pc=True, L=None, brute_max=18):
    t0 = time.time()
    z = to_zz(inst)
    ex = zz.exact_dfs(z)[0]
    if len(inst[1]) <= brute_max:
        assert (brute(inst) is not None) == ex, "exact_dfs disagrees with brute force"
    ac = zz.ac_answer(z, L)
    p = pcfast.pc_answer(z, L) if (ac and pc) else (False if not ac else None)
    flag = "  <-- PC FALSE POSITIVE" if (p and not ex) else ""
    print("%-40s switches=%2d n=%3d |R|=%3d P2=%-5s exact=%-5s AC=%-5s PC=%-5s %6.1fs%s"
          % (name, len(inst[1]), z.n, len(z.R), not p2_bad(inst), ex, ac, p, time.time() - t0, flag), flush=True)
    return ex, ac, p
