"""Generators of 2CH + P2 instances with a planted path (agent r4-switch).

planted(word, rng, ...): positions 1..L with types word[k-1] in {'E','F'}; path side h_k of that type, partner
(flip) side Fl_k of the other type; nodes s in h_1, t in h_L, y_k in h_k & h_{k+1}.  P2 is completed pair by pair:
  same type, far:      a private node in Fl_p & Fl_q            ('w')
  opposite types:      a private node in Fl_p & h_q (forward contact of Fl_p, p < q)  or
                       a private node in h_p & Fl_q (backward contact of Fl_q)       chosen by `orient`
  adjacent same type:  satisfied by y_p.
Optional extra contacts: private nodes in Fl_p & h_q (forward, q > p + 1) with probability pfwd, and in
h_p & Fl_q (backward, p < q - 1) with probability pbwd.
orient(p, q) returns 'f' or 'b' for opposite-type pairs p < q.
The planted path is h_1 .. h_L; whether it is the unique solution is checked by the caller.
"""
import random


def planted(word, rng=None, orient=None, pfwd=0.0, pbwd=0.0, fwd_only=None, bwd_only=None, extra=None):
    L = len(word)
    nodes = {}

    def node(name):
        if name not in nodes:
            nodes[name] = len(nodes)
        return nodes[name]

    path = [0] * (L + 1)
    flip = [0] * (L + 1)
    s = node("s")
    t = node("t")
    path[1] |= 1 << s
    path[L] |= 1 << t
    for k in range(1, L):
        y = node(("y", k))
        path[k] |= 1 << y
        path[k + 1] |= 1 << y
    for p in range(1, L + 1):
        for q in range(p + 1, L + 1):
            same = word[p - 1] == word[q - 1]
            if same:
                if q == p + 1:
                    continue
                w = node(("w", p, q))
                flip[p] |= 1 << w
                flip[q] |= 1 << w
            else:
                o = orient(p, q) if orient else "f"
                if o == "f":
                    z = node(("z", p, q))
                    flip[p] |= 1 << z
                    path[q] |= 1 << z
                else:
                    z = node(("zb", p, q))
                    path[p] |= 1 << z
                    flip[q] |= 1 << z
    if rng is not None:
        for p in range(1, L + 1):
            for q in range(p + 2, L + 1):
                if pfwd and rng.random() < pfwd:
                    z = node(("xf", p, q))
                    flip[p] |= 1 << z
                    path[q] |= 1 << z
                if pbwd and rng.random() < pbwd:
                    z = node(("xb", p, q))
                    path[p] |= 1 << z
                    flip[q] |= 1 << z
    if extra:
        for (kind, p, q) in extra:
            z = node(("x", kind, p, q))
            if kind == "ff":       # flip p meets flip q
                flip[p] |= 1 << z
                flip[q] |= 1 << z
            elif kind == "fh":     # flip p meets path side q
                flip[p] |= 1 << z
                path[q] |= 1 << z
    E = [0] * L
    F = [0] * L
    for k in range(1, L + 1):
        if word[k - 1] == "E":
            E[k - 1], F[k - 1] = path[k], flip[k]
        else:
            F[k - 1], E[k - 1] = path[k], flip[k]
    planted_path = tuple(2 * (k - 1) + (0 if word[k - 1] == "E" else 1) for k in range(1, L + 1))
    return (len(nodes), E, F, s, t), planted_path


def rigid(L):
    word = "".join("E" if k % 2 == 1 else "F" for k in range(1, L + 1))
    return planted(word)


import sw  # noqa: E402


def rigid_variants(L):
    inst, P = rigid(L)
    yield "R", inst
    N, E, F, s_, t = inst
    # Helly form: t in every flip side
    E2, F2 = list(E), list(F)
    for k in range(L):
        if P[k] & 1:
            E2[k] |= 1 << t
        else:
            F2[k] |= 1 << t
    yield "Rhelly", (N, E2, F2, s_, t)
    # one-node no-variants keeping P2
    for w in range(L):
        for typ in (0, 1):
            S = E if typ == 0 else F
            for x in sw.bits(S[w]):
                E3, F3 = list(E), list(F)
                if typ == 0:
                    E3[w] &= ~(1 << x)
                else:
                    F3[w] &= ~(1 << x)
                inst3 = (N, E3, F3, s_, t)
                if sw.p2_ok(inst3):
                    yield "Rdel", inst3
    # t moved into a flip side
    for k in range(L - 1):
        E4, F4 = list(E), list(F)
        if P[L - 1] & 1:
            F4[L - 1] &= ~(1 << t)
        else:
            E4[L - 1] &= ~(1 << t)
        if P[k] & 1:
            E4[k] |= 1 << t
        else:
            F4[k] |= 1 << t
        inst4 = (N, E4, F4, s_, t)
        if sw.p2_ok(inst4):
            yield "Rtflip", inst4


