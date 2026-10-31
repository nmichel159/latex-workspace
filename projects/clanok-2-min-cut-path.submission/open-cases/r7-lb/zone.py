"""Agent r7-lb: zone families  E^k F^k  (and variants) with a 0/1 matrix of cross contacts (r7-lb.md Section 3.3).

Path word E^k F^k: members a_0..a_{k-1} (E-sides), b_0..b_{k-1} (F-sides) at positions 0..2k-1; the planted path is
s, E_{a_0}, .., E_{a_{k-1}}, F_{b_0}, .., F_{b_{k-1}}, t.
Contacts (P2) of incomparable pairs:   a_i a_j: FF (a node in F_{a_i} and F_{a_j})    [aa]
                                       b_i b_j: EE (a node in E_{b_i} and E_{b_j})    [bb]
                                       a_i b_j: EE if M[i][j] == 'E' else FF            [ab]
Extra switches (nx) are added after the members, with contacts chosen by the genome (default EE/FF/R).
A genome is the dict of design.py; zone_genome() fills in the contacts.

usage (module): from zone import zone_genome ; g = zone_genome(k, M) ; I = design.build(g)
"""
import os
import sys
import random

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import design
import lbcore


def zone_genome(k, M, aa="FF", bb="EE", word=None, nx=0, rel=None, extra_contacts=None):
    word = word or ("E" * k + "F" * k)
    g = design.new_genome(word, nx, default="EE")
    n = len(word)
    for x in range(n):
        for y in range(x + 1, n):
            if word[x] == "E" and word[y] == "E":
                kind = aa
            elif word[x] == "F" and word[y] == "F":
                kind = bb
            else:
                i = x if word[x] == "E" else y
                j = y if word[y] == "F" else x
                kind = "EE" if M[i][j - k] == "E" else "FF"
            g["contact"][design.pair_key(x, y)] = kind
    if rel:
        g["rel"] = list(rel)
    if extra_contacts:
        for key, v in extra_contacts.items():
            g["contact"][key] = v
    return g


def random_matrix(k, rng, p=0.5):
    return [["E" if rng.random() < p else "F" for _ in range(k)] for _ in range(k)]


def evaluate(g, cap=10, state_cap=300000):
    I = design.build(g)
    if I is None:
        return None
    pairs = lbcore.valid_pairs(I, state_cap=state_cap)
    if not pairs:
        return dict(total=None, m=I.m)
    r = lbcore.mincost(I, cap=cap, pairs=pairs)
    r["m"] = I.m
    r["npairs"] = len(pairs)
    return r


if __name__ == "__main__":
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    for k in range(3, 9):
        res = []
        for rep in range(6):
            M = random_matrix(k, rng)
            g = zone_genome(k, M)
            r = evaluate(g)
            res.append((r["total"], r.get("npairs")))
        print("k", k, res, flush=True)
