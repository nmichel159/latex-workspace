"""Gadget search, part C: uniform witness rules for the encoding E3 (2CH with classes) of CNF formulas.

E3 (gadgets.enc_e3): clause nodes m_0 = s, ..., m_k = t in series; one switch per literal occurrence; the clause edge
{m_(j-1), m_j} is its E-side (positive literal; live in E-mode = literal true) or its F-side (negative literal; live
in F-mode = literal true); the other side is empty (dead); the occurrences of a variable are tied.  E3(F) is a
yes-instance iff F is satisfiable.  Every pair of occurrences of different variables without a common node needs a
witness; by Proposition W' (report Section 5.2) private witnesses in the class of u ('low': a bottom joined to both)
or of v ('up') are the weakest possible repairs.  Adding witnesses never removes solutions, so satisfiable formulas
stay satisfiable under every rule; a rule is *valid on F* if E3(F) + witnesses stays a no-instance for unsatisfiable F.
A rule decides the direction of every pair from local data only:
  low, up        all lower / all upper
  dead-low       same sign: the common dead side (pos-pos 'up', neg-neg 'low'); mixed: 'low'
  dead-up        same sign as above; mixed: 'up'
  early-live     same sign as above; mixed: the witness goes on the live side of the occurrence in the earlier clause
  late-live      same sign as above; mixed: live side of the later clause
  parity         same sign as above; mixed: 'low' iff the clause distance is even
Usage: python gadgets_c.py SEED COUNT NVMAX MMAX"""
import sys
import random
import json
from common import zz, HERE
from gadgets import enc_e3, random_unsat, satisfiable
from gadgets_b import completion_bt


def occurrences(clauses):
    occ = []
    for j, cl in enumerate(clauses, 1):
        for lit in cl:
            occ.append((j, lit))
    return occ


def rule_dir(rule, oa, ob):
    (ja, la), (jb, lb) = oa, ob
    pa, pb = la > 0, lb > 0
    if rule == "low":
        return "low"
    if rule == "up":
        return "up"
    if pa == pb:
        return "up" if pa else "low"
    if rule == "dead-low":
        return "low"
    if rule == "dead-up":
        return "up"
    pos_clause = ja if pa else jb
    neg_clause = jb if pa else ja
    if rule == "early-live":
        # live side of the positive literal is E ('low'), of the negative one is F ('up')
        return "low" if pos_clause < neg_clause else "up"
    if rule == "late-live":
        return "low" if pos_clause > neg_clause else "up"
    if rule == "parity":
        return "low" if (abs(ja - jb) % 2 == 0) else "up"
    raise ValueError(rule)


RULES = ["low", "up", "dead-low", "dead-up", "early-live", "late-live", "parity"]


def apply_rule(nv, clauses, rule):
    z, names = enc_e3(nv, clauses)
    occ = occurrences(clauses)
    # switch elements in the ZZ form: names ('m', w) -> occurrence w (dc-general families.to_inst naming)
    sw = {}
    for i, nm in enumerate(names):
        if isinstance(nm, tuple) and nm[0] == "m":
            sw[i] = nm[1]
    pairs = z.p2_bad()
    c = []
    for x, y in pairs:
        assert x in sw and y in sw, "P2 violation outside the switches"
        c.append(rule_dir(rule, occ[sw[x]], occ[sw[y]]))
    zc = completion_bt(z, pairs, c)
    assert not zc.p2_bad()
    return z, zc


if __name__ == "__main__":
    seed, count, nvmax, mmax = (int(a) for a in sys.argv[1:5])
    rng = random.Random(seed)
    fails = {r: 0 for r in RULES}
    smallest = {r: None for r in RULES}
    tested = 0
    out = open("%s/runs/gadgets-C-%d.jsonl" % (HERE, seed), "w")
    formulas = [(2, [[1, 2], [1, -2], [-1, 2], [-1, -2]])]
    for i in range(count):
        nv = rng.randint(2, nvmax)
        width = rng.choice([2, 3]) if nv >= 3 else 2
        m = rng.randint(3, mmax)
        formulas.append((nv, random_unsat(rng, nv, m, width)))
    for nv, cls in formulas:
        tested += 1
        rec = {"nv": nv, "clauses": cls}
        for r in RULES:
            z, zc = apply_rule(nv, cls, r)
            bad = zz.exact_dfs(zc)[0]
            rec[r] = bad
            if bad:
                fails[r] += 1
                size = (len(cls), sum(len(c) for c in cls))
                if smallest[r] is None or size < smallest[r][0]:
                    smallest[r] = (size, nv, cls)
        out.write(json.dumps(rec) + "\n")
    print("seed %d: %d unsatisfiable formulas (nv <= %d, clauses <= %d)" % (seed, tested, nvmax, mmax))
    for r in RULES:
        print("  rule %-11s invalid on %4d   smallest failing formula %s" % (r, fails[r], smallest[r]), flush=True)
